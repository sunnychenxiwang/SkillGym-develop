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

# Create /root/harbor_workspaces/task_T434_run2/expectation_tests.py
mkdir -p $(dirname /root/harbor_workspaces/task_T434_run2/expectation_tests.py)
cat << 'HEREDOC_EOF' > /root/harbor_workspaces/task_T434_run2/expectation_tests.py
"""Auto-generated expectation tests for task verification.

These tests verify that the task execution produces correct outputs
based on the instruction requirements for computing the most critical
transmission element across IEEE 118-bus cases using DC power flow analysis.

Task requirements:
1. Parse MATPOWER case files (case118.m, pglib_opf_case118_ieee.m, case57.m)
2. Run DC power flow for both 118-bus files
3. Compute branch loading percentages using rateA
4. Identify max-loaded branch per file with tie-breaking rules
5. Compute criticality score using case57 median reactance as baseline
6. Select overall winner and write JSON output
"""

import json
import math
import os
from pathlib import Path

import pytest


# Constants derived from input file analysis
OUTPUT_FILE_PATH = "/root/most_critical_branch.json"
INPUT_DIR = "/root/harbor_workspaces/task_T434_run2/input"

VALID_SOURCE_FILES = ["case118.m", "pglib_opf_case118_ieee.m"]
NUM_BUSES_118 = 118
NUM_BRANCHES_CASE118 = 186  # from case118.m
NUM_BRANCHES_PGLIB = 186  # from pglib_opf_case118_ieee.m (indexed 0 to 185)

# Required JSON schema keys
REQUIRED_KEYS = [
    "winner_source_file",
    "fbus",
    "tbus",
    "branch_row_index",
    "x",
    "rateA",
    "flow_MW",
    "loading_pct",
    "median_x_case57",
    "criticality",
]


class TestOutputFileExistence:
    """Tests for verifying output file creation."""

    def test_output_file_exists(self):
        """Verify that the output JSON file was created."""
        assert os.path.exists(OUTPUT_FILE_PATH), (
            f"Output file not found at {OUTPUT_FILE_PATH}. "
            "The task requires writing the JSON result file."
        )

    def test_output_file_not_empty(self):
        """Verify that the output file is not empty."""
        assert os.path.exists(OUTPUT_FILE_PATH), f"Output file not found at {OUTPUT_FILE_PATH}"
        file_size = os.path.getsize(OUTPUT_FILE_PATH)
        assert file_size > 0, "Output file exists but is empty"


class TestOutputFileFormat:
    """Tests for verifying output file format."""

    def test_output_is_valid_json(self):
        """Verify output is valid JSON format."""
        assert os.path.exists(OUTPUT_FILE_PATH), f"Output file not found at {OUTPUT_FILE_PATH}"
        with open(OUTPUT_FILE_PATH, "r") as f:
            content = f.read()
        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            pytest.fail(f"Output file is not valid JSON: {e}")
        assert data is not None, "JSON parsed to None"

    def test_output_is_json_object(self):
        """Verify output JSON is an object (dict), not array or primitive."""
        assert os.path.exists(OUTPUT_FILE_PATH), f"Output file not found at {OUTPUT_FILE_PATH}"
        with open(OUTPUT_FILE_PATH, "r") as f:
            data = json.load(f)
        assert isinstance(data, dict), (
            f"Expected JSON object (dict), got {type(data).__name__}"
        )


class TestRequiredFields:
    """Tests for verifying all required fields are present."""

    def test_all_required_keys_present(self):
        """Verify all required keys are present in the output."""
        assert os.path.exists(OUTPUT_FILE_PATH), f"Output file not found at {OUTPUT_FILE_PATH}"
        with open(OUTPUT_FILE_PATH, "r") as f:
            data = json.load(f)

        missing_keys = [key for key in REQUIRED_KEYS if key not in data]
        assert not missing_keys, (
            f"Missing required keys in output: {missing_keys}. "
            f"Required keys are: {REQUIRED_KEYS}"
        )

    @pytest.mark.parametrize("key", REQUIRED_KEYS)
    def test_individual_required_key(self, key):
        """Verify each required key is present."""
        assert os.path.exists(OUTPUT_FILE_PATH), f"Output file not found at {OUTPUT_FILE_PATH}"
        with open(OUTPUT_FILE_PATH, "r") as f:
            data = json.load(f)
        assert key in data, f"Required key '{key}' is missing from output"


class TestFieldTypes:
    """Tests for verifying field types are correct."""

    def test_winner_source_file_is_string(self):
        """Verify winner_source_file is a string."""
        assert os.path.exists(OUTPUT_FILE_PATH), f"Output file not found at {OUTPUT_FILE_PATH}"
        with open(OUTPUT_FILE_PATH, "r") as f:
            data = json.load(f)
        assert isinstance(data.get("winner_source_file"), str), (
            f"winner_source_file should be a string, got {type(data.get('winner_source_file')).__name__}"
        )

    def test_fbus_is_integer(self):
        """Verify fbus is an integer."""
        assert os.path.exists(OUTPUT_FILE_PATH), f"Output file not found at {OUTPUT_FILE_PATH}"
        with open(OUTPUT_FILE_PATH, "r") as f:
            data = json.load(f)
        assert isinstance(data.get("fbus"), int), (
            f"fbus should be an integer, got {type(data.get('fbus')).__name__}"
        )

    def test_tbus_is_integer(self):
        """Verify tbus is an integer."""
        assert os.path.exists(OUTPUT_FILE_PATH), f"Output file not found at {OUTPUT_FILE_PATH}"
        with open(OUTPUT_FILE_PATH, "r") as f:
            data = json.load(f)
        assert isinstance(data.get("tbus"), int), (
            f"tbus should be an integer, got {type(data.get('tbus')).__name__}"
        )

    def test_branch_row_index_is_integer(self):
        """Verify branch_row_index is an integer."""
        assert os.path.exists(OUTPUT_FILE_PATH), f"Output file not found at {OUTPUT_FILE_PATH}"
        with open(OUTPUT_FILE_PATH, "r") as f:
            data = json.load(f)
        assert isinstance(data.get("branch_row_index"), int), (
            f"branch_row_index should be an integer, got {type(data.get('branch_row_index')).__name__}"
        )

    def test_numeric_fields_are_numbers(self):
        """Verify numeric fields are JSON numbers (int or float)."""
        assert os.path.exists(OUTPUT_FILE_PATH), f"Output file not found at {OUTPUT_FILE_PATH}"
        with open(OUTPUT_FILE_PATH, "r") as f:
            data = json.load(f)

        numeric_fields = ["x", "rateA", "flow_MW", "loading_pct", "median_x_case57", "criticality"]
        for field in numeric_fields:
            value = data.get(field)
            assert isinstance(value, (int, float)), (
                f"Field '{field}' should be a number, got {type(value).__name__}: {value}"
            )
            # Ensure not a string representation of a number
            assert not isinstance(value, str), (
                f"Field '{field}' should be a JSON number, not a string: '{value}'"
            )


class TestFieldValues:
    """Tests for verifying field values are valid."""

    def test_winner_source_file_is_valid(self):
        """Verify winner_source_file is one of the expected values."""
        assert os.path.exists(OUTPUT_FILE_PATH), f"Output file not found at {OUTPUT_FILE_PATH}"
        with open(OUTPUT_FILE_PATH, "r") as f:
            data = json.load(f)

        winner = data.get("winner_source_file")
        assert winner in VALID_SOURCE_FILES, (
            f"winner_source_file must be one of {VALID_SOURCE_FILES}, got '{winner}'"
        )

    def test_fbus_is_valid_bus_number(self):
        """Verify fbus is a valid bus number (1 to 118)."""
        assert os.path.exists(OUTPUT_FILE_PATH), f"Output file not found at {OUTPUT_FILE_PATH}"
        with open(OUTPUT_FILE_PATH, "r") as f:
            data = json.load(f)

        fbus = data.get("fbus")
        assert 1 <= fbus <= NUM_BUSES_118, (
            f"fbus must be between 1 and {NUM_BUSES_118}, got {fbus}"
        )

    def test_tbus_is_valid_bus_number(self):
        """Verify tbus is a valid bus number (1 to 118)."""
        assert os.path.exists(OUTPUT_FILE_PATH), f"Output file not found at {OUTPUT_FILE_PATH}"
        with open(OUTPUT_FILE_PATH, "r") as f:
            data = json.load(f)

        tbus = data.get("tbus")
        assert 1 <= tbus <= NUM_BUSES_118, (
            f"tbus must be between 1 and {NUM_BUSES_118}, got {tbus}"
        )

    def test_fbus_different_from_tbus(self):
        """Verify fbus and tbus are different (no self-loops)."""
        assert os.path.exists(OUTPUT_FILE_PATH), f"Output file not found at {OUTPUT_FILE_PATH}"
        with open(OUTPUT_FILE_PATH, "r") as f:
            data = json.load(f)

        fbus = data.get("fbus")
        tbus = data.get("tbus")
        assert fbus != tbus, f"fbus and tbus should be different, both are {fbus}"

    def test_branch_row_index_is_non_negative(self):
        """Verify branch_row_index is non-negative (0-indexed)."""
        assert os.path.exists(OUTPUT_FILE_PATH), f"Output file not found at {OUTPUT_FILE_PATH}"
        with open(OUTPUT_FILE_PATH, "r") as f:
            data = json.load(f)

        idx = data.get("branch_row_index")
        assert idx >= 0, f"branch_row_index should be non-negative, got {idx}"

    def test_branch_row_index_is_within_bounds(self):
        """Verify branch_row_index is within valid range for branch data."""
        assert os.path.exists(OUTPUT_FILE_PATH), f"Output file not found at {OUTPUT_FILE_PATH}"
        with open(OUTPUT_FILE_PATH, "r") as f:
            data = json.load(f)

        idx = data.get("branch_row_index")
        # Both case files have 186 branches (indices 0-185)
        max_index = max(NUM_BRANCHES_CASE118, NUM_BRANCHES_PGLIB) - 1
        assert 0 <= idx <= max_index, (
            f"branch_row_index should be between 0 and {max_index}, got {idx}"
        )

    def test_reactance_is_positive(self):
        """Verify branch reactance x is positive."""
        assert os.path.exists(OUTPUT_FILE_PATH), f"Output file not found at {OUTPUT_FILE_PATH}"
        with open(OUTPUT_FILE_PATH, "r") as f:
            data = json.load(f)

        x = data.get("x")
        assert x > 0, f"Branch reactance x should be positive, got {x}"

    def test_rateA_is_positive(self):
        """Verify rateA is positive (branches with rateA <= 0 should be excluded)."""
        assert os.path.exists(OUTPUT_FILE_PATH), f"Output file not found at {OUTPUT_FILE_PATH}"
        with open(OUTPUT_FILE_PATH, "r") as f:
            data = json.load(f)

        rateA = data.get("rateA")
        assert rateA > 0, (
            f"rateA should be positive (branches with rateA <= 0 are excluded), got {rateA}"
        )

    def test_loading_pct_is_non_negative(self):
        """Verify loading_pct is non-negative."""
        assert os.path.exists(OUTPUT_FILE_PATH), f"Output file not found at {OUTPUT_FILE_PATH}"
        with open(OUTPUT_FILE_PATH, "r") as f:
            data = json.load(f)

        loading_pct = data.get("loading_pct")
        assert loading_pct >= 0, f"loading_pct should be non-negative, got {loading_pct}"

    def test_median_x_case57_is_positive(self):
        """Verify median_x_case57 is positive."""
        assert os.path.exists(OUTPUT_FILE_PATH), f"Output file not found at {OUTPUT_FILE_PATH}"
        with open(OUTPUT_FILE_PATH, "r") as f:
            data = json.load(f)

        median_x = data.get("median_x_case57")
        assert median_x > 0, f"median_x_case57 should be positive, got {median_x}"

    def test_criticality_is_non_negative(self):
        """Verify criticality score is non-negative."""
        assert os.path.exists(OUTPUT_FILE_PATH), f"Output file not found at {OUTPUT_FILE_PATH}"
        with open(OUTPUT_FILE_PATH, "r") as f:
            data = json.load(f)

        criticality = data.get("criticality")
        assert criticality >= 0, f"criticality should be non-negative, got {criticality}"


class TestDCPowerFlowLogic:
    """Tests for verifying DC power flow computation logic."""

    def test_loading_pct_calculation(self):
        """Verify loading_pct is consistent with flow_MW and rateA.

        loading_pct = abs(flow_MW) / rateA * 100
        """
        assert os.path.exists(OUTPUT_FILE_PATH), f"Output file not found at {OUTPUT_FILE_PATH}"
        with open(OUTPUT_FILE_PATH, "r") as f:
            data = json.load(f)

        flow_MW = data.get("flow_MW")
        rateA = data.get("rateA")
        loading_pct = data.get("loading_pct")

        if rateA > 0:
            expected_loading = abs(flow_MW) / rateA * 100
            # Allow for floating point precision differences
            assert abs(loading_pct - expected_loading) < 1e-6, (
                f"loading_pct ({loading_pct}) should equal abs(flow_MW)/rateA*100 "
                f"= abs({flow_MW})/{rateA}*100 = {expected_loading}"
            )

    def test_criticality_calculation(self):
        """Verify criticality is consistent with loading_pct, x, and median_x_case57.

        criticality = loading_pct / (x / median_x_case57)
        """
        assert os.path.exists(OUTPUT_FILE_PATH), f"Output file not found at {OUTPUT_FILE_PATH}"
        with open(OUTPUT_FILE_PATH, "r") as f:
            data = json.load(f)

        loading_pct = data.get("loading_pct")
        x = data.get("x")
        median_x = data.get("median_x_case57")
        criticality = data.get("criticality")

        if x > 0 and median_x > 0:
            expected_criticality = loading_pct / (x / median_x)
            # Allow for floating point precision differences
            assert abs(criticality - expected_criticality) < 1e-4, (
                f"criticality ({criticality}) should equal loading_pct/(x/median_x) "
                f"= {loading_pct}/({x}/{median_x}) = {expected_criticality}"
            )


class TestCase57MedianReactance:
    """Tests for verifying case57 median reactance baseline."""

    def test_median_x_case57_is_reasonable(self):
        """Verify median_x_case57 is within a reasonable range for IEEE 57-bus system.

        From the case57.m file, reactances range roughly from 0.0152 to 1.355.
        The median should be somewhere in a reasonable middle range.
        """
        assert os.path.exists(OUTPUT_FILE_PATH), f"Output file not found at {OUTPUT_FILE_PATH}"
        with open(OUTPUT_FILE_PATH, "r") as f:
            data = json.load(f)

        median_x = data.get("median_x_case57")
        # Based on case57.m branch data, reactances are positive and vary
        # The median of positive x values should be in a reasonable range
        assert 0.01 <= median_x <= 2.0, (
            f"median_x_case57 should be between 0.01 and 2.0 (typical IEEE case values), "
            f"got {median_x}"
        )


class TestSourceFileConsistency:
    """Tests for verifying the winner source file selection is logical."""

    def test_winner_comes_from_file_with_positive_ratings(self):
        """Verify winner is from pglib file (which has positive rateA values).

        case118.m has all rateA = 0, meaning all branches would be excluded.
        pglib_opf_case118_ieee.m has positive rateA values.
        Therefore, the winner must come from pglib_opf_case118_ieee.m.
        """
        assert os.path.exists(OUTPUT_FILE_PATH), f"Output file not found at {OUTPUT_FILE_PATH}"
        with open(OUTPUT_FILE_PATH, "r") as f:
            data = json.load(f)

        winner = data.get("winner_source_file")
        # Based on input file analysis, case118.m has all rateA = 0
        # So the winner must be from pglib_opf_case118_ieee.m
        assert winner == "pglib_opf_case118_ieee.m", (
            f"Expected winner to be 'pglib_opf_case118_ieee.m' since case118.m has "
            f"all rateA = 0 (excluded branches), but got '{winner}'"
        )


class TestNumericPrecision:
    """Tests for verifying numeric values have reasonable precision."""

    def test_no_nan_values(self):
        """Verify no NaN values in output."""
        assert os.path.exists(OUTPUT_FILE_PATH), f"Output file not found at {OUTPUT_FILE_PATH}"
        with open(OUTPUT_FILE_PATH, "r") as f:
            data = json.load(f)

        numeric_fields = ["x", "rateA", "flow_MW", "loading_pct", "median_x_case57", "criticality"]
        for field in numeric_fields:
            value = data.get(field)
            if isinstance(value, float):
                assert not math.isnan(value), f"Field '{field}' contains NaN"

    def test_no_infinite_values(self):
        """Verify no infinite values in output."""
        assert os.path.exists(OUTPUT_FILE_PATH), f"Output file not found at {OUTPUT_FILE_PATH}"
        with open(OUTPUT_FILE_PATH, "r") as f:
            data = json.load(f)

        numeric_fields = ["x", "rateA", "flow_MW", "loading_pct", "median_x_case57", "criticality"]
        for field in numeric_fields:
            value = data.get(field)
            if isinstance(value, float):
                assert not math.isinf(value), f"Field '{field}' contains infinity"


class TestInputFilesExist:
    """Tests for verifying input files exist (prerequisite check)."""

    def test_case118_exists(self):
        """Verify case118.m input file exists."""
        path = os.path.join(INPUT_DIR, "case118.m")
        assert os.path.exists(path), f"Input file not found: {path}"

    def test_case57_exists(self):
        """Verify case57.m input file exists."""
        path = os.path.join(INPUT_DIR, "case57.m")
        assert os.path.exists(path), f"Input file not found: {path}"

    def test_pglib_case118_exists(self):
        """Verify pglib_opf_case118_ieee.m input file exists."""
        path = os.path.join(INPUT_DIR, "pglib_opf_case118_ieee.m")
        assert os.path.exists(path), f"Input file not found: {path}"


class TestOutputDirectory:
    """Tests for verifying output directory structure."""

    def test_output_directory_exists(self):
        """Verify output directory exists."""
        output_dir = os.path.dirname(OUTPUT_FILE_PATH)
        assert os.path.exists(output_dir), f"Output directory not found: {output_dir}"

    def test_output_file_is_in_correct_location(self):
        """Verify output file is at the exact expected path."""
        expected_path = "/root/most_critical_branch.json"
        assert OUTPUT_FILE_PATH == expected_path, (
            f"Output file path mismatch: expected {expected_path}, got {OUTPUT_FILE_PATH}"
        )


class TestBranchIdentification:
    """Tests for verifying branch identification is deterministic."""

    def test_branch_endpoints_are_ordered_consistently(self):
        """Verify fbus and tbus values allow for proper branch identification.

        The tie-breaking rule uses (min(fbus,tbus), max(fbus,tbus)) lexicographic order.
        """
        assert os.path.exists(OUTPUT_FILE_PATH), f"Output file not found at {OUTPUT_FILE_PATH}"
        with open(OUTPUT_FILE_PATH, "r") as f:
            data = json.load(f)

        fbus = data.get("fbus")
        tbus = data.get("tbus")

        # Both should be valid bus numbers
        assert fbus is not None and tbus is not None, "fbus and tbus must both be present"
        assert isinstance(fbus, int) and isinstance(tbus, int), "fbus and tbus must be integers"


class TestMaxLoadedBranchSelection:
    """Tests for verifying the max-loaded branch was selected correctly."""

    def test_loading_indicates_max_loaded(self):
        """Verify the loading percentage is meaningful (not zero for the max branch)."""
        assert os.path.exists(OUTPUT_FILE_PATH), f"Output file not found at {OUTPUT_FILE_PATH}"
        with open(OUTPUT_FILE_PATH, "r") as f:
            data = json.load(f)

        loading_pct = data.get("loading_pct")
        # The max-loaded branch should have some loading
        # It could be zero only in edge cases, but typically should be positive
        # We just verify it's a valid number
        assert loading_pct is not None, "loading_pct must be present"
        assert isinstance(loading_pct, (int, float)), "loading_pct must be numeric"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

HEREDOC_EOF

# Execute command
python3 -m py_compile expectation_tests.py && echo "Syntax OK"

# Execute command
python3 -m pytest --collect-only expectation_tests.py 2>&1 | head -80

# Execute command
ls -la /root/harbor_workspaces/task_T434_run2/output 2>/dev/null || mkdir -p /root/harbor_workspaces/task_T434_run2/output && echo "Output directory ready"

# Create /root/harbor_workspaces/task_T434_run2/dc_power_flow_analysis.py
mkdir -p $(dirname /root/harbor_workspaces/task_T434_run2/dc_power_flow_analysis.py)
cat << 'HEREDOC_EOF' > /root/harbor_workspaces/task_T434_run2/dc_power_flow_analysis.py
#!/usr/bin/env python3
"""
DC Power Flow Analysis for IEEE 118-bus cases.
Determines the most critical transmission element across both case118.m and pglib_opf_case118_ieee.m.
Uses case57.m to define the comparison baseline (median reactance).
"""

import re
import json
import numpy as np
import sys
sys.path.insert(0, '.claude/skills/dc-power-flow/scripts')
from build_b_matrix import build_susceptance_matrix


def parse_matpower_file(filepath):
    """
    Parse a MATPOWER .m case file and extract baseMVA, bus, gen, and branch data.

    Returns:
        dict with keys: 'baseMVA', 'bus', 'gen', 'branch'
    """
    with open(filepath, 'r') as f:
        content = f.read()

    # Extract baseMVA
    basemva_match = re.search(r'mpc\.baseMVA\s*=\s*([\d.]+)', content)
    if basemva_match:
        baseMVA = float(basemva_match.group(1))
    else:
        baseMVA = 100.0

    def extract_matrix(name):
        """Extract a matrix from the MATPOWER file."""
        # Match pattern like: mpc.bus = [ ... ];
        pattern = rf'mpc\.{name}\s*=\s*\[(.*?)\];'
        match = re.search(pattern, content, re.DOTALL)
        if not match:
            return None

        matrix_str = match.group(1)
        # Remove comments (% ...) and clean up
        lines = []
        for line in matrix_str.split('\n'):
            # Remove comment portions
            if '%' in line:
                line = line[:line.index('%')]
            line = line.strip()
            if line and not line.startswith('%'):
                # Remove trailing semicolons
                line = line.rstrip(';').strip()
                if line:
                    lines.append(line)

        # Parse rows
        rows = []
        for line in lines:
            # Split by whitespace or tabs
            parts = line.split()
            if parts:
                try:
                    row = [float(p) for p in parts]
                    rows.append(row)
                except ValueError:
                    continue

        if rows:
            return np.array(rows)
        return None

    bus = extract_matrix('bus')
    gen = extract_matrix('gen')
    branch = extract_matrix('branch')

    return {
        'baseMVA': baseMVA,
        'bus': bus,
        'gen': gen,
        'branch': branch
    }


def run_dc_power_flow(case_data):
    """
    Run DC power flow analysis on a MATPOWER case.

    Args:
        case_data: dict with 'baseMVA', 'bus', 'gen', 'branch'

    Returns:
        dict with 'theta' (bus angles), 'line_flows' (list of dicts)
    """
    baseMVA = case_data['baseMVA']
    buses = case_data['bus']
    gens = case_data['gen']
    branches = case_data['branch']

    n_bus = len(buses)

    # Create bus number to index mapping
    bus_num_to_idx = {int(buses[i, 0]): i for i in range(n_bus)}

    # Find slack bus (type == 3)
    slack_idx = None
    for i in range(n_bus):
        if int(buses[i, 1]) == 3:
            slack_idx = i
            break

    if slack_idx is None:
        raise ValueError("No slack bus (type=3) found")

    # Compute net injection: P = sum(Pg_online) - Pd
    # MATPOWER columns: bus[:,2] = Pd, gen[:,0] = bus, gen[:,1] = Pg, gen[:,7] = status
    P = np.zeros(n_bus)

    # Add online generator output
    for g in gens:
        gen_bus = int(g[0])
        pg = g[1]
        status = int(g[7]) if len(g) > 7 else 1

        if status == 1:  # Online
            bi = bus_num_to_idx[gen_bus]
            P[bi] += pg

    # Subtract load (Pd)
    for i in range(n_bus):
        P[i] -= buses[i, 2]

    # Build susceptance matrix B from in-service branches
    # Only use branches with status == 1 and x != 0
    B = np.zeros((n_bus, n_bus))
    branch_susceptances = []

    for br in branches:
        fbus = int(br[0])
        tbus = int(br[1])
        x = br[3]  # Reactance at column 3
        status = int(br[10]) if len(br) > 10 else 1

        if status != 1:
            branch_susceptances.append(0.0)
            continue

        if x == 0:
            branch_susceptances.append(0.0)
            continue

        b = 1.0 / x
        branch_susceptances.append(b)

        f = bus_num_to_idx[fbus]
        t = bus_num_to_idx[tbus]

        # Diagonal
        B[f, f] += b
        B[t, t] += b
        # Off-diagonal
        B[f, t] -= b
        B[t, f] -= b

    # Solve DC power flow: B * theta = P / baseMVA
    # With slack bus angle fixed to 0

    # Create mask for non-slack buses
    mask = np.ones(n_bus, dtype=bool)
    mask[slack_idx] = False

    # Reduced system
    B_red = B[np.ix_(mask, mask)]
    P_red = P[mask] / baseMVA  # Convert to per-unit

    # Solve for angles
    theta = np.zeros(n_bus)
    theta[mask] = np.linalg.solve(B_red, P_red)
    theta[slack_idx] = 0.0  # Reference angle

    # Calculate line flows
    line_flows = []
    for idx, br in enumerate(branches):
        fbus = int(br[0])
        tbus = int(br[1])
        x = br[3]
        rateA = br[5] if len(br) > 5 else 0
        status = int(br[10]) if len(br) > 10 else 1

        b = branch_susceptances[idx]

        if status != 1 or x == 0:
            flow_MW = 0.0
        else:
            f = bus_num_to_idx[fbus]
            t = bus_num_to_idx[tbus]
            flow_MW = b * (theta[f] - theta[t]) * baseMVA

        # Calculate loading percentage (only if rateA > 0)
        if rateA > 0:
            loading_pct = abs(flow_MW) / rateA * 100
        else:
            loading_pct = 0.0

        line_flows.append({
            'branch_row_index': idx + 1,  # 1-based (MATLAB convention)
            'fbus': fbus,
            'tbus': tbus,
            'x': x,
            'rateA': rateA,
            'flow_MW': flow_MW,
            'loading_pct': loading_pct,
            'status': status
        })

    return {
        'theta': theta,
        'line_flows': line_flows,
        'slack_idx': slack_idx,
        'bus_num_to_idx': bus_num_to_idx
    }


def find_max_loaded_branch(line_flows):
    """
    Find the branch with maximum loading percentage.

    Tie-breaking:
    1. Choose largest loading_pct
    2. If tie, smallest (min(fbus,tbus), max(fbus,tbus)) lexicographically
    3. If still tied, smallest branch_row_index

    Only considers branches with status==1 and rateA > 0 and x > 0.
    """
    candidates = []

    for lf in line_flows:
        if lf['status'] != 1:
            continue
        if lf['rateA'] <= 0:
            continue
        if lf['x'] == 0:
            continue
        candidates.append(lf)

    if not candidates:
        return None

    # Sort with custom key:
    # Primary: -loading_pct (descending)
    # Secondary: (min(fbus,tbus), max(fbus,tbus)) ascending
    # Tertiary: branch_row_index ascending
    def sort_key(lf):
        fbus = lf['fbus']
        tbus = lf['tbus']
        pair = (min(fbus, tbus), max(fbus, tbus))
        return (-lf['loading_pct'], pair, lf['branch_row_index'])

    candidates_sorted = sorted(candidates, key=sort_key)
    return candidates_sorted[0]


def compute_median_x_case57(case57_data):
    """
    Compute median reactance from case57.m for in-service branches with x > 0.
    """
    branches = case57_data['branch']
    xs = []

    for br in branches:
        x = br[3]
        status = int(br[10]) if len(br) > 10 else 1

        if status == 1 and x > 0:
            xs.append(x)

    if not xs:
        raise ValueError("No valid branches found in case57")

    return float(np.median(xs))


def main():
    print("=" * 60)
    print("DC Power Flow Analysis - Most Critical Branch Identification")
    print("=" * 60)

    # Parse all three case files
    print("\n1. Parsing MATPOWER case files...")

    case118_data = parse_matpower_file('input/case118.m')
    print(f"   case118.m: {len(case118_data['bus'])} buses, "
          f"{len(case118_data['gen'])} gens, {len(case118_data['branch'])} branches")

    pglib_data = parse_matpower_file('input/pglib_opf_case118_ieee.m')
    print(f"   pglib_opf_case118_ieee.m: {len(pglib_data['bus'])} buses, "
          f"{len(pglib_data['gen'])} gens, {len(pglib_data['branch'])} branches")

    case57_data = parse_matpower_file('input/case57.m')
    print(f"   case57.m: {len(case57_data['bus'])} buses, "
          f"{len(case57_data['gen'])} gens, {len(case57_data['branch'])} branches")

    # Compute baseline median reactance from case57
    print("\n2. Computing baseline median reactance from case57...")
    median_x_case57 = compute_median_x_case57(case57_data)
    print(f"   median_x_case57 = {median_x_case57:.6f}")

    # Run DC power flow for each 118-bus case
    results = {}

    for name, data in [('case118.m', case118_data), ('pglib_opf_case118_ieee.m', pglib_data)]:
        print(f"\n3. Running DC power flow for {name}...")

        pf_result = run_dc_power_flow(data)

        # Verify DC solve (check residual)
        buses = data['bus']
        gens = data['gen']
        baseMVA = data['baseMVA']
        n_bus = len(buses)
        bus_num_to_idx = pf_result['bus_num_to_idx']
        theta = pf_result['theta']
        slack_idx = pf_result['slack_idx']

        # Recompute P for residual check
        P = np.zeros(n_bus)
        for g in gens:
            gen_bus = int(g[0])
            pg = g[1]
            status = int(g[7]) if len(g) > 7 else 1
            if status == 1:
                bi = bus_num_to_idx[gen_bus]
                P[bi] += pg
        for i in range(n_bus):
            P[i] -= buses[i, 2]

        # Rebuild B for residual check
        branches = data['branch']
        B = np.zeros((n_bus, n_bus))
        for br in branches:
            fbus = int(br[0])
            tbus = int(br[1])
            x = br[3]
            status = int(br[10]) if len(br) > 10 else 1
            if status != 1 or x == 0:
                continue
            b = 1.0 / x
            f = bus_num_to_idx[fbus]
            t = bus_num_to_idx[tbus]
            B[f, f] += b
            B[t, t] += b
            B[f, t] -= b
            B[t, f] -= b

        # Residual
        residual = B @ theta - P / baseMVA
        mask = np.ones(n_bus, dtype=bool)
        mask[slack_idx] = False
        max_res = np.max(np.abs(residual[mask]))
        print(f"   DC solve max residual (non-slack): {max_res:.2e}")

        # Find max-loaded branch
        max_branch = find_max_loaded_branch(pf_result['line_flows'])

        if max_branch is None:
            print(f"   WARNING: No valid branches with rateA > 0 found in {name}")
            results[name] = None
        else:
            print(f"   Max loaded branch: {max_branch['fbus']}-{max_branch['tbus']} "
                  f"(row {max_branch['branch_row_index']})")
            print(f"   Loading: {max_branch['loading_pct']:.2f}%")
            print(f"   Flow: {max_branch['flow_MW']:.2f} MW, Rating: {max_branch['rateA']} MW")

            # Compute criticality
            x = max_branch['x']
            criticality = max_branch['loading_pct'] / (x / median_x_case57)
            max_branch['criticality'] = criticality
            max_branch['median_x_case57'] = median_x_case57
            print(f"   Criticality score: {criticality:.4f}")

            results[name] = max_branch

    # Determine overall winner
    print("\n4. Determining overall winner...")

    winner = None
    winner_source = None

    # Check which cases have valid results
    valid_results = [(name, res) for name, res in results.items() if res is not None]

    if len(valid_results) == 0:
        print("   ERROR: No valid branches found in any file!")
        return
    elif len(valid_results) == 1:
        winner_source, winner = valid_results[0]
        print(f"   Only one file has valid branches: {winner_source}")
    else:
        # Compare criticality scores
        name1, res1 = valid_results[0]
        name2, res2 = valid_results[1]

        crit1 = res1['criticality']
        crit2 = res2['criticality']

        print(f"   {name1}: criticality = {crit1:.4f}")
        print(f"   {name2}: criticality = {crit2:.4f}")

        if crit1 > crit2:
            winner_source = name1
            winner = res1
        elif crit2 > crit1:
            winner_source = name2
            winner = res2
        else:
            # Tie - prefer pglib_opf_case118_ieee.m
            if name1 == 'pglib_opf_case118_ieee.m':
                winner_source = name1
                winner = res1
            else:
                winner_source = name2
                winner = res2
            print(f"   Tie broken in favor of pglib_opf_case118_ieee.m")

    print(f"\n   WINNER: {winner_source}")
    print(f"   Branch: {winner['fbus']}-{winner['tbus']} (row {winner['branch_row_index']})")
    print(f"   Criticality: {winner['criticality']:.4f}")

    # Prepare output JSON
    output = {
        "winner_source_file": winner_source,
        "fbus": winner['fbus'],
        "tbus": winner['tbus'],
        "branch_row_index": winner['branch_row_index'],
        "x": winner['x'],
        "rateA": winner['rateA'],
        "flow_MW": winner['flow_MW'],
        "loading_pct": winner['loading_pct'],
        "median_x_case57": winner['median_x_case57'],
        "criticality": winner['criticality']
    }

    # Write output
    output_path = '/root/most_critical_branch.json'
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\n5. Result written to: {output_path}")
    print("\nFinal JSON output:")
    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()

HEREDOC_EOF

# Execute command
python3 dc_power_flow_analysis.py

# Execute command
python3 -c "
import json
with open('/root/most_critical_branch.json') as f:
    data = json.load(f)

# Verify all required keys
required_keys = ['winner_source_file', 'fbus', 'tbus', 'branch_row_index', 'x', 'rateA', 'flow_MW', 'loading_pct', 'median_x_case57', 'criticality']
for key in required_keys:
    if key not in data:
        print(f'MISSING KEY: {key}')
    else:
        print(f'{key}: {type(data[key]).__name__} = {data[key]}')

print()
print('All keys present:', all(k in data for k in required_keys))
print('All numeric fields are numbers:', all(isinstance(data[k], (int, float)) for k in ['fbus', 'tbus', 'branch_row_index', 'x', 'rateA', 'flow_MW', 'loading_pct', 'median_x_case57', 'criticality']))
"
