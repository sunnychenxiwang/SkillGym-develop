"""Expectation tests for volatility matching task verification.

These tests verify that the task execution produces correct outputs
based on the instruction requirements for matching construction spending
volatility to LuxO-vs-C6706 growth advantage volatility.

Tests recompute expected results from the three input CSVs and assert
exact matches against the output, including proper 6-decimal rounding.
"""

import json
import math
import os
import re
from pathlib import Path

import numpy as np
import pandas as pd
import pytest


OUTPUT_FILE = "/root/volatility_match.json"
DATASET_S9_PATH = "/root/Dataset_S9.csv"
CONSTRUCTION_PATH = "/root/construction.csv"
CONSTRUCTION_SPENDING_PATH = "/root/construction_spending.csv"

# Month name to month number mapping for sorting
MONTH_TO_NUM = {
    "January": 1, "February": 2, "March": 3, "April": 4,
    "May": 5, "June": 6, "July": 7, "August": 8,
    "September": 9, "October": 10, "November": 11, "December": 12,
    "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
    "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12
}


class ExpectedResultsCalculator:
    """Computes expected results from the input CSVs following the task specification."""

    def __init__(self):
        self._sigma_adv = None
        self._matched_months_count = None
        self._winner_column = None
        self._sigma_winner = None
        self._abs_gap = None
        self._computed = False
        self._restricted_df = None  # Store for NaN validation

    def compute_all(self):
        """Compute all expected values from input data."""
        if self._computed:
            return

        # Step 1: Compute sigma_adv from Dataset S9
        self._sigma_adv = self._compute_sigma_adv()

        # Step 2: Get restriction months from construction.csv
        restriction_months = self._get_restriction_months()

        # Step 3: Compute sigma for each annual column in construction_spending
        # restricted to matching months, sorted by (year, month number)
        results = self._compute_construction_volatilities(restriction_months)

        # Step 4: Find winner with minimum |sigma_c - sigma_adv|, lexicographic tie-break
        self._winner_column, self._sigma_winner, self._abs_gap, self._matched_months_count = \
            self._find_winner(results)

        self._computed = True

    def _compute_sigma_adv(self):
        """
        Compute sigma_adv from Dataset S9:
        1. Exclude Strain == 'Blank'
        2. Average OD by (Strain, Time_hours) across replicates
        3. Pivot to get LuxO and C6706 columns
        4. Order by increasing Time_hours
        5. Compute adv = LuxO - C6706
        6. Compute d_adv = diff(adv)
        7. Return std(d_adv, ddof=1)
        """
        df = pd.read_csv(DATASET_S9_PATH)

        # Exclude Blank rows (if present)
        df_no_blank = df[df["Strain"] != "Blank"].copy()

        # Average OD by (Strain, Time_hours)
        mean_od = df_no_blank.groupby(["Strain", "Time_hours"])["OD"].mean().reset_index()

        # Pivot to get LuxO and C6706 as columns
        pivot = mean_od.pivot(index="Time_hours", columns="Strain", values="OD")

        # Sort by Time_hours (index) - ascending order
        pivot = pivot.sort_index()

        # Compute growth advantage: adv = LuxO - C6706
        adv = pivot["LuxO"] - pivot["C6706"]

        # Compute differences
        d_adv = np.diff(adv.values)

        # Compute sample standard deviation (ddof=1)
        sigma_adv = np.std(d_adv, ddof=1)

        return sigma_adv

    def _get_restriction_months(self):
        """Get (Year, MonthName) pairs from construction.csv for restriction."""
        df = pd.read_csv(CONSTRUCTION_PATH)
        # Return list of (year, month) tuples exactly as given
        return list(zip(df["Year"], df["Month"]))

    def _compute_construction_volatilities(self, restriction_months):
        """
        For each annual.* column in construction_spending.csv:
        1. Restrict to rows where (time.year, time.month name) matches restriction_months EXACTLY
        2. Sort by (year, month number)
        3. Compute differences
        4. Compute sample std (ddof=1)

        Returns dict: {column_name: (sigma_c, matched_count)}

        NOTE: Per spec, matching is done by exact equality on (Year, Month) pairs
        "as given" - no month-name normalization is applied.
        """
        df = pd.read_csv(CONSTRUCTION_SPENDING_PATH)

        # Create a set of (year, month_name) for efficient lookup
        # EXACT matching only - no month name normalization per spec
        restriction_set = set(restriction_months)

        # Filter rows by exact match on (time.year, time.month name)
        mask = df.apply(
            lambda row: (row["time.year"], row["time.month name"]) in restriction_set,
            axis=1
        )
        df_restricted = df[mask].copy()

        matched_count = len(df_restricted)

        # Add month number for sorting
        df_restricted["month_num"] = df_restricted["time.month name"].map(MONTH_TO_NUM)

        # Sort by year, then month number
        df_restricted = df_restricted.sort_values(["time.year", "month_num"])

        # Store restricted dataframe for NaN validation
        self._restricted_df = df_restricted

        # Get annual.combined.* columns only (per output schema requirement)
        annual_cols = [c for c in df.columns if c.startswith("annual.combined.")]

        results = {}
        for col in annual_cols:
            values = df_restricted[col].values
            # Check for NaN values - only include columns with no NaNs in restricted series
            if np.any(np.isnan(values)):
                continue
            if len(values) >= 3:  # Need at least 3 values for 2 diffs
                d_c = np.diff(values)
                if len(d_c) >= 2:
                    sigma_c = np.std(d_c, ddof=1)
                    if np.isfinite(sigma_c):
                        results[col] = (sigma_c, matched_count)

        return results

    def _find_winner(self, results):
        """
        Find the column with minimum |sigma_c - sigma_adv|.
        Tie-break: lexicographically smallest column name.
        """
        if not results:
            raise ValueError("No valid columns found in construction_spending")

        candidates = []
        for col, (sigma_c, matched_count) in results.items():
            gap = abs(sigma_c - self._sigma_adv)
            candidates.append((gap, col, sigma_c, matched_count))

        # Sort by (gap, column_name) for tie-break
        candidates.sort(key=lambda x: (x[0], x[1]))

        winner_gap, winner_col, winner_sigma, matched_count = candidates[0]
        return winner_col, winner_sigma, winner_gap, matched_count

    @property
    def sigma_adv(self):
        self.compute_all()
        return round(self._sigma_adv, 6)

    @property
    def sigma_winner(self):
        self.compute_all()
        return round(self._sigma_winner, 6)

    @property
    def abs_gap(self):
        self.compute_all()
        return round(self._abs_gap, 6)

    @property
    def winner_column(self):
        self.compute_all()
        return self._winner_column

    @property
    def matched_months_count(self):
        self.compute_all()
        return self._matched_months_count

    @property
    def restricted_df(self):
        self.compute_all()
        return self._restricted_df


@pytest.fixture(scope="module")
def expected_calculator():
    """Fixture providing computed expected values."""
    return ExpectedResultsCalculator()


@pytest.fixture(scope="module")
def output_data():
    """Load the output JSON file."""
    with open(OUTPUT_FILE) as f:
        return json.load(f)


@pytest.fixture(scope="module")
def raw_json_content():
    """Load raw JSON content for precision validation."""
    with open(OUTPUT_FILE) as f:
        return f.read()


class TestOutputFileExists:
    """Tests for output file existence and basic validity."""

    def test_output_file_exists(self):
        """Verify output file was created at expected path."""
        assert os.path.exists(OUTPUT_FILE), f"Output file not found at {OUTPUT_FILE}"

    def test_output_file_not_empty(self):
        """Verify output file is not empty."""
        assert os.path.getsize(OUTPUT_FILE) > 0, "Output file is empty"


class TestOutputSchema:
    """Tests for JSON format validity and schema compliance."""

    def test_output_is_valid_json(self):
        """Verify output is valid JSON format."""
        with open(OUTPUT_FILE) as f:
            data = json.load(f)
        assert data is not None, "Failed to parse JSON"

    def test_output_is_dict(self, output_data):
        """Verify output is a dictionary/object."""
        assert isinstance(output_data, dict), "Output should be a JSON object"

    def test_exact_schema_keys(self, output_data):
        """Verify output has exactly the required keys."""
        expected_keys = {"winner_column", "sigma_adv", "sigma_winner", "abs_gap", "matched_months_count"}
        actual_keys = set(output_data.keys())
        assert actual_keys == expected_keys, \
            f"Expected exactly keys {expected_keys}, got {actual_keys}"


class TestFieldTypes:
    """Tests for correct data types of fields."""

    def test_winner_column_is_string(self, output_data):
        """Verify winner_column is a non-empty string."""
        assert isinstance(output_data["winner_column"], str), "winner_column should be a string"
        assert len(output_data["winner_column"]) > 0, "winner_column should not be empty"

    def test_sigma_adv_is_number(self, output_data):
        """Verify sigma_adv is a finite number."""
        val = output_data["sigma_adv"]
        assert isinstance(val, (int, float)), "sigma_adv should be a number"
        assert math.isfinite(val), "sigma_adv should be finite (not NaN or Inf)"

    def test_sigma_winner_is_number(self, output_data):
        """Verify sigma_winner is a finite number."""
        val = output_data["sigma_winner"]
        assert isinstance(val, (int, float)), "sigma_winner should be a number"
        assert math.isfinite(val), "sigma_winner should be finite (not NaN or Inf)"

    def test_abs_gap_is_number(self, output_data):
        """Verify abs_gap is a finite number."""
        val = output_data["abs_gap"]
        assert isinstance(val, (int, float)), "abs_gap should be a number"
        assert math.isfinite(val), "abs_gap should be finite (not NaN or Inf)"

    def test_matched_months_count_is_integer(self, output_data):
        """Verify matched_months_count is an integer."""
        assert isinstance(output_data["matched_months_count"], int), \
            "matched_months_count should be an integer"


class TestInputDataAssumptions:
    """Tests to verify input data assumptions hold for the pipeline."""

    def test_dataset_s9_has_required_strains(self):
        """Verify Dataset S9 contains required strains (LuxO, C6706)."""
        df = pd.read_csv(DATASET_S9_PATH)
        strains = set(df["Strain"].unique())
        assert "C6706" in strains, "Dataset S9 missing C6706 strain"
        assert "LuxO" in strains, "Dataset S9 missing LuxO strain"

    def test_dataset_s9_has_required_columns(self):
        """Verify Dataset S9 has required columns for processing."""
        df = pd.read_csv(DATASET_S9_PATH)
        required_cols = {"Time_hours", "Strain", "OD"}
        assert required_cols.issubset(set(df.columns)), \
            f"Dataset S9 missing required columns. Has: {df.columns.tolist()}"

    def test_dataset_s9_has_multiple_timepoints(self):
        """Verify Dataset S9 has multiple time points for computing volatility."""
        df = pd.read_csv(DATASET_S9_PATH)
        df_no_blank = df[df["Strain"] != "Blank"]
        unique_times = df_no_blank["Time_hours"].nunique()
        # Need at least 3 time points to get 2 differences for std(ddof=1)
        assert unique_times >= 3, \
            f"Dataset S9 needs at least 3 unique time points, found {unique_times}"

    def test_construction_has_required_columns(self):
        """Verify construction.csv has Year and Month columns."""
        df = pd.read_csv(CONSTRUCTION_PATH)
        assert "Year" in df.columns, "construction.csv missing Year column"
        assert "Month" in df.columns, "construction.csv missing Month column"

    def test_construction_has_sufficient_months(self):
        """Verify construction.csv has at least 3 months for computing volatility."""
        df = pd.read_csv(CONSTRUCTION_PATH)
        unique_months = len(df[["Year", "Month"]].drop_duplicates())
        assert unique_months >= 3, \
            f"construction.csv needs at least 3 unique (Year, Month) pairs for std(ddof=1), found {unique_months}"

    def test_construction_spending_has_time_columns(self):
        """Verify construction_spending.csv has required time columns."""
        df = pd.read_csv(CONSTRUCTION_SPENDING_PATH, nrows=1)
        assert "time.year" in df.columns, "construction_spending.csv missing time.year"
        assert "time.month name" in df.columns, "construction_spending.csv missing time.month name"

    def test_construction_spending_has_annual_columns(self):
        """Verify construction_spending.csv has annual.* columns to evaluate."""
        df = pd.read_csv(CONSTRUCTION_SPENDING_PATH, nrows=1)
        annual_cols = [c for c in df.columns if c.startswith("annual.")]
        assert len(annual_cols) > 0, "construction_spending.csv has no annual.* columns"


class TestDatasetS9Processing:
    """Tests verifying correct processing of Dataset S9."""

    def test_blank_rows_excluded_if_present(self):
        """Verify Blank rows are excluded from sigma_adv computation when present."""
        df = pd.read_csv(DATASET_S9_PATH)

        # If Blank rows exist, verify they would be excluded
        if "Blank" in df["Strain"].values:
            df_no_blank = df[df["Strain"] != "Blank"]
            assert len(df_no_blank) < len(df), \
                "When Blank rows exist, they should be excluded from processing"

    def test_ordering_by_time_hours(self):
        """Verify data is ordered by increasing Time_hours before differencing."""
        df = pd.read_csv(DATASET_S9_PATH)
        df_no_blank = df[df["Strain"] != "Blank"]
        mean_od = df_no_blank.groupby(["Strain", "Time_hours"])["OD"].mean().reset_index()
        pivot = mean_od.pivot(index="Time_hours", columns="Strain", values="OD")
        pivot_sorted = pivot.sort_index()

        # Verify index is monotonically increasing
        time_values = pivot_sorted.index.values
        assert all(time_values[i] < time_values[i+1] for i in range(len(time_values)-1)), \
            "Time_hours should be sorted in increasing order"

    def test_sigma_adv_uses_ddof1(self, expected_calculator):
        """Verify sample standard deviation (ddof=1) is used for sigma_adv.

        Directly validates the produced sigma_adv equals the ddof=1 computation.
        """
        # Recompute with ddof=1 independently
        df = pd.read_csv(DATASET_S9_PATH)
        df_no_blank = df[df["Strain"] != "Blank"]
        mean_od = df_no_blank.groupby(["Strain", "Time_hours"])["OD"].mean().reset_index()
        pivot = mean_od.pivot(index="Time_hours", columns="Strain", values="OD").sort_index()
        adv = pivot["LuxO"] - pivot["C6706"]
        d_adv = np.diff(adv.values)

        sigma_ddof1 = np.std(d_adv, ddof=1)

        # Expected calculator should produce the same value
        expected_calculator.compute_all()
        assert abs(round(sigma_ddof1, 6) - expected_calculator.sigma_adv) < 1e-9, \
            f"sigma_adv should use sample std (ddof=1): expected {round(sigma_ddof1, 6)}, " \
            f"got {expected_calculator.sigma_adv}"


class TestConstructionSpendingProcessing:
    """Tests verifying correct processing of construction_spending.csv."""

    def test_exact_month_restriction_applied(self, expected_calculator):
        """Verify only months from construction.csv are used with EXACT matching.

        Per spec, matching is done by exact equality on (Year, Month) pairs
        'as given' - no month-name normalization should be applied.
        """
        construction = pd.read_csv(CONSTRUCTION_PATH)
        # Build set of exact (Year, Month) pairs as given in construction.csv
        construction_months = set(zip(construction["Year"], construction["Month"]))

        spending = pd.read_csv(CONSTRUCTION_SPENDING_PATH)

        # Count spending rows that match EXACTLY (no normalization)
        def matches_exactly(row):
            return (row["time.year"], row["time.month name"]) in construction_months

        matching_rows = spending.apply(matches_exactly, axis=1).sum()

        expected_calculator.compute_all()
        assert expected_calculator.matched_months_count == matching_rows, \
            f"matched_months_count should equal number of rows with exact (Year, Month) match: " \
            f"expected {matching_rows}, computed {expected_calculator.matched_months_count}. " \
            f"Ensure exact matching without month-name normalization."

    def test_sorting_by_year_then_month(self):
        """Verify construction_spending is sorted by (year, month number) before differencing."""
        spending = pd.read_csv(CONSTRUCTION_SPENDING_PATH)
        spending["month_num"] = spending["time.month name"].map(MONTH_TO_NUM)
        sorted_df = spending.sort_values(["time.year", "month_num"])

        # Check it's properly sorted
        years = sorted_df["time.year"].values
        months = sorted_df["month_num"].values

        for i in range(len(years) - 1):
            if years[i] == years[i+1]:
                assert months[i] <= months[i+1], "Within same year, months should be ascending"
            else:
                assert years[i] < years[i+1], "Years should be ascending"


class TestNaNHandling:
    """Tests for NaN/missing data policy validation."""

    def test_winner_series_has_no_nans_in_restricted_data(self, output_data, expected_calculator):
        """Verify the winner column's restricted series contains no NaN values before differencing.

        This validates that the implementation correctly handles missing data by either:
        - Excluding columns with NaN values, or
        - Ensuring the winner column specifically has complete data
        """
        expected_calculator.compute_all()
        winner_col = output_data["winner_column"]
        restricted_df = expected_calculator.restricted_df

        if restricted_df is not None and winner_col in restricted_df.columns:
            winner_values = restricted_df[winner_col].values
            nan_count = np.sum(np.isnan(winner_values))
            assert nan_count == 0, \
                f"Winner column '{winner_col}' has {nan_count} NaN values in the restricted series. " \
                f"The restricted series must have no NaN values before differencing to compute " \
                f"a valid standard deviation."

    def test_sigma_winner_is_finite_implies_no_nans(self, output_data):
        """Verify sigma_winner being finite implies the computation had no NaN contamination."""
        sigma_winner = output_data["sigma_winner"]
        assert math.isfinite(sigma_winner), \
            f"sigma_winner must be finite (not NaN or Inf), got {sigma_winner}. " \
            f"A non-finite value indicates NaN contamination in the winner column's data."

    def test_all_candidate_columns_validated_for_nans(self, expected_calculator):
        """Verify that columns with NaN values in restricted series are excluded from consideration.

        The implementation should skip columns where the restricted series contains NaN,
        as np.diff and np.std would produce NaN/invalid results.
        """
        expected_calculator.compute_all()
        restricted_df = expected_calculator.restricted_df

        if restricted_df is None:
            pytest.skip("Restricted dataframe not available for NaN validation")

        # Get all annual columns
        annual_cols = [c for c in restricted_df.columns if c.startswith("annual.")]

        # Count columns that would be invalid due to NaN
        cols_with_nan = []
        for col in annual_cols:
            values = restricted_df[col].values
            if np.any(np.isnan(values)):
                cols_with_nan.append(col)

        # The winner should not be among columns with NaN
        winner = expected_calculator.winner_column
        assert winner not in cols_with_nan, \
            f"Winner column '{winner}' should not have NaN values in restricted series. " \
            f"Columns with NaN that should be excluded: {cols_with_nan[:5]}..."


class TestExactValueMatching:
    """Tests that verify output matches exactly computed expected values."""

    def test_sigma_adv_exact_match(self, output_data, expected_calculator):
        """Verify sigma_adv matches computed value (rounded to 6 decimals)."""
        expected = expected_calculator.sigma_adv
        actual = output_data["sigma_adv"]

        assert abs(actual - expected) < 1e-9, \
            f"sigma_adv mismatch: expected {expected} (computed from Dataset S9 with " \
            f"Blank excluded, replicates averaged, ordered by Time_hours, sample std ddof=1), " \
            f"got {actual}"

    def test_winner_column_exact_match(self, output_data, expected_calculator):
        """Verify winner_column matches computed winner with lexicographic tie-break."""
        expected = expected_calculator.winner_column
        actual = output_data["winner_column"]

        assert actual == expected, \
            f"winner_column mismatch: expected '{expected}' (column with min |sigma_c - sigma_adv| " \
            f"using lexicographic tie-break), got '{actual}'"

    def test_sigma_winner_exact_match(self, output_data, expected_calculator):
        """Verify sigma_winner matches computed value for the winner column."""
        expected = expected_calculator.sigma_winner
        actual = output_data["sigma_winner"]

        assert abs(actual - expected) < 1e-9, \
            f"sigma_winner mismatch: expected {expected} (sample std ddof=1 of restricted/sorted " \
            f"construction_spending for winner column), got {actual}"

    def test_abs_gap_exact_match(self, output_data, expected_calculator):
        """Verify abs_gap matches |sigma_winner - sigma_adv|."""
        expected = expected_calculator.abs_gap
        actual = output_data["abs_gap"]

        assert abs(actual - expected) < 1e-9, \
            f"abs_gap mismatch: expected {expected} (|sigma_winner - sigma_adv| rounded to 6 decimals), " \
            f"got {actual}"

    def test_matched_months_count_exact_match(self, output_data, expected_calculator):
        """Verify matched_months_count matches computed restricted month count."""
        expected = expected_calculator.matched_months_count
        actual = output_data["matched_months_count"]

        assert actual == expected, \
            f"matched_months_count mismatch: expected {expected} (number of construction_spending " \
            f"rows matching (Year, Month) from construction.csv with exact matching), got {actual}"


class TestAbsGapConsistency:
    """Tests for abs_gap internal consistency."""

    def test_abs_gap_equals_sigma_difference(self, output_data):
        """Verify abs_gap equals |sigma_winner - sigma_adv| within rounding."""
        sigma_winner = output_data["sigma_winner"]
        sigma_adv = output_data["sigma_adv"]
        abs_gap = output_data["abs_gap"]

        computed_gap = abs(sigma_winner - sigma_adv)
        # Allow for rounding: both values are rounded to 6 decimals, so gap may differ slightly
        assert abs(computed_gap - abs_gap) < 1e-5, \
            f"abs_gap ({abs_gap}) should approximately equal |sigma_winner - sigma_adv| ({computed_gap})"


class TestWinnerColumnValidity:
    """Tests for winner_column validity and naming convention."""

    def test_winner_column_exists_in_spending(self, output_data):
        """Verify winner_column exists in construction_spending.csv."""
        df = pd.read_csv(CONSTRUCTION_SPENDING_PATH, nrows=1)
        winner = output_data["winner_column"]
        assert winner in df.columns, \
            f"winner_column '{winner}' not found in construction_spending.csv columns"

    def test_winner_column_is_annual_column(self, output_data):
        """Verify winner_column is one of the annual.* columns."""
        df = pd.read_csv(CONSTRUCTION_SPENDING_PATH, nrows=1)
        annual_cols = [c for c in df.columns if c.startswith("annual.")]
        winner = output_data["winner_column"]

        assert winner in annual_cols, \
            f"winner_column '{winner}' should be an annual.* column. " \
            f"Available annual columns: {annual_cols[:5]}..."

    def test_winner_column_has_required_prefix(self, output_data):
        """Verify winner_column follows the required naming convention: 'annual.combined.<name>'.

        Per the output schema specification, winner_column must be of the form
        'annual.combined.<exact column name from file>'.
        """
        winner = output_data["winner_column"]
        required_prefix = "annual.combined."

        assert winner.startswith(required_prefix), \
            f"winner_column must start with '{required_prefix}' per the required output schema. " \
            f"Got '{winner}' which does not follow the required naming convention " \
            f"'annual.combined.<column_name>'"

    def test_winner_column_has_valid_suffix(self, output_data):
        """Verify winner_column has a non-empty suffix after 'annual.combined.' prefix."""
        winner = output_data["winner_column"]
        required_prefix = "annual.combined."

        if winner.startswith(required_prefix):
            suffix = winner[len(required_prefix):]
            assert len(suffix) > 0, \
                f"winner_column '{winner}' has empty suffix after '{required_prefix}'. " \
                f"Expected format: 'annual.combined.<column_name>' with non-empty column_name"


class TestMatchedMonthsConstraints:
    """Tests for matched_months_count constraints."""

    def test_matched_months_at_least_three(self, output_data):
        """Verify at least 3 months matched (needed for 2 diffs with ddof=1 std)."""
        count = output_data["matched_months_count"]
        assert count >= 3, \
            f"matched_months_count must be >= 3 to compute std(ddof=1) on differences " \
            f"(need at least 2 diff values), got {count}"

    def test_matched_months_within_construction_bounds(self, output_data):
        """Verify matched_months_count does not exceed construction.csv rows."""
        construction = pd.read_csv(CONSTRUCTION_PATH)
        max_possible = len(construction)
        actual = output_data["matched_months_count"]

        assert actual <= max_possible, \
            f"matched_months_count ({actual}) should not exceed construction.csv rows ({max_possible})"

    def test_matched_months_is_positive(self, output_data):
        """Verify matched_months_count is a positive integer."""
        count = output_data["matched_months_count"]
        assert count > 0, \
            f"matched_months_count must be positive, got {count}"


class TestNumericPrecision:
    """Tests for 6-decimal precision requirements."""

    def test_sigma_adv_six_decimal_precision(self, output_data, expected_calculator):
        """Verify sigma_adv is rounded to exactly 6 decimal places."""
        actual = output_data["sigma_adv"]
        expected_calculator.compute_all()
        expected = round(expected_calculator._sigma_adv, 6)

        # Check it matches the 6-decimal rounded value
        assert actual == expected, \
            f"sigma_adv should be rounded to 6 decimals: expected {expected}, got {actual}"

    def test_sigma_winner_six_decimal_precision(self, output_data, expected_calculator):
        """Verify sigma_winner is rounded to exactly 6 decimal places."""
        actual = output_data["sigma_winner"]
        expected_calculator.compute_all()
        expected = round(expected_calculator._sigma_winner, 6)

        assert actual == expected, \
            f"sigma_winner should be rounded to 6 decimals: expected {expected}, got {actual}"

    def test_abs_gap_six_decimal_precision(self, output_data, expected_calculator):
        """Verify abs_gap is rounded to exactly 6 decimal places."""
        actual = output_data["abs_gap"]
        expected_calculator.compute_all()
        expected = round(expected_calculator._abs_gap, 6)

        assert actual == expected, \
            f"abs_gap should be rounded to 6 decimals: expected {expected}, got {actual}"


class TestJsonSerializationPrecision:
    """Tests for JSON serialization precision."""

    def test_numeric_values_have_valid_decimal_format(self, raw_json_content):
        """Verify numeric values in JSON have at most 6 decimal digits."""
        # Parse numeric values from raw JSON using regex
        # Match numbers like 0.123456 or 1234.567890
        number_pattern = r':\s*(-?\d+\.?\d*)'
        matches = re.findall(number_pattern, raw_json_content)

        for match in matches:
            if '.' in match:
                decimal_part = match.split('.')[1]
                # Allow trailing zeros to be stripped in JSON, but no more than 6 significant decimals
                # after stripping trailing zeros
                stripped = decimal_part.rstrip('0')
                assert len(stripped) <= 6, \
                    f"Numeric value {match} has more than 6 significant decimal places"


class TestNonNegativity:
    """Tests for non-negativity of standard deviations and absolute values."""

    def test_sigma_adv_non_negative(self, output_data):
        """Verify sigma_adv (standard deviation) is non-negative."""
        assert output_data["sigma_adv"] >= 0, \
            f"sigma_adv should be non-negative (it's a std dev), got {output_data['sigma_adv']}"

    def test_sigma_winner_non_negative(self, output_data):
        """Verify sigma_winner (standard deviation) is non-negative."""
        assert output_data["sigma_winner"] >= 0, \
            f"sigma_winner should be non-negative (it's a std dev), got {output_data['sigma_winner']}"

    def test_abs_gap_non_negative(self, output_data):
        """Verify abs_gap (absolute value) is non-negative."""
        assert output_data["abs_gap"] >= 0, \
            f"abs_gap should be non-negative (it's an absolute value), got {output_data['abs_gap']}"


class TestWinnerIsOptimal:
    """Tests verifying the winner column is truly optimal."""

    def test_winner_has_minimum_gap(self, output_data, expected_calculator):
        """Verify no other annual column has a smaller gap than the winner."""
        expected_calculator.compute_all()
        sigma_adv = expected_calculator._sigma_adv
        winner_gap = expected_calculator._abs_gap

        # Recompute all gaps
        restriction_months = expected_calculator._get_restriction_months()
        results = expected_calculator._compute_construction_volatilities(restriction_months)

        for col, (sigma_c, _) in results.items():
            gap = abs(sigma_c - sigma_adv)
            if col != expected_calculator.winner_column:
                # No other column should have a strictly smaller gap
                assert gap >= winner_gap - 1e-12, \
                    f"Column '{col}' has gap {gap} which is smaller than winner gap {winner_gap}"

    def test_winner_wins_lexicographic_tiebreak(self, output_data, expected_calculator):
        """Verify winner is lexicographically first among columns with same minimum gap."""
        expected_calculator.compute_all()
        sigma_adv = expected_calculator._sigma_adv
        winner_gap = expected_calculator._abs_gap
        winner_col = expected_calculator.winner_column

        restriction_months = expected_calculator._get_restriction_months()
        results = expected_calculator._compute_construction_volatilities(restriction_months)

        # Find all columns with the same (or very close) gap
        tied_columns = []
        for col, (sigma_c, _) in results.items():
            gap = abs(sigma_c - sigma_adv)
            if abs(gap - winner_gap) < 1e-12:
                tied_columns.append(col)

        if len(tied_columns) > 1:
            tied_columns.sort()
            assert winner_col == tied_columns[0], \
                f"With tied gaps, winner should be lexicographically first: " \
                f"expected '{tied_columns[0]}', got '{winner_col}'. Tied columns: {tied_columns}"
