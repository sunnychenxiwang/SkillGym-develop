#!/bin/bash
set -e

# Create the solution Python script using heredoc
cat << 'EOF' > /root/solve_task.py
#!/usr/bin/env python3
"""Iris species driver analysis - R² contribution analysis to identify top measurement."""

import csv
import numpy as np
import polars as pl
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.drawing.image import Image
import os

INPUT_PATH = "/root/iris.csv"
OUTPUT_PATH = "/root/output/iris_species_driver.xlsx"
CHART_PATH = "/root/output/contributions_chart.png"

EXPECTED_HEADERS = ["sepal_length", "sepal_width", "petal_length", "petal_width", "species"]
MEASUREMENTS = ["petal_length", "petal_width", "sepal_length", "sepal_width"]  # alphabetical

# Ensure output directory exists
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

# Step 1: Streaming CSV header validation
print("Step 1: Validating CSV headers using streaming approach...")
with open(INPUT_PATH, "r", newline="") as f:
    reader = csv.DictReader(f)
    headers = list(reader.fieldnames)

assert headers == EXPECTED_HEADERS, f"Header mismatch: got {headers}, expected {EXPECTED_HEADERS}"
print(f"  Headers validated: {headers}")

# Step 2: High-performance load with polars + deterministic dummy encoding
print("\nStep 2: Loading data with polars and creating dummy variables...")
df = pl.read_csv(INPUT_PATH)
print(f"  Loaded {df.shape[0]} rows, {df.shape[1]} columns")

species_order = sorted(df["species"].unique().to_list())
print(f"  Species (alphabetical): {species_order}")
assert len(species_order) == 3, f"Expected 3 species, got {len(species_order)}"

baseline = species_order[0]  # setosa
dummies = species_order[1:]  # versicolor, virginica

df_model = df.with_columns([
    pl.when(pl.col("species") == dummies[0]).then(1.0).otherwise(0.0).alias(f"species_{dummies[0]}"),
    pl.when(pl.col("species") == dummies[1]).then(1.0).otherwise(0.0).alias(f"species_{dummies[1]}")
])

print(f"  Created dummy columns: species_{dummies[0]}, species_{dummies[1]}")
print(f"  Baseline species: {baseline}")

# Step 3: Contribution analysis via averaged multi-target R²
print("\nStep 3: Performing R² contribution analysis...")

X_raw = df_model.select(MEASUREMENTS).to_numpy()
Y = df_model.select([f"species_{d}" for d in dummies]).to_numpy()

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_raw)

def calc_avg_r2(X, Y):
    """Calculate average R² across multiple targets."""
    model = LinearRegression()
    model.fit(X, Y)
    r2_values = []
    for i in range(Y.shape[1]):
        y_pred = model.predict(X)[:, i]
        y_true = Y[:, i]
        ss_res = np.sum((y_true - y_pred) ** 2)
        ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
        r2 = 1 - (ss_res / ss_tot)
        r2_values.append(r2)
    return np.mean(r2_values)

avg_r2_full = calc_avg_r2(X_scaled, Y)
print(f"  Full model average R²: {avg_r2_full:.6f}")

contributions = {}
for i, measurement in enumerate(MEASUREMENTS):
    idx_keep = [j for j in range(len(MEASUREMENTS)) if j != i]
    X_reduced = X_scaled[:, idx_keep]
    avg_r2_reduced = calc_avg_r2(X_reduced, Y)
    contribution = avg_r2_full - avg_r2_reduced
    contributions[measurement] = contribution
    print(f"  {measurement}: R² without = {avg_r2_reduced:.6f}, contribution = {contribution:.6f}")

sorted_contributions = sorted(contributions.items(), key=lambda x: (-x[1], x[0]))
top_measurement = sorted_contributions[0][0]
top_contribution = sorted_contributions[0][1]

print(f"\n  Top measurement: {top_measurement} with contribution {top_contribution:.6f}")

# Step 4: Create bar chart
print("\nStep 4: Creating bar chart...")
contrib_df_sorted = sorted_contributions

fig, ax = plt.subplots(figsize=(8, 5))
measurements_sorted = [x[0] for x in contrib_df_sorted]
values_sorted = [x[1] for x in contrib_df_sorted]

bars = ax.bar(measurements_sorted, values_sorted, color='steelblue', edgecolor='navy')
ax.set_xlabel('Measurement', fontsize=11)
ax.set_ylabel('R² Contribution', fontsize=11)
ax.set_title('Contribution of Each Measurement to Species Prediction', fontsize=12)
ax.set_ylim(bottom=0)

for bar, val in zip(bars, values_sorted):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.002,
            f'{val:.4f}', ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig(CHART_PATH, dpi=150, bbox_inches='tight')
plt.close()
print(f"  Chart saved to {CHART_PATH}")

# Step 5: Create Excel workbook with professional formatting
print("\nStep 5: Creating Excel workbook...")

wb = Workbook()
ws_result = wb.active
ws_result.title = "Result"

header_fill = PatternFill(start_color='D9E1F2', end_color='D9E1F2', fill_type='solid')
header_font = Font(bold=True, color='000000')
blue_font = Font(color='0000FF')
black_font = Font(color='000000')

ws_result['A1'] = 'Top_Measurement'
ws_result['B1'] = 'Contribution'
ws_result['C1'] = 'Avg_R2_Full'

for col in ['A', 'B', 'C']:
    ws_result[f'{col}1'].fill = header_fill
    ws_result[f'{col}1'].font = header_font
    ws_result[f'{col}1'].alignment = Alignment(horizontal='center')

ws_result['A2'] = top_measurement
ws_result['A2'].font = blue_font

ws_result['B2'] = top_contribution
ws_result['B2'].number_format = '0.0000'
ws_result['B2'].font = black_font

ws_result['C2'] = avg_r2_full
ws_result['C2'].number_format = '0.0000'
ws_result['C2'].font = black_font

ws_result.column_dimensions['A'].width = 18
ws_result.column_dimensions['B'].width = 14
ws_result.column_dimensions['C'].width = 14

ws_contrib = wb.create_sheet("Contributions")

ws_contrib['A1'] = 'Measurement'
ws_contrib['B1'] = 'Contribution'

for col in ['A', 'B']:
    ws_contrib[f'{col}1'].fill = header_fill
    ws_contrib[f'{col}1'].font = header_font
    ws_contrib[f'{col}1'].alignment = Alignment(horizontal='center')

for row_idx, (measurement, contribution) in enumerate(sorted_contributions, start=2):
    ws_contrib[f'A{row_idx}'] = measurement
    ws_contrib[f'B{row_idx}'] = contribution
    ws_contrib[f'B{row_idx}'].number_format = '0.0000'

ws_contrib.column_dimensions['A'].width = 16
ws_contrib.column_dimensions['B'].width = 14

img = Image(CHART_PATH)
img.anchor = 'D2'
ws_contrib.add_image(img)

wb.save(OUTPUT_PATH)
print(f"  Workbook saved to {OUTPUT_PATH}")

print(f"\nOutput file exists: {os.path.exists(OUTPUT_PATH)}")
EOF

# Execute the script
python3 /root/solve_task.py
