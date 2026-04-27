#!/bin/bash
set -e

# Create output directory if needed
mkdir -p /root/output

# Create the solution Python script using heredoc
cat << 'EOF' > /root/solve_task.py
import pandas as pd
import json

# Input paths
FLIGHTS_PATH = "/root/flights_2.csv"
AIRLINES_PATH = "/root/airlines.csv"
OUTPUT_PATH = "/root/output/sea_lax_best_carrier_2014.json"

def main():
    # Load flights data with NA values properly handled
    df = pd.read_csv(FLIGHTS_PATH, na_values=["NA"])

    # Filter for SEA→LAX flights in 2014
    sea_lax = df[(df["year"] == 2014) & (df["origin"] == "SEA") & (df["dest"] == "LAX")]

    # Exclude cancelled flights (arr_delay is NA)
    included = sea_lax[sea_lax["arr_delay"].notna()].copy()

    # Compute on-time flag (arr_delay <= 15)
    included["on_time"] = included["arr_delay"] <= 15

    # Group by carrier and compute metrics
    carrier_summary = (
        included.groupby("carrier")
        .agg(
            total_flights_included=("on_time", "size"),
            on_time_flights=("on_time", "sum"),
        )
        .assign(on_time_rate=lambda x: x["on_time_flights"] / x["total_flights_included"])
        .reset_index()
    )

    # Sort by: highest on_time_rate, then higher total_flights_included, then smallest carrier code
    carrier_summary = carrier_summary.sort_values(
        by=["on_time_rate", "total_flights_included", "carrier"],
        ascending=[False, False, True],
        kind="mergesort"
    )

    # Get the winner
    winner = carrier_summary.iloc[0]
    winning_code = str(winner["carrier"])
    winning_rate = float(winner["on_time_rate"])
    winning_total = int(winner["total_flights_included"])

    # Load airlines.csv to get full name
    airlines_df = pd.read_csv(AIRLINES_PATH)

    # Find the airline name for the winning code
    airline_match = airlines_df[airlines_df["Code"] == winning_code]
    if len(airline_match) > 0:
        winning_name = airline_match.iloc[0]["Description"]
    else:
        winning_name = f"Unknown ({winning_code})"

    # Create output JSON with exact schema
    out = {
        "route": "SEA-LAX",
        "year": 2014,
        "winning_carrier_code": winning_code,
        "winning_carrier_name": winning_name,
        "on_time_rate": winning_rate,
        "total_flights_included": winning_total
    }

    # Write to output file
    with open(OUTPUT_PATH, "w") as f:
        json.dump(out, f, indent=2)

if __name__ == '__main__':
    main()
EOF

# Execute the script
python3 /root/solve_task.py
