"""Auto-generated expectation tests for task verification.

These tests verify that the task execution produces correct outputs
for identifying the airline with highest mean arrival delay on SEA->LAX
route on 2014-01-01.
"""

import csv
import json
import math
import os
from pathlib import Path

import pytest


# Constants
OUTPUT_FILE = "/root/sea_lax_worst_airline_2014-01-01.json"
FLIGHTS_FILE = "/root/flights_2.csv"
AIRLINES_FILE = "/root/airlines.csv"

# Expected schema keys (exact set, no more, no less)
EXPECTED_KEYS = {
    "date",
    "origin",
    "dest",
    "carrier_code",
    "carrier_name",
    "mean_arr_delay_minutes",
    "flight_count_used",
}


class TestFileExistence:
    """Tests for verifying output file creation."""

    def test_output_file_exists(self):
        """Verify output file was created at the expected path."""
        assert os.path.exists(OUTPUT_FILE), f"Output file not found at {OUTPUT_FILE}"

    def test_output_file_is_not_empty(self):
        """Verify output file is not empty."""
        assert os.path.getsize(OUTPUT_FILE) > 0, "Output file is empty"


class TestJsonFormat:
    """Tests for verifying JSON format validity."""

    def test_output_is_valid_json(self):
        """Verify output is valid JSON format."""
        with open(OUTPUT_FILE, "r") as f:
            content = f.read()
        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            pytest.fail(f"Output file is not valid JSON: {e}")
        assert data is not None

    def test_output_is_json_object(self):
        """Verify output is a JSON object (dict), not array or primitive."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        assert isinstance(data, dict), f"Expected JSON object, got {type(data).__name__}"


class TestSchemaValidation:
    """Tests for verifying JSON schema matches specification."""

    def test_all_required_keys_present(self):
        """Verify all required keys are present in output."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        missing_keys = EXPECTED_KEYS - set(data.keys())
        assert not missing_keys, f"Missing required keys: {missing_keys}"

    def test_no_extra_keys(self):
        """Verify no extra keys beyond the schema specification."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        extra_keys = set(data.keys()) - EXPECTED_KEYS
        assert not extra_keys, f"Extra keys found (not allowed): {extra_keys}"

    def test_exact_key_set(self):
        """Verify exact match of keys with schema."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        assert set(data.keys()) == EXPECTED_KEYS, (
            f"Key mismatch. Expected: {EXPECTED_KEYS}, Got: {set(data.keys())}"
        )


class TestDataTypes:
    """Tests for verifying data types of output fields."""

    def test_date_is_string(self):
        """Verify 'date' field is a string."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        assert isinstance(data["date"], str), f"'date' should be string, got {type(data['date']).__name__}"

    def test_origin_is_string(self):
        """Verify 'origin' field is a string."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        assert isinstance(data["origin"], str), f"'origin' should be string, got {type(data['origin']).__name__}"

    def test_dest_is_string(self):
        """Verify 'dest' field is a string."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        assert isinstance(data["dest"], str), f"'dest' should be string, got {type(data['dest']).__name__}"

    def test_carrier_code_is_string(self):
        """Verify 'carrier_code' field is a string."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        assert isinstance(data["carrier_code"], str), f"'carrier_code' should be string, got {type(data['carrier_code']).__name__}"

    def test_carrier_name_is_string(self):
        """Verify 'carrier_name' field is a string."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        assert isinstance(data["carrier_name"], str), f"'carrier_name' should be string, got {type(data['carrier_name']).__name__}"

    def test_mean_arr_delay_minutes_is_number(self):
        """Verify 'mean_arr_delay_minutes' field is a JSON number (int or float)."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        assert isinstance(data["mean_arr_delay_minutes"], (int, float)), (
            f"'mean_arr_delay_minutes' should be number, got {type(data['mean_arr_delay_minutes']).__name__}"
        )

    def test_flight_count_used_is_integer(self):
        """Verify 'flight_count_used' field is an integer."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        # JSON integers are loaded as int in Python
        assert isinstance(data["flight_count_used"], int), (
            f"'flight_count_used' should be integer, got {type(data['flight_count_used']).__name__}"
        )
        # Also verify it's not a float masquerading as int
        assert data["flight_count_used"] == int(data["flight_count_used"]), (
            "'flight_count_used' should be a whole number"
        )


class TestValueConstraints:
    """Tests for verifying specific value constraints."""

    def test_date_value(self):
        """Verify 'date' field has the correct value '2014-01-01'."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        assert data["date"] == "2014-01-01", f"Expected date='2014-01-01', got '{data['date']}'"

    def test_origin_value(self):
        """Verify 'origin' field is 'SEA'."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        assert data["origin"] == "SEA", f"Expected origin='SEA', got '{data['origin']}'"

    def test_dest_value(self):
        """Verify 'dest' field is 'LAX'."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        assert data["dest"] == "LAX", f"Expected dest='LAX', got '{data['dest']}'"

    def test_flight_count_positive(self):
        """Verify 'flight_count_used' is positive (at least one flight)."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        assert data["flight_count_used"] > 0, (
            f"Expected flight_count_used > 0, got {data['flight_count_used']}"
        )

    def test_mean_arr_delay_rounded_to_2_decimals(self):
        """Verify 'mean_arr_delay_minutes' is rounded to exactly 2 decimal places."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        value = data["mean_arr_delay_minutes"]
        # Round to 2 decimals and compare
        rounded_value = round(value, 2)
        assert abs(value - rounded_value) < 1e-10, (
            f"'mean_arr_delay_minutes' should be rounded to 2 decimal places, got {value}"
        )

    def test_carrier_code_not_empty(self):
        """Verify 'carrier_code' is not an empty string."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        assert data["carrier_code"] != "", "'carrier_code' should not be empty"


class TestCarrierValidation:
    """Tests for verifying carrier code and name are valid."""

    def test_carrier_code_exists_in_flights(self):
        """Verify carrier_code actually exists in the flights data for SEA->LAX on 2014-01-01."""
        with open(OUTPUT_FILE, "r") as f:
            output_data = json.load(f)

        # Get all unique carriers for SEA->LAX on 2014-01-01 from flights data
        valid_carriers = set()
        with open(FLIGHTS_FILE, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if (row["year"] == "2014" and row["month"] == "1" and row["day"] == "1"
                    and row["origin"] == "SEA" and row["dest"] == "LAX"
                    and row["arr_delay"] != "NA"):
                    valid_carriers.add(row["carrier"])

        assert output_data["carrier_code"] in valid_carriers, (
            f"carrier_code '{output_data['carrier_code']}' not found in SEA->LAX flights on 2014-01-01. "
            f"Valid carriers: {valid_carriers}"
        )

    def test_carrier_name_matches_code(self):
        """Verify carrier_name matches the lookup from airlines.csv for the given carrier_code."""
        with open(OUTPUT_FILE, "r") as f:
            output_data = json.load(f)

        # Build lookup from airlines.csv
        code_to_name = {}
        with open(AIRLINES_FILE, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                code_to_name[row["Code"]] = row["Description"]

        carrier_code = output_data["carrier_code"]
        expected_name = code_to_name.get(carrier_code, "")

        assert output_data["carrier_name"] == expected_name, (
            f"carrier_name mismatch. For carrier_code='{carrier_code}', "
            f"expected '{expected_name}', got '{output_data['carrier_name']}'"
        )


class TestDataCorrectness:
    """Tests for verifying the computation is correct."""

    def test_flight_count_matches_actual_data(self):
        """Verify flight_count_used matches the actual number of valid flights for the reported carrier."""
        with open(OUTPUT_FILE, "r") as f:
            output_data = json.load(f)

        carrier_code = output_data["carrier_code"]

        # Count valid flights for this carrier on SEA->LAX on 2014-01-01
        actual_count = 0
        with open(FLIGHTS_FILE, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if (row["year"] == "2014" and row["month"] == "1" and row["day"] == "1"
                    and row["origin"] == "SEA" and row["dest"] == "LAX"
                    and row["carrier"] == carrier_code
                    and row["arr_delay"] != "NA"):
                    actual_count += 1

        assert output_data["flight_count_used"] == actual_count, (
            f"flight_count_used mismatch for carrier '{carrier_code}'. "
            f"Expected {actual_count}, got {output_data['flight_count_used']}"
        )

    def test_mean_arr_delay_matches_actual_data(self):
        """Verify mean_arr_delay_minutes matches the actual computed mean for the reported carrier."""
        with open(OUTPUT_FILE, "r") as f:
            output_data = json.load(f)

        carrier_code = output_data["carrier_code"]

        # Compute actual mean for this carrier on SEA->LAX on 2014-01-01
        delays = []
        with open(FLIGHTS_FILE, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if (row["year"] == "2014" and row["month"] == "1" and row["day"] == "1"
                    and row["origin"] == "SEA" and row["dest"] == "LAX"
                    and row["carrier"] == carrier_code
                    and row["arr_delay"] != "NA"):
                    delays.append(float(row["arr_delay"]))

        if delays:
            expected_mean = round(sum(delays) / len(delays), 2)
            assert output_data["mean_arr_delay_minutes"] == expected_mean, (
                f"mean_arr_delay_minutes mismatch for carrier '{carrier_code}'. "
                f"Expected {expected_mean}, got {output_data['mean_arr_delay_minutes']}"
            )

    def test_selected_carrier_has_highest_mean_delay(self):
        """Verify the selected carrier actually has the highest mean arrival delay."""
        with open(OUTPUT_FILE, "r") as f:
            output_data = json.load(f)

        # Compute mean delay for all carriers on SEA->LAX on 2014-01-01
        carrier_delays = {}  # carrier -> list of delays
        with open(FLIGHTS_FILE, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if (row["year"] == "2014" and row["month"] == "1" and row["day"] == "1"
                    and row["origin"] == "SEA" and row["dest"] == "LAX"
                    and row["arr_delay"] != "NA"):
                    carrier = row["carrier"]
                    if carrier not in carrier_delays:
                        carrier_delays[carrier] = []
                    carrier_delays[carrier].append(float(row["arr_delay"]))

        # Compute means
        carrier_stats = {}  # carrier -> (mean, count)
        for carrier, delays in carrier_delays.items():
            mean_delay = sum(delays) / len(delays)
            carrier_stats[carrier] = (mean_delay, len(delays), carrier)

        # Find the max according to tie-breaking rules:
        # 1. Maximum mean
        # 2. If tie, larger flight_count_used
        # 3. If still tie, lexicographically smallest carrier_code
        def sort_key(item):
            carrier, (mean, count, code) = item
            return (-mean, -count, code)

        sorted_carriers = sorted(carrier_stats.items(), key=sort_key)
        expected_carrier = sorted_carriers[0][0] if sorted_carriers else None

        assert output_data["carrier_code"] == expected_carrier, (
            f"Selected carrier mismatch. Expected '{expected_carrier}' "
            f"(highest mean delay with tie-breaking), got '{output_data['carrier_code']}'"
        )


class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""

    def test_mean_delay_can_be_negative(self):
        """Verify that mean_arr_delay_minutes can be negative (early arrivals)."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        # This is a validity check - mean delay can be any real number
        assert isinstance(data["mean_arr_delay_minutes"], (int, float)), (
            "mean_arr_delay_minutes should be a number (can be negative)"
        )

    def test_no_na_values_included_in_computation(self):
        """Verify that NA values are properly excluded from the computation."""
        with open(OUTPUT_FILE, "r") as f:
            output_data = json.load(f)

        carrier_code = output_data["carrier_code"]

        # Count total flights vs valid flights (non-NA arr_delay)
        total_flights = 0
        valid_flights = 0
        with open(FLIGHTS_FILE, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if (row["year"] == "2014" and row["month"] == "1" and row["day"] == "1"
                    and row["origin"] == "SEA" and row["dest"] == "LAX"
                    and row["carrier"] == carrier_code):
                    total_flights += 1
                    if row["arr_delay"] != "NA":
                        valid_flights += 1

        # The flight_count_used should match valid flights (non-NA only)
        assert output_data["flight_count_used"] == valid_flights, (
            f"flight_count_used should only count non-NA arr_delay flights. "
            f"Total flights: {total_flights}, Valid flights: {valid_flights}, "
            f"Reported: {output_data['flight_count_used']}"
        )
