#!/bin/bash
set -e

# Create output directory
mkdir -p /root/output

# Create the solution Python script using heredoc
cat << 'EOF' > /root/solve_task.py
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font

# Input paths
S9_PATH = "/root/Dataset_S9.csv"
CONSTRUCTION_PATH = "/root/construction.csv"
SPENDING_PATH = "/root/construction_spending.csv"
OUTPUT_PATH = "/root/output/blank_distortion_construction_scaled.xlsx"

def main():
    # Step 1: Load Dataset_S9.csv and compute BDR
    s9 = pd.read_csv(S9_PATH)
    key = "Time_hours"

    # Mean OD across all strains/replicates at each timestamp
    mean_all = s9.groupby(key)["OD"].mean()

    # Mean OD across non-Blank strains at each timestamp
    mean_nonblank = s9[s9["Strain"] != "Blank"].groupby(key)["OD"].mean()

    # Mean OD of Blank (Replicate=0) at each timestamp
    mean_blank = s9[(s9["Strain"] == "Blank") & (s9["Replicate"] == 0)].groupby(key)["OD"].mean()

    # Combine into dataframe for calculation
    tmp = pd.concat([mean_all, mean_nonblank, mean_blank], axis=1)
    tmp.columns = ["mean_all", "mean_nonblank", "mean_blank"]
    tmp["Net_OD"] = tmp["mean_nonblank"] - tmp["mean_blank"]

    # BDR = sum(|mean_all - mean_nonblank|) / sum(|Net_OD|)
    numerator = (tmp["mean_all"] - tmp["mean_nonblank"]).abs().sum()
    denominator = tmp["Net_OD"].abs().sum()
    bdr = numerator / denominator

    # Step 2: Compute permits grand mean from construction.csv
    cons = pd.read_csv(CONSTRUCTION_PATH)
    permits_mean = cons["Total"].mean()

    # Step 3: Compute spending grand mean from construction_spending.csv
    spend = pd.read_csv(SPENDING_PATH)
    spending_mean = spend["current.combined.total construction"].mean()

    # Step 4: Create Excel workbook
    wb = Workbook()
    ws_r = wb.active
    ws_r.title = "Result"
    ws_s = wb.create_sheet("Scaled_Impact")

    # Define fonts
    blue = Font(color="0000FF")
    bold = Font(bold=True)
    black = Font(color="000000")

    # Result sheet - Row 1: BDR
    ws_r["A1"].value = "BDR"
    ws_r["A1"].font = bold
    ws_r["B1"].value = float(bdr)
    ws_r["B1"].font = blue
    ws_r["B1"].number_format = "0.000000"

    # Result sheet - Row 2: Permits
    ws_r["A2"].value = "Permits_Total_GrandMean"
    ws_r["A2"].font = bold
    ws_r["B2"].value = float(permits_mean)
    ws_r["B2"].font = blue
    ws_r["B2"].number_format = "#,##0.00"

    # Result sheet - Row 3: Spending
    ws_r["A3"].value = "Spending_CurrentCombinedTotal_GrandMean"
    ws_r["A3"].font = bold
    ws_r["B3"].value = float(spending_mean)
    ws_r["B3"].font = blue
    ws_r["B3"].number_format = "$#,##0.00"

    # Scaled_Impact sheet - Row 1: BDR * Permits
    ws_s["A1"].value = "BDR * Permits_Total_GrandMean"
    ws_s["B1"].value = "=Result!B1*Result!B2"
    ws_s["B1"].font = black
    ws_s["B1"].number_format = "#,##0.00"

    # Scaled_Impact sheet - Row 2: BDR * Spending
    ws_s["A2"].value = "BDR * Spending_CurrentCombinedTotal_GrandMean"
    ws_s["B2"].value = "=Result!B1*Result!B3"
    ws_s["B2"].font = black
    ws_s["B2"].number_format = "$#,##0.00"

    wb.save(OUTPUT_PATH)
    print(f"Workbook saved to: {OUTPUT_PATH}")
    print(f"BDR: {bdr}")
    print(f"Permits_Total_GrandMean: {permits_mean}")
    print(f"Spending_CurrentCombinedTotal_GrandMean: {spending_mean}")

if __name__ == '__main__':
    main()
EOF

# Execute the script
python3 /root/solve_task.py
