# HARBOR_PATH_FIX_START
BASE_FIX="/root/harbor_workspaces/task_T430_run1"
mkdir -p "$BASE_FIX/input" "$BASE_FIX/output"
if [ ! -e "$BASE_FIX/input/case57.m" ] && [ -e "/root/case57.m" ]; then cp -f "/root/case57.m" "$BASE_FIX/input/case57.m"; fi
if [ ! -e "$BASE_FIX/input/case118.m" ] && [ -e "/root/case118.m" ]; then cp -f "/root/case118.m" "$BASE_FIX/input/case118.m"; fi
if [ ! -e "$BASE_FIX/input/pglib_opf_case118_ieee.m" ] && [ -e "/root/pglib_opf_case118_ieee.m" ]; then cp -f "/root/pglib_opf_case118_ieee.m" "$BASE_FIX/input/pglib_opf_case118_ieee.m"; fi
# HARBOR_PATH_FIX_END
#!/bin/bash

# Create output directory if it doesn't exist
mkdir -p /root/harbor_workspaces/task_T430_run1/output

# Run embedded Python script to parse MATPOWER files and compute result
python3 << 'PYTHON_SCRIPT'
import re
import json
from collections import defaultdict

def parse_matpower_branches(filepath):
    """Parse branch data from a MATPOWER case file.

    Returns a dict mapping (bus_i, bus_j) unordered pairs to list of x values.
    """
    with open(filepath, 'r') as f:
        content = f.read()

    # Find branch data section using regex
    match = re.search(r'mpc\.branch\s*=\s*\[\s*(.*?)\];', content, re.DOTALL)
    if not match:
        raise ValueError(f"Could not find mpc.branch in {filepath}")

    branch_text = match.group(1)

    # Remove comments
    branch_text = re.sub(r'%.*', '', branch_text)

    # Parse branch rows
    branches = defaultdict(list)

    for line in branch_text.split(';'):
        line = line.strip()
        if not line:
            continue

        # Split on whitespace
        values = line.split()
        if len(values) >= 4:
            fbus = int(float(values[0]))
            tbus = int(float(values[1]))
            x = float(values[3])  # Column 4 is x (reactance)

            # Create unordered pair
            bus_i = min(fbus, tbus)
            bus_j = max(fbus, tbus)

            branches[(bus_i, bus_j)].append(x)

    return branches

def compute_mean_x(branches):
    """Compute mean x value for each unordered bus pair."""
    return {pair: sum(x_vals) / len(x_vals) for pair, x_vals in branches.items()}

# File paths
input_dir = '/root/harbor_workspaces/task_T430_run1/input'
output_file = '/root/harbor_workspaces/task_T430_run1/output/max_reactance_change.json'

# Parse all three files
branches_57 = parse_matpower_branches(f'{input_dir}/case57.m')
branches_118 = parse_matpower_branches(f'{input_dir}/case118.m')
branches_pglib = parse_matpower_branches(f'{input_dir}/pglib_opf_case118_ieee.m')

# Compute mean x for each pair in each file
mean_x_57 = compute_mean_x(branches_57)
mean_x_118 = compute_mean_x(branches_118)
mean_x_pglib = compute_mean_x(branches_pglib)

# Find common pairs (present in all three files)
common_pairs = set(mean_x_57.keys()) & set(mean_x_118.keys()) & set(mean_x_pglib.keys())

# Compute pct_change for each common pair
results = []
for pair in common_pairs:
    x_case118 = mean_x_118[pair]
    x_pglib = mean_x_pglib[pair]

    # Skip if x_case118 is zero to avoid division by zero
    if x_case118 == 0:
        continue

    pct_change = abs(x_pglib - x_case118) / abs(x_case118)

    results.append({
        'pair': pair,
        'x_case118': x_case118,
        'x_pglib': x_pglib,
        'pct_change': pct_change
    })

# Sort by pct_change (descending), then by pair (ascending) for tie-breaking
results.sort(key=lambda r: (-r['pct_change'], r['pair']))

# Take the result with maximum pct_change (first after sorting)
if results:
    best = results[0]
    output = {
        'bus_i': best['pair'][0],
        'bus_j': best['pair'][1],
        'x_case118': best['x_case118'],
        'x_pglib': best['x_pglib'],
        'pct_change': best['pct_change']
    }
else:
    # Fallback if no common pairs found (shouldn't happen)
    output = {
        'bus_i': 0,
        'bus_j': 0,
        'x_case118': 0.0,
        'x_pglib': 0.0,
        'pct_change': 0.0
    }

# Write output JSON
with open(output_file, 'w') as f:
    json.dump(output, f, indent=2)

print(f"Result written to {output_file}")
print(json.dumps(output, indent=2))
PYTHON_SCRIPT

# HARBOR_OUTPUT_FIX_START
if [ -f "/root/harbor_workspaces/task_T430_run1/output/max_reactance_change.json" ]; then cp -f "/root/harbor_workspaces/task_T430_run1/output/max_reactance_change.json" "/root/max_reactance_change.json"; fi
# HARBOR_OUTPUT_FIX_END
