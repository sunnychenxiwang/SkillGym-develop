#!/bin/bash
# solve.sh - Recreates the critical bus analysis output files
# This script parses MATPOWER case files, computes articulation points using NetworkX,
# and generates an Excel report with critical bus information.

set -e

# HARBOR_PATH_FIX_START
BASE_FIX="/root/harbor_workspaces/task_T228_run1"
mkdir -p "$BASE_FIX/input" "$BASE_FIX/output"
if [ ! -e "$BASE_FIX/input/case57.m" ] && [ -e "/root/case57.m" ]; then cp -f "/root/case57.m" "$BASE_FIX/input/case57.m"; fi
if [ ! -e "$BASE_FIX/input/case118.m" ] && [ -e "/root/case118.m" ]; then cp -f "/root/case118.m" "$BASE_FIX/input/case118.m"; fi
if [ ! -e "$BASE_FIX/input/pglib_opf_case118_ieee.m" ] && [ -e "/root/pglib_opf_case118_ieee.m" ]; then cp -f "/root/pglib_opf_case118_ieee.m" "$BASE_FIX/input/pglib_opf_case118_ieee.m"; fi
# HARBOR_PATH_FIX_END

cd /root/harbor_workspaces/task_T228_run1

# Create output directory
mkdir -p output

# Create analyze_critical_buses.py
cat > analyze_critical_buses.py << 'PYTHON_SCRIPT_1'
import re
import networkx as nx
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

def parse_matpower_file(filepath):
    """Parse a MATPOWER case file and extract bus IDs and branch data."""
    with open(filepath, 'r') as f:
        content = f.read()

    # Extract bus data
    bus_match = re.search(r'mpc\.bus\s*=\s*\[(.*?)\];', content, re.DOTALL)
    bus_ids = []
    if bus_match:
        bus_data = bus_match.group(1)
        for line in bus_data.strip().split('\n'):
            line = re.sub(r'%.*', '', line).strip()
            if line and not line.startswith('%'):
                parts = line.rstrip(';').split()
                if parts:
                    try:
                        bus_ids.append(int(float(parts[0])))
                    except ValueError:
                        continue

    # Extract branch data
    branch_match = re.search(r'mpc\.branch\s*=\s*\[(.*?)\];', content, re.DOTALL)
    branches = []
    if branch_match:
        branch_data = branch_match.group(1)
        for line in branch_data.strip().split('\n'):
            line = re.sub(r'%.*', '', line).strip()
            if line and not line.startswith('%'):
                parts = line.rstrip(';').split()
                if len(parts) >= 11:
                    try:
                        fbus = int(float(parts[0]))
                        tbus = int(float(parts[1]))
                        status = int(float(parts[10]))
                        branches.append((fbus, tbus, status))
                    except ValueError:
                        continue

    return bus_ids, branches

def build_graph(bus_ids, branches):
    """Build a NetworkX undirected graph from bus IDs and in-service branches."""
    G = nx.Graph()
    G.add_nodes_from(bus_ids)

    in_service_edges = set()
    for fbus, tbus, status in branches:
        if status == 1:
            edge = (min(fbus, tbus), max(fbus, tbus))
            in_service_edges.add(edge)

    G.add_edges_from(in_service_edges)
    return G, len(in_service_edges)

def find_articulation_data(G):
    """Find articulation points and compute components after removal."""
    baseline_components = len(list(nx.connected_components(G)))
    betweenness = nx.betweenness_centrality(G)

    articulation_points = list(nx.articulation_points(G))
    art_data = []

    for v in articulation_points:
        H = G.copy()
        H.remove_node(v)
        k_v = len(list(nx.connected_components(H)))
        art_data.append({
            'bus': v,
            'components_after_removal': k_v,
            'betweenness': betweenness[v],
            'degree': G.degree(v)
        })

    # Sort: max k_v, then max betweenness, then min bus number
    art_data.sort(key=lambda r: (-r['components_after_removal'], -r['betweenness'], r['bus']))
    return art_data, betweenness

def analyze_case(filepath, case_name):
    """Analyze a single MATPOWER case file."""
    bus_ids, branches = parse_matpower_file(filepath)
    G, n_branches_in_service = build_graph(bus_ids, branches)
    art_data, betweenness = find_articulation_data(G)

    critical_bus = art_data[0]['bus'] if art_data else None
    critical_k = art_data[0]['components_after_removal'] if art_data else 0
    critical_bet = art_data[0]['betweenness'] if art_data else 0.0

    return {
        'case_name': case_name,
        'n_buses': G.number_of_nodes(),
        'n_branches_in_service': n_branches_in_service,
        'critical_bus': critical_bus,
        'components_after_removal': critical_k,
        'betweenness': critical_bet,
        'top_articulation_points': art_data[:10]
    }

def create_excel_report(results, output_path):
    """Create the Excel report with proper formatting."""
    wb = Workbook()

    header_font = Font(bold=True, color='000000')
    header_fill = PatternFill('solid', fgColor='D9D9D9')
    black_font = Font(color='000000')

    # Summary sheet
    ws = wb.active
    ws.title = 'Summary'

    summary_headers = ['case_name', 'n_buses', 'n_branches_in_service', 'critical_bus',
                       'components_after_removal', 'betweenness']
    for col, header in enumerate(summary_headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.font = header_font
        cell.fill = header_fill

    for row_idx, result in enumerate(results, 2):
        ws.cell(row=row_idx, column=1, value=result['case_name']).font = black_font
        ws.cell(row=row_idx, column=2, value=result['n_buses']).font = black_font
        ws.cell(row=row_idx, column=2).number_format = '0'
        ws.cell(row=row_idx, column=3, value=result['n_branches_in_service']).font = black_font
        ws.cell(row=row_idx, column=3).number_format = '0'
        ws.cell(row=row_idx, column=4, value=result['critical_bus']).font = black_font
        ws.cell(row=row_idx, column=4).number_format = '0'
        ws.cell(row=row_idx, column=5, value=result['components_after_removal']).font = black_font
        ws.cell(row=row_idx, column=5).number_format = '0'
        ws.cell(row=row_idx, column=6, value=result['betweenness']).font = black_font
        ws.cell(row=row_idx, column=6).number_format = '0.000000'

    ws.freeze_panes = 'A2'

    # Details sheet
    ws2 = wb.create_sheet('Details')

    details_headers = ['case_name', 'bus', 'components_after_removal', 'betweenness', 'degree']
    for col, header in enumerate(details_headers, 1):
        cell = ws2.cell(row=1, column=col, value=header)
        cell.font = header_font
        cell.fill = header_fill

    row_idx = 2
    for result in results:
        for art in result['top_articulation_points']:
            ws2.cell(row=row_idx, column=1, value=result['case_name']).font = black_font
            ws2.cell(row=row_idx, column=2, value=art['bus']).font = black_font
            ws2.cell(row=row_idx, column=2).number_format = '0'
            ws2.cell(row=row_idx, column=3, value=art['components_after_removal']).font = black_font
            ws2.cell(row=row_idx, column=3).number_format = '0'
            ws2.cell(row=row_idx, column=4, value=art['betweenness']).font = black_font
            ws2.cell(row=row_idx, column=4).number_format = '0.000000'
            ws2.cell(row=row_idx, column=5, value=art['degree']).font = black_font
            ws2.cell(row=row_idx, column=5).number_format = '0'
            row_idx += 1

    ws2.freeze_panes = 'A2'

    wb.save(output_path)

def main():
    cases = [
        ('/root/harbor_workspaces/task_T228_run1/input/case57.m', 'case57'),
        ('/root/harbor_workspaces/task_T228_run1/input/case118.m', 'case118'),
        ('/root/harbor_workspaces/task_T228_run1/input/pglib_opf_case118_ieee.m', 'pglib_opf_case118_ieee')
    ]

    results = []
    for filepath, case_name in cases:
        result = analyze_case(filepath, case_name)
        results.append(result)
        print(f"{case_name}: n_buses={result['n_buses']}, n_branches={result['n_branches_in_service']}, "
              f"critical_bus={result['critical_bus']}, k={result['components_after_removal']}, "
              f"betweenness={result['betweenness']:.6f}")

    output_path = '/root/harbor_workspaces/task_T228_run1/output/critical_bus_report.xlsx'
    create_excel_report(results, output_path)
    print(f"\nExcel report saved to: {output_path}")

if __name__ == '__main__':
    main()
PYTHON_SCRIPT_1

# Create analyze_networks.py
cat > analyze_networks.py << 'PYTHON_SCRIPT_2'
#!/usr/bin/env python3
"""
Analyze MATPOWER case files to find critical buses using NetworkX.
"""

import re
import networkx as nx
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter

def parse_matpower_file(filepath):
    """Parse a MATPOWER case file and extract bus IDs and branch data."""
    with open(filepath, 'r') as f:
        content = f.read()

    # Extract bus matrix
    bus_match = re.search(r'mpc\.bus\s*=\s*\[\s*(.*?)\];', content, re.DOTALL)
    if not bus_match:
        raise ValueError(f"Could not find mpc.bus in {filepath}")

    bus_text = bus_match.group(1)
    bus_ids = []
    for line in bus_text.split('\n'):
        # Remove comments
        line = re.sub(r'%.*', '', line).strip()
        if not line:
            continue
        # Split by semicolon to get rows
        for row_str in line.split(';'):
            row_str = row_str.strip()
            if not row_str:
                continue
            parts = row_str.split()
            if len(parts) >= 1:
                try:
                    bus_id = int(float(parts[0]))
                    bus_ids.append(bus_id)
                except ValueError:
                    continue

    # Extract branch matrix
    branch_match = re.search(r'mpc\.branch\s*=\s*\[\s*(.*?)\];', content, re.DOTALL)
    if not branch_match:
        raise ValueError(f"Could not find mpc.branch in {filepath}")

    branch_text = branch_match.group(1)
    branches = []  # List of (fbus, tbus, status)
    for line in branch_text.split('\n'):
        # Remove comments
        line = re.sub(r'%.*', '', line).strip()
        if not line:
            continue
        # Split by semicolon to get rows
        for row_str in line.split(';'):
            row_str = row_str.strip()
            if not row_str:
                continue
            parts = row_str.split()
            if len(parts) >= 11:
                try:
                    fbus = int(float(parts[0]))
                    tbus = int(float(parts[1]))
                    status = int(float(parts[10]))  # Column 11 (0-indexed: 10)
                    branches.append((fbus, tbus, status))
                except ValueError:
                    continue

    return bus_ids, branches


def analyze_case(filepath, case_name):
    """Analyze a single MATPOWER case file."""
    bus_ids, branches = parse_matpower_file(filepath)

    n_buses = len(bus_ids)

    # Count in-service branches (raw count, including parallel lines)
    in_service_branches = [(f, t) for f, t, s in branches if s == 1]
    n_branches_in_service = len(in_service_branches)

    # Build NetworkX graph (parallel edges will be collapsed since nx.Graph is simple)
    G = nx.Graph()
    G.add_nodes_from(bus_ids)
    G.add_edges_from(in_service_branches)

    # Compute betweenness centrality on original graph
    betweenness = nx.betweenness_centrality(G)

    # Get baseline number of components
    baseline_components = len(list(nx.connected_components(G)))

    # Find articulation points
    articulation_points = list(nx.articulation_points(G))

    # For each articulation point, compute components after removal
    art_data = []
    for v in articulation_points:
        H = G.copy()
        H.remove_node(v)
        k_v = len(list(nx.connected_components(H)))
        art_data.append({
            'bus': v,
            'components_after_removal': k_v,
            'betweenness': betweenness[v],
            'degree': G.degree(v)
        })

    # Sort by: max k_v (descending), max betweenness (descending), min bus (ascending)
    art_data.sort(key=lambda r: (-r['components_after_removal'], -r['betweenness'], r['bus']))

    # Select the critical bus (first in sorted list)
    if art_data:
        critical_bus = art_data[0]['bus']
        critical_k_v = art_data[0]['components_after_removal']
        critical_betweenness = art_data[0]['betweenness']
    else:
        # No articulation points - select bus with highest betweenness, then smallest ID
        sorted_buses = sorted(bus_ids, key=lambda b: (-betweenness[b], b))
        critical_bus = sorted_buses[0] if sorted_buses else None
        critical_k_v = baseline_components  # No change in components
        critical_betweenness = betweenness.get(critical_bus, 0)

    # Get top 10 articulation points
    top_10 = art_data[:10]

    return {
        'case_name': case_name,
        'n_buses': n_buses,
        'n_branches_in_service': n_branches_in_service,
        'critical_bus': critical_bus,
        'components_after_removal': critical_k_v,
        'betweenness': critical_betweenness,
        'top_10_articulation': top_10
    }


def create_excel_report(results, output_path):
    """Create the Excel report with required formatting."""
    wb = Workbook()

    # Summary sheet
    ws_summary = wb.active
    ws_summary.title = "Summary"

    # Header style
    header_font = Font(bold=True, color='000000')
    header_fill = PatternFill('solid', start_color='D9D9D9', end_color='D9D9D9')

    # Summary headers
    summary_headers = ['case_name', 'n_buses', 'n_branches_in_service', 'critical_bus',
                       'components_after_removal', 'betweenness']
    for col, header in enumerate(summary_headers, 1):
        cell = ws_summary.cell(row=1, column=col, value=header)
        cell.font = header_font
        cell.fill = header_fill

    # Summary data
    for row_idx, result in enumerate(results, 2):
        ws_summary.cell(row=row_idx, column=1, value=result['case_name'])
        ws_summary.cell(row=row_idx, column=2, value=result['n_buses'])
        ws_summary.cell(row=row_idx, column=3, value=result['n_branches_in_service'])
        ws_summary.cell(row=row_idx, column=4, value=result['critical_bus'])
        ws_summary.cell(row=row_idx, column=5, value=result['components_after_removal'])
        cell = ws_summary.cell(row=row_idx, column=6, value=result['betweenness'])
        cell.number_format = '0.000000'

    # Apply number formats to columns
    for row in range(2, len(results) + 2):
        for col in [2, 3, 4, 5]:  # Integer columns
            ws_summary.cell(row=row, column=col).number_format = '0'

    # Freeze panes
    ws_summary.freeze_panes = 'A2'

    # Details sheet
    ws_details = wb.create_sheet("Details")

    # Details headers
    details_headers = ['case_name', 'bus', 'components_after_removal', 'betweenness', 'degree']
    for col, header in enumerate(details_headers, 1):
        cell = ws_details.cell(row=1, column=col, value=header)
        cell.font = header_font
        cell.fill = header_fill

    # Details data
    row_idx = 2
    for result in results:
        for art in result['top_10_articulation']:
            ws_details.cell(row=row_idx, column=1, value=result['case_name'])
            ws_details.cell(row=row_idx, column=2, value=art['bus'])
            ws_details.cell(row=row_idx, column=3, value=art['components_after_removal'])
            cell = ws_details.cell(row=row_idx, column=4, value=art['betweenness'])
            cell.number_format = '0.000000'
            ws_details.cell(row=row_idx, column=5, value=art['degree'])
            row_idx += 1

    # Apply integer format to columns
    for row in range(2, row_idx):
        for col in [2, 3, 5]:  # Integer columns
            ws_details.cell(row=row, column=col).number_format = '0'

    # Freeze panes
    ws_details.freeze_panes = 'A2'

    # Save workbook
    wb.save(output_path)
    print(f"Report saved to: {output_path}")


def main():
    base_path = '/root/harbor_workspaces/task_T228_run1/input'

    # Process each case file
    cases = [
        (f'{base_path}/case57.m', 'case57'),
        (f'{base_path}/case118.m', 'case118'),
        (f'{base_path}/pglib_opf_case118_ieee.m', 'pglib_opf_case118_ieee'),
    ]

    results = []
    for filepath, case_name in cases:
        print(f"\nAnalyzing {case_name}...")
        result = analyze_case(filepath, case_name)
        results.append(result)

        print(f"  n_buses: {result['n_buses']}")
        print(f"  n_branches_in_service: {result['n_branches_in_service']}")
        print(f"  critical_bus: {result['critical_bus']}")
        print(f"  components_after_removal: {result['components_after_removal']}")
        print(f"  betweenness: {result['betweenness']:.6f}")
        print(f"  Number of articulation points: {len(result['top_10_articulation'])}")

    # Create Excel report
    output_path = '/root/harbor_workspaces/task_T228_run1/output/critical_bus_report.xlsx'
    create_excel_report(results, output_path)


if __name__ == '__main__':
    main()
PYTHON_SCRIPT_2

# Create expectation_tests.py
cat > expectation_tests.py << 'PYTHON_SCRIPT_3'
"""Auto-generated expectation tests for critical bus report task verification.

These tests verify that the task execution produces correct outputs
based on the instruction requirements for parsing MATPOWER files,
computing articulation points, and generating an Excel report.
"""

import os
import re
from pathlib import Path

import networkx as nx
import pytest

# Expected output path
OUTPUT_FILE = "/root/harbor_workspaces/task_T228_run1/output/critical_bus_report.xlsx"

# Input file paths
INPUT_DIR = "/root/harbor_workspaces/task_T228_run1/input"
MATPOWER_FILES = {
    "case57": os.path.join(INPUT_DIR, "case57.m"),
    "case118": os.path.join(INPUT_DIR, "case118.m"),
    "pglib_opf_case118_ieee": os.path.join(INPUT_DIR, "pglib_opf_case118_ieee.m"),
}

CASE_ORDER = ["case57", "case118", "pglib_opf_case118_ieee"]

# Expected column names and order for each sheet
SUMMARY_COLUMNS = [
    "case_name",
    "n_buses",
    "n_branches_in_service",
    "critical_bus",
    "components_after_removal",
    "betweenness",
]

DETAILS_COLUMNS = [
    "case_name",
    "bus",
    "components_after_removal",
    "betweenness",
    "degree",
]

# Light gray fill colors that are acceptable (ARGB format)
# Only accept light grays with R/G/B >= 0xB0 (176)
ACCEPTABLE_LIGHT_GRAY_FILLS = [
    "FFD3D3D3",  # Light gray (211, 211, 211)
    "FFC0C0C0",  # Silver (192, 192, 192)
    "FFD9D9D9",  # Slightly lighter gray (217, 217, 217)
    "FFE0E0E0",  # Very light gray (224, 224, 224)
    "FFCCCCCC",  # Medium light gray (204, 204, 204)
    "FFBFBFBF",  # Common Excel gray (191, 191, 191)
    "FFB0B0B0",  # Light gray threshold (176, 176, 176)
    "FFE6E6E6",  # Excel default light gray
    "FFF0F0F0",  # Very light gray
    "FFDDDDDD",  # Light gray
]

# Minimum brightness threshold for light gray (R/G/B must be >= this value)
MIN_LIGHT_GRAY_BRIGHTNESS = 0xB0  # 176


def parse_matpower_file(filepath):
    """Parse a MATPOWER file and extract bus and branch data.

    Uses robust tokenization that handles multi-row entries and validates bus IDs.

    Returns:
        dict with keys:
            - n_buses: number of buses
            - bus_ids: set of unique bus IDs
            - branches: list of (from_bus, to_bus, status) tuples
            - n_branches_in_service: count of in-service branches
    """
    with open(filepath, 'r') as f:
        content = f.read()

    # Extract bus matrix block
    bus_match = re.search(r'mpc\.bus\s*=\s*\[(.*?)\];', content, re.DOTALL)
    bus_ids = set()
    if bus_match:
        bus_block = bus_match.group(1)
        # Remove comments (lines starting with % or inline comments)
        bus_block = re.sub(r'%.*$', '', bus_block, flags=re.MULTILINE)
        # Tokenize: split on whitespace and semicolons, parse numeric values
        tokens = re.findall(r'-?\d+\.?\d*(?:[eE][+-]?\d+)?', bus_block)
        # Each bus row has 13 columns, first column is bus_id
        if tokens:
            # Group into rows of 13 values
            num_cols = 13
            for i in range(0, len(tokens), num_cols):
                if i + num_cols <= len(tokens):
                    bus_id = int(float(tokens[i]))
                    bus_ids.add(bus_id)

    n_buses = len(bus_ids)

    # Extract branch data
    branch_match = re.search(r'mpc\.branch\s*=\s*\[(.*?)\];', content, re.DOTALL)
    branches = []
    if branch_match:
        branch_block = branch_match.group(1)
        # Remove comments
        branch_block = re.sub(r'%.*$', '', branch_block, flags=re.MULTILINE)
        # Tokenize numeric values
        tokens = re.findall(r'-?\d+\.?\d*(?:[eE][+-]?\d+)?', branch_block)
        # Each branch row has at least 11 columns (could have more for extended format)
        # Minimum columns: fbus, tbus, r, x, b, rateA, rateB, rateC, ratio, angle, status
        # We look for rows with at least 11 values
        num_cols = 13  # Standard MATPOWER branch has 13 columns
        for i in range(0, len(tokens), num_cols):
            if i + 11 <= len(tokens):
                from_bus = int(float(tokens[i]))
                to_bus = int(float(tokens[i + 1]))
                status = int(float(tokens[i + 10]))
                branches.append((from_bus, to_bus, status))

    in_service_branches = [(f, t) for f, t, s in branches if s == 1]

    return {
        'n_buses': n_buses,
        'bus_ids': bus_ids,
        'branches': branches,
        'n_branches_in_service': len(in_service_branches),
        'in_service_edges': in_service_branches,
    }


def build_graph_from_matpower(filepath):
    """Build a NetworkX graph from in-service branches in a MATPOWER file."""
    data = parse_matpower_file(filepath)
    G = nx.Graph()

    # Add all buses as nodes using actual bus IDs
    for bus_id in data['bus_ids']:
        G.add_node(bus_id)

    # Add in-service branches as edges
    for from_bus, to_bus in data['in_service_edges']:
        G.add_edge(from_bus, to_bus)

    return G, data


def compute_expected_values(filepath):
    """Compute expected articulation points and metrics for a MATPOWER file."""
    G, data = build_graph_from_matpower(filepath)

    # Find articulation points
    articulation_points = set(nx.articulation_points(G))

    # Compute betweenness centrality (normalized)
    betweenness = nx.betweenness_centrality(G, normalized=True)

    # Compute degree for each node
    degrees = dict(G.degree())

    # For each articulation point, compute k_v (components after removal)
    ap_metrics = []
    for ap in articulation_points:
        # Create graph without this node
        G_removed = G.copy()
        G_removed.remove_node(ap)
        n_components = nx.number_connected_components(G_removed)
        ap_metrics.append({
            'bus': ap,
            'components_after_removal': n_components,
            'betweenness': betweenness[ap],
            'degree': degrees[ap],
        })

    # Sort by: components_after_removal (desc), betweenness (desc), bus (asc)
    ap_metrics.sort(key=lambda x: (-x['components_after_removal'], -x['betweenness'], x['bus']))

    # Take top 10
    top_10 = ap_metrics[:10]

    # The critical bus is the first one (highest k_v, then highest betweenness, then lowest bus)
    critical_bus = top_10[0] if top_10 else None

    return {
        'n_buses': data['n_buses'],
        'bus_ids': data['bus_ids'],
        'n_branches_in_service': data['n_branches_in_service'],
        'articulation_points': articulation_points,
        'top_10': top_10,
        'critical_bus': critical_bus,
        'all_betweenness': betweenness,
        'all_degrees': degrees,
    }


def is_light_gray_color(rgb_str):
    """Check if an ARGB color string represents a light gray.

    Args:
        rgb_str: 8-character ARGB hex string like 'FFD3D3D3'

    Returns:
        True if the color is a light gray (R==G==B and all >= MIN_LIGHT_GRAY_BRIGHTNESS)
    """
    if rgb_str in ACCEPTABLE_LIGHT_GRAY_FILLS:
        return True

    if len(rgb_str) != 8:
        return False

    try:
        r = int(rgb_str[2:4], 16)
        g = int(rgb_str[4:6], 16)
        b = int(rgb_str[6:8], 16)

        # Must be gray (R == G == B) and light (>= brightness threshold)
        is_gray = (r == g == b)
        is_light = (r >= MIN_LIGHT_GRAY_BRIGHTNESS)
        return is_gray and is_light
    except ValueError:
        return False


def is_black_font_color(font_color):
    """Check if a font color is black (or default/unset which renders as black).

    Args:
        font_color: openpyxl Color object from cell.font.color

    Returns:
        True if the color is black or unset (default black)
    """
    if font_color is None:
        # Unset font color defaults to black
        return True

    if font_color.type == 'rgb' and font_color.rgb:
        rgb = font_color.rgb.upper()
        # Black is 'FF000000' or '00000000'
        return rgb in ['FF000000', '00000000']

    if font_color.type == 'theme':
        # Theme index 1 is typically the default text color (black in most themes)
        # Theme index 0 or None also typically means default
        return font_color.theme in [None, 0, 1]

    # If color type is 'auto' or 'indexed' with index 0/8, it's typically black
    if font_color.type == 'indexed':
        # Index 0 and 8 are typically black in the default palette
        return font_color.indexed in [0, 8, 64]  # 64 is also system text color

    # Default: assume unset means black
    return True


# Precompute expected values for all cases
EXPECTED_VALUES = {}
for case_name, filepath in MATPOWER_FILES.items():
    if os.path.exists(filepath):
        EXPECTED_VALUES[case_name] = compute_expected_values(filepath)


class TestOutputFileExists:
    """Tests for output file existence and basic validity."""

    def test_output_file_exists(self):
        """Verify output Excel file was created at the specified path."""
        assert os.path.exists(OUTPUT_FILE), (
            f"Output file not found at {OUTPUT_FILE}"
        )

    def test_output_file_is_not_empty(self):
        """Verify output file is not empty."""
        assert os.path.exists(OUTPUT_FILE), "Output file does not exist"
        file_size = os.path.getsize(OUTPUT_FILE)
        assert file_size > 0, "Output file is empty"

    def test_output_file_has_xlsx_extension(self):
        """Verify output file has .xlsx extension."""
        assert OUTPUT_FILE.endswith(".xlsx"), (
            "Output file should have .xlsx extension"
        )

    def test_output_directory_exists(self):
        """Verify output directory exists."""
        output_dir = os.path.dirname(OUTPUT_FILE)
        assert os.path.isdir(output_dir), (
            f"Output directory {output_dir} does not exist"
        )


class TestExcelFileValidity:
    """Tests for Excel file validity and structure."""

    def test_file_is_valid_xlsx(self):
        """Verify file can be opened as a valid Excel workbook."""
        from openpyxl import load_workbook

        assert os.path.exists(OUTPUT_FILE), "Output file does not exist"
        try:
            wb = load_workbook(OUTPUT_FILE)
            wb.close()
        except Exception as e:
            pytest.fail(f"Failed to open file as valid Excel workbook: {e}")

    def test_workbook_has_exactly_two_sheets_with_correct_names(self):
        """Verify workbook contains exactly two sheets named 'Summary' and 'Details' in that order."""
        from openpyxl import load_workbook

        assert os.path.exists(OUTPUT_FILE), "Output file does not exist"
        wb = load_workbook(OUTPUT_FILE)
        try:
            assert wb.sheetnames == ['Summary', 'Details'], (
                f"Expected sheets ['Summary', 'Details'] in that exact order, "
                f"but found {wb.sheetnames}"
            )
        finally:
            wb.close()

    def test_no_hidden_sheets(self):
        """Verify there are no hidden sheets in the workbook."""
        from openpyxl import load_workbook

        assert os.path.exists(OUTPUT_FILE), "Output file does not exist"
        wb = load_workbook(OUTPUT_FILE)
        try:
            for sheet_name in wb.sheetnames:
                ws = wb[sheet_name]
                assert ws.sheet_state == 'visible', (
                    f"Sheet '{sheet_name}' is hidden (state: {ws.sheet_state})"
                )
        finally:
            wb.close()

    def test_summary_sheet_exists(self):
        """Verify 'Summary' sheet exists in workbook."""
        from openpyxl import load_workbook

        assert os.path.exists(OUTPUT_FILE), "Output file does not exist"
        wb = load_workbook(OUTPUT_FILE)
        try:
            assert "Summary" in wb.sheetnames, (
                f"'Summary' sheet not found. Available sheets: {wb.sheetnames}"
            )
        finally:
            wb.close()

    def test_details_sheet_exists(self):
        """Verify 'Details' sheet exists in workbook."""
        from openpyxl import load_workbook

        assert os.path.exists(OUTPUT_FILE), "Output file does not exist"
        wb = load_workbook(OUTPUT_FILE)
        try:
            assert "Details" in wb.sheetnames, (
                f"'Details' sheet not found. Available sheets: {wb.sheetnames}"
            )
        finally:
            wb.close()


class TestSummarySheetStructure:
    """Tests for Summary sheet structure and content."""

    def test_summary_has_exact_columns_in_order(self):
        """Verify Summary sheet has exactly the required columns in the correct order."""
        from openpyxl import load_workbook

        assert os.path.exists(OUTPUT_FILE), "Output file does not exist"
        wb = load_workbook(OUTPUT_FILE)
        try:
            ws = wb["Summary"]
            # Get header row values (filter out None values from empty cells)
            headers = [cell.value for cell in ws[1] if cell.value is not None]

            assert headers == SUMMARY_COLUMNS, (
                f"Summary sheet columns must be exactly {SUMMARY_COLUMNS} in that order, "
                f"but found {headers}"
            )
        finally:
            wb.close()

    def test_summary_has_three_data_rows(self):
        """Verify Summary sheet has exactly 3 data rows (one per case)."""
        from openpyxl import load_workbook

        assert os.path.exists(OUTPUT_FILE), "Output file does not exist"
        wb = load_workbook(OUTPUT_FILE)
        try:
            ws = wb["Summary"]
            # Count non-empty rows (excluding header)
            data_rows = 0
            for row in ws.iter_rows(min_row=2, max_col=1):
                if row[0].value is not None:
                    data_rows += 1

            assert data_rows == 3, (
                f"Expected 3 data rows in Summary sheet, found {data_rows}"
            )
        finally:
            wb.close()

    def test_summary_case_names_correct(self):
        """Verify Summary sheet contains all expected case names in correct order."""
        from openpyxl import load_workbook

        assert os.path.exists(OUTPUT_FILE), "Output file does not exist"
        wb = load_workbook(OUTPUT_FILE)
        try:
            ws = wb["Summary"]
            # Find case_name column index
            headers = [cell.value for cell in ws[1]]
            case_name_idx = headers.index("case_name") + 1  # 1-indexed

            case_names = []
            for row in ws.iter_rows(min_row=2, min_col=case_name_idx, max_col=case_name_idx):
                if row[0].value is not None:
                    case_names.append(row[0].value)

            assert case_names == CASE_ORDER, (
                f"Case names not in expected order. Expected {CASE_ORDER}, got {case_names}"
            )
        finally:
            wb.close()

    def test_summary_n_buses_values_exact(self):
        """Verify n_buses values match exact bus counts from MATPOWER files."""
        from openpyxl import load_workbook

        assert os.path.exists(OUTPUT_FILE), "Output file does not exist"
        wb = load_workbook(OUTPUT_FILE)
        try:
            ws = wb["Summary"]
            headers = [cell.value for cell in ws[1]]
            case_name_idx = headers.index("case_name") + 1
            n_buses_idx = headers.index("n_buses") + 1

            for row_idx in range(2, 5):
                case_name = ws.cell(row=row_idx, column=case_name_idx).value
                n_buses = ws.cell(row=row_idx, column=n_buses_idx).value

                if case_name in EXPECTED_VALUES:
                    expected = EXPECTED_VALUES[case_name]['n_buses']
                    assert n_buses == expected, (
                        f"n_buses for {case_name}: expected {expected}, got {n_buses}"
                    )
        finally:
            wb.close()

    def test_summary_n_branches_in_service_exact(self):
        """Verify n_branches_in_service matches exact count of in-service branches from MATPOWER files."""
        from openpyxl import load_workbook

        assert os.path.exists(OUTPUT_FILE), "Output file does not exist"
        wb = load_workbook(OUTPUT_FILE)
        try:
            ws = wb["Summary"]
            headers = [cell.value for cell in ws[1]]
            case_name_idx = headers.index("case_name") + 1
            n_branches_idx = headers.index("n_branches_in_service") + 1

            for row_idx in range(2, 5):
                case_name = ws.cell(row=row_idx, column=case_name_idx).value
                n_branches = ws.cell(row=row_idx, column=n_branches_idx).value

                if case_name in EXPECTED_VALUES:
                    expected = EXPECTED_VALUES[case_name]['n_branches_in_service']
                    assert n_branches == expected, (
                        f"n_branches_in_service for {case_name}: expected {expected}, got {n_branches}"
                    )
        finally:
            wb.close()

    def test_summary_critical_bus_is_correct(self):
        """Verify critical_bus matches the expected articulation point with highest k_v."""
        from openpyxl import load_workbook

        assert os.path.exists(OUTPUT_FILE), "Output file does not exist"
        wb = load_workbook(OUTPUT_FILE)
        try:
            ws = wb["Summary"]
            headers = [cell.value for cell in ws[1]]
            case_name_idx = headers.index("case_name") + 1
            critical_bus_idx = headers.index("critical_bus") + 1

            for row_idx in range(2, 5):
                case_name = ws.cell(row=row_idx, column=case_name_idx).value
                critical_bus = ws.cell(row=row_idx, column=critical_bus_idx).value

                if case_name in EXPECTED_VALUES:
                    expected_critical = EXPECTED_VALUES[case_name]['critical_bus']
                    if expected_critical:
                        expected_bus = expected_critical['bus']
                        assert critical_bus == expected_bus, (
                            f"critical_bus for {case_name}: expected {expected_bus}, got {critical_bus}"
                        )
        finally:
            wb.close()

    def test_summary_components_after_removal_correct(self):
        """Verify components_after_removal matches computed value for critical bus."""
        from openpyxl import load_workbook

        assert os.path.exists(OUTPUT_FILE), "Output file does not exist"
        wb = load_workbook(OUTPUT_FILE)
        try:
            ws = wb["Summary"]
            headers = [cell.value for cell in ws[1]]
            case_name_idx = headers.index("case_name") + 1
            components_idx = headers.index("components_after_removal") + 1

            for row_idx in range(2, 5):
                case_name = ws.cell(row=row_idx, column=case_name_idx).value
                components = ws.cell(row=row_idx, column=components_idx).value

                if case_name in EXPECTED_VALUES:
                    expected_critical = EXPECTED_VALUES[case_name]['critical_bus']
                    if expected_critical:
                        expected_components = expected_critical['components_after_removal']
                        assert components == expected_components, (
                            f"components_after_removal for {case_name}: "
                            f"expected {expected_components}, got {components}"
                        )
        finally:
            wb.close()

    def test_summary_betweenness_correct(self):
        """Verify betweenness matches computed value for critical bus within tolerance."""
        from openpyxl import load_workbook

        assert os.path.exists(OUTPUT_FILE), "Output file does not exist"
        wb = load_workbook(OUTPUT_FILE)
        try:
            ws = wb["Summary"]
            headers = [cell.value for cell in ws[1]]
            case_name_idx = headers.index("case_name") + 1
            betweenness_idx = headers.index("betweenness") + 1

            for row_idx in range(2, 5):
                case_name = ws.cell(row=row_idx, column=case_name_idx).value
                betweenness = ws.cell(row=row_idx, column=betweenness_idx).value

                if case_name in EXPECTED_VALUES:
                    expected_critical = EXPECTED_VALUES[case_name]['critical_bus']
                    if expected_critical:
                        expected_betweenness = expected_critical['betweenness']
                        assert abs(betweenness - expected_betweenness) < 1e-9, (
                            f"betweenness for {case_name}: expected {expected_betweenness:.9f}, "
                            f"got {betweenness:.9f} (diff: {abs(betweenness - expected_betweenness):.2e})"
                        )
        finally:
            wb.close()


class TestDetailsSheetStructure:
    """Tests for Details sheet structure and content."""

    def test_details_has_exact_columns_in_order(self):
        """Verify Details sheet has exactly the required columns in the correct order."""
        from openpyxl import load_workbook

        assert os.path.exists(OUTPUT_FILE), "Output file does not exist"
        wb = load_workbook(OUTPUT_FILE)
        try:
            ws = wb["Details"]
            # Get header row values (filter out None values from empty cells)
            headers = [cell.value for cell in ws[1] if cell.value is not None]

            assert headers == DETAILS_COLUMNS, (
                f"Details sheet columns must be exactly {DETAILS_COLUMNS} in that order, "
                f"but found {headers}"
            )
        finally:
            wb.close()

    def test_details_has_correct_row_count_per_case(self):
        """Verify Details sheet has exactly min(10, |AP|) rows per case."""
        from openpyxl import load_workbook

        assert os.path.exists(OUTPUT_FILE), "Output file does not exist"
        wb = load_workbook(OUTPUT_FILE)
        try:
            ws = wb["Details"]
            headers = [cell.value for cell in ws[1]]
            case_name_idx = headers.index("case_name") + 1

            case_counts = {}
            for row in ws.iter_rows(min_row=2, min_col=case_name_idx, max_col=case_name_idx):
                case_name = row[0].value
                if case_name is not None:
                    case_counts[case_name] = case_counts.get(case_name, 0) + 1

            for case_name in CASE_ORDER:
                if case_name in EXPECTED_VALUES:
                    num_aps = len(EXPECTED_VALUES[case_name]['articulation_points'])
                    expected_count = min(10, num_aps)
                    actual_count = case_counts.get(case_name, 0)
                    assert actual_count == expected_count, (
                        f"Case '{case_name}' should have {expected_count} rows "
                        f"(min(10, {num_aps} articulation points)), found {actual_count}"
                    )
        finally:
            wb.close()

    def test_details_cases_grouped_in_order(self):
        """Verify Details rows are grouped by case in CASE_ORDER with no interleaving."""
        from openpyxl import load_workbook

        assert os.path.exists(OUTPUT_FILE), "Output file does not exist"
        wb = load_workbook(OUTPUT_FILE)
        try:
            ws = wb["Details"]
            headers = [cell.value for cell in ws[1]]
            case_name_idx = headers.index("case_name") + 1

            # Collect case names in order of appearance
            case_names_in_order = []
            for row in ws.iter_rows(min_row=2, min_col=case_name_idx, max_col=case_name_idx):
                case_name = row[0].value
                if case_name is not None:
                    case_names_in_order.append(case_name)

            # Verify no interleaving: once we move to a new case, we shouldn't go back
            seen_cases = []
            current_case = None
            for case_name in case_names_in_order:
                if case_name != current_case:
                    assert case_name not in seen_cases, (
                        f"Case '{case_name}' appears again after other cases - "
                        f"cases must be grouped together without interleaving. "
                        f"Order seen: {seen_cases + [case_name]}"
                    )
                    if current_case is not None:
                        seen_cases.append(current_case)
                    current_case = case_name

            # Add the last case
            if current_case is not None:
                seen_cases.append(current_case)

            # Verify the order matches CASE_ORDER
            assert seen_cases == CASE_ORDER, (
                f"Cases should appear in order {CASE_ORDER}, but found {seen_cases}"
            )
        finally:
            wb.close()

    def test_details_all_buses_are_articulation_points(self):
        """Verify all buses in Details sheet are actual articulation points."""
        from openpyxl import load_workbook

        assert os.path.exists(OUTPUT_FILE), "Output file does not exist"
        wb = load_workbook(OUTPUT_FILE)
        try:
            ws = wb["Details"]
            headers = [cell.value for cell in ws[1]]
            case_name_idx = headers.index("case_name") + 1
            bus_idx = headers.index("bus") + 1

            for row_idx in range(2, ws.max_row + 1):
                case_name = ws.cell(row=row_idx, column=case_name_idx).value
                bus = ws.cell(row=row_idx, column=bus_idx).value

                if case_name in EXPECTED_VALUES and bus is not None:
                    aps = EXPECTED_VALUES[case_name]['articulation_points']
                    assert bus in aps, (
                        f"Bus {bus} in row {row_idx} for case '{case_name}' "
                        f"is not an articulation point. Valid APs: {sorted(aps)}"
                    )
        finally:
            wb.close()

    def test_details_top_10_buses_match_expected(self):
        """Verify the top 10 buses for each case match the expected ranking."""
        from openpyxl import load_workbook

        assert os.path.exists(OUTPUT_FILE), "Output file does not exist"
        wb = load_workbook(OUTPUT_FILE)
        try:
            ws = wb["Details"]
            headers = [cell.value for cell in ws[1]]
            case_name_idx = headers.index("case_name") + 1
            bus_idx = headers.index("bus") + 1

            # Collect buses per case
            case_buses = {}
            for row_idx in range(2, ws.max_row + 1):
                case_name = ws.cell(row=row_idx, column=case_name_idx).value
                bus = ws.cell(row=row_idx, column=bus_idx).value
                if case_name and bus is not None:
                    if case_name not in case_buses:
                        case_buses[case_name] = []
                    case_buses[case_name].append(bus)

            for case_name in CASE_ORDER:
                if case_name in EXPECTED_VALUES and case_name in case_buses:
                    expected_top_10 = [ap['bus'] for ap in EXPECTED_VALUES[case_name]['top_10']]
                    actual_buses = case_buses[case_name]
                    assert actual_buses == expected_top_10, (
                        f"Top 10 buses for {case_name} don't match expected. "
                        f"Expected: {expected_top_10}, Got: {actual_buses}"
                    )
        finally:
            wb.close()

    def test_details_components_after_removal_correct(self):
        """Verify components_after_removal values match computed values."""
        from openpyxl import load_workbook

        assert os.path.exists(OUTPUT_FILE), "Output file does not exist"
        wb = load_workbook(OUTPUT_FILE)
        try:
            ws = wb["Details"]
            headers = [cell.value for cell in ws[1]]
            case_name_idx = headers.index("case_name") + 1
            bus_idx = headers.index("bus") + 1
            components_idx = headers.index("components_after_removal") + 1

            for row_idx in range(2, ws.max_row + 1):
                case_name = ws.cell(row=row_idx, column=case_name_idx).value
                bus = ws.cell(row=row_idx, column=bus_idx).value
                components = ws.cell(row=row_idx, column=components_idx).value

                if case_name in EXPECTED_VALUES and bus is not None:
                    # Find expected value for this bus
                    expected_ap = next(
                        (ap for ap in EXPECTED_VALUES[case_name]['top_10'] if ap['bus'] == bus),
                        None
                    )
                    if expected_ap:
                        expected_components = expected_ap['components_after_removal']
                        assert components == expected_components, (
                            f"components_after_removal for bus {bus} in {case_name} (row {row_idx}): "
                            f"expected {expected_components}, got {components}"
                        )
        finally:
            wb.close()

    def test_details_betweenness_correct(self):
        """Verify betweenness values match computed values within tolerance."""
        from openpyxl import load_workbook

        assert os.path.exists(OUTPUT_FILE), "Output file does not exist"
        wb = load_workbook(OUTPUT_FILE)
        try:
            ws = wb["Details"]
            headers = [cell.value for cell in ws[1]]
            case_name_idx = headers.index("case_name") + 1
            bus_idx = headers.index("bus") + 1
            betweenness_idx = headers.index("betweenness") + 1

            for row_idx in range(2, ws.max_row + 1):
                case_name = ws.cell(row=row_idx, column=case_name_idx).value
                bus = ws.cell(row=row_idx, column=bus_idx).value
                betweenness = ws.cell(row=row_idx, column=betweenness_idx).value

                if case_name in EXPECTED_VALUES and bus is not None:
                    expected_betweenness = EXPECTED_VALUES[case_name]['all_betweenness'].get(bus)
                    if expected_betweenness is not None:
                        assert abs(betweenness - expected_betweenness) < 1e-9, (
                            f"betweenness for bus {bus} in {case_name} (row {row_idx}): "
                            f"expected {expected_betweenness:.9f}, got {betweenness:.9f}"
                        )
        finally:
            wb.close()

    def test_details_degree_correct(self):
        """Verify degree values match computed values."""
        from openpyxl import load_workbook

        assert os.path.exists(OUTPUT_FILE), "Output file does not exist"
        wb = load_workbook(OUTPUT_FILE)
        try:
            ws = wb["Details"]
            headers = [cell.value for cell in ws[1]]
            case_name_idx = headers.index("case_name") + 1
            bus_idx = headers.index("bus") + 1
            degree_idx = headers.index("degree") + 1

            for row_idx in range(2, ws.max_row + 1):
                case_name = ws.cell(row=row_idx, column=case_name_idx).value
                bus = ws.cell(row=row_idx, column=bus_idx).value
                degree = ws.cell(row=row_idx, column=degree_idx).value

                if case_name in EXPECTED_VALUES and bus is not None:
                    expected_degree = EXPECTED_VALUES[case_name]['all_degrees'].get(bus)
                    if expected_degree is not None:
                        assert degree == expected_degree, (
                            f"degree for bus {bus} in {case_name} (row {row_idx}): "
                            f"expected {expected_degree}, got {degree}"
                        )
        finally:
            wb.close()

    def test_details_sorted_correctly(self):
        """Verify Details rows for each case are sorted by k_v desc, betweenness desc, bus asc."""
        from openpyxl import load_workbook

        assert os.path.exists(OUTPUT_FILE), "Output file does not exist"
        wb = load_workbook(OUTPUT_FILE)
        try:
            ws = wb["Details"]
            headers = [cell.value for cell in ws[1]]
            case_name_idx = headers.index("case_name") + 1
            bus_idx = headers.index("bus") + 1
            components_idx = headers.index("components_after_removal") + 1
            betweenness_idx = headers.index("betweenness") + 1

            # Group rows by case
            case_rows = {}
            for row_idx in range(2, ws.max_row + 1):
                case_name = ws.cell(row=row_idx, column=case_name_idx).value
                if case_name is None:
                    continue

                bus = ws.cell(row=row_idx, column=bus_idx).value
                components = ws.cell(row=row_idx, column=components_idx).value
                betweenness = ws.cell(row=row_idx, column=betweenness_idx).value

                if case_name not in case_rows:
                    case_rows[case_name] = []
                case_rows[case_name].append((components, betweenness, bus))

            # Check sorting for each case
            for case_name, rows in case_rows.items():
                for i in range(len(rows) - 1):
                    curr = rows[i]
                    next_row = rows[i + 1]

                    # Sort key: -components (desc), -betweenness (desc), bus (asc)
                    curr_key = (-curr[0], -curr[1], curr[2])
                    next_key = (-next_row[0], -next_row[1], next_row[2])

                    assert curr_key <= next_key, (
                        f"Rows for {case_name} not properly sorted at position {i}. "
                        f"Row {i}: (k_v={curr[0]}, betweenness={curr[1]:.6f}, bus={curr[2]}), "
                        f"Row {i+1}: (k_v={next_row[0]}, betweenness={next_row[1]:.6f}, bus={next_row[2]})"
                    )
        finally:
            wb.close()


class TestExcelFormatting:
    """Tests for Excel formatting requirements."""

    def test_summary_header_row_bold(self):
        """Verify Summary sheet header row has bold font."""
        from openpyxl import load_workbook

        assert os.path.exists(OUTPUT_FILE), "Output file does not exist"
        wb = load_workbook(OUTPUT_FILE)
        try:
            ws = wb["Summary"]
            for cell in ws[1]:
                if cell.value is not None:
                    assert cell.font.bold, (
                        f"Header cell '{cell.value}' in Summary should be bold "
                        f"(font.bold={cell.font.bold})"
                    )
        finally:
            wb.close()

    def test_details_header_row_bold(self):
        """Verify Details sheet header row has bold font."""
        from openpyxl import load_workbook

        assert os.path.exists(OUTPUT_FILE), "Output file does not exist"
        wb = load_workbook(OUTPUT_FILE)
        try:
            ws = wb["Details"]
            for cell in ws[1]:
                if cell.value is not None:
                    assert cell.font.bold, (
                        f"Header cell '{cell.value}' in Details should be bold "
                        f"(font.bold={cell.font.bold})"
                    )
        finally:
            wb.close()

    def test_summary_header_row_black_font(self):
        """Verify Summary sheet header row has black font color (financial-model convention)."""
        from openpyxl import load_workbook

        assert os.path.exists(OUTPUT_FILE), "Output file does not exist"
        wb = load_workbook(OUTPUT_FILE)
        try:
            ws = wb["Summary"]
            for cell in ws[1]:
                if cell.value is not None:
                    font_color = cell.font.color
                    assert is_black_font_color(font_color), (
                        f"Header cell '{cell.value}' in Summary should have black font "
                        f"(financial-model convention), got color={font_color}"
                    )
        finally:
            wb.close()

    def test_details_header_row_black_font(self):
        """Verify Details sheet header row has black font color (financial-model convention)."""
        from openpyxl import load_workbook

        assert os.path.exists(OUTPUT_FILE), "Output file does not exist"
        wb = load_workbook(OUTPUT_FILE)
        try:
            ws = wb["Details"]
            for cell in ws[1]:
                if cell.value is not None:
                    font_color = cell.font.color
                    assert is_black_font_color(font_color), (
                        f"Header cell '{cell.value}' in Details should have black font "
                        f"(financial-model convention), got color={font_color}"
                    )
        finally:
            wb.close()

    def test_summary_header_row_light_gray_fill(self):
        """Verify Summary sheet header row has light gray fill."""
        from openpyxl import load_workbook

        assert os.path.exists(OUTPUT_FILE), "Output file does not exist"
        wb = load_workbook(OUTPUT_FILE)
        try:
            ws = wb["Summary"]
            for cell in ws[1]:
                if cell.value is not None:
                    fill = cell.fill
                    assert fill.patternType is not None and fill.patternType != "none", (
                        f"Header cell '{cell.value}' in Summary should have fill "
                        f"(patternType={fill.patternType})"
                    )
                    # Check that it's a light gray color
                    fg_color = fill.fgColor
                    if fg_color.type == 'rgb' and fg_color.rgb:
                        rgb = fg_color.rgb.upper()
                        assert is_light_gray_color(rgb), (
                            f"Header cell '{cell.value}' fill color should be light gray "
                            f"(R==G==B >= 0x{MIN_LIGHT_GRAY_BRIGHTNESS:02X}), "
                            f"got fgColor.rgb={rgb}"
                        )
        finally:
            wb.close()

    def test_details_header_row_light_gray_fill(self):
        """Verify Details sheet header row has light gray fill."""
        from openpyxl import load_workbook

        assert os.path.exists(OUTPUT_FILE), "Output file does not exist"
        wb = load_workbook(OUTPUT_FILE)
        try:
            ws = wb["Details"]
            for cell in ws[1]:
                if cell.value is not None:
                    fill = cell.fill
                    assert fill.patternType is not None and fill.patternType != "none", (
                        f"Header cell '{cell.value}' in Details should have fill "
                        f"(patternType={fill.patternType})"
                    )
                    fg_color = fill.fgColor
                    if fg_color.type == 'rgb' and fg_color.rgb:
                        rgb = fg_color.rgb.upper()
                        assert is_light_gray_color(rgb), (
                            f"Header cell '{cell.value}' fill color should be light gray "
                            f"(R==G==B >= 0x{MIN_LIGHT_GRAY_BRIGHTNESS:02X}), "
                            f"got fgColor.rgb={rgb}"
                        )
        finally:
            wb.close()

    def test_summary_freeze_panes_at_A2(self):
        """Verify Summary sheet has freeze panes at exactly A2."""
        from openpyxl import load_workbook

        assert os.path.exists(OUTPUT_FILE), "Output file does not exist"
        wb = load_workbook(OUTPUT_FILE)
        try:
            ws = wb["Summary"]
            assert ws.freeze_panes is not None, (
                "Summary sheet should have freeze panes set (got None)"
            )
            assert ws.freeze_panes == "A2", (
                f"Summary sheet freeze_panes should be exactly 'A2', got '{ws.freeze_panes}'"
            )
        finally:
            wb.close()

    def test_details_freeze_panes_at_A2(self):
        """Verify Details sheet has freeze panes at exactly A2."""
        from openpyxl import load_workbook

        assert os.path.exists(OUTPUT_FILE), "Output file does not exist"
        wb = load_workbook(OUTPUT_FILE)
        try:
            ws = wb["Details"]
            assert ws.freeze_panes is not None, (
                "Details sheet should have freeze panes set (got None)"
            )
            assert ws.freeze_panes == "A2", (
                f"Details sheet freeze_panes should be exactly 'A2', got '{ws.freeze_panes}'"
            )
        finally:
            wb.close()

    def test_summary_betweenness_number_format(self):
        """Verify betweenness column in Summary has exactly '0.000000' format."""
        from openpyxl import load_workbook

        assert os.path.exists(OUTPUT_FILE), "Output file does not exist"
        wb = load_workbook(OUTPUT_FILE)
        try:
            ws = wb["Summary"]
            headers = [cell.value for cell in ws[1]]
            betweenness_idx = headers.index("betweenness") + 1

            for row_idx in range(2, 5):
                cell = ws.cell(row=row_idx, column=betweenness_idx)
                if cell.value is not None:
                    number_format = cell.number_format
                    assert number_format == "0.000000", (
                        f"Betweenness cell at row {row_idx} should have format '0.000000', "
                        f"got '{number_format}'"
                    )
        finally:
            wb.close()

    def test_details_betweenness_number_format(self):
        """Verify betweenness column in Details has exactly '0.000000' format."""
        from openpyxl import load_workbook

        assert os.path.exists(OUTPUT_FILE), "Output file does not exist"
        wb = load_workbook(OUTPUT_FILE)
        try:
            ws = wb["Details"]
            headers = [cell.value for cell in ws[1]]
            betweenness_idx = headers.index("betweenness") + 1

            for row_idx in range(2, ws.max_row + 1):
                cell = ws.cell(row=row_idx, column=betweenness_idx)
                if cell.value is not None:
                    number_format = cell.number_format
                    assert number_format == "0.000000", (
                        f"Betweenness cell at row {row_idx} should have format '0.000000', "
                        f"got '{number_format}'"
                    )
        finally:
            wb.close()

    def test_summary_integer_columns_format(self):
        """Verify integer columns in Summary have exactly '0' number format."""
        from openpyxl import load_workbook

        assert os.path.exists(OUTPUT_FILE), "Output file does not exist"
        wb = load_workbook(OUTPUT_FILE)
        try:
            ws = wb["Summary"]
            headers = [cell.value for cell in ws[1]]

            integer_columns = ["n_buses", "n_branches_in_service", "critical_bus", "components_after_removal"]

            for col_name in integer_columns:
                if col_name in headers:
                    col_idx = headers.index(col_name) + 1
                    for row_idx in range(2, 5):
                        cell = ws.cell(row=row_idx, column=col_idx)
                        if cell.value is not None:
                            # Check value is integer
                            assert isinstance(cell.value, int), (
                                f"{col_name} at row {row_idx} should be integer, "
                                f"got {type(cell.value).__name__}: {cell.value}"
                            )
                            # Check number format is exactly '0' (not 'General')
                            assert cell.number_format == '0', (
                                f"{col_name} at row {row_idx} should have format '0', "
                                f"got '{cell.number_format}'"
                            )
        finally:
            wb.close()

    def test_details_integer_columns_format(self):
        """Verify integer columns in Details have exactly '0' number format."""
        from openpyxl import load_workbook

        assert os.path.exists(OUTPUT_FILE), "Output file does not exist"
        wb = load_workbook(OUTPUT_FILE)
        try:
            ws = wb["Details"]
            headers = [cell.value for cell in ws[1]]

            integer_columns = ["bus", "components_after_removal", "degree"]

            for col_name in integer_columns:
                if col_name in headers:
                    col_idx = headers.index(col_name) + 1
                    for row_idx in range(2, ws.max_row + 1):
                        cell = ws.cell(row=row_idx, column=col_idx)
                        if cell.value is not None:
                            assert isinstance(cell.value, int), (
                                f"{col_name} at row {row_idx} should be integer, "
                                f"got {type(cell.value).__name__}: {cell.value}"
                            )
                            # Check number format is exactly '0' (not 'General')
                            assert cell.number_format == '0', (
                                f"{col_name} at row {row_idx} should have format '0', "
                                f"got '{cell.number_format}'"
                            )
        finally:
            wb.close()

    def test_summary_header_cells_not_integer_formatted(self):
        """Verify header cells do not have '0' number format (they are text labels)."""
        from openpyxl import load_workbook

        assert os.path.exists(OUTPUT_FILE), "Output file does not exist"
        wb = load_workbook(OUTPUT_FILE)
        try:
            ws = wb["Summary"]
            for cell in ws[1]:
                if cell.value is not None:
                    # Headers should not have the integer '0' format
                    assert cell.number_format != '0', (
                        f"Header cell '{cell.value}' should not have '0' number format "
                        f"(it's a text label, not an integer)"
                    )
        finally:
            wb.close()

    def test_details_header_cells_not_integer_formatted(self):
        """Verify header cells do not have '0' number format (they are text labels)."""
        from openpyxl import load_workbook

        assert os.path.exists(OUTPUT_FILE), "Output file does not exist"
        wb = load_workbook(OUTPUT_FILE)
        try:
            ws = wb["Details"]
            for cell in ws[1]:
                if cell.value is not None:
                    # Headers should not have the integer '0' format
                    assert cell.number_format != '0', (
                        f"Header cell '{cell.value}' should not have '0' number format "
                        f"(it's a text label, not an integer)"
                    )
        finally:
            wb.close()

    def test_formula_cells_have_black_font(self):
        """Verify formula cells have black font color."""
        from openpyxl import load_workbook

        assert os.path.exists(OUTPUT_FILE), "Output file does not exist"
        # Load with data_only=False to see formulas
        wb = load_workbook(OUTPUT_FILE, data_only=False)
        try:
            for sheet_name in ['Summary', 'Details']:
                ws = wb[sheet_name]
                for row in ws.iter_rows():
                    for cell in row:
                        if cell.data_type == 'f':  # Formula cell
                            font_color = cell.font.color
                            assert is_black_font_color(font_color), (
                                f"Formula cell {cell.coordinate} in {sheet_name} "
                                f"should have black font, got color={font_color}"
                            )
        finally:
            wb.close()

    def test_all_data_cells_have_black_font(self):
        """Verify all data cells (non-header) have black font color."""
        from openpyxl import load_workbook

        assert os.path.exists(OUTPUT_FILE), "Output file does not exist"
        wb = load_workbook(OUTPUT_FILE)
        try:
            for sheet_name in ['Summary', 'Details']:
                ws = wb[sheet_name]
                for row in ws.iter_rows(min_row=2):  # Skip header row
                    for cell in row:
                        if cell.value is not None:
                            font_color = cell.font.color
                            assert is_black_font_color(font_color), (
                                f"Data cell {cell.coordinate} in {sheet_name} "
                                f"should have black font, got color={font_color}"
                            )
        finally:
            wb.close()


class TestDataConsistency:
    """Tests for data consistency across sheets and with input files."""

    def test_summary_critical_bus_appears_in_details(self):
        """Verify each critical_bus from Summary appears in Details for that case."""
        from openpyxl import load_workbook

        assert os.path.exists(OUTPUT_FILE), "Output file does not exist"
        wb = load_workbook(OUTPUT_FILE)
        try:
            # Get critical buses from Summary
            ws_summary = wb["Summary"]
            summary_headers = [cell.value for cell in ws_summary[1]]
            case_name_idx = summary_headers.index("case_name") + 1
            critical_bus_idx = summary_headers.index("critical_bus") + 1

            critical_buses = {}
            for row_idx in range(2, 5):
                case_name = ws_summary.cell(row=row_idx, column=case_name_idx).value
                critical_bus = ws_summary.cell(row=row_idx, column=critical_bus_idx).value
                if case_name and critical_bus:
                    critical_buses[case_name] = critical_bus

            # Check Details sheet
            ws_details = wb["Details"]
            details_headers = [cell.value for cell in ws_details[1]]
            det_case_name_idx = details_headers.index("case_name") + 1
            det_bus_idx = details_headers.index("bus") + 1

            # Get all buses for each case in Details
            details_buses = {}
            for row_idx in range(2, ws_details.max_row + 1):
                case_name = ws_details.cell(row=row_idx, column=det_case_name_idx).value
                bus = ws_details.cell(row=row_idx, column=det_bus_idx).value
                if case_name and bus:
                    if case_name not in details_buses:
                        details_buses[case_name] = set()
                    details_buses[case_name].add(bus)

            # Verify critical bus is in details
            for case_name, critical_bus in critical_buses.items():
                assert case_name in details_buses, (
                    f"Case {case_name} not found in Details sheet"
                )
                assert critical_bus in details_buses[case_name], (
                    f"Critical bus {critical_bus} for {case_name} not found in Details. "
                    f"Details buses: {sorted(details_buses[case_name])}"
                )
        finally:
            wb.close()

    def test_summary_critical_bus_has_max_components(self):
        """Verify the critical_bus has the maximum components_after_removal in Details."""
        from openpyxl import load_workbook

        assert os.path.exists(OUTPUT_FILE), "Output file does not exist"
        wb = load_workbook(OUTPUT_FILE)
        try:
            # Get summary data
            ws_summary = wb["Summary"]
            summary_headers = [cell.value for cell in ws_summary[1]]
            case_name_idx = summary_headers.index("case_name") + 1
            critical_bus_idx = summary_headers.index("critical_bus") + 1
            components_idx = summary_headers.index("components_after_removal") + 1

            summary_data = {}
            for row_idx in range(2, 5):
                case_name = ws_summary.cell(row=row_idx, column=case_name_idx).value
                critical_bus = ws_summary.cell(row=row_idx, column=critical_bus_idx).value
                components = ws_summary.cell(row=row_idx, column=components_idx).value
                if case_name:
                    summary_data[case_name] = {"critical_bus": critical_bus, "components": components}

            # Get details data
            ws_details = wb["Details"]
            details_headers = [cell.value for cell in ws_details[1]]
            det_case_name_idx = details_headers.index("case_name") + 1
            det_components_idx = details_headers.index("components_after_removal") + 1

            details_max_components = {}
            for row_idx in range(2, ws_details.max_row + 1):
                case_name = ws_details.cell(row=row_idx, column=det_case_name_idx).value
                components = ws_details.cell(row=row_idx, column=det_components_idx).value
                if case_name and components:
                    if case_name not in details_max_components:
                        details_max_components[case_name] = components
                    else:
                        details_max_components[case_name] = max(details_max_components[case_name], components)

            # Verify consistency
            for case_name, data in summary_data.items():
                if case_name in details_max_components:
                    assert data["components"] == details_max_components[case_name], (
                        f"Critical bus components for {case_name} ({data['components']}) "
                        f"doesn't match max in Details ({details_max_components[case_name]})"
                    )
        finally:
            wb.close()

    def test_details_first_row_per_case_is_critical_bus(self):
        """Verify the first row for each case in Details is the critical bus from Summary."""
        from openpyxl import load_workbook

        assert os.path.exists(OUTPUT_FILE), "Output file does not exist"
        wb = load_workbook(OUTPUT_FILE)
        try:
            # Get critical buses from Summary
            ws_summary = wb["Summary"]
            summary_headers = [cell.value for cell in ws_summary[1]]
            case_name_idx = summary_headers.index("case_name") + 1
            critical_bus_idx = summary_headers.index("critical_bus") + 1

            critical_buses = {}
            for row_idx in range(2, 5):
                case_name = ws_summary.cell(row=row_idx, column=case_name_idx).value
                critical_bus = ws_summary.cell(row=row_idx, column=critical_bus_idx).value
                if case_name and critical_bus:
                    critical_buses[case_name] = critical_bus

            # Get first bus for each case in Details
            ws_details = wb["Details"]
            details_headers = [cell.value for cell in ws_details[1]]
            det_case_name_idx = details_headers.index("case_name") + 1
            det_bus_idx = details_headers.index("bus") + 1

            first_bus_per_case = {}
            for row_idx in range(2, ws_details.max_row + 1):
                case_name = ws_details.cell(row=row_idx, column=det_case_name_idx).value
                bus = ws_details.cell(row=row_idx, column=det_bus_idx).value
                if case_name and bus and case_name not in first_bus_per_case:
                    first_bus_per_case[case_name] = bus

            # Verify consistency
            for case_name, critical_bus in critical_buses.items():
                if case_name in first_bus_per_case:
                    assert first_bus_per_case[case_name] == critical_bus, (
                        f"First bus in Details for {case_name} ({first_bus_per_case[case_name]}) "
                        f"should be the critical bus ({critical_bus})"
                    )
        finally:
            wb.close()


class TestGraphTheoryConstraints:
    """Tests for graph theory constraints on the results."""

    def test_articulation_points_exist(self):
        """Verify that articulation points were found for each case."""
        from openpyxl import load_workbook

        assert os.path.exists(OUTPUT_FILE), "Output file does not exist"
        wb = load_workbook(OUTPUT_FILE)
        try:
            ws = wb["Details"]
            headers = [cell.value for cell in ws[1]]
            case_name_idx = headers.index("case_name") + 1

            case_counts = {}
            for row in ws.iter_rows(min_row=2, min_col=case_name_idx, max_col=case_name_idx):
                case_name = row[0].value
                if case_name is not None:
                    case_counts[case_name] = case_counts.get(case_name, 0) + 1

            for case_name in CASE_ORDER:
                assert case_name in case_counts, (
                    f"No articulation points found for {case_name}"
                )
                assert case_counts[case_name] >= 1, (
                    f"At least one articulation point expected for {case_name}"
                )
        finally:
            wb.close()

    def test_components_removal_is_connected_split(self):
        """Verify components_after_removal indicates proper graph split."""
        from openpyxl import load_workbook

        assert os.path.exists(OUTPUT_FILE), "Output file does not exist"
        wb = load_workbook(OUTPUT_FILE)
        try:
            ws = wb["Details"]
            headers = [cell.value for cell in ws[1]]
            components_idx = headers.index("components_after_removal") + 1

            for row_idx in range(2, ws.max_row + 1):
                components = ws.cell(row=row_idx, column=components_idx).value
                if components is not None:
                    # An articulation point removal should create at least 2 components
                    # (the graph was originally connected)
                    assert components >= 2, (
                        f"Row {row_idx}: articulation point should create >= 2 components, "
                        f"got {components}"
                    )
        finally:
            wb.close()


class TestMatpowerParsing:
    """Tests to verify MATPOWER parsing correctness."""

    def test_case57_bus_count(self):
        """Verify case57 has 57 buses."""
        assert 'case57' in EXPECTED_VALUES, "case57 not parsed"
        assert EXPECTED_VALUES['case57']['n_buses'] == 57, (
            f"case57 should have 57 buses, got {EXPECTED_VALUES['case57']['n_buses']}"
        )

    def test_case57_bus_ids_unique(self):
        """Verify case57 bus IDs are unique and count matches expected."""
        assert 'case57' in EXPECTED_VALUES, "case57 not parsed"
        bus_ids = EXPECTED_VALUES['case57']['bus_ids']
        assert len(bus_ids) == 57, (
            f"case57 should have 57 unique bus IDs, got {len(bus_ids)}"
        )

    def test_case118_bus_count(self):
        """Verify case118 has 118 buses."""
        assert 'case118' in EXPECTED_VALUES, "case118 not parsed"
        assert EXPECTED_VALUES['case118']['n_buses'] == 118, (
            f"case118 should have 118 buses, got {EXPECTED_VALUES['case118']['n_buses']}"
        )

    def test_case118_bus_ids_unique(self):
        """Verify case118 bus IDs are unique and count matches expected."""
        assert 'case118' in EXPECTED_VALUES, "case118 not parsed"
        bus_ids = EXPECTED_VALUES['case118']['bus_ids']
        assert len(bus_ids) == 118, (
            f"case118 should have 118 unique bus IDs, got {len(bus_ids)}"
        )

    def test_pglib_case118_bus_count(self):
        """Verify pglib_opf_case118_ieee has 118 buses."""
        assert 'pglib_opf_case118_ieee' in EXPECTED_VALUES, "pglib_opf_case118_ieee not parsed"
        assert EXPECTED_VALUES['pglib_opf_case118_ieee']['n_buses'] == 118, (
            f"pglib_opf_case118_ieee should have 118 buses, "
            f"got {EXPECTED_VALUES['pglib_opf_case118_ieee']['n_buses']}"
        )

    def test_pglib_case118_bus_ids_unique(self):
        """Verify pglib_opf_case118_ieee bus IDs are unique and count matches expected."""
        assert 'pglib_opf_case118_ieee' in EXPECTED_VALUES, "pglib_opf_case118_ieee not parsed"
        bus_ids = EXPECTED_VALUES['pglib_opf_case118_ieee']['bus_ids']
        assert len(bus_ids) == 118, (
            f"pglib_opf_case118_ieee should have 118 unique bus IDs, got {len(bus_ids)}"
        )

    def test_case57_has_articulation_points(self):
        """Verify case57 has articulation points."""
        assert 'case57' in EXPECTED_VALUES, "case57 not parsed"
        aps = EXPECTED_VALUES['case57']['articulation_points']
        assert len(aps) > 0, f"case57 should have articulation points, found {len(aps)}"

    def test_case118_has_articulation_points(self):
        """Verify case118 has articulation points."""
        assert 'case118' in EXPECTED_VALUES, "case118 not parsed"
        aps = EXPECTED_VALUES['case118']['articulation_points']
        assert len(aps) > 0, f"case118 should have articulation points, found {len(aps)}"

    def test_pglib_case118_has_articulation_points(self):
        """Verify pglib_opf_case118_ieee has articulation points."""
        assert 'pglib_opf_case118_ieee' in EXPECTED_VALUES, "pglib_opf_case118_ieee not parsed"
        aps = EXPECTED_VALUES['pglib_opf_case118_ieee']['articulation_points']
        assert len(aps) > 0, f"pglib_opf_case118_ieee should have articulation points, found {len(aps)}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
PYTHON_SCRIPT_3

# Run analyze_networks.py to generate the Excel output file
echo "Running critical bus analysis..."
python3 analyze_networks.py

echo ""
echo "All output files have been created successfully!"
echo "  - analyze_critical_buses.py"
echo "  - analyze_networks.py"
echo "  - expectation_tests.py"
echo "  - output/critical_bus_report.xlsx"

# HARBOR_OUTPUT_FIX_START
if [ -f "/root/harbor_workspaces/task_T228_run1/output/critical_bus_report.xlsx" ]; then cp -f "/root/harbor_workspaces/task_T228_run1/output/critical_bus_report.xlsx" "/root/critical_bus_report.xlsx"; fi
# HARBOR_OUTPUT_FIX_END
