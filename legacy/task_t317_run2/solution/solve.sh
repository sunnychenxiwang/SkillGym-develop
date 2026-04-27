#!/bin/bash
python3 << 'EOF'
import csv
import json

# Input files (harbor symlinks to /root/)
FLIGHTS_FILE = "/root/flights_2.csv"
AIRLINES_FILE = "/root/airlines.csv"
OUTPUT_FILE = "/root/worst_airline_by_mean_arr_delay.json"

# Missing value markers
MISSING_VALUE_MARKERS = {'', 'NA', 'NAN', 'N/A', 'NULL', 'NONE', 'NaN'}

def is_missing_value(value):
    if value is None:
        return True
    if not isinstance(value, str):
        return False
    stripped = value.strip()
    if stripped == '':
        return True
    return stripped.upper() in MISSING_VALUE_MARKERS

def parse_numeric_or_none(value):
    if is_missing_value(value):
        return None
    try:
        import math
        result = float(value.strip())
        if math.isnan(result):
            return None
        return result
    except (ValueError, AttributeError):
        return None

# Load airlines mapping (Code -> lexicographically smallest Description)
airlines_mapping = {}
with open(AIRLINES_FILE, newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        code = row['Code']
        desc = row['Description']
        if code not in airlines_mapping or desc < airlines_mapping[code]:
            airlines_mapping[code] = desc

# Compute per-carrier statistics
carrier_delays = {}
with open(FLIGHTS_FILE, newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        carrier = row.get('carrier', '')
        arr_delay_raw = row.get('arr_delay')
        arr_delay = parse_numeric_or_none(arr_delay_raw)
        if arr_delay is None:
            continue
        if carrier not in carrier_delays:
            carrier_delays[carrier] = []
        carrier_delays[carrier].append(arr_delay)

# Compute mean delay for each carrier
carrier_stats = {}
for carrier, delays in carrier_delays.items():
    if delays:
        mean_delay = sum(delays) / len(delays)
        carrier_stats[carrier] = {
            'mean_arr_delay': round(mean_delay, 3),
            'flight_count': len(delays)
        }

# Find worst carrier (highest mean delay, tiebreaker: lexicographically smallest code)
max_mean = max(stats['mean_arr_delay'] for stats in carrier_stats.values())
tied_carriers = sorted([
    code for code, stats in carrier_stats.items()
    if abs(stats['mean_arr_delay'] - max_mean) < 1e-6
])
worst_carrier = tied_carriers[0]

# Build output
result = {
    "carrier_code": worst_carrier,
    "airline_description": airlines_mapping.get(worst_carrier, ''),
    "flight_count_used": carrier_stats[worst_carrier]['flight_count'],
    "mean_arr_delay_minutes": carrier_stats[worst_carrier]['mean_arr_delay']
}

# Write compact JSON
with open(OUTPUT_FILE, 'w') as f:
    json.dump(result, f, separators=(',', ':'))

print(f"Output written to {OUTPUT_FILE}")
EOF
