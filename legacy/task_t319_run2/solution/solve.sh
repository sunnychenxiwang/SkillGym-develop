#!/bin/bash
set -euo pipefail

python3 <<'PY'
import csv
import json
from pathlib import Path


FLIGHTS_FILE = Path("/root/flights_2.csv")
AIRLINES_FILE = Path("/root/airlines.csv")
OUTPUT_FILE = Path("/root/highest_delay_burden_route.json")


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
            code_to_name[str(row["Code"]).strip()] = str(row["Description"]).strip()
    return code_to_name


def compute_route_stats():
    stats = {}
    with FLIGHTS_FILE.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            year = str(row.get("year", "")).strip()
            month = str(row.get("month", "")).strip()
            if year != "2014" or month != "1":
                continue

            dep_delay = parse_number(row.get("dep_delay"))
            if dep_delay is None:
                continue

            carrier = str(row["carrier"]).strip()
            origin = str(row["origin"]).strip()
            dest = str(row["dest"]).strip()
            key = (carrier, origin, dest)

            if key not in stats:
                stats[key] = {
                    "n_valid_dep_delay": 0,
                    "dep_delay_sum": 0.0,
                }

            stats[key]["n_valid_dep_delay"] += 1
            stats[key]["dep_delay_sum"] += dep_delay

    if not stats:
        raise ValueError("No qualifying January 2014 rows with non-null dep_delay")

    for key, values in stats.items():
        count = values["n_valid_dep_delay"]
        mean_dep_delay = values["dep_delay_sum"] / count
        values["mean_dep_delay"] = mean_dep_delay
        values["delay_burden"] = mean_dep_delay * count

    return stats


def select_winner(stats):
    winner_key = None
    winner_values = None

    for key in sorted(stats.keys()):
        values = stats[key]
        if winner_key is None:
            winner_key = key
            winner_values = values
            continue

        candidate_rank = (
            values["delay_burden"],
            values["mean_dep_delay"],
            values["n_valid_dep_delay"],
        )
        winner_rank = (
            winner_values["delay_burden"],
            winner_values["mean_dep_delay"],
            winner_values["n_valid_dep_delay"],
        )

        if candidate_rank > winner_rank:
            winner_key = key
            winner_values = values

    return winner_key, winner_values


def main():
    airlines = load_airlines()
    stats = compute_route_stats()
    winner_key, winner_values = select_winner(stats)
    carrier, origin, dest = winner_key

    if carrier not in airlines:
        raise ValueError(f"Carrier code {carrier!r} not found in airlines.csv")

    output = {
        "carrier": carrier,
        "airline_name": airlines[carrier],
        "origin": origin,
        "dest": dest,
        "n_valid_dep_delay": int(winner_values["n_valid_dep_delay"]),
        "mean_dep_delay": round(float(winner_values["mean_dep_delay"]), 2),
        "delay_burden": round(float(winner_values["delay_burden"]), 2),
    }

    with OUTPUT_FILE.open("w", encoding="utf-8") as handle:
        json.dump(output, handle)


if __name__ == "__main__":
    main()
PY
