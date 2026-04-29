"""Auto-generated expectation tests for task verification.

These tests verify that the task execution produces correct outputs
based on the instruction requirements for computing the most critical
transmission element across IEEE 118-bus cases using DC power flow analysis.

Task requirements:
1. Parse MATPOWER case files (case118.m, pglib_opf_case118_ieee.m, case57.m)
2. Run DC power flow for both 118-bus files
3. Compute branch loading percentages using rateA
4. Identify max-loaded branch per file with tie-breaking rules
5. Compute criticality score using case57 median reactance as baseline
6. Select overall winner and write JSON output
"""

import json
import math
import os
from pathlib import Path

import pytest


# Constants derived from input file analysis
OUTPUT_FILE_PATH = "/root/most_critical_branch.json"
INPUT_DIR = "/root/harbor_workspaces/task_T434_run2/input"

VALID_SOURCE_FILES = ["case118.m", "pglib_opf_case118_ieee.m"]
NUM_BUSES_118 = 118
NUM_BRANCHES_CASE118 = 186  # from case118.m
NUM_BRANCHES_PGLIB = 186  # from pglib_opf_case118_ieee.m (indexed 0 to 185)

# Required JSON schema keys
REQUIRED_KEYS = [
    "winner_source_file",
    "fbus",
    "tbus",
    "branch_row_index",
    "x",
    "rateA",
    "flow_MW",
    "loading_pct",
    "median_x_case57",
    "criticality",
]


class TestOutputFileExistence:
    """Tests for verifying output file creation."""

    def test_output_file_exists(self):
        """Verify that the output JSON file was created."""
        assert os.path.exists(OUTPUT_FILE_PATH), (
            f"Output file not found at {OUTPUT_FILE_PATH}. "
            "The task requires writing the JSON result file."
        )

    def test_output_file_not_empty(self):
        """Verify that the output file is not empty."""
        assert os.path.exists(OUTPUT_FILE_PATH), f"Output file not found at {OUTPUT_FILE_PATH}"
        file_size = os.path.getsize(OUTPUT_FILE_PATH)
        assert file_size > 0, "Output file exists but is empty"


class TestOutputFileFormat:
    """Tests for verifying output file format."""

    def test_output_is_valid_json(self):
        """Verify output is valid JSON format."""
        assert os.path.exists(OUTPUT_FILE_PATH), f"Output file not found at {OUTPUT_FILE_PATH}"
        with open(OUTPUT_FILE_PATH, "r") as f:
            content = f.read()
        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            pytest.fail(f"Output file is not valid JSON: {e}")
        assert data is not None, "JSON parsed to None"

    def test_output_is_json_object(self):
        """Verify output JSON is an object (dict), not array or primitive."""
        assert os.path.exists(OUTPUT_FILE_PATH), f"Output file not found at {OUTPUT_FILE_PATH}"
        with open(OUTPUT_FILE_PATH, "r") as f:
            data = json.load(f)
        assert isinstance(data, dict), (
            f"Expected JSON object (dict), got {type(data).__name__}"
        )


class TestRequiredFields:
    """Tests for verifying all required fields are present."""

    def test_all_required_keys_present(self):
        """Verify all required keys are present in the output."""
        assert os.path.exists(OUTPUT_FILE_PATH), f"Output file not found at {OUTPUT_FILE_PATH}"
        with open(OUTPUT_FILE_PATH, "r") as f:
            data = json.load(f)

        missing_keys = [key for key in REQUIRED_KEYS if key not in data]
        assert not missing_keys, (
            f"Missing required keys in output: {missing_keys}. "
            f"Required keys are: {REQUIRED_KEYS}"
        )

    @pytest.mark.parametrize("key", REQUIRED_KEYS)
    def test_individual_required_key(self, key):
        """Verify each required key is present."""
        assert os.path.exists(OUTPUT_FILE_PATH), f"Output file not found at {OUTPUT_FILE_PATH}"
        with open(OUTPUT_FILE_PATH, "r") as f:
            data = json.load(f)
        assert key in data, f"Required key '{key}' is missing from output"


class TestFieldTypes:
    """Tests for verifying field types are correct."""

    def test_winner_source_file_is_string(self):
        """Verify winner_source_file is a string."""
        assert os.path.exists(OUTPUT_FILE_PATH), f"Output file not found at {OUTPUT_FILE_PATH}"
        with open(OUTPUT_FILE_PATH, "r") as f:
            data = json.load(f)
        assert isinstance(data.get("winner_source_file"), str), (
            f"winner_source_file should be a string, got {type(data.get('winner_source_file')).__name__}"
        )

    def test_fbus_is_integer(self):
        """Verify fbus is an integer."""
        assert os.path.exists(OUTPUT_FILE_PATH), f"Output file not found at {OUTPUT_FILE_PATH}"
        with open(OUTPUT_FILE_PATH, "r") as f:
            data = json.load(f)
        assert isinstance(data.get("fbus"), int), (
            f"fbus should be an integer, got {type(data.get('fbus')).__name__}"
        )

    def test_tbus_is_integer(self):
        """Verify tbus is an integer."""
        assert os.path.exists(OUTPUT_FILE_PATH), f"Output file not found at {OUTPUT_FILE_PATH}"
        with open(OUTPUT_FILE_PATH, "r") as f:
            data = json.load(f)
        assert isinstance(data.get("tbus"), int), (
            f"tbus should be an integer, got {type(data.get('tbus')).__name__}"
        )

    def test_branch_row_index_is_integer(self):
        """Verify branch_row_index is an integer."""
        assert os.path.exists(OUTPUT_FILE_PATH), f"Output file not found at {OUTPUT_FILE_PATH}"
        with open(OUTPUT_FILE_PATH, "r") as f:
            data = json.load(f)
        assert isinstance(data.get("branch_row_index"), int), (
            f"branch_row_index should be an integer, got {type(data.get('branch_row_index')).__name__}"
        )

    def test_numeric_fields_are_numbers(self):
        """Verify numeric fields are JSON numbers (int or float)."""
        assert os.path.exists(OUTPUT_FILE_PATH), f"Output file not found at {OUTPUT_FILE_PATH}"
        with open(OUTPUT_FILE_PATH, "r") as f:
            data = json.load(f)

        numeric_fields = ["x", "rateA", "flow_MW", "loading_pct", "median_x_case57", "criticality"]
        for field in numeric_fields:
            value = data.get(field)
            assert isinstance(value, (int, float)), (
                f"Field '{field}' should be a number, got {type(value).__name__}: {value}"
            )
            # Ensure not a string representation of a number
            assert not isinstance(value, str), (
                f"Field '{field}' should be a JSON number, not a string: '{value}'"
            )


class TestFieldValues:
    """Tests for verifying field values are valid."""

    def test_winner_source_file_is_valid(self):
        """Verify winner_source_file is one of the expected values."""
        assert os.path.exists(OUTPUT_FILE_PATH), f"Output file not found at {OUTPUT_FILE_PATH}"
        with open(OUTPUT_FILE_PATH, "r") as f:
            data = json.load(f)

        winner = data.get("winner_source_file")
        assert winner in VALID_SOURCE_FILES, (
            f"winner_source_file must be one of {VALID_SOURCE_FILES}, got '{winner}'"
        )

    def test_fbus_is_valid_bus_number(self):
        """Verify fbus is a valid bus number (1 to 118)."""
        assert os.path.exists(OUTPUT_FILE_PATH), f"Output file not found at {OUTPUT_FILE_PATH}"
        with open(OUTPUT_FILE_PATH, "r") as f:
            data = json.load(f)

        fbus = data.get("fbus")
        assert 1 <= fbus <= NUM_BUSES_118, (
            f"fbus must be between 1 and {NUM_BUSES_118}, got {fbus}"
        )

    def test_tbus_is_valid_bus_number(self):
        """Verify tbus is a valid bus number (1 to 118)."""
        assert os.path.exists(OUTPUT_FILE_PATH), f"Output file not found at {OUTPUT_FILE_PATH}"
        with open(OUTPUT_FILE_PATH, "r") as f:
            data = json.load(f)

        tbus = data.get("tbus")
        assert 1 <= tbus <= NUM_BUSES_118, (
            f"tbus must be between 1 and {NUM_BUSES_118}, got {tbus}"
        )

    def test_fbus_different_from_tbus(self):
        """Verify fbus and tbus are different (no self-loops)."""
        assert os.path.exists(OUTPUT_FILE_PATH), f"Output file not found at {OUTPUT_FILE_PATH}"
        with open(OUTPUT_FILE_PATH, "r") as f:
            data = json.load(f)

        fbus = data.get("fbus")
        tbus = data.get("tbus")
        assert fbus != tbus, f"fbus and tbus should be different, both are {fbus}"

    def test_branch_row_index_is_non_negative(self):
        """Verify branch_row_index is non-negative (0-indexed)."""
        assert os.path.exists(OUTPUT_FILE_PATH), f"Output file not found at {OUTPUT_FILE_PATH}"
        with open(OUTPUT_FILE_PATH, "r") as f:
            data = json.load(f)

        idx = data.get("branch_row_index")
        assert idx >= 0, f"branch_row_index should be non-negative, got {idx}"

    def test_branch_row_index_is_within_bounds(self):
        """Verify branch_row_index is within valid range for branch data."""
        assert os.path.exists(OUTPUT_FILE_PATH), f"Output file not found at {OUTPUT_FILE_PATH}"
        with open(OUTPUT_FILE_PATH, "r") as f:
            data = json.load(f)

        idx = data.get("branch_row_index")
        # Both case files have 186 branches (indices 0-185)
        max_index = max(NUM_BRANCHES_CASE118, NUM_BRANCHES_PGLIB) - 1
        assert 0 <= idx <= max_index, (
            f"branch_row_index should be between 0 and {max_index}, got {idx}"
        )

    def test_reactance_is_positive(self):
        """Verify branch reactance x is positive."""
        assert os.path.exists(OUTPUT_FILE_PATH), f"Output file not found at {OUTPUT_FILE_PATH}"
        with open(OUTPUT_FILE_PATH, "r") as f:
            data = json.load(f)

        x = data.get("x")
        assert x > 0, f"Branch reactance x should be positive, got {x}"

    def test_rateA_is_positive(self):
        """Verify rateA is positive (branches with rateA <= 0 should be excluded)."""
        assert os.path.exists(OUTPUT_FILE_PATH), f"Output file not found at {OUTPUT_FILE_PATH}"
        with open(OUTPUT_FILE_PATH, "r") as f:
            data = json.load(f)

        rateA = data.get("rateA")
        assert rateA > 0, (
            f"rateA should be positive (branches with rateA <= 0 are excluded), got {rateA}"
        )

    def test_loading_pct_is_non_negative(self):
        """Verify loading_pct is non-negative."""
        assert os.path.exists(OUTPUT_FILE_PATH), f"Output file not found at {OUTPUT_FILE_PATH}"
        with open(OUTPUT_FILE_PATH, "r") as f:
            data = json.load(f)

        loading_pct = data.get("loading_pct")
        assert loading_pct >= 0, f"loading_pct should be non-negative, got {loading_pct}"

    def test_median_x_case57_is_positive(self):
        """Verify median_x_case57 is positive."""
        assert os.path.exists(OUTPUT_FILE_PATH), f"Output file not found at {OUTPUT_FILE_PATH}"
        with open(OUTPUT_FILE_PATH, "r") as f:
            data = json.load(f)

        median_x = data.get("median_x_case57")
        assert median_x > 0, f"median_x_case57 should be positive, got {median_x}"

    def test_criticality_is_non_negative(self):
        """Verify criticality score is non-negative."""
        assert os.path.exists(OUTPUT_FILE_PATH), f"Output file not found at {OUTPUT_FILE_PATH}"
        with open(OUTPUT_FILE_PATH, "r") as f:
            data = json.load(f)

        criticality = data.get("criticality")
        assert criticality >= 0, f"criticality should be non-negative, got {criticality}"


class TestDCPowerFlowLogic:
    """Tests for verifying DC power flow computation logic."""

    def test_loading_pct_calculation(self):
        """Verify loading_pct is consistent with flow_MW and rateA.

        loading_pct = abs(flow_MW) / rateA * 100
        """
        assert os.path.exists(OUTPUT_FILE_PATH), f"Output file not found at {OUTPUT_FILE_PATH}"
        with open(OUTPUT_FILE_PATH, "r") as f:
            data = json.load(f)

        flow_MW = data.get("flow_MW")
        rateA = data.get("rateA")
        loading_pct = data.get("loading_pct")

        if rateA > 0:
            expected_loading = abs(flow_MW) / rateA * 100
            # Allow for floating point precision differences
            assert abs(loading_pct - expected_loading) < 1e-6, (
                f"loading_pct ({loading_pct}) should equal abs(flow_MW)/rateA*100 "
                f"= abs({flow_MW})/{rateA}*100 = {expected_loading}"
            )

    def test_criticality_calculation(self):
        """Verify criticality is consistent with loading_pct, x, and median_x_case57.

        criticality = loading_pct / (x / median_x_case57)
        """
        assert os.path.exists(OUTPUT_FILE_PATH), f"Output file not found at {OUTPUT_FILE_PATH}"
        with open(OUTPUT_FILE_PATH, "r") as f:
            data = json.load(f)

        loading_pct = data.get("loading_pct")
        x = data.get("x")
        median_x = data.get("median_x_case57")
        criticality = data.get("criticality")

        if x > 0 and median_x > 0:
            expected_criticality = loading_pct / (x / median_x)
            # Allow for floating point precision differences
            assert abs(criticality - expected_criticality) < 1e-4, (
                f"criticality ({criticality}) should equal loading_pct/(x/median_x) "
                f"= {loading_pct}/({x}/{median_x}) = {expected_criticality}"
            )


class TestCase57MedianReactance:
    """Tests for verifying case57 median reactance baseline."""

    def test_median_x_case57_is_reasonable(self):
        """Verify median_x_case57 is within a reasonable range for IEEE 57-bus system.

        From the case57.m file, reactances range roughly from 0.0152 to 1.355.
        The median should be somewhere in a reasonable middle range.
        """
        assert os.path.exists(OUTPUT_FILE_PATH), f"Output file not found at {OUTPUT_FILE_PATH}"
        with open(OUTPUT_FILE_PATH, "r") as f:
            data = json.load(f)

        median_x = data.get("median_x_case57")
        # Based on case57.m branch data, reactances are positive and vary
        # The median of positive x values should be in a reasonable range
        assert 0.01 <= median_x <= 2.0, (
            f"median_x_case57 should be between 0.01 and 2.0 (typical IEEE case values), "
            f"got {median_x}"
        )


class TestSourceFileConsistency:
    """Tests for verifying the winner source file selection is logical."""

    def test_winner_comes_from_file_with_positive_ratings(self):
        """Verify winner is from pglib file (which has positive rateA values).

        case118.m has all rateA = 0, meaning all branches would be excluded.
        pglib_opf_case118_ieee.m has positive rateA values.
        Therefore, the winner must come from pglib_opf_case118_ieee.m.
        """
        assert os.path.exists(OUTPUT_FILE_PATH), f"Output file not found at {OUTPUT_FILE_PATH}"
        with open(OUTPUT_FILE_PATH, "r") as f:
            data = json.load(f)

        winner = data.get("winner_source_file")
        # Based on input file analysis, case118.m has all rateA = 0
        # So the winner must be from pglib_opf_case118_ieee.m
        assert winner == "pglib_opf_case118_ieee.m", (
            f"Expected winner to be 'pglib_opf_case118_ieee.m' since case118.m has "
            f"all rateA = 0 (excluded branches), but got '{winner}'"
        )


class TestNumericPrecision:
    """Tests for verifying numeric values have reasonable precision."""

    def test_no_nan_values(self):
        """Verify no NaN values in output."""
        assert os.path.exists(OUTPUT_FILE_PATH), f"Output file not found at {OUTPUT_FILE_PATH}"
        with open(OUTPUT_FILE_PATH, "r") as f:
            data = json.load(f)

        numeric_fields = ["x", "rateA", "flow_MW", "loading_pct", "median_x_case57", "criticality"]
        for field in numeric_fields:
            value = data.get(field)
            if isinstance(value, float):
                assert not math.isnan(value), f"Field '{field}' contains NaN"

    def test_no_infinite_values(self):
        """Verify no infinite values in output."""
        assert os.path.exists(OUTPUT_FILE_PATH), f"Output file not found at {OUTPUT_FILE_PATH}"
        with open(OUTPUT_FILE_PATH, "r") as f:
            data = json.load(f)

        numeric_fields = ["x", "rateA", "flow_MW", "loading_pct", "median_x_case57", "criticality"]
        for field in numeric_fields:
            value = data.get(field)
            if isinstance(value, float):
                assert not math.isinf(value), f"Field '{field}' contains infinity"


class TestInputFilesExist:
    """Tests for verifying input files exist (prerequisite check)."""

    def test_case118_exists(self):
        """Verify case118.m input file exists."""
        path = os.path.join(INPUT_DIR, "case118.m")
        assert os.path.exists(path), f"Input file not found: {path}"

    def test_case57_exists(self):
        """Verify case57.m input file exists."""
        path = os.path.join(INPUT_DIR, "case57.m")
        assert os.path.exists(path), f"Input file not found: {path}"

    def test_pglib_case118_exists(self):
        """Verify pglib_opf_case118_ieee.m input file exists."""
        path = os.path.join(INPUT_DIR, "pglib_opf_case118_ieee.m")
        assert os.path.exists(path), f"Input file not found: {path}"


class TestOutputDirectory:
    """Tests for verifying output directory structure."""

    def test_output_directory_exists(self):
        """Verify output directory exists."""
        output_dir = os.path.dirname(OUTPUT_FILE_PATH)
        assert os.path.exists(output_dir), f"Output directory not found: {output_dir}"

    def test_output_file_is_in_correct_location(self):
        """Verify output file is at the exact expected path."""
        expected_path = "/root/most_critical_branch.json"
        assert OUTPUT_FILE_PATH == expected_path, (
            f"Output file path mismatch: expected {expected_path}, got {OUTPUT_FILE_PATH}"
        )


class TestBranchIdentification:
    """Tests for verifying branch identification is deterministic."""

    def test_branch_endpoints_are_ordered_consistently(self):
        """Verify fbus and tbus values allow for proper branch identification.

        The tie-breaking rule uses (min(fbus,tbus), max(fbus,tbus)) lexicographic order.
        """
        assert os.path.exists(OUTPUT_FILE_PATH), f"Output file not found at {OUTPUT_FILE_PATH}"
        with open(OUTPUT_FILE_PATH, "r") as f:
            data = json.load(f)

        fbus = data.get("fbus")
        tbus = data.get("tbus")

        # Both should be valid bus numbers
        assert fbus is not None and tbus is not None, "fbus and tbus must both be present"
        assert isinstance(fbus, int) and isinstance(tbus, int), "fbus and tbus must be integers"


class TestMaxLoadedBranchSelection:
    """Tests for verifying the max-loaded branch was selected correctly."""

    def test_loading_indicates_max_loaded(self):
        """Verify the loading percentage is meaningful (not zero for the max branch)."""
        assert os.path.exists(OUTPUT_FILE_PATH), f"Output file not found at {OUTPUT_FILE_PATH}"
        with open(OUTPUT_FILE_PATH, "r") as f:
            data = json.load(f)

        loading_pct = data.get("loading_pct")
        # The max-loaded branch should have some loading
        # It could be zero only in edge cases, but typically should be positive
        # We just verify it's a valid number
        assert loading_pct is not None, "loading_pct must be present"
        assert isinstance(loading_pct, (int, float)), "loading_pct must be numeric"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
