"""Auto-generated expectation tests for DC power flow stress metrics verification.

These tests verify that the task execution produces correct outputs
based on the instruction requirements for computing DC power flow
stress indices from MATPOWER case files.
"""

import json
import math
import os
from pathlib import Path

import pytest


# Constants
OUTPUT_FILE_PATH = "/root/powerflow_stress_metrics.json"
INPUT_DIR = "/root/harbor_workspaces/task_T406_run2/input"

# Expected case names
EXPECTED_CASES = ["case57", "case118", "pglib_opf_case118_ieee"]

# Required JSON schema keys
REQUIRED_TOP_LEVEL_KEYS = [
    "case57",
    "case118",
    "pglib_opf_case118_ieee",
    "comparative_stress_ratio_pglib_over_case118"
]


class TestOutputFileExists:
    """Tests to verify output file existence and basic properties."""

    def test_output_file_exists(self):
        """Verify output file was created at the specified path."""
        assert os.path.exists(OUTPUT_FILE_PATH), (
            f"Output file not found at {OUTPUT_FILE_PATH}"
        )

    def test_output_file_is_not_empty(self):
        """Verify output file is not empty."""
        assert os.path.exists(OUTPUT_FILE_PATH), "Output file does not exist"
        file_size = os.path.getsize(OUTPUT_FILE_PATH)
        assert file_size > 0, "Output file is empty"

    def test_output_file_has_json_extension(self):
        """Verify output file has .json extension."""
        assert OUTPUT_FILE_PATH.endswith(".json"), (
            "Output file should have .json extension"
        )


class TestJsonValidity:
    """Tests to verify JSON format validity."""

    def test_output_is_valid_json(self):
        """Verify output is valid JSON format."""
        assert os.path.exists(OUTPUT_FILE_PATH), "Output file does not exist"
        with open(OUTPUT_FILE_PATH) as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                pytest.fail(f"Output file is not valid JSON: {e}")
        assert data is not None, "JSON data is None"

    def test_json_root_is_object(self):
        """Verify JSON root element is an object (dict)."""
        with open(OUTPUT_FILE_PATH) as f:
            data = json.load(f)
        assert isinstance(data, dict), (
            f"JSON root should be an object/dict, got {type(data).__name__}"
        )


class TestJsonSchema:
    """Tests to verify JSON schema compliance."""

    @pytest.fixture
    def json_data(self):
        """Load JSON data from output file."""
        with open(OUTPUT_FILE_PATH) as f:
            return json.load(f)

    def test_all_required_keys_present(self, json_data):
        """Verify all required top-level keys are present."""
        for key in REQUIRED_TOP_LEVEL_KEYS:
            assert key in json_data, f"Missing required key: {key}"

    def test_no_extra_top_level_keys(self, json_data):
        """Verify no unexpected top-level keys are present."""
        expected_keys = set(REQUIRED_TOP_LEVEL_KEYS)
        actual_keys = set(json_data.keys())
        extra_keys = actual_keys - expected_keys
        assert not extra_keys, f"Unexpected top-level keys: {extra_keys}"

    def test_case57_has_stress_index_key(self, json_data):
        """Verify case57 object has stress_index key."""
        assert "case57" in json_data, "Missing case57 key"
        assert isinstance(json_data["case57"], dict), "case57 should be an object"
        assert "stress_index" in json_data["case57"], (
            "case57 missing stress_index key"
        )

    def test_case118_has_stress_index_key(self, json_data):
        """Verify case118 object has stress_index key."""
        assert "case118" in json_data, "Missing case118 key"
        assert isinstance(json_data["case118"], dict), "case118 should be an object"
        assert "stress_index" in json_data["case118"], (
            "case118 missing stress_index key"
        )

    def test_pglib_case_has_stress_index_key(self, json_data):
        """Verify pglib_opf_case118_ieee object has stress_index key."""
        key = "pglib_opf_case118_ieee"
        assert key in json_data, f"Missing {key} key"
        assert isinstance(json_data[key], dict), f"{key} should be an object"
        assert "stress_index" in json_data[key], f"{key} missing stress_index key"

    def test_case_objects_have_only_stress_index(self, json_data):
        """Verify each case object contains only stress_index key."""
        for case_name in EXPECTED_CASES:
            case_data = json_data[case_name]
            assert set(case_data.keys()) == {"stress_index"}, (
                f"{case_name} should only have 'stress_index' key, "
                f"got: {list(case_data.keys())}"
            )


class TestDataTypes:
    """Tests to verify correct data types for all values."""

    @pytest.fixture
    def json_data(self):
        """Load JSON data from output file."""
        with open(OUTPUT_FILE_PATH) as f:
            return json.load(f)

    def test_case57_stress_index_is_number(self, json_data):
        """Verify case57 stress_index is a number."""
        value = json_data["case57"]["stress_index"]
        assert isinstance(value, (int, float)), (
            f"case57 stress_index should be a number, got {type(value).__name__}"
        )

    def test_case118_stress_index_is_number(self, json_data):
        """Verify case118 stress_index is a number."""
        value = json_data["case118"]["stress_index"]
        assert isinstance(value, (int, float)), (
            f"case118 stress_index should be a number, got {type(value).__name__}"
        )

    def test_pglib_stress_index_is_number(self, json_data):
        """Verify pglib_opf_case118_ieee stress_index is a number."""
        value = json_data["pglib_opf_case118_ieee"]["stress_index"]
        assert isinstance(value, (int, float)), (
            f"pglib stress_index should be a number, got {type(value).__name__}"
        )

    def test_comparative_ratio_is_number(self, json_data):
        """Verify comparative_stress_ratio is a number."""
        value = json_data["comparative_stress_ratio_pglib_over_case118"]
        assert isinstance(value, (int, float)), (
            f"comparative_stress_ratio should be a number, got {type(value).__name__}"
        )

    def test_all_values_are_finite(self, json_data):
        """Verify all numeric values are finite (not inf or nan)."""
        values_to_check = [
            ("case57.stress_index", json_data["case57"]["stress_index"]),
            ("case118.stress_index", json_data["case118"]["stress_index"]),
            ("pglib.stress_index", json_data["pglib_opf_case118_ieee"]["stress_index"]),
            ("comparative_ratio", json_data["comparative_stress_ratio_pglib_over_case118"]),
        ]
        for name, value in values_to_check:
            assert math.isfinite(value), f"{name} is not finite: {value}"


class TestValueRanges:
    """Tests to verify values are within reasonable ranges."""

    @pytest.fixture
    def json_data(self):
        """Load JSON data from output file."""
        with open(OUTPUT_FILE_PATH) as f:
            return json.load(f)

    def test_case57_stress_index_is_positive(self, json_data):
        """Verify case57 stress_index is positive."""
        value = json_data["case57"]["stress_index"]
        assert value > 0, f"case57 stress_index should be positive, got {value}"

    def test_case118_stress_index_is_positive(self, json_data):
        """Verify case118 stress_index is positive."""
        value = json_data["case118"]["stress_index"]
        assert value > 0, f"case118 stress_index should be positive, got {value}"

    def test_pglib_stress_index_is_positive(self, json_data):
        """Verify pglib_opf_case118_ieee stress_index is positive."""
        value = json_data["pglib_opf_case118_ieee"]["stress_index"]
        assert value > 0, f"pglib stress_index should be positive, got {value}"

    def test_comparative_ratio_is_positive(self, json_data):
        """Verify comparative_stress_ratio is positive."""
        value = json_data["comparative_stress_ratio_pglib_over_case118"]
        assert value > 0, f"comparative_stress_ratio should be positive, got {value}"

    def test_stress_indices_are_reasonable(self, json_data):
        """Verify stress indices are in a reasonable range.

        Stress Index = 95th percentile of |branch MW flows| / total load
        This ratio should typically be less than 2.0 for realistic power systems
        (the 95th percentile flow shouldn't exceed 2x total load).
        """
        for case_name in EXPECTED_CASES:
            value = json_data[case_name]["stress_index"]
            assert 0 < value < 10.0, (
                f"{case_name} stress_index {value} is outside reasonable range (0, 10)"
            )


class TestPrecisionRequirements:
    """Tests to verify decimal precision requirements."""

    @pytest.fixture
    def json_data(self):
        """Load JSON data from output file."""
        with open(OUTPUT_FILE_PATH) as f:
            return json.load(f)

    def test_values_have_at_most_6_decimal_places(self, json_data):
        """Verify all values are rounded to at most 6 decimal places."""
        values_to_check = [
            ("case57.stress_index", json_data["case57"]["stress_index"]),
            ("case118.stress_index", json_data["case118"]["stress_index"]),
            ("pglib.stress_index", json_data["pglib_opf_case118_ieee"]["stress_index"]),
            ("comparative_ratio", json_data["comparative_stress_ratio_pglib_over_case118"]),
        ]

        for name, value in values_to_check:
            # Convert to string and check decimal places
            str_value = f"{value:.15f}".rstrip('0')
            if '.' in str_value:
                decimal_places = len(str_value.split('.')[1])
                assert decimal_places <= 6, (
                    f"{name} has {decimal_places} decimal places, "
                    f"expected at most 6. Value: {value}"
                )


class TestComparativeStressRatioCalculation:
    """Tests to verify correct calculation of comparative stress ratio."""

    @pytest.fixture
    def json_data(self):
        """Load JSON data from output file."""
        with open(OUTPUT_FILE_PATH) as f:
            return json.load(f)

    def test_comparative_ratio_equals_pglib_over_case118(self, json_data):
        """Verify comparative ratio = pglib stress_index / case118 stress_index."""
        pglib_stress = json_data["pglib_opf_case118_ieee"]["stress_index"]
        case118_stress = json_data["case118"]["stress_index"]
        reported_ratio = json_data["comparative_stress_ratio_pglib_over_case118"]

        expected_ratio = pglib_stress / case118_stress

        # Allow for rounding differences (6 decimal places)
        assert abs(reported_ratio - expected_ratio) < 1e-5, (
            f"comparative_stress_ratio ({reported_ratio}) does not match "
            f"pglib/case118 ({expected_ratio})"
        )


class TestInputFilesExist:
    """Tests to verify input files exist (precondition checks)."""

    def test_case57_input_exists(self):
        """Verify case57.m input file exists."""
        path = os.path.join(INPUT_DIR, "case57.m")
        assert os.path.exists(path), f"Input file not found: {path}"

    def test_case118_input_exists(self):
        """Verify case118.m input file exists."""
        path = os.path.join(INPUT_DIR, "case118.m")
        assert os.path.exists(path), f"Input file not found: {path}"

    def test_pglib_input_exists(self):
        """Verify pglib_opf_case118_ieee.m input file exists."""
        path = os.path.join(INPUT_DIR, "pglib_opf_case118_ieee.m")
        assert os.path.exists(path), f"Input file not found: {path}"


class TestConsistencyChecks:
    """Tests for internal consistency of the results."""

    @pytest.fixture
    def json_data(self):
        """Load JSON data from output file."""
        with open(OUTPUT_FILE_PATH) as f:
            return json.load(f)

    def test_different_cases_have_different_stress_indices(self, json_data):
        """Verify the three cases produce different stress indices.

        case57 has a different network topology than the 118-bus cases,
        and pglib_opf_case118_ieee has different generation dispatch than case118.
        """
        case57_stress = json_data["case57"]["stress_index"]
        case118_stress = json_data["case118"]["stress_index"]
        pglib_stress = json_data["pglib_opf_case118_ieee"]["stress_index"]

        # case57 should differ from 118-bus cases (different network size)
        assert case57_stress != case118_stress, (
            "case57 and case118 have identical stress indices - unexpected"
        )
        assert case57_stress != pglib_stress, (
            "case57 and pglib have identical stress indices - unexpected"
        )

    def test_118_bus_cases_may_differ(self, json_data):
        """Verify the two 118-bus cases may have different stress indices.

        case118 and pglib_opf_case118_ieee have the same topology but
        different generation dispatch, so stress indices may differ.
        """
        case118_stress = json_data["case118"]["stress_index"]
        pglib_stress = json_data["pglib_opf_case118_ieee"]["stress_index"]

        # They can be equal or different - just verify both are valid
        assert case118_stress > 0, "case118 stress_index should be positive"
        assert pglib_stress > 0, "pglib stress_index should be positive"


class TestDeterminism:
    """Tests to verify deterministic behavior of calculations."""

    @pytest.fixture
    def json_data(self):
        """Load JSON data from output file."""
        with open(OUTPUT_FILE_PATH) as f:
            return json.load(f)

    def test_stress_index_not_zero(self, json_data):
        """Verify stress indices are not exactly zero.

        With non-trivial power systems, there should always be some
        power flow on at least one branch.
        """
        for case_name in EXPECTED_CASES:
            value = json_data[case_name]["stress_index"]
            assert value != 0.0, (
                f"{case_name} stress_index is exactly 0.0, "
                "which is unexpected for a non-trivial power system"
            )

    def test_ratio_not_exactly_one(self, json_data):
        """Verify comparative ratio is not exactly 1.0.

        The two 118-bus cases have different generation dispatch,
        so their stress indices should typically differ.
        """
        ratio = json_data["comparative_stress_ratio_pglib_over_case118"]
        # Note: It's possible but unlikely for them to be exactly equal
        # This is a soft check - if they are equal, the test will still pass
        # but log a warning-level message
        if ratio == 1.0:
            pytest.skip(
                "Comparative ratio is exactly 1.0 - both 118-bus cases "
                "have identical stress indices (unusual but possible)"
            )


class TestOutputDirectory:
    """Tests to verify output directory structure."""

    def test_output_directory_exists(self):
        """Verify output directory exists."""
        output_dir = os.path.dirname(OUTPUT_FILE_PATH)
        assert os.path.isdir(output_dir), f"Output directory not found: {output_dir}"

    def test_output_file_is_regular_file(self):
        """Verify output is a regular file (not a directory or symlink)."""
        assert os.path.exists(OUTPUT_FILE_PATH), "Output file does not exist"
        assert os.path.isfile(OUTPUT_FILE_PATH), (
            f"{OUTPUT_FILE_PATH} is not a regular file"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
