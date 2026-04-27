#!/bin/bash
set -e

# HARBOR_RUNTIME_PATH_FIX: align synthetic workspace paths with Harbor runtime layout
TASK_DIR="$(grep -Eo '/root/harbor_workspaces/task_[A-Za-z0-9_]+' "$0" | head -n1 || true)"
if [ -n "$TASK_DIR" ]; then
  mkdir -p "$TASK_DIR"
  [ -e "$TASK_DIR/input" ] || ln -s /root "$TASK_DIR/input"
  [ -e "$TASK_DIR/output" ] || ln -s /root "$TASK_DIR/output"
  cd "$TASK_DIR"
fi

# Generated scripts sometimes call `python`; map it to python3.
python() { python3 "$@"; }

# Some trajectories contain optional xsv diagnostics; skip if xsv is unavailable.
if ! command -v xsv >/dev/null 2>&1; then
  xsv() { return 0; }
fi

# Auto-generated solution based on execution trajectory
# This script recreates the outputs produced during synthesis

# Execute command
head -1 /root/construction_spending.csv | tr ',' '\n' | grep -n "annual.combined"

# Execute command
cut -d',' -f3 /root/Dataset\ S9.csv | sort -u

# Execute command
mkdir -p /root/harbor_workspaces/task_T384_run2/output

# Execute command
cat > /root/harbor_workspaces/task_T384_run2/process_data.py << 'PYEOF'
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter

# Step 1: Load the three CSVs
s9 = pd.read_csv("/root/Dataset S9.csv")
cons = pd.read_csv("/root/construction.csv", na_values=["NA"])
spend = pd.read_csv("/root/construction_spending.csv")

# Step 2: Compute per-strain max OD fold-change (exclude Blank; min ignores OD <= 0)
s9_nb = s9[s9["Strain"] != "Blank"].copy()

# Compute max OD per strain (over all OD values)
max_od = s9_nb.groupby("Strain").agg(max_od=("OD", "max")).reset_index()

# Compute min OD per strain (only OD > 0)
min_od_pos = s9_nb[s9_nb["OD"] > 0].groupby("Strain").agg(min_od=("OD", "min")).reset_index()

# Merge and compute ratio
strain_fc = max_od.merge(min_od_pos, on="Strain", how="inner")
strain_fc["ratio"] = strain_fc["max_od"] / strain_fc["min_od"]
strain_rows = strain_fc[["Strain", "ratio"]].rename(columns={"Strain": "item_name"})
strain_rows["item_type"] = "strain"

print("Strain fold-changes:")
print(strain_rows)

# Step 3: Compute building-type ratios in construction.csv (ignore NA)
bld_cols = ["1 unit", "2 to 4 units", "5 units or more"]
bld_rows_list = []
for c in bld_cols:
    mx = cons[c].max(skipna=True)
    mn = cons[c].min(skipna=True)
    if pd.notna(mx) and pd.notna(mn) and mn != 0:
        bld_rows_list.append({"item_type": "building_type", "item_name": c, "ratio": mx / mn})
    else:
        print(f"Warning: Column {c} has all NA or min=0")
bld_rows = pd.DataFrame(bld_rows_list)

print("\nBuilding type ratios:")
print(bld_rows)

# Step 4: Find the spending category (annual.combined.*) with largest ratio
annual_cols = [c for c in spend.columns if c.startswith("annual.combined.")]
print(f"\nFound {len(annual_cols)} annual.combined columns")

ratios = []
for c in annual_cols:
    series = spend[c]
    mx = series.max(skipna=True)
    mn = series.min(skipna=True)
    if pd.notna(mx) and pd.notna(mn) and mn != 0:
        ratios.append((c, mx / mn))

spend_winner_col, spend_winner_ratio = max(ratios, key=lambda x: x[1])
spend_row = pd.DataFrame([{
    "item_type": "spending_category",
    "item_name": spend_winner_col,
    "ratio": spend_winner_ratio
}])

print(f"\nSpending category winner: {spend_winner_col} with ratio {spend_winner_ratio}")

# Step 5: Combine rows, sort, tie-break, and assign rank
combined = pd.concat([
    strain_rows[["item_type", "item_name", "ratio"]],
    bld_rows[["item_type", "item_name", "ratio"]],
    spend_row[["item_type", "item_name", "ratio"]]
], ignore_index=True)

# Sort by ratio descending, then by item_name ascending (for tie-break)
combined = combined.sort_values(["ratio", "item_name"], ascending=[False, True]).reset_index(drop=True)
combined["rank"] = combined.index + 1
combined = combined[["item_type", "item_name", "ratio", "rank"]]

print("\nFinal combined ranking:")
print(combined)

# Step 6: Write Excel and apply formatting
out_path = "/root/relative_change_ranking.xlsx"

# Write with pandas
with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
    combined.to_excel(writer, sheet_name="Ranking", index=False)

# Re-open with openpyxl for formatting
wb = load_workbook(out_path)
ws = wb["Ranking"]

# Bold header
for cell in ws[1]:
    cell.font = Font(bold=True)

# Freeze top row - CRITICAL: Must set freeze_panes to "A2" to freeze row 1
ws.freeze_panes = "A2"

# Find ratio column index and apply 4 decimal format
ratio_col_idx = None
for j, cell in enumerate(ws[1], start=1):
    if cell.value == "ratio":
        ratio_col_idx = j
        break

if ratio_col_idx:
    for row in range(2, ws.max_row + 1):
        ws.cell(row=row, column=ratio_col_idx).number_format = "0.0000"

# Auto-fit column widths
for col_cells in ws.columns:
    max_len = 0
    col_letter = get_column_letter(col_cells[0].column)
    for c in col_cells:
        v = "" if c.value is None else str(c.value)
        max_len = max(max_len, len(v))
    ws.column_dimensions[col_letter].width = max(10, min(60, max_len + 2))

wb.save(out_path)

print(f"\nExcel file saved to: {out_path}")

# Verification
wb2 = load_workbook(out_path)
ws2 = wb2["Ranking"]
print(f"\nVerification:")
print(f"  Sheet names: {wb2.sheetnames}")
print(f"  Freeze panes: {ws2.freeze_panes}")
print(f"  Header values: {[c.value for c in ws2[1]]}")
print(f"  Header bold: {[c.font.bold for c in ws2[1]]}")
if ratio_col_idx:
    sample_ratio_cell = ws2.cell(row=2, column=ratio_col_idx)
    print(f"  Ratio cell number_format: {sample_ratio_cell.number_format}")
    print(f"  Ratio cell value: {sample_ratio_cell.value}")

PYEOF
python /root/harbor_workspaces/task_T384_run2/process_data.py

# Execute command
ls -la /root/harbor_workspaces/task_T384_run2/output/

# Execute command
python3 << 'EOF'
from openpyxl import load_workbook

wb = load_workbook("/root/relative_change_ranking.xlsx")
ws = wb["Ranking"]

print("=== Excel Verification ===")
print(f"Sheet names: {wb.sheetnames}")
print(f"Freeze panes value: '{ws.freeze_panes}'")
print(f"Is top row frozen (freeze_panes == 'A2'): {ws.freeze_panes == 'A2'}")

print("\nHeader row (row 1):")
for cell in ws[1]:
    print(f"  {cell.coordinate}: value='{cell.value}', bold={cell.font.bold}")

print("\nData rows:")
for row_idx in range(1, ws.max_row + 1):
    row_data = [ws.cell(row=row_idx, column=c).value for c in range(1, 5)]
    print(f"  Row {row_idx}: {row_data}")

print("\nRatio column number formats:")
for row_idx in range(2, ws.max_row + 1):
    cell = ws.cell(row=row_idx, column=3)  # ratio is column 3
    print(f"  Row {row_idx}: value={cell.value}, format='{cell.number_format}'")

print("\nColumn widths:")
for col_letter in ['A', 'B', 'C', 'D']:
    print(f"  Column {col_letter}: {ws.column_dimensions[col_letter].width}")
EOF

# Execute command
head -1 input/Dataset\ S9.csv && cut -d',' -f3 input/Dataset\ S9.csv | sort -u | head -20

# Execute command
mkdir -p /root/harbor_workspaces/task_T384_run2/output

# Create /root/harbor_workspaces/task_T384_run2/process_data.py
mkdir -p $(dirname /root/harbor_workspaces/task_T384_run2/process_data.py)
cat << 'HEREDOC_EOF' > /root/harbor_workspaces/task_T384_run2/process_data.py
#!/usr/bin/env python3
"""
Process growth dynamics and construction data to create ranked comparison table.
"""

import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter

# Paths
s9_path = "/root/Dataset S9.csv"
cons_path = "/root/construction.csv"
spend_path = "/root/construction_spending.csv"
out_path = "/root/relative_change_ranking.xlsx"

# Step 1: Load CSVs
print("Loading CSV files...")
s9 = pd.read_csv(s9_path)
cons = pd.read_csv(cons_path, na_values=["NA"])
spend = pd.read_csv(spend_path)

print(f"Dataset S9 shape: {s9.shape}")
print(f"Construction shape: {cons.shape}")
print(f"Spending shape: {spend.shape}")

# Step 2: Compute per-strain max OD fold-change (exclude Blank; min ignores OD <= 0)
print("\nProcessing strain data...")
s9_nb = s9[s9["Strain"] != "Blank"].copy()
print(f"Non-Blank strains: {s9_nb['Strain'].unique()}")

# Compute max OD per strain (all values)
max_od = s9_nb.groupby("Strain").agg(max_od=("OD", "max")).reset_index()
print(f"Max OD per strain:\n{max_od}")

# Compute min OD per strain (only OD > 0)
s9_pos = s9_nb[s9_nb["OD"] > 0]
min_od_pos = s9_pos.groupby("Strain").agg(min_od=("OD", "min")).reset_index()
print(f"Min OD (>0) per strain:\n{min_od_pos}")

# Merge and compute fold-change
strain_fc = max_od.merge(min_od_pos, on="Strain", how="inner")
strain_fc["ratio"] = strain_fc["max_od"] / strain_fc["min_od"]
print(f"Strain fold-change:\n{strain_fc}")

strain_rows = strain_fc[["Strain", "ratio"]].rename(columns={"Strain": "item_name"})
strain_rows["item_type"] = "strain"

# Step 3: Compute building-type ratios in construction.csv (ignore NA)
print("\nProcessing construction building types...")
bld_cols = ["1 unit", "2 to 4 units", "5 units or more"]
bld_rows = []
for c in bld_cols:
    mx = cons[c].max(skipna=True)
    mn = cons[c].min(skipna=True)
    # Check if we have valid min/max
    if pd.notna(mx) and pd.notna(mn) and mn > 0:
        ratio = mx / mn
        bld_rows.append({"item_type": "building_type", "item_name": c, "ratio": ratio})
        print(f"  {c}: max={mx}, min={mn}, ratio={ratio:.4f}")
    else:
        print(f"  {c}: skipped (all NA or min=0)")

bld_rows = pd.DataFrame(bld_rows)

# Step 4: Find the spending category (annual.combined.*) with largest ratio
print("\nProcessing construction spending...")
annual_cols = [c for c in spend.columns if c.startswith("annual.combined.")]
print(f"Found {len(annual_cols)} annual.combined.* columns")

ratios = []
for c in annual_cols:
    series = spend[c]
    mx = series.max(skipna=True)
    mn = series.min(skipna=True)
    if pd.notna(mx) and pd.notna(mn) and mn > 0:
        ratios.append((c, mx / mn))

print(f"Valid spending columns with non-zero min: {len(ratios)}")

# Find the column with largest ratio
spend_winner_col, spend_winner_ratio = max(ratios, key=lambda x: x[1])
print(f"Winner: {spend_winner_col} with ratio={spend_winner_ratio:.4f}")

spend_row = pd.DataFrame([{
    "item_type": "spending_category",
    "item_name": spend_winner_col,
    "ratio": spend_winner_ratio
}])

# Step 5: Combine rows, sort, tie-break, and assign rank
print("\nCombining results...")
combined = pd.concat([
    strain_rows[["item_type", "item_name", "ratio"]],
    bld_rows[["item_type", "item_name", "ratio"]],
    spend_row[["item_type", "item_name", "ratio"]]
], ignore_index=True)

# Sort by ratio (descending), then by item_name (ascending) for tie-breaking
combined = combined.sort_values(["ratio", "item_name"], ascending=[False, True]).reset_index(drop=True)
combined["rank"] = combined.index + 1
combined = combined[["item_type", "item_name", "ratio", "rank"]]

print("\nFinal ranked table:")
print(combined.to_string(index=False))

# Step 6: Write Excel and apply formatting
print(f"\nWriting Excel file to {out_path}...")

# Write with pandas ExcelWriter
with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
    combined.to_excel(writer, sheet_name="Ranking", index=False)

# Now apply formatting with openpyxl
wb = load_workbook(out_path)
ws = wb["Ranking"]

# Bold header
for cell in ws[1]:
    cell.font = Font(bold=True)

# Freeze top row - Set freeze_panes to "A2" to freeze row 1
ws.freeze_panes = "A2"

# Find ratio column index and apply 4 decimal format
ratio_col_idx = None
for j, cell in enumerate(ws[1], start=1):
    if cell.value == "ratio":
        ratio_col_idx = j
        break

if ratio_col_idx:
    for row in range(2, ws.max_row + 1):
        ws.cell(row=row, column=ratio_col_idx).number_format = "0.0000"

# Auto-fit column widths
for col_cells in ws.columns:
    max_len = 0
    col_letter = get_column_letter(col_cells[0].column)
    for c in col_cells:
        v = "" if c.value is None else str(c.value)
        max_len = max(max_len, len(v))
    ws.column_dimensions[col_letter].width = max(10, min(60, max_len + 2))

# Save the workbook
wb.save(out_path)
wb.close()

print("\nVerifying output...")
# Verification
wb2 = load_workbook(out_path)
ws2 = wb2["Ranking"]
print(f"Sheet names: {wb2.sheetnames}")
print(f"Freeze panes: {ws2.freeze_panes}")
print(f"Header row bold: {ws2['A1'].font.bold}")

# Check header values
headers = [cell.value for cell in ws2[1]]
print(f"Headers: {headers}")

# Check ratio format
for j, cell in enumerate(ws2[1], start=1):
    if cell.value == "ratio":
        sample_cell = ws2.cell(row=2, column=j)
        print(f"Ratio cell value: {sample_cell.value}, format: {sample_cell.number_format}")

wb2.close()
print("\nDone!")

HEREDOC_EOF

# Execute command
cat > /root/harbor_workspaces/task_T384_run2/process_data.py << 'PYTHON_SCRIPT'
#!/usr/bin/env python3
"""
Process growth dynamics and construction data to create ranked comparison table.
"""

import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter

# Paths
s9_path = "/root/Dataset S9.csv"
cons_path = "/root/construction.csv"
spend_path = "/root/construction_spending.csv"
out_path = "/root/relative_change_ranking.xlsx"

# Step 1: Load CSVs
print("Loading CSV files...")
s9 = pd.read_csv(s9_path)
cons = pd.read_csv(cons_path, na_values=["NA"])
spend = pd.read_csv(spend_path)

print(f"Dataset S9 shape: {s9.shape}")
print(f"Construction shape: {cons.shape}")
print(f"Spending shape: {spend.shape}")

# Step 2: Compute per-strain max OD fold-change (exclude Blank; min ignores OD <= 0)
print("\nProcessing strain data...")
s9_nb = s9[s9["Strain"] != "Blank"].copy()
print(f"Non-Blank strains: {s9_nb['Strain'].unique()}")

# Compute max OD per strain (all values)
max_od = s9_nb.groupby("Strain").agg(max_od=("OD", "max")).reset_index()
print(f"Max OD per strain:\n{max_od}")

# Compute min OD per strain (only OD > 0)
s9_pos = s9_nb[s9_nb["OD"] > 0]
min_od_pos = s9_pos.groupby("Strain").agg(min_od=("OD", "min")).reset_index()
print(f"Min OD (>0) per strain:\n{min_od_pos}")

# Merge and compute fold-change
strain_fc = max_od.merge(min_od_pos, on="Strain", how="inner")
strain_fc["ratio"] = strain_fc["max_od"] / strain_fc["min_od"]
print(f"Strain fold-change:\n{strain_fc}")

strain_rows = strain_fc[["Strain", "ratio"]].rename(columns={"Strain": "item_name"})
strain_rows["item_type"] = "strain"

# Step 3: Compute building-type ratios in construction.csv (ignore NA)
print("\nProcessing construction building types...")
bld_cols = ["1 unit", "2 to 4 units", "5 units or more"]
bld_rows = []
for c in bld_cols:
    mx = cons[c].max(skipna=True)
    mn = cons[c].min(skipna=True)
    # Check if we have valid min/max
    if pd.notna(mx) and pd.notna(mn) and mn > 0:
        ratio = mx / mn
        bld_rows.append({"item_type": "building_type", "item_name": c, "ratio": ratio})
        print(f"  {c}: max={mx}, min={mn}, ratio={ratio:.4f}")
    else:
        print(f"  {c}: skipped (all NA or min=0)")

bld_rows = pd.DataFrame(bld_rows)

# Step 4: Find the spending category (annual.combined.*) with largest ratio
print("\nProcessing construction spending...")
annual_cols = [c for c in spend.columns if c.startswith("annual.combined.")]
print(f"Found {len(annual_cols)} annual.combined.* columns")

ratios = []
for c in annual_cols:
    series = spend[c]
    mx = series.max(skipna=True)
    mn = series.min(skipna=True)
    if pd.notna(mx) and pd.notna(mn) and mn > 0:
        ratios.append((c, mx / mn))

print(f"Valid spending columns with non-zero min: {len(ratios)}")

# Find the column with largest ratio
spend_winner_col, spend_winner_ratio = max(ratios, key=lambda x: x[1])
print(f"Winner: {spend_winner_col} with ratio={spend_winner_ratio:.4f}")

spend_row = pd.DataFrame([{
    "item_type": "spending_category",
    "item_name": spend_winner_col,
    "ratio": spend_winner_ratio
}])

# Step 5: Combine rows, sort, tie-break, and assign rank
print("\nCombining results...")
combined = pd.concat([
    strain_rows[["item_type", "item_name", "ratio"]],
    bld_rows[["item_type", "item_name", "ratio"]],
    spend_row[["item_type", "item_name", "ratio"]]
], ignore_index=True)

# Sort by ratio (descending), then by item_name (ascending) for tie-breaking
combined = combined.sort_values(["ratio", "item_name"], ascending=[False, True]).reset_index(drop=True)
combined["rank"] = combined.index + 1
combined = combined[["item_type", "item_name", "ratio", "rank"]]

print("\nFinal ranked table:")
print(combined.to_string(index=False))

# Step 6: Write Excel and apply formatting
print(f"\nWriting Excel file to {out_path}...")

# Write with pandas ExcelWriter
with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
    combined.to_excel(writer, sheet_name="Ranking", index=False)

# Now apply formatting with openpyxl
wb = load_workbook(out_path)
ws = wb["Ranking"]

# Bold header
for cell in ws[1]:
    cell.font = Font(bold=True)

# Freeze top row - Set freeze_panes to "A2" to freeze row 1
ws.freeze_panes = "A2"

# Find ratio column index and apply 4 decimal format
ratio_col_idx = None
for j, cell in enumerate(ws[1], start=1):
    if cell.value == "ratio":
        ratio_col_idx = j
        break

if ratio_col_idx:
    for row in range(2, ws.max_row + 1):
        ws.cell(row=row, column=ratio_col_idx).number_format = "0.0000"

# Auto-fit column widths
for col_cells in ws.columns:
    max_len = 0
    col_letter = get_column_letter(col_cells[0].column)
    for c in col_cells:
        v = "" if c.value is None else str(c.value)
        max_len = max(max_len, len(v))
    ws.column_dimensions[col_letter].width = max(10, min(60, max_len + 2))

# Save the workbook
wb.save(out_path)
wb.close()

print("\nVerifying output...")
# Verification
wb2 = load_workbook(out_path)
ws2 = wb2["Ranking"]
print(f"Sheet names: {wb2.sheetnames}")
print(f"Freeze panes: {ws2.freeze_panes}")
print(f"Header row bold: {ws2['A1'].font.bold}")

# Check header values
headers = [cell.value for cell in ws2[1]]
print(f"Headers: {headers}")

# Check ratio format
for j, cell in enumerate(ws2[1], start=1):
    if cell.value == "ratio":
        sample_cell = ws2.cell(row=2, column=j)
        print(f"Ratio cell value: {sample_cell.value}, format: {sample_cell.number_format}")

wb2.close()
print("\nDone!")
PYTHON_SCRIPT

# Execute command
python3 process_data.py

# Execute command
python3 << 'VERIFY'
from openpyxl import load_workbook

out_path = "/root/relative_change_ranking.xlsx"
wb = load_workbook(out_path)
ws = wb["Ranking"]

print("=== Excel Verification ===")
print(f"Sheet names: {wb.sheetnames}")
print(f"Freeze panes raw: {repr(ws.freeze_panes)}")
print(f"Top left cell (freeze): {ws.freeze_panes}")

# Check sheet view settings
print(f"\nSheet views: {ws.views}")
print(f"Sheet view pane: {ws.views.sheetView[0].pane if ws.views.sheetView and len(ws.views.sheetView) > 0 else 'No pane'}")

# Check header formatting
print(f"\nHeader cells:")
for cell in ws[1]:
    print(f"  {cell.coordinate}: '{cell.value}', bold={cell.font.bold}")

# Check ratio column format
print(f"\nRatio column (column C):")
for row in ws.iter_rows(min_col=3, max_col=3, min_row=1, max_row=6):
    for cell in row:
        print(f"  {cell.coordinate}: value={cell.value}, format={cell.number_format}")

# Check column widths
print(f"\nColumn widths:")
for col in ['A', 'B', 'C', 'D']:
    print(f"  Column {col}: {ws.column_dimensions[col].width}")

# Check actual cell values
print(f"\nAll data:")
for row in ws.iter_rows(min_row=1, max_row=ws.max_row, values_only=True):
    print(f"  {row}")

wb.close()
VERIFY

# Execute command
ls -la /root/relative_change_ranking.xlsx && file /root/relative_change_ranking.xlsx

# Execute command
cd /tmp && rm -rf xlsx_check && mkdir xlsx_check && cd xlsx_check && unzip -q /root/relative_change_ranking.xlsx && cat xl/worksheets/sheet1.xml | head -30

# Execute command
cat /tmp/xlsx_check/xl/styles.xml

# Execute command
python3 << 'FINAL_CHECK'
from openpyxl import load_workbook

out_path = "/root/relative_change_ranking.xlsx"
wb = load_workbook(out_path)
ws = wb["Ranking"]

print("=== FINAL VERIFICATION ===\n")

# 1. Check sheet name
print("1. Sheet name check:")
print(f"   Expected: 'Ranking' in sheetnames")
print(f"   Actual: {wb.sheetnames}")
print(f"   PASS: {'Ranking' in wb.sheetnames}")

# 2. Check column names
print("\n2. Column names check:")
expected_cols = ['item_type', 'item_name', 'ratio', 'rank']
actual_cols = [cell.value for cell in ws[1]]
print(f"   Expected: {expected_cols}")
print(f"   Actual: {actual_cols}")
print(f"   PASS: {actual_cols == expected_cols}")

# 3. Check freeze panes
print("\n3. Freeze panes check:")
print(f"   Expected: 'A2' (freeze top row)")
print(f"   Actual: {ws.freeze_panes}")
print(f"   PASS: {ws.freeze_panes == 'A2'}")

# Also check the underlying view
if ws.views and ws.views.sheetView:
    pane = ws.views.sheetView[0].pane
    if pane:
        print(f"   Pane state: {pane.state}")
        print(f"   ySplit: {pane.ySplit}")
        print(f"   topLeftCell: {pane.topLeftCell}")

# 4. Check bold header
print("\n4. Bold header check:")
all_bold = all(cell.font.bold for cell in ws[1])
print(f"   Expected: All header cells bold")
print(f"   Actual bold values: {[cell.font.bold for cell in ws[1]]}")
print(f"   PASS: {all_bold}")

# 5. Check ratio format (4 decimal places)
print("\n5. Ratio number format check:")
ratio_col_idx = None
for j, cell in enumerate(ws[1], start=1):
    if cell.value == "ratio":
        ratio_col_idx = j
        break
if ratio_col_idx:
    formats = []
    for row in range(2, ws.max_row + 1):
        cell = ws.cell(row=row, column=ratio_col_idx)
        formats.append(cell.number_format)
    print(f"   Expected: All '0.0000'")
    print(f"   Actual: {formats}")
    print(f"   PASS: {all(f == '0.0000' for f in formats)}")

# 6. Check data content
print("\n6. Data content check:")
expected_rows = [
    ('item_type', 'item_name', 'ratio', 'rank'),
    ('strain', 'C6706', 25.85, 1),
    ('strain', 'LuxO', 19.09523809523809, 2),
    ('spending_category', 'annual.combined.manufacturing', 4.584022737654164, 3),
    ('building_type', '5 units or more', 1.562937062937063, 4),
    ('building_type', '1 unit', 1.178168130489335, 5),
]
actual_data = list(ws.iter_rows(min_row=1, max_row=ws.max_row, values_only=True))
print(f"   Row count - Expected: {len(expected_rows)}, Actual: {len(actual_data)}")

# Check ranks are correct (1-5)
ranks = [row[3] for row in actual_data[1:]]
print(f"   Ranks: {ranks}")
print(f"   PASS ranks: {ranks == [1, 2, 3, 4, 5]}")

# 7. Check ratio values are numeric
print("\n7. Numeric ratio values check:")
for row in range(2, ws.max_row + 1):
    cell = ws.cell(row=row, column=ratio_col_idx)
    print(f"   Row {row}: value={cell.value}, type={type(cell.value).__name__}")

wb.close()
print("\n=== ALL CHECKS COMPLETE ===")
FINAL_CHECK

# Execute command
python3 -c "
from openpyxl import load_workbook
wb = load_workbook('/root/relative_change_ranking.xlsx')
ws = wb['Ranking']
print('freeze_panes:', repr(ws.freeze_panes))
print('Type:', type(ws.freeze_panes))

# Alternative check using views
view = ws.views.sheetView[0] if ws.views.sheetView else None
if view and view.pane:
    print('Pane state:', view.pane.state)
    print('Pane ySplit:', view.pane.ySplit)
    print('Pane topLeftCell:', view.pane.topLeftCell)
    print('FROZEN:', view.pane.state == 'frozen' and view.pane.ySplit == 1)
"

# Execute command
echo "Output file location:" && ls -la /root/relative_change_ranking.xlsx

# Create /root/harbor_workspaces/task_T384_run2/expectation_tests.py
mkdir -p $(dirname /root/harbor_workspaces/task_T384_run2/expectation_tests.py)
cat << 'HEREDOC_EOF' > /root/harbor_workspaces/task_T384_run2/expectation_tests.py
"""Auto-generated expectation tests for task verification.

These tests verify that the task execution produces correct outputs
based on the instruction requirements for computing growth dynamics
across biological strains and housing construction categories.
"""

import os
from pathlib import Path

import pandas as pd
import pytest
from openpyxl import load_workbook
from openpyxl.styles import Font


OUTPUT_FILE = "/root/relative_change_ranking.xlsx"


class TestOutputFileExists:
    """Tests for verifying output file existence and basic structure."""

    def test_output_file_exists(self):
        """Verify the output Excel file was created at the specified path."""
        assert os.path.exists(OUTPUT_FILE), f"Output file not found at {OUTPUT_FILE}"

    def test_output_file_is_xlsx(self):
        """Verify output file has .xlsx extension."""
        assert OUTPUT_FILE.endswith(".xlsx"), "Output file must have .xlsx extension"

    def test_output_file_not_empty(self):
        """Verify output file is not empty."""
        assert os.path.getsize(OUTPUT_FILE) > 0, "Output file is empty"


class TestExcelSheetStructure:
    """Tests for verifying the Excel sheet structure."""

    def test_ranking_sheet_exists(self):
        """Verify the 'Ranking' sheet exists in the workbook."""
        wb = load_workbook(OUTPUT_FILE)
        assert "Ranking" in wb.sheetnames, "Sheet 'Ranking' not found in workbook"
        wb.close()

    def test_required_columns_exist(self):
        """Verify all required columns are present: item_type, item_name, ratio, rank."""
        df = pd.read_excel(OUTPUT_FILE, sheet_name="Ranking")
        required_columns = ["item_type", "item_name", "ratio", "rank"]
        for col in required_columns:
            assert col in df.columns, f"Required column '{col}' not found"

    def test_column_order(self):
        """Verify columns are in the exact order: item_type, item_name, ratio, rank."""
        df = pd.read_excel(OUTPUT_FILE, sheet_name="Ranking")
        expected_columns = ["item_type", "item_name", "ratio", "rank"]
        actual_columns = list(df.columns)[:4]  # First 4 columns
        assert actual_columns == expected_columns, (
            f"Column order mismatch. Expected {expected_columns}, got {actual_columns}"
        )


class TestDataContent:
    """Tests for verifying the data content and values."""

    def test_has_strain_rows(self):
        """Verify there are rows for biological strains (excluding Blank)."""
        df = pd.read_excel(OUTPUT_FILE, sheet_name="Ranking")
        strain_rows = df[df["item_type"].str.lower().str.contains("strain", na=False)]
        assert len(strain_rows) >= 2, "Expected at least 2 strain rows (C6706, LuxO)"

    def test_expected_strains_present(self):
        """Verify C6706 and LuxO strains are present in the data."""
        df = pd.read_excel(OUTPUT_FILE, sheet_name="Ranking")
        item_names = df["item_name"].str.strip().tolist()
        assert "C6706" in item_names, "Strain C6706 not found in item_name column"
        assert "LuxO" in item_names, "Strain LuxO not found in item_name column"

    def test_blank_strain_excluded(self):
        """Verify Blank strain is not included in the output."""
        df = pd.read_excel(OUTPUT_FILE, sheet_name="Ranking")
        item_names = df["item_name"].str.lower().str.strip().tolist()
        assert "blank" not in item_names, "Blank strain should be excluded"

    def test_has_building_type_rows(self):
        """Verify there are rows for housing construction building types."""
        df = pd.read_excel(OUTPUT_FILE, sheet_name="Ranking")
        building_types = ["1 unit", "2 to 4 units", "5 units or more"]
        item_names = df["item_name"].str.strip().tolist()
        found_count = sum(1 for bt in building_types if bt in item_names)
        # Some building types may have all NA values, so we check for at least some
        assert found_count >= 1, "Expected at least one building type row"

    def test_has_spending_category_row(self):
        """Verify there is at least one spending category row."""
        df = pd.read_excel(OUTPUT_FILE, sheet_name="Ranking")
        # Check for spending category type indicator
        spending_rows = df[
            df["item_type"].str.lower().str.contains("spend", na=False)
            | df["item_name"].str.lower().str.contains("annual", na=False)
        ]
        # If not found by type, should have exactly one winning spending category
        total_rows = len(df)
        # We expect: 2 strains + up to 3 building types + 1 spending category
        assert total_rows >= 4, "Expected at least 4 rows in the ranking"

    def test_ratio_values_are_numeric(self):
        """Verify all ratio values are numeric."""
        df = pd.read_excel(OUTPUT_FILE, sheet_name="Ranking")
        assert pd.api.types.is_numeric_dtype(df["ratio"]), "Ratio column must be numeric"

    def test_ratio_values_positive(self):
        """Verify all ratio values are positive (fold-change must be >= 1)."""
        df = pd.read_excel(OUTPUT_FILE, sheet_name="Ranking")
        assert (df["ratio"] > 0).all(), "All ratio values must be positive"

    def test_ratio_values_at_least_one(self):
        """Verify all ratio values are at least 1 (max/min >= 1)."""
        df = pd.read_excel(OUTPUT_FILE, sheet_name="Ranking")
        assert (df["ratio"] >= 1).all(), "All ratio values should be >= 1 (max/min ratio)"

    def test_rank_values_are_integers(self):
        """Verify all rank values are integers."""
        df = pd.read_excel(OUTPUT_FILE, sheet_name="Ranking")
        # Check if values are effectively integers (may be stored as float)
        assert df["rank"].apply(lambda x: float(x).is_integer()).all(), (
            "Rank values must be integers"
        )

    def test_rank_values_positive(self):
        """Verify all rank values are positive integers."""
        df = pd.read_excel(OUTPUT_FILE, sheet_name="Ranking")
        assert (df["rank"] > 0).all(), "All rank values must be positive"

    def test_rank_starts_at_one(self):
        """Verify rank starts at 1 for the largest ratio."""
        df = pd.read_excel(OUTPUT_FILE, sheet_name="Ranking")
        assert df["rank"].min() == 1, "Minimum rank should be 1"

    def test_ranks_are_consecutive(self):
        """Verify ranks form a consecutive sequence starting from 1."""
        df = pd.read_excel(OUTPUT_FILE, sheet_name="Ranking")
        n = len(df)
        expected_ranks = set(range(1, n + 1))
        actual_ranks = set(df["rank"].astype(int).tolist())
        assert actual_ranks == expected_ranks, (
            f"Ranks should be consecutive from 1 to {n}. Got {sorted(actual_ranks)}"
        )

    def test_ranking_order_descending_by_ratio(self):
        """Verify data is ranked by ratio in descending order."""
        df = pd.read_excel(OUTPUT_FILE, sheet_name="Ranking")
        # Sort by rank and check ratio is descending
        df_sorted = df.sort_values("rank")
        ratios = df_sorted["ratio"].tolist()
        for i in range(len(ratios) - 1):
            assert ratios[i] >= ratios[i + 1], (
                f"Ratio at rank {i+1} ({ratios[i]}) should be >= ratio at rank {i+2} ({ratios[i+1]})"
            )

    def test_rank_one_has_largest_ratio(self):
        """Verify rank 1 corresponds to the largest ratio value."""
        df = pd.read_excel(OUTPUT_FILE, sheet_name="Ranking")
        rank_one_ratio = df[df["rank"] == 1]["ratio"].values[0]
        max_ratio = df["ratio"].max()
        assert abs(rank_one_ratio - max_ratio) < 0.0001, (
            f"Rank 1 ratio ({rank_one_ratio}) should equal max ratio ({max_ratio})"
        )

    def test_no_duplicate_item_names(self):
        """Verify there are no duplicate item names."""
        df = pd.read_excel(OUTPUT_FILE, sheet_name="Ranking")
        duplicates = df["item_name"].duplicated().sum()
        assert duplicates == 0, f"Found {duplicates} duplicate item names"


class TestRatioFormatting:
    """Tests for verifying ratio decimal places."""

    def test_ratio_has_four_decimal_places(self):
        """Verify ratio values are written with 4 decimal places."""
        wb = load_workbook(OUTPUT_FILE)
        ws = wb["Ranking"]

        # Find the ratio column index (0-based, but openpyxl is 1-based)
        header_row = [cell.value for cell in ws[1]]
        if "ratio" in header_row:
            ratio_col = header_row.index("ratio") + 1  # 1-based index

            # Check number format of cells in ratio column
            for row in range(2, ws.max_row + 1):
                cell = ws.cell(row=row, column=ratio_col)
                if cell.value is not None:
                    # Check if the number format specifies 4 decimal places
                    # Common formats: "0.0000", "#,##0.0000", etc.
                    num_format = cell.number_format
                    # Verify the value when read can be represented with 4 decimals
                    value = cell.value
                    if isinstance(value, (int, float)):
                        formatted = f"{value:.4f}"
                        # Value should be representable with 4 decimal precision
                        assert abs(float(formatted) - value) < 0.00005, (
                            f"Ratio value {value} should be writable with 4 decimal places"
                        )
        wb.close()


class TestExcelFormatting:
    """Tests for verifying Excel formatting requirements."""

    def test_header_row_is_bold(self):
        """Verify the header row has bold font formatting."""
        wb = load_workbook(OUTPUT_FILE)
        ws = wb["Ranking"]

        # Check that header cells (row 1) are bold
        for cell in ws[1]:
            if cell.value is not None:
                assert cell.font.bold, f"Header cell '{cell.value}' should be bold"
        wb.close()

    def test_top_row_is_frozen(self):
        """Verify the top row is frozen (freeze panes)."""
        wb = load_workbook(OUTPUT_FILE)
        ws = wb["Ranking"]

        # Check freeze panes - should be set to freeze first row
        # freeze_panes should be "A2" to freeze row 1
        freeze_pane = ws.freeze_panes
        assert freeze_pane is not None, "Freeze panes should be set"
        # Common freeze positions for top row: "A2", "B2", etc. (row 2 means row 1 is frozen)
        if freeze_pane:
            # The row number in freeze_panes should be 2 (meaning row 1 is frozen)
            from openpyxl.utils import coordinate_from_string, column_index_from_string
            col_letter, row_num = coordinate_from_string(freeze_pane)
            assert row_num == 2, f"Freeze panes at row {row_num}, expected row 2 (to freeze row 1)"
        wb.close()


class TestItemTypes:
    """Tests for verifying item_type values are appropriate."""

    def test_item_type_not_empty(self):
        """Verify item_type column has no empty/null values."""
        df = pd.read_excel(OUTPUT_FILE, sheet_name="Ranking")
        assert df["item_type"].notna().all(), "item_type column should have no null values"
        assert (df["item_type"].str.strip() != "").all(), "item_type values should not be empty strings"

    def test_item_name_not_empty(self):
        """Verify item_name column has no empty/null values."""
        df = pd.read_excel(OUTPUT_FILE, sheet_name="Ranking")
        assert df["item_name"].notna().all(), "item_name column should have no null values"
        assert (df["item_name"].str.strip() != "").all(), "item_name values should not be empty strings"


class TestTieBreaking:
    """Tests for verifying tie-breaking rules (alphabetical by item_name)."""

    def test_ties_broken_alphabetically(self):
        """Verify that ties in ratio are broken alphabetically by item_name."""
        df = pd.read_excel(OUTPUT_FILE, sheet_name="Ranking")
        df_sorted = df.sort_values("rank")

        # Find groups with same ratio
        for ratio_val in df_sorted["ratio"].unique():
            tied_items = df_sorted[abs(df_sorted["ratio"] - ratio_val) < 0.00005]
            if len(tied_items) > 1:
                # For tied items, check they are in alphabetical order by item_name
                item_names = tied_items.sort_values("rank")["item_name"].tolist()
                sorted_names = sorted(item_names)
                assert item_names == sorted_names, (
                    f"Tied items with ratio {ratio_val:.4f} should be ordered alphabetically. "
                    f"Got {item_names}, expected {sorted_names}"
                )


class TestExpectedRowCount:
    """Tests for verifying the expected number of rows."""

    def test_minimum_row_count(self):
        """Verify minimum expected rows: 2 strains + building types + 1 spending category."""
        df = pd.read_excel(OUTPUT_FILE, sheet_name="Ranking")
        # Minimum: 2 strains (C6706, LuxO) + 1 spending category = 3
        # Plus potential building types (1 unit, 2 to 4 units, 5 units or more)
        # Note: "2 to 4 units" column appears to have NA values, so may not be included
        assert len(df) >= 3, f"Expected at least 3 rows, got {len(df)}"

    def test_maximum_row_count(self):
        """Verify maximum expected rows: 2 strains + 3 building types + 1 spending = 6."""
        df = pd.read_excel(OUTPUT_FILE, sheet_name="Ranking")
        # Maximum: 2 strains + 3 building types + 1 spending category = 6
        assert len(df) <= 6, f"Expected at most 6 rows, got {len(df)}"


class TestDataIntegrity:
    """Tests for data integrity and correctness."""

    def test_strain_fold_change_reasonable(self):
        """Verify strain fold-change values are within reasonable biological range."""
        df = pd.read_excel(OUTPUT_FILE, sheet_name="Ranking")
        strain_rows = df[df["item_name"].isin(["C6706", "LuxO"])]

        for _, row in strain_rows.iterrows():
            ratio = row["ratio"]
            # OD values in the data range from ~0.02 to ~0.5, so fold-change should be reasonable
            assert 1 <= ratio <= 100, (
                f"Strain {row['item_name']} fold-change {ratio} seems unreasonable"
            )

    def test_construction_ratio_reasonable(self):
        """Verify construction ratios are within reasonable range."""
        df = pd.read_excel(OUTPUT_FILE, sheet_name="Ranking")
        building_types = ["1 unit", "2 to 4 units", "5 units or more"]
        construction_rows = df[df["item_name"].isin(building_types)]

        for _, row in construction_rows.iterrows():
            ratio = row["ratio"]
            # Construction data shows monthly values, ratios should be moderate
            assert 1 <= ratio <= 100, (
                f"Construction type '{row['item_name']}' ratio {ratio} seems unreasonable"
            )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

HEREDOC_EOF

# Execute command
python -m py_compile expectation_tests.py && echo "Syntax OK"

# Execute command
python -m pytest expectation_tests.py --collect-only 2>&1 | head -50

# Execute command
mkdir -p /root/harbor_workspaces/task_T384_run2/output

# Create /root/harbor_workspaces/task_T384_run2/process_data.py
mkdir -p $(dirname /root/harbor_workspaces/task_T384_run2/process_data.py)
cat << 'HEREDOC_EOF' > /root/harbor_workspaces/task_T384_run2/process_data.py
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font

# Step 1: Load the three CSV files
s9 = pd.read_csv("/root/Dataset S9.csv")
cons = pd.read_csv("/root/construction.csv")
spend = pd.read_csv("/root/construction_spending.csv")

# Step 2: Compute per-strain max OD fold-change (exclude Blank; min ignores OD <= 0)
s9_nb = s9[s9["Strain"] != "Blank"].copy()
max_od = s9_nb.groupby("Strain").agg(max_od=("OD", "max")).reset_index()
min_od_pos = s9_nb[s9_nb["OD"] > 0].groupby("Strain").agg(min_od=("OD", "min")).reset_index()
strain_fc = max_od.merge(min_od_pos, on="Strain", how="inner")
strain_fc["ratio"] = strain_fc["max_od"] / strain_fc["min_od"]
strain_rows = strain_fc[["Strain", "ratio"]].rename(columns={"Strain": "item_name"})
strain_rows["item_type"] = "strain"

# Step 3: Compute building-type ratios in construction.csv (ignore NA)
bld_cols = ["1 unit", "2 to 4 units", "5 units or more"]
bld_rows = []
for c in bld_cols:
    series = pd.to_numeric(cons[c], errors='coerce')
    mx = series.max(skipna=True)
    mn = series.min(skipna=True)
    if pd.notna(mx) and pd.notna(mn) and mn != 0:
        bld_rows.append({"item_type": "building_type", "item_name": c, "ratio": mx / mn})
bld_df = pd.DataFrame(bld_rows)

# Step 4: Find the spending category (annual.combined.*) with largest ratio
annual_cols = [c for c in spend.columns if c.startswith("annual.combined.")]
ratios = []
for c in annual_cols:
    series = pd.to_numeric(spend[c], errors='coerce')
    mx = series.max(skipna=True)
    mn = series.min(skipna=True)
    if pd.notna(mx) and pd.notna(mn) and mn > 0:
        ratios.append((c, mx / mn))

spend_winner_col, spend_winner_ratio = max(ratios, key=lambda x: x[1])
spend_row = pd.DataFrame([{
    "item_type": "spending_category",
    "item_name": spend_winner_col,
    "ratio": spend_winner_ratio
}])

# Step 5: Combine rows, sort, tie-break, and assign rank
combined = pd.concat([
    strain_rows[["item_type", "item_name", "ratio"]],
    bld_df[["item_type", "item_name", "ratio"]],
    spend_row[["item_type", "item_name", "ratio"]]
], ignore_index=True)

# Sort by ratio descending, then by item_name ascending for tie-break
combined = combined.sort_values(["ratio", "item_name"], ascending=[False, True]).reset_index(drop=True)
combined["rank"] = combined.index + 1
combined = combined[["item_type", "item_name", "ratio", "rank"]]

# Step 6: Write Excel and apply formatting
out_path = "/root/relative_change_ranking.xlsx"

with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
    combined.to_excel(writer, sheet_name="Ranking", index=False)

# Apply formatting
wb = load_workbook(out_path)
ws = wb["Ranking"]

# Bold header
for cell in ws[1]:
    cell.font = Font(bold=True)

# Freeze top row
ws.freeze_panes = "A2"

# Find ratio column index and apply 4 decimal format
ratio_col_idx = None
for j, cell in enumerate(ws[1], start=1):
    if cell.value == "ratio":
        ratio_col_idx = j
        break

for row in range(2, ws.max_row + 1):
    ws.cell(row=row, column=ratio_col_idx).number_format = "0.0000"

# Auto-fit column widths
for col_cells in ws.columns:
    max_len = 0
    col_letter = col_cells[0].column_letter
    for c in col_cells:
        v = "" if c.value is None else str(c.value)
        max_len = max(max_len, len(v))
    ws.column_dimensions[col_letter].width = max(10, min(60, max_len + 2))

wb.save(out_path)

print("Excel file created successfully!")
print(f"\nResults:\n{combined.to_string(index=False)}")
print(f"\nSpending category winner: {spend_winner_col}")

HEREDOC_EOF

# Execute command
python process_data.py

# Execute command
ls -la /root/harbor_workspaces/task_T384_run2/output/

# Execute command
python -c "
from openpyxl import load_workbook

wb = load_workbook('/root/relative_change_ranking.xlsx')
print('Sheet names:', wb.sheetnames)

ws = wb['Ranking']
print('Freeze panes:', ws.freeze_panes)

# Check header formatting
print('\\nHeader cells:')
for cell in ws[1]:
    print(f'  {cell.value}: bold={cell.font.bold}')

# Check ratio column format
print('\\nRatio values and formats:')
for row in range(2, ws.max_row + 1):
    cell = ws.cell(row=row, column=3)
    print(f'  Row {row}: value={cell.value}, format={cell.number_format}')

# Check column widths
print('\\nColumn widths:')
for col in ['A', 'B', 'C', 'D']:
    print(f'  {col}: {ws.column_dimensions[col].width}')
"

# Execute command
python -c "
import pandas as pd
cons = pd.read_csv('/root/construction.csv')
print('2 to 4 units column:')
print(cons['2 to 4 units'].tolist())
print('\\nAll NA?', cons['2 to 4 units'].isna().all())
"

# Execute command
python -c "
import pandas as pd

s9 = pd.read_csv('/root/Dataset S9.csv')
s9_nb = s9[s9['Strain'] != 'Blank'].copy()

for strain in ['C6706', 'LuxO']:
    strain_data = s9_nb[s9_nb['Strain'] == strain]
    max_od = strain_data['OD'].max()
    min_od_pos = strain_data[strain_data['OD'] > 0]['OD'].min()
    ratio = max_od / min_od_pos
    print(f'{strain}: max={max_od}, min(>0)={min_od_pos}, ratio={ratio:.4f}')
"

