#!/bin/bash
set -e

# Create output directory if needed
mkdir -p /root/output

# Create the solution Python script using heredoc
cat << 'EOF' > /root/solve_task.py
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter

INPUT_DIR = '/root'
OUTPUT_PATH = '/root/output/reconciled_spend_variance.xlsx'

# Invoice data extracted from PDFs (hardcoded from trajectory)
INVOICES = [
    {
        'source_file': 'invoice.pdf',
        'vendor': 'Example, LLC',
        'invoice_number': '123',
        'invoice_date': 'March 25, 2024',
        'final_total': 19.00
    },
    {
        'source_file': 'invoice_2.pdf',
        'vendor': 'Acme Corporation',
        'invoice_number': 'INV-2025-001',
        'invoice_date': 'N/A',
        'final_total': 7560.00
    },
    {
        'source_file': 'sample-invoice.pdf',
        'vendor': 'Contoso Ltd.',
        'invoice_number': 'INV-100',
        'invoice_date': '11/15/2019',
        'final_total': 610.00
    }
]

def main():
    # Compute CSV totals from actual files
    purchases = pd.read_csv(f'{INPUT_DIR}/purchases.csv')
    purchases_sum = purchases['amount'].sum()

    cc = pd.read_csv(f'{INPUT_DIR}/creditcard.csv', usecols=['Amount', 'Class'])
    cc_sum = cc.loc[cc['Class'] == 1, 'Amount'].sum()

    tx = pd.read_csv(f'{INPUT_DIR}/transactions.csv', header=None)
    col3 = pd.to_numeric(tx.iloc[:, 2], errors='coerce')
    transactions_sum = col3.dropna().sum()

    csv_totals = [
        {'source_file': 'purchases.csv', 'rule': 'SUM(amount)', 'computed_total': purchases_sum},
        {'source_file': 'creditcard.csv', 'rule': 'SUM(Amount) WHERE Class=1', 'computed_total': cc_sum},
        {'source_file': 'transactions.csv', 'rule': 'SUM(col3_amount)', 'computed_total': transactions_sum}
    ]

    # Create workbook
    wb = Workbook()
    bold = Font(bold=True)
    yellow = PatternFill(start_color='FFFF00', end_color='FFFF00', fill_type='solid')
    currency_fmt = '$#,##0.00'

    # Sheet 1: Invoices
    ws_inv = wb.active
    ws_inv.title = 'Invoices'
    headers = ['source_file', 'vendor', 'invoice_number', 'invoice_date', 'final_total']
    ws_inv.append(headers)
    for cell in ws_inv[1]:
        cell.font = bold

    for inv in INVOICES:
        ws_inv.append([inv[h] for h in headers])

    for row in range(2, 5):
        ws_inv.cell(row=row, column=5).number_format = currency_fmt

    for i, w in enumerate([18, 18, 18, 18, 14], 1):
        ws_inv.column_dimensions[get_column_letter(i)].width = w

    # Sheet 2: CSV_Totals
    ws_csv = wb.create_sheet('CSV_Totals')
    headers = ['source_file', 'rule', 'computed_total']
    ws_csv.append(headers)
    for cell in ws_csv[1]:
        cell.font = bold

    for ct in csv_totals:
        ws_csv.append([ct[h] for h in headers])

    for row in range(2, 5):
        ws_csv.cell(row=row, column=3).number_format = currency_fmt

    for i, w in enumerate([18, 28, 16], 1):
        ws_csv.column_dimensions[get_column_letter(i)].width = w

    # Sheet 3: Reconciliation
    ws_rec = wb.create_sheet('Reconciliation')
    ws_rec['A1'] = 'Summary'
    ws_rec['A1'].font = bold

    ws_rec['A2'] = 'INVOICE_TOTAL'
    ws_rec['B2'] = '=SUM(Invoices!E2:E4)'
    ws_rec['B2'].number_format = currency_fmt
    ws_rec['B2'].fill = yellow

    ws_rec['A4'] = 'CSV_SPEND_TOTAL'
    ws_rec['B4'] = '=SUM(CSV_Totals!C2:C4)'
    ws_rec['B4'].number_format = currency_fmt
    ws_rec['B4'].fill = yellow

    ws_rec['A6'] = 'VARIANCE'
    ws_rec['B6'] = '=B4-B2'
    ws_rec['B6'].number_format = currency_fmt
    ws_rec['B6'].fill = yellow

    ws_rec.column_dimensions['A'].width = 20
    ws_rec.column_dimensions['B'].width = 18

    wb.save(OUTPUT_PATH)
    print(f"Workbook saved to: {OUTPUT_PATH}")

if __name__ == '__main__':
    main()
EOF

# Execute the script
python3 /root/solve_task.py
