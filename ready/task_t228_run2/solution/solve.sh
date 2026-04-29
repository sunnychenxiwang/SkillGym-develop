#!/bin/bash
# solve.sh - Recreates critical edge DC flow analysis and Excel report
# This script parses MATPOWER case files, computes edge betweenness centrality,
# runs DC power flow, and creates an Excel report.

set -e

# HARBOR_PATH_FIX_START
BASE_FIX="/root/harbor_workspaces/task_T228_run2"
mkdir -p "$BASE_FIX/input" "$BASE_FIX/output"
if [ ! -e "$BASE_FIX/input/case57.m" ] && [ -e "/root/case57.m" ]; then cp -f "/root/case57.m" "$BASE_FIX/input/case57.m"; fi
if [ ! -e "$BASE_FIX/input/case118.m" ] && [ -e "/root/case118.m" ]; then cp -f "/root/case118.m" "$BASE_FIX/input/case118.m"; fi
if [ ! -e "$BASE_FIX/input/pglib_opf_case118_ieee.m" ] && [ -e "/root/pglib_opf_case118_ieee.m" ]; then cp -f "/root/pglib_opf_case118_ieee.m" "$BASE_FIX/input/pglib_opf_case118_ieee.m"; fi
# HARBOR_PATH_FIX_END

cd /root

# Install required dependencies
pip install --break-system-packages networkx openpyxl

# Create the main analysis Python script
cat > analysis_script.py << 'PYTHON_SCRIPT_EOF'
#!/usr/bin/env python3
"""
Parse MATPOWER case files, compute edge betweenness centrality,
run DC power flow, and create Excel report.
"""

import re
import os
import numpy as np
import networkx as nx
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

# File paths
INPUT_DIR = "/root"
OUTPUT_DIR = "/root"
CASE_FILES = [
    "case57.m",
    "case118.m",
    "pglib_opf_case118_ieee.m"
]


def parse_matpower_file(filepath):
    """Parse a MATPOWER .m file and extract baseMVA, bus, gen, branch data."""
    with open(filepath, 'r') as f:
        content = f.read()

    # Remove comments (lines starting with %)
    lines = content.split('\n')
    clean_lines = []
    for line in lines:
        # Remove inline comments (but preserve line content before %)
        idx = line.find('%')
        if idx != -1:
            line = line[:idx]
        clean_lines.append(line)
    content = '\n'.join(clean_lines)

    # Extract baseMVA
    basemva_match = re.search(r'mpc\.baseMVA\s*=\s*([0-9.]+)', content)
    baseMVA = float(basemva_match.group(1)) if basemva_match else 100.0

    # Extract bus data
    bus_match = re.search(r'mpc\.bus\s*=\s*\[\s*([\s\S]*?)\];', content)
    bus_data = []
    if bus_match:
        bus_text = bus_match.group(1)
        for line in bus_text.strip().split('\n'):
            line = line.strip()
            if line and not line.startswith('%'):
                # Parse semicolon-separated entries or space-separated
                line = line.rstrip(';').strip()
                if line:
                    values = line.split()
                    if len(values) >= 3:
                        bus_data.append([float(v) for v in values])
    bus = np.array(bus_data)

    # Extract gen data
    gen_match = re.search(r'mpc\.gen\s*=\s*\[\s*([\s\S]*?)\];', content)
    gen_data = []
    if gen_match:
        gen_text = gen_match.group(1)
        for line in gen_text.strip().split('\n'):
            line = line.strip()
            if line and not line.startswith('%'):
                line = line.rstrip(';').strip()
                if line:
                    values = line.split()
                    if len(values) >= 2:
                        gen_data.append([float(v) for v in values])
    gen = np.array(gen_data) if gen_data else np.zeros((0, 21))

    # Extract branch data
    branch_match = re.search(r'mpc\.branch\s*=\s*\[\s*([\s\S]*?)\];', content)
    branch_data = []
    if branch_match:
        branch_text = branch_match.group(1)
        for line in branch_text.strip().split('\n'):
            line = line.strip()
            if line and not line.startswith('%'):
                line = line.rstrip(';').strip()
                if line:
                    values = line.split()
                    if len(values) >= 11:
                        branch_data.append([float(v) for v in values])
    branch = np.array(branch_data)

    return baseMVA, bus, gen, branch


def build_networkx_graph(bus, branch):
    """Build an undirected NetworkX graph from in-service branches.

    Returns the graph and the number of unique edges (not branch rows).
    Since NetworkX Graph merges parallel edges, n_branch_in_service
    is the count of unique edges in the graph.
    """
    G = nx.Graph()

    # Add all bus nodes
    for i in range(len(bus)):
        bus_id = int(bus[i, 0])
        G.add_node(bus_id)

    # Add edges for in-service branches only (status is column 10, 0-indexed)
    # nx.Graph() automatically handles parallel edges by merging them
    for br in branch:
        status = int(br[10])
        if status == 1:
            fbus = int(br[0])
            tbus = int(br[1])
            G.add_edge(fbus, tbus)

    # n_branch_in_service is the count of unique edges (parallel edges merged)
    n_branch_in_service = len(G.edges())

    return G, n_branch_in_service


def find_critical_edge(G):
    """Find the edge with maximum edge betweenness centrality.

    Tie-break: lexicographically smallest (min(u,v), max(u,v)).
    """
    edge_bc = nx.edge_betweenness_centrality(G)

    # Find max value
    max_bc = max(edge_bc.values())

    # Get all edges with max value
    max_edges = [(e, bc) for e, bc in edge_bc.items() if abs(bc - max_bc) < 1e-12]

    # Sort by lexicographic key (min, max) for deterministic tie-breaking
    def edge_key(item):
        e, _ = item
        return (min(e[0], e[1]), max(e[0], e[1]))

    max_edges.sort(key=edge_key)

    # Return the first one
    critical_edge, critical_bc = max_edges[0]
    # Return as sorted tuple (smaller, larger)
    sorted_edge = (min(critical_edge[0], critical_edge[1]), max(critical_edge[0], critical_edge[1]))

    return sorted_edge, critical_bc


def run_dc_power_flow(baseMVA, bus, gen, branch):
    """Run DC power flow and return voltage angles."""
    n_bus = len(bus)

    # Create bus number to index mapping
    bus_num_to_idx = {int(bus[i, 0]): i for i in range(n_bus)}

    # Find slack bus (type == 3)
    slack_idx = None
    for i in range(n_bus):
        if int(bus[i, 1]) == 3:
            slack_idx = i
            break

    if slack_idx is None:
        raise ValueError("No slack bus (type=3) found")

    # Build net injection P = Pg - Pd (in MW)
    P = np.zeros(n_bus)

    # Subtract Pd (column 2 in bus data)
    for i in range(n_bus):
        P[i] = -bus[i, 2]  # Pd

    # Add Pg from in-service generators (gen status is column 7)
    for g in gen:
        gen_bus = int(g[0])
        gen_pg = g[1]
        gen_status = int(g[7]) if len(g) > 7 else 1
        if gen_status == 1:
            idx = bus_num_to_idx[gen_bus]
            P[idx] += gen_pg

    # Build B matrix from in-service branches only
    B = np.zeros((n_bus, n_bus))

    for br in branch:
        status = int(br[10])
        if status != 1:
            continue

        fbus = int(br[0])
        tbus = int(br[1])
        f = bus_num_to_idx[fbus]
        t = bus_num_to_idx[tbus]
        x = br[3]  # Reactance

        if x == 0:
            continue

        b = 1.0 / x
        B[f, f] += b
        B[t, t] += b
        B[f, t] -= b
        B[t, f] -= b

    # Convert P to per unit
    P_pu = P / baseMVA

    # Remove slack bus row/col and solve
    non_slack = [i for i in range(n_bus) if i != slack_idx]

    B_red = B[np.ix_(non_slack, non_slack)]
    P_red = P_pu[non_slack]

    # Solve B_red * theta_red = P_red
    theta_red = np.linalg.solve(B_red, P_red)

    # Reconstruct full theta vector with slack = 0
    theta = np.zeros(n_bus)
    for i, idx in enumerate(non_slack):
        theta[idx] = theta_red[i]
    theta[slack_idx] = 0.0

    return theta, bus_num_to_idx


def compute_edge_flow(critical_edge, branch, theta, baseMVA, bus_num_to_idx):
    """Compute MW flow on the critical edge using file direction."""
    u, v = critical_edge  # sorted (smaller, larger)

    # Find the in-service branch row that matches this edge
    selected_branch = None
    for br in branch:
        status = int(br[10])
        if status != 1:
            continue
        fbus = int(br[0])
        tbus = int(br[1])
        if (min(fbus, tbus), max(fbus, tbus)) == (u, v):
            selected_branch = br
            break  # Use first occurrence for determinism

    if selected_branch is None:
        raise ValueError(f"Critical edge {critical_edge} not found in in-service branches")

    fbus_file = int(selected_branch[0])
    tbus_file = int(selected_branch[1])
    x = selected_branch[3]

    f_idx = bus_num_to_idx[fbus_file]
    t_idx = bus_num_to_idx[tbus_file]

    flow_MW = (theta[f_idx] - theta[t_idx]) * (1.0 / x) * baseMVA

    return flow_MW


def process_case(filepath):
    """Process a single case file and return results."""
    basename = os.path.basename(filepath)

    # Parse the file
    baseMVA, bus, gen, branch = parse_matpower_file(filepath)
    n_bus = len(bus)

    # Build NetworkX graph
    G, n_branch_in_service = build_networkx_graph(bus, branch)

    # Find critical edge (max edge betweenness)
    critical_edge, critical_bc = find_critical_edge(G)

    # Run DC power flow
    theta, bus_num_to_idx = run_dc_power_flow(baseMVA, bus, gen, branch)

    # Compute flow on critical edge
    flow_MW = compute_edge_flow(critical_edge, branch, theta, baseMVA, bus_num_to_idx)

    return {
        'case_file': basename,
        'n_bus': n_bus,
        'n_branch_in_service': n_branch_in_service,
        'critical_edge_fbus': critical_edge[0],
        'critical_edge_tbus': critical_edge[1],
        'critical_edge_edge_betweenness': critical_bc,
        'critical_edge_flow_MW': flow_MW
    }


def create_excel_report(results, output_path):
    """Create the Excel report with proper styling."""
    wb = Workbook()
    ws = wb.active
    ws.title = "Summary"

    # Define headers
    headers = [
        'case_file',
        'n_bus',
        'n_branch_in_service',
        'critical_edge_fbus',
        'critical_edge_tbus',
        'critical_edge_edge_betweenness',
        'critical_edge_flow_MW'
    ]

    # Style definitions
    header_font = Font(bold=True, color='000000')  # Bold black
    header_fill = PatternFill('solid', fgColor='D9D9D9')  # Light gray
    blue_font = Font(color='0000FF')  # Blue for numeric inputs

    # Write header row
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.font = header_font
        cell.fill = header_fill

    # Write data rows
    for row_idx, result in enumerate(results, 2):
        for col_idx, header in enumerate(headers, 1):
            value = result[header]
            cell = ws.cell(row=row_idx, column=col_idx, value=value)

            # Apply blue font to numeric cells (all except case_file)
            if isinstance(value, (int, float, np.integer, np.floating)):
                cell.font = blue_font

    # Adjust column widths for readability
    ws.column_dimensions['A'].width = 28  # case_file
    ws.column_dimensions['B'].width = 8   # n_bus
    ws.column_dimensions['C'].width = 20  # n_branch_in_service
    ws.column_dimensions['D'].width = 18  # critical_edge_fbus
    ws.column_dimensions['E'].width = 18  # critical_edge_tbus
    ws.column_dimensions['F'].width = 30  # critical_edge_edge_betweenness
    ws.column_dimensions['G'].width = 22  # critical_edge_flow_MW

    wb.save(output_path)
    print(f"Excel report saved to: {output_path}")


def main():
    results = []

    for case_file in CASE_FILES:
        filepath = os.path.join(INPUT_DIR, case_file)
        print(f"Processing {case_file}...")
        result = process_case(filepath)
        results.append(result)
        print(f"  n_bus: {result['n_bus']}")
        print(f"  n_branch_in_service: {result['n_branch_in_service']}")
        print(f"  Critical edge: ({result['critical_edge_fbus']}, {result['critical_edge_tbus']})")
        print(f"  Edge betweenness: {result['critical_edge_edge_betweenness']:.10f}")
        print(f"  Flow MW: {result['critical_edge_flow_MW']:.6f}")

    # Create Excel report
    output_path = os.path.join(OUTPUT_DIR, "critical_edge_dcflow_report.xlsx")
    create_excel_report(results, output_path)


if __name__ == "__main__":
    main()
PYTHON_SCRIPT_EOF

# Run the main analysis script to generate the Excel output
echo "Running analysis script..."
python3 analysis_script.py

echo ""
echo "=== Output verification ==="
ls -la /root/critical_edge_dcflow_report.xlsx

echo ""
echo "=== Excel contents ==="
python3 -c "
import pandas as pd
df = pd.read_excel('/root/critical_edge_dcflow_report.xlsx', sheet_name='Summary')
print(df.to_string(index=False))
"

echo ""
echo "solve.sh completed successfully"

# HARBOR_OUTPUT_FIX_START
if [ -f "/root/harbor_workspaces/task_T228_run2/output/critical_edge_dcflow_report.xlsx" ]; then cp -f "/root/harbor_workspaces/task_T228_run2/output/critical_edge_dcflow_report.xlsx" "/root/critical_edge_dcflow_report.xlsx"; fi
# HARBOR_OUTPUT_FIX_END
