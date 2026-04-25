#!/bin/bash
set -e

# Create the output directory
mkdir -p /root/output

# Create the solution Python script using heredoc
cat << 'EOF' > /root/solve_task.py
"""
Process growth curve and construction data to create spending vs growth analysis workbook.
"""

import pandas as pd
import numpy as np
from openpyxl import load_workbook
from openpyxl.styles import Font
from openpyxl.utils.dataframe import dataframe_to_rows

# File paths
GROWTH_PATH = "/root/Dataset_S9.csv"
SPEND_PATH = "/root/construction_spending.csv"
HOUSE_PATH = "/root/construction.csv"
OUTPUT_PATH = "/root/output/spending_vs_growth_answer.xlsx"

# Step 1: Load all three CSVs
growth = pd.read_csv(GROWTH_PATH)
spend = pd.read_csv(SPEND_PATH)
house = pd.read_csv(HOUSE_PATH)

# Clean column names
growth["Strain"] = growth["Strain"].astype(str).str.strip()

# Step 2: Compute baseline-corrected OD
# Extract blank curve at each Time_hours
blank = (growth[(growth["Strain"] == "Blank") & (growth["Replicate"] == 0)]
         .groupby("Time_hours", as_index=False)
         .agg(blank_mean_od=("OD", "mean")))

# Merge blank mean onto all rows by Time_hours, then baseline-correct
g2 = growth.merge(blank, on="Time_hours", how="left")
g2["OD_bc"] = g2["OD"] - g2["blank_mean_od"]

# Step 3: Compute max growth rate per (Strain, Replicate) using consecutive slopes
# Filter to non-Blank strain+replicates
nonblank = g2[~((g2["Strain"] == "Blank") & (g2["Replicate"] == 0))].copy()
nonblank = nonblank.sort_values(["Strain", "Replicate", "Time_hours"])

# Compute consecutive slopes within each group
nonblank["dOD"] = nonblank.groupby(["Strain", "Replicate"])["OD_bc"].diff()
nonblank["dT"] = nonblank.groupby(["Strain", "Replicate"])["Time_hours"].diff()

# Filter out dT == 0 to avoid inf slopes
nonblank_valid = nonblank[nonblank["dT"] > 0].copy()
nonblank_valid["slope"] = nonblank_valid["dOD"] / nonblank_valid["dT"]

# Max slope per group
max_rates = (nonblank_valid.groupby(["Strain", "Replicate"], as_index=False)
             .agg(max_growth_rate=("slope", "max")))

# Calculate mean of max growth rates
mean_max_growth_rate = max_rates["max_growth_rate"].mean()

# Step 4: Compute annual_total_spending and spending_intensity
# Identify spending columns that start with "annual.combined."
spend_cols = [c for c in spend.columns if c.startswith("annual.combined.")]

# Ensure numeric
spend[spend_cols] = spend[spend_cols].apply(pd.to_numeric, errors="coerce")
spend["time.year"] = pd.to_numeric(spend["time.year"], errors="coerce")

# Row-wise sum across annual.combined.* then year sum
spend["row_annual_total"] = spend[spend_cols].sum(axis=1, skipna=True)

by_year = (spend.groupby("time.year", as_index=False)
           .agg(annual_total_spending=("row_annual_total", "sum")))

by_year["spending_intensity"] = by_year["annual_total_spending"] / mean_max_growth_rate

# Pick best year (max intensity, tie -> smallest year)
by_year_sorted = by_year.sort_values(
    ["spending_intensity", "time.year"],
    ascending=[False, True]
)

best = by_year_sorted.iloc[0]
best_year = int(best["time.year"])
annual_total_spending = best["annual_total_spending"]
spending_intensity = best["spending_intensity"]

# Step 5: Compute avg_monthly_total from construction.csv for best_year
house["Year"] = pd.to_numeric(house["Year"], errors="coerce")
house["Total"] = pd.to_numeric(house["Total"], errors="coerce")

if (house["Year"] == best_year).any():
    avg_monthly_total = house.loc[house["Year"] == best_year, "Total"].mean(skipna=True)
else:
    avg_monthly_total = None  # blank cell

# Step 6: Build the Excel workbook
# Create pivot table for Checks sheet: max_growth_rate by Strain and Replicate
pivot_rates = pd.pivot_table(
    max_rates, values="max_growth_rate",
    index="Strain", columns="Replicate",
    aggfunc="max"
)

# Year table for Checks
year_tbl = by_year.sort_values("time.year").copy()
year_tbl.columns = ["time_year", "annual_total_spending", "spending_intensity"]

# Summary row for Checks (to enable formula references)
summary_data = pd.DataFrame({
    "Metric": ["mean_max_growth_rate", "best_year", "best_annual_total_spending", "best_spending_intensity"],
    "Value": [mean_max_growth_rate, best_year, annual_total_spending, spending_intensity]
})

# Write to Excel using pandas first
with pd.ExcelWriter(OUTPUT_PATH, engine="openpyxl") as writer:
    # Checks sheet
    # 1. Pivot table of max_growth_rate
    pivot_rates.to_excel(writer, sheet_name="Checks", startrow=1, startcol=0)

    # 2. Year table below pivot
    pivot_end_row = pivot_rates.shape[0] + 4
    year_tbl.to_excel(writer, sheet_name="Checks", startrow=pivot_end_row, startcol=0, index=False)

    # 3. Summary metrics below year table
    summary_start_row = pivot_end_row + len(year_tbl) + 3
    summary_data.to_excel(writer, sheet_name="Checks", startrow=summary_start_row, startcol=0, index=False)

    # Answer sheet (just headers)
    ans_cols = ["mean_max_growth_rate", "best_year", "annual_total_spending", "spending_intensity", "avg_monthly_total"]
    pd.DataFrame(columns=ans_cols).to_excel(writer, sheet_name="Answer", index=False)

# Step 7: Re-open with openpyxl and apply formulas + formats
wb = load_workbook(OUTPUT_PATH)
ws_checks = wb["Checks"]
ws_answer = wb["Answer"]

# Add labels to Checks sheet
ws_checks["A1"] = "Max Growth Rate by Strain/Replicate"
ws_checks["A1"].font = Font(bold=True)

# Find the rows where summary data was written
mean_rate_row = summary_start_row + 2  # +1 for 0-index to 1-index, +1 for header
best_year_row = mean_rate_row + 1
best_spending_row = mean_rate_row + 2
best_intensity_row = mean_rate_row + 3

# Write Answer sheet with formulas referencing Checks
# A2: mean_max_growth_rate
ws_answer["A2"] = f"=Checks!B{mean_rate_row}"

# B2: best_year
ws_answer["B2"] = f"=Checks!B{best_year_row}"

# C2: annual_total_spending (with IFERROR)
ws_answer["C2"] = f'=IFERROR(Checks!B{best_spending_row},"-")'

# D2: spending_intensity (with IFERROR for division safety)
ws_answer["D2"] = f'=IFERROR(Checks!B{best_intensity_row},"-")'

# E2: avg_monthly_total
if avg_monthly_total is not None:
    ws_checks[f"A{best_intensity_row + 2}"] = "avg_monthly_total"
    ws_checks[f"B{best_intensity_row + 2}"] = avg_monthly_total
    ws_answer["E2"] = f"=Checks!B{best_intensity_row + 2}"
else:
    ws_checks[f"A{best_intensity_row + 2}"] = "avg_monthly_total"
    ws_checks[f"B{best_intensity_row + 2}"] = ""
    ws_answer["E2"] = f'=IF(Checks!B{best_intensity_row + 2}="","",Checks!B{best_intensity_row + 2})'

# Apply number formatting to Answer sheet
currency_format = '$#,##0;($#,##0);"-"'
ws_answer["C2"].number_format = currency_format
ws_answer["E2"].number_format = currency_format

# 3-decimal format for mean_max_growth_rate (A2) and spending_intensity (D2)
decimal_format = "0.000"
ws_answer["A2"].number_format = decimal_format
ws_answer["D2"].number_format = decimal_format

# Black font for computed values
black_font = Font(color="000000")
for cell in ["A2", "B2", "C2", "D2", "E2"]:
    ws_answer[cell].font = black_font

# Also format the Checks sheet for consistency
year_data_start = pivot_end_row + 2  # +1 for header
for row in range(year_data_start, year_data_start + len(year_tbl)):
    ws_checks[f"B{row}"].number_format = currency_format
    ws_checks[f"C{row}"].number_format = decimal_format

# Format summary values in Checks
ws_checks[f"B{mean_rate_row}"].number_format = decimal_format
ws_checks[f"B{best_spending_row}"].number_format = currency_format
ws_checks[f"B{best_intensity_row}"].number_format = decimal_format
if avg_monthly_total is not None:
    ws_checks[f"B{best_intensity_row + 2}"].number_format = currency_format

# Save the workbook
wb.save(OUTPUT_PATH)
print(f"Workbook saved to: {OUTPUT_PATH}")
EOF

# Execute the script
python3 /root/solve_task.py
