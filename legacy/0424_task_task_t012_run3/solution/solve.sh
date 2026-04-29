#!/bin/bash
set -e
mkdir -p /root/output
# Create the solution Python script using heredoc
cat << 'EOF' > /root/solve_task.py
#!/usr/bin/env python3
"""
Deterministic critical line identifier combining DC power flow and graph-theoretic criticality.
"""

import re
import json
import numpy as np
import networkx as nx

INPUT_DIR = '/root'
OUTPUT_PATH = '/root/output/most_critical_branch.json'

CASES = [
    ('case57', f'{INPUT_DIR}/case57.m'),
    ('case118', f'{INPUT_DIR}/case118.m'),
    ('pglib_opf_case118_ieee', f'{INPUT_DIR}/pglib_opf_case118_ieee.m')
]


def parse_matpower_case(filepath):
    """Parse a MATPOWER .m case file and extract bus, gen, branch, and baseMVA data."""
    with open(filepath, 'r') as f:
        content = f.read()

    # Extract baseMVA
    basemva_match = re.search(r'mpc\.baseMVA\s*=\s*(\d+\.?\d*)', content)
    baseMVA = float(basemva_match.group(1)) if basemva_match else 100.0

    def extract_matrix(content, name):
        """Extract a MATPOWER matrix from content."""
        pattern = rf'mpc\.{name}\s*=\s*\[(.*?)\];'
        match = re.search(pattern, content, re.DOTALL)
        if not match:
            return np.array([])

        matrix_str = match.group(1)
        rows = []
        for line in matrix_str.strip().split('\n'):
            line = re.sub(r'%.*', '', line).strip()
            line = re.sub(r';$', '', line).strip()
            if not line:
                continue
            values = []
            for part in line.split():
                try:
                    values.append(float(part))
                except ValueError:
                    continue
            if values:
                rows.append(values)

        return np.array(rows) if rows else np.array([])

    return {
        'baseMVA': baseMVA,
        'bus': extract_matrix(content, 'bus'),
        'gen': extract_matrix(content, 'gen'),
        'branch': extract_matrix(content, 'branch')
    }


def solve_dc_power_flow(mpc):
    """Solve DC power flow for a MATPOWER case."""
    bus = mpc['bus']
    gen = mpc['gen']
    branch = mpc['branch']
    baseMVA = mpc['baseMVA']

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

    # Build susceptance matrix B (only for in-service branches with x != 0)
    B = np.zeros((n_bus, n_bus))
    eligible_branches = []

    for br_idx, br in enumerate(branch):
        fbus_num = int(br[0])
        tbus_num = int(br[1])
        x = float(br[3])  # reactance
        status = int(br[10]) if len(br) > 10 else 1

        if status == 0 or x == 0:
            continue

        f = bus_num_to_idx[fbus_num]
        t = bus_num_to_idx[tbus_num]
        b = 1.0 / x

        B[f, f] += b
        B[t, t] += b
        B[f, t] -= b
        B[t, f] -= b

        eligible_branches.append({
            'idx': br_idx,
            'fbus': fbus_num,
            'tbus': tbus_num,
            'x': x,
            'b': b,
            'f_idx': f,
            't_idx': t
        })

    # Compute net injections P (in per-unit)
    P = np.zeros(n_bus)

    # Subtract load (Pd) from each bus
    for i in range(n_bus):
        Pd_mw = bus[i, 2]
        P[i] = -Pd_mw / baseMVA

    # Add generation (Pg) from each generator
    for g in gen:
        gen_bus_num = int(g[0])
        Pg_mw = g[1]
        gen_status = int(g[7]) if len(g) > 7 else 1
        if gen_status == 1:
            idx = bus_num_to_idx[gen_bus_num]
            P[idx] += Pg_mw / baseMVA

    # Solve DC power flow by removing slack bus equation
    B_red = np.delete(np.delete(B, slack_idx, axis=0), slack_idx, axis=1)
    P_red = np.delete(P, slack_idx)

    theta_red = np.linalg.solve(B_red, P_red)

    # Reconstruct full theta with slack angle = 0
    theta = np.zeros(n_bus)
    theta[:slack_idx] = theta_red[:slack_idx]
    theta[slack_idx] = 0.0
    theta[slack_idx+1:] = theta_red[slack_idx:]

    return theta, bus_num_to_idx, slack_idx, eligible_branches


def compute_branch_flows(eligible_branches, theta, baseMVA):
    """Compute MW flow on every eligible branch."""
    flows = []
    for br in eligible_branches:
        f_idx = br['f_idx']
        t_idx = br['t_idx']
        b = br['b']

        flow_pu = b * (theta[f_idx] - theta[t_idx])
        flow_mw = flow_pu * baseMVA

        flows.append({
            'fbus': br['fbus'],
            'tbus': br['tbus'],
            'flow_mw': flow_mw,
            'abs_flow_mw': abs(flow_mw)
        })

    return flows


def build_topology_graph(eligible_branches):
    """Build an undirected NetworkX graph from eligible branches."""
    G = nx.Graph()
    for br in eligible_branches:
        G.add_edge(br['fbus'], br['tbus'])
    return G


def compute_criticality_scores(case_name, mpc):
    """Compute criticality scores for all eligible branches in a case."""
    theta, bus_num_to_idx, slack_idx, eligible_branches = solve_dc_power_flow(mpc)
    flows = compute_branch_flows(eligible_branches, theta, mpc['baseMVA'])
    G = build_topology_graph(eligible_branches)
    eb = nx.edge_betweenness_centrality(G)

    records = []
    for i, flow in enumerate(flows):
        fbus = flow['fbus']
        tbus = flow['tbus']
        abs_flow_mw = flow['abs_flow_mw']

        # Normalize edge key for lookup (undirected graph uses sorted tuple)
        edge_key = (min(fbus, tbus), max(fbus, tbus))
        edge_betweenness = eb.get(edge_key, 0.0)

        score = abs_flow_mw * edge_betweenness

        records.append({
            'case_name': case_name,
            'fbus': fbus,
            'tbus': tbus,
            'abs_flow_mw': abs_flow_mw,
            'edge_betweenness': edge_betweenness,
            'score': score
        })

    return records


def find_most_critical_branch(all_records):
    """
    Find the single branch with maximum criticality score.

    Tie-break order:
    1) higher score
    2) higher abs_flow_mw
    3) lexicographically smaller case_name
    4) smaller fbus
    5) smaller tbus
    """
    sorted_records = sorted(
        all_records,
        key=lambda r: (-r['score'], -r['abs_flow_mw'], r['case_name'], r['fbus'], r['tbus'])
    )
    return sorted_records[0]


def main():
    all_records = []

    for case_name, filepath in CASES:
        mpc = parse_matpower_case(filepath)
        records = compute_criticality_scores(case_name, mpc)
        all_records.extend(records)

    winner = find_most_critical_branch(all_records)

    output = {
        'case_name': winner['case_name'],
        'fbus': winner['fbus'],
        'tbus': winner['tbus'],
        'abs_flow_mw': winner['abs_flow_mw'],
        'edge_betweenness': winner['edge_betweenness'],
        'score': winner['score']
    }

    with open(OUTPUT_PATH, 'w') as f:
        json.dump(output, f, indent=2)


if __name__ == '__main__':
    main()
EOF

# Execute the script
python3 /root/solve_task.py
