#!/bin/bash
set -e

# Create output directory if needed
mkdir -p /root/output

# Create the solution Python script using heredoc
cat << 'EOF' > /root/solve_task.py
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font

# Input and output paths
FLIGHTS_PATH = "/root/flights_2.csv"
AIRLINES_PATH = "/root/airlines.csv"
OUTPUT_PATH = "/root/output/sea_lax_worst_carrier.xlsx"

def main():
    # Read flights and filter to SEA->LAX with non-missing arr_delay
    flights = pd.read_csv(FLIGHTS_PATH, na_values=["NA"])
    filtered = flights[
        (flights["origin"] == "SEA") &
        (flights["dest"] == "LAX") &
        (flights["arr_delay"].notna())
    ].copy()

    # Compute summary stats per carrier
    summary = (filtered.groupby("carrier")
               .agg(flight_count_used=("arr_delay", "size"),
                    avg_arr_delay_min=("arr_delay", "mean"))
               .reset_index())
    summary["avg_arr_delay_min"] = summary["avg_arr_delay_min"].round(2)

    # Sort by avg_arr_delay_min descending, then carrier ascending
    summary = summary.sort_values(
        ["avg_arr_delay_min", "carrier"],
        ascending=[False, True]
    ).reset_index(drop=True)

    # Merge with airlines to get carrier names
    airlines = pd.read_csv(AIRLINES_PATH)
    summary = summary.merge(
        airlines[["Code", "Description"]],
        left_on="carrier",
        right_on="Code",
        how="left"
    )
    summary = summary.drop(columns=["Code"]).rename(columns={"Description": "carrier_name"})
    summary = summary[["carrier", "carrier_name", "flight_count_used", "avg_arr_delay_min"]]

    # Get worst carrier (first row after sorting)
    worst_carrier_code = summary.loc[0, "carrier"]
    worst_carrier_name = summary.loc[0, "carrier_name"]

    # Create Excel workbook
    wb = Workbook()

    # Sheet 1: Route_Carrier_Summary
    ws_sum = wb.active
    ws_sum.title = "Route_Carrier_Summary"

    # Write headers with bold formatting
    headers = ["carrier", "carrier_name", "flight_count_used", "avg_arr_delay_min"]
    for c, h in enumerate(headers, start=1):
        cell = ws_sum.cell(row=1, column=c, value=h)
        cell.font = Font(bold=True)

    # Write data rows
    for r_idx, row in enumerate(summary.itertuples(index=False), start=2):
        ws_sum.cell(r_idx, 1, row.carrier)
        ws_sum.cell(r_idx, 2, row.carrier_name)
        ws_sum.cell(r_idx, 3, int(row.flight_count_used))
        delay_cell = ws_sum.cell(r_idx, 4, float(row.avg_arr_delay_min))
        delay_cell.number_format = "0.00"

    # Sheet 2: Answer
    ws_ans = wb.create_sheet("Answer")

    ws_ans["A1"] = "worst_carrier_code"
    ws_ans["B1"] = worst_carrier_code

    ws_ans["A2"] = "worst_carrier_name"
    ws_ans["B2"] = worst_carrier_name

    ws_ans["A3"] = "worst_avg_arr_delay_min"
    # Cross-sheet formula referencing D2 (first data row) from Route_Carrier_Summary
    ws_ans["B3"] = "='Route_Carrier_Summary'!D2"
    ws_ans["B3"].number_format = "0.00"

    # Save workbook
    wb.save(OUTPUT_PATH)
    print(f"Workbook saved to {OUTPUT_PATH}")
    print(f"Worst carrier: {worst_carrier_code} ({worst_carrier_name})")

if __name__ == '__main__':
    main()
EOF

# Execute the script
python3 /root/solve_task.py
