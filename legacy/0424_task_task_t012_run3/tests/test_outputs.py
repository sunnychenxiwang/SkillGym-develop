import json
import math
import os

import pytest


class TestMostCriticalBranch:
    """Tests for verifying the most critical branch output."""

    OUTPUT_FILE = "/root/output/most_critical_branch.json"

    EXPECTED_RESULT = {
        "case_name": "pglib_opf_case118_ieee",
        "fbus": 38,
        "tbus": 65,
        "abs_flow_mw": 353.11266121412024,
        "edge_betweenness": 0.2574439527829361,
        "score": 90.90671928066487,
    }

    TOLERANCE = 1e-6

    REQUIRED_FIELDS = ["case_name", "fbus", "tbus", "abs_flow_mw", "edge_betweenness", "score"]

    VALID_CASE_NAMES = ["case57", "case118", "pglib_opf_case118_ieee"]

    def test_output_file_exists(self):
        """Verify the output file was created."""
        assert os.path.exists(self.OUTPUT_FILE), f"Output file not found: {self.OUTPUT_FILE}"

    def test_output_valid_json(self):
        """Verify output is valid JSON format."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert isinstance(data, dict), "Output should be a JSON object"

    def test_has_required_fields(self):
        """Verify all required fields are present."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        for field in self.REQUIRED_FIELDS:
            assert field in data, f"Missing required field: {field}"

    def test_no_extra_fields(self):
        """Verify no unexpected fields are present."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        for field in data.keys():
            assert field in self.REQUIRED_FIELDS, f"Unexpected field: {field}"

    def test_case_name_type(self):
        """Verify case_name is a string."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert isinstance(data["case_name"], str), "case_name should be a string"

    def test_case_name_valid(self):
        """Verify case_name is one of the expected values."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert data["case_name"] in self.VALID_CASE_NAMES, (
            f"case_name should be one of {self.VALID_CASE_NAMES}, got {data['case_name']}"
        )

    def test_fbus_type(self):
        """Verify fbus is an integer."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert isinstance(data["fbus"], int), "fbus should be an integer"

    def test_tbus_type(self):
        """Verify tbus is an integer."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert isinstance(data["tbus"], int), "tbus should be an integer"

    def test_abs_flow_mw_type(self):
        """Verify abs_flow_mw is a number."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert isinstance(data["abs_flow_mw"], (int, float)), "abs_flow_mw should be a number"

    def test_edge_betweenness_type(self):
        """Verify edge_betweenness is a number."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert isinstance(data["edge_betweenness"], (int, float)), "edge_betweenness should be a number"

    def test_score_type(self):
        """Verify score is a number."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert isinstance(data["score"], (int, float)), "score should be a number"

    def test_abs_flow_mw_positive(self):
        """Verify abs_flow_mw is non-negative."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert data["abs_flow_mw"] >= 0, "abs_flow_mw should be non-negative"

    def test_edge_betweenness_range(self):
        """Verify edge_betweenness is in valid range [0, 1]."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert 0 <= data["edge_betweenness"] <= 1, "edge_betweenness should be in [0, 1]"

    def test_score_positive(self):
        """Verify score is non-negative."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert data["score"] >= 0, "score should be non-negative"

    def test_fbus_positive(self):
        """Verify fbus is a positive integer."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert data["fbus"] > 0, "fbus should be a positive integer"

    def test_tbus_positive(self):
        """Verify tbus is a positive integer."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert data["tbus"] > 0, "tbus should be a positive integer"

    def test_case_name_value(self):
        """Verify case_name matches expected value."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert data["case_name"] == self.EXPECTED_RESULT["case_name"], (
            f"case_name mismatch: expected {self.EXPECTED_RESULT['case_name']}, got {data['case_name']}"
        )

    def test_fbus_value(self):
        """Verify fbus matches expected value."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert data["fbus"] == self.EXPECTED_RESULT["fbus"], (
            f"fbus mismatch: expected {self.EXPECTED_RESULT['fbus']}, got {data['fbus']}"
        )

    def test_tbus_value(self):
        """Verify tbus matches expected value."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert data["tbus"] == self.EXPECTED_RESULT["tbus"], (
            f"tbus mismatch: expected {self.EXPECTED_RESULT['tbus']}, got {data['tbus']}"
        )

    def test_abs_flow_mw_value(self):
        """Verify abs_flow_mw matches expected value within tolerance."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert math.isclose(data["abs_flow_mw"], self.EXPECTED_RESULT["abs_flow_mw"], rel_tol=self.TOLERANCE), (
            f"abs_flow_mw mismatch: expected {self.EXPECTED_RESULT['abs_flow_mw']}, got {data['abs_flow_mw']}"
        )

    def test_edge_betweenness_value(self):
        """Verify edge_betweenness matches expected value within tolerance."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert math.isclose(data["edge_betweenness"], self.EXPECTED_RESULT["edge_betweenness"], rel_tol=self.TOLERANCE), (
            f"edge_betweenness mismatch: expected {self.EXPECTED_RESULT['edge_betweenness']}, got {data['edge_betweenness']}"
        )

    def test_score_value(self):
        """Verify score matches expected value within tolerance."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert math.isclose(data["score"], self.EXPECTED_RESULT["score"], rel_tol=self.TOLERANCE), (
            f"score mismatch: expected {self.EXPECTED_RESULT['score']}, got {data['score']}"
        )

    def test_score_calculation_consistency(self):
        """Verify score equals abs_flow_mw * edge_betweenness."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        calculated_score = data["abs_flow_mw"] * data["edge_betweenness"]
        assert math.isclose(data["score"], calculated_score, rel_tol=self.TOLERANCE), (
            f"score should equal abs_flow_mw * edge_betweenness: expected {calculated_score}, got {data['score']}"
        )
