#!/bin/bash
set -e

# Auto-generated solution based on execution trajectory
# This script recreates the outputs produced during synthesis

# Execute command
python3 -c "
import pandas as pd

# Read sample-salesv3.xlsx
print('=== sample-salesv3.xlsx ===')
df = pd.read_excel('input/sample-salesv3.xlsx')
print('Columns:', df.columns.tolist())
print('Shape:', df.shape)
print('Dtypes:')
print(df.dtypes)
print('\nFirst 5 rows:')
print(df.head())
print('\nUnique account numbers:', df['account number'].nunique())
"


# Execute command
python3 -c "
import pandas as pd

# Read Products.xlsx
print('=== Products.xlsx ===')
df = pd.read_excel('input/Products.xlsx')
print('Columns:', df.columns.tolist())
print('Shape:', df.shape)
print('Dtypes:')
print(df.dtypes)
print('\nFirst 5 rows:')
print(df.head())
print('\nPrice column stats:')
print(df['Price'].describe())
"


# Execute command
python3 -c "
import pandas as pd

# Read sample-1-sheet.xlsx
print('=== sample-1-sheet.xlsx ===')
df = pd.read_excel('input/sample-1-sheet.xlsx')
print('Columns:', df.columns.tolist())
print('Shape:', df.shape)
print('Dtypes:')
print(df.dtypes)
print('\nAll rows:')
print(df)
print('\nBoolean value at number=1:', df.loc[df['number']==1, 'boolean'].values)
"


# Execute command
python3 -c "
import pandas as pd
from openpyxl import load_workbook

# Read Formula Excel Template.xlsx
print('=== Formula Excel Template.xlsx ===')
wb = load_workbook('input/Formula Excel Template.xlsx')
print('Sheet names:', wb.sheetnames)
for sheet_name in wb.sheetnames:
    ws = wb[sheet_name]
    print(f'\nSheet: {sheet_name}')
    print(f'Dimensions: {ws.dimensions}')
    print('First few rows:')
    for i, row in enumerate(ws.iter_rows(max_row=5, values_only=True)):
        print(f'  Row {i+1}: {row}')
"


# Execute command
python3 -c "
import pandas as pd
import numpy as np

# Load sales data
sales = pd.read_excel('input/sample-salesv3.xlsx')
sales['date'] = pd.to_datetime(sales['date'])
sales['ext price'] = pd.to_numeric(sales['ext price'], errors='coerce')

# Filter to 2014 (should be all rows)
sales_2014 = sales[sales['date'].dt.year == 2014]
print(f'Rows in 2014: {len(sales_2014)} out of {len(sales)}')

# Compute net revenue per account
net_revenue = sales_2014.groupby('account number')['ext price'].sum().reset_index()
net_revenue.columns = ['account number', 'net_revenue']
print('\\nNet Revenue per Account:')
print(net_revenue.sort_values('net_revenue'))

# Compute median
median_rev = net_revenue['net_revenue'].median()
print(f'\\nMedian Net Revenue: {median_rev}')

# Find account closest to median
net_revenue['abs_diff'] = abs(net_revenue['net_revenue'] - median_rev)
closest = net_revenue.sort_values(['abs_diff', 'account number']).iloc[0]
print(f'\\nClosest account to median:')
print(f'  Account Number: {closest[\"account number\"]}')
print(f'  Net Revenue: {closest[\"net_revenue\"]}')
print(f'  Abs Diff from Median: {closest[\"abs_diff\"]}')

# Get customer name (most frequent for that account, tie-break: lexicographically smallest)
target_account = closest['account number']
account_names = sales_2014[sales_2014['account number'] == target_account]['name'].value_counts()
print(f'\\nName counts for account {target_account}:')
print(account_names)
# If tie, pick lexicographically smallest
max_count = account_names.max()
top_names = account_names[account_names == max_count].index.tolist()
customer_name = sorted(top_names)[0]
print(f'Customer Name: {customer_name}')

# Weighted average unit price (only positive quantity rows)
account_txns = sales_2014[sales_2014['account number'] == target_account]
pos_qty_txns = account_txns[account_txns['quantity'] > 0]
print(f'\\nTransactions with qty > 0: {len(pos_qty_txns)} out of {len(account_txns)}')
weighted_sum = (pos_qty_txns['quantity'] * pos_qty_txns['unit price']).sum()
total_qty = pos_qty_txns['quantity'].sum()
weighted_avg_price = weighted_sum / total_qty
print(f'Weighted Avg Unit Price (pos qty only): {weighted_avg_price}')

# Catalog median product price
products = pd.read_excel('input/Products.xlsx')
catalog_median = products['Price'].median()
print(f'\\nCatalog Median Product Price: {catalog_median}')

# AboveCatalogMedian flag
above_catalog_median = weighted_avg_price > catalog_median
print(f'AboveCatalogMedian: {above_catalog_median}')

# Summary
print('\\n=== EXPECTED OUTPUT ===')
print(f'AccountNumber: {target_account}')
print(f'CustomerName: {customer_name}')
print(f'NetRevenue2014: {closest[\"net_revenue\"]}')
print(f'MedianNetRevenueAllAccounts: {median_rev}')
print(f'AbsDiffFromMedian: {closest[\"abs_diff\"]}')
print(f'WeightedAvgUnitPrice_PosQtyOnly: {weighted_avg_price}')
print(f'CatalogMedianProductPrice: {catalog_median}')
print(f'AboveCatalogMedian: {above_catalog_median}')
"


# Create /root/expectation_tests.py
mkdir -p $(dirname /root/expectation_tests.py)
cat << 'HEREDOC_EOF' > /root/expectation_tests.py
"""Auto-generated expectation tests for task verification.

These tests verify that the task execution produces correct outputs
based on the instruction requirements for the median account report task.

Expected calculations:
- Target account: 146832 (closest to median net revenue)
- Customer name: Kiehn-Spinka
- Net Revenue 2014: 99608.77
- Median Net Revenue (all accounts): 100271.535
- Abs Diff from Median: ~662.765
- Weighted Avg Unit Price (positive qty only): ~56.723
- Catalog Median Product Price: 19.5
- AboveCatalogMedian: True (because 56.723 > 19.5)
"""

import os
from pathlib import Path

import pandas as pd
import pytest
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill


class TestOutputFileExists:
    """Tests for output file existence and basic structure."""

    OUTPUT_PATH = "/root/median_account_report.xlsx"

    def test_output_file_exists(self):
        """Verify output file was created at the specified path."""
        assert os.path.exists(self.OUTPUT_PATH), (
            f"Output file not found at {self.OUTPUT_PATH}"
        )

    def test_output_file_is_valid_excel(self):
        """Verify output is a valid Excel file that can be loaded."""
        wb = load_workbook(self.OUTPUT_PATH)
        assert wb is not None, "Failed to load output file as Excel workbook"
        wb.close()

    def test_output_directory_exists(self):
        """Verify output directory exists."""
        output_dir = "/root"
        assert os.path.isdir(output_dir), f"Output directory not found: {output_dir}"


class TestWorkbookStructure:
    """Tests for workbook sheet structure and template preservation."""

    OUTPUT_PATH = "/root/median_account_report.xlsx"
    TEMPLATE_SHEETS = [
        'Max-Min', 'IF-IFS', 'Len', 'LeftRight', 'DateToText', 'TRIM',
        'Substitute', 'SUM-SumIF', 'Count-CountIF', 'Concatenate', 'Days-NetworkDays'
    ]

    def test_median_account_sheet_exists(self):
        """Verify MedianAccount sheet was created."""
        wb = load_workbook(self.OUTPUT_PATH)
        assert 'MedianAccount' in wb.sheetnames, (
            f"MedianAccount sheet not found. Available sheets: {wb.sheetnames}"
        )
        wb.close()

    def test_template_sheets_preserved(self):
        """Verify all original template sheets are preserved."""
        wb = load_workbook(self.OUTPUT_PATH)
        for sheet_name in self.TEMPLATE_SHEETS:
            assert sheet_name in wb.sheetnames, (
                f"Template sheet '{sheet_name}' is missing from output workbook"
            )
        wb.close()

    def test_total_sheet_count(self):
        """Verify correct total number of sheets (11 template + 1 MedianAccount)."""
        wb = load_workbook(self.OUTPUT_PATH)
        expected_count = len(self.TEMPLATE_SHEETS) + 1  # 12 total
        assert len(wb.sheetnames) == expected_count, (
            f"Expected {expected_count} sheets, found {len(wb.sheetnames)}: {wb.sheetnames}"
        )
        wb.close()


class TestMedianAccountSheetHeaders:
    """Tests for MedianAccount sheet header structure."""

    OUTPUT_PATH = "/root/median_account_report.xlsx"
    REQUIRED_HEADERS = [
        'AccountNumber',
        'CustomerName',
        'NetRevenue2014',
        'MedianNetRevenueAllAccounts',
        'AbsDiffFromMedian',
        'WeightedAvgUnitPrice_PosQtyOnly',
        'CatalogMedianProductPrice',
        'AboveCatalogMedian'
    ]

    def test_required_headers_present(self):
        """Verify all required column headers are present in MedianAccount sheet."""
        wb = load_workbook(self.OUTPUT_PATH)
        ws = wb['MedianAccount']

        # Get all values from the first row (headers)
        headers = []
        for cell in ws[1]:
            if cell.value is not None:
                headers.append(str(cell.value))

        for required_header in self.REQUIRED_HEADERS:
            assert required_header in headers, (
                f"Required header '{required_header}' not found. Found headers: {headers}"
            )
        wb.close()

    def test_header_count_matches(self):
        """Verify the number of headers matches expected count."""
        wb = load_workbook(self.OUTPUT_PATH)
        ws = wb['MedianAccount']

        headers = [cell.value for cell in ws[1] if cell.value is not None]
        assert len(headers) == len(self.REQUIRED_HEADERS), (
            f"Expected {len(self.REQUIRED_HEADERS)} headers, found {len(headers)}: {headers}"
        )
        wb.close()


class TestMedianAccountValues:
    """Tests for computed values in MedianAccount sheet."""

    OUTPUT_PATH = "/root/median_account_report.xlsx"

    # Expected values (computed from task requirements)
    EXPECTED_ACCOUNT_NUMBER = 146832
    EXPECTED_CUSTOMER_NAME = "Kiehn-Spinka"
    EXPECTED_NET_REVENUE = 99608.77
    EXPECTED_MEDIAN_NET_REVENUE = 100271.535
    EXPECTED_ABS_DIFF = 662.765  # approximately
    EXPECTED_WEIGHTED_AVG_PRICE = 56.723  # approximately
    EXPECTED_CATALOG_MEDIAN = 19.5
    EXPECTED_ABOVE_CATALOG_MEDIAN = True

    def _get_sheet_data(self):
        """Helper to load MedianAccount data as a dictionary."""
        wb = load_workbook(self.OUTPUT_PATH)
        ws = wb['MedianAccount']

        # Get headers from row 1
        headers = [cell.value for cell in ws[1] if cell.value is not None]

        # Get values from row 2 (data row)
        values = [cell.value for cell in ws[2]][:len(headers)]

        data = dict(zip(headers, values))
        wb.close()
        return data

    def test_account_number_value(self):
        """Verify AccountNumber is the expected value (146832)."""
        data = self._get_sheet_data()
        account_num = data.get('AccountNumber')
        assert account_num is not None, "AccountNumber value is missing"
        assert int(account_num) == self.EXPECTED_ACCOUNT_NUMBER, (
            f"Expected AccountNumber {self.EXPECTED_ACCOUNT_NUMBER}, got {account_num}"
        )

    def test_customer_name_value(self):
        """Verify CustomerName is the expected value."""
        data = self._get_sheet_data()
        customer_name = data.get('CustomerName')
        assert customer_name is not None, "CustomerName value is missing"
        assert str(customer_name).strip() == self.EXPECTED_CUSTOMER_NAME, (
            f"Expected CustomerName '{self.EXPECTED_CUSTOMER_NAME}', got '{customer_name}'"
        )

    def test_net_revenue_2014_value(self):
        """Verify NetRevenue2014 is close to expected value."""
        data = self._get_sheet_data()
        net_revenue = data.get('NetRevenue2014')
        assert net_revenue is not None, "NetRevenue2014 value is missing"
        assert abs(float(net_revenue) - self.EXPECTED_NET_REVENUE) < 0.01, (
            f"Expected NetRevenue2014 ~{self.EXPECTED_NET_REVENUE}, got {net_revenue}"
        )

    def test_median_net_revenue_value(self):
        """Verify MedianNetRevenueAllAccounts is close to expected value."""
        data = self._get_sheet_data()
        median_rev = data.get('MedianNetRevenueAllAccounts')
        assert median_rev is not None, "MedianNetRevenueAllAccounts value is missing"
        assert abs(float(median_rev) - self.EXPECTED_MEDIAN_NET_REVENUE) < 0.01, (
            f"Expected MedianNetRevenueAllAccounts ~{self.EXPECTED_MEDIAN_NET_REVENUE}, got {median_rev}"
        )

    def test_abs_diff_from_median_value(self):
        """Verify AbsDiffFromMedian is close to expected value."""
        data = self._get_sheet_data()
        abs_diff = data.get('AbsDiffFromMedian')
        assert abs_diff is not None, "AbsDiffFromMedian value is missing"
        assert abs(float(abs_diff) - self.EXPECTED_ABS_DIFF) < 0.01, (
            f"Expected AbsDiffFromMedian ~{self.EXPECTED_ABS_DIFF}, got {abs_diff}"
        )

    def test_weighted_avg_unit_price_value(self):
        """Verify WeightedAvgUnitPrice_PosQtyOnly is close to expected value."""
        data = self._get_sheet_data()
        weighted_avg = data.get('WeightedAvgUnitPrice_PosQtyOnly')
        assert weighted_avg is not None, "WeightedAvgUnitPrice_PosQtyOnly value is missing"
        assert abs(float(weighted_avg) - self.EXPECTED_WEIGHTED_AVG_PRICE) < 0.01, (
            f"Expected WeightedAvgUnitPrice_PosQtyOnly ~{self.EXPECTED_WEIGHTED_AVG_PRICE}, got {weighted_avg}"
        )

    def test_catalog_median_product_price_value(self):
        """Verify CatalogMedianProductPrice is the expected value."""
        data = self._get_sheet_data()
        catalog_median = data.get('CatalogMedianProductPrice')
        assert catalog_median is not None, "CatalogMedianProductPrice value is missing"
        assert abs(float(catalog_median) - self.EXPECTED_CATALOG_MEDIAN) < 0.01, (
            f"Expected CatalogMedianProductPrice ~{self.EXPECTED_CATALOG_MEDIAN}, got {catalog_median}"
        )

    def test_above_catalog_median_value(self):
        """Verify AboveCatalogMedian is TRUE (since weighted avg > catalog median)."""
        data = self._get_sheet_data()
        above_flag = data.get('AboveCatalogMedian')
        assert above_flag is not None, "AboveCatalogMedian value is missing"

        # Handle various representations of True
        if isinstance(above_flag, bool):
            assert above_flag is True, f"Expected AboveCatalogMedian to be True, got {above_flag}"
        elif isinstance(above_flag, str):
            assert above_flag.upper() in ['TRUE', 'YES', '1'], (
                f"Expected AboveCatalogMedian to be TRUE, got '{above_flag}'"
            )
        else:
            assert bool(above_flag), f"Expected AboveCatalogMedian to be truthy, got {above_flag}"


class TestValueConsistency:
    """Tests for internal consistency of computed values."""

    OUTPUT_PATH = "/root/median_account_report.xlsx"

    def _get_sheet_data(self):
        """Helper to load MedianAccount data as a dictionary."""
        wb = load_workbook(self.OUTPUT_PATH)
        ws = wb['MedianAccount']
        headers = [cell.value for cell in ws[1] if cell.value is not None]
        values = [cell.value for cell in ws[2]][:len(headers)]
        data = dict(zip(headers, values))
        wb.close()
        return data

    def test_abs_diff_calculation_correct(self):
        """Verify AbsDiffFromMedian = |NetRevenue2014 - MedianNetRevenueAllAccounts|."""
        data = self._get_sheet_data()
        net_rev = float(data['NetRevenue2014'])
        median_rev = float(data['MedianNetRevenueAllAccounts'])
        abs_diff = float(data['AbsDiffFromMedian'])

        expected_abs_diff = abs(net_rev - median_rev)
        assert abs(abs_diff - expected_abs_diff) < 0.01, (
            f"AbsDiffFromMedian ({abs_diff}) should equal |{net_rev} - {median_rev}| = {expected_abs_diff}"
        )

    def test_above_catalog_median_calculation_correct(self):
        """Verify AboveCatalogMedian flag matches weighted avg > catalog median."""
        data = self._get_sheet_data()
        weighted_avg = float(data['WeightedAvgUnitPrice_PosQtyOnly'])
        catalog_median = float(data['CatalogMedianProductPrice'])
        above_flag = data['AboveCatalogMedian']

        expected_flag = weighted_avg > catalog_median

        # Normalize the flag to boolean
        if isinstance(above_flag, bool):
            actual_flag = above_flag
        elif isinstance(above_flag, str):
            actual_flag = above_flag.upper() in ['TRUE', 'YES', '1']
        else:
            actual_flag = bool(above_flag)

        assert actual_flag == expected_flag, (
            f"AboveCatalogMedian should be {expected_flag} "
            f"(weighted avg {weighted_avg} {'>' if expected_flag else '<='} catalog median {catalog_median})"
        )


class TestHeaderFormatting:
    """Tests for header formatting based on sample-1-sheet.xlsx boolean value."""

    OUTPUT_PATH = "/root/median_account_report.xlsx"

    def test_header_row_is_bold(self):
        """Verify header row has bold font (since boolean=True for number=1)."""
        wb = load_workbook(self.OUTPUT_PATH)
        ws = wb['MedianAccount']

        # Check if any header cell is bold (at least one should be)
        has_bold = False
        for cell in ws[1]:
            if cell.value is not None and cell.font and cell.font.bold:
                has_bold = True
                break

        assert has_bold, (
            "Header row should have bold font because boolean=True for number=1 "
            "in sample-1-sheet.xlsx"
        )
        wb.close()

    def test_header_row_has_yellow_fill(self):
        """Verify header row has yellow fill (since boolean=True for number=1)."""
        wb = load_workbook(self.OUTPUT_PATH)
        ws = wb['MedianAccount']

        # Check if any header cell has a yellow fill
        has_yellow_fill = False
        for cell in ws[1]:
            if cell.value is not None and cell.fill:
                # Check for yellow fill (various shades)
                fill_color = cell.fill.start_color
                if fill_color and fill_color.rgb:
                    # Yellow colors typically have high R, high G, low B
                    # Common yellow: FFFF00, FFFF99, etc.
                    rgb = str(fill_color.rgb)
                    if rgb.upper() in ['FFFFFF00', 'FFFF00', 'FFFFFF99', 'FFFFCC00', 'FFFFE599'] or \
                       (len(rgb) >= 6 and rgb[-6:-4].upper() == 'FF' and rgb[-4:-2].upper() == 'FF'):
                        has_yellow_fill = True
                        break
                    # Also check for any non-white fill that could be yellow
                    if fill_color.type == 'rgb' and fill_color.rgb not in [None, '00000000', 'FFFFFFFF']:
                        # Check if it's a yellowish color
                        try:
                            if len(rgb) >= 6:
                                r = int(rgb[-6:-4], 16) if len(rgb) >= 6 else 0
                                g = int(rgb[-4:-2], 16) if len(rgb) >= 4 else 0
                                b = int(rgb[-2:], 16) if len(rgb) >= 2 else 0
                                # Yellow has high R, high G, low B
                                if r > 200 and g > 200 and b < 150:
                                    has_yellow_fill = True
                                    break
                        except (ValueError, IndexError):
                            pass

        assert has_yellow_fill, (
            "Header row should have yellow fill because boolean=True for number=1 "
            "in sample-1-sheet.xlsx"
        )
        wb.close()


class TestDataRowStructure:
    """Tests for data row structure in MedianAccount sheet."""

    OUTPUT_PATH = "/root/median_account_report.xlsx"

    def test_single_data_row_only(self):
        """Verify there is exactly one data row (plus header)."""
        wb = load_workbook(self.OUTPUT_PATH)
        ws = wb['MedianAccount']

        # Count non-empty rows
        non_empty_rows = 0
        for row in ws.iter_rows(max_row=10):  # Check first 10 rows
            if any(cell.value is not None for cell in row):
                non_empty_rows += 1

        # Should have exactly 2 rows: header + 1 data row
        assert non_empty_rows == 2, (
            f"Expected exactly 2 rows (1 header + 1 data), found {non_empty_rows} non-empty rows"
        )
        wb.close()

    def test_all_values_populated(self):
        """Verify all required fields have values (no None/empty)."""
        wb = load_workbook(self.OUTPUT_PATH)
        ws = wb['MedianAccount']

        headers = [cell.value for cell in ws[1] if cell.value is not None]
        values = [cell.value for cell in ws[2]][:len(headers)]

        for i, (header, value) in enumerate(zip(headers, values)):
            assert value is not None, f"Value for '{header}' is missing (None)"
            if isinstance(value, str):
                assert value.strip() != '', f"Value for '{header}' is empty string"

        wb.close()


class TestNumericTypes:
    """Tests for correct numeric types in computed values."""

    OUTPUT_PATH = "/root/median_account_report.xlsx"

    def _get_sheet_data(self):
        """Helper to load MedianAccount data as a dictionary."""
        wb = load_workbook(self.OUTPUT_PATH)
        ws = wb['MedianAccount']
        headers = [cell.value for cell in ws[1] if cell.value is not None]
        values = [cell.value for cell in ws[2]][:len(headers)]
        data = dict(zip(headers, values))
        wb.close()
        return data

    def test_account_number_is_numeric(self):
        """Verify AccountNumber can be converted to integer."""
        data = self._get_sheet_data()
        account_num = data.get('AccountNumber')
        try:
            int(account_num)
        except (TypeError, ValueError) as e:
            pytest.fail(f"AccountNumber '{account_num}' cannot be converted to integer: {e}")

    def test_revenue_values_are_numeric(self):
        """Verify revenue-related values are numeric."""
        data = self._get_sheet_data()
        numeric_fields = [
            'NetRevenue2014',
            'MedianNetRevenueAllAccounts',
            'AbsDiffFromMedian',
            'WeightedAvgUnitPrice_PosQtyOnly',
            'CatalogMedianProductPrice'
        ]

        for field in numeric_fields:
            value = data.get(field)
            try:
                float(value)
            except (TypeError, ValueError) as e:
                pytest.fail(f"{field} value '{value}' cannot be converted to float: {e}")


class TestSourceDataValidation:
    """Tests to validate that output data is consistent with source files."""

    OUTPUT_PATH = "/root/median_account_report.xlsx"
    INPUT_DIR = "/root"

    def test_account_number_exists_in_sales_data(self):
        """Verify the reported account number exists in the sales data."""
        # Get account from output
        wb = load_workbook(self.OUTPUT_PATH)
        ws = wb['MedianAccount']
        headers = [cell.value for cell in ws[1] if cell.value is not None]
        values = [cell.value for cell in ws[2]][:len(headers)]
        data = dict(zip(headers, values))
        wb.close()

        account_num = int(data['AccountNumber'])

        # Check against source
        sales_df = pd.read_excel(f"{self.INPUT_DIR}/sample-salesv3.xlsx")
        assert account_num in sales_df['account number'].values, (
            f"AccountNumber {account_num} not found in sample-salesv3.xlsx"
        )

    def test_customer_name_exists_for_account(self):
        """Verify the reported customer name exists for the account in sales data."""
        # Get data from output
        wb = load_workbook(self.OUTPUT_PATH)
        ws = wb['MedianAccount']
        headers = [cell.value for cell in ws[1] if cell.value is not None]
        values = [cell.value for cell in ws[2]][:len(headers)]
        data = dict(zip(headers, values))
        wb.close()

        account_num = int(data['AccountNumber'])
        customer_name = str(data['CustomerName']).strip()

        # Check against source
        sales_df = pd.read_excel(f"{self.INPUT_DIR}/sample-salesv3.xlsx")
        account_names = sales_df[sales_df['account number'] == account_num]['name'].unique()

        assert customer_name in account_names, (
            f"CustomerName '{customer_name}' not found for account {account_num}. "
            f"Available names: {list(account_names)}"
        )

    def test_catalog_median_matches_products_file(self):
        """Verify CatalogMedianProductPrice matches median from Products.xlsx."""
        # Get data from output
        wb = load_workbook(self.OUTPUT_PATH)
        ws = wb['MedianAccount']
        headers = [cell.value for cell in ws[1] if cell.value is not None]
        values = [cell.value for cell in ws[2]][:len(headers)]
        data = dict(zip(headers, values))
        wb.close()

        reported_median = float(data['CatalogMedianProductPrice'])

        # Calculate from source
        products_df = pd.read_excel(f"{self.INPUT_DIR}/Products.xlsx")
        actual_median = products_df['Price'].median()

        assert abs(reported_median - actual_median) < 0.01, (
            f"CatalogMedianProductPrice ({reported_median}) doesn't match "
            f"actual median from Products.xlsx ({actual_median})"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

HEREDOC_EOF

# Execute command
python3 -m py_compile expectation_tests.py && echo "Syntax OK"

# Execute command
python3 -m pytest expectation_tests.py --collect-only 2>/dev/null | head -60

# Execute command
python3 -m pytest expectation_tests.py --collect-only 2>&1 | head -80

# Execute command
pip install pytest -q && python3 -m pytest expectation_tests.py --collect-only 2>&1 | head -80

# Execute command
ls -la /root/

# Execute command
mkdir -p /root/output

# Create /root/process_sales.py
mkdir -p $(dirname /root/process_sales.py)
cat << 'HEREDOC_EOF' > /root/process_sales.py
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill

# Paths
sales_path = '/root/sample-salesv3.xlsx'
products_path = '/root/Products.xlsx'
sample1_path = '/root/sample-1-sheet.xlsx'
template_path = '/root/Formula Excel Template.xlsx'
output_path = '/root/median_account_report.xlsx'

# Step 1: Load and clean sales data
df = pd.read_excel(sales_path)
df['date'] = pd.to_datetime(df['date'])
df = df[df['date'].dt.year == 2014]
df['ext price'] = pd.to_numeric(df['ext price'], errors='coerce')
df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
df['unit price'] = pd.to_numeric(df['unit price'], errors='coerce')

print(f"Sales data rows after 2014 filter: {len(df)}")
print(f"Years in data: {df['date'].dt.year.unique()}")

# Step 2: Compute per-account net revenue and median
acct_rev = df.groupby('account number', as_index=False)['ext price'].sum()
acct_rev.columns = ['account number', 'net_revenue']
median_rev = acct_rev['net_revenue'].median()
print(f"Number of accounts: {len(acct_rev)}")
print(f"Median net revenue: {median_rev}")

# Step 3: Find the account closest to median (deterministic tie-break)
acct_rev['AbsDiffFromMedian'] = (acct_rev['net_revenue'] - median_rev).abs()
acct_rev_sorted = acct_rev.sort_values(['AbsDiffFromMedian', 'account number'], ascending=[True, True])
target = acct_rev_sorted.iloc[0]

account_number = int(target['account number'])
net_revenue_2014 = float(target['net_revenue'])
abs_diff = float(target['AbsDiffFromMedian'])

print(f"Target account: {account_number}")
print(f"Net revenue: {net_revenue_2014}")
print(f"Abs diff from median: {abs_diff}")

# Step 4: Derive CustomerName (mode; tie -> lexicographically smallest)
df_t = df[df['account number'] == account_number]
name_counts = df_t.groupby('name').size().reset_index(name='cnt')
name_counts = name_counts.sort_values(['cnt', 'name'], ascending=[False, True])
customer_name = name_counts.iloc[0]['name']
print(f"Customer name: {customer_name}")

# Step 5: Weighted average unit price (positive quantity only)
df_pos = df_t[df_t['quantity'] > 0].copy()
if len(df_pos) > 0 and df_pos['quantity'].sum() > 0:
    num = (df_pos['quantity'] * df_pos['unit price']).sum()
    den = df_pos['quantity'].sum()
    wavg_unit_price = num / den
else:
    wavg_unit_price = 0.0
print(f"Weighted avg unit price (pos qty only): {wavg_unit_price}")

# Step 6: Compute catalog median product price from Products.xlsx
prod = pd.read_excel(products_path)
prod['Price'] = pd.to_numeric(prod['Price'], errors='coerce')
catalog_median = prod['Price'].median()
above_catalog_median = bool(wavg_unit_price > catalog_median)
print(f"Catalog median price: {catalog_median}")
print(f"Above catalog median: {above_catalog_median}")

# Step 7: Read sample-1-sheet.xlsx to decide header formatting
s1 = pd.read_excel(sample1_path)
fmt_on = bool(s1.loc[s1['number'] == 1, 'boolean'].iloc[0])
print(f"Format headers (from sample-1-sheet.xlsx): {fmt_on}")

# Step 8: Load template and add MedianAccount sheet
wb = load_workbook(template_path)
ws = wb.create_sheet('MedianAccount')

# Define headers
headers = [
    'AccountNumber',
    'CustomerName',
    'NetRevenue2014',
    'MedianNetRevenueAllAccounts',
    'AbsDiffFromMedian',
    'WeightedAvgUnitPrice_PosQtyOnly',
    'CatalogMedianProductPrice',
    'AboveCatalogMedian'
]

# Define values
values = [
    account_number,
    customer_name,
    net_revenue_2014,
    median_rev,
    abs_diff,
    wavg_unit_price,
    catalog_median,
    above_catalog_median
]

# Write headers (row 1)
for col_idx, header in enumerate(headers, start=1):
    ws.cell(row=1, column=col_idx, value=header)

# Write values (row 2)
for col_idx, val in enumerate(values, start=1):
    ws.cell(row=2, column=col_idx, value=val)

# Apply formatting based on sample-1-sheet.xlsx boolean
if fmt_on:
    yellow_fill = PatternFill('solid', fgColor='FFFF00')
    bold_font = Font(bold=True)
    for col_idx in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=col_idx)
        cell.font = bold_font
        cell.fill = yellow_fill

# Adjust column widths for readability
for col_idx, header in enumerate(headers, start=1):
    ws.column_dimensions[ws.cell(row=1, column=col_idx).column_letter].width = max(len(header) + 2, 15)

# Step 9: Save
wb.save(output_path)
print(f"\nSaved to: {output_path}")

# Verification
print("\n=== Verification ===")
print(f"Template sheets preserved: {[s for s in wb.sheetnames if s != 'MedianAccount']}")
print(f"New sheet added: MedianAccount")
print(f"Total sheets: {len(wb.sheetnames)}")

HEREDOC_EOF

# Execute command
python3 process_sales.py

# Execute command
python3 -c "
import pandas as pd
from openpyxl import load_workbook

output_path = '/root/median_account_report.xlsx'

# Verify the file exists and can be opened
wb = load_workbook(output_path)
print('=== Sheet Names ===')
print(wb.sheetnames)

print('\n=== MedianAccount Sheet Content ===')
ws = wb['MedianAccount']
for row in ws.iter_rows(min_row=1, max_row=2, values_only=True):
    print(row)

print('\n=== Header Formatting Check ===')
for col in range(1, 9):
    cell = ws.cell(row=1, column=col)
    print(f'{cell.value}: bold={cell.font.bold}, fill={cell.fill.fgColor.rgb if cell.fill.patternType else None}')
"


# Execute command
python3 -c "
import pandas as pd

# Check that original sheets have their data intact
output_path = '/root/median_account_report.xlsx'
template_path = '/root/Formula Excel Template.xlsx'

# Compare a sample sheet (Max-Min) from original and output
original_df = pd.read_excel(template_path, sheet_name='Max-Min')
output_df = pd.read_excel(output_path, sheet_name='Max-Min')

print('=== Original Max-Min sheet (first 5 rows) ===')
print(original_df.head())

print('\n=== Output Max-Min sheet (first 5 rows) ===')
print(output_df.head())

print('\n=== Data preserved correctly? ===')
print(f'Shapes match: {original_df.shape == output_df.shape}')
"


# Execute command
python3 -c "
import pandas as pd

# Detailed verification of the deterministic selection
sales_path = '/root/sample-salesv3.xlsx'
df = pd.read_excel(sales_path)
df['date'] = pd.to_datetime(df['date'])
df = df[df['date'].dt.year == 2014]
df['ext price'] = pd.to_numeric(df['ext price'], errors='coerce')

acct_rev = df.groupby('account number', as_index=False)['ext price'].sum()
acct_rev.columns = ['account number', 'net_revenue']
median_rev = acct_rev['net_revenue'].median()

acct_rev['AbsDiffFromMedian'] = (acct_rev['net_revenue'] - median_rev).abs()
acct_rev_sorted = acct_rev.sort_values(['AbsDiffFromMedian', 'account number'], ascending=[True, True])

print('=== Top 5 accounts closest to median ===')
print(acct_rev_sorted[['account number', 'net_revenue', 'AbsDiffFromMedian']].head())

print(f'\n=== Median Net Revenue: {median_rev} ===')
print(f'Selected account: {int(acct_rev_sorted.iloc[0][\"account number\"])}')

# Verify sample-1-sheet.xlsx boolean value
s1 = pd.read_excel('/root/sample-1-sheet.xlsx')
print('\n=== sample-1-sheet.xlsx content ===')
print(s1)
print(f'Boolean value at number=1: {s1.loc[s1[\"number\"] == 1, \"boolean\"].iloc[0]}')
"


# Execute command
ls -la /root/

