"""Auto-generated expectation tests for task verification.

These tests verify that the task execution produces correct outputs
based on the instruction requirements for computing critical corridor rankings
from MATPOWER case files using DC power flow analysis.
"""

import os
from pathlib import Path

import pandas as pd
import pytest


# Constants
OUTPUT_FILE = "/root/critical_corridor.xlsx"
EXPECTED_CASES = {"case57", "case118", "pglib118"}
VALID_BASEMVA_VALUES = {100.0, 100}  # Both case files use baseMVA = 100


class TestOutputFileExists:
    """Tests for output file existence and basic validity."""

    def test_output_directory_exists(self):
        """Verify output directory exists."""
        output_dir = Path(OUTPUT_FILE).parent
        assert output_dir.exists(), f"Output directory not found: {output_dir}"

    def test_output_file_exists(self):
        """Verify output Excel file was created at exact path."""
        assert os.path.exists(OUTPUT_FILE), f"Output file not found: {OUTPUT_FILE}"

    def test_output_file_not_empty(self):
        """Verify output file is not empty."""
        file_size = os.path.getsize(OUTPUT_FILE)
        assert file_size > 0, "Output file is empty"

    def test_output_file_is_valid_xlsx(self):
        """Verify output file is a valid Excel file."""
        try:
            excel_file = pd.ExcelFile(OUTPUT_FILE)
            assert excel_file is not None
        except Exception as e:
            pytest.fail(f"Output file is not a valid Excel file: {e}")


class TestResultSheet:
    """Tests for the 'result' sheet structure and content."""

    @pytest.fixture
    def result_df(self):
        """Load the result sheet from the Excel file."""
        return pd.read_excel(OUTPUT_FILE, sheet_name="result")

    def test_result_sheet_exists(self):
        """Verify 'result' sheet exists in the workbook."""
        excel_file = pd.ExcelFile(OUTPUT_FILE)
        assert "result" in excel_file.sheet_names, (
            f"'result' sheet not found. Available sheets: {excel_file.sheet_names}"
        )

    def test_result_sheet_has_exactly_one_data_row(self, result_df):
        """Verify result sheet has exactly one row of data."""
        assert len(result_df) == 1, f"Expected 1 row in result sheet, got {len(result_df)}"

    def test_result_sheet_has_corridor_fbus_column(self, result_df):
        """Verify 'corridor_fbus' column exists."""
        assert "corridor_fbus" in result_df.columns, (
            f"'corridor_fbus' column not found. Columns: {list(result_df.columns)}"
        )

    def test_result_sheet_has_corridor_tbus_column(self, result_df):
        """Verify 'corridor_tbus' column exists."""
        assert "corridor_tbus" in result_df.columns, (
            f"'corridor_tbus' column not found. Columns: {list(result_df.columns)}"
        )

    def test_result_sheet_has_cases_where_topflow_column(self, result_df):
        """Verify 'cases_where_topflow' column exists."""
        assert "cases_where_topflow" in result_df.columns, (
            f"'cases_where_topflow' column not found. Columns: {list(result_df.columns)}"
        )

    def test_corridor_fbus_is_integer(self, result_df):
        """Verify corridor_fbus is an integer value."""
        fbus = result_df["corridor_fbus"].iloc[0]
        assert pd.notna(fbus), "corridor_fbus is null/NaN"
        # Check if it's a whole number (int or float that represents int)
        assert float(fbus) == int(fbus), f"corridor_fbus is not an integer: {fbus}"

    def test_corridor_tbus_is_integer(self, result_df):
        """Verify corridor_tbus is an integer value."""
        tbus = result_df["corridor_tbus"].iloc[0]
        assert pd.notna(tbus), "corridor_tbus is null/NaN"
        assert float(tbus) == int(tbus), f"corridor_tbus is not an integer: {tbus}"

    def test_corridor_fbus_less_than_tbus(self, result_df):
        """Verify corridor_fbus < corridor_tbus (undirected corridor key)."""
        fbus = int(result_df["corridor_fbus"].iloc[0])
        tbus = int(result_df["corridor_tbus"].iloc[0])
        assert fbus < tbus, (
            f"corridor_fbus ({fbus}) must be less than corridor_tbus ({tbus})"
        )

    def test_corridor_fbus_is_positive(self, result_df):
        """Verify corridor_fbus is a positive bus number."""
        fbus = int(result_df["corridor_fbus"].iloc[0])
        assert fbus > 0, f"corridor_fbus must be positive: {fbus}"

    def test_corridor_tbus_is_positive(self, result_df):
        """Verify corridor_tbus is a positive bus number."""
        tbus = int(result_df["corridor_tbus"].iloc[0])
        assert tbus > 0, f"corridor_tbus must be positive: {tbus}"

    def test_cases_where_topflow_is_string(self, result_df):
        """Verify cases_where_topflow is a string."""
        cases = result_df["cases_where_topflow"].iloc[0]
        assert pd.notna(cases), "cases_where_topflow is null/NaN"
        assert isinstance(cases, str), f"cases_where_topflow must be a string: {type(cases)}"

    def test_cases_where_topflow_contains_valid_cases(self, result_df):
        """Verify cases_where_topflow contains only valid case names."""
        cases_str = result_df["cases_where_topflow"].iloc[0]
        cases_list = [c.strip() for c in cases_str.split(",")]
        for case in cases_list:
            assert case in EXPECTED_CASES, (
                f"Invalid case name '{case}'. Valid cases: {EXPECTED_CASES}"
            )

    def test_cases_where_topflow_has_at_least_two_cases(self, result_df):
        """Verify corridor appears in at least 2 cases (per task requirement)."""
        cases_str = result_df["cases_where_topflow"].iloc[0]
        cases_list = [c.strip() for c in cases_str.split(",")]
        assert len(cases_list) >= 2, (
            f"Corridor must appear in at least 2 cases, found: {len(cases_list)}"
        )


class TestEvidenceSheet:
    """Tests for the 'evidence' sheet structure and content."""

    @pytest.fixture
    def evidence_df(self):
        """Load the evidence sheet from the Excel file."""
        return pd.read_excel(OUTPUT_FILE, sheet_name="evidence")

    def test_evidence_sheet_exists(self):
        """Verify 'evidence' sheet exists in the workbook."""
        excel_file = pd.ExcelFile(OUTPUT_FILE)
        assert "evidence" in excel_file.sheet_names, (
            f"'evidence' sheet not found. Available sheets: {excel_file.sheet_names}"
        )

    def test_evidence_sheet_has_three_rows(self, evidence_df):
        """Verify evidence sheet has exactly 3 rows (one per case)."""
        assert len(evidence_df) == 3, (
            f"Expected 3 rows in evidence sheet (one per case), got {len(evidence_df)}"
        )

    def test_evidence_sheet_has_case_column(self, evidence_df):
        """Verify 'case' column exists."""
        assert "case" in evidence_df.columns, (
            f"'case' column not found. Columns: {list(evidence_df.columns)}"
        )

    def test_evidence_sheet_has_top_fbus_column(self, evidence_df):
        """Verify 'top_fbus' column exists."""
        assert "top_fbus" in evidence_df.columns, (
            f"'top_fbus' column not found. Columns: {list(evidence_df.columns)}"
        )

    def test_evidence_sheet_has_top_tbus_column(self, evidence_df):
        """Verify 'top_tbus' column exists."""
        assert "top_tbus" in evidence_df.columns, (
            f"'top_tbus' column not found. Columns: {list(evidence_df.columns)}"
        )

    def test_evidence_sheet_has_top_abs_flow_mw_column(self, evidence_df):
        """Verify 'top_abs_flow_mw' column exists."""
        assert "top_abs_flow_mw" in evidence_df.columns, (
            f"'top_abs_flow_mw' column not found. Columns: {list(evidence_df.columns)}"
        )

    def test_evidence_sheet_has_top_flow_mw_signed_column(self, evidence_df):
        """Verify 'top_flow_mw_signed' column exists."""
        assert "top_flow_mw_signed" in evidence_df.columns, (
            f"'top_flow_mw_signed' column not found. Columns: {list(evidence_df.columns)}"
        )

    def test_evidence_sheet_has_basemva_column(self, evidence_df):
        """Verify 'baseMVA' column exists."""
        assert "baseMVA" in evidence_df.columns, (
            f"'baseMVA' column not found. Columns: {list(evidence_df.columns)}"
        )

    def test_evidence_contains_all_three_cases(self, evidence_df):
        """Verify evidence sheet contains entries for all three cases."""
        case_names = set(evidence_df["case"].tolist())
        assert case_names == EXPECTED_CASES, (
            f"Expected cases {EXPECTED_CASES}, found {case_names}"
        )

    def test_all_top_fbus_are_positive_integers(self, evidence_df):
        """Verify all top_fbus values are positive integers."""
        for idx, row in evidence_df.iterrows():
            fbus = row["top_fbus"]
            assert pd.notna(fbus), f"top_fbus is null at row {idx}"
            assert float(fbus) == int(fbus), f"top_fbus is not an integer at row {idx}: {fbus}"
            assert int(fbus) > 0, f"top_fbus must be positive at row {idx}: {fbus}"

    def test_all_top_tbus_are_positive_integers(self, evidence_df):
        """Verify all top_tbus values are positive integers."""
        for idx, row in evidence_df.iterrows():
            tbus = row["top_tbus"]
            assert pd.notna(tbus), f"top_tbus is null at row {idx}"
            assert float(tbus) == int(tbus), f"top_tbus is not an integer at row {idx}: {tbus}"
            assert int(tbus) > 0, f"top_tbus must be positive at row {idx}: {tbus}"

    def test_all_top_abs_flow_mw_are_non_negative(self, evidence_df):
        """Verify all top_abs_flow_mw values are non-negative (absolute values)."""
        for idx, row in evidence_df.iterrows():
            abs_flow = row["top_abs_flow_mw"]
            assert pd.notna(abs_flow), f"top_abs_flow_mw is null at row {idx}"
            assert abs_flow >= 0, f"top_abs_flow_mw must be non-negative at row {idx}: {abs_flow}"

    def test_all_top_flow_mw_signed_are_numeric(self, evidence_df):
        """Verify all top_flow_mw_signed values are numeric."""
        for idx, row in evidence_df.iterrows():
            signed_flow = row["top_flow_mw_signed"]
            assert pd.notna(signed_flow), f"top_flow_mw_signed is null at row {idx}"
            assert isinstance(signed_flow, (int, float)), (
                f"top_flow_mw_signed must be numeric at row {idx}: {type(signed_flow)}"
            )

    def test_abs_flow_matches_signed_flow_absolute_value(self, evidence_df):
        """Verify top_abs_flow_mw equals abs(top_flow_mw_signed)."""
        for idx, row in evidence_df.iterrows():
            abs_flow = row["top_abs_flow_mw"]
            signed_flow = row["top_flow_mw_signed"]
            expected_abs = abs(signed_flow)
            # Use relative tolerance for floating point comparison
            assert abs(abs_flow - expected_abs) < 1e-6, (
                f"top_abs_flow_mw ({abs_flow}) doesn't match abs(top_flow_mw_signed) "
                f"({expected_abs}) at row {idx}"
            )

    def test_all_basemva_are_positive(self, evidence_df):
        """Verify all baseMVA values are positive."""
        for idx, row in evidence_df.iterrows():
            basemva = row["baseMVA"]
            assert pd.notna(basemva), f"baseMVA is null at row {idx}"
            assert basemva > 0, f"baseMVA must be positive at row {idx}: {basemva}"

    def test_basemva_values_are_valid(self, evidence_df):
        """Verify baseMVA values match expected values from case files (100)."""
        for idx, row in evidence_df.iterrows():
            basemva = row["baseMVA"]
            # All three case files use baseMVA = 100
            assert basemva == 100 or basemva == 100.0, (
                f"baseMVA should be 100 for all cases at row {idx}: {basemva}"
            )


class TestCorridorConsistency:
    """Tests for consistency between result and evidence sheets."""

    @pytest.fixture
    def result_df(self):
        """Load the result sheet from the Excel file."""
        return pd.read_excel(OUTPUT_FILE, sheet_name="result")

    @pytest.fixture
    def evidence_df(self):
        """Load the evidence sheet from the Excel file."""
        return pd.read_excel(OUTPUT_FILE, sheet_name="evidence")

    def test_critical_corridor_appears_in_evidence(self, result_df, evidence_df):
        """Verify the critical corridor from result sheet appears in evidence sheet."""
        corridor_fbus = int(result_df["corridor_fbus"].iloc[0])
        corridor_tbus = int(result_df["corridor_tbus"].iloc[0])

        # Check if this corridor appears as a top-flow branch in evidence
        matching_rows = []
        for _, row in evidence_df.iterrows():
            fbus = int(row["top_fbus"])
            tbus = int(row["top_tbus"])
            # Normalize to undirected corridor (min, max)
            normalized = (min(fbus, tbus), max(fbus, tbus))
            if normalized == (corridor_fbus, corridor_tbus):
                matching_rows.append(row["case"])

        # The corridor should appear in at least 2 cases
        assert len(matching_rows) >= 2, (
            f"Critical corridor ({corridor_fbus}, {corridor_tbus}) should appear in "
            f"at least 2 cases in evidence, found in: {matching_rows}"
        )

    def test_cases_where_topflow_matches_evidence(self, result_df, evidence_df):
        """Verify cases_where_topflow matches actual cases in evidence."""
        corridor_fbus = int(result_df["corridor_fbus"].iloc[0])
        corridor_tbus = int(result_df["corridor_tbus"].iloc[0])
        cases_str = result_df["cases_where_topflow"].iloc[0]
        claimed_cases = set(c.strip() for c in cases_str.split(","))

        # Find actual cases where this corridor is the top-flow branch
        actual_cases = set()
        for _, row in evidence_df.iterrows():
            fbus = int(row["top_fbus"])
            tbus = int(row["top_tbus"])
            normalized = (min(fbus, tbus), max(fbus, tbus))
            if normalized == (corridor_fbus, corridor_tbus):
                actual_cases.add(row["case"])

        assert claimed_cases == actual_cases, (
            f"cases_where_topflow ({claimed_cases}) doesn't match evidence ({actual_cases})"
        )


class TestFlowValueReasonableness:
    """Tests for reasonable power flow values."""

    @pytest.fixture
    def evidence_df(self):
        """Load the evidence sheet from the Excel file."""
        return pd.read_excel(OUTPUT_FILE, sheet_name="evidence")

    def test_top_flows_are_within_reasonable_range(self, evidence_df):
        """Verify top flow values are within reasonable range for these systems."""
        # IEEE 57-bus and 118-bus systems typically have flows in 0-500+ MW range
        # The highest flow in any case shouldn't exceed total system generation
        MAX_REASONABLE_FLOW = 2000  # MW - generous upper bound

        for idx, row in evidence_df.iterrows():
            abs_flow = row["top_abs_flow_mw"]
            assert abs_flow <= MAX_REASONABLE_FLOW, (
                f"Flow value {abs_flow} MW seems unreasonably high for case {row['case']}"
            )

    def test_top_flows_are_significant(self, evidence_df):
        """Verify top flow values are significant (not near-zero)."""
        # The top flow in any case should be a significant value, not near zero
        MIN_SIGNIFICANT_FLOW = 10  # MW - minimum expected for top flow

        for idx, row in evidence_df.iterrows():
            abs_flow = row["top_abs_flow_mw"]
            assert abs_flow >= MIN_SIGNIFICANT_FLOW, (
                f"Top flow value {abs_flow} MW seems too small for case {row['case']}"
            )


class TestBusNumberValidity:
    """Tests to verify bus numbers are valid for the respective case files."""

    @pytest.fixture
    def evidence_df(self):
        """Load the evidence sheet from the Excel file."""
        return pd.read_excel(OUTPUT_FILE, sheet_name="evidence")

    def test_case57_bus_numbers_in_valid_range(self, evidence_df):
        """Verify case57 bus numbers are within valid range (1-57)."""
        case57_row = evidence_df[evidence_df["case"] == "case57"]
        if len(case57_row) > 0:
            fbus = int(case57_row["top_fbus"].iloc[0])
            tbus = int(case57_row["top_tbus"].iloc[0])
            assert 1 <= fbus <= 57, f"case57 top_fbus {fbus} out of range [1, 57]"
            assert 1 <= tbus <= 57, f"case57 top_tbus {tbus} out of range [1, 57]"

    def test_case118_bus_numbers_in_valid_range(self, evidence_df):
        """Verify case118 bus numbers are within valid range (1-118)."""
        case118_row = evidence_df[evidence_df["case"] == "case118"]
        if len(case118_row) > 0:
            fbus = int(case118_row["top_fbus"].iloc[0])
            tbus = int(case118_row["top_tbus"].iloc[0])
            assert 1 <= fbus <= 118, f"case118 top_fbus {fbus} out of range [1, 118]"
            assert 1 <= tbus <= 118, f"case118 top_tbus {tbus} out of range [1, 118]"

    def test_pglib118_bus_numbers_in_valid_range(self, evidence_df):
        """Verify pglib118 bus numbers are within valid range (1-118)."""
        pglib118_row = evidence_df[evidence_df["case"] == "pglib118"]
        if len(pglib118_row) > 0:
            fbus = int(pglib118_row["top_fbus"].iloc[0])
            tbus = int(pglib118_row["top_tbus"].iloc[0])
            assert 1 <= fbus <= 118, f"pglib118 top_fbus {fbus} out of range [1, 118]"
            assert 1 <= tbus <= 118, f"pglib118 top_tbus {tbus} out of range [1, 118]"


class TestColumnOrder:
    """Tests to verify column ordering (optional but good for consistency)."""

    @pytest.fixture
    def result_df(self):
        """Load the result sheet from the Excel file."""
        return pd.read_excel(OUTPUT_FILE, sheet_name="result")

    @pytest.fixture
    def evidence_df(self):
        """Load the evidence sheet from the Excel file."""
        return pd.read_excel(OUTPUT_FILE, sheet_name="evidence")

    def test_result_has_all_required_columns(self, result_df):
        """Verify result sheet has all required columns."""
        required_columns = {"corridor_fbus", "corridor_tbus", "cases_where_topflow"}
        actual_columns = set(result_df.columns)
        missing = required_columns - actual_columns
        assert not missing, f"Missing required columns in result sheet: {missing}"

    def test_evidence_has_all_required_columns(self, evidence_df):
        """Verify evidence sheet has all required columns."""
        required_columns = {
            "case", "top_fbus", "top_tbus",
            "top_abs_flow_mw", "top_flow_mw_signed", "baseMVA"
        }
        actual_columns = set(evidence_df.columns)
        missing = required_columns - actual_columns
        assert not missing, f"Missing required columns in evidence sheet: {missing}"
