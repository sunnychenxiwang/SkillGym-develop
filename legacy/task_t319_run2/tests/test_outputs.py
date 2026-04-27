"""Stronger expectation tests for the highest delay burden route task.

This version recomputes the expected answer directly from the source CSV files
according to the instruction, then compares the produced JSON exactly.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import pandas as pd
import pytest


OUTPUT_FILE = Path("/root/highest_delay_burden_route.json")
FLIGHTS_FILE = Path("/root/flights_2.csv")
AIRLINES_FILE = Path("/root/airlines.csv")

EXPECTED_KEYS = [
    "carrier",
    "airline_name",
    "origin",
    "dest",
    "n_valid_dep_delay",
    "mean_dep_delay",
    "delay_burden",
]


def compute_expected_result() -> dict:
    flights = pd.read_csv(FLIGHTS_FILE)
    airlines = pd.read_csv(AIRLINES_FILE)

    required_flight_cols = {"carrier", "origin", "dest", "dep_delay"}
    missing_flight_cols = required_flight_cols - set(flights.columns)
    assert not missing_flight_cols, f"Missing required flight columns: {missing_flight_cols}"

    required_airline_cols = {"Code", "Description"}
    missing_airline_cols = required_airline_cols - set(airlines.columns)
    assert not missing_airline_cols, f"Missing required airline columns: {missing_airline_cols}"

    # Follow the instruction: only include flights where dep_delay is not null.
    work = flights.copy()
    work["dep_delay"] = pd.to_numeric(work["dep_delay"], errors="coerce")
    work = work[work["dep_delay"].notna()].copy()

    # Constrain to January 2014 if year/month columns are present.
    if "year" in work.columns:
        work = work[work["year"] == 2014]
    if "month" in work.columns:
        work = work[work["month"] == 1]

    assert not work.empty, "No qualifying flights remain after filtering"

    grouped = (
        work.groupby(["carrier", "origin", "dest"], as_index=False)
        .agg(
            n_valid_dep_delay=("dep_delay", "size"),
            mean_dep_delay=("dep_delay", "mean"),
        )
    )
    grouped["delay_burden_unrounded"] = (
        grouped["mean_dep_delay"] * grouped["n_valid_dep_delay"]
    )

    # Deterministic selection:
    # 1) higher delay_burden
    # 2) higher mean_dep_delay
    # 3) higher n_valid_dep_delay
    # 4) lexicographically smallest carrier, then origin, then dest
    grouped = grouped.sort_values(
        by=[
            "delay_burden_unrounded",
            "mean_dep_delay",
            "n_valid_dep_delay",
            "carrier",
            "origin",
            "dest",
        ],
        ascending=[False, False, False, True, True, True],
        kind="mergesort",
    ).reset_index(drop=True)

    winner = grouped.iloc[0]

    carrier = winner["carrier"]
    match = airlines.loc[airlines["Code"] == carrier, "Description"]
    assert not match.empty, f"Carrier {carrier!r} not found in airlines.csv"
    airline_name = match.iloc[0]

    mean_dep_delay_rounded = round(float(winner["mean_dep_delay"]), 2)
    delay_burden_rounded = round(float(winner["delay_burden_unrounded"]), 2)

    return {
        "carrier": str(carrier),
        "airline_name": str(airline_name),
        "origin": str(winner["origin"]),
        "dest": str(winner["dest"]),
        "n_valid_dep_delay": int(winner["n_valid_dep_delay"]),
        "mean_dep_delay": mean_dep_delay_rounded,
        "delay_burden": delay_burden_rounded,
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


class TestOutputExists:
    def test_output_file_exists(self):
        assert OUTPUT_FILE.exists(), f"Output file not found at {OUTPUT_FILE}"

    def test_output_file_not_empty(self):
        assert OUTPUT_FILE.exists(), f"Output file not found at {OUTPUT_FILE}"
        assert OUTPUT_FILE.stat().st_size > 0, "Output file is empty"


class TestSchema:
    def test_json_is_object(self, output_data):
        assert isinstance(output_data, dict), f"Expected dict, got {type(output_data).__name__}"

    def test_exact_keys_present(self, output_data):
        assert list(output_data.keys()) == EXPECTED_KEYS, (
            f"JSON keys/order must be exactly {EXPECTED_KEYS}, got {list(output_data.keys())}"
        )

    def test_no_extra_or_missing_keys(self, output_data):
        assert set(output_data.keys()) == set(EXPECTED_KEYS), (
            f"Expected keys {set(EXPECTED_KEYS)}, got {set(output_data.keys())}"
        )


class TestFieldTypesAndBasicConstraints:
    def test_carrier_type(self, output_data):
        assert isinstance(output_data["carrier"], str)
        assert output_data["carrier"].strip() != ""

    def test_airline_name_type(self, output_data):
        assert isinstance(output_data["airline_name"], str)
        assert output_data["airline_name"].strip() != ""

    def test_origin_type_and_format(self, output_data):
        origin = output_data["origin"]
        assert isinstance(origin, str)
        assert len(origin) == 3 and origin.isupper() and origin.isalpha()

    def test_dest_type_and_format(self, output_data):
        dest = output_data["dest"]
        assert isinstance(dest, str)
        assert len(dest) == 3 and dest.isupper() and dest.isalpha()

    def test_origin_dest_different(self, output_data):
        assert output_data["origin"] != output_data["dest"]

    def test_n_valid_dep_delay_type(self, output_data):
        value = output_data["n_valid_dep_delay"]
        assert isinstance(value, int), f"n_valid_dep_delay should be int, got {type(value).__name__}"
        assert value > 0

    def test_mean_dep_delay_type(self, output_data):
        value = output_data["mean_dep_delay"]
        assert isinstance(value, (int, float)), f"mean_dep_delay should be numeric, got {type(value).__name__}"
        assert math.isfinite(float(value))

    def test_delay_burden_type(self, output_data):
        value = output_data["delay_burden"]
        assert isinstance(value, (int, float)), f"delay_burden should be numeric, got {type(value).__name__}"
        assert math.isfinite(float(value))

    def test_mean_dep_delay_rounded_2dp(self, output_data):
        value = float(output_data["mean_dep_delay"])
        assert value == round(value, 2), f"mean_dep_delay should be rounded to 2 decimals, got {value}"

    def test_delay_burden_rounded_2dp(self, output_data):
        value = float(output_data["delay_burden"])
        assert value == round(value, 2), f"delay_burden should be rounded to 2 decimals, got {value}"


class TestExactCorrectness:
    def test_carrier_matches_expected(self, output_data, expected_data):
        assert output_data["carrier"] == expected_data["carrier"], (
            f"carrier mismatch: expected {expected_data['carrier']!r}, got {output_data['carrier']!r}"
        )

    def test_airline_name_matches_expected(self, output_data, expected_data):
        assert output_data["airline_name"] == expected_data["airline_name"], (
            f"airline_name mismatch: expected {expected_data['airline_name']!r}, got {output_data['airline_name']!r}"
        )

    def test_origin_matches_expected(self, output_data, expected_data):
        assert output_data["origin"] == expected_data["origin"], (
            f"origin mismatch: expected {expected_data['origin']!r}, got {output_data['origin']!r}"
        )

    def test_dest_matches_expected(self, output_data, expected_data):
        assert output_data["dest"] == expected_data["dest"], (
            f"dest mismatch: expected {expected_data['dest']!r}, got {output_data['dest']!r}"
        )

    def test_n_valid_dep_delay_matches_expected(self, output_data, expected_data):
        assert output_data["n_valid_dep_delay"] == expected_data["n_valid_dep_delay"], (
            f"n_valid_dep_delay mismatch: expected {expected_data['n_valid_dep_delay']}, "
            f"got {output_data['n_valid_dep_delay']}"
        )

    def test_mean_dep_delay_matches_expected(self, output_data, expected_data):
        assert float(output_data["mean_dep_delay"]) == pytest.approx(
            float(expected_data["mean_dep_delay"]), rel=0, abs=1e-9
        ), (
            f"mean_dep_delay mismatch: expected {expected_data['mean_dep_delay']}, "
            f"got {output_data['mean_dep_delay']}"
        )

    def test_delay_burden_matches_expected(self, output_data, expected_data):
        assert float(output_data["delay_burden"]) == pytest.approx(
            float(expected_data["delay_burden"]), rel=0, abs=1e-9
        ), (
            f"delay_burden mismatch: expected {expected_data['delay_burden']}, "
            f"got {output_data['delay_burden']}"
        )


class TestInternalConsistency:
    def test_delay_burden_consistent_with_reported_mean_and_n(self, output_data):
        mean_delay = float(output_data["mean_dep_delay"])
        n_valid = int(output_data["n_valid_dep_delay"])
        expected_from_reported = round(mean_delay * n_valid, 2)
        actual = float(output_data["delay_burden"])

        # mean_dep_delay is itself rounded to 2 decimals in the JSON, so
        # reconstructing delay_burden from the reported mean can drift by up to
        # about 0.005 * n_valid, plus the final 2-decimal rounding on burden.
        tolerance = 0.005 * n_valid + 0.01
        assert actual == pytest.approx(expected_from_reported, rel=0, abs=tolerance), (
            f"delay_burden inconsistent with reported mean and count: "
            f"expected about {expected_from_reported}, got {actual}"
        )

    def test_airline_name_matches_airlines_lookup(self, output_data):
        airlines = pd.read_csv(AIRLINES_FILE)
        match = airlines.loc[airlines["Code"] == output_data["carrier"], "Description"]
        assert not match.empty, f"Carrier {output_data['carrier']!r} not found in airlines.csv"
        assert output_data["airline_name"] == match.iloc[0], (
            f"airline_name mismatch for carrier {output_data['carrier']!r}: "
            f"expected {match.iloc[0]!r}, got {output_data['airline_name']!r}"
        )
