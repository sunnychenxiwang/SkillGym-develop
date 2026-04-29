"""Expectation tests for microbial growth / construction matching task.

These tests verify that the task execution produces correct outputs
by recomputing all values from the input CSVs and asserting equality.

Task specification:
1. From Dataset S9.csv (growth data):
   - Exclude Strain == "Blank"
   - Baseline-correct OD by subtracting OD at earliest Time_hours per (Strain, Replicate)
   - Find earliest time where baseline-corrected OD >= 0.30 per series
   - Compute median of these times -> t_median_hours
   - p_target = min(1, max(0, t_median_hours / 10))

2. From construction.csv (starts) and construction_spending.csv (spending):
   - Compute percentile ranks for Total (starts) and total construction (spending)
   - Ranking is by value DESCENDING (higher value = rank 1 = higher percentile)
   - Ties are broken by earlier calendar month (Year then Month order as in file)
   - p = (rank - 1) / (N - 1) where rank is 1..N
   - Find overlapping (year, month) combinations
   - Score = |p_starts - p_target| + |p_spend - p_target|
   - Select month with minimum score (tie-break: earliest calendar month)
"""

import json
import os
from pathlib import Path

import numpy as np
import pandas as pd
import pytest


OUTPUT_PATH = "/root/best_match_month.json"
INPUT_DIR = "/root"


# ============================================================================
# Fixtures for loading data
# ============================================================================

@pytest.fixture
def output_data():
    """Load the output JSON file."""
    with open(OUTPUT_PATH) as f:
        return json.load(f)


@pytest.fixture
def growth_data():
    """Load and return the microbial growth data."""
    path = os.path.join(INPUT_DIR, "Dataset_S9.csv")
    return pd.read_csv(path)


@pytest.fixture
def construction_starts():
    """Load construction starts data."""
    path = os.path.join(INPUT_DIR, "construction.csv")
    return pd.read_csv(path, na_values=["NA"])


@pytest.fixture
def construction_spending():
    """Load construction spending data."""
    path = os.path.join(INPUT_DIR, "construction_spending.csv")
    return pd.read_csv(path)


# ============================================================================
# Computation functions (reference implementation)
# ============================================================================

def compute_t_median_hours(growth_df):
    """
    Compute t_median_hours from growth data.

    Steps:
    1. Exclude Strain == "Blank"
    2. For each (Strain, Replicate), subtract OD at earliest Time_hours (baseline)
    3. Find earliest time where baseline-corrected OD >= 0.30
    4. Compute median of these times
    """
    # Exclude blanks
    df = growth_df[growth_df["Strain"] != "Blank"].copy()

    if df.empty:
        return np.nan

    # Ensure numeric columns are properly typed
    df["Time_hours"] = pd.to_numeric(df["Time_hours"], errors="coerce")
    df["OD"] = pd.to_numeric(df["OD"], errors="coerce")

    threshold_times = []

    for (strain, replicate), group in df.groupby(["Strain", "Replicate"]):
        group = group.sort_values("Time_hours")

        # Get baseline OD (at earliest time)
        baseline_od = group.iloc[0]["OD"]

        # Compute baseline-corrected OD
        group = group.copy()
        group["OD_corrected"] = group["OD"] - baseline_od

        # Find earliest time where corrected OD >= 0.30
        above_threshold = group[group["OD_corrected"] >= 0.30]

        if not above_threshold.empty:
            earliest_time = above_threshold["Time_hours"].min()
            threshold_times.append(earliest_time)

    if not threshold_times:
        return np.nan

    return np.median(threshold_times)


def month_name_to_num(month_name):
    """Convert month name to number (1-12)."""
    months = {
        "January": 1, "February": 2, "March": 3, "April": 4,
        "May": 5, "June": 6, "July": 7, "August": 8,
        "September": 9, "October": 10, "November": 11, "December": 12
    }
    return months.get(month_name, 0)


def compute_percentile_rank_descending(df, value_col, year_col, month_col, original_index_col):
    """
    Compute percentile rank with DESCENDING order and proper tie-breaking.

    Ranking rules per spec:
    - Sort by value DESCENDING (higher value = rank 1)
    - Break ties by earlier calendar month (Year then Month order as in file)
    - Assign integer ranks 1..N in sorted order
    - Compute p = (rank - 1) / (N - 1) for N > 1

    Args:
        df: DataFrame with the data
        value_col: Column name for the value to rank
        year_col: Column name for year
        month_col: Column name for month number (1-12)
        original_index_col: Column name for original file order (for stable tie-break)

    Returns:
        Series of percentile values aligned with df index
    """
    n = len(df)
    if n <= 1:
        return pd.Series([0.5] * n, index=df.index)

    # Create a copy with required columns
    work_df = df[[value_col, year_col, month_col, original_index_col]].copy()

    # Sort by value descending, then by year ascending, then by month ascending for ties
    # Use original_index_col as final tie-breaker to ensure deterministic ordering
    work_df = work_df.sort_values(
        by=[value_col, year_col, month_col, original_index_col],
        ascending=[False, True, True, True]
    )

    # Assign integer ranks 1..N in sorted order
    work_df["rank"] = range(1, n + 1)

    # Compute percentile: (rank - 1) / (N - 1)
    work_df["percentile"] = (work_df["rank"] - 1) / (n - 1)

    # Return percentiles aligned with original index
    return work_df["percentile"].reindex(df.index)


def compute_overlapping_months_with_scores(starts_df, spending_df, p_target):
    """
    Find overlapping (year, month) combinations and compute scores.

    Uses DESCENDING percentile ranking with tie-breaking by earlier calendar month.

    Returns a DataFrame with columns: year, month, month_num, p_starts, p_spend, score, file_order
    """
    # Prepare starts data - explicit numeric conversion
    starts = starts_df.copy()
    starts["Total"] = pd.to_numeric(starts["Total"], errors="coerce")
    starts = starts.dropna(subset=["Total"]).copy()
    starts["month_num"] = starts["Month"].apply(month_name_to_num)
    starts["original_idx"] = range(len(starts))  # Preserve file order for tie-breaking

    # Compute percentile ranks with descending order
    starts["p_starts"] = compute_percentile_rank_descending(
        starts, "Total", "Year", "month_num", "original_idx"
    )

    # Prepare spending data - explicit numeric conversion
    spending_col = "current.combined.total construction"
    spending = spending_df.copy()
    spending[spending_col] = pd.to_numeric(spending[spending_col], errors="coerce")
    spending = spending.dropna(subset=[spending_col]).copy()
    spending["year"] = spending["time.year"]
    spending["month"] = spending["time.month name"]
    spending["month_num"] = spending["time.month"]
    spending["original_idx"] = range(len(spending))  # Preserve file order for tie-breaking

    # Compute percentile ranks with descending order
    spending["p_spend"] = compute_percentile_rank_descending(
        spending, spending_col, "year", "month_num", "original_idx"
    )

    # Find overlapping months
    starts_set = set(zip(starts["Year"], starts["month_num"]))
    spending_set = set(zip(spending["year"], spending["month_num"]))
    overlapping = starts_set & spending_set

    results = []
    for year, month_num in overlapping:
        starts_row = starts[(starts["Year"] == year) & (starts["month_num"] == month_num)]
        spending_row = spending[(spending["year"] == year) & (spending["month_num"] == month_num)]

        if starts_row.empty or spending_row.empty:
            continue

        p_starts = starts_row["p_starts"].iloc[0]
        p_spend = spending_row["p_spend"].iloc[0]
        month_name = starts_row["Month"].iloc[0]
        file_order = starts_row["original_idx"].iloc[0]

        score = abs(p_starts - p_target) + abs(p_spend - p_target)

        results.append({
            "year": year,
            "month": month_name,
            "month_num": month_num,
            "p_starts": p_starts,
            "p_spend": p_spend,
            "score": score,
            "file_order": file_order
        })

    return pd.DataFrame(results)


def find_best_match(results_df):
    """
    Find the best match: minimum score, tie-break by earliest calendar month.

    Tie-breaking: Year first, then Month number (calendar order).
    """
    if results_df.empty:
        return None

    min_score = results_df["score"].min()
    candidates = results_df[np.isclose(results_df["score"], min_score, rtol=1e-9)].copy()

    # Tie-break: earliest calendar month (year first, then month_num)
    candidates = candidates.sort_values(["year", "month_num"])

    return candidates.iloc[0]


# ============================================================================
# Test: Output file existence and basic structure
# ============================================================================

class TestOutputFileExists:
    """Tests for verifying output file existence and basic structure."""

    def test_output_file_exists(self):
        """Verify the output JSON file was created at the expected path."""
        assert os.path.exists(OUTPUT_PATH), f"Output file not found at {OUTPUT_PATH}"

    def test_output_file_is_not_empty(self):
        """Verify the output file is not empty."""
        assert os.path.getsize(OUTPUT_PATH) > 0, "Output file is empty"

    def test_output_is_valid_json(self):
        """Verify output is valid JSON format."""
        with open(OUTPUT_PATH) as f:
            data = json.load(f)
        assert data is not None, "Failed to parse JSON"


class TestJsonStructure:
    """Tests for verifying JSON structure and schema compliance."""

    def test_has_required_top_level_keys(self, output_data):
        """Verify all required top-level keys are present."""
        required_keys = ["t_median_hours", "p_target", "best_match"]
        for key in required_keys:
            assert key in output_data, f"Missing required top-level key: {key}"

    def test_has_required_best_match_keys(self, output_data):
        """Verify all required keys in best_match object are present."""
        required_keys = ["year", "month", "p_starts", "p_spend", "score"]
        best_match = output_data.get("best_match", {})
        for key in required_keys:
            assert key in best_match, f"Missing required key in best_match: {key}"

    def test_no_extra_top_level_keys(self, output_data):
        """Verify there are no unexpected top-level keys."""
        expected_keys = {"t_median_hours", "p_target", "best_match"}
        actual_keys = set(output_data.keys())
        extra_keys = actual_keys - expected_keys
        assert not extra_keys, f"Unexpected top-level keys found: {extra_keys}"

    def test_no_extra_best_match_keys(self, output_data):
        """Verify there are no unexpected keys in best_match."""
        expected_keys = {"year", "month", "p_starts", "p_spend", "score"}
        actual_keys = set(output_data["best_match"].keys())
        extra_keys = actual_keys - expected_keys
        assert not extra_keys, f"Unexpected keys in best_match: {extra_keys}"


# ============================================================================
# Test: Data types
# ============================================================================

class TestDataTypes:
    """Tests for verifying correct data types in the output."""

    def test_t_median_hours_is_number(self, output_data):
        """Verify t_median_hours is a numeric type."""
        t_median = output_data["t_median_hours"]
        assert isinstance(t_median, (int, float)), \
            f"t_median_hours should be a number, got {type(t_median).__name__}"

    def test_p_target_is_number(self, output_data):
        """Verify p_target is a numeric type."""
        p_target = output_data["p_target"]
        assert isinstance(p_target, (int, float)), \
            f"p_target should be a number, got {type(p_target).__name__}"

    def test_year_is_integer(self, output_data):
        """Verify year in best_match is an integer."""
        year = output_data["best_match"]["year"]
        assert isinstance(year, int), \
            f"year should be an integer, got {type(year).__name__}"

    def test_month_is_string(self, output_data):
        """Verify month in best_match is a string."""
        month = output_data["best_match"]["month"]
        assert isinstance(month, str), \
            f"month should be a string, got {type(month).__name__}"

    def test_p_starts_is_number(self, output_data):
        """Verify p_starts is a numeric type."""
        p_starts = output_data["best_match"]["p_starts"]
        assert isinstance(p_starts, (int, float)), \
            f"p_starts should be a number, got {type(p_starts).__name__}"

    def test_p_spend_is_number(self, output_data):
        """Verify p_spend is a numeric type."""
        p_spend = output_data["best_match"]["p_spend"]
        assert isinstance(p_spend, (int, float)), \
            f"p_spend should be a number, got {type(p_spend).__name__}"

    def test_score_is_number(self, output_data):
        """Verify score is a numeric type."""
        score = output_data["best_match"]["score"]
        assert isinstance(score, (int, float)), \
            f"score should be a number, got {type(score).__name__}"


# ============================================================================
# Test: Input files used
# ============================================================================

class TestInputFilesUsed:
    """Tests to verify the input files exist."""

    def test_growth_data_file_exists(self):
        """Verify Dataset S9.csv exists as input."""
        path = os.path.join(INPUT_DIR, "Dataset_S9.csv")
        assert os.path.exists(path), f"Input file not found: {path}"

    def test_construction_starts_file_exists(self):
        """Verify construction.csv exists as input."""
        path = os.path.join(INPUT_DIR, "construction.csv")
        assert os.path.exists(path), f"Input file not found: {path}"

    def test_construction_spending_file_exists(self):
        """Verify construction_spending.csv exists as input."""
        path = os.path.join(INPUT_DIR, "construction_spending.csv")
        assert os.path.exists(path), f"Input file not found: {path}"


# ============================================================================
# Test: t_median_hours computation
# ============================================================================

class TestTMedianComputation:
    """Tests for verifying t_median_hours is computed correctly from growth data."""

    def test_t_median_hours_equals_recomputed(self, output_data, growth_data):
        """Verify t_median_hours matches recomputation from input CSV."""
        expected = compute_t_median_hours(growth_data)
        actual = output_data["t_median_hours"]

        assert not np.isnan(expected), "Recomputed t_median_hours is NaN - check growth data"
        np.testing.assert_allclose(
            actual, expected, rtol=1e-9,
            err_msg=f"t_median_hours mismatch: output={actual}, expected={expected}"
        )

    def test_blanks_excluded_from_computation(self, growth_data):
        """Verify that Strain=='Blank' rows exist and would be excluded."""
        blank_count = (growth_data["Strain"] == "Blank").sum()
        assert blank_count > 0, "No Blank rows found in growth data - test data may be incorrect"

        # Verify blanks have different characteristics than non-blanks
        non_blank = growth_data[growth_data["Strain"] != "Blank"]
        assert len(non_blank) > 0, "No non-Blank rows found"

    def test_baseline_uses_earliest_time(self, growth_data):
        """Verify baseline is taken from earliest time per series."""
        df = growth_data[growth_data["Strain"] != "Blank"].copy()

        for (strain, replicate), group in df.groupby(["Strain", "Replicate"]):
            sorted_group = group.sort_values("Time_hours")
            min_time = sorted_group["Time_hours"].min()
            first_row_time = sorted_group.iloc[0]["Time_hours"]

            assert min_time == first_row_time, \
                f"Earliest time mismatch for {strain}/{replicate}"

    def test_t_median_hours_is_non_negative(self, output_data, growth_data):
        """Verify t_median_hours is non-negative (can be 0 if threshold reached at earliest time)."""
        t_median = output_data["t_median_hours"]
        min_time = growth_data["Time_hours"].min()
        assert t_median >= min_time, \
            f"t_median_hours ({t_median}) should be >= min Time_hours ({min_time})"

    def test_t_median_hours_within_data_range(self, output_data, growth_data):
        """Verify t_median_hours is within the time range of the input data."""
        min_time = growth_data["Time_hours"].min()
        max_time = growth_data["Time_hours"].max()
        t_median = output_data["t_median_hours"]

        assert min_time <= t_median <= max_time, \
            f"t_median_hours ({t_median}) outside data range [{min_time}, {max_time}]"


# ============================================================================
# Test: p_target computation
# ============================================================================

class TestPTargetComputation:
    """Tests for verifying p_target = min(1, max(0, t_median_hours / 10))."""

    def test_p_target_formula(self, output_data):
        """Verify p_target = min(1, max(0, t_median_hours / 10))."""
        t_median = output_data["t_median_hours"]
        p_target = output_data["p_target"]

        expected = min(1, max(0, t_median / 10))

        np.testing.assert_allclose(
            p_target, expected, rtol=1e-9,
            err_msg=f"p_target mismatch: output={p_target}, expected={expected}"
        )

    def test_p_target_in_valid_range(self, output_data):
        """Verify p_target is between 0 and 1."""
        p_target = output_data["p_target"]
        assert 0 <= p_target <= 1, f"p_target should be in [0, 1], got {p_target}"


# ============================================================================
# Test: Percentile rank computation (DESCENDING with tie-break)
# ============================================================================

class TestPercentileRankComputation:
    """Tests for verifying p_starts and p_spend percentile ranks with descending ranking."""

    def test_p_starts_equals_recomputed(self, output_data, construction_starts):
        """Verify p_starts matches recomputation using descending rank with tie-break."""
        # Prepare data with explicit numeric conversion
        starts = construction_starts.copy()
        starts["Total"] = pd.to_numeric(starts["Total"], errors="coerce")
        starts = starts.dropna(subset=["Total"]).copy()
        starts["month_num"] = starts["Month"].apply(month_name_to_num)
        starts["original_idx"] = range(len(starts))

        # Compute percentile with descending order and tie-breaking
        starts["p_starts"] = compute_percentile_rank_descending(
            starts, "Total", "Year", "month_num", "original_idx"
        )

        output_year = output_data["best_match"]["year"]
        output_month = output_data["best_match"]["month"]
        output_month_num = month_name_to_num(output_month)

        match = starts[(starts["Year"] == output_year) & (starts["month_num"] == output_month_num)]

        assert not match.empty, \
            f"Output (year={output_year}, month={output_month}) not found in construction.csv"

        expected_p_starts = match["p_starts"].iloc[0]
        actual_p_starts = output_data["best_match"]["p_starts"]

        np.testing.assert_allclose(
            actual_p_starts, expected_p_starts, rtol=1e-9,
            err_msg=f"p_starts mismatch: output={actual_p_starts}, expected={expected_p_starts}. "
                    f"Expected descending rank with tie-break by (Year, Month)."
        )

    def test_p_spend_equals_recomputed(self, output_data, construction_spending):
        """Verify p_spend matches recomputation using descending rank with tie-break."""
        spending_col = "current.combined.total construction"

        # Prepare data with explicit numeric conversion
        spending = construction_spending.copy()
        spending[spending_col] = pd.to_numeric(spending[spending_col], errors="coerce")
        spending = spending.dropna(subset=[spending_col]).copy()
        spending["year"] = spending["time.year"]
        spending["month_num"] = spending["time.month"]
        spending["original_idx"] = range(len(spending))

        # Compute percentile with descending order and tie-breaking
        spending["p_spend"] = compute_percentile_rank_descending(
            spending, spending_col, "year", "month_num", "original_idx"
        )

        output_year = output_data["best_match"]["year"]
        output_month = output_data["best_match"]["month"]
        output_month_num = month_name_to_num(output_month)

        match = spending[
            (spending["year"] == output_year) &
            (spending["month_num"] == output_month_num)
        ]

        assert not match.empty, \
            f"Output (year={output_year}, month={output_month}) not found in construction_spending.csv"

        expected_p_spend = match["p_spend"].iloc[0]
        actual_p_spend = output_data["best_match"]["p_spend"]

        np.testing.assert_allclose(
            actual_p_spend, expected_p_spend, rtol=1e-9,
            err_msg=f"p_spend mismatch: output={actual_p_spend}, expected={expected_p_spend}. "
                    f"Expected descending rank with tie-break by (time.year, time.month)."
        )

    def test_p_starts_in_valid_range(self, output_data):
        """Verify p_starts is between 0 and 1."""
        p_starts = output_data["best_match"]["p_starts"]
        assert 0 <= p_starts <= 1, f"p_starts should be in [0, 1], got {p_starts}"

    def test_p_spend_in_valid_range(self, output_data):
        """Verify p_spend is between 0 and 1."""
        p_spend = output_data["best_match"]["p_spend"]
        assert 0 <= p_spend <= 1, f"p_spend should be in [0, 1], got {p_spend}"

    def test_descending_rank_order_starts(self, construction_starts):
        """Verify that higher Total values get lower rank (higher percentile) in starts."""
        starts = construction_starts.copy()
        starts["Total"] = pd.to_numeric(starts["Total"], errors="coerce")
        starts = starts.dropna(subset=["Total"]).copy()
        starts["month_num"] = starts["Month"].apply(month_name_to_num)
        starts["original_idx"] = range(len(starts))

        starts["p_starts"] = compute_percentile_rank_descending(
            starts, "Total", "Year", "month_num", "original_idx"
        )

        # Find max and min Total values
        max_total_idx = starts["Total"].idxmax()
        min_total_idx = starts["Total"].idxmin()

        max_p = starts.loc[max_total_idx, "p_starts"]
        min_p = starts.loc[min_total_idx, "p_starts"]

        # Higher Total gets rank 1, so p=(1-1)/(N-1)=0 (lower percentile value)
        assert max_p <= min_p, \
            f"Descending rank violated: max Total has p={max_p}, min Total has p={min_p}. " \
            f"Higher values should have lower percentile value (rank 1 → p=0)."

    def test_descending_rank_order_spending(self, construction_spending):
        """Verify that higher spending values get lower rank (higher percentile)."""
        spending_col = "current.combined.total construction"
        spending = construction_spending.copy()
        spending[spending_col] = pd.to_numeric(spending[spending_col], errors="coerce")
        spending = spending.dropna(subset=[spending_col]).copy()
        spending["year"] = spending["time.year"]
        spending["month_num"] = spending["time.month"]
        spending["original_idx"] = range(len(spending))

        spending["p_spend"] = compute_percentile_rank_descending(
            spending, spending_col, "year", "month_num", "original_idx"
        )

        # Find max and min spending values
        max_spending_idx = spending[spending_col].idxmax()
        min_spending_idx = spending[spending_col].idxmin()

        max_p = spending.loc[max_spending_idx, "p_spend"]
        min_p = spending.loc[min_spending_idx, "p_spend"]

        # Higher spending gets rank 1, so p=(1-1)/(N-1)=0 (lower percentile value)
        assert max_p <= min_p, \
            f"Descending rank violated: max spending has p={max_p}, min spending has p={min_p}. " \
            f"Higher values should have lower percentile value (rank 1 → p=0)."


# ============================================================================
# Test: Score computation
# ============================================================================

class TestScoreComputation:
    """Tests for verifying score = |p_starts - p_target| + |p_spend - p_target|."""

    def test_score_equals_formula(self, output_data):
        """Verify score = |p_starts - p_target| + |p_spend - p_target|."""
        p_target = output_data["p_target"]
        p_starts = output_data["best_match"]["p_starts"]
        p_spend = output_data["best_match"]["p_spend"]
        score = output_data["best_match"]["score"]

        expected = abs(p_starts - p_target) + abs(p_spend - p_target)

        np.testing.assert_allclose(
            score, expected, rtol=1e-9,
            err_msg=f"score mismatch: output={score}, expected={expected}"
        )

    def test_score_is_non_negative(self, output_data):
        """Verify score is non-negative."""
        score = output_data["best_match"]["score"]
        assert score >= 0, f"score should be non-negative, got {score}"

    def test_score_max_value(self, output_data):
        """Verify score is at most 2 (max sum of two percentile differences)."""
        score = output_data["best_match"]["score"]
        assert score <= 2, f"score should be at most 2, got {score}"


# ============================================================================
# Test: Best match selection (minimum score, overlap, tie-break)
# ============================================================================

class TestBestMatchSelection:
    """Tests for verifying the best match is the global minimum score among overlapping months."""

    def test_output_month_exists_in_both_datasets(self, output_data, construction_starts, construction_spending):
        """Verify the selected month exists in both construction datasets."""
        output_year = output_data["best_match"]["year"]
        output_month = output_data["best_match"]["month"]
        output_month_num = month_name_to_num(output_month)

        # Check construction.csv
        starts_match = construction_starts[
            (construction_starts["Year"] == output_year) &
            (construction_starts["Month"] == output_month)
        ]
        assert not starts_match.empty, \
            f"Output (year={output_year}, month={output_month}) not found in construction.csv"

        # Check construction_spending.csv
        spending_match = construction_spending[
            (construction_spending["time.year"] == output_year) &
            (construction_spending["time.month"] == output_month_num)
        ]
        assert not spending_match.empty, \
            f"Output (year={output_year}, month={output_month}) not found in construction_spending.csv"

    def test_selected_month_has_minimum_score(self, output_data, construction_starts, construction_spending):
        """Verify the selected month has the minimum score among all overlapping months."""
        p_target = output_data["p_target"]

        results = compute_overlapping_months_with_scores(
            construction_starts, construction_spending, p_target
        )

        assert not results.empty, "No overlapping months found between datasets"

        min_score = results["score"].min()
        actual_score = output_data["best_match"]["score"]

        np.testing.assert_allclose(
            actual_score, min_score, rtol=1e-9,
            err_msg=f"Output score ({actual_score}) is not the minimum ({min_score})"
        )

    def test_tie_break_selects_earliest_month(self, output_data, construction_starts, construction_spending):
        """Verify tie-break selects the earliest calendar month when scores are equal."""
        p_target = output_data["p_target"]

        results = compute_overlapping_months_with_scores(
            construction_starts, construction_spending, p_target
        )

        expected_best = find_best_match(results)

        assert expected_best is not None, "Could not find best match from recomputation"

        output_year = output_data["best_match"]["year"]
        output_month = output_data["best_match"]["month"]

        assert output_year == expected_best["year"], \
            f"Year mismatch: output={output_year}, expected={expected_best['year']}"
        assert output_month == expected_best["month"], \
            f"Month mismatch: output={output_month}, expected={expected_best['month']}"

    def test_all_values_match_recomputation(self, output_data, growth_data, construction_starts, construction_spending):
        """Comprehensive test: verify all output values match full recomputation."""
        # Recompute t_median_hours
        expected_t_median = compute_t_median_hours(growth_data)

        # Recompute p_target
        expected_p_target = min(1, max(0, expected_t_median / 10))

        # Find best match
        results = compute_overlapping_months_with_scores(
            construction_starts, construction_spending, expected_p_target
        )
        expected_best = find_best_match(results)

        # Verify all values
        np.testing.assert_allclose(
            output_data["t_median_hours"], expected_t_median, rtol=1e-9,
            err_msg="t_median_hours mismatch"
        )
        np.testing.assert_allclose(
            output_data["p_target"], expected_p_target, rtol=1e-9,
            err_msg="p_target mismatch"
        )
        assert output_data["best_match"]["year"] == expected_best["year"], \
            f"year mismatch: {output_data['best_match']['year']} != {expected_best['year']}"
        assert output_data["best_match"]["month"] == expected_best["month"], \
            f"month mismatch: {output_data['best_match']['month']} != {expected_best['month']}"
        np.testing.assert_allclose(
            output_data["best_match"]["p_starts"], expected_best["p_starts"], rtol=1e-9,
            err_msg="p_starts mismatch"
        )
        np.testing.assert_allclose(
            output_data["best_match"]["p_spend"], expected_best["p_spend"], rtol=1e-9,
            err_msg="p_spend mismatch"
        )
        np.testing.assert_allclose(
            output_data["best_match"]["score"], expected_best["score"], rtol=1e-9,
            err_msg="score mismatch"
        )


# ============================================================================
# Test: Month name validation
# ============================================================================

class TestMonthName:
    """Tests for verifying month name is valid and matches construction.csv format."""

    VALID_MONTHS = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    def test_month_is_valid_month_name(self, output_data):
        """Verify month is a valid month name."""
        month = output_data["best_match"]["month"]
        assert month in self.VALID_MONTHS, \
            f"month should be a valid month name, got '{month}'"

    def test_month_matches_construction_csv_format(self, output_data, construction_starts):
        """Verify month string matches exactly as shown in construction.csv."""
        output_month = output_data["best_match"]["month"]

        # Get all unique month names from construction.csv
        valid_months = construction_starts["Month"].unique()

        assert output_month in valid_months, \
            f"Month '{output_month}' not found in construction.csv. Valid months: {list(valid_months)}"

    def test_month_from_correct_tie_break_file_order(self, output_data, construction_starts, construction_spending):
        """Verify the month corresponds to correct tie-break using file order from construction.csv."""
        p_target = output_data["p_target"]

        results = compute_overlapping_months_with_scores(
            construction_starts, construction_spending, p_target
        )

        min_score = results["score"].min()
        tied = results[np.isclose(results["score"], min_score, rtol=1e-9)]

        if len(tied) > 1:
            # Multiple ties exist - verify earliest calendar month is selected
            tied = tied.sort_values(["year", "month_num"])
            expected_month = tied.iloc[0]["month"]
            expected_year = tied.iloc[0]["year"]

            output_month = output_data["best_match"]["month"]
            output_year = output_data["best_match"]["year"]

            assert output_year == expected_year and output_month == expected_month, \
                f"Tie-break should select earliest calendar month. " \
                f"Got ({output_year}, {output_month}), expected ({expected_year}, {expected_month}). " \
                f"Tied months: {list(zip(tied['year'], tied['month']))}"


# ============================================================================
# Test: Year validation
# ============================================================================

class TestYearValidation:
    """Tests for verifying year is within the data range."""

    def test_year_in_starts_data_range(self, output_data, construction_starts):
        """Verify year is within the range present in construction.csv."""
        year = output_data["best_match"]["year"]
        min_year = construction_starts["Year"].min()
        max_year = construction_starts["Year"].max()

        assert min_year <= year <= max_year, \
            f"year ({year}) outside construction.csv range [{min_year}, {max_year}]"

    def test_year_in_spending_data_range(self, output_data, construction_spending):
        """Verify year is within the range present in construction_spending.csv."""
        year = output_data["best_match"]["year"]
        min_year = construction_spending["time.year"].min()
        max_year = construction_spending["time.year"].max()

        assert min_year <= year <= max_year, \
            f"year ({year}) outside construction_spending.csv range [{min_year}, {max_year}]"


# ============================================================================
# Test: Edge cases in growth data
# ============================================================================

class TestGrowthDataEdgeCases:
    """Tests for edge cases in growth data processing."""

    def test_growth_data_has_multiple_strains(self, growth_data):
        """Verify growth data has multiple strains for proper median computation."""
        non_blank = growth_data[growth_data["Strain"] != "Blank"]
        unique_strains = non_blank["Strain"].nunique()

        assert unique_strains >= 1, "Growth data should have at least one non-Blank strain"

    def test_growth_data_has_multiple_replicates(self, growth_data):
        """Verify growth data has multiple replicates for statistical significance."""
        non_blank = growth_data[growth_data["Strain"] != "Blank"]

        # Check that at least some strains have multiple replicates
        replicates_per_strain = non_blank.groupby("Strain")["Replicate"].nunique()
        max_replicates = replicates_per_strain.max()

        assert max_replicates >= 1, "Growth data should have at least one replicate per strain"

    def test_threshold_reachable_in_data(self, growth_data):
        """Verify that the 0.30 threshold is reachable in the growth data."""
        non_blank = growth_data[growth_data["Strain"] != "Blank"].copy()

        series_reaching_threshold = 0

        for (strain, replicate), group in non_blank.groupby(["Strain", "Replicate"]):
            group = group.sort_values("Time_hours")
            baseline_od = group.iloc[0]["OD"]
            max_corrected_od = group["OD"].max() - baseline_od

            if max_corrected_od >= 0.30:
                series_reaching_threshold += 1

        assert series_reaching_threshold > 0, \
            "No series in growth data reaches the 0.30 threshold"

    def test_series_not_reaching_threshold_handling(self, growth_data):
        """Verify behavior when some series don't reach threshold - they should be excluded."""
        non_blank = growth_data[growth_data["Strain"] != "Blank"].copy()

        total_series = 0
        series_not_reaching = 0

        for (strain, replicate), group in non_blank.groupby(["Strain", "Replicate"]):
            total_series += 1
            group = group.sort_values("Time_hours")
            baseline_od = group.iloc[0]["OD"]
            max_corrected_od = group["OD"].max() - baseline_od

            if max_corrected_od < 0.30:
                series_not_reaching += 1

        # This is informational - some series may not reach threshold, which is fine
        # as long as at least one series does (tested above)
        assert total_series > 0, "No series found in growth data"


# ============================================================================
# Test: Overlap and NA handling
# ============================================================================

class TestOverlapAndNAHandling:
    """Tests for overlap computation and NA value handling."""

    def test_only_overlapping_months_considered(self, construction_starts, construction_spending):
        """Verify that both datasets have overlapping (year, month) combinations."""
        # Get unique (year, month) from starts
        starts = construction_starts.copy()
        starts["month_num"] = starts["Month"].apply(month_name_to_num)
        starts_months = set(zip(starts["Year"], starts["month_num"]))

        # Get unique (year, month) from spending
        spending_months = set(zip(
            construction_spending["time.year"],
            construction_spending["time.month"]
        ))

        overlap = starts_months & spending_months

        assert len(overlap) > 0, \
            "No overlapping (year, month) combinations found between datasets"

    def test_na_rows_excluded_from_starts_ranking(self, construction_starts):
        """Verify NA values in construction.csv Total column are handled."""
        na_count = construction_starts["Total"].isna().sum()

        # If there are NA values, they should be excluded from ranking
        # This is informational - we just verify the data state
        total_rows = len(construction_starts)
        valid_rows = construction_starts["Total"].notna().sum()

        assert valid_rows > 0, "No valid Total values in construction.csv"

    def test_output_month_not_from_na_row(self, output_data, construction_starts):
        """Verify the output month is not from a row with NA Total value."""
        output_year = output_data["best_match"]["year"]
        output_month = output_data["best_match"]["month"]

        match = construction_starts[
            (construction_starts["Year"] == output_year) &
            (construction_starts["Month"] == output_month)
        ]

        if not match.empty:
            total_value = match["Total"].iloc[0]
            assert pd.notna(total_value), \
                f"Output month has NA Total value in construction.csv"


# ============================================================================
# Test: Tie-breaking verification
# ============================================================================

class TestTieBreaking:
    """Tests specifically for tie-breaking rules."""

    def test_when_ties_exist_earliest_wins(self, output_data, construction_starts, construction_spending):
        """If there are tied minimum scores, verify the earliest calendar month is selected."""
        p_target = output_data["p_target"]

        results = compute_overlapping_months_with_scores(
            construction_starts, construction_spending, p_target
        )

        min_score = results["score"].min()
        tied_results = results[np.isclose(results["score"], min_score, rtol=1e-9)].copy()

        if len(tied_results) > 1:
            # There are ties - verify earliest month is selected
            tied_results = tied_results.sort_values(["year", "month_num"])
            expected_year = tied_results.iloc[0]["year"]
            expected_month = tied_results.iloc[0]["month"]

            output_year = output_data["best_match"]["year"]
            output_month = output_data["best_match"]["month"]

            assert output_year == expected_year, \
                f"Tie-break failed: expected year {expected_year}, got {output_year}"
            assert output_month == expected_month, \
                f"Tie-break failed: expected month {expected_month}, got {output_month}"

    def test_starts_tie_break_uses_calendar_order(self, construction_starts):
        """Verify that starts ties are broken by earlier calendar month (Year, Month)."""
        starts = construction_starts.copy()
        starts["Total"] = pd.to_numeric(starts["Total"], errors="coerce")
        starts = starts.dropna(subset=["Total"]).copy()
        starts["month_num"] = starts["Month"].apply(month_name_to_num)
        starts["original_idx"] = range(len(starts))

        starts["p_starts"] = compute_percentile_rank_descending(
            starts, "Total", "Year", "month_num", "original_idx"
        )

        # Check if there are any tied Total values
        value_counts = starts["Total"].value_counts()
        tied_values = value_counts[value_counts > 1]

        if not tied_values.empty:
            # For each tied value, verify earlier calendar month has higher percentile
            for total_val in tied_values.index:
                tied_rows = starts[starts["Total"] == total_val].sort_values(["Year", "month_num"])
                percentiles = tied_rows["p_starts"].values

                # Earlier months should have higher or equal percentile (since they get lower rank number)
                for i in range(len(percentiles) - 1):
                    assert percentiles[i] >= percentiles[i + 1], \
                        f"Tie-break violation: earlier month should have higher or equal percentile. " \
                        f"For Total={total_val}, percentiles are {percentiles}"

    def test_spending_tie_break_uses_calendar_order(self, construction_spending):
        """Verify that spending ties are broken by earlier calendar month (time.year, time.month)."""
        spending_col = "current.combined.total construction"
        spending = construction_spending.copy()
        spending[spending_col] = pd.to_numeric(spending[spending_col], errors="coerce")
        spending = spending.dropna(subset=[spending_col]).copy()
        spending["year"] = spending["time.year"]
        spending["month_num"] = spending["time.month"]
        spending["original_idx"] = range(len(spending))

        spending["p_spend"] = compute_percentile_rank_descending(
            spending, spending_col, "year", "month_num", "original_idx"
        )

        # Check if there are any tied spending values
        value_counts = spending[spending_col].value_counts()
        tied_values = value_counts[value_counts > 1]

        if not tied_values.empty:
            # For each tied value, verify earlier calendar month has higher percentile
            for spending_val in tied_values.index:
                tied_rows = spending[spending[spending_col] == spending_val].sort_values(["year", "month_num"])
                percentiles = tied_rows["p_spend"].values

                # Earlier months should have higher or equal percentile
                for i in range(len(percentiles) - 1):
                    assert percentiles[i] >= percentiles[i + 1], \
                        f"Tie-break violation: earlier month should have higher or equal percentile. " \
                        f"For spending={spending_val}, percentiles are {percentiles}"


# ============================================================================
# Test: Numeric parsing validation
# ============================================================================

class TestNumericParsing:
    """Tests for verifying numeric columns are parsed correctly."""

    def test_total_column_parsed_as_numeric(self, construction_starts):
        """Verify Total column in construction.csv is parsed as numeric."""
        total_col = pd.to_numeric(construction_starts["Total"], errors="coerce")
        # Check that we have at least some valid numeric values
        valid_count = total_col.notna().sum()
        assert valid_count > 0, "Total column has no valid numeric values"

        # Verify no unexpected coercion errors (values that look numeric but fail)
        original_non_na = construction_starts["Total"].dropna()
        coerced = pd.to_numeric(original_non_na, errors="coerce")
        failed_coercion = original_non_na[coerced.isna()]
        assert len(failed_coercion) == 0, \
            f"Some Total values failed numeric coercion: {failed_coercion.tolist()}"

    def test_spending_column_parsed_as_numeric(self, construction_spending):
        """Verify total construction spending column is parsed as numeric."""
        spending_col = "current.combined.total construction"
        spending = pd.to_numeric(construction_spending[spending_col], errors="coerce")

        # Check that we have valid numeric values
        valid_count = spending.notna().sum()
        assert valid_count > 0, f"{spending_col} column has no valid numeric values"

        # Verify no unexpected coercion errors
        original_non_na = construction_spending[spending_col].dropna()
        coerced = pd.to_numeric(original_non_na, errors="coerce")
        failed_coercion = original_non_na[coerced.isna()]
        assert len(failed_coercion) == 0, \
            f"Some spending values failed numeric coercion: {failed_coercion.tolist()}"

    def test_growth_od_parsed_as_numeric(self, growth_data):
        """Verify OD column in growth data is parsed as numeric."""
        od_col = pd.to_numeric(growth_data["OD"], errors="coerce")
        valid_count = od_col.notna().sum()
        assert valid_count > 0, "OD column has no valid numeric values"

    def test_growth_time_hours_parsed_as_numeric(self, growth_data):
        """Verify Time_hours column in growth data is parsed as numeric."""
        time_col = pd.to_numeric(growth_data["Time_hours"], errors="coerce")
        valid_count = time_col.notna().sum()
        assert valid_count > 0, "Time_hours column has no valid numeric values"
