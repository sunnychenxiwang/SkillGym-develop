import json
import math
import os

import pytest


class TestSeaLaxBestCarrier2014:
    """Tests for verifying SEA-LAX best carrier 2014 output."""

    OUTPUT_FILE = "/root/output/sea_lax_best_carrier_2014.json"

    EXPECTED_RESULT = {
        "route": "SEA-LAX",
        "year": 2014,
        "winning_carrier_code": "VX",
        "winning_carrier_name": "Virgin America",
        "on_time_rate": 0.9183187946074544,
        "total_flights_included": 1261,
    }

    REQUIRED_FIELDS = [
        "route",
        "year",
        "winning_carrier_code",
        "winning_carrier_name",
        "on_time_rate",
        "total_flights_included",
    ]

    TOLERANCE = 0.0001

    # ==================== Structural Tests ====================

    def test_output_file_exists(self):
        """Verify output file was created."""
        assert os.path.exists(self.OUTPUT_FILE), f"Output file not found: {self.OUTPUT_FILE}"

    def test_valid_json_format(self):
        """Verify output is valid JSON."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert isinstance(data, dict), "JSON root should be an object/dict"

    # ==================== Content Tests ====================

    def test_has_required_fields(self):
        """Verify all required fields are present."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        for field in self.REQUIRED_FIELDS:
            assert field in data, f"Missing required field: {field}"

    def test_no_extra_fields(self):
        """Verify JSON contains only the required keys (no extras)."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        extra_keys = set(data.keys()) - set(self.REQUIRED_FIELDS)
        assert len(extra_keys) == 0, f"Found unexpected extra keys: {extra_keys}"

    def test_field_types(self):
        """Verify all fields have correct data types."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        assert isinstance(data["route"], str), "route should be a string"
        assert isinstance(data["year"], int), "year should be an integer"
        assert isinstance(data["winning_carrier_code"], str), "winning_carrier_code should be a string"
        assert isinstance(data["winning_carrier_name"], str), "winning_carrier_name should be a string"
        assert isinstance(data["on_time_rate"], (int, float)), "on_time_rate should be a number"
        assert isinstance(data["total_flights_included"], int), "total_flights_included should be an integer"

    def test_on_time_rate_in_valid_range(self):
        """Verify on_time_rate is a proportion in [0, 1]."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        rate = data["on_time_rate"]
        assert 0.0 <= rate <= 1.0, f"on_time_rate should be in [0, 1], got {rate}"

    # ==================== Value Tests ====================

    def test_route_value(self):
        """Verify route is SEA-LAX."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert data["route"] == self.EXPECTED_RESULT["route"], \
            f"route mismatch: expected {self.EXPECTED_RESULT['route']}, got {data['route']}"

    def test_year_value(self):
        """Verify year is 2014."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert data["year"] == self.EXPECTED_RESULT["year"], \
            f"year mismatch: expected {self.EXPECTED_RESULT['year']}, got {data['year']}"

    def test_winning_carrier_code_value(self):
        """Verify winning carrier code is VX (Virgin America)."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert data["winning_carrier_code"] == self.EXPECTED_RESULT["winning_carrier_code"], \
            f"winning_carrier_code mismatch: expected {self.EXPECTED_RESULT['winning_carrier_code']}, got {data['winning_carrier_code']}"

    def test_winning_carrier_name_value(self):
        """Verify winning carrier name is Virgin America."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert data["winning_carrier_name"] == self.EXPECTED_RESULT["winning_carrier_name"], \
            f"winning_carrier_name mismatch: expected {self.EXPECTED_RESULT['winning_carrier_name']}, got {data['winning_carrier_name']}"

    def test_on_time_rate_value(self):
        """Verify on_time_rate matches expected value (with tolerance)."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert math.isclose(
            data["on_time_rate"],
            self.EXPECTED_RESULT["on_time_rate"],
            rel_tol=self.TOLERANCE
        ), f"on_time_rate mismatch: expected {self.EXPECTED_RESULT['on_time_rate']}, got {data['on_time_rate']}"

    def test_total_flights_included_value(self):
        """Verify total_flights_included matches expected value."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert data["total_flights_included"] == self.EXPECTED_RESULT["total_flights_included"], \
            f"total_flights_included mismatch: expected {self.EXPECTED_RESULT['total_flights_included']}, got {data['total_flights_included']}"

    def test_total_flights_included_positive(self):
        """Verify total_flights_included is a positive integer."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert data["total_flights_included"] > 0, \
            f"total_flights_included should be positive, got {data['total_flights_included']}"
