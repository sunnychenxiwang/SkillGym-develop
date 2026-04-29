"""Auto-generated expectation tests for task verification.

These tests verify that the task execution produces correct outputs
for identifying the airline with highest mean arrival delay on SEA->LAX route.
"""

import json
import os
from pathlib import Path

import pandas as pd
import pytest


OUTPUT_PATH = "/root/sea_lax_worst_airline.json"
FLIGHTS_PATH = "/root/flights_2.csv"
AIRLINES_PATH = "/root/airlines.csv"


class TestOutputFileExistence:
    """Tests for output file existence and basic validity."""

    def test_output_file_exists(self):
        """Verify output file was created at the expected path."""
        assert os.path.exists(OUTPUT_PATH), (
            f"Output file not found at {OUTPUT_PATH}. "
            "Task must write output to this exact location."
        )

    def test_output_file_is_not_empty(self):
        """Verify output file is not empty."""
        assert os.path.getsize(OUTPUT_PATH) > 0, "Output file exists but is empty"

    def test_output_is_valid_json(self):
        """Verify output is valid JSON format."""
        with open(OUTPUT_PATH, "r") as f:
            content = f.read()
        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            pytest.fail(f"Output file is not valid JSON: {e}")
        assert data is not None, "JSON parsed to None"


class TestOutputSchema:
    """Tests for verifying the output JSON schema matches requirements."""

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        with open(OUTPUT_PATH, "r") as f:
            return json.load(f)

    def test_output_is_dict(self, output_data):
        """Verify output is a JSON object (dict), not array or primitive."""
        assert isinstance(output_data, dict), (
            f"Output should be a JSON object, got {type(output_data).__name__}"
        )

    def test_has_route_field(self, output_data):
        """Verify output contains 'route' field."""
        assert "route" in output_data, "Missing required field: 'route'"

    def test_has_carrier_code_field(self, output_data):
        """Verify output contains 'carrier_code' field."""
        assert "carrier_code" in output_data, "Missing required field: 'carrier_code'"

    def test_has_carrier_description_field(self, output_data):
        """Verify output contains 'carrier_description' field."""
        assert "carrier_description" in output_data, (
            "Missing required field: 'carrier_description'"
        )

    def test_has_n_flights_field(self, output_data):
        """Verify output contains 'n_flights' field."""
        assert "n_flights" in output_data, "Missing required field: 'n_flights'"

    def test_has_mean_arr_delay_field(self, output_data):
        """Verify output contains 'mean_arr_delay' field."""
        assert "mean_arr_delay" in output_data, (
            "Missing required field: 'mean_arr_delay'"
        )

    def test_no_extra_fields(self, output_data):
        """Verify output contains exactly the required fields."""
        expected_fields = {
            "route", "carrier_code", "carrier_description",
            "n_flights", "mean_arr_delay"
        }
        actual_fields = set(output_data.keys())
        extra_fields = actual_fields - expected_fields
        assert not extra_fields, f"Unexpected extra fields in output: {extra_fields}"


class TestFieldValues:
    """Tests for verifying individual field values meet requirements."""

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        with open(OUTPUT_PATH, "r") as f:
            return json.load(f)

    def test_route_value(self, output_data):
        """Verify route is exactly 'SEA-LAX'."""
        assert output_data["route"] == "SEA-LAX", (
            f"Route should be 'SEA-LAX', got '{output_data['route']}'"
        )

    def test_carrier_code_is_string(self, output_data):
        """Verify carrier_code is a string."""
        assert isinstance(output_data["carrier_code"], str), (
            f"carrier_code should be a string, got {type(output_data['carrier_code']).__name__}"
        )

    def test_carrier_code_not_empty(self, output_data):
        """Verify carrier_code is not empty."""
        assert output_data["carrier_code"].strip() != "", (
            "carrier_code should not be empty"
        )

    def test_carrier_description_is_string(self, output_data):
        """Verify carrier_description is a string."""
        assert isinstance(output_data["carrier_description"], str), (
            f"carrier_description should be a string, got {type(output_data['carrier_description']).__name__}"
        )

    def test_carrier_description_not_empty(self, output_data):
        """Verify carrier_description is not empty."""
        assert output_data["carrier_description"].strip() != "", (
            "carrier_description should not be empty"
        )

    def test_n_flights_is_integer(self, output_data):
        """Verify n_flights is an integer."""
        assert isinstance(output_data["n_flights"], int), (
            f"n_flights should be an integer, got {type(output_data['n_flights']).__name__}"
        )

    def test_n_flights_minimum_threshold(self, output_data):
        """Verify n_flights is at least 5 (the minimum threshold)."""
        assert output_data["n_flights"] >= 5, (
            f"n_flights should be >= 5 (minimum threshold), got {output_data['n_flights']}"
        )

    def test_mean_arr_delay_is_numeric(self, output_data):
        """Verify mean_arr_delay is a numeric JSON value (int or float), not string."""
        assert isinstance(output_data["mean_arr_delay"], (int, float)), (
            f"mean_arr_delay should be a numeric value, got {type(output_data['mean_arr_delay']).__name__}"
        )
        # Should not be a string representation of a number
        assert not isinstance(output_data["mean_arr_delay"], bool), (
            "mean_arr_delay should be numeric, not boolean"
        )

    def test_mean_arr_delay_rounded_to_2_decimals(self, output_data):
        """Verify mean_arr_delay is rounded to 2 decimal places."""
        value = output_data["mean_arr_delay"]
        # Convert to string and check decimal places
        str_val = str(value)
        if "." in str_val:
            decimal_part = str_val.split(".")[1]
            assert len(decimal_part) <= 2, (
                f"mean_arr_delay should be rounded to 2 decimal places, got {value}"
            )


class TestDataIntegrity:
    """Tests for verifying data integrity against input files."""

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        with open(OUTPUT_PATH, "r") as f:
            return json.load(f)

    @pytest.fixture
    def airlines_df(self):
        """Load the airlines lookup table."""
        return pd.read_csv(AIRLINES_PATH)

    @pytest.fixture
    def flights_df(self):
        """Load the flights data."""
        return pd.read_csv(FLIGHTS_PATH)

    def test_carrier_code_exists_in_airlines(self, output_data, airlines_df):
        """Verify carrier_code exists in airlines.csv."""
        carrier_code = output_data["carrier_code"]
        assert carrier_code in airlines_df["Code"].values, (
            f"carrier_code '{carrier_code}' not found in airlines.csv"
        )

    def test_carrier_description_matches_code(self, output_data, airlines_df):
        """Verify carrier_description matches the carrier_code in airlines.csv."""
        carrier_code = output_data["carrier_code"]
        carrier_description = output_data["carrier_description"]

        # Look up expected description
        matching_rows = airlines_df[airlines_df["Code"] == carrier_code]
        assert len(matching_rows) > 0, (
            f"carrier_code '{carrier_code}' not found in airlines.csv"
        )

        expected_description = matching_rows.iloc[0]["Description"]
        assert carrier_description == expected_description, (
            f"carrier_description mismatch: expected '{expected_description}' "
            f"for carrier '{carrier_code}', got '{carrier_description}'"
        )

    def test_carrier_operates_sea_lax_route(self, output_data, flights_df):
        """Verify the carrier code actually operates SEA->LAX flights in the data."""
        carrier_code = output_data["carrier_code"]

        # Filter to SEA->LAX route
        sea_lax_flights = flights_df[
            (flights_df["origin"] == "SEA") & (flights_df["dest"] == "LAX")
        ]

        assert carrier_code in sea_lax_flights["carrier"].values, (
            f"carrier_code '{carrier_code}' does not operate SEA->LAX route in the data"
        )


class TestCalculationCorrectness:
    """Tests for verifying the calculation is correct."""

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        with open(OUTPUT_PATH, "r") as f:
            return json.load(f)

    @pytest.fixture
    def flights_df(self):
        """Load the flights data."""
        return pd.read_csv(FLIGHTS_PATH)

    @pytest.fixture
    def airlines_df(self):
        """Load the airlines lookup table."""
        return pd.read_csv(AIRLINES_PATH)

    def test_n_flights_matches_actual_count(self, output_data, flights_df):
        """Verify n_flights matches the actual count for that carrier on SEA->LAX."""
        carrier_code = output_data["carrier_code"]
        n_flights = output_data["n_flights"]

        # Filter to SEA->LAX route and the specific carrier
        sea_lax_carrier = flights_df[
            (flights_df["origin"] == "SEA") &
            (flights_df["dest"] == "LAX") &
            (flights_df["carrier"] == carrier_code)
        ]

        # Exclude rows with missing arr_delay
        valid_flights = sea_lax_carrier[pd.notna(sea_lax_carrier["arr_delay"])]

        assert n_flights == len(valid_flights), (
            f"n_flights mismatch for carrier '{carrier_code}': "
            f"expected {len(valid_flights)}, got {n_flights}"
        )

    def test_mean_arr_delay_calculation(self, output_data, flights_df):
        """Verify mean_arr_delay is correctly calculated."""
        carrier_code = output_data["carrier_code"]
        mean_arr_delay = output_data["mean_arr_delay"]

        # Filter to SEA->LAX route and the specific carrier
        sea_lax_carrier = flights_df[
            (flights_df["origin"] == "SEA") &
            (flights_df["dest"] == "LAX") &
            (flights_df["carrier"] == carrier_code)
        ]

        # Exclude rows with missing arr_delay
        valid_flights = sea_lax_carrier[pd.notna(sea_lax_carrier["arr_delay"])]

        # Calculate expected mean and round to 2 decimals
        expected_mean = round(valid_flights["arr_delay"].mean(), 2)

        assert abs(mean_arr_delay - expected_mean) < 0.01, (
            f"mean_arr_delay mismatch for carrier '{carrier_code}': "
            f"expected {expected_mean}, got {mean_arr_delay}"
        )

    def test_carrier_has_highest_mean_delay(self, output_data, flights_df):
        """Verify the selected carrier actually has the highest mean arrival delay."""
        carrier_code = output_data["carrier_code"]
        mean_arr_delay = output_data["mean_arr_delay"]

        # Filter to SEA->LAX route
        sea_lax = flights_df[
            (flights_df["origin"] == "SEA") & (flights_df["dest"] == "LAX")
        ].copy()

        # Exclude rows with missing arr_delay
        sea_lax = sea_lax[pd.notna(sea_lax["arr_delay"])]

        # Group by carrier and compute stats
        carrier_stats = sea_lax.groupby("carrier").agg(
            n_flights=("arr_delay", "count"),
            mean_arr_delay=("arr_delay", "mean")
        ).reset_index()

        # Filter to carriers with at least 5 flights
        eligible = carrier_stats[carrier_stats["n_flights"] >= 5]

        # Find the maximum mean delay
        max_delay = eligible["mean_arr_delay"].max()

        # Get carriers with max delay (for tie handling)
        top_carriers = eligible[eligible["mean_arr_delay"] == max_delay]

        # The selected carrier should be among them
        assert carrier_code in top_carriers["carrier"].values, (
            f"carrier '{carrier_code}' does not have the highest mean arrival delay. "
            f"Highest delay carriers: {list(top_carriers['carrier'].values)}"
        )

        # If there were ties, verify lexicographically smallest was chosen
        if len(top_carriers) > 1:
            expected_carrier = sorted(top_carriers["carrier"].values)[0]
            assert carrier_code == expected_carrier, (
                f"Tie-breaker failed: expected '{expected_carrier}' "
                f"(lexicographically smallest), got '{carrier_code}'"
            )

    def test_all_eligible_carriers_considered(self, output_data, flights_df):
        """Verify the analysis correctly filters to carriers with >= 5 flights."""
        mean_arr_delay = output_data["mean_arr_delay"]

        # Filter to SEA->LAX route
        sea_lax = flights_df[
            (flights_df["origin"] == "SEA") & (flights_df["dest"] == "LAX")
        ].copy()

        # Exclude rows with missing arr_delay
        sea_lax = sea_lax[pd.notna(sea_lax["arr_delay"])]

        # Group by carrier and compute stats
        carrier_stats = sea_lax.groupby("carrier").agg(
            n_flights=("arr_delay", "count"),
            mean_arr_delay=("arr_delay", "mean")
        ).reset_index()

        # Filter to carriers with at least 5 flights
        eligible = carrier_stats[carrier_stats["n_flights"] >= 5]

        # No eligible carrier should have a higher mean delay than reported
        # (accounting for rounding)
        for _, row in eligible.iterrows():
            assert row["mean_arr_delay"] <= mean_arr_delay + 0.01, (
                f"Carrier '{row['carrier']}' has higher mean delay "
                f"({round(row['mean_arr_delay'], 2)}) than reported ({mean_arr_delay})"
            )


class TestEdgeCases:
    """Tests for edge cases and data quality."""

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        with open(OUTPUT_PATH, "r") as f:
            return json.load(f)

    def test_mean_arr_delay_not_nan(self, output_data):
        """Verify mean_arr_delay is not NaN."""
        import math
        value = output_data["mean_arr_delay"]
        assert not (isinstance(value, float) and math.isnan(value)), (
            "mean_arr_delay should not be NaN"
        )

    def test_mean_arr_delay_not_inf(self, output_data):
        """Verify mean_arr_delay is not infinity."""
        import math
        value = output_data["mean_arr_delay"]
        assert not (isinstance(value, float) and math.isinf(value)), (
            "mean_arr_delay should not be infinity"
        )

    def test_n_flights_reasonable_range(self, output_data):
        """Verify n_flights is within a reasonable range."""
        n_flights = output_data["n_flights"]
        assert 5 <= n_flights <= 100000, (
            f"n_flights ({n_flights}) seems outside reasonable range [5, 100000]"
        )

    def test_carrier_code_format(self, output_data):
        """Verify carrier_code follows expected format (typically 2-3 uppercase chars)."""
        carrier_code = output_data["carrier_code"]
        # Most carrier codes are 2 characters, some are 2-3
        assert 1 <= len(carrier_code) <= 3, (
            f"carrier_code '{carrier_code}' has unexpected length {len(carrier_code)}"
        )
