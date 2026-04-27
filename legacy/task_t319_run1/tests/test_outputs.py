"""Stronger expectation tests for the max average delay burden airline task.

This version recomputes the expected result directly from:
- /root/flights_2.csv
- /root/airlines.csv

It validates the actual computation required by the instruction:
- filter rows where both dep_delay and arr_delay are present
- compute per-row delay_burden = max(dep_delay, 0) + max(arr_delay, 0)
- aggregate by carrier
- pick the unique winner by max avg_delay_burden, breaking ties by
  lexicographically smallest carrier code
- join to airlines.csv for the airline description
- enforce exact JSON schema and key order
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import pandas as pd
import pytest


OUTPUT_FILE = Path("/root/max_avg_delay_burden_airline.json")
FLIGHTS_FILE = Path("/root/flights_2.csv")
AIRLINES_FILE = Path("/root/airlines.csv")

EXPECTED_KEYS = [
    "carrier_code",
    "airline_name",
    "avg_delay_burden",
    "total_delay_burden",
    "flight_count",
]


def compute_expected_result() -> dict:
    flights = pd.read_csv(FLIGHTS_FILE)
    airlines = pd.read_csv(AIRLINES_FILE)

    required_flight_cols = {"carrier", "dep_delay", "arr_delay"}
    missing_flight_cols = required_flight_cols - set(flights.columns)
    assert not missing_flight_cols, f"Missing required flight columns: {missing_flight_cols}"

    required_airline_cols = {"Code", "Description"}
    missing_airline_cols = required_airline_cols - set(airlines.columns)
    assert not missing_airline_cols, f"Missing required airline columns: {missing_airline_cols}"

    work = flights.copy()

    # Constrain to January 2014 if the dataset exposes year/month columns.
    if "year" in work.columns:
        work = work[work["year"] == 2014]
    if "month" in work.columns:
        work = work[work["month"] == 1]

    work["dep_delay"] = pd.to_numeric(work["dep_delay"], errors="coerce")
    work["arr_delay"] = pd.to_numeric(work["arr_delay"], errors="coerce")

    # Instruction: only include rows where both dep_delay and arr_delay are present.
    work = work[work["dep_delay"].notna() & work["arr_delay"].notna()].copy()
    assert not work.empty, "No qualifying rows remain after filtering dep_delay and arr_delay"

    # Row-level delay burden.
    work["delay_burden"] = work["dep_delay"].clip(lower=0) + work["arr_delay"].clip(lower=0)

    grouped = (
        work.groupby("carrier", as_index=False)
        .agg(
            total_delay_burden=("delay_burden", "sum"),
            flight_count=("delay_burden", "size"),
        )
    )
    grouped["avg_delay_burden_unrounded"] = (
        grouped["total_delay_burden"] / grouped["flight_count"]
    )

    # Winner: max avg_delay_burden; tie -> lexicographically smallest carrier code.
    grouped = grouped.sort_values(
        by=["avg_delay_burden_unrounded", "carrier"],
        ascending=[False, True],
        kind="mergesort",
    ).reset_index(drop=True)

    winner = grouped.iloc[0]
    carrier_code = str(winner["carrier"])

    airline_match = airlines.loc[airlines["Code"] == carrier_code, "Description"]
    assert not airline_match.empty, f"Carrier code {carrier_code!r} not found in airlines.csv"
    airline_name = str(airline_match.iloc[0])

    total_delay_burden = round(float(winner["total_delay_burden"]), 2)
    avg_delay_burden = round(float(winner["avg_delay_burden_unrounded"]), 2)
    flight_count = int(winner["flight_count"])

    return {
        "carrier_code": carrier_code,
        "airline_name": airline_name,
        "avg_delay_burden": avg_delay_burden,
        "total_delay_burden": total_delay_burden,
        "flight_count": flight_count,
    }


@pytest.fixture(scope="module")
def output_data():
    assert OUTPUT_FILE.exists(), f"Output file not found at {OUTPUT_FILE}"
    assert OUTPUT_FILE.stat().st_size > 0, "Output file is empty"
    with OUTPUT_FILE.open("r", encoding="utf-8") as f:
        data = json.load(f)
    assert isinstance(data, dict), f"Expected JSON object, got {type(data).__name__}"
    return data


@pytest.fixture(scope="module")
def expected_data():
    return compute_expected_result()


class TestOutputFile:
    def test_output_file_exists(self):
        assert OUTPUT_FILE.exists(), f"Output file not found at {OUTPUT_FILE}"

    def test_output_file_not_empty(self):
        assert OUTPUT_FILE.exists(), f"Output file not found at {OUTPUT_FILE}"
        assert OUTPUT_FILE.stat().st_size > 0, "Output file is empty"


class TestSchema:
    def test_output_is_valid_json_object(self, output_data):
        assert isinstance(output_data, dict), f"Expected dict, got {type(output_data).__name__}"

    def test_exact_key_order(self, output_data):
        assert list(output_data.keys()) == EXPECTED_KEYS, (
            f"JSON keys/order must be exactly {EXPECTED_KEYS}, got {list(output_data.keys())}"
        )

    def test_no_extra_or_missing_keys(self, output_data):
        assert set(output_data.keys()) == set(EXPECTED_KEYS), (
            f"Expected keys {set(EXPECTED_KEYS)}, got {set(output_data.keys())}"
        )


class TestFieldTypesAndConstraints:
    def test_carrier_code_type(self, output_data):
        assert isinstance(output_data["carrier_code"], str), "carrier_code must be a string"
        assert output_data["carrier_code"].strip() != "", "carrier_code cannot be empty"

    def test_airline_name_type(self, output_data):
        assert isinstance(output_data["airline_name"], str), "airline_name must be a string"
        assert output_data["airline_name"].strip() != "", "airline_name cannot be empty"

    def test_avg_delay_burden_type(self, output_data):
        value = output_data["avg_delay_burden"]
        assert isinstance(value, (int, float)), "avg_delay_burden must be numeric"
        assert math.isfinite(float(value)), "avg_delay_burden must be finite"
        assert float(value) >= 0, "avg_delay_burden must be non-negative"

    def test_total_delay_burden_type(self, output_data):
        value = output_data["total_delay_burden"]
        assert isinstance(value, (int, float)), "total_delay_burden must be numeric"
        assert math.isfinite(float(value)), "total_delay_burden must be finite"
        assert float(value) >= 0, "total_delay_burden must be non-negative"

    def test_flight_count_type(self, output_data):
        value = output_data["flight_count"]
        assert isinstance(value, int), f"flight_count must be int, got {type(value).__name__}"
        assert value > 0, "flight_count must be positive"

    def test_avg_delay_burden_precision(self, output_data):
        value = float(output_data["avg_delay_burden"])
        assert value == round(value, 2), (
            f"avg_delay_burden must be rounded to 2 decimals, got {value}"
        )

    def test_total_delay_burden_precision(self, output_data):
        value = float(output_data["total_delay_burden"])
        assert value == round(value, 2), (
            f"total_delay_burden must be rounded to 2 decimals, got {value}"
        )


class TestExactCorrectness:
    def test_carrier_code_matches_expected(self, output_data, expected_data):
        assert output_data["carrier_code"] == expected_data["carrier_code"], (
            f"carrier_code mismatch: expected {expected_data['carrier_code']!r}, "
            f"got {output_data['carrier_code']!r}"
        )

    def test_airline_name_matches_expected(self, output_data, expected_data):
        assert output_data["airline_name"] == expected_data["airline_name"], (
            f"airline_name mismatch: expected {expected_data['airline_name']!r}, "
            f"got {output_data['airline_name']!r}"
        )

    def test_avg_delay_burden_matches_expected(self, output_data, expected_data):
        assert float(output_data["avg_delay_burden"]) == pytest.approx(
            float(expected_data["avg_delay_burden"]), rel=0, abs=1e-9
        ), (
            f"avg_delay_burden mismatch: expected {expected_data['avg_delay_burden']}, "
            f"got {output_data['avg_delay_burden']}"
        )

    def test_total_delay_burden_matches_expected(self, output_data, expected_data):
        assert float(output_data["total_delay_burden"]) == pytest.approx(
            float(expected_data["total_delay_burden"]), rel=0, abs=1e-9
        ), (
            f"total_delay_burden mismatch: expected {expected_data['total_delay_burden']}, "
            f"got {output_data['total_delay_burden']}"
        )

    def test_flight_count_matches_expected(self, output_data, expected_data):
        assert output_data["flight_count"] == expected_data["flight_count"], (
            f"flight_count mismatch: expected {expected_data['flight_count']}, "
            f"got {output_data['flight_count']}"
        )


class TestInternalConsistency:
    def test_average_matches_total_divided_by_count(self, output_data):
        total = float(output_data["total_delay_burden"])
        count = int(output_data["flight_count"])
        expected_avg = round(total / count, 2)
        actual_avg = float(output_data["avg_delay_burden"])
        assert actual_avg == pytest.approx(expected_avg, rel=0, abs=0.01), (
            f"avg_delay_burden inconsistent with total_delay_burden / flight_count: "
            f"expected about {expected_avg}, got {actual_avg}"
        )

    def test_carrier_code_exists_in_airlines_csv(self, output_data):
        airlines = pd.read_csv(AIRLINES_FILE)
        valid_codes = set(airlines["Code"].astype(str))
        assert output_data["carrier_code"] in valid_codes, (
            f"carrier_code {output_data['carrier_code']!r} not found in airlines.csv"
        )

    def test_airline_name_matches_carrier_code_lookup(self, output_data):
        airlines = pd.read_csv(AIRLINES_FILE)
        match = airlines.loc[
            airlines["Code"].astype(str) == output_data["carrier_code"],
            "Description",
        ]
        assert not match.empty, f"carrier_code {output_data['carrier_code']!r} not found in airlines.csv"
        assert output_data["airline_name"] == str(match.iloc[0]), (
            f"airline_name mismatch for carrier_code {output_data['carrier_code']!r}: "
            f"expected {str(match.iloc[0])!r}, got {output_data['airline_name']!r}"
        )

    def test_carrier_code_appears_in_flights_data(self, output_data):
        flights = pd.read_csv(FLIGHTS_FILE)
        assert output_data["carrier_code"] in set(flights["carrier"].astype(str)), (
            f"carrier_code {output_data['carrier_code']!r} not found in flights_2.csv"
        )