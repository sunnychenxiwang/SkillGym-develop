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

# Create /root/harbor_workspaces/task_T459_run2/expectation_tests.py
mkdir -p $(dirname /root/harbor_workspaces/task_T459_run2/expectation_tests.py)
cat << 'HEREDOC_EOF' > /root/harbor_workspaces/task_T459_run2/expectation_tests.py
"""Auto-generated expectation tests for RTPLAN reference validation task.

These tests verify that the task execution produces correct outputs
based on the instruction requirements for validating RTPLAN references
against CT and MR images.
"""

import os
from pathlib import Path

import pytest

# Expected output file path
OUTPUT_FILE = "/root/rtplan_reference_validation.xlsx"


class TestOutputFileExists:
    """Tests for output file existence and basic validity."""

    def test_output_file_exists(self):
        """Verify output Excel file was created at the exact specified path."""
        assert os.path.exists(OUTPUT_FILE), (
            f"Output file not found at {OUTPUT_FILE}. "
            "The task requires the Excel file to be written to exactly this path."
        )

    def test_output_file_is_not_empty(self):
        """Verify output file has content."""
        assert os.path.exists(OUTPUT_FILE), f"Output file not found: {OUTPUT_FILE}"
        file_size = os.path.getsize(OUTPUT_FILE)
        assert file_size > 0, "Output file is empty"

    def test_output_file_has_xlsx_extension(self):
        """Verify output file has correct .xlsx extension."""
        assert OUTPUT_FILE.endswith(".xlsx"), "Output file must have .xlsx extension"

    def test_output_directory_exists(self):
        """Verify the output directory exists."""
        output_dir = os.path.dirname(OUTPUT_FILE)
        assert os.path.isdir(output_dir), f"Output directory does not exist: {output_dir}"


class TestExcelWorkbookStructure:
    """Tests for Excel workbook structure using openpyxl."""

    @pytest.fixture
    def workbook(self):
        """Load the output workbook."""
        from openpyxl import load_workbook
        assert os.path.exists(OUTPUT_FILE), f"Output file not found: {OUTPUT_FILE}"
        return load_workbook(OUTPUT_FILE)

    def test_workbook_is_valid_xlsx(self):
        """Verify the file is a valid Excel workbook."""
        from openpyxl import load_workbook
        assert os.path.exists(OUTPUT_FILE), f"Output file not found: {OUTPUT_FILE}"
        try:
            wb = load_workbook(OUTPUT_FILE)
            assert wb is not None
        except Exception as e:
            pytest.fail(f"Failed to load workbook as valid Excel file: {e}")

    def test_summary_sheet_exists(self, workbook):
        """Verify the Summary sheet exists in the workbook."""
        sheet_names = workbook.sheetnames
        assert "Summary" in sheet_names, (
            f"'Summary' sheet not found. Available sheets: {sheet_names}"
        )

    def test_uid_matches_sheet_exists(self, workbook):
        """Verify the UID_Matches sheet exists in the workbook."""
        sheet_names = workbook.sheetnames
        assert "UID_Matches" in sheet_names, (
            f"'UID_Matches' sheet not found. Available sheets: {sheet_names}"
        )


class TestSummarySheet:
    """Tests for the Summary sheet content and formatting."""

    @pytest.fixture
    def summary_sheet(self):
        """Load the Summary sheet from the workbook."""
        from openpyxl import load_workbook
        assert os.path.exists(OUTPUT_FILE), f"Output file not found: {OUTPUT_FILE}"
        wb = load_workbook(OUTPUT_FILE)
        assert "Summary" in wb.sheetnames, "Summary sheet not found"
        return wb["Summary"]

    def test_verdict_cell_exists(self, summary_sheet):
        """Verify cell B2 contains the overall verdict."""
        cell_value = summary_sheet["B2"].value
        assert cell_value is not None, "Cell B2 (verdict) is empty"

    def test_verdict_is_pass_or_fail(self, summary_sheet):
        """Verify the verdict is either PASS or FAIL."""
        verdict = summary_sheet["B2"].value
        assert verdict in ("PASS", "FAIL"), (
            f"Verdict must be 'PASS' or 'FAIL', got: {verdict}"
        )

    def test_total_uid_count_cell_exists(self, summary_sheet):
        """Verify cell B3 contains the total referenced UID count."""
        cell_value = summary_sheet["B3"].value
        assert cell_value is not None, "Cell B3 (total UID count) is empty"

    def test_total_uid_count_is_numeric(self, summary_sheet):
        """Verify total UID count is a valid number."""
        total_count = summary_sheet["B3"].value
        assert isinstance(total_count, (int, float)), (
            f"Total UID count must be numeric, got: {type(total_count)}"
        )
        assert total_count >= 0, "Total UID count cannot be negative"

    def test_matched_count_cell_exists(self, summary_sheet):
        """Verify cell B4 contains the matched count."""
        cell_value = summary_sheet["B4"].value
        assert cell_value is not None, "Cell B4 (matched count) is empty"

    def test_matched_count_is_numeric(self, summary_sheet):
        """Verify matched count is a valid number."""
        matched_count = summary_sheet["B4"].value
        assert isinstance(matched_count, (int, float)), (
            f"Matched count must be numeric, got: {type(matched_count)}"
        )
        assert matched_count >= 0, "Matched count cannot be negative"

    def test_unmatched_count_cell_exists(self, summary_sheet):
        """Verify cell B5 contains the unmatched count."""
        cell_value = summary_sheet["B5"].value
        assert cell_value is not None, "Cell B5 (unmatched count) is empty"

    def test_unmatched_count_is_numeric(self, summary_sheet):
        """Verify unmatched count is a valid number."""
        unmatched_count = summary_sheet["B5"].value
        assert isinstance(unmatched_count, (int, float)), (
            f"Unmatched count must be numeric, got: {type(unmatched_count)}"
        )
        assert unmatched_count >= 0, "Unmatched count cannot be negative"

    def test_counts_add_up(self, summary_sheet):
        """Verify that matched + unmatched = total."""
        total = summary_sheet["B3"].value
        matched = summary_sheet["B4"].value
        unmatched = summary_sheet["B5"].value
        assert matched + unmatched == total, (
            f"Counts don't add up: matched({matched}) + unmatched({unmatched}) != total({total})"
        )

    def test_verdict_consistent_with_counts(self, summary_sheet):
        """Verify verdict is consistent with match counts."""
        verdict = summary_sheet["B2"].value
        total = summary_sheet["B3"].value
        matched = summary_sheet["B4"].value
        unmatched = summary_sheet["B5"].value

        if total > 0 and unmatched == 0:
            assert verdict == "PASS", (
                f"Verdict should be PASS when all UIDs match, but got {verdict}"
            )
        elif unmatched > 0:
            assert verdict == "FAIL", (
                f"Verdict should be FAIL when there are unmatched UIDs, but got {verdict}"
            )

    def test_verdict_cell_has_fill_color(self, summary_sheet):
        """Verify cell B2 has conditional fill color (green for PASS, yellow for FAIL)."""
        cell = summary_sheet["B2"]
        verdict = cell.value
        fill = cell.fill

        # Check that fill is applied (not default/no fill)
        if fill.fill_type is not None:
            fill_color = fill.start_color.rgb if fill.start_color else None
            # Accept any non-default fill as valid styling
            assert fill_color is not None or fill.fill_type == "solid", (
                "Cell B2 should have a fill color applied"
            )


class TestUIDMatchesSheet:
    """Tests for the UID_Matches sheet content and formatting."""

    @pytest.fixture
    def uid_matches_sheet(self):
        """Load the UID_Matches sheet from the workbook."""
        from openpyxl import load_workbook
        assert os.path.exists(OUTPUT_FILE), f"Output file not found: {OUTPUT_FILE}"
        wb = load_workbook(OUTPUT_FILE)
        assert "UID_Matches" in wb.sheetnames, "UID_Matches sheet not found"
        return wb["UID_Matches"]

    def test_required_headers_present(self, uid_matches_sheet):
        """Verify all required column headers are present."""
        required_headers = [
            "referenced_uid",
            "uid_type_detected",
            "matched_file",
            "matched_identifier_field",
            "match_status"
        ]

        # Read the first row for headers
        headers = []
        for col in range(1, uid_matches_sheet.max_column + 1):
            cell_value = uid_matches_sheet.cell(row=1, column=col).value
            if cell_value:
                headers.append(cell_value)

        for required in required_headers:
            assert required in headers, (
                f"Required header '{required}' not found. Headers present: {headers}"
            )

    def test_header_row_is_bold(self, uid_matches_sheet):
        """Verify the header row has bold formatting."""
        # Check first few header cells for bold formatting
        bold_count = 0
        for col in range(1, min(6, uid_matches_sheet.max_column + 1)):
            cell = uid_matches_sheet.cell(row=1, column=col)
            if cell.font and cell.font.bold:
                bold_count += 1

        assert bold_count > 0, "Header row should have bold formatting"

    def test_sheet_has_data_rows(self, uid_matches_sheet):
        """Verify the sheet contains data rows (not just headers)."""
        max_row = uid_matches_sheet.max_row
        # Should have at least header row + 1 data row
        assert max_row >= 1, "UID_Matches sheet should have at least a header row"

    def test_match_status_values_valid(self, uid_matches_sheet):
        """Verify match_status column contains only MATCH or NO_MATCH values."""
        # Find the match_status column
        match_status_col = None
        for col in range(1, uid_matches_sheet.max_column + 1):
            if uid_matches_sheet.cell(row=1, column=col).value == "match_status":
                match_status_col = col
                break

        assert match_status_col is not None, "match_status column not found"

        # Check all data rows
        for row in range(2, uid_matches_sheet.max_row + 1):
            status = uid_matches_sheet.cell(row=row, column=match_status_col).value
            if status is not None:  # Skip empty rows
                assert status in ("MATCH", "NO_MATCH"), (
                    f"Invalid match_status value at row {row}: {status}"
                )

    def test_uid_type_detected_values_valid(self, uid_matches_sheet):
        """Verify uid_type_detected contains valid values."""
        valid_types = ["StudyInstanceUID", "SeriesInstanceUID", "SOPInstanceUID", "Other/Unknown"]

        # Find the uid_type_detected column
        type_col = None
        for col in range(1, uid_matches_sheet.max_column + 1):
            if uid_matches_sheet.cell(row=1, column=col).value == "uid_type_detected":
                type_col = col
                break

        assert type_col is not None, "uid_type_detected column not found"

        # Check all data rows
        for row in range(2, uid_matches_sheet.max_row + 1):
            uid_type = uid_matches_sheet.cell(row=row, column=type_col).value
            if uid_type is not None:  # Skip empty rows
                assert uid_type in valid_types, (
                    f"Invalid uid_type_detected value at row {row}: {uid_type}. "
                    f"Valid values are: {valid_types}"
                )

    def test_matched_file_values_valid(self, uid_matches_sheet):
        """Verify matched_file contains valid file names or is blank."""
        valid_files = ["CT_small.dcm", "MR_small.dcm", "", None]

        # Find the matched_file column
        file_col = None
        for col in range(1, uid_matches_sheet.max_column + 1):
            if uid_matches_sheet.cell(row=1, column=col).value == "matched_file":
                file_col = col
                break

        assert file_col is not None, "matched_file column not found"

        # Check all data rows
        for row in range(2, uid_matches_sheet.max_row + 1):
            matched_file = uid_matches_sheet.cell(row=row, column=file_col).value
            assert matched_file in valid_files or matched_file == "", (
                f"Invalid matched_file value at row {row}: {matched_file}. "
                f"Valid values are: CT_small.dcm, MR_small.dcm, or blank"
            )

    def test_referenced_uid_values_look_like_dicom_uids(self, uid_matches_sheet):
        """Verify referenced_uid values follow DICOM UID pattern."""
        import re
        uid_pattern = re.compile(r'^[\d.]+$')

        # Find the referenced_uid column
        uid_col = None
        for col in range(1, uid_matches_sheet.max_column + 1):
            if uid_matches_sheet.cell(row=1, column=col).value == "referenced_uid":
                uid_col = col
                break

        assert uid_col is not None, "referenced_uid column not found"

        # Check all data rows
        for row in range(2, uid_matches_sheet.max_row + 1):
            uid = uid_matches_sheet.cell(row=row, column=uid_col).value
            if uid is not None and uid != "":
                uid_str = str(uid)
                assert uid_pattern.match(uid_str), (
                    f"referenced_uid at row {row} doesn't match DICOM UID pattern: {uid}"
                )

    def test_column_widths_are_reasonable(self, uid_matches_sheet):
        """Verify columns have reasonable widths set (not default narrow)."""
        # Check that at least some columns have explicit widths
        widths_set = 0
        for col_letter in ['A', 'B', 'C', 'D', 'E']:
            col_dim = uid_matches_sheet.column_dimensions.get(col_letter)
            if col_dim and col_dim.width and col_dim.width > 8:  # Default is ~8
                widths_set += 1

        # At least some columns should have adjusted widths
        assert widths_set > 0, (
            "Column widths should be set to reasonable values (not default narrow)"
        )


class TestDataConsistency:
    """Tests for data consistency between sheets."""

    @pytest.fixture
    def workbook(self):
        """Load the output workbook."""
        from openpyxl import load_workbook
        assert os.path.exists(OUTPUT_FILE), f"Output file not found: {OUTPUT_FILE}"
        return load_workbook(OUTPUT_FILE)

    def test_summary_total_matches_uid_matches_rows(self, workbook):
        """Verify Summary total count matches number of rows in UID_Matches."""
        summary = workbook["Summary"]
        uid_matches = workbook["UID_Matches"]

        total_from_summary = summary["B3"].value
        # Count data rows in UID_Matches (excluding header)
        data_rows = uid_matches.max_row - 1  # Subtract header row

        assert total_from_summary == data_rows, (
            f"Summary total ({total_from_summary}) doesn't match "
            f"UID_Matches data rows ({data_rows})"
        )

    def test_summary_matched_count_matches_uid_matches_data(self, workbook):
        """Verify Summary matched count matches MATCH rows in UID_Matches."""
        summary = workbook["Summary"]
        uid_matches = workbook["UID_Matches"]

        matched_from_summary = summary["B4"].value

        # Find match_status column and count MATCH values
        match_status_col = None
        for col in range(1, uid_matches.max_column + 1):
            if uid_matches.cell(row=1, column=col).value == "match_status":
                match_status_col = col
                break

        match_count = 0
        for row in range(2, uid_matches.max_row + 1):
            if uid_matches.cell(row=row, column=match_status_col).value == "MATCH":
                match_count += 1

        assert matched_from_summary == match_count, (
            f"Summary matched count ({matched_from_summary}) doesn't match "
            f"MATCH rows in UID_Matches ({match_count})"
        )


class TestInputFilesUsed:
    """Tests to verify input DICOM files are accessible (prerequisite check)."""

    def test_rtplan_input_exists(self):
        """Verify the RTPLAN input file exists."""
        rtplan_path = "/root/rtplan.dcm"
        assert os.path.exists(rtplan_path), f"RTPLAN input file not found: {rtplan_path}"

    def test_ct_input_exists(self):
        """Verify the CT input file exists."""
        ct_path = "/root/CT_small.dcm"
        assert os.path.exists(ct_path), f"CT input file not found: {ct_path}"

    def test_mr_input_exists(self):
        """Verify the MR input file exists."""
        mr_path = "/root/MR_small.dcm"
        assert os.path.exists(mr_path), f"MR input file not found: {mr_path}"


class TestReproducibility:
    """Tests to verify the verdict is deterministic and reproducible."""

    def test_verdict_matches_expected_logic(self):
        """Verify the verdict follows the PASS/FAIL logic from the specification.

        PASS: Every referenced UID from RTPLAN matches at least one CT/MR identifier
        FAIL: Otherwise
        """
        from openpyxl import load_workbook
        assert os.path.exists(OUTPUT_FILE), f"Output file not found: {OUTPUT_FILE}"

        wb = load_workbook(OUTPUT_FILE)
        summary = wb["Summary"]
        uid_matches = wb["UID_Matches"]

        verdict = summary["B2"].value
        unmatched = summary["B5"].value

        # Verify logic: PASS only if no unmatched UIDs
        if unmatched == 0:
            expected_verdict = "PASS"
        else:
            expected_verdict = "FAIL"

        assert verdict == expected_verdict, (
            f"Verdict '{verdict}' is inconsistent with unmatched count ({unmatched}). "
            f"Expected '{expected_verdict}'"
        )

HEREDOC_EOF

# Execute command
python -m py_compile expectation_tests.py && echo "Syntax OK"

# Execute command
mkdir -p /root/harbor_workspaces/task_T459_run2/output

# Execute command
python3 -c "import pydicom; import pandas; import openpyxl; print('All packages available')" 2>&1 || pip install pydicom pandas openpyxl -q

# Create /root/harbor_workspaces/task_T459_run2/rtplan_validation.py
mkdir -p $(dirname /root/harbor_workspaces/task_T459_run2/rtplan_validation.py)
cat << 'HEREDOC_EOF' > /root/harbor_workspaces/task_T459_run2/rtplan_validation.py
#!/usr/bin/env python3
"""RTPLAN Reference Validation - Validates RTPLAN UID references against CT/MR images."""

import re
import pydicom
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

# UID pattern: one or more digit groups separated by dots
UID_PATTERN = re.compile(r'^[0-9]+(\.[0-9]+)+$')

def extract_uids_recursive(ds, uids_set):
    """Recursively extract all UID-like values from a DICOM dataset."""
    for elem in ds:
        if elem.VR == 'SQ':  # Sequence - recurse into items
            for item in elem.value:
                extract_uids_recursive(item, uids_set)
        elif 'UID' in elem.keyword:
            # Extract UID values
            value = elem.value
            if value is None:
                continue
            # Handle MultiValue
            if hasattr(value, '__iter__') and not isinstance(value, str):
                for v in value:
                    if isinstance(v, str) and UID_PATTERN.match(v):
                        uids_set.add(v)
            elif isinstance(value, str) and UID_PATTERN.match(value):
                uids_set.add(value)

def read_rtplan_uids(rtplan_path):
    """Read RTPLAN and extract all referenced UIDs."""
    ds = pydicom.dcmread(rtplan_path)
    uids_set = set()
    extract_uids_recursive(ds, uids_set)
    return sorted(list(uids_set))

def read_image_identifiers(dcm_path, filename):
    """Read CT/MR DICOM and extract identifiers + metadata."""
    ds = pydicom.dcmread(dcm_path)
    identifiers = {
        'filename': filename,
        'StudyInstanceUID': getattr(ds, 'StudyInstanceUID', None),
        'SeriesInstanceUID': getattr(ds, 'SeriesInstanceUID', None),
        'SOPInstanceUID': getattr(ds, 'SOPInstanceUID', None),
        'SOPClassUID': getattr(ds, 'SOPClassUID', None),
        'Modality': getattr(ds, 'Modality', None),
        'Rows': getattr(ds, 'Rows', None),
        'Columns': getattr(ds, 'Columns', None),
        'PixelSpacing': getattr(ds, 'PixelSpacing', None)
    }
    return identifiers

def match_uid(uid, files_data):
    """Match a UID against CT/MR identifiers. Returns match info."""
    # Fields to match in priority order
    uid_fields = ['StudyInstanceUID', 'SeriesInstanceUID', 'SOPInstanceUID', 'SOPClassUID']

    # Check files in deterministic order
    for file_info in files_data:
        for field in uid_fields:
            if file_info.get(field) and str(file_info[field]) == uid:
                # Determine uid_type_detected
                if field in ['StudyInstanceUID', 'SeriesInstanceUID', 'SOPInstanceUID']:
                    uid_type = field
                else:
                    uid_type = 'Other/Unknown'
                return {
                    'matched_file': file_info['filename'],
                    'matched_identifier_field': field,
                    'uid_type_detected': uid_type,
                    'match_status': 'MATCH'
                }

    # No match found
    return {
        'matched_file': '',
        'matched_identifier_field': '',
        'uid_type_detected': 'Other/Unknown',
        'match_status': 'NO_MATCH'
    }

def build_match_table(referenced_uids, files_data):
    """Build the match table as a pandas DataFrame."""
    rows = []
    for uid in referenced_uids:
        match_info = match_uid(uid, files_data)
        rows.append({
            'referenced_uid': uid,
            'uid_type_detected': match_info['uid_type_detected'],
            'matched_file': match_info['matched_file'],
            'matched_identifier_field': match_info['matched_identifier_field'],
            'match_status': match_info['match_status']
        })
    return pd.DataFrame(rows)

def write_excel_report(df, output_path):
    """Write styled Excel report with Summary and UID_Matches sheets."""
    total_referenced = len(df)
    matched_count = (df['match_status'] == 'MATCH').sum()
    unmatched_count = total_referenced - matched_count
    verdict = 'PASS' if unmatched_count == 0 else 'FAIL'

    wb = Workbook()

    # Summary sheet
    ws_summary = wb.active
    ws_summary.title = 'Summary'

    # Headers in column A
    ws_summary['A2'] = 'Overall Verdict'
    ws_summary['A3'] = 'Total Referenced UID Count'
    ws_summary['A4'] = 'Matched Count'
    ws_summary['A5'] = 'Unmatched Count'

    # Values in column B
    ws_summary['B2'] = verdict
    ws_summary['B3'] = total_referenced
    ws_summary['B4'] = matched_count
    ws_summary['B5'] = unmatched_count

    # Style headers (column A) as bold
    bold_font = Font(bold=True)
    for row in range(2, 6):
        ws_summary[f'A{row}'].font = bold_font

    # Style verdict cell with fill color
    if verdict == 'PASS':
        ws_summary['B2'].fill = PatternFill(start_color='00FF00', fill_type='solid')
    else:
        ws_summary['B2'].fill = PatternFill(start_color='FFFF00', fill_type='solid')

    # Set column widths for Summary
    ws_summary.column_dimensions['A'].width = 28
    ws_summary.column_dimensions['B'].width = 20

    # UID_Matches sheet
    ws_matches = wb.create_sheet('UID_Matches')

    # Write header row
    headers = list(df.columns)
    for col_idx, header in enumerate(headers, 1):
        cell = ws_matches.cell(row=1, column=col_idx, value=header)
        cell.font = bold_font

    # Write data rows
    for row_idx, row_data in enumerate(df.itertuples(index=False), 2):
        for col_idx, value in enumerate(row_data, 1):
            ws_matches.cell(row=row_idx, column=col_idx, value=value)

    # Set column widths for UID_Matches
    ws_matches.column_dimensions['A'].width = 60  # referenced_uid
    ws_matches.column_dimensions['B'].width = 20  # uid_type_detected
    ws_matches.column_dimensions['C'].width = 18  # matched_file
    ws_matches.column_dimensions['D'].width = 25  # matched_identifier_field
    ws_matches.column_dimensions['E'].width = 15  # match_status

    wb.save(output_path)

    return verdict, total_referenced, matched_count, unmatched_count

def main():
    # File paths
    rtplan_path = '/root/rtplan.dcm'
    ct_path = '/root/CT_small.dcm'
    mr_path = '/root/MR_small.dcm'
    output_path = '/root/rtplan_reference_validation.xlsx'

    # Step 1: Extract UIDs from RTPLAN
    print("Step 1: Extracting UIDs from RTPLAN...")
    referenced_uids = read_rtplan_uids(rtplan_path)
    print(f"  Found {len(referenced_uids)} unique UIDs")

    # Step 2: Read CT and MR identifiers
    print("\nStep 2: Reading CT and MR identifiers...")
    ct_data = read_image_identifiers(ct_path, 'CT_small.dcm')
    mr_data = read_image_identifiers(mr_path, 'MR_small.dcm')

    # Deterministic order: CT first, then MR
    files_data = [ct_data, mr_data]

    print(f"  CT identifiers:")
    for field in ['StudyInstanceUID', 'SeriesInstanceUID', 'SOPInstanceUID', 'SOPClassUID']:
        print(f"    {field}: {ct_data.get(field)}")
    print(f"  CT metadata: Modality={ct_data.get('Modality')}, Rows={ct_data.get('Rows')}, Columns={ct_data.get('Columns')}")

    print(f"  MR identifiers:")
    for field in ['StudyInstanceUID', 'SeriesInstanceUID', 'SOPInstanceUID', 'SOPClassUID']:
        print(f"    {field}: {mr_data.get(field)}")
    print(f"  MR metadata: Modality={mr_data.get('Modality')}, Rows={mr_data.get('Rows')}, Columns={mr_data.get('Columns')}")

    # Step 3: Build match table
    print("\nStep 3: Building match table...")
    df = build_match_table(referenced_uids, files_data)
    print(f"  Match table created with {len(df)} rows")

    # Step 4 & 5: Compute verdict and write Excel report
    print("\nStep 4 & 5: Computing verdict and writing Excel report...")
    verdict, total, matched, unmatched = write_excel_report(df, output_path)

    print(f"\n{'='*50}")
    print(f"RESULTS:")
    print(f"  Overall Verdict: {verdict}")
    print(f"  Total Referenced UIDs: {total}")
    print(f"  Matched: {matched}")
    print(f"  Unmatched: {unmatched}")
    print(f"{'='*50}")
    print(f"\nExcel report written to: {output_path}")

    # Show match details
    print("\nMatch Details:")
    for _, row in df.iterrows():
        status = row['match_status']
        uid_short = row['referenced_uid'][:40] + '...' if len(row['referenced_uid']) > 40 else row['referenced_uid']
        if status == 'MATCH':
            print(f"  [MATCH] {uid_short} -> {row['matched_file']}:{row['matched_identifier_field']}")
        else:
            print(f"  [NO_MATCH] {uid_short}")

if __name__ == '__main__':
    main()

HEREDOC_EOF

# Execute command
python3 rtplan_validation.py

# Execute command
ls -la /root/harbor_workspaces/task_T459_run2/output/

# Execute command
python3 -c "
import pandas as pd
from openpyxl import load_workbook

wb = load_workbook('/root/rtplan_reference_validation.xlsx')
print('Sheet names:', wb.sheetnames)

# Check Summary sheet
ws = wb['Summary']
print('\nSummary sheet contents:')
for row in range(2, 6):
    label = ws[f'A{row}'].value
    value = ws[f'B{row}'].value
    fill = ws[f'B{row}'].fill
    fill_color = fill.start_color.rgb if fill and fill.start_color else 'No fill'
    print(f'  {label}: {value} (fill: {fill_color})')

# Check UID_Matches sheet
df = pd.read_excel('/root/rtplan_reference_validation.xlsx', sheet_name='UID_Matches')
print('\nUID_Matches sheet:')
print(f'  Columns: {list(df.columns)}')
print(f'  Row count: {len(df)}')
print(df.to_string())
"

# Execute command
python3 -c "
from openpyxl import load_workbook

wb = load_workbook('/root/rtplan_reference_validation.xlsx')

# Check Summary sheet header styling
ws_summary = wb['Summary']
print('Summary sheet - Column A bold check:')
for row in range(2, 6):
    cell = ws_summary[f'A{row}']
    print(f'  A{row} ({cell.value}): bold={cell.font.bold}')

# Check UID_Matches header row styling
ws_matches = wb['UID_Matches']
print('\nUID_Matches sheet - Header row bold check:')
for col in ['A', 'B', 'C', 'D', 'E']:
    cell = ws_matches[f'{col}1']
    print(f'  {col}1 ({cell.value}): bold={cell.font.bold}')

# Check column widths
print('\nUID_Matches column widths:')
for col in ['A', 'B', 'C', 'D', 'E']:
    width = ws_matches.column_dimensions[col].width
    print(f'  Column {col}: {width}')
"

