"""Auto-generated expectation tests for task verification.

These tests verify that the task execution produces correct outputs
based on the instruction requirements for identifying the airline with
the worst on-time performance (highest mean arrival delay).
"""

import json
import math
import os
import re
from pathlib import Path

import pytest

# Constants
OUTPUT_FILE = "/root/worst_airline_by_mean_arr_delay.json"
FLIGHTS_FILE = "/root/flights_2.csv"
AIRLINES_FILE = "/root/airlines.csv"

# Missing value markers to exclude - ALL UPPERCASE for consistent comparison
# Compare using value.strip().upper() in MISSING_VALUE_MARKERS
MISSING_VALUE_MARKERS = {'', 'NA', 'NAN', 'N/A', 'NULL', 'NONE', 'NaN'}


def is_missing_value(value):
    """Check if a value should be treated as missing/NA.

    Handles None, empty strings, whitespace-only strings, and common NA markers
    in a case-insensitive manner.

    Args:
        value: The value to check (may be None, string, or other type)

    Returns:
        True if the value should be treated as missing, False otherwise
    """
    if value is None:
        return True
    if not isinstance(value, str):
        # Non-string, non-None values are not missing
        return False
    stripped = value.strip()
    if stripped == '':
        return True
    # Case-insensitive comparison with markers
    return stripped.upper() in MISSING_VALUE_MARKERS


def parse_numeric_or_none(value):
    """Parse a value as a float, returning None if it's missing or unparseable.

    Args:
        value: The value to parse

    Returns:
        float if parseable, None if missing or unparseable
    """
    if is_missing_value(value):
        return None
    try:
        result = float(value.strip())
        # Check for NaN which should be treated as missing
        if math.isnan(result):
            return None
        return result
    except (ValueError, AttributeError):
        return None


class TestOutputFileExists:
    """Tests for output file existence and basic validity."""

    def test_output_file_exists(self):
        """Verify output file was created at the expected path."""
        assert os.path.exists(OUTPUT_FILE), (
            f"Output file not found at {OUTPUT_FILE}"
        )

    def test_output_file_is_not_empty(self):
        """Verify output file is not empty."""
        assert os.path.getsize(OUTPUT_FILE) > 0, "Output file is empty"


class TestOutputFormat:
    """Tests for output JSON format validity."""

    def test_output_is_valid_json(self):
        """Verify output is valid JSON format."""
        with open(OUTPUT_FILE) as f:
            data = json.load(f)
        assert data is not None, "JSON data is None"

    def test_output_is_json_object(self):
        """Verify output is a JSON object (dict), not an array."""
        with open(OUTPUT_FILE) as f:
            data = json.load(f)
        assert isinstance(data, dict), (
            f"Expected JSON object (dict), got {type(data).__name__}"
        )

    def test_output_is_compact_json(self):
        """Verify output JSON is compact (no pretty-printing with newlines/indentation).

        Requirement: Output should be a compact JSON file.
        """
        with open(OUTPUT_FILE) as f:
            content = f.read()

        # Compact JSON should not have newlines (except possibly one trailing newline)
        content_stripped = content.rstrip('\n')
        assert '\n' not in content_stripped, (
            "JSON should be compact (single line) but contains newlines. "
            "Found newlines in output, indicating pretty-printed format."
        )

        # Compact JSON should not have indentation patterns (multiple spaces after { or ,)
        assert not re.search(r'[{,]\s{2,}', content_stripped), (
            "JSON should be compact but appears to have indentation. "
            "Found multiple spaces after '{' or ',' indicating pretty-printing."
        )


class TestRequiredFields:
    """Tests for required JSON fields presence."""

    @pytest.fixture
    def output_data(self):
        """Load output JSON data."""
        with open(OUTPUT_FILE) as f:
            return json.load(f)

    def test_has_carrier_code_field(self, output_data):
        """Verify carrier_code field exists."""
        assert "carrier_code" in output_data, (
            "Missing required field: carrier_code"
        )

    def test_has_airline_description_field(self, output_data):
        """Verify airline_description field exists."""
        assert "airline_description" in output_data, (
            "Missing required field: airline_description"
        )

    def test_has_flight_count_used_field(self, output_data):
        """Verify flight_count_used field exists."""
        assert "flight_count_used" in output_data, (
            "Missing required field: flight_count_used"
        )

    def test_has_mean_arr_delay_minutes_field(self, output_data):
        """Verify mean_arr_delay_minutes field exists."""
        assert "mean_arr_delay_minutes" in output_data, (
            "Missing required field: mean_arr_delay_minutes"
        )

    def test_exact_field_count(self, output_data):
        """Verify output has exactly 4 fields."""
        assert len(output_data) == 4, (
            f"Expected exactly 4 fields, got {len(output_data)}: {list(output_data.keys())}"
        )


class TestFieldTypes:
    """Tests for field data types."""

    @pytest.fixture
    def output_data(self):
        """Load output JSON data."""
        with open(OUTPUT_FILE) as f:
            return json.load(f)

    def test_carrier_code_is_string(self, output_data):
        """Verify carrier_code is a string."""
        assert isinstance(output_data["carrier_code"], str), (
            f"carrier_code should be string, got {type(output_data['carrier_code']).__name__}"
        )

    def test_airline_description_is_string(self, output_data):
        """Verify airline_description is a string."""
        assert isinstance(output_data["airline_description"], str), (
            f"airline_description should be string, got {type(output_data['airline_description']).__name__}"
        )

    def test_flight_count_used_is_integer(self, output_data):
        """Verify flight_count_used is an integer."""
        assert isinstance(output_data["flight_count_used"], int), (
            f"flight_count_used should be integer, got {type(output_data['flight_count_used']).__name__}"
        )

    def test_mean_arr_delay_minutes_is_number(self, output_data):
        """Verify mean_arr_delay_minutes is a number (int or float)."""
        value = output_data["mean_arr_delay_minutes"]
        assert isinstance(value, (int, float)), (
            f"mean_arr_delay_minutes should be a number, got {type(value).__name__}"
        )


class TestFieldValues:
    """Tests for field value validity and constraints."""

    @pytest.fixture
    def output_data(self):
        """Load output JSON data."""
        with open(OUTPUT_FILE) as f:
            return json.load(f)

    def test_carrier_code_not_empty(self, output_data):
        """Verify carrier_code is not empty."""
        assert len(output_data["carrier_code"]) > 0, (
            "carrier_code should not be empty"
        )

    def test_airline_description_not_empty(self, output_data):
        """Verify airline_description is not empty."""
        assert len(output_data["airline_description"]) > 0, (
            "airline_description should not be empty"
        )

    def test_flight_count_used_is_positive(self, output_data):
        """Verify flight_count_used is a positive integer (at least 1 flight)."""
        assert output_data["flight_count_used"] > 0, (
            f"flight_count_used should be positive, got {output_data['flight_count_used']}"
        )

    def test_mean_arr_delay_minutes_rounded_to_3_decimals_numeric(self, output_data):
        """Verify mean_arr_delay_minutes is numerically rounded to 3 decimal places.

        Requirement: Round to 3 decimal places.
        Note: This validates the numeric precision, not the JSON serialization format.
        A value like 12.3 is valid (equivalent to 12.300 when rounded to 3 decimals).
        """
        value = output_data["mean_arr_delay_minutes"]
        rounded_value = round(value, 3)
        # Use approximate comparison to handle floating point representation
        assert abs(value - rounded_value) < 1e-9, (
            f"mean_arr_delay_minutes should be rounded to 3 decimal places. "
            f"Got {value}, expected {rounded_value} after rounding."
        )


class TestDataConsistency:
    """Tests for data consistency with input files."""

    @pytest.fixture
    def output_data(self):
        """Load output JSON data."""
        with open(OUTPUT_FILE) as f:
            return json.load(f)

    @pytest.fixture
    def airlines_data(self):
        """Load airlines CSV and return Code -> Description mapping.

        For duplicate codes, keeps the lexicographically smallest Description.
        """
        import csv
        airlines = {}
        with open(AIRLINES_FILE, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                code = row['Code']
                desc = row['Description']
                # Keep lexicographically smallest description for duplicate codes
                if code not in airlines or desc < airlines[code]:
                    airlines[code] = desc
        return airlines

    @pytest.fixture
    def flights_carriers(self):
        """Load unique carrier codes from flights CSV."""
        import csv
        carriers = set()
        with open(FLIGHTS_FILE, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                carriers.add(row['carrier'])
        return carriers

    def test_carrier_code_exists_in_flights(self, output_data, flights_carriers):
        """Verify carrier_code exists in the flights data."""
        assert output_data["carrier_code"] in flights_carriers, (
            f"carrier_code '{output_data['carrier_code']}' not found in flights data. "
            f"Valid carriers: {sorted(flights_carriers)}"
        )

    def test_carrier_code_exists_in_airlines(self, output_data, airlines_data):
        """Verify carrier_code exists in the airlines mapping."""
        assert output_data["carrier_code"] in airlines_data, (
            f"carrier_code '{output_data['carrier_code']}' not found in airlines data"
        )

    def test_airline_description_matches_carrier_code(self, output_data, airlines_data):
        """Verify airline_description matches the carrier_code in airlines.csv.

        For duplicate codes, the lexicographically smallest Description should be used.
        """
        carrier_code = output_data["carrier_code"]
        expected_description = airlines_data.get(carrier_code)
        assert output_data["airline_description"] == expected_description, (
            f"airline_description mismatch for carrier '{carrier_code}': "
            f"expected '{expected_description}', got '{output_data['airline_description']}'"
        )


class TestWorstAirlineCalculation:
    """Tests to verify the worst airline calculation is correct."""

    @pytest.fixture
    def output_data(self):
        """Load output JSON data."""
        with open(OUTPUT_FILE) as f:
            return json.load(f)

    @pytest.fixture
    def airlines_mapping(self):
        """Load airlines CSV and return Code -> Description mapping.

        For duplicate codes, keeps the lexicographically smallest Description.
        """
        import csv
        airlines = {}
        with open(AIRLINES_FILE, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                code = row['Code']
                desc = row['Description']
                if code not in airlines or desc < airlines[code]:
                    airlines[code] = desc
        return airlines

    @pytest.fixture
    def computed_stats(self, airlines_mapping):
        """Compute carrier statistics from the raw data.

        Excludes missing/NA values as per task requirements.
        Uses robust missing value detection that handles None, empty strings,
        whitespace-only strings, and common NA markers case-insensitively.

        Returns a dict with:
            - carrier_stats: dict mapping carrier code to stats
            - parse_issues: list of any parsing issues encountered (for diagnostics)
        """
        import csv

        # Compute per-carrier statistics
        carrier_delays = {}  # carrier -> list of arr_delay values
        parse_issues = []  # Collect any issues for diagnostic purposes

        with open(FLIGHTS_FILE, newline='') as f:
            reader = csv.DictReader(f)
            for row_num, row in enumerate(reader, start=2):  # Start at 2 (1-indexed + header)
                carrier = row.get('carrier', '')
                arr_delay_raw = row.get('arr_delay')

                # Use robust missing value detection
                arr_delay = parse_numeric_or_none(arr_delay_raw)

                if arr_delay is None:
                    # This is a missing/NA value - skip it
                    continue

                if carrier not in carrier_delays:
                    carrier_delays[carrier] = []
                carrier_delays[carrier].append(arr_delay)

        # Compute mean delay for each carrier (rounded to 3 decimals)
        carrier_stats = {}
        for carrier, delays in carrier_delays.items():
            if delays:
                mean_delay = sum(delays) / len(delays)
                carrier_stats[carrier] = {
                    'mean_arr_delay': round(mean_delay, 3),
                    'flight_count': len(delays),
                    'description': airlines_mapping.get(carrier, '')
                }

        return {
            'carrier_stats': carrier_stats,
            'parse_issues': parse_issues,
            'airlines_mapping': airlines_mapping
        }

    def test_carrier_exists_in_computed_stats(self, output_data, computed_stats):
        """Verify the output carrier_code exists in our computed statistics.

        This ensures our parsing matches the task implementation.
        """
        carrier_code = output_data["carrier_code"]
        carrier_stats = computed_stats['carrier_stats']
        assert carrier_code in carrier_stats, (
            f"Output carrier_code '{carrier_code}' not found in computed statistics. "
            f"This may indicate a difference in NA/missing value handling. "
            f"Available carriers: {sorted(carrier_stats.keys())}"
        )

    def test_flight_count_matches_computation(self, output_data, computed_stats):
        """Verify flight_count_used matches the computed count for the carrier.

        Requirement: flight_count_used is the number of rows used in mean calculation
        (excluding NA arr_delay rows).
        """
        carrier_code = output_data["carrier_code"]
        carrier_stats = computed_stats['carrier_stats']

        assert carrier_code in carrier_stats, (
            f"Carrier '{carrier_code}' not found in computed stats - cannot verify flight count"
        )

        expected_count = carrier_stats[carrier_code]['flight_count']
        assert output_data["flight_count_used"] == expected_count, (
            f"flight_count_used mismatch for carrier '{carrier_code}': "
            f"expected {expected_count}, got {output_data['flight_count_used']}. "
            f"This should be the count of flights with valid (non-NA) arr_delay values."
        )

    def test_mean_delay_matches_computation(self, output_data, computed_stats):
        """Verify mean_arr_delay_minutes matches the computed mean (rounded to 3 decimals).

        Requirement: mean_arr_delay_minutes rounded to 3 decimal places.
        """
        carrier_code = output_data["carrier_code"]
        carrier_stats = computed_stats['carrier_stats']

        assert carrier_code in carrier_stats, (
            f"Carrier '{carrier_code}' not found in computed stats - cannot verify mean delay"
        )

        expected_mean = carrier_stats[carrier_code]['mean_arr_delay']
        output_mean = output_data["mean_arr_delay_minutes"]

        # Use approximate comparison for floating point
        assert abs(output_mean - expected_mean) < 1e-6, (
            f"mean_arr_delay_minutes mismatch for carrier '{carrier_code}': "
            f"expected {expected_mean}, got {output_mean}. "
            f"Both values should be rounded to 3 decimal places."
        )

    def test_carrier_has_highest_mean_delay(self, output_data, computed_stats):
        """Verify the selected carrier has the highest mean arrival delay.

        Requirement: Identify the airline with the worst on-time performance
        (highest mean arrival delay).
        """
        carrier_code = output_data["carrier_code"]
        output_mean = output_data["mean_arr_delay_minutes"]
        carrier_stats = computed_stats['carrier_stats']

        # Find the maximum mean delay (already rounded to 3 decimals in carrier_stats)
        max_mean = max(stats['mean_arr_delay'] for stats in carrier_stats.values())

        # The output mean should equal the maximum mean (both rounded to 3 decimals)
        # Use approximate comparison for floating point
        assert abs(output_mean - max_mean) < 1e-6, (
            f"Output mean_arr_delay_minutes ({output_mean}) does not equal "
            f"the maximum mean delay ({max_mean}). "
            f"The selected carrier should have the highest mean arrival delay."
        )

        # Also verify the carrier is among those with max delay
        max_carriers = [
            code for code, stats in carrier_stats.items()
            if abs(stats['mean_arr_delay'] - max_mean) < 1e-6
        ]

        assert carrier_code in max_carriers, (
            f"Selected carrier '{carrier_code}' (mean={output_mean}) is not among "
            f"carriers with the highest mean delay ({max_mean}): {max_carriers}"
        )

    def test_tiebreaker_lexicographically_smallest(self, output_data, computed_stats):
        """Verify tiebreaker uses lexicographically smallest carrier_code.

        Requirement: If there is a tie, select the airline with the lexicographically
        smallest carrier_code.
        """
        carrier_code = output_data["carrier_code"]
        carrier_stats = computed_stats['carrier_stats']

        # Find all carriers with the maximum mean delay
        max_mean = max(stats['mean_arr_delay'] for stats in carrier_stats.values())
        tied_carriers = sorted([
            code for code, stats in carrier_stats.items()
            if abs(stats['mean_arr_delay'] - max_mean) < 1e-6
        ])

        # The selected carrier should be the lexicographically smallest among tied carriers
        expected_carrier = tied_carriers[0]
        assert carrier_code == expected_carrier, (
            f"Tiebreaker failed: expected lexicographically smallest carrier "
            f"'{expected_carrier}', got '{carrier_code}'. "
            f"Carriers tied for highest mean delay ({max_mean}): {tied_carriers}"
        )

    def test_recomputed_worst_carrier_matches_output(self, output_data, computed_stats):
        """Verify the complete worst carrier calculation using join logic.

        This test recomputes the worst carrier from scratch using:
        1. flights_2.csv.carrier joined to airlines.csv.Code
        2. Lexicographically smallest Description for duplicate airline codes
        3. Highest mean arr_delay (excluding NA values)
        4. Lexicographically smallest carrier_code for ties

        Then verifies both carrier_code and airline_description match.
        """
        carrier_stats = computed_stats['carrier_stats']
        airlines_mapping = computed_stats['airlines_mapping']

        # Find the worst carrier
        max_mean = max(stats['mean_arr_delay'] for stats in carrier_stats.values())
        tied_carriers = sorted([
            code for code, stats in carrier_stats.items()
            if abs(stats['mean_arr_delay'] - max_mean) < 1e-6
        ])

        expected_carrier_code = tied_carriers[0]
        expected_stats = carrier_stats[expected_carrier_code]
        expected_description = airlines_mapping.get(expected_carrier_code, '')

        # Verify carrier_code
        assert output_data["carrier_code"] == expected_carrier_code, (
            f"Recomputed worst carrier mismatch: "
            f"expected carrier_code '{expected_carrier_code}', got '{output_data['carrier_code']}'. "
            f"Max mean delay: {max_mean}, tied carriers: {tied_carriers}"
        )

        # Verify airline_description matches the join result
        assert output_data["airline_description"] == expected_description, (
            f"airline_description from join mismatch for carrier '{expected_carrier_code}': "
            f"expected '{expected_description}' (from airlines.csv), "
            f"got '{output_data['airline_description']}'"
        )

        # Verify flight_count_used
        assert output_data["flight_count_used"] == expected_stats['flight_count'], (
            f"flight_count_used mismatch: "
            f"expected {expected_stats['flight_count']}, got {output_data['flight_count_used']}"
        )

        # Verify mean_arr_delay_minutes
        assert abs(output_data["mean_arr_delay_minutes"] - expected_stats['mean_arr_delay']) < 1e-6, (
            f"mean_arr_delay_minutes mismatch: "
            f"expected {expected_stats['mean_arr_delay']}, got {output_data['mean_arr_delay_minutes']}"
        )


class TestJoinValidation:
    """Tests to verify the join between flights and airlines is performed correctly."""

    @pytest.fixture
    def output_data(self):
        """Load output JSON data."""
        with open(OUTPUT_FILE) as f:
            return json.load(f)

    @pytest.fixture
    def airlines_mapping(self):
        """Load airlines CSV and return Code -> Description mapping.

        For duplicate codes, keeps the lexicographically smallest Description.
        """
        import csv
        airlines = {}
        with open(AIRLINES_FILE, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                code = row['Code']
                desc = row['Description']
                if code not in airlines or desc < airlines[code]:
                    airlines[code] = desc
        return airlines

    @pytest.fixture
    def flights_carriers_with_valid_delays(self):
        """Load carriers from flights CSV that have at least one valid arr_delay."""
        import csv
        carriers_with_delays = set()
        with open(FLIGHTS_FILE, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                carrier = row.get('carrier', '')
                arr_delay_raw = row.get('arr_delay')
                arr_delay = parse_numeric_or_none(arr_delay_raw)
                if arr_delay is not None:
                    carriers_with_delays.add(carrier)
        return carriers_with_delays

    def test_output_carrier_has_airline_mapping(self, output_data, airlines_mapping):
        """Verify that the output carrier_code has a corresponding entry in airlines.csv.

        The join requires that the carrier exists in the airlines mapping.
        """
        carrier_code = output_data["carrier_code"]
        assert carrier_code in airlines_mapping, (
            f"Output carrier_code '{carrier_code}' does not exist in airlines.csv. "
            f"The join between flights_2.csv.carrier and airlines.csv.Code requires "
            f"the carrier to exist in the airlines mapping."
        )

    def test_description_is_lexicographically_smallest_for_code(self, output_data, airlines_mapping):
        """Verify airline_description is the lexicographically smallest for the carrier code.

        Requirement: For duplicate airline codes, select the single airline by the
        lexicographically smallest full Description.
        """
        carrier_code = output_data["carrier_code"]
        expected_description = airlines_mapping.get(carrier_code)

        assert expected_description is not None, (
            f"Carrier '{carrier_code}' not found in airlines mapping"
        )

        assert output_data["airline_description"] == expected_description, (
            f"airline_description should be the lexicographically smallest Description "
            f"for carrier '{carrier_code}'. Expected '{expected_description}', "
            f"got '{output_data['airline_description']}'"
        )


class TestKeyOrder:
    """Tests for JSON key ordering (as specified in requirements)."""

    def test_json_keys_in_correct_order(self):
        """Verify JSON keys are in the specified order.

        Requirement: JSON should have keys in this order:
        carrier_code, airline_description, flight_count_used, mean_arr_delay_minutes
        """
        with open(OUTPUT_FILE) as f:
            content = f.read()
        data = json.loads(content)

        expected_order = [
            "carrier_code",
            "airline_description",
            "flight_count_used",
            "mean_arr_delay_minutes"
        ]
        actual_keys = list(data.keys())

        assert actual_keys == expected_order, (
            f"Keys should be in order {expected_order}, got {actual_keys}. "
            f"The JSON schema requires this specific key ordering."
        )


class TestMissingValueHandling:
    """Tests to verify NA/missing value handling is robust."""

    @pytest.fixture
    def flights_arr_delay_values(self):
        """Load all arr_delay values from flights CSV for analysis."""
        import csv
        values = []
        with open(FLIGHTS_FILE, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                values.append(row.get('arr_delay'))
        return values

    def test_missing_value_detection_consistency(self, flights_arr_delay_values):
        """Verify that our missing value detection is consistent with common patterns.

        This test documents what values are treated as missing in the test suite.
        """
        missing_count = 0
        valid_count = 0

        for value in flights_arr_delay_values:
            if is_missing_value(value):
                missing_count += 1
            elif parse_numeric_or_none(value) is not None:
                valid_count += 1

        # Ensure we found some valid values (sanity check)
        assert valid_count > 0, (
            "No valid arr_delay values found in flights data. "
            "This suggests a problem with the data or parsing logic."
        )

        # Document what we found (this test always passes if valid_count > 0)
        total = len(flights_arr_delay_values)
        unparseable = total - missing_count - valid_count
        assert unparseable == 0 or True, (  # This assertion is informational
            f"Found {missing_count} missing, {valid_count} valid, "
            f"{unparseable} unparseable values out of {total} total"
        )
