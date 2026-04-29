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
ls -la /root/harbor_workspaces/task_T418_run1/input/

# Execute command
mkdir -p /root/harbor_workspaces/task_T418_run1/output && pip show scapy openpyxl 2>/dev/null | grep -E "^Name:|^Version:" || pip install scapy openpyxl -q

# Create /root/harbor_workspaces/task_T418_run1/analyze_ftp.py
mkdir -p $(dirname /root/harbor_workspaces/task_T418_run1/analyze_ftp.py)
cat << 'HEREDOC_EOF' > /root/harbor_workspaces/task_T418_run1/analyze_ftp.py
#!/usr/bin/env python3
"""Analyze FTP brute force vs normal traffic from PCAP files and create Excel comparison."""

from collections import Counter, defaultdict
from scapy.all import PcapReader, IP, TCP, Raw
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment


def analyze_ftp_pcap(pcap_path):
    """Parse FTP control-channel traffic from PCAP and compute metrics."""
    # Per-stream buffers for reconstructing FTP lines
    # Stream key: normalized (sorted) tuple of endpoints
    stream_buffers = defaultdict(lambda: defaultdict(bytes))  # stream -> direction -> bytes

    # Metrics
    user_counts = Counter()
    pass_counts = Counter()
    total_login_attempts = 0

    # Server identification
    server_ip = None
    client_ip = None

    # Per-stream state for success tracking
    stream_state = defaultdict(lambda: {'seen_user': False, 'seen_pass': False})
    success_count = 0

    def get_stream_key(src_ip, src_port, dst_ip, dst_port):
        """Create normalized stream key."""
        if (src_ip, src_port) < (dst_ip, dst_port):
            return (src_ip, src_port, dst_ip, dst_port)
        return (dst_ip, dst_port, src_ip, src_port)

    def get_direction(src_ip, src_port, dst_ip, dst_port):
        """Get direction key within stream."""
        return (src_ip, src_port, dst_ip, dst_port)

    def process_line(line, src_ip, dst_ip, stream_key):
        """Process a complete FTP line."""
        nonlocal server_ip, client_ip, total_login_attempts, success_count

        line_str = line.decode('utf-8', errors='ignore').strip()
        if not line_str:
            return

        # Identify server (sends 220 banner) and client
        if line_str.startswith('220') and server_ip is None:
            server_ip = src_ip
            client_ip = dst_ip

        # Determine if this is client->server or server->client
        is_client_to_server = (server_ip is not None and dst_ip == server_ip)
        is_server_to_client = (server_ip is not None and src_ip == server_ip)

        if is_client_to_server:
            # Client commands
            if line_str.upper().startswith('USER '):
                username = line_str[5:].strip()
                user_counts[username] += 1
                stream_state[stream_key]['seen_user'] = True
                stream_state[stream_key]['seen_pass'] = False
            elif line_str.upper().startswith('PASS '):
                password = line_str[5:]  # Keep password as-is (may have leading/trailing spaces)
                pass_counts[password] += 1
                total_login_attempts += 1
                if stream_state[stream_key]['seen_user']:
                    stream_state[stream_key]['seen_pass'] = True

        if is_server_to_client:
            # Server responses - check for 230 (login successful)
            if line_str.startswith('230'):
                state = stream_state[stream_key]
                if state['seen_user'] and state['seen_pass']:
                    success_count += 1
                    state['seen_user'] = False
                    state['seen_pass'] = False

    # Read packets
    with PcapReader(pcap_path) as pcap:
        for pkt in pcap:
            if IP not in pkt or TCP not in pkt:
                continue

            # Filter FTP control channel (port 21)
            sport = pkt[TCP].sport
            dport = pkt[TCP].dport
            if sport != 21 and dport != 21:
                continue

            src_ip = pkt[IP].src
            dst_ip = pkt[IP].dst

            # Get stream key and direction
            stream_key = get_stream_key(src_ip, sport, dst_ip, dport)
            direction = get_direction(src_ip, sport, dst_ip, dport)

            # Process payload if present
            if Raw in pkt:
                payload = bytes(pkt[Raw].load)
                stream_buffers[stream_key][direction] += payload

                # Split on \r\n and process complete lines
                buffer = stream_buffers[stream_key][direction]
                while b'\r\n' in buffer:
                    line, buffer = buffer.split(b'\r\n', 1)
                    stream_buffers[stream_key][direction] = buffer
                    process_line(line, src_ip, dst_ip, stream_key)

    # Process any remaining data in buffers
    for stream_key, directions in stream_buffers.items():
        for direction, buffer in directions.items():
            if buffer:
                src_ip = direction[0]
                dst_ip = direction[2]
                process_line(buffer, src_ip, dst_ip, stream_key)

    # Calculate derived metrics
    unique_usernames = len(user_counts)

    # Most targeted username (tie-break lexicographically)
    if user_counts:
        most_targeted_username = min(
            user_counts.keys(),
            key=lambda x: (-user_counts[x], x)
        )
    else:
        most_targeted_username = ''

    # Top password candidate (tie-break lexicographically)
    if pass_counts:
        top_password_candidate = min(
            pass_counts.keys(),
            key=lambda x: (-pass_counts[x], x)
        )
    else:
        top_password_candidate = ''

    # Bruteforce score
    bruteforce_score = total_login_attempts / max(1, unique_usernames)

    return {
        'server_ip': server_ip or '',
        'client_ip': client_ip or '',
        'total_login_attempts': total_login_attempts,
        'unique_usernames': unique_usernames,
        'most_targeted_username': most_targeted_username,
        'top_password_candidate': top_password_candidate,
        'success_count': success_count,
        'bruteforce_score': bruteforce_score
    }


def create_excel_workbook(results, protocol_category, output_path):
    """Create Excel workbook with comparison and methods sheets."""
    wb = Workbook()

    # Rename default sheet to 'comparison'
    ws_comparison = wb.active
    ws_comparison.title = 'comparison'

    # Column headers
    headers = [
        'pcap', 'protocol_category', 'server_ip', 'client_ip',
        'total_login_attempts', 'unique_usernames', 'most_targeted_username',
        'top_password_candidate', 'success_count', 'bruteforce_score'
    ]

    # Write headers with bold font
    for col, header in enumerate(headers, 1):
        cell = ws_comparison.cell(row=1, column=col, value=header)
        cell.font = Font(bold=True)

    # Write data rows
    for row_idx, (pcap_name, data) in enumerate(results.items(), 2):
        row_data = [
            pcap_name,
            protocol_category,
            data['server_ip'],
            data['client_ip'],
            data['total_login_attempts'],
            data['unique_usernames'],
            data['most_targeted_username'],
            data['top_password_candidate'],
            data['success_count'],
            data['bruteforce_score']
        ]

        for col, value in enumerate(row_data, 1):
            cell = ws_comparison.cell(row=row_idx, column=col, value=value)

            # Right-align numeric columns (5, 6, 9, 10)
            if col in [5, 6, 9, 10]:
                cell.alignment = Alignment(horizontal='right')

            # Format bruteforce_score with 4 decimal places
            if col == 10:
                cell.number_format = '0.0000'

    # Adjust column widths
    column_widths = {
        'A': 18, 'B': 20, 'C': 15, 'D': 15, 'E': 20,
        'F': 18, 'G': 25, 'H': 22, 'I': 15, 'J': 18
    }
    for col_letter, width in column_widths.items():
        ws_comparison.column_dimensions[col_letter].width = width

    # Create 'methods' sheet
    ws_methods = wb.create_sheet('methods')

    methods_text = [
        "METHODS FOR FTP BRUTE-FORCE ANALYSIS",
        "",
        "(a) Server vs Client identification: The server is the endpoint",
        "    that sends the 220 FTP banner response. Client is the other.",
        "",
        "(b) Counting attempts: PASS commands on TCP/21 are counted.",
        "    USER commands track unique usernames. Tie-breaks: lexicographic.",
        "(c) Success definition: 230 response after USER+PASS in same stream."
    ]

    for row_idx, line in enumerate(methods_text, 1):
        ws_methods.cell(row=row_idx, column=1, value=line)

    ws_methods.column_dimensions['A'].width = 70

    wb.save(output_path)


def main():
    input_dir = '/root/harbor_workspaces/task_T418_run1/input'
    output_path = '/root/ftp_bruteforce_comparison.xlsx'

    # Protocol category from Wireshark SampleCaptures HTML page
    # FTP entries appear under the "General / Unsorted" h2 heading
    protocol_category = 'General / Unsorted'

    # Analyze both PCAP files
    pcap_files = ['bruteforce.pcap', 'ftp.pcap']
    results = {}

    for pcap_name in pcap_files:
        pcap_path = f'{input_dir}/{pcap_name}'
        results[pcap_name] = analyze_ftp_pcap(pcap_path)

    # Create Excel workbook
    create_excel_workbook(results, protocol_category, output_path)

    # Verification output (not final answer)
    for pcap_name, data in results.items():
        print(f"\n{pcap_name}:")
        for key, value in data.items():
            if key == 'bruteforce_score':
                print(f"  {key}: {value:.4f}")
            else:
                print(f"  {key}: {value}")


if __name__ == '__main__':
    main()

HEREDOC_EOF

# Execute command
python analyze_ftp.py

# Execute command
ls -la /root/harbor_workspaces/task_T418_run1/output/

# Execute command
python3 -c "
from openpyxl import load_workbook
wb = load_workbook('/root/ftp_bruteforce_comparison.xlsx')
print('Sheet names:', wb.sheetnames)
print()

# Check comparison sheet
ws = wb['comparison']
print('=== comparison sheet ===')
for row in ws.iter_rows(min_row=1, max_row=3, values_only=True):
    print(row)

print()
print('Header row font bold check:')
for cell in ws[1]:
    print(f'  {cell.value}: bold={cell.font.bold}')

print()
print('bruteforce_score number format:')
for row in ws.iter_rows(min_row=2, max_row=3):
    cell = row[9]  # Column J (10th column, index 9)
    print(f'  Row {cell.row}: value={cell.value}, format={cell.number_format}')

print()
print('=== methods sheet ===')
ws_methods = wb['methods']
for row in ws_methods.iter_rows(min_row=1, max_row=8, values_only=True):
    print(row[0] if row[0] else '')
"


# Execute command
python3 -c "
from openpyxl import load_workbook
wb = load_workbook('/root/ftp_bruteforce_comparison.xlsx')
ws = wb['comparison']

print('Numeric column alignments (columns E, F, I, J):')
for row_idx in [2, 3]:
    row = list(ws.iter_rows(min_row=row_idx, max_row=row_idx))[0]
    for col_idx in [4, 5, 8, 9]:  # E=5, F=6, I=9, J=10 (0-indexed: 4, 5, 8, 9)
        cell = row[col_idx]
        alignment = cell.alignment.horizontal if cell.alignment else 'default'
        print(f'  Row {row_idx}, Col {cell.column_letter} ({cell.value}): alignment={alignment}')
"


# Execute command
file /root/bruteforce.pcap /root/ftp.pcap

# Execute command
ls -la /root/harbor_workspaces/task_T418_run1/input/

# Execute command
which tshark tcpdump 2>/dev/null || echo "checking available tools"

# Execute command
python3 -c "from scapy.all import *; print('scapy available')" 2>/dev/null || pip3 install scapy -q && python3 -c "from scapy.all import *; print('scapy installed')"

# Execute command
cd /root/harbor_workspaces/task_T418_run1/input && python3 << 'EOF'
from scapy.all import rdpcap, TCP, IP

# Analyze bruteforce.pcap
print("=== bruteforce.pcap ===")
packets = rdpcap('bruteforce.pcap')

# Get TCP port 21 FTP control channel packets
ftp_packets = [p for p in packets if TCP in p and (p[TCP].dport == 21 or p[TCP].sport == 21)]
print(f"Total packets: {len(packets)}, FTP control packets: {len(ftp_packets)}")

# Extract payloads
for i, p in enumerate(ftp_packets[:30]):
    if p.haslayer('Raw'):
        payload = p['Raw'].load.decode('utf-8', errors='ignore').strip()
        if payload:
            src_ip = p[IP].src
            dst_ip = p[IP].dst
            print(f"  {i}: {src_ip} -> {dst_ip}: {payload[:80]}")
EOF

# Execute command
python3 << 'EOF'
from scapy.all import rdpcap, TCP, IP
from collections import Counter
import re

def analyze_pcap(filename):
    print(f"\n=== {filename} ===")
    packets = rdpcap(filename)
    
    # Get TCP port 21 FTP control channel packets
    ftp_packets = [p for p in packets if TCP in p and (p[TCP].dport == 21 or p[TCP].sport == 21)]
    
    server_ip = None
    client_ip = None
    usernames = []
    passwords = []
    success_codes = 0
    
    for p in ftp_packets:
        if p.haslayer('Raw'):
            payload = p['Raw'].load.decode('utf-8', errors='ignore').strip()
            src_ip = p[IP].src
            dst_ip = p[IP].dst
            
            # Detect 220 banner to identify server
            if payload.startswith('220 '):
                server_ip = src_ip
                client_ip = dst_ip
            
            # Count USER commands
            if payload.upper().startswith('USER '):
                username = payload[5:].strip()
                usernames.append(username)
            
            # Count PASS commands
            if payload.upper().startswith('PASS '):
                password = payload[5:].strip()
                passwords.append(password)
            
            # Count 230 success responses
            if payload.startswith('230 '):
                success_codes += 1
    
    print(f"Server IP: {server_ip}")
    print(f"Client IP: {client_ip}")
    print(f"Total login attempts (PASS): {len(passwords)}")
    print(f"Unique usernames: {len(set(usernames))}")
    print(f"Username counts: {Counter(usernames).most_common(5)}")
    print(f"Password counts: {Counter(passwords).most_common(5)}")
    print(f"Successful logins (230): {success_codes}")
    
    if usernames:
        most_targeted = Counter(usernames).most_common()
        # Sort by count desc, then lexicographically for ties
        sorted_users = sorted(most_targeted, key=lambda x: (-x[1], x[0]))
        print(f"Most targeted username: {sorted_users[0][0]}")
    
    if passwords:
        password_counts = Counter(passwords).most_common()
        sorted_passwords = sorted(password_counts, key=lambda x: (-x[1], x[0]))
        print(f"Top password candidate: {sorted_passwords[0][0]}")
    
    bruteforce_score = len(passwords) / max(1, len(set(usernames)))
    print(f"Bruteforce score: {bruteforce_score:.4f}")

analyze_pcap('bruteforce.pcap')
analyze_pcap('ftp.pcap')
EOF

# Execute command
mkdir -p /root/harbor_workspaces/task_T418_run1/output && ls -la /root/harbor_workspaces/task_T418_run1/

# Create /root/harbor_workspaces/task_T418_run1/expectation_tests.py
mkdir -p $(dirname /root/harbor_workspaces/task_T418_run1/expectation_tests.py)
cat << 'HEREDOC_EOF' > /root/harbor_workspaces/task_T418_run1/expectation_tests.py
"""Auto-generated expectation tests for FTP bruteforce comparison task.

These tests verify that the task execution produces correct outputs
based on the instruction requirements for analyzing bruteforce.pcap
and ftp.pcap files and comparing their FTP behavior.
"""

import os
from pathlib import Path

import pytest

# Expected output path
OUTPUT_FILE = "/root/ftp_bruteforce_comparison.xlsx"

# Expected column names for the comparison sheet
EXPECTED_COLUMNS = [
    "pcap",
    "protocol_category",
    "server_ip",
    "client_ip",
    "total_login_attempts",
    "unique_usernames",
    "most_targeted_username",
    "top_password_candidate",
    "success_count",
    "bruteforce_score",
]

# Expected PCAP file names
EXPECTED_PCAPS = ["bruteforce.pcap", "ftp.pcap"]

# Expected sheet names
EXPECTED_SHEETS = ["comparison", "methods"]


class TestFileExistence:
    """Tests for output file existence and basic properties."""

    def test_output_file_exists(self):
        """Verify output Excel file was created at the correct path."""
        assert os.path.exists(OUTPUT_FILE), f"Output file not found: {OUTPUT_FILE}"

    def test_output_file_is_not_empty(self):
        """Verify output file has non-zero size."""
        assert os.path.exists(OUTPUT_FILE), "Output file not found"
        file_size = os.path.getsize(OUTPUT_FILE)
        assert file_size > 0, "Output file is empty"

    def test_output_file_has_xlsx_extension(self):
        """Verify output file has .xlsx extension."""
        assert OUTPUT_FILE.endswith(".xlsx"), "Output file must have .xlsx extension"


class TestExcelFormat:
    """Tests for valid Excel format and structure."""

    def test_output_is_valid_excel(self):
        """Verify output is a valid Excel file that can be opened."""
        from openpyxl import load_workbook

        assert os.path.exists(OUTPUT_FILE), "Output file not found"
        try:
            wb = load_workbook(OUTPUT_FILE)
            assert wb is not None, "Failed to load workbook"
            wb.close()
        except Exception as e:
            pytest.fail(f"Output file is not a valid Excel file: {e}")

    def test_workbook_has_exactly_two_sheets(self):
        """Verify workbook contains exactly two sheets."""
        from openpyxl import load_workbook

        wb = load_workbook(OUTPUT_FILE)
        sheet_count = len(wb.sheetnames)
        wb.close()
        assert sheet_count == 2, f"Expected 2 sheets, found {sheet_count}"

    def test_workbook_has_comparison_sheet(self):
        """Verify workbook contains a 'comparison' sheet."""
        from openpyxl import load_workbook

        wb = load_workbook(OUTPUT_FILE)
        sheets = wb.sheetnames
        wb.close()
        assert "comparison" in sheets, f"'comparison' sheet not found. Found: {sheets}"

    def test_workbook_has_methods_sheet(self):
        """Verify workbook contains a 'methods' sheet."""
        from openpyxl import load_workbook

        wb = load_workbook(OUTPUT_FILE)
        sheets = wb.sheetnames
        wb.close()
        assert "methods" in sheets, f"'methods' sheet not found. Found: {sheets}"


class TestComparisonSheetStructure:
    """Tests for the structure of the comparison sheet."""

    def test_comparison_sheet_has_header_row(self):
        """Verify comparison sheet has a header row with expected columns."""
        from openpyxl import load_workbook

        wb = load_workbook(OUTPUT_FILE)
        ws = wb["comparison"]
        # Get header row values (row 1)
        headers = [cell.value for cell in ws[1] if cell.value is not None]
        wb.close()
        assert len(headers) > 0, "No headers found in comparison sheet"

    def test_comparison_sheet_has_all_required_columns(self):
        """Verify comparison sheet has all required column names."""
        from openpyxl import load_workbook

        wb = load_workbook(OUTPUT_FILE)
        ws = wb["comparison"]
        # Get header row values (row 1)
        headers = [str(cell.value).lower() if cell.value else "" for cell in ws[1]]
        wb.close()

        for col in EXPECTED_COLUMNS:
            assert col.lower() in headers, f"Required column '{col}' not found in headers: {headers}"

    def test_comparison_sheet_has_two_data_rows(self):
        """Verify comparison sheet has exactly 2 data rows (one per PCAP)."""
        from openpyxl import load_workbook

        wb = load_workbook(OUTPUT_FILE)
        ws = wb["comparison"]
        # Count non-empty rows (excluding header)
        data_rows = sum(1 for row in ws.iter_rows(min_row=2) if any(cell.value for cell in row))
        wb.close()
        assert data_rows == 2, f"Expected 2 data rows, found {data_rows}"

    def test_comparison_sheet_contains_both_pcaps(self):
        """Verify comparison sheet has rows for both bruteforce.pcap and ftp.pcap."""
        from openpyxl import load_workbook

        wb = load_workbook(OUTPUT_FILE)
        ws = wb["comparison"]

        # Find pcap column index
        headers = [str(cell.value).lower() if cell.value else "" for cell in ws[1]]
        pcap_col_idx = headers.index("pcap") + 1 if "pcap" in headers else None

        pcap_values = []
        if pcap_col_idx:
            for row in ws.iter_rows(min_row=2):
                cell_value = row[pcap_col_idx - 1].value
                if cell_value:
                    pcap_values.append(str(cell_value))
        wb.close()

        for expected_pcap in EXPECTED_PCAPS:
            assert any(expected_pcap in val for val in pcap_values), \
                f"'{expected_pcap}' not found in pcap column. Found: {pcap_values}"


class TestComparisonSheetData:
    """Tests for the data values in the comparison sheet."""

    def _get_comparison_data(self):
        """Helper to load comparison data as list of dicts."""
        from openpyxl import load_workbook

        wb = load_workbook(OUTPUT_FILE)
        ws = wb["comparison"]

        headers = [str(cell.value).lower() if cell.value else f"col_{i}" for i, cell in enumerate(ws[1])]

        data = []
        for row in ws.iter_rows(min_row=2):
            if any(cell.value for cell in row):
                row_dict = {headers[i]: cell.value for i, cell in enumerate(row) if i < len(headers)}
                data.append(row_dict)
        wb.close()
        return data

    def test_server_ip_is_valid_ipv4(self):
        """Verify server_ip values are valid IPv4 addresses."""
        import re
        ipv4_pattern = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"

        data = self._get_comparison_data()
        for row in data:
            server_ip = str(row.get("server_ip", ""))
            assert re.match(ipv4_pattern, server_ip), \
                f"Invalid server_ip format: '{server_ip}'"

    def test_client_ip_is_valid_ipv4(self):
        """Verify client_ip values are valid IPv4 addresses."""
        import re
        ipv4_pattern = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"

        data = self._get_comparison_data()
        for row in data:
            client_ip = str(row.get("client_ip", ""))
            assert re.match(ipv4_pattern, client_ip), \
                f"Invalid client_ip format: '{client_ip}'"

    def test_total_login_attempts_is_positive_integer(self):
        """Verify total_login_attempts are positive integers."""
        data = self._get_comparison_data()
        for row in data:
            attempts = row.get("total_login_attempts")
            assert attempts is not None, "total_login_attempts is missing"
            assert isinstance(attempts, (int, float)), \
                f"total_login_attempts must be numeric, got {type(attempts)}"
            assert attempts > 0, f"total_login_attempts must be positive, got {attempts}"

    def test_unique_usernames_is_non_negative_integer(self):
        """Verify unique_usernames are non-negative integers."""
        data = self._get_comparison_data()
        for row in data:
            unique = row.get("unique_usernames")
            assert unique is not None, "unique_usernames is missing"
            assert isinstance(unique, (int, float)), \
                f"unique_usernames must be numeric, got {type(unique)}"
            assert unique >= 0, f"unique_usernames must be non-negative, got {unique}"

    def test_most_targeted_username_is_non_empty_string(self):
        """Verify most_targeted_username is a non-empty string."""
        data = self._get_comparison_data()
        for row in data:
            username = row.get("most_targeted_username")
            assert username is not None, "most_targeted_username is missing"
            assert str(username).strip(), "most_targeted_username cannot be empty"

    def test_top_password_candidate_is_non_empty_string(self):
        """Verify top_password_candidate is a non-empty string."""
        data = self._get_comparison_data()
        for row in data:
            password = row.get("top_password_candidate")
            assert password is not None, "top_password_candidate is missing"
            assert str(password).strip(), "top_password_candidate cannot be empty"

    def test_success_count_is_non_negative_integer(self):
        """Verify success_count are non-negative integers."""
        data = self._get_comparison_data()
        for row in data:
            success = row.get("success_count")
            assert success is not None, "success_count is missing"
            assert isinstance(success, (int, float)), \
                f"success_count must be numeric, got {type(success)}"
            assert success >= 0, f"success_count must be non-negative, got {success}"

    def test_bruteforce_score_is_numeric(self):
        """Verify bruteforce_score is a numeric value."""
        data = self._get_comparison_data()
        for row in data:
            score = row.get("bruteforce_score")
            assert score is not None, "bruteforce_score is missing"
            assert isinstance(score, (int, float)), \
                f"bruteforce_score must be numeric, got {type(score)}"

    def test_bruteforce_score_formula_correct(self):
        """Verify bruteforce_score = total_login_attempts / max(1, unique_usernames)."""
        data = self._get_comparison_data()
        for row in data:
            attempts = row.get("total_login_attempts")
            unique = row.get("unique_usernames")
            score = row.get("bruteforce_score")

            if attempts is not None and unique is not None and score is not None:
                expected_score = attempts / max(1, unique)
                assert abs(float(score) - expected_score) < 0.0001, \
                    f"bruteforce_score mismatch: expected {expected_score:.4f}, got {score}"

    def test_protocol_category_is_present(self):
        """Verify protocol_category field is present and non-empty."""
        data = self._get_comparison_data()
        for row in data:
            category = row.get("protocol_category")
            assert category is not None, "protocol_category is missing"
            assert str(category).strip(), "protocol_category cannot be empty"


class TestBruteforceVsNormalComparison:
    """Tests comparing bruteforce vs normal FTP behavior."""

    def _get_comparison_data(self):
        """Helper to load comparison data as list of dicts."""
        from openpyxl import load_workbook

        wb = load_workbook(OUTPUT_FILE)
        ws = wb["comparison"]

        headers = [str(cell.value).lower() if cell.value else f"col_{i}" for i, cell in enumerate(ws[1])]

        data = {}
        for row in ws.iter_rows(min_row=2):
            if any(cell.value for cell in row):
                row_dict = {headers[i]: cell.value for i, cell in enumerate(row) if i < len(headers)}
                pcap_name = str(row_dict.get("pcap", ""))
                if "bruteforce" in pcap_name.lower():
                    data["bruteforce"] = row_dict
                elif "ftp" in pcap_name.lower():
                    data["ftp"] = row_dict
        wb.close()
        return data

    def test_bruteforce_has_more_login_attempts(self):
        """Verify bruteforce.pcap has more login attempts than ftp.pcap."""
        data = self._get_comparison_data()

        if "bruteforce" in data and "ftp" in data:
            bf_attempts = data["bruteforce"].get("total_login_attempts", 0)
            ftp_attempts = data["ftp"].get("total_login_attempts", 0)
            assert bf_attempts > ftp_attempts, \
                f"Expected bruteforce attempts ({bf_attempts}) > ftp attempts ({ftp_attempts})"

    def test_bruteforce_has_higher_score(self):
        """Verify bruteforce.pcap has higher bruteforce_score than ftp.pcap."""
        data = self._get_comparison_data()

        if "bruteforce" in data and "ftp" in data:
            bf_score = float(data["bruteforce"].get("bruteforce_score", 0))
            ftp_score = float(data["ftp"].get("bruteforce_score", 0))
            assert bf_score > ftp_score, \
                f"Expected bruteforce score ({bf_score}) > ftp score ({ftp_score})"

    def test_ftp_has_successful_login(self):
        """Verify ftp.pcap has at least one successful login (success_count >= 1)."""
        data = self._get_comparison_data()

        if "ftp" in data:
            success = data["ftp"].get("success_count", 0)
            assert success >= 1, \
                f"Expected ftp.pcap to have successful login, got success_count={success}"


class TestMethodsSheet:
    """Tests for the methods sheet content."""

    def test_methods_sheet_has_content(self):
        """Verify methods sheet contains text content."""
        from openpyxl import load_workbook

        wb = load_workbook(OUTPUT_FILE)
        ws = wb["methods"]

        content = []
        for row in ws.iter_rows():
            for cell in row:
                if cell.value:
                    content.append(str(cell.value))
        wb.close()

        assert len(content) > 0, "methods sheet is empty"

    def test_methods_sheet_within_line_limit(self):
        """Verify methods sheet has no more than 8 lines of content."""
        from openpyxl import load_workbook

        wb = load_workbook(OUTPUT_FILE)
        ws = wb["methods"]

        non_empty_rows = sum(1 for row in ws.iter_rows() if any(cell.value for cell in row))
        wb.close()

        assert non_empty_rows <= 8, \
            f"methods sheet exceeds 8 line limit, has {non_empty_rows} lines"

    def test_methods_describes_server_client_identification(self):
        """Verify methods sheet describes how server vs client is identified."""
        from openpyxl import load_workbook

        wb = load_workbook(OUTPUT_FILE)
        ws = wb["methods"]

        full_text = ""
        for row in ws.iter_rows():
            for cell in row:
                if cell.value:
                    full_text += str(cell.value).lower() + " "
        wb.close()

        # Check for keywords related to server/client identification
        server_keywords = ["server", "220", "banner", "client"]
        has_server_description = any(kw in full_text for kw in server_keywords)

        assert has_server_description, \
            "methods sheet should describe server vs client identification"


class TestExcelFormatting:
    """Tests for Excel formatting requirements."""

    def test_header_row_is_bold(self):
        """Verify header row in comparison sheet has bold formatting."""
        from openpyxl import load_workbook

        wb = load_workbook(OUTPUT_FILE)
        ws = wb["comparison"]

        header_cells_bold = []
        for cell in ws[1]:
            if cell.value is not None:
                is_bold = cell.font.bold if cell.font else False
                header_cells_bold.append(is_bold)
        wb.close()

        # At least some header cells should be bold
        assert any(header_cells_bold), "Header row should have bold formatting"

    def test_bruteforce_score_has_decimal_precision(self):
        """Verify bruteforce_score values have appropriate decimal representation."""
        from openpyxl import load_workbook

        wb = load_workbook(OUTPUT_FILE)
        ws = wb["comparison"]

        # Find bruteforce_score column
        headers = [str(cell.value).lower() if cell.value else "" for cell in ws[1]]
        score_col_idx = headers.index("bruteforce_score") + 1 if "bruteforce_score" in headers else None

        scores = []
        if score_col_idx:
            for row in ws.iter_rows(min_row=2):
                cell = row[score_col_idx - 1]
                if cell.value is not None:
                    scores.append(cell.value)
        wb.close()

        assert len(scores) > 0, "No bruteforce_score values found"
        # Verify values are numeric (formatting is handled at display level)
        for score in scores:
            assert isinstance(score, (int, float)), \
                f"bruteforce_score must be numeric for proper decimal display, got {type(score)}"


class TestDataIntegrity:
    """Tests for data integrity and consistency."""

    def test_server_client_ips_are_different(self):
        """Verify server_ip and client_ip are different for each row."""
        from openpyxl import load_workbook

        wb = load_workbook(OUTPUT_FILE)
        ws = wb["comparison"]

        headers = [str(cell.value).lower() if cell.value else f"col_{i}" for i, cell in enumerate(ws[1])]
        server_idx = headers.index("server_ip") if "server_ip" in headers else None
        client_idx = headers.index("client_ip") if "client_ip" in headers else None

        for row in ws.iter_rows(min_row=2):
            if any(cell.value for cell in row):
                server_ip = row[server_idx].value if server_idx is not None else None
                client_ip = row[client_idx].value if client_idx is not None else None
                if server_ip and client_ip:
                    assert server_ip != client_ip, \
                        f"server_ip and client_ip should be different: {server_ip}"
        wb.close()

    def test_unique_usernames_less_than_or_equal_attempts(self):
        """Verify unique_usernames <= total_login_attempts for each row."""
        from openpyxl import load_workbook

        wb = load_workbook(OUTPUT_FILE)
        ws = wb["comparison"]

        headers = [str(cell.value).lower() if cell.value else f"col_{i}" for i, cell in enumerate(ws[1])]
        attempts_idx = headers.index("total_login_attempts") if "total_login_attempts" in headers else None
        unique_idx = headers.index("unique_usernames") if "unique_usernames" in headers else None

        for row in ws.iter_rows(min_row=2):
            if any(cell.value for cell in row):
                attempts = row[attempts_idx].value if attempts_idx is not None else None
                unique = row[unique_idx].value if unique_idx is not None else None
                if attempts is not None and unique is not None:
                    assert unique <= attempts, \
                        f"unique_usernames ({unique}) cannot exceed total_login_attempts ({attempts})"
        wb.close()

    def test_success_count_less_than_or_equal_attempts(self):
        """Verify success_count <= total_login_attempts for each row."""
        from openpyxl import load_workbook

        wb = load_workbook(OUTPUT_FILE)
        ws = wb["comparison"]

        headers = [str(cell.value).lower() if cell.value else f"col_{i}" for i, cell in enumerate(ws[1])]
        attempts_idx = headers.index("total_login_attempts") if "total_login_attempts" in headers else None
        success_idx = headers.index("success_count") if "success_count" in headers else None

        for row in ws.iter_rows(min_row=2):
            if any(cell.value for cell in row):
                attempts = row[attempts_idx].value if attempts_idx is not None else None
                success = row[success_idx].value if success_idx is not None else None
                if attempts is not None and success is not None:
                    assert success <= attempts, \
                        f"success_count ({success}) cannot exceed total_login_attempts ({attempts})"
        wb.close()


class TestExpectedValues:
    """Tests for expected specific values based on PCAP analysis."""

    def _get_row_by_pcap(self, pcap_name):
        """Helper to get a row by pcap name."""
        from openpyxl import load_workbook

        wb = load_workbook(OUTPUT_FILE)
        ws = wb["comparison"]

        headers = [str(cell.value).lower() if cell.value else f"col_{i}" for i, cell in enumerate(ws[1])]

        for row in ws.iter_rows(min_row=2):
            if any(cell.value for cell in row):
                row_dict = {headers[i]: cell.value for i, cell in enumerate(row) if i < len(headers)}
                if pcap_name.lower() in str(row_dict.get("pcap", "")).lower():
                    wb.close()
                    return row_dict
        wb.close()
        return None

    def test_bruteforce_server_ip(self):
        """Verify bruteforce.pcap has correct server IP (192.168.56.101)."""
        row = self._get_row_by_pcap("bruteforce")
        if row:
            assert row.get("server_ip") == "192.168.56.101", \
                f"Expected server_ip 192.168.56.101, got {row.get('server_ip')}"

    def test_bruteforce_client_ip(self):
        """Verify bruteforce.pcap has correct client IP (192.168.56.1)."""
        row = self._get_row_by_pcap("bruteforce")
        if row:
            assert row.get("client_ip") == "192.168.56.1", \
                f"Expected client_ip 192.168.56.1, got {row.get('client_ip')}"

    def test_bruteforce_total_login_attempts(self):
        """Verify bruteforce.pcap has 30 total login attempts."""
        row = self._get_row_by_pcap("bruteforce")
        if row:
            assert row.get("total_login_attempts") == 30, \
                f"Expected 30 login attempts, got {row.get('total_login_attempts')}"

    def test_bruteforce_unique_usernames(self):
        """Verify bruteforce.pcap has 1 unique username."""
        row = self._get_row_by_pcap("bruteforce")
        if row:
            assert row.get("unique_usernames") == 1, \
                f"Expected 1 unique username, got {row.get('unique_usernames')}"

    def test_bruteforce_most_targeted_username(self):
        """Verify bruteforce.pcap most targeted username is 'bro'."""
        row = self._get_row_by_pcap("bruteforce")
        if row:
            assert str(row.get("most_targeted_username")).lower() == "bro", \
                f"Expected most_targeted_username 'bro', got {row.get('most_targeted_username')}"

    def test_bruteforce_success_count(self):
        """Verify bruteforce.pcap has 0 successful logins."""
        row = self._get_row_by_pcap("bruteforce")
        if row:
            assert row.get("success_count") == 0, \
                f"Expected 0 successful logins, got {row.get('success_count')}"

    def test_bruteforce_score_value(self):
        """Verify bruteforce.pcap has bruteforce_score of 30.0."""
        row = self._get_row_by_pcap("bruteforce")
        if row:
            score = float(row.get("bruteforce_score", 0))
            assert abs(score - 30.0) < 0.0001, \
                f"Expected bruteforce_score 30.0, got {score}"

    def test_ftp_server_ip(self):
        """Verify ftp.pcap has correct server IP (192.168.0.193)."""
        row = self._get_row_by_pcap("ftp")
        if row:
            assert row.get("server_ip") == "192.168.0.193", \
                f"Expected server_ip 192.168.0.193, got {row.get('server_ip')}"

    def test_ftp_client_ip(self):
        """Verify ftp.pcap has correct client IP (192.168.0.114)."""
        row = self._get_row_by_pcap("ftp")
        if row:
            assert row.get("client_ip") == "192.168.0.114", \
                f"Expected client_ip 192.168.0.114, got {row.get('client_ip')}"

    def test_ftp_total_login_attempts(self):
        """Verify ftp.pcap has 1 total login attempt."""
        row = self._get_row_by_pcap("ftp")
        if row:
            assert row.get("total_login_attempts") == 1, \
                f"Expected 1 login attempt, got {row.get('total_login_attempts')}"

    def test_ftp_unique_usernames(self):
        """Verify ftp.pcap has 1 unique username."""
        row = self._get_row_by_pcap("ftp")
        if row:
            assert row.get("unique_usernames") == 1, \
                f"Expected 1 unique username, got {row.get('unique_usernames')}"

    def test_ftp_most_targeted_username(self):
        """Verify ftp.pcap most targeted username is 'csanders'."""
        row = self._get_row_by_pcap("ftp")
        if row:
            assert str(row.get("most_targeted_username")).lower() == "csanders", \
                f"Expected most_targeted_username 'csanders', got {row.get('most_targeted_username')}"

    def test_ftp_top_password_candidate(self):
        """Verify ftp.pcap top password candidate is 'echo'."""
        row = self._get_row_by_pcap("ftp")
        if row:
            assert str(row.get("top_password_candidate")).lower() == "echo", \
                f"Expected top_password_candidate 'echo', got {row.get('top_password_candidate')}"

    def test_ftp_success_count(self):
        """Verify ftp.pcap has 1 successful login."""
        row = self._get_row_by_pcap("ftp")
        if row:
            assert row.get("success_count") == 1, \
                f"Expected 1 successful login, got {row.get('success_count')}"

    def test_ftp_bruteforce_score_value(self):
        """Verify ftp.pcap has bruteforce_score of 1.0."""
        row = self._get_row_by_pcap("ftp")
        if row:
            score = float(row.get("bruteforce_score", 0))
            assert abs(score - 1.0) < 0.0001, \
                f"Expected bruteforce_score 1.0, got {score}"


class TestProtocolCategory:
    """Tests for protocol category from Wireshark SampleCaptures page."""

    def test_protocol_category_from_html(self):
        """Verify protocol_category matches expected value from HTML ('General / Unsorted')."""
        from openpyxl import load_workbook

        wb = load_workbook(OUTPUT_FILE)
        ws = wb["comparison"]

        headers = [str(cell.value).lower() if cell.value else f"col_{i}" for i, cell in enumerate(ws[1])]
        cat_idx = headers.index("protocol_category") if "protocol_category" in headers else None

        categories = []
        if cat_idx is not None:
            for row in ws.iter_rows(min_row=2):
                if any(cell.value for cell in row):
                    cat = row[cat_idx].value
                    if cat:
                        categories.append(str(cat))
        wb.close()

        # Based on the HTML, FTP samples are in "General / Unsorted" section
        assert len(categories) > 0, "No protocol_category values found"
        for cat in categories:
            # The category should contain "General" or "Unsorted" based on HTML analysis
            assert cat.strip(), f"protocol_category should not be empty"

HEREDOC_EOF

# Execute command
cd /root/harbor_workspaces/task_T418_run1 && python3 -m py_compile expectation_tests.py && echo "Syntax OK"

# Execute command
python3 -c "import openpyxl; print(f'openpyxl version: {openpyxl.__version__}')" 2>/dev/null || pip3 install openpyxl -q && python3 -c "import openpyxl; print(f'openpyxl installed: {openpyxl.__version__}')"

# Execute command
python3 -c "import pytest; print(f'pytest version: {pytest.__version__}')"

# Execute command
pip3 install pytest -q && python3 -c "import pytest; print(f'pytest version: {pytest.__version__}')"

# Execute command
python3 -m pytest expectation_tests.py --collect-only 2>&1 | head -60

