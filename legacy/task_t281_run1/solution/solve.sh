#!/bin/bash

set -euo pipefail

BASE_DIR="/root/harbor_workspaces/task_T281_run1"
INPUT_DIR="${BASE_DIR}/input"
OUTPUT_FILE="/root/variability_winner.json"

mkdir -p "${INPUT_DIR}"

if [ ! -e "${INPUT_DIR}/construction.csv" ] && [ -e "/root/construction.csv" ]; then
  cp -f "/root/construction.csv" "${INPUT_DIR}/construction.csv"
fi
if [ ! -e "${INPUT_DIR}/construction_spending.csv" ] && [ -e "/root/construction_spending.csv" ]; then
  cp -f "/root/construction_spending.csv" "${INPUT_DIR}/construction_spending.csv"
fi
if [ ! -e "${INPUT_DIR}/Dataset S9.csv" ] && [ -e "/root/Dataset S9.csv" ]; then
  cp -f "/root/Dataset S9.csv" "${INPUT_DIR}/Dataset S9.csv"
fi

python3 - <<'PY'
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

INPUT_DIR = Path("/root/harbor_workspaces/task_T281_run1/input")
OUTPUT_FILE = Path("/root/variability_winner.json")


def compute_cv(series: pd.Series):
    clean = pd.to_numeric(series, errors="coerce").dropna()
    if len(clean) < 2:
        return None
    mean_val = clean.mean()
    if pd.isna(mean_val) or not np.isfinite(mean_val) or abs(mean_val) < 1e-15:
        return None
    std_val = clean.std(ddof=1)
    if pd.isna(std_val) or not np.isfinite(std_val):
        return None
    cv = std_val / abs(mean_val)
    if not np.isfinite(cv):
        return None
    return float(cv)


def compute_construction_cv():
    df = pd.read_csv(INPUT_DIR / "construction.csv")
    df["date"] = pd.to_datetime(
        df["Year"].astype(str) + "-" + df["Month"].astype(str),
        format="%Y-%B",
    )
    df = df.sort_values("date")
    total = pd.to_numeric(df["Total"], errors="coerce")
    pct_change = total.pct_change().dropna()
    return compute_cv(pct_change)


def select_spending_column(df: pd.DataFrame):
    if "annual.combined.total" in df.columns:
        return "annual.combined.total"
    matching_cols = [
        col
        for col in df.columns
        if col.startswith("annual.combined.") and col.endswith(".total")
    ]
    if len(matching_cols) == 1:
        return matching_cols[0]
    return None


def compute_spending_cv():
    df = pd.read_csv(INPUT_DIR / "construction_spending.csv")
    if "time.period" not in df.columns:
        return None
    df = df[df["time.period"] == "annual"].copy()
    if df.empty:
        return None
    if "time.year" not in df.columns or "time.month" not in df.columns:
        return None
    df["date"] = pd.to_datetime(
        df["time.year"].astype(str) + "-" + df["time.month"].astype(str) + "-01"
    )
    df = df.sort_values("date")
    spending_col = select_spending_column(df)
    if spending_col is None:
        return None
    spending = pd.to_numeric(df[spending_col], errors="coerce")
    pct_change = spending.pct_change().dropna()
    return compute_cv(pct_change)


def compute_microbe_cv():
    df = pd.read_csv(INPUT_DIR / "Dataset S9.csv")
    df = df[df["Strain"] != "Blank"].copy()
    if df.empty:
        return None

    all_rates = []
    for (_strain, _replicate), group in df.groupby(["Strain", "Replicate"]):
        group = group.sort_values("Time_hours")
        od_values = pd.to_numeric(group["OD"], errors="coerce").to_numpy()
        time_values = pd.to_numeric(group["Time_hours"], errors="coerce").to_numpy()
        if len(od_values) < 2:
            continue
        delta_od = np.diff(od_values)
        delta_time = np.diff(time_values)
        valid_mask = np.isfinite(delta_od) & np.isfinite(delta_time) & (delta_time > 0)
        if not np.any(valid_mask):
            continue
        rates = delta_od[valid_mask] / delta_time[valid_mask]
        all_rates.extend(rates.tolist())

    if len(all_rates) < 2:
        return None
    return compute_cv(pd.Series(all_rates))


cv_construction = compute_construction_cv()
cv_spending = compute_spending_cv()
cv_microbe = compute_microbe_cv()

cv_mapping = {
    "construction": cv_construction,
    "construction_spending": cv_spending,
    "microbe": cv_microbe,
}
valid = {name: value for name, value in cv_mapping.items() if value is not None}
if valid:
    max_cv = max(valid.values())
    winner = sorted(name for name, value in valid.items() if value == max_cv)[0]
else:
    winner = ""

result = {
    "CV_construction": cv_construction,
    "CV_spending": cv_spending,
    "CV_microbe": cv_microbe,
    "winner": winner,
}

OUTPUT_FILE.write_text(json.dumps(result, indent=2), encoding="utf-8")
PY
