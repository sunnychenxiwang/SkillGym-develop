#!/bin/bash
set -e

# HARBOR_RUNTIME_PATH_FIX: align synthetic workspace paths with Harbor runtime layout
TASK_DIR="$(grep -Eo '/root/harbor_workspaces/task_[A-Za-z0-9_]+' "$0" | head -n1 || true)"
if [ -n "$TASK_DIR" ]; then
  mkdir -p "$TASK_DIR"
  [ -e "$TASK_DIR/input" ] || ln -s /root "$TASK_DIR/input"
  mkdir -p "$TASK_DIR/output"
  for d in .claude .codex .opencode .goose .factory .agents .gemini; do
    [ -e "$TASK_DIR/$d" ] || ln -s "/root/$d" "$TASK_DIR/$d"
  done
  cd "$TASK_DIR"
fi

if [ -d /root/.claude/skills/dc-power-flow/scripts ]; then
  export PYTHONPATH="/root/.claude/skills/dc-power-flow/scripts:${PYTHONPATH:-}"
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
ls -la /root/harbor_workspaces/task_T406_run1/output 2>/dev/null || mkdir -p /root/harbor_workspaces/task_T406_run1/output && echo "Output directory ready"

# Create /root/harbor_workspaces/task_T406_run1/dc_power_flow_analysis.py
mkdir -p $(dirname /root/harbor_workspaces/task_T406_run1/dc_power_flow_analysis.py)
cat << 'HEREDOC_EOF' > /root/harbor_workspaces/task_T406_run1/dc_power_flow_analysis.py
#!/usr/bin/env python3
"""DC Power Flow Analysis for Critical Corridor Identification"""

import sys
import re
import numpy as np
import pandas as pd

sys.path.insert(0, '/root/harbor_workspaces/task_T406_run1/.claude/skills/dc-power-flow/scripts')
from build_b_matrix import build_susceptance_matrix


def parse_matpower_file(filepath):
    """Parse MATPOWER .m file and extract bus, gen, branch data and baseMVA."""
    with open(filepath, 'r') as f:
        content = f.read()

    # Extract baseMVA
    basemva_match = re.search(r'mpc\.baseMVA\s*=\s*([\d.]+)', content)
    baseMVA = float(basemva_match.group(1)) if basemva_match else 100.0

    def extract_matrix(name):
        pattern = rf'mpc\.{name}\s*=\s*\[(.*?)\];'
        match = re.search(pattern, content, re.DOTALL)
        if not match:
            return None
        matrix_str = match.group(1)
        # Remove MATLAB comments
        lines = []
        for line in matrix_str.split('\n'):
            line = re.sub(r'%.*', '', line).strip()
            if line and line != ';':
                # Split by semicolons for MATLAB row notation
                for part in line.split(';'):
                    part = part.strip()
                    if part:
                        values = part.split()
                        if values:
                            try:
                                row = [float(v) for v in values]
                                lines.append(row)
                            except ValueError:
                                continue
        return np.array(lines) if lines else None

    bus = extract_matrix('bus')
    gen = extract_matrix('gen')
    branch = extract_matrix('branch')

    return baseMVA, bus, gen, branch


def run_dc_power_flow(baseMVA, bus, gen, branch, case_name):
    """Run DC power flow and return results."""
    nbus = bus.shape[0]

    # Create bus number to index mapping (handles non-contiguous bus numbering)
    bus_ids = bus[:, 0].astype(int)
    bus_num_to_idx = {int(bus_ids[i]): i for i in range(nbus)}

    # Find slack bus (type 3, lowest bus_i if multiple)
    type3_buses = bus[bus[:, 1] == 3, 0].astype(int)
    if len(type3_buses) == 0:
        raise ValueError(f"No slack bus (type 3) found in {case_name}")
    slack_bus_id = min(type3_buses)
    slack_idx = bus_num_to_idx[slack_bus_id]

    # Compute net injections P (per-unit)
    # Load: Pd from bus data (column 2)
    Pd = bus[:, 2]  # MW

    # Generation: sum Pg from gen data at each bus
    Pg_sum = np.zeros(nbus)
    for g in gen:
        gen_bus = int(g[0])
        gen_pg = g[1]  # MW
        # Check generator status if available (column 7 in MATPOWER)
        if gen.shape[1] > 7:
            gen_status = g[7]
            if gen_status == 0:
                continue  # Skip offline generators
        if gen_bus in bus_num_to_idx:
            idx = bus_num_to_idx[gen_bus]
            Pg_sum[idx] += gen_pg

    # Net injection (MW) and per-unit
    P_MW = Pg_sum - Pd
    P = P_MW / baseMVA  # per-unit

    # Build susceptance matrix B (only for in-service branches with x != 0)
    B = np.zeros((nbus, nbus))
    valid_branches = []  # Track valid branches for flow calculation

    for br in branch:
        fbus = int(br[0])
        tbus = int(br[1])
        x = br[3]  # reactance
        status = br[10] if branch.shape[1] > 10 else 1  # status column

        # Skip out-of-service branches
        if status == 0:
            continue
        # Skip branches with x = 0
        if x == 0:
            continue

        f_idx = bus_num_to_idx[fbus]
        t_idx = bus_num_to_idx[tbus]
        b = 1.0 / x

        B[f_idx, f_idx] += b
        B[t_idx, t_idx] += b
        B[f_idx, t_idx] -= b
        B[t_idx, f_idx] -= b

        valid_branches.append((fbus, tbus, x, f_idx, t_idx))

    # Solve DC power flow: B_red * theta_red = P_red (with slack removed)
    mask = np.ones(nbus, dtype=bool)
    mask[slack_idx] = False

    B_red = B[np.ix_(mask, mask)]
    P_red = P[mask]

    # Solve
    theta_red = np.linalg.solve(B_red, P_red)

    # Reconstruct full theta with slack = 0
    theta = np.zeros(nbus)
    theta[mask] = theta_red
    theta[slack_idx] = 0.0

    # Verify residual
    residual = np.max(np.abs(B_red @ theta_red - P_red))
    if residual > 1e-6:
        print(f"Warning: Large residual in {case_name}: {residual}")

    # Compute branch flows and find top flow
    top_abs_flow = 0.0
    top_fbus = None
    top_tbus = None
    top_flow_signed = None

    for fbus, tbus, x, f_idx, t_idx in valid_branches:
        b = 1.0 / x
        flow_signed = (theta[f_idx] - theta[t_idx]) * b * baseMVA  # MW
        abs_flow = abs(flow_signed)

        if abs_flow > top_abs_flow:
            top_abs_flow = abs_flow
            top_fbus = fbus
            top_tbus = tbus
            top_flow_signed = flow_signed

    # Corridor key (undirected)
    corridor_key = (min(top_fbus, top_tbus), max(top_fbus, top_tbus))

    return {
        'case': case_name,
        'top_fbus': top_fbus,
        'top_tbus': top_tbus,
        'top_abs_flow_mw': top_abs_flow,
        'top_flow_mw_signed': top_flow_signed,
        'baseMVA': baseMVA,
        'corridor_key': corridor_key,
        'slack_bus': slack_bus_id,
        'nbus': nbus,
        'nbranch': len(valid_branches)
    }


def main():
    # Define case files
    cases = [
        ('/root/case57.m', 'case57'),
        ('/root/case118.m', 'case118'),
        ('/root/pglib_opf_case118_ieee.m', 'pglib118'),
    ]

    results = []

    for filepath, case_name in cases:
        print(f"\nProcessing {case_name}...")
        baseMVA, bus, gen, branch = parse_matpower_file(filepath)
        print(f"  baseMVA: {baseMVA}, buses: {bus.shape[0]}, branches: {branch.shape[0]}")

        result = run_dc_power_flow(baseMVA, bus, gen, branch, case_name)
        print(f"  Slack bus: {result['slack_bus']}")
        print(f"  Top flow branch: {result['top_fbus']}->{result['top_tbus']}")
        print(f"  Top abs flow: {result['top_abs_flow_mw']:.2f} MW")
        print(f"  Corridor key: {result['corridor_key']}")
        results.append(result)

    # Find unique corridor appearing in at least 2 cases
    corridor_counts = {}
    corridor_cases = {}

    for r in results:
        ck = r['corridor_key']
        corridor_counts[ck] = corridor_counts.get(ck, 0) + 1
        if ck not in corridor_cases:
            corridor_cases[ck] = []
        corridor_cases[ck].append(r['case'])

    print("\n\nCorridor counts:")
    for ck, count in corridor_counts.items():
        print(f"  {ck}: {count} cases - {corridor_cases[ck]}")

    # Find corridor appearing in >= 2 cases
    critical_corridors = [(ck, count, corridor_cases[ck])
                         for ck, count in corridor_counts.items() if count >= 2]

    if len(critical_corridors) != 1:
        print(f"\nWarning: Expected exactly 1 corridor with >= 2 cases, found {len(critical_corridors)}")
        if len(critical_corridors) == 0:
            print("No corridor found in multiple cases - using most common or first")
            # Fallback: use the first corridor
            critical_corridor = list(corridor_counts.keys())[0]
            critical_cases = corridor_cases[critical_corridor]
        else:
            critical_corridor = critical_corridors[0][0]
            critical_cases = critical_corridors[0][2]
    else:
        critical_corridor = critical_corridors[0][0]
        critical_cases = critical_corridors[0][2]

    print(f"\nCritical corridor: {critical_corridor}")
    print(f"Cases: {critical_cases}")

    # Create Excel workbook
    output_path = '/root/critical_corridor.xlsx'

    # Result sheet - one row
    result_df = pd.DataFrame([{
        'corridor_fbus': critical_corridor[0],
        'corridor_tbus': critical_corridor[1],
        'cases_where_topflow': ','.join(sorted(critical_cases))
    }])

    # Evidence sheet - one row per case
    evidence_data = []
    for r in results:
        evidence_data.append({
            'case': r['case'],
            'top_fbus': r['top_fbus'],
            'top_tbus': r['top_tbus'],
            'top_abs_flow_mw': r['top_abs_flow_mw'],
            'top_flow_mw_signed': r['top_flow_mw_signed'],
            'baseMVA': r['baseMVA']
        })
    evidence_df = pd.DataFrame(evidence_data)

    # Write to Excel
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        result_df.to_excel(writer, sheet_name='result', index=False)
        evidence_df.to_excel(writer, sheet_name='evidence', index=False)

    print(f"\nExcel file saved to: {output_path}")

    # Verify
    print("\nVerification:")
    from openpyxl import load_workbook
    wb = load_workbook(output_path)
    print(f"  Sheets: {wb.sheetnames}")
    print(f"  Result sheet rows: {wb['result'].max_row - 1}")  # minus header
    print(f"  Evidence sheet rows: {wb['evidence'].max_row - 1}")  # minus header

    return results


if __name__ == '__main__':
    main()

HEREDOC_EOF

# Execute command
python dc_power_flow_analysis.py

# Execute command
python -c "
import pandas as pd

# Read and display both sheets
result_df = pd.read_excel('output/critical_corridor.xlsx', sheet_name='result')
evidence_df = pd.read_excel('output/critical_corridor.xlsx', sheet_name='evidence')

print('=== RESULT SHEET ===')
print(result_df.to_string(index=False))
print()
print('Columns:', list(result_df.columns))
print('Row count:', len(result_df))

print()
print('=== EVIDENCE SHEET ===')
print(evidence_df.to_string(index=False))
print()
print('Columns:', list(evidence_df.columns))
print('Row count:', len(evidence_df))
"


# Execute command
ls -la /root/critical_corridor.xlsx

# Create /root/harbor_workspaces/task_T406_run1/expectation_tests.py
mkdir -p $(dirname /root/harbor_workspaces/task_T406_run1/expectation_tests.py)
cat << 'HEREDOC_EOF' > /root/harbor_workspaces/task_T406_run1/expectation_tests.py
"""Auto-generated expectation tests for task verification.

These tests verify that the task execution produces correct outputs
based on the instruction requirements for computing critical corridor rankings
from MATPOWER case files using DC power flow analysis.
"""

import os
from pathlib import Path

import pandas as pd
import pytest


# Constants
OUTPUT_FILE = "/root/critical_corridor.xlsx"
EXPECTED_CASES = {"case57", "case118", "pglib118"}
VALID_BASEMVA_VALUES = {100.0, 100}  # Both case files use baseMVA = 100


class TestOutputFileExists:
    """Tests for output file existence and basic validity."""

    def test_output_directory_exists(self):
        """Verify output directory exists."""
        output_dir = Path(OUTPUT_FILE).parent
        assert output_dir.exists(), f"Output directory not found: {output_dir}"

    def test_output_file_exists(self):
        """Verify output Excel file was created at exact path."""
        assert os.path.exists(OUTPUT_FILE), f"Output file not found: {OUTPUT_FILE}"

    def test_output_file_not_empty(self):
        """Verify output file is not empty."""
        file_size = os.path.getsize(OUTPUT_FILE)
        assert file_size > 0, "Output file is empty"

    def test_output_file_is_valid_xlsx(self):
        """Verify output file is a valid Excel file."""
        try:
            excel_file = pd.ExcelFile(OUTPUT_FILE)
            assert excel_file is not None
        except Exception as e:
            pytest.fail(f"Output file is not a valid Excel file: {e}")


class TestResultSheet:
    """Tests for the 'result' sheet structure and content."""

    @pytest.fixture
    def result_df(self):
        """Load the result sheet from the Excel file."""
        return pd.read_excel(OUTPUT_FILE, sheet_name="result")

    def test_result_sheet_exists(self):
        """Verify 'result' sheet exists in the workbook."""
        excel_file = pd.ExcelFile(OUTPUT_FILE)
        assert "result" in excel_file.sheet_names, (
            f"'result' sheet not found. Available sheets: {excel_file.sheet_names}"
        )

    def test_result_sheet_has_exactly_one_data_row(self, result_df):
        """Verify result sheet has exactly one row of data."""
        assert len(result_df) == 1, f"Expected 1 row in result sheet, got {len(result_df)}"

    def test_result_sheet_has_corridor_fbus_column(self, result_df):
        """Verify 'corridor_fbus' column exists."""
        assert "corridor_fbus" in result_df.columns, (
            f"'corridor_fbus' column not found. Columns: {list(result_df.columns)}"
        )

    def test_result_sheet_has_corridor_tbus_column(self, result_df):
        """Verify 'corridor_tbus' column exists."""
        assert "corridor_tbus" in result_df.columns, (
            f"'corridor_tbus' column not found. Columns: {list(result_df.columns)}"
        )

    def test_result_sheet_has_cases_where_topflow_column(self, result_df):
        """Verify 'cases_where_topflow' column exists."""
        assert "cases_where_topflow" in result_df.columns, (
            f"'cases_where_topflow' column not found. Columns: {list(result_df.columns)}"
        )

    def test_corridor_fbus_is_integer(self, result_df):
        """Verify corridor_fbus is an integer value."""
        fbus = result_df["corridor_fbus"].iloc[0]
        assert pd.notna(fbus), "corridor_fbus is null/NaN"
        # Check if it's a whole number (int or float that represents int)
        assert float(fbus) == int(fbus), f"corridor_fbus is not an integer: {fbus}"

    def test_corridor_tbus_is_integer(self, result_df):
        """Verify corridor_tbus is an integer value."""
        tbus = result_df["corridor_tbus"].iloc[0]
        assert pd.notna(tbus), "corridor_tbus is null/NaN"
        assert float(tbus) == int(tbus), f"corridor_tbus is not an integer: {tbus}"

    def test_corridor_fbus_less_than_tbus(self, result_df):
        """Verify corridor_fbus < corridor_tbus (undirected corridor key)."""
        fbus = int(result_df["corridor_fbus"].iloc[0])
        tbus = int(result_df["corridor_tbus"].iloc[0])
        assert fbus < tbus, (
            f"corridor_fbus ({fbus}) must be less than corridor_tbus ({tbus})"
        )

    def test_corridor_fbus_is_positive(self, result_df):
        """Verify corridor_fbus is a positive bus number."""
        fbus = int(result_df["corridor_fbus"].iloc[0])
        assert fbus > 0, f"corridor_fbus must be positive: {fbus}"

    def test_corridor_tbus_is_positive(self, result_df):
        """Verify corridor_tbus is a positive bus number."""
        tbus = int(result_df["corridor_tbus"].iloc[0])
        assert tbus > 0, f"corridor_tbus must be positive: {tbus}"

    def test_cases_where_topflow_is_string(self, result_df):
        """Verify cases_where_topflow is a string."""
        cases = result_df["cases_where_topflow"].iloc[0]
        assert pd.notna(cases), "cases_where_topflow is null/NaN"
        assert isinstance(cases, str), f"cases_where_topflow must be a string: {type(cases)}"

    def test_cases_where_topflow_contains_valid_cases(self, result_df):
        """Verify cases_where_topflow contains only valid case names."""
        cases_str = result_df["cases_where_topflow"].iloc[0]
        cases_list = [c.strip() for c in cases_str.split(",")]
        for case in cases_list:
            assert case in EXPECTED_CASES, (
                f"Invalid case name '{case}'. Valid cases: {EXPECTED_CASES}"
            )

    def test_cases_where_topflow_has_at_least_two_cases(self, result_df):
        """Verify corridor appears in at least 2 cases (per task requirement)."""
        cases_str = result_df["cases_where_topflow"].iloc[0]
        cases_list = [c.strip() for c in cases_str.split(",")]
        assert len(cases_list) >= 2, (
            f"Corridor must appear in at least 2 cases, found: {len(cases_list)}"
        )


class TestEvidenceSheet:
    """Tests for the 'evidence' sheet structure and content."""

    @pytest.fixture
    def evidence_df(self):
        """Load the evidence sheet from the Excel file."""
        return pd.read_excel(OUTPUT_FILE, sheet_name="evidence")

    def test_evidence_sheet_exists(self):
        """Verify 'evidence' sheet exists in the workbook."""
        excel_file = pd.ExcelFile(OUTPUT_FILE)
        assert "evidence" in excel_file.sheet_names, (
            f"'evidence' sheet not found. Available sheets: {excel_file.sheet_names}"
        )

    def test_evidence_sheet_has_three_rows(self, evidence_df):
        """Verify evidence sheet has exactly 3 rows (one per case)."""
        assert len(evidence_df) == 3, (
            f"Expected 3 rows in evidence sheet (one per case), got {len(evidence_df)}"
        )

    def test_evidence_sheet_has_case_column(self, evidence_df):
        """Verify 'case' column exists."""
        assert "case" in evidence_df.columns, (
            f"'case' column not found. Columns: {list(evidence_df.columns)}"
        )

    def test_evidence_sheet_has_top_fbus_column(self, evidence_df):
        """Verify 'top_fbus' column exists."""
        assert "top_fbus" in evidence_df.columns, (
            f"'top_fbus' column not found. Columns: {list(evidence_df.columns)}"
        )

    def test_evidence_sheet_has_top_tbus_column(self, evidence_df):
        """Verify 'top_tbus' column exists."""
        assert "top_tbus" in evidence_df.columns, (
            f"'top_tbus' column not found. Columns: {list(evidence_df.columns)}"
        )

    def test_evidence_sheet_has_top_abs_flow_mw_column(self, evidence_df):
        """Verify 'top_abs_flow_mw' column exists."""
        assert "top_abs_flow_mw" in evidence_df.columns, (
            f"'top_abs_flow_mw' column not found. Columns: {list(evidence_df.columns)}"
        )

    def test_evidence_sheet_has_top_flow_mw_signed_column(self, evidence_df):
        """Verify 'top_flow_mw_signed' column exists."""
        assert "top_flow_mw_signed" in evidence_df.columns, (
            f"'top_flow_mw_signed' column not found. Columns: {list(evidence_df.columns)}"
        )

    def test_evidence_sheet_has_basemva_column(self, evidence_df):
        """Verify 'baseMVA' column exists."""
        assert "baseMVA" in evidence_df.columns, (
            f"'baseMVA' column not found. Columns: {list(evidence_df.columns)}"
        )

    def test_evidence_contains_all_three_cases(self, evidence_df):
        """Verify evidence sheet contains entries for all three cases."""
        case_names = set(evidence_df["case"].tolist())
        assert case_names == EXPECTED_CASES, (
            f"Expected cases {EXPECTED_CASES}, found {case_names}"
        )

    def test_all_top_fbus_are_positive_integers(self, evidence_df):
        """Verify all top_fbus values are positive integers."""
        for idx, row in evidence_df.iterrows():
            fbus = row["top_fbus"]
            assert pd.notna(fbus), f"top_fbus is null at row {idx}"
            assert float(fbus) == int(fbus), f"top_fbus is not an integer at row {idx}: {fbus}"
            assert int(fbus) > 0, f"top_fbus must be positive at row {idx}: {fbus}"

    def test_all_top_tbus_are_positive_integers(self, evidence_df):
        """Verify all top_tbus values are positive integers."""
        for idx, row in evidence_df.iterrows():
            tbus = row["top_tbus"]
            assert pd.notna(tbus), f"top_tbus is null at row {idx}"
            assert float(tbus) == int(tbus), f"top_tbus is not an integer at row {idx}: {tbus}"
            assert int(tbus) > 0, f"top_tbus must be positive at row {idx}: {tbus}"

    def test_all_top_abs_flow_mw_are_non_negative(self, evidence_df):
        """Verify all top_abs_flow_mw values are non-negative (absolute values)."""
        for idx, row in evidence_df.iterrows():
            abs_flow = row["top_abs_flow_mw"]
            assert pd.notna(abs_flow), f"top_abs_flow_mw is null at row {idx}"
            assert abs_flow >= 0, f"top_abs_flow_mw must be non-negative at row {idx}: {abs_flow}"

    def test_all_top_flow_mw_signed_are_numeric(self, evidence_df):
        """Verify all top_flow_mw_signed values are numeric."""
        for idx, row in evidence_df.iterrows():
            signed_flow = row["top_flow_mw_signed"]
            assert pd.notna(signed_flow), f"top_flow_mw_signed is null at row {idx}"
            assert isinstance(signed_flow, (int, float)), (
                f"top_flow_mw_signed must be numeric at row {idx}: {type(signed_flow)}"
            )

    def test_abs_flow_matches_signed_flow_absolute_value(self, evidence_df):
        """Verify top_abs_flow_mw equals abs(top_flow_mw_signed)."""
        for idx, row in evidence_df.iterrows():
            abs_flow = row["top_abs_flow_mw"]
            signed_flow = row["top_flow_mw_signed"]
            expected_abs = abs(signed_flow)
            # Use relative tolerance for floating point comparison
            assert abs(abs_flow - expected_abs) < 1e-6, (
                f"top_abs_flow_mw ({abs_flow}) doesn't match abs(top_flow_mw_signed) "
                f"({expected_abs}) at row {idx}"
            )

    def test_all_basemva_are_positive(self, evidence_df):
        """Verify all baseMVA values are positive."""
        for idx, row in evidence_df.iterrows():
            basemva = row["baseMVA"]
            assert pd.notna(basemva), f"baseMVA is null at row {idx}"
            assert basemva > 0, f"baseMVA must be positive at row {idx}: {basemva}"

    def test_basemva_values_are_valid(self, evidence_df):
        """Verify baseMVA values match expected values from case files (100)."""
        for idx, row in evidence_df.iterrows():
            basemva = row["baseMVA"]
            # All three case files use baseMVA = 100
            assert basemva == 100 or basemva == 100.0, (
                f"baseMVA should be 100 for all cases at row {idx}: {basemva}"
            )


class TestCorridorConsistency:
    """Tests for consistency between result and evidence sheets."""

    @pytest.fixture
    def result_df(self):
        """Load the result sheet from the Excel file."""
        return pd.read_excel(OUTPUT_FILE, sheet_name="result")

    @pytest.fixture
    def evidence_df(self):
        """Load the evidence sheet from the Excel file."""
        return pd.read_excel(OUTPUT_FILE, sheet_name="evidence")

    def test_critical_corridor_appears_in_evidence(self, result_df, evidence_df):
        """Verify the critical corridor from result sheet appears in evidence sheet."""
        corridor_fbus = int(result_df["corridor_fbus"].iloc[0])
        corridor_tbus = int(result_df["corridor_tbus"].iloc[0])

        # Check if this corridor appears as a top-flow branch in evidence
        matching_rows = []
        for _, row in evidence_df.iterrows():
            fbus = int(row["top_fbus"])
            tbus = int(row["top_tbus"])
            # Normalize to undirected corridor (min, max)
            normalized = (min(fbus, tbus), max(fbus, tbus))
            if normalized == (corridor_fbus, corridor_tbus):
                matching_rows.append(row["case"])

        # The corridor should appear in at least 2 cases
        assert len(matching_rows) >= 2, (
            f"Critical corridor ({corridor_fbus}, {corridor_tbus}) should appear in "
            f"at least 2 cases in evidence, found in: {matching_rows}"
        )

    def test_cases_where_topflow_matches_evidence(self, result_df, evidence_df):
        """Verify cases_where_topflow matches actual cases in evidence."""
        corridor_fbus = int(result_df["corridor_fbus"].iloc[0])
        corridor_tbus = int(result_df["corridor_tbus"].iloc[0])
        cases_str = result_df["cases_where_topflow"].iloc[0]
        claimed_cases = set(c.strip() for c in cases_str.split(","))

        # Find actual cases where this corridor is the top-flow branch
        actual_cases = set()
        for _, row in evidence_df.iterrows():
            fbus = int(row["top_fbus"])
            tbus = int(row["top_tbus"])
            normalized = (min(fbus, tbus), max(fbus, tbus))
            if normalized == (corridor_fbus, corridor_tbus):
                actual_cases.add(row["case"])

        assert claimed_cases == actual_cases, (
            f"cases_where_topflow ({claimed_cases}) doesn't match evidence ({actual_cases})"
        )


class TestFlowValueReasonableness:
    """Tests for reasonable power flow values."""

    @pytest.fixture
    def evidence_df(self):
        """Load the evidence sheet from the Excel file."""
        return pd.read_excel(OUTPUT_FILE, sheet_name="evidence")

    def test_top_flows_are_within_reasonable_range(self, evidence_df):
        """Verify top flow values are within reasonable range for these systems."""
        # IEEE 57-bus and 118-bus systems typically have flows in 0-500+ MW range
        # The highest flow in any case shouldn't exceed total system generation
        MAX_REASONABLE_FLOW = 2000  # MW - generous upper bound

        for idx, row in evidence_df.iterrows():
            abs_flow = row["top_abs_flow_mw"]
            assert abs_flow <= MAX_REASONABLE_FLOW, (
                f"Flow value {abs_flow} MW seems unreasonably high for case {row['case']}"
            )

    def test_top_flows_are_significant(self, evidence_df):
        """Verify top flow values are significant (not near-zero)."""
        # The top flow in any case should be a significant value, not near zero
        MIN_SIGNIFICANT_FLOW = 10  # MW - minimum expected for top flow

        for idx, row in evidence_df.iterrows():
            abs_flow = row["top_abs_flow_mw"]
            assert abs_flow >= MIN_SIGNIFICANT_FLOW, (
                f"Top flow value {abs_flow} MW seems too small for case {row['case']}"
            )


class TestBusNumberValidity:
    """Tests to verify bus numbers are valid for the respective case files."""

    @pytest.fixture
    def evidence_df(self):
        """Load the evidence sheet from the Excel file."""
        return pd.read_excel(OUTPUT_FILE, sheet_name="evidence")

    def test_case57_bus_numbers_in_valid_range(self, evidence_df):
        """Verify case57 bus numbers are within valid range (1-57)."""
        case57_row = evidence_df[evidence_df["case"] == "case57"]
        if len(case57_row) > 0:
            fbus = int(case57_row["top_fbus"].iloc[0])
            tbus = int(case57_row["top_tbus"].iloc[0])
            assert 1 <= fbus <= 57, f"case57 top_fbus {fbus} out of range [1, 57]"
            assert 1 <= tbus <= 57, f"case57 top_tbus {tbus} out of range [1, 57]"

    def test_case118_bus_numbers_in_valid_range(self, evidence_df):
        """Verify case118 bus numbers are within valid range (1-118)."""
        case118_row = evidence_df[evidence_df["case"] == "case118"]
        if len(case118_row) > 0:
            fbus = int(case118_row["top_fbus"].iloc[0])
            tbus = int(case118_row["top_tbus"].iloc[0])
            assert 1 <= fbus <= 118, f"case118 top_fbus {fbus} out of range [1, 118]"
            assert 1 <= tbus <= 118, f"case118 top_tbus {tbus} out of range [1, 118]"

    def test_pglib118_bus_numbers_in_valid_range(self, evidence_df):
        """Verify pglib118 bus numbers are within valid range (1-118)."""
        pglib118_row = evidence_df[evidence_df["case"] == "pglib118"]
        if len(pglib118_row) > 0:
            fbus = int(pglib118_row["top_fbus"].iloc[0])
            tbus = int(pglib118_row["top_tbus"].iloc[0])
            assert 1 <= fbus <= 118, f"pglib118 top_fbus {fbus} out of range [1, 118]"
            assert 1 <= tbus <= 118, f"pglib118 top_tbus {tbus} out of range [1, 118]"


class TestColumnOrder:
    """Tests to verify column ordering (optional but good for consistency)."""

    @pytest.fixture
    def result_df(self):
        """Load the result sheet from the Excel file."""
        return pd.read_excel(OUTPUT_FILE, sheet_name="result")

    @pytest.fixture
    def evidence_df(self):
        """Load the evidence sheet from the Excel file."""
        return pd.read_excel(OUTPUT_FILE, sheet_name="evidence")

    def test_result_has_all_required_columns(self, result_df):
        """Verify result sheet has all required columns."""
        required_columns = {"corridor_fbus", "corridor_tbus", "cases_where_topflow"}
        actual_columns = set(result_df.columns)
        missing = required_columns - actual_columns
        assert not missing, f"Missing required columns in result sheet: {missing}"

    def test_evidence_has_all_required_columns(self, evidence_df):
        """Verify evidence sheet has all required columns."""
        required_columns = {
            "case", "top_fbus", "top_tbus",
            "top_abs_flow_mw", "top_flow_mw_signed", "baseMVA"
        }
        actual_columns = set(evidence_df.columns)
        missing = required_columns - actual_columns
        assert not missing, f"Missing required columns in evidence sheet: {missing}"

HEREDOC_EOF

# Execute command
python -m py_compile expectation_tests.py && echo "Syntax check passed"

# Execute command
python -c "import pytest; import pandas as pd; from pathlib import Path; print('All imports successful')"
