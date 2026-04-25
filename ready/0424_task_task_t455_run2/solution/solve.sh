#!/bin/bash
set -e

# Create the solution Python script using heredoc
cat << 'EOF' > /root/solve_task.py
import pandas as pd
import statsmodels.api as sm
import json
import os

# Input paths
FLIGHTS_PATH = '/root/flights_2.csv'
AIRLINES_PATH = '/root/airlines.csv'
OUTPUT_PATH = '/root/output/steepest_distance_delay_carrier.json'

def main():
    # Load data
    flights = pd.read_csv(FLIGHTS_PATH, na_values=["NA"])
    airlines = pd.read_csv(AIRLINES_PATH)

    # Step 1: Filter rows - keep only where dep_delay and distance are both present and distance > 0
    f = flights.dropna(subset=["dep_delay", "distance"])
    f = f[f["distance"] > 0]

    # Step 2: Enforce >= 30 qualifying flights per carrier
    counts = f.groupby("carrier").size()
    eligible = counts[counts >= 30].index
    f2 = f[f["carrier"].isin(eligible)]

    # Step 3: For each eligible carrier, fit OLS dep_delay ~ distance with intercept
    results = []
    for c, g in f2.groupby("carrier"):
        X = sm.add_constant(g["distance"])
        y = g["dep_delay"]
        model = sm.OLS(y, X).fit()
        slope = float(model.params["distance"])
        n = int(len(g))
        results.append((c, n, slope))

    # Step 4: Select winner with tie-break rules
    # - Largest positive slope
    # - Tie-break by larger n_flights
    # - Tie-break by lexicographically smallest carrier code
    pos = [r for r in results if r[2] > 0]

    # Sort: -slope (descending), -n (descending), code (ascending)
    pos.sort(key=lambda x: (-x[2], -x[1], x[0]))

    winner_code, winner_n, winner_slope = pos[0]

    # Step 5: Map carrier code to full name
    name_map = dict(zip(airlines["Code"], airlines["Description"]))
    winner_name = name_map.get(winner_code, None)

    # Step 6: Output JSON
    out = {
        "carrier_code": winner_code,
        "carrier_name": winner_name,
        "n_flights": winner_n,
        "distance_slope": round(winner_slope, 6)
    }

    # Ensure output directory exists
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    with open(OUTPUT_PATH, "w") as outfile:
        json.dump(out, outfile, indent=2)

if __name__ == '__main__':
    main()
EOF

# Execute the script
python3 /root/solve_task.py
