#!/bin/bash
set -euo pipefail

python3 <<'PY'
import csv
import json
from pathlib import Path


FLIGHTS_FILE = Path("/root/flights_2.csv")
AIRLINES_FILE = Path("/root/airlines.csv")
OUTPUT_FILE = Path("/root/max_avg_delay_burden_airline.json")


def parse_number(value: str):
    if value is None:
        return None
    text = str(value).strip()
    if text == "" or text.upper() == "NA":
        return None
    return float(text)


def load_airlines():
    code_to_name = {}
    with AIRLINES_FILE.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            code = str(row["Code"]).strip()
            description = str(row["Description"]).strip()
            code_to_name[code] = description
    return code_to_name


def compute_winner():
    stats = {}
    with FLIGHTS_FILE.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            year = str(row.get("year", "")).strip()
            month = str(row.get("month", "")).strip()
            if year != "2014" or month != "1":
                continue

            dep_delay = parse_number(row.get("dep_delay"))
            arr_delay = parse_number(row.get("arr_delay"))
            if dep_delay is None or arr_delay is None:
                continue

            carrier = str(row["carrier"]).strip()
            delay_burden = max(dep_delay, 0.0) + max(arr_delay, 0.0)

            if carrier not in stats:
                stats[carrier] = {
                    "total_delay_burden": 0.0,
                    "flight_count": 0,
                }

            stats[carrier]["total_delay_burden"] += delay_burden
            stats[carrier]["flight_count"] += 1

    if not stats:
        raise ValueError("No qualifying January 2014 rows with both dep_delay and arr_delay present")

    winner_code = None
    winner_avg = None
    for carrier in sorted(stats):
        total = stats[carrier]["total_delay_burden"]
        count = stats[carrier]["flight_count"]
        avg = total / count
        stats[carrier]["avg_delay_burden"] = avg
        if winner_code is None or avg > winner_avg:
            winner_code = carrier
            winner_avg = avg

    return winner_code, stats[winner_code]


def main():
    airlines = load_airlines()
    winner_code, winner_stats = compute_winner()
    if winner_code not in airlines:
        raise ValueError(f"Carrier code {winner_code!r} not found in airlines.csv")

    output = {
        "carrier_code": winner_code,
        "airline_name": airlines[winner_code],
        "avg_delay_burden": round(float(winner_stats["avg_delay_burden"]), 2),
        "total_delay_burden": round(float(winner_stats["total_delay_burden"]), 2),
        "flight_count": int(winner_stats["flight_count"]),
    }

    with OUTPUT_FILE.open("w", encoding="utf-8") as handle:
        json.dump(output, handle)


if __name__ == "__main__":
    main()
PY
