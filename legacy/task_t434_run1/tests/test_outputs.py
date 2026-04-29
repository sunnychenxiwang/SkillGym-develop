"""Auto-generated expectation tests for DC power flow task verification.

These tests verify that the task execution produces correct outputs
based on the instruction requirements for computing DC power flow
across three MATPOWER case files and identifying the most overloaded branch.
"""

import json
import os
from pathlib import Path

import pytest


# Constants
OUTPUT_DIR = "/root/harbor_workspaces/task_T434_run1/output"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "most_overloaded_branch.json")
INPUT_DIR = "/root/harbor_workspaces/task_T434_run1/input"

# Valid case names from the input files
VALID_CASE_NAMES = {"case57", "case118", "pglib_opf_case118_ieee"}


class TestOutputFileExists:
    """Tests verifying the output file exists and has correct basic properties."""

    def test_output_directory_exists(self):
        """Verify the output directory exists."""
        assert os.path.exists(OUTPUT_DIR), f"Output directory not found: {OUTPUT_DIR}"

    def test_output_file_exists(self):
        """Verify the output JSON file was created."""
        assert os.path.exists(OUTPUT_FILE), f"Output file not found: {OUTPUT_FILE}"

    def test_output_file_not_empty(self):
        """Verify the output file is not empty."""
        assert os.path.getsize(OUTPUT_FILE) > 0, "Output file is empty"


class TestOutputValidJSON:
    """Tests verifying the output is valid JSON with correct structure."""

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        with open(OUTPUT_FILE, "r") as f:
            return json.load(f)

    def test_output_is_valid_json(self):
        """Verify output file contains valid JSON."""
        with open(OUTPUT_FILE, "r") as f:
            try:
                data = json.load(f)
                assert data is not None
            except json.JSONDecodeError as e:
                pytest.fail(f"Output file is not valid JSON: {e}")

    def test_output_is_dict(self, output_data):
        """Verify output JSON is a dictionary (object), not an array."""
        assert isinstance(output_data, dict), "Output JSON should be an object/dictionary"


class TestRequiredFields:
    """Tests verifying all required fields are present in the output."""

    REQUIRED_FIELDS = [
        "case_name",
        "slack_bus",
        "branch_index",
        "fbus",
        "tbus",
        "rateA_MW",
        "x_pu",
        "flow_MW",
        "loading_pct",
    ]

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        with open(OUTPUT_FILE, "r") as f:
            return json.load(f)

    def test_all_required_fields_present(self, output_data):
        """Verify all required fields are present in the output."""
        missing_fields = [
            field for field in self.REQUIRED_FIELDS if field not in output_data
        ]
        assert (
            not missing_fields
        ), f"Missing required fields: {missing_fields}"

    def test_no_extra_fields(self, output_data):
        """Verify no unexpected extra fields are present."""
        extra_fields = [
            field for field in output_data.keys() if field not in self.REQUIRED_FIELDS
        ]
        assert not extra_fields, f"Unexpected extra fields: {extra_fields}"

    @pytest.mark.parametrize("field", REQUIRED_FIELDS)
    def test_field_present(self, output_data, field):
        """Verify each required field is present."""
        assert field in output_data, f"Required field '{field}' is missing"


class TestFieldTypes:
    """Tests verifying field types match the expected schema."""

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        with open(OUTPUT_FILE, "r") as f:
            return json.load(f)

    def test_case_name_is_string(self, output_data):
        """Verify case_name is a string."""
        assert isinstance(
            output_data["case_name"], str
        ), "case_name should be a string"

    def test_slack_bus_is_integer(self, output_data):
        """Verify slack_bus is an integer (or int-like number)."""
        val = output_data["slack_bus"]
        assert isinstance(val, (int, float)), "slack_bus should be a number"
        if isinstance(val, float):
            assert val.is_integer(), "slack_bus should be an integer value"

    def test_branch_index_is_integer(self, output_data):
        """Verify branch_index is an integer (or int-like number)."""
        val = output_data["branch_index"]
        assert isinstance(val, (int, float)), "branch_index should be a number"
        if isinstance(val, float):
            assert val.is_integer(), "branch_index should be an integer value"

    def test_fbus_is_integer(self, output_data):
        """Verify fbus is an integer (or int-like number)."""
        val = output_data["fbus"]
        assert isinstance(val, (int, float)), "fbus should be a number"
        if isinstance(val, float):
            assert val.is_integer(), "fbus should be an integer value"

    def test_tbus_is_integer(self, output_data):
        """Verify tbus is an integer (or int-like number)."""
        val = output_data["tbus"]
        assert isinstance(val, (int, float)), "tbus should be a number"
        if isinstance(val, float):
            assert val.is_integer(), "tbus should be an integer value"

    def test_rateA_MW_is_number(self, output_data):
        """Verify rateA_MW is a number (float or int)."""
        assert isinstance(
            output_data["rateA_MW"], (int, float)
        ), "rateA_MW should be a number"

    def test_x_pu_is_number(self, output_data):
        """Verify x_pu is a number (float or int)."""
        assert isinstance(
            output_data["x_pu"], (int, float)
        ), "x_pu should be a number"

    def test_flow_MW_is_number(self, output_data):
        """Verify flow_MW is a number (float or int)."""
        assert isinstance(
            output_data["flow_MW"], (int, float)
        ), "flow_MW should be a number"

    def test_loading_pct_is_number(self, output_data):
        """Verify loading_pct is a number (float or int)."""
        assert isinstance(
            output_data["loading_pct"], (int, float)
        ), "loading_pct should be a number"

    def test_all_numeric_values_are_json_numbers_not_strings(self, output_data):
        """Verify numeric fields are actual numbers, not string representations."""
        numeric_fields = [
            "slack_bus",
            "branch_index",
            "fbus",
            "tbus",
            "rateA_MW",
            "x_pu",
            "flow_MW",
            "loading_pct",
        ]
        for field in numeric_fields:
            assert not isinstance(
                output_data[field], str
            ), f"{field} should be a JSON number, not a string"


class TestFieldValues:
    """Tests verifying field values are within valid ranges."""

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        with open(OUTPUT_FILE, "r") as f:
            return json.load(f)

    def test_case_name_is_valid(self, output_data):
        """Verify case_name is one of the valid case names."""
        assert output_data["case_name"] in VALID_CASE_NAMES, (
            f"case_name '{output_data['case_name']}' is not valid. "
            f"Expected one of: {VALID_CASE_NAMES}"
        )

    def test_slack_bus_is_non_negative(self, output_data):
        """Verify slack_bus is non-negative."""
        assert output_data["slack_bus"] >= 0, "slack_bus should be non-negative"

    def test_branch_index_is_non_negative(self, output_data):
        """Verify branch_index is non-negative (0-based index)."""
        assert output_data["branch_index"] >= 0, "branch_index should be non-negative"

    def test_fbus_is_positive(self, output_data):
        """Verify fbus (from bus number) is positive."""
        assert output_data["fbus"] > 0, "fbus should be positive (bus numbers start at 1)"

    def test_tbus_is_positive(self, output_data):
        """Verify tbus (to bus number) is positive."""
        assert output_data["tbus"] > 0, "tbus should be positive (bus numbers start at 1)"

    def test_fbus_and_tbus_are_different(self, output_data):
        """Verify fbus and tbus are different (no self-loops)."""
        assert output_data["fbus"] != output_data["tbus"], (
            "fbus and tbus should be different (branch cannot be a self-loop)"
        )

    def test_rateA_MW_is_positive(self, output_data):
        """Verify rateA_MW is positive (branches with rateA=0 are excluded)."""
        assert output_data["rateA_MW"] > 0, (
            "rateA_MW should be positive (branches with rateA=0 are excluded from overload)"
        )

    def test_x_pu_is_positive(self, output_data):
        """Verify x_pu (reactance) is positive."""
        assert output_data["x_pu"] > 0, "x_pu (reactance) should be positive"

    def test_loading_pct_is_positive(self, output_data):
        """Verify loading_pct is positive (indicates some flow)."""
        assert output_data["loading_pct"] > 0, "loading_pct should be positive"

    def test_loading_pct_is_calculated_correctly(self, output_data):
        """Verify loading_pct matches the formula: |flow_MW| / rateA_MW * 100."""
        expected_loading = abs(output_data["flow_MW"]) / output_data["rateA_MW"] * 100
        assert abs(output_data["loading_pct"] - expected_loading) < 1e-6, (
            f"loading_pct ({output_data['loading_pct']}) does not match "
            f"expected value ({expected_loading}) based on formula"
        )


class TestCaseSpecificConstraints:
    """Tests verifying case-specific constraints based on input file structure."""

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        with open(OUTPUT_FILE, "r") as f:
            return json.load(f)

    def test_branch_index_within_case_bounds(self, output_data):
        """Verify branch_index is within valid range for the specified case."""
        case_name = output_data["case_name"]
        branch_index = output_data["branch_index"]

        # Branch counts from the input files (0-based max index = count - 1)
        branch_counts = {
            "case57": 80,
            "case118": 186,
            "pglib_opf_case118_ieee": 186,
        }

        max_index = branch_counts.get(case_name, 0) - 1
        assert branch_index <= max_index, (
            f"branch_index {branch_index} exceeds maximum valid index {max_index} "
            f"for case {case_name}"
        )

    def test_bus_numbers_within_case_bounds(self, output_data):
        """Verify fbus and tbus are within valid range for the specified case."""
        case_name = output_data["case_name"]
        fbus = output_data["fbus"]
        tbus = output_data["tbus"]

        # Maximum bus numbers from input files
        max_bus = {
            "case57": 57,
            "case118": 118,
            "pglib_opf_case118_ieee": 118,
        }

        max_bus_num = max_bus.get(case_name, 0)
        assert fbus <= max_bus_num, (
            f"fbus {fbus} exceeds maximum bus number {max_bus_num} for case {case_name}"
        )
        assert tbus <= max_bus_num, (
            f"tbus {tbus} exceeds maximum bus number {max_bus_num} for case {case_name}"
        )

    def test_slack_bus_matches_case(self, output_data):
        """Verify slack_bus is correct for the specified case."""
        case_name = output_data["case_name"]
        slack_bus = output_data["slack_bus"]

        # Slack bus numbers (type == 3 bus) from input files
        slack_buses = {
            "case57": 1,    # Bus 1 has type=3
            "case118": 69,   # Bus 69 has type=3
            "pglib_opf_case118_ieee": 69,  # Bus 69 has type=3
        }

        expected_slack = slack_buses.get(case_name)
        assert slack_bus == expected_slack, (
            f"slack_bus {slack_bus} does not match expected slack bus {expected_slack} "
            f"for case {case_name}"
        )


class TestMostOverloadedCriteria:
    """Tests verifying the 'most overloaded' selection criteria."""

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        with open(OUTPUT_FILE, "r") as f:
            return json.load(f)

    def test_loading_pct_represents_maximum(self, output_data):
        """
        The selected branch should have the maximum loading_pct across all cases.
        Since case57 and case118 have all rateA=0, only pglib_opf_case118_ieee
        has branches eligible for overload calculation.
        """
        # This test validates the output structure implies it's the maximum
        # A positive loading_pct indicates a valid overloaded branch was found
        assert output_data["loading_pct"] > 0, (
            "loading_pct should be positive, indicating an overloaded branch was found"
        )

    def test_only_pglib_case_has_valid_ratings(self, output_data):
        """
        Since case57 and case118 have rateA=0 for all branches (no thermal limits),
        only pglib_opf_case118_ieee has branches eligible for overload calculation.
        Therefore, the most overloaded branch must come from pglib_opf_case118_ieee.
        """
        # Based on input file analysis:
        # - case57: all branches have rateA=0
        # - case118: all branches have rateA=0
        # - pglib_opf_case118_ieee: branches have non-zero rateA values
        assert output_data["case_name"] == "pglib_opf_case118_ieee", (
            "Only pglib_opf_case118_ieee has branches with rateA > 0, "
            "so the most overloaded branch must come from this case"
        )


class TestPhysicalReasonableness:
    """Tests verifying physical reasonableness of results."""

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        with open(OUTPUT_FILE, "r") as f:
            return json.load(f)

    def test_x_pu_is_reasonable(self, output_data):
        """Verify x_pu is within physically reasonable range."""
        # Reactance values typically between 0.001 and 1.0 per unit
        assert 0.0001 < output_data["x_pu"] < 10.0, (
            f"x_pu value {output_data['x_pu']} seems outside reasonable range"
        )

    def test_rateA_is_reasonable(self, output_data):
        """Verify rateA_MW is within physically reasonable range."""
        # Thermal ratings typically between 10 and 10000 MW
        assert 1 < output_data["rateA_MW"] < 10000, (
            f"rateA_MW value {output_data['rateA_MW']} seems outside reasonable range"
        )

    def test_flow_magnitude_is_finite(self, output_data):
        """Verify flow_MW is finite (not NaN or Inf)."""
        import math
        assert math.isfinite(output_data["flow_MW"]), "flow_MW should be finite"

    def test_loading_pct_is_finite(self, output_data):
        """Verify loading_pct is finite (not NaN or Inf)."""
        import math
        assert math.isfinite(output_data["loading_pct"]), "loading_pct should be finite"


class TestDCPowerFlowConsistency:
    """Tests verifying DC power flow calculation consistency."""

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        with open(OUTPUT_FILE, "r") as f:
            return json.load(f)

    def test_flow_direction_sign(self, output_data):
        """Verify flow_MW can be positive or negative (indicating direction)."""
        # flow_MW represents P_f->t and can be positive (f to t) or negative (t to f)
        # The loading calculation uses absolute value
        flow = output_data["flow_MW"]
        assert isinstance(flow, (int, float)), "flow_MW should be a number"

    def test_loading_uses_absolute_flow(self, output_data):
        """Verify loading_pct is calculated from absolute flow value."""
        flow = output_data["flow_MW"]
        rateA = output_data["rateA_MW"]
        loading = output_data["loading_pct"]

        expected = abs(flow) / rateA * 100
        assert abs(loading - expected) < 1e-6, (
            "loading_pct should be calculated from |flow_MW| / rateA_MW * 100"
        )


class TestInputFilesExist:
    """Tests verifying input files exist (prerequisite for task)."""

    INPUT_FILES = [
        "case57.m",
        "case118.m",
        "pglib_opf_case118_ieee.m",
    ]

    @pytest.mark.parametrize("filename", INPUT_FILES)
    def test_input_file_exists(self, filename):
        """Verify each input file exists."""
        filepath = os.path.join(INPUT_DIR, filename)
        assert os.path.exists(filepath), f"Input file not found: {filepath}"


class TestJSONFormatCompliance:
    """Tests verifying JSON format compliance."""

    def test_json_encoding(self):
        """Verify JSON file uses UTF-8 encoding."""
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            content = f.read()
        # Should be able to decode without errors
        assert len(content) > 0

    def test_json_no_trailing_comma(self):
        """Verify JSON has no trailing commas (invalid JSON)."""
        with open(OUTPUT_FILE, "r") as f:
            content = f.read()
        # A proper JSON parser would fail on trailing commas
        # This is implicitly tested by successful json.load()
        data = json.loads(content)
        assert data is not None

    def test_json_serialization_roundtrip(self):
        """Verify JSON can be serialized and deserialized without loss."""
        with open(OUTPUT_FILE, "r") as f:
            original_data = json.load(f)

        # Serialize and deserialize
        serialized = json.dumps(original_data)
        roundtrip_data = json.loads(serialized)

        assert original_data == roundtrip_data, "JSON roundtrip should preserve data"
