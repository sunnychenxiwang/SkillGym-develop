#!/bin/bash
set -e
mkdir -p /root/output
# Create the solution Python script using heredoc
cat << 'EOF' > /root/solve_task.py
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill

# Paths
DATASET_PATH = "/root/Dataset_S9.csv"
SPENDING_PATH = "/root/construction_spending.csv"
PERMITS_PATH = "/root/construction.csv"
OUTPUT_PATH = "/root/output/growth_vs_construction_correlation.xlsx"

# Sector columns to analyze
SECTORS = [
    "annual.combined.residential",
    "annual.combined.commercial",
    "annual.combined.educational",
]

def main():
    # Ensure output directory exists
    import os
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    # Step 1: Compute OD_mean from Dataset_S9.csv
    # Exclude Strain == "Blank", group by Time_hours, take mean OD
    df_growth = pd.read_csv(DATASET_PATH)
    df_growth = df_growth[df_growth["Strain"] != "Blank"]
    od_mean = df_growth.groupby("Time_hours")["OD"].mean().reset_index(drop=True)

    # Step 2: Load construction_spending.csv and compute correlations
    df_spending = pd.read_csv(SPENDING_PATH)

    results = []
    for col in SECTORS:
        series = pd.to_numeric(df_spending[col], errors="coerce").dropna().reset_index(drop=True)
        od_vec = od_mean.copy()
        # Align by taking first N points where N = min(len(OD_mean), len(series))
        N = min(len(od_vec), len(series))
        od_aligned = od_vec.iloc[:N]
        s_aligned = series.iloc[:N]
        corr = od_aligned.corr(s_aligned)
        results.append((col, corr, od_aligned, s_aligned))

    # Step 3: Compute avg_total_permits from construction.csv
    df_permits = pd.read_csv(PERMITS_PATH)
    total_num = pd.to_numeric(df_permits["Total"], errors="coerce")
    avg_total_permits = total_num.mean()

    # Step 4: Determine best-match sector (highest correlation)
    best_idx = max(range(len(results)), key=lambda i: results[i][1])
    best_col, best_corr, best_od, best_series = results[best_idx]

    # Build Results DataFrame
    out_rows = []
    for i, (col, corr, _, _) in enumerate(results):
        out_rows.append({
            "sector_column": col,
            "corr_with_OD_mean": round(float(corr), 6),
            "avg_total_permits": round(float(avg_total_permits), 2),
            "best_match": (i == best_idx),
        })
    results_df = pd.DataFrame(out_rows)

    # Build Data_Used DataFrame with aligned vectors for best sector
    data_used_df = pd.DataFrame({
        "OD_mean": best_od.values,
        "best_sector_series": best_series.values
    })

    # Step 5: Write Excel with two sheets
    with pd.ExcelWriter(OUTPUT_PATH, engine="openpyxl") as writer:
        results_df.to_excel(writer, sheet_name="Results", index=False)
        data_used_df.to_excel(writer, sheet_name="Data_Used", index=False)

    # Step 6: Apply professional formatting with openpyxl
    wb = load_workbook(OUTPUT_PATH)

    header_font = Font(bold=True)
    header_fill = PatternFill("solid", fgColor="D9E1F2")

    # Format Results sheet
    ws = wb["Results"]
    for cell in ws[1]:
        cell.font = header_font
        cell.fill = header_fill

    # Get column indices for number formatting
    headers = [c.value for c in ws[1]]
    corr_col = headers.index("corr_with_OD_mean") + 1
    perm_col = headers.index("avg_total_permits") + 1

    # Apply number formats to data rows
    for r in range(2, ws.max_row + 1):
        ws.cell(r, corr_col).number_format = "0.000000"
        ws.cell(r, perm_col).number_format = "0.00"

    # Freeze top row and enable autofilter
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions

    # Format Data_Used sheet
    ws2 = wb["Data_Used"]
    for cell in ws2[1]:
        cell.font = header_font
        cell.fill = header_fill
    ws2.freeze_panes = "A2"
    ws2.auto_filter.ref = ws2.dimensions

    wb.save(OUTPUT_PATH)

    print(f"Excel file created: {OUTPUT_PATH}")
    print(f"Best sector: {best_col} with correlation {best_corr:.6f}")
    print(f"Avg total permits: {avg_total_permits:.2f}")

if __name__ == '__main__':
    main()
EOF

# Execute the script
python3 /root/solve_task.py
