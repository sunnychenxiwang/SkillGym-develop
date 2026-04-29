"""Auto-generated expectation tests for task verification.

These tests verify that the CV variability analysis task produces correct outputs
based on the instruction requirements by recomputing expected values from inputs.

Input files:
- construction.csv: Monthly housing starts/permits with Year, Month, Total columns
- construction_spending.csv: Monthly spending data with time.year, time.month, time.period columns
- Dataset S9.csv: Microbial growth curves with Strain, Replicate, OD, Time_hours columns

Expected output:
- /root/variability_winner.json

Notes on ambiguity handling:
- The instruction says "standard deviation" but does not specify ddof.
  Therefore these tests accept either ddof=0 or ddof=1 when recomputing admissible CVs.
- The instruction does not explicitly define the winner string when all three CVs are null.
  Therefore these tests do not over-constrain that edge case.
"""

import itertools
import json
import math
import os
from typing import Dict, Optional, Set

import numpy as np
import pandas as pd
import pytest


# Constants
OUTPUT_FILE = "/root/variability_winner.json"
INPUT_DIR = "/root/harbor_workspaces/task_T281_run1/input"
CONSTRUCTION_FILE = os.path.join(INPUT_DIR, "construction.csv")
SPENDING_FILE = os.path.join(INPUT_DIR, "construction_spending.csv")
MICROBE_FILE = os.path.join(INPUT_DIR, "Dataset S9.csv")

VALID_DATASET_NAMES = ["construction", "construction_spending", "microbe"]
REQUIRED_KEYS = ["CV_construction", "CV_spending", "CV_microbe", "winner"]

RELATIVE_TOLERANCE = 1e-6
ABSOLUTE_TOLERANCE = 1e-10


def compute_cv_candidates(series: pd.Series) -> Set[Optional[float]]:
    """
    Compute all admissible CV values for a series, given the instruction only says
    "standard deviation" without specifying ddof.

    Admissible values include:
    - std(ddof=0) / |mean|
    - std(ddof=1) / |mean|, when defined

    Returns:
        A set of admissible float values, or {None} when CV is undefined.
    """
    clean_series = series.dropna()

    if len(clean_series) == 0:
        return {None}

    mean_val = clean_series.mean()
    if abs(mean_val) < 1e-15:
        return {None}

    candidates: Set[Optional[float]] = set()

    # Population std (ddof=0)
    try:
        std0 = clean_series.std(ddof=0)
        cv0 = std0 / abs(mean_val)
        if np.isfinite(cv0):
            candidates.add(float(cv0))
    except Exception:
        pass

    # Sample std (ddof=1), only meaningful when len >= 2
    if len(clean_series) >= 2:
        try:
            std1 = clean_series.std(ddof=1)
            cv1 = std1 / abs(mean_val)
            if np.isfinite(cv1):
                candidates.add(float(cv1))
        except Exception:
            pass

    if not candidates:
        return {None}

    return candidates


def compute_construction_cv_candidates() -> Set[Optional[float]]:
    """
    Compute admissible CV values for construction.csv.

    Steps:
    1. Build monthly date from Year + Month (English month name)
    2. Use Total column only
    3. Sort by date
    4. Compute month-over-month percent change
    5. Compute admissible CV values on that percent-change series
    """
    df = pd.read_csv(CONSTRUCTION_FILE)

    month_map = {
        "January": 1, "February": 2, "March": 3, "April": 4,
        "May": 5, "June": 6, "July": 7, "August": 8,
        "September": 9, "October": 10, "November": 11, "December": 12,
    }

    df["month_num"] = df["Month"].map(month_map)
    df["date"] = pd.to_datetime(
        df["Year"].astype(str) + "-" + df["month_num"].astype(str) + "-01"
    )
    df = df.set_index("date").sort_index()

    total_series = pd.to_numeric(df["Total"], errors="coerce")
    pct_change = total_series.pct_change().dropna()

    return compute_cv_candidates(pct_change)


def select_spending_column(df: pd.DataFrame) -> Optional[str]:
    """
    Select the spending column using the exact rule from the instruction:

    1. Use 'annual.combined.total' if present
    2. Otherwise use the unique column that:
       - starts with 'annual.combined.'
       - ends with '.total'
    3. Return None if no match or multiple matches
    """
    if "annual.combined.total" in df.columns:
        return "annual.combined.total"

    matching_cols = [
        col for col in df.columns
        if col.startswith("annual.combined.") and col.endswith(".total")
    ]

    if len(matching_cols) == 1:
        return matching_cols[0]

    return None


def compute_spending_cv_candidates() -> Set[Optional[float]]:
    """
    Compute admissible CV values for construction_spending.csv.

    Steps:
    1. Filter rows where time.period == 'annual' exactly
    2. Build date from time.year + time.month
    3. Sort by date
    4. Select annual combined total column per exact rule
    5. Compute month-over-month percent change
    6. Compute admissible CV values on that percent-change series
    """
    df = pd.read_csv(SPENDING_FILE)

    if "time.period" not in df.columns:
        return {None}

    df_annual = df[df["time.period"] == "annual"].copy()
    if len(df_annual) == 0:
        return {None}

    if "time.year" not in df_annual.columns or "time.month" not in df_annual.columns:
        return {None}

    df_annual["date"] = pd.to_datetime(
        df_annual["time.year"].astype(str) + "-" +
        df_annual["time.month"].astype(str) + "-01"
    )
    df_annual = df_annual.set_index("date").sort_index()

    spending_col = select_spending_column(df_annual)
    if spending_col is None:
        return {None}

    spending_series = pd.to_numeric(df_annual[spending_col], errors="coerce")
    pct_change = spending_series.pct_change().dropna()

    return compute_cv_candidates(pct_change)


def compute_microbe_cv_candidates() -> Set[Optional[float]]:
    """
    Compute admissible CV values for Dataset S9.csv.

    Steps:
    1. Exclude Strain == 'Blank'
    2. For each (Strain, Replicate), sort by Time_hours
    3. Compute dOD/dt via first differences
    4. Pool all dOD/dt values
    5. Compute admissible CV values on pooled rates
    """
    df = pd.read_csv(MICROBE_FILE)

    df_no_blank = df[df["Strain"] != "Blank"].copy()
    if len(df_no_blank) == 0:
        return {None}

    all_rates = []

    for (_strain, _replicate), group in df_no_blank.groupby(["Strain", "Replicate"]):
        group = group.sort_values("Time_hours")

        od_values = group["OD"].values
        time_values = group["Time_hours"].values

        if len(od_values) < 2:
            continue

        delta_od = np.diff(od_values)
        delta_time = np.diff(time_values)

        valid_mask = delta_time > 0
        if np.sum(valid_mask) == 0:
            continue

        rates = delta_od[valid_mask] / delta_time[valid_mask]
        all_rates.extend(rates)

    if len(all_rates) == 0:
        return {None}

    pooled_rates = pd.Series(all_rates)
    return compute_cv_candidates(pooled_rates)


def compute_admissible_winners(
    cv_construction_candidates: Set[Optional[float]],
    cv_spending_candidates: Set[Optional[float]],
    cv_microbe_candidates: Set[Optional[float]],
) -> Set[str]:
    """
    Compute all admissible winners under the ambiguous standard-deviation definition.

    If all three CVs are null in a candidate interpretation, no winner is added.
    """
    winners: Set[str] = set()

    for cv_c, cv_s, cv_m in itertools.product(
        cv_construction_candidates,
        cv_spending_candidates,
        cv_microbe_candidates,
    ):
        mapping = {
            "construction": cv_c,
            "construction_spending": cv_s,
            "microbe": cv_m,
        }

        valid = {k: v for k, v in mapping.items() if v is not None}
        if not valid:
            continue

        max_cv = max(valid.values())
        tied = [k for k, v in valid.items() if v == max_cv]
        winners.add(sorted(tied)[0])

    return winners


def assert_matches_any_candidate(
    actual_value: Optional[float],
    candidates: Set[Optional[float]],
    field_name: str,
):
    """
    Assert that actual_value matches one admissible candidate or is null when allowed.
    """
    if actual_value is None:
        assert None in candidates, (
            f"{field_name} should not be null; admissible values are "
            f"{sorted(v for v in candidates if v is not None)}"
        )
        return

    assert isinstance(actual_value, (int, float)), (
        f"{field_name} should be a JSON number or null, got {type(actual_value).__name__}: {actual_value}"
    )
    assert math.isfinite(actual_value), f"{field_name} must be finite, got {actual_value}"

    numeric_candidates = [v for v in candidates if v is not None]
    assert numeric_candidates, f"No numeric admissible candidates for {field_name}"

    matched = any(
        actual_value == pytest.approx(candidate, rel=RELATIVE_TOLERANCE, abs=ABSOLUTE_TOLERANCE)
        for candidate in numeric_candidates
    )
    assert matched, (
        f"{field_name} mismatch: got {actual_value:.12f}, admissible values are "
        f"{[round(v, 12) for v in sorted(numeric_candidates)]}"
    )


class TestOutputFileExists:
    """Tests for verifying the output file was created."""

    def test_output_file_exists(self):
        assert os.path.exists(OUTPUT_FILE), f"Output file not found at {OUTPUT_FILE}"

    def test_output_directory_exists(self):
        output_dir = os.path.dirname(OUTPUT_FILE)
        assert os.path.isdir(output_dir), f"Output directory {output_dir} does not exist"

    def test_output_file_not_empty(self):
        assert os.path.getsize(OUTPUT_FILE) > 0, "Output file is empty"


class TestOutputFormat:
    """Tests for verifying the output is valid JSON with correct structure."""

    @pytest.fixture
    def output_data(self):
        with open(OUTPUT_FILE, "r") as f:
            return json.load(f)

    def test_output_is_valid_json(self):
        try:
            with open(OUTPUT_FILE, "r") as f:
                data = json.load(f)
            assert data is not None
        except json.JSONDecodeError as e:
            pytest.fail(f"Output file is not valid JSON: {e}")

    def test_output_is_object(self, output_data):
        assert isinstance(output_data, dict), (
            f"Output should be a JSON object, got {type(output_data).__name__}"
        )

    def test_all_required_keys_present(self, output_data):
        missing_keys = [k for k in REQUIRED_KEYS if k not in output_data]
        assert not missing_keys, f"Missing required keys: {missing_keys}"

    def test_no_extra_keys(self, output_data):
        extra_keys = [k for k in output_data if k not in REQUIRED_KEYS]
        assert not extra_keys, f"Unexpected keys in output: {extra_keys}"


class TestCVValueTypes:
    """Tests for verifying CV values are correctly typed."""

    @pytest.fixture
    def output_data(self):
        with open(OUTPUT_FILE, "r") as f:
            return json.load(f)

    def test_cv_construction_type(self, output_data):
        cv = output_data.get("CV_construction")
        assert cv is None or isinstance(cv, (int, float)), (
            f"CV_construction should be float or null, got {type(cv).__name__}: {cv}"
        )

    def test_cv_spending_type(self, output_data):
        cv = output_data.get("CV_spending")
        assert cv is None or isinstance(cv, (int, float)), (
            f"CV_spending should be float or null, got {type(cv).__name__}: {cv}"
        )

    def test_cv_microbe_type(self, output_data):
        cv = output_data.get("CV_microbe")
        assert cv is None or isinstance(cv, (int, float)), (
            f"CV_microbe should be float or null, got {type(cv).__name__}: {cv}"
        )

    def test_cv_values_finite_when_not_null(self, output_data):
        for key in ["CV_construction", "CV_spending", "CV_microbe"]:
            cv = output_data.get(key)
            if cv is not None:
                assert math.isfinite(cv), f"{key} must be finite, got {cv}"

    def test_cv_values_non_negative_when_finite(self, output_data):
        for key in ["CV_construction", "CV_spending", "CV_microbe"]:
            cv = output_data.get(key)
            if cv is not None:
                assert cv >= 0, f"{key} should be non-negative, got {cv}"


class TestCVRecomputation:
    """Tests that verify CV values match admissible recomputed values from input files."""

    @pytest.fixture
    def output_data(self):
        with open(OUTPUT_FILE, "r") as f:
            return json.load(f)

    @pytest.fixture
    def expected_construction_candidates(self):
        return compute_construction_cv_candidates()

    @pytest.fixture
    def expected_spending_candidates(self):
        return compute_spending_cv_candidates()

    @pytest.fixture
    def expected_microbe_candidates(self):
        return compute_microbe_cv_candidates()

    def test_cv_construction_matches_recomputed_candidates(
        self, output_data, expected_construction_candidates
    ):
        assert_matches_any_candidate(
            output_data.get("CV_construction"),
            expected_construction_candidates,
            "CV_construction",
        )

    def test_cv_spending_matches_recomputed_candidates(
        self, output_data, expected_spending_candidates
    ):
        assert_matches_any_candidate(
            output_data.get("CV_spending"),
            expected_spending_candidates,
            "CV_spending",
        )

    def test_cv_microbe_matches_recomputed_candidates(
        self, output_data, expected_microbe_candidates
    ):
        assert_matches_any_candidate(
            output_data.get("CV_microbe"),
            expected_microbe_candidates,
            "CV_microbe",
        )


class TestConstructionCVComputation:
    """Tests specific to construction CV computation methodology."""

    @pytest.fixture
    def construction_df(self):
        return pd.read_csv(CONSTRUCTION_FILE)

    def test_construction_uses_total_column(self, construction_df):
        assert "Total" in construction_df.columns, (
            "construction.csv must have 'Total' column for CV computation"
        )

    def test_construction_has_year_month_columns(self, construction_df):
        assert "Year" in construction_df.columns, "construction.csv must have 'Year' column"
        assert "Month" in construction_df.columns, "construction.csv must have 'Month' column"

    def test_construction_month_names_are_english(self, construction_df):
        valid_months = {
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December",
        }
        actual_months = set(construction_df["Month"].unique())
        assert actual_months.issubset(valid_months), (
            f"Month column should contain English month names, found unexpected values: "
            f"{actual_months - valid_months}"
        )

    def test_construction_has_sufficient_rows_for_pct_change_series(self, construction_df):
        assert len(construction_df) >= 2, (
            "construction.csv must have at least 2 rows to form a percent-change series"
        )


class TestSpendingColumnSelection:
    """Tests for spending column selection rule."""

    @pytest.fixture
    def spending_df(self):
        return pd.read_csv(SPENDING_FILE)

    def test_spending_has_time_period_column(self, spending_df):
        assert "time.period" in spending_df.columns, (
            "construction_spending.csv must have 'time.period' column for filtering"
        )

    def test_spending_has_time_year_column(self, spending_df):
        assert "time.year" in spending_df.columns, (
            "construction_spending.csv must have 'time.year' column for date construction"
        )

    def test_spending_has_time_month_column(self, spending_df):
        assert "time.month" in spending_df.columns, (
            "construction_spending.csv must have 'time.month' column for date construction"
        )

    def test_spending_column_selection_strict_rule(self, spending_df):
        selected = select_spending_column(spending_df)

        if "annual.combined.total" in spending_df.columns:
            assert selected == "annual.combined.total", (
                "When 'annual.combined.total' exists, it must be selected"
            )
        else:
            matching_cols = [
                col for col in spending_df.columns
                if col.startswith("annual.combined.") and col.endswith(".total")
            ]

            if len(matching_cols) == 1:
                assert selected == matching_cols[0], (
                    f"Should select the unique matching column: {matching_cols[0]}"
                )
            elif len(matching_cols) == 0:
                assert selected is None, "Should return None when no matching column exists"
            else:
                assert selected is None, (
                    f"Should return None when multiple columns match: {matching_cols}"
                )

    def test_spending_rejects_loose_column_matching(self, spending_df):
        col = "annual.combined.total construction"
        if col in spending_df.columns and "annual.combined.total" not in spending_df.columns:
            selected = select_spending_column(spending_df)
            assert selected != col, (
                f"Column '{col}' should NOT be selected - it does not end with '.total'"
            )


class TestSpendingFilteringStrict:
    """Tests for strict filtering of spending data."""

    @pytest.fixture
    def spending_df(self):
        return pd.read_csv(SPENDING_FILE)

    def test_spending_filtering_uses_strict_equality(self, spending_df):
        if "time.period" not in spending_df.columns:
            pytest.skip("time.period column missing")

        strict_annual = spending_df[spending_df["time.period"] == "annual"]
        loose_annual = spending_df[
            spending_df["time.period"].astype(str).str.lower().str.contains("annual", na=False)
        ]

        if len(loose_annual) > 0 and len(strict_annual) == 0:
            candidates = compute_spending_cv_candidates()
            assert candidates == {None}, (
                "If no rows match time.period == 'annual' exactly, CV_spending should be null"
            )


class TestMicrobeDataProcessing:
    """Tests specific to microbe data processing methodology."""

    @pytest.fixture
    def microbe_df(self):
        return pd.read_csv(MICROBE_FILE)

    def test_microbe_has_required_columns(self, microbe_df):
        required_cols = ["Time", "Time_hours", "Strain", "Replicate", "OD"]
        for col in required_cols:
            assert col in microbe_df.columns, f"Dataset S9.csv must have '{col}' column"

    def test_microbe_has_blank_strain(self, microbe_df):
        strains = microbe_df["Strain"].unique()
        assert "Blank" in strains, "Dataset S9.csv should have 'Blank' strain data to exclude"

    def test_microbe_has_non_blank_strains(self, microbe_df):
        non_blank = microbe_df[microbe_df["Strain"] != "Blank"]
        assert len(non_blank) > 0, (
            "Dataset S9.csv must have non-Blank strain data for CV computation"
        )

    def test_microbe_blank_excluded_from_computation(self, microbe_df):
        with_blank = []
        for (_strain, _replicate), group in microbe_df.groupby(["Strain", "Replicate"]):
            group = group.sort_values("Time_hours")
            od_values = group["OD"].values
            time_values = group["Time_hours"].values
            if len(od_values) >= 2:
                delta_od = np.diff(od_values)
                delta_time = np.diff(time_values)
                valid_mask = delta_time > 0
                if np.sum(valid_mask) > 0:
                    with_blank.extend((delta_od[valid_mask] / delta_time[valid_mask]).tolist())

        no_blank_df = microbe_df[microbe_df["Strain"] != "Blank"]
        no_blank = []
        for (_strain, _replicate), group in no_blank_df.groupby(["Strain", "Replicate"]):
            group = group.sort_values("Time_hours")
            od_values = group["OD"].values
            time_values = group["Time_hours"].values
            if len(od_values) >= 2:
                delta_od = np.diff(od_values)
                delta_time = np.diff(time_values)
                valid_mask = delta_time > 0
                if np.sum(valid_mask) > 0:
                    no_blank.extend((delta_od[valid_mask] / delta_time[valid_mask]).tolist())

        assert len(no_blank) <= len(with_blank), (
            "Excluding Blank strain should not increase the number of pooled rates"
        )


class TestWinnerDetermination:
    """Tests for verifying the winner field is correctly determined."""

    @pytest.fixture
    def output_data(self):
        with open(OUTPUT_FILE, "r") as f:
            return json.load(f)

    @pytest.fixture
    def admissible_winners(self):
        return compute_admissible_winners(
            compute_construction_cv_candidates(),
            compute_spending_cv_candidates(),
            compute_microbe_cv_candidates(),
        )

    def test_winner_type(self, output_data):
        winner = output_data.get("winner")
        assert isinstance(winner, str), (
            f"winner should be a string, got {type(winner).__name__}: {winner}"
        )

    def test_winner_valid_when_any_non_null_cv_exists(self, output_data):
        winner = output_data.get("winner")
        cvs = [
            output_data.get("CV_construction"),
            output_data.get("CV_spending"),
            output_data.get("CV_microbe"),
        ]
        if any(cv is not None for cv in cvs):
            assert winner in VALID_DATASET_NAMES, (
                f"When at least one CV is non-null, winner must be one of {VALID_DATASET_NAMES}. "
                f"Got '{winner}'"
            )

    def test_winner_matches_admissible_recomputed_winners_when_defined(
        self, output_data, admissible_winners
    ):
        winner = output_data.get("winner")
        if admissible_winners:
            assert winner in admissible_winners, (
                f"winner '{winner}' is not admissible under any valid interpretation of "
                f"the instruction's unspecified standard-deviation convention. "
                f"Admissible winners: {sorted(admissible_winners)}"
            )

    def test_winner_consistent_with_output_cvs(self, output_data):
        winner = output_data.get("winner")
        cv_mapping = {
            "construction": output_data.get("CV_construction"),
            "construction_spending": output_data.get("CV_spending"),
            "microbe": output_data.get("CV_microbe"),
        }
        valid = {k: v for k, v in cv_mapping.items() if v is not None}

        if not valid:
            # Instruction does not explicitly define this edge case.
            # Do not over-constrain the winner string here.
            return

        max_cv = max(valid.values())
        tied = [k for k, v in valid.items() if v == max_cv]
        expected_from_output = sorted(tied)[0]

        assert winner == expected_from_output, (
            f"winner '{winner}' is inconsistent with the output CV values themselves. "
            f"Expected '{expected_from_output}' by max-CV + lexicographic tie-break."
        )


class TestWinnerTieBreaking:
    """Tests specifically for tie-breaking behavior."""

    def test_tie_breaking_uses_exact_equality(self):
        mapping = {"construction": 0.5, "construction_spending": None, "microbe": 0.5}
        valid = {k: v for k, v in mapping.items() if v is not None}
        max_cv = max(valid.values())
        tied = [k for k, v in valid.items() if v == max_cv]
        assert sorted(tied)[0] == "construction"

    def test_tie_breaking_three_way_tie(self):
        mapping = {
            "construction": 1.0,
            "construction_spending": 1.0,
            "microbe": 1.0,
        }
        max_cv = max(mapping.values())
        tied = [k for k, v in mapping.items() if v == max_cv]
        assert sorted(tied)[0] == "construction"

    def test_close_but_not_equal_values_are_not_ties(self):
        mapping = {
            "construction": 0.5,
            "construction_spending": None,
            "microbe": 0.5 + 1e-10,
        }
        valid = {k: v for k, v in mapping.items() if v is not None}
        max_cv = max(valid.values())
        tied = [k for k, v in valid.items() if v == max_cv]
        assert sorted(tied)[0] == "microbe"


class TestMeanZeroHandling:
    """Tests for verifying proper handling of mean==0 case."""

    @pytest.fixture
    def output_data(self):
        with open(OUTPUT_FILE, "r") as f:
            return json.load(f)

    def test_null_cv_values_match_admissible_null_cases(self, output_data):
        recomputed = {
            "CV_construction": compute_construction_cv_candidates(),
            "CV_spending": compute_spending_cv_candidates(),
            "CV_microbe": compute_microbe_cv_candidates(),
        }

        for key, candidates in recomputed.items():
            actual = output_data.get(key)
            if actual is None:
                assert None in candidates, (
                    f"{key} is null in output, but null is not admissible from recomputation"
                )

    def test_winner_excludes_null_datasets_when_valid_values_exist(self, output_data):
        winner = output_data.get("winner")
        cv_mapping = {
            "construction": output_data.get("CV_construction"),
            "construction_spending": output_data.get("CV_spending"),
            "microbe": output_data.get("CV_microbe"),
        }
        valid = {k: v for k, v in cv_mapping.items() if v is not None}

        if valid:
            assert winner in valid, (
                f"winner '{winner}' should not be a dataset with null CV when valid CVs exist"
            )


class TestDataIntegrity:
    """Tests for verifying the data is processed correctly."""

    @pytest.fixture
    def output_data(self):
        with open(OUTPUT_FILE, "r") as f:
            return json.load(f)

    def test_input_files_exist(self):
        assert os.path.exists(CONSTRUCTION_FILE), f"Construction input file not found: {CONSTRUCTION_FILE}"
        assert os.path.exists(SPENDING_FILE), f"Spending input file not found: {SPENDING_FILE}"
        assert os.path.exists(MICROBE_FILE), f"Microbe input file not found: {MICROBE_FILE}"

    def test_winner_valid_when_some_cv_is_valid(self, output_data):
        cvs = [
            output_data.get("CV_construction"),
            output_data.get("CV_spending"),
            output_data.get("CV_microbe"),
        ]
        winner = output_data.get("winner")

        if any(cv is not None for cv in cvs):
            assert winner in VALID_DATASET_NAMES, (
                f"With at least one valid CV, winner should be a valid dataset name. Got '{winner}'"
            )


class TestJSONFormatting:
    """Tests for verifying JSON output formatting details."""

    def test_json_readable(self):
        with open(OUTPUT_FILE, "r") as f:
            content = f.read()
        assert content.strip(), "JSON file content is empty or whitespace only"
        data = json.loads(content)
        assert isinstance(data, dict)

    def test_json_uses_standard_encoding(self):
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            content = f.read()
        data = json.loads(content)
        assert data is not None