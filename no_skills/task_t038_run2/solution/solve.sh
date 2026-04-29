#!/bin/bash
# solve.sh - Recreates output files for microbial growth / construction matching task

set -e

# Create the main analysis script
python3 << 'ANALYSIS_EOF'
import pandas as pd
import numpy as np
import json

IN_DIR = "/root"
OUT_DIR = "/root"

# ==============================
# Step 1: Load all three CSVs
# ==============================
growth_df = pd.read_csv(f'{IN_DIR}/Dataset_S9.csv', na_values=["NA"])
starts_df = pd.read_csv(f'{IN_DIR}/construction.csv', na_values=["NA"])
spend_df = pd.read_csv(f'{IN_DIR}/construction_spending.csv', na_values=["NA"])

print("Loaded datasets:")
print(f"  Growth: {len(growth_df)} rows")
print(f"  Starts: {len(starts_df)} rows")
print(f"  Spending: {len(spend_df)} rows")

# ==============================
# Step 2: Compute t_median_hours from growth data
# ==============================

# Exclude Blank strain
non_blank = growth_df[growth_df['Strain'] != 'Blank'].copy()
print(f"\nNon-blank growth data: {len(non_blank)} rows")

# For each (Strain, Replicate) series, baseline-correct OD and find earliest time where corrected OD >= 0.30
def find_time_to_threshold(group):
    g = group.sort_values('Time_hours').copy()
    baseline_od = g['OD'].iloc[0]
    g['OD_corr'] = g['OD'] - baseline_od
    above_threshold = g[g['OD_corr'] >= 0.30]
    if len(above_threshold) > 0:
        return above_threshold['Time_hours'].iloc[0]
    else:
        return np.nan

time_to_threshold = non_blank.groupby(['Strain', 'Replicate']).apply(
    find_time_to_threshold, include_groups=False
)
print(f"\nTime-to-threshold values per series:")
print(time_to_threshold)

t_median_hours = time_to_threshold.median()
print(f"\nt_median_hours = {t_median_hours}")

# ==============================
# Step 3: Compute p_target
# ==============================
p_target = min(1, max(0, t_median_hours / 10))
print(f"p_target = {p_target}")

# ==============================
# Step 4: Percentile rank computation function
# ==============================

# Month name to number mapping
month_map = {
    'January': 1, 'February': 2, 'March': 3, 'April': 4,
    'May': 5, 'June': 6, 'July': 7, 'August': 8,
    'September': 9, 'October': 10, 'November': 11, 'December': 12
}

def compute_percentile_rank_descending(df, value_col, year_col, month_col, original_index_col):
    """
    Compute percentile rank with DESCENDING order (higher value = higher percentile).
    p = (rank - 1) / (N - 1) where rank 1 is highest value
    """
    n = len(df)
    if n <= 1:
        return pd.Series([0.5] * n, index=df.index)

    work_df = df[[value_col, year_col, month_col, original_index_col]].copy()

    # Sort by value descending, then by year ascending, then by month ascending for ties
    work_df = work_df.sort_values(
        by=[value_col, year_col, month_col, original_index_col],
        ascending=[False, True, True, True]
    )

    # Assign integer ranks 1..N in sorted order (highest value gets rank 1)
    work_df["rank"] = range(1, n + 1)

    # Compute percentile: (rank - 1) / (N - 1)
    work_df["percentile"] = (work_df["rank"] - 1) / (n - 1)

    return work_df["percentile"].reindex(df.index)

# ==============================
# Step 5: Compute p_starts from construction.csv
# ==============================

starts_df['starts_total'] = pd.to_numeric(starts_df['Total'], errors='coerce')
starts_df = starts_df.dropna(subset=['starts_total']).copy()
starts_df['month_num'] = starts_df['Month'].map(month_map)
starts_df['original_idx'] = range(len(starts_df))

starts_df['p_starts'] = compute_percentile_rank_descending(
    starts_df, 'starts_total', 'Year', 'month_num', 'original_idx'
)

N_starts = len(starts_df)
print(f"\nStarts data with ranks (N={N_starts}):")

# ==============================
# Step 6: Compute p_spend from construction_spending.csv
# ==============================

spend_df['spend_total'] = pd.to_numeric(spend_df['current.combined.total construction'], errors='coerce')
spend_df = spend_df.dropna(subset=['spend_total']).copy()
spend_df['year'] = pd.to_numeric(spend_df['time.year'], errors='coerce').astype(int)
spend_df['month_num'] = pd.to_numeric(spend_df['time.month'], errors='coerce').astype(int)
spend_df['month_name'] = spend_df['time.month name']
spend_df['original_idx'] = range(len(spend_df))

spend_df['p_spend'] = compute_percentile_rank_descending(
    spend_df, 'spend_total', 'year', 'month_num', 'original_idx'
)

N_spend = len(spend_df)
print(f"\nSpending data with ranks (N={N_spend}):")

# ==============================
# Step 7: Find overlapping (year, month) pairs
# ==============================

print(f"\nStarts years: {sorted(starts_df['Year'].unique())}")
print(f"Spending years: {sorted(spend_df['year'].unique())}")

starts_keys = set(zip(starts_df['Year'], starts_df['month_num']))
spend_keys = set(zip(spend_df['year'], spend_df['month_num']))

overlap_keys = starts_keys.intersection(spend_keys)
print(f"\nOverlapping (year, month) pairs: {len(overlap_keys)}")

if not overlap_keys:
    print("ERROR: No overlapping (year, month) pairs found!")
    exit(1)

# Build index lookups for p values
starts_p_lookup = {}
for _, row in starts_df.iterrows():
    key = (row['Year'], row['month_num'])
    starts_p_lookup[key] = {
        'p_starts': row['p_starts'],
        'month_name': row['Month'],
        'value': row['starts_total'],
        'original_idx': row['original_idx']
    }

spend_p_lookup = {}
for _, row in spend_df.iterrows():
    key = (row['year'], row['month_num'])
    spend_p_lookup[key] = {
        'p_spend': row['p_spend'],
        'month_name': row['month_name'],
        'value': row['spend_total']
    }

# Compute scores for overlapping months
results = []
for year, month_num in overlap_keys:
    starts_info = starts_p_lookup[(year, month_num)]
    spend_info = spend_p_lookup[(year, month_num)]

    p_starts = starts_info['p_starts']
    p_spend = spend_info['p_spend']
    score = abs(p_starts - p_target) + abs(p_spend - p_target)

    results.append({
        'year': year,
        'month_num': month_num,
        'month_name': starts_info['month_name'],
        'p_starts': p_starts,
        'p_spend': p_spend,
        'score': score,
        'file_order': starts_info['original_idx']
    })

results_df = pd.DataFrame(results)
print(f"\nResults ({len(results_df)} candidates):")
print(results_df.sort_values('score').to_string())

# ==============================
# Step 8: Find best match (minimum score, tie-break by earliest date)
# ==============================

results_df = results_df.sort_values(
    ['score', 'year', 'month_num'],
    ascending=[True, True, True]
)

best = results_df.iloc[0]

print(f"\nBest match:")
print(f"  Year: {best['year']}")
print(f"  Month: {best['month_name']}")
print(f"  p_starts: {best['p_starts']:.6f}")
print(f"  p_spend: {best['p_spend']:.6f}")
print(f"  Score: {best['score']:.6f}")

# ==============================
# Step 9: Write output JSON
# ==============================

output = {
    "t_median_hours": float(t_median_hours),
    "p_target": float(p_target),
    "best_match": {
        "year": int(best['year']),
        "month": str(best['month_name']),
        "p_starts": float(best['p_starts']),
        "p_spend": float(best['p_spend']),
        "score": float(best['score'])
    }
}

output_path = f'{OUT_DIR}/best_match_month.json'
with open(output_path, 'w') as f:
    json.dump(output, f, indent=2)

print(f"\nOutput written to {output_path}")
print(json.dumps(output, indent=2))
ANALYSIS_EOF

echo ""
echo "=== solve.sh completed ==="
