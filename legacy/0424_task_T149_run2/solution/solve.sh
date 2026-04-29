#!/bin/bash
set -e

# Create output directory
mkdir -p /root/output

# Create the solution Python script using heredoc
cat << 'EOF' > /root/solve_task.py
import pandas as pd
import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.chart import ScatterChart, Reference, Series

# Paths
FLIGHTS_CSV = '/root/flights.csv'
FLIGHTS_2_CSV = '/root/flights_2.csv'
OUTPUT_PATH = '/root/output/delay_vs_demand.xlsx'

# Month name to number mapping
MONTH_MAP = {
    'January': 1, 'February': 2, 'March': 3, 'April': 4,
    'May': 5, 'June': 6, 'July': 7, 'August': 8,
    'September': 9, 'October': 10, 'November': 11, 'December': 12
}

def main():
    # Step 1: Load flights.csv and compute monthly passengers
    df1 = pd.read_csv(FLIGHTS_CSV)
    df1['month'] = df1['month'].str.strip().map(MONTH_MAP)
    df1 = df1.rename(columns={'passengers': 'monthly_passengers'})
    monthly_passengers = df1[['year', 'month', 'monthly_passengers']]

    # Step 2: Load flights_2.csv, clean missing values, compute monthly avg arrival delay
    df2 = pd.read_csv(FLIGHTS_2_CSV, na_values=["NA", ""], keep_default_na=True)
    df2['arr_delay'] = pd.to_numeric(df2['arr_delay'], errors='coerce')
    df2['year'] = pd.to_numeric(df2['year'], errors='coerce')
    df2['month'] = pd.to_numeric(df2['month'], errors='coerce')

    avg_delay = df2.groupby(['year', 'month'], as_index=False)['arr_delay'].mean()
    avg_delay = avg_delay.rename(columns={'arr_delay': 'avg_arr_delay'})

    # Step 3: Inner join on (year, month)
    joined = pd.merge(monthly_passengers, avg_delay, on=['year', 'month'], how='inner')
    joined = joined[['year', 'month', 'monthly_passengers', 'avg_arr_delay']]

    # Step 4: Compute Pearson correlation
    if len(joined) >= 2:
        corr = joined['monthly_passengers'].corr(joined['avg_arr_delay'])
    else:
        corr = np.nan

    # Step 5: Create Excel workbook
    wb = Workbook()

    # Sheet 1: monthly_joined
    ws1 = wb.active
    ws1.title = 'monthly_joined'

    # Write headers with bold formatting
    headers = ['year', 'month', 'monthly_passengers', 'avg_arr_delay']
    for col, header in enumerate(headers, 1):
        cell = ws1.cell(row=1, column=col, value=header)
        cell.font = Font(bold=True)

    # Write data rows with blue font and number formats
    for row_idx, row in enumerate(joined.itertuples(index=False), 2):
        for col_idx, value in enumerate(row, 1):
            cell = ws1.cell(row=row_idx, column=col_idx, value=value)
            cell.font = Font(color='0000FF')
            if col_idx == 3:  # monthly_passengers - integer with thousands separator
                cell.number_format = '#,##0'
            elif col_idx == 4:  # avg_arr_delay - 1 decimal
                cell.number_format = '0.0'

    # Set column widths
    ws1.column_dimensions['A'].width = 8
    ws1.column_dimensions['B'].width = 8
    ws1.column_dimensions['C'].width = 18
    ws1.column_dimensions['D'].width = 14

    # Sheet 2: result
    ws2 = wb.create_sheet('result')
    ws2['A1'] = 'correlation'
    ws2['A1'].font = Font(bold=True)
    ws2['B1'] = corr if not np.isnan(corr) else None
    ws2['B1'].font = Font(color='000000')
    ws2['B1'].number_format = '0.0000'

    ws2.column_dimensions['A'].width = 12
    ws2.column_dimensions['B'].width = 12

    # Add scatter chart if we have data
    if len(joined) >= 2:
        chart = ScatterChart()
        chart.title = "Monthly Passengers vs Avg Arrival Delay"
        chart.x_axis.title = "Monthly Passengers"
        chart.y_axis.title = "Avg Arrival Delay (min)"
        chart.style = 10

        n_rows = len(joined) + 1
        x_values = Reference(ws1, min_col=3, min_row=2, max_row=n_rows)
        y_values = Reference(ws1, min_col=4, min_row=2, max_row=n_rows)

        series = Series(y_values, x_values, title="Delay vs Demand")
        chart.series.append(series)

        ws2.add_chart(chart, "A3")

    # Save workbook
    wb.save(OUTPUT_PATH)
    print(f"Excel file saved to: {OUTPUT_PATH}")

if __name__ == '__main__':
    main()
EOF

# Execute the script
python3 /root/solve_task.py
