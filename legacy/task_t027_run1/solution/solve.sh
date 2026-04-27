#!/bin/bash
set -euo pipefail

# Input/output at /root (Harbor local environment symlinks files here)
IN_DIR="/root"
OUT_DIR="/root"

python3 << 'PYEOF'
import pandas as pd
import numpy as np
import json
import os

IN_DIR = "/root"
OUT_DIR = "/root"

DATASET_S9_PATH = os.path.join(IN_DIR, "Dataset_S9.csv")
CONSTRUCTION_PATH = os.path.join(IN_DIR, "construction.csv")
CONSTRUCTION_SPENDING_PATH = os.path.join(IN_DIR, "construction_spending.csv")
OUTPUT_PATH = os.path.join(OUT_DIR, "volatility_match.json")

# Month name to month number mapping for sorting
MONTH_TO_NUM = {
    "January": 1, "February": 2, "March": 3, "April": 4,
    "May": 5, "June": 6, "July": 7, "August": 8,
    "September": 9, "October": 10, "November": 11, "December": 12,
    "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
    "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12
}

# Step 1: Compute sigma_adv from Dataset S9
s9 = pd.read_csv(DATASET_S9_PATH)

# Exclude Blank rows
s9_nb = s9[s9["Strain"] != "Blank"].copy()

# Mean OD per (Strain, Time_hours)
s9_mean = s9_nb.groupby(["Strain", "Time_hours"])["OD"].mean().reset_index()

# Pivot to wide form
wide = s9_mean.pivot(index="Time_hours", columns="Strain", values="OD")

# Sort by Time_hours and compute advantage
wide = wide.sort_index()
adv = wide["LuxO"] - wide["C6706"]
d_adv = np.diff(adv.values)

# Sample standard deviation (ddof=1)
sigma_adv = np.std(d_adv, ddof=1)

# Step 2: Get restriction months from construction.csv (exact Year, Month pairs)
cons = pd.read_csv(CONSTRUCTION_PATH)
restriction_set = set(zip(cons["Year"], cons["Month"]))

# Step 3: Filter construction_spending by exact (time.year, time.month name) match
spend = pd.read_csv(CONSTRUCTION_SPENDING_PATH)

# Filter rows by exact match
mask = spend.apply(
    lambda row: (row["time.year"], row["time.month name"]) in restriction_set,
    axis=1
)
spend_restricted = spend[mask].copy()

matched_months_count = len(spend_restricted)

# Step 4: Sort by (year, month_num)
spend_restricted["month_num"] = spend_restricted["time.month name"].map(MONTH_TO_NUM)
spend_restricted = spend_restricted.sort_values(["time.year", "month_num"]).reset_index(drop=True)

# Step 5: Identify candidate columns (annual.combined.* per output schema requirement)
candidates = [c for c in spend_restricted.columns if c.startswith("annual.combined.")]

# Step 6: Compute sigma_c for each candidate
results = []
for c in candidates:
    values = pd.to_numeric(spend_restricted[c], errors="coerce").values
    if np.any(np.isnan(values)):
        continue
    if len(values) >= 3:  # Need at least 3 values for 2 diffs with ddof=1
        d_c = np.diff(values)
        if len(d_c) >= 2:
            sigma_c = np.std(d_c, ddof=1)
            if np.isfinite(sigma_c):
                gap = abs(sigma_c - sigma_adv)
                results.append((c, sigma_c, gap))

# Step 7: Find winner (minimum gap, lexicographic tie-break)
results.sort(key=lambda x: (x[2], x[0]))
winner_column, sigma_winner, abs_gap = results[0]

# Step 8: Write output JSON
output = {
    "winner_column": winner_column,
    "sigma_adv": round(float(sigma_adv), 6),
    "sigma_winner": round(float(sigma_winner), 6),
    "abs_gap": round(float(abs_gap), 6),
    "matched_months_count": int(matched_months_count)
}

with open(OUTPUT_PATH, "w") as f:
    json.dump(output, f, indent=2)
    f.write("\n")

print(f"Output written to {OUTPUT_PATH}")
print(json.dumps(output, indent=2))
PYEOF

echo "solve.sh completed"
