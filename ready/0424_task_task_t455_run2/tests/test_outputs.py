import json
import math
import os

import pytest


class TestOutputs:
    """Tests for verifying task outputs."""

    EXPECTED_RESULT = {
        "carrier_code": "HA",
        "carrier_name": "Hawaiian Airlines Inc.",
        "n_flights": 1094,
        "distance_slope": 0.059266
    }
    TOLERANCE = 1e-6  # For 6 decimal place precision

    OUTPUT_FILE = "/root/output/steepest_distance_delay_carrier.json"

    # Structural Tests

    def test_output_file_exists(self):
        """Verify output file was created."""
        assert os.path.exists(self.OUTPUT_FILE), f"Output file not found: {self.OUTPUT_FILE}"

    def test_valid_json(self):
        """Verify output is valid JSON."""
        with open(self.OUTPUT_FILE) as f:
            json.load(f)

    # Content Tests

    def test_has_required_fields(self):
        """Verify all required fields are present."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        required_fields = ["carrier_code", "carrier_name", "n_flights", "distance_slope"]
        for field in required_fields:
            assert field in data, f"Missing required field: {field}"

    def test_no_extra_fields(self):
        """Verify no extra fields beyond the required schema."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        expected_fields = {"carrier_code", "carrier_name", "n_flights", "distance_slope"}
        actual_fields = set(data.keys())

        extra_fields = actual_fields - expected_fields
        assert len(extra_fields) == 0, f"Unexpected extra fields found: {extra_fields}"

        assert len(actual_fields) == 4, f"Expected exactly 4 fields, found {len(actual_fields)}"

    def test_field_types(self):
        """Verify data types are correct."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        assert isinstance(data["carrier_code"], str), \
            f"carrier_code should be string, got {type(data['carrier_code'])}"

        assert isinstance(data["carrier_name"], (str, type(None))), \
            f"carrier_name should be string or null, got {type(data['carrier_name'])}"

        assert isinstance(data["n_flights"], int), \
            f"n_flights should be integer, got {type(data['n_flights'])}"

        assert isinstance(data["distance_slope"], (int, float)), \
            f"distance_slope should be numeric, got {type(data['distance_slope'])}"

    # Value Tests

    def test_carrier_code_correct(self):
        """Verify carrier_code matches expected value."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        assert data["carrier_code"] == self.EXPECTED_RESULT["carrier_code"], \
            f"carrier_code mismatch: expected {self.EXPECTED_RESULT['carrier_code']}, got {data['carrier_code']}"

    def test_carrier_name_correct(self):
        """Verify carrier_name matches expected value."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        assert data["carrier_name"] == self.EXPECTED_RESULT["carrier_name"], \
            f"carrier_name mismatch: expected {self.EXPECTED_RESULT['carrier_name']}, got {data['carrier_name']}"

    def test_n_flights_correct(self):
        """Verify n_flights matches expected value."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        assert data["n_flights"] == self.EXPECTED_RESULT["n_flights"], \
            f"n_flights mismatch: expected {self.EXPECTED_RESULT['n_flights']}, got {data['n_flights']}"

    def test_distance_slope_correct(self):
        """Verify distance_slope matches expected value within tolerance."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        assert math.isclose(data["distance_slope"], self.EXPECTED_RESULT["distance_slope"], abs_tol=self.TOLERANCE), \
            f"distance_slope mismatch: expected {self.EXPECTED_RESULT['distance_slope']}, got {data['distance_slope']}"

    def test_distance_slope_precision(self):
        """Verify distance_slope is rounded to 6 decimal places."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        slope_str = str(data["distance_slope"])
        if '.' in slope_str:
            decimal_places = len(slope_str.split('.')[1])
            assert decimal_places <= 6, \
                f"distance_slope should have at most 6 decimal places, found {decimal_places}"

    def test_n_flights_positive(self):
        """Verify n_flights is positive (at least 30 per task requirements)."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        assert data["n_flights"] >= 30, \
            f"n_flights should be at least 30 (task requirement), got {data['n_flights']}"

    def test_distance_slope_positive(self):
        """Verify distance_slope is positive (task requires strongest positive relationship)."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        assert data["distance_slope"] > 0, \
            f"distance_slope should be positive, got {data['distance_slope']}"
