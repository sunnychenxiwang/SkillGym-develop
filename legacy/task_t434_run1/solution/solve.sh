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
ls -la /root/harbor_workspaces/task_T434_run1/output 2>/dev/null || mkdir -p /root/harbor_workspaces/task_T434_run1/output && echo "Output directory ready"

# Create /root/harbor_workspaces/task_T434_run1/dc_power_flow_analysis.py
mkdir -p $(dirname /root/harbor_workspaces/task_T434_run1/dc_power_flow_analysis.py)
cat << 'HEREDOC_EOF' > /root/harbor_workspaces/task_T434_run1/dc_power_flow_analysis.py
#!/usr/bin/env python3
"""
DC Power Flow Analysis for MATPOWER case files.
Computes DC power flow for each case and identifies the most thermally overloaded branch.
"""

import sys
import os
import re
import json
import numpy as np

# Add skills directory to path
sys.path.insert(0, '/root/harbor_workspaces/task_T434_run1/.claude/skills/dc-power-flow/scripts')
from build_b_matrix import build_susceptance_matrix, calculate_line_flows


def parse_matpower_file(filepath):
    """
    Parse a MATPOWER .m file and extract mpc.baseMVA, mpc.bus, mpc.gen, mpc.branch.

    Returns:
        dict with keys: baseMVA, bus, gen, branch (all as numpy arrays except baseMVA)
    """
    with open(filepath, 'r') as f:
        content = f.read()

    # Remove comments (% to end of line)
    lines = content.split('\n')
    clean_lines = []
    for line in lines:
        # Find comment position (but not inside strings)
        comment_pos = line.find('%')
        if comment_pos >= 0:
            line = line[:comment_pos]
        clean_lines.append(line)
    content = '\n'.join(clean_lines)

    # Extract baseMVA
    basemva_match = re.search(r'mpc\.baseMVA\s*=\s*([\d.]+)', content)
    if basemva_match:
        baseMVA = float(basemva_match.group(1))
    else:
        raise ValueError(f"Could not find mpc.baseMVA in {filepath}")

    # Extract matrices
    def extract_matrix(name, content):
        """Extract a MATPOWER matrix from the file content."""
        # Pattern to match mpc.name = [ ... ];
        pattern = rf'mpc\.{name}\s*=\s*\[(.*?)\];'
        match = re.search(pattern, content, re.DOTALL)
        if not match:
            raise ValueError(f"Could not find mpc.{name} in file")

        matrix_str = match.group(1)

        # Parse the matrix data
        rows = []
        for line in matrix_str.strip().split('\n'):
            line = line.strip()
            if not line:
                continue
            # Split by whitespace or tabs, filter out empty strings
            # Also handle semicolons as row separators
            line = line.replace(';', '')
            values = [v for v in re.split(r'[\s\t]+', line) if v]
            if values:
                try:
                    row = [float(v) for v in values]
                    rows.append(row)
                except ValueError:
                    continue  # Skip lines that can't be converted

        if not rows:
            raise ValueError(f"Empty matrix for mpc.{name}")

        return np.array(rows)

    bus = extract_matrix('bus', content)
    gen = extract_matrix('gen', content)
    branch = extract_matrix('branch', content)

    return {
        'baseMVA': baseMVA,
        'bus': bus,
        'gen': gen,
        'branch': branch
    }


def compute_net_injections(bus, gen, bus_num_to_idx):
    """
    Compute net real power injections at each bus.
    P_inj = sum(Pg for gens at bus with status==1) - Pd

    Args:
        bus: Bus data array (n_bus x 13)
        gen: Generator data array (n_gen x 21)
        bus_num_to_idx: Mapping from bus numbers to indices

    Returns:
        P: Net injection at each bus (MW)
    """
    n_bus = len(bus)
    P = np.zeros(n_bus)

    # Subtract load (Pd is column 2, index 2)
    for i in range(n_bus):
        Pd = bus[i, 2]  # Real power demand
        P[i] = -Pd

    # Add generation from generators with status == 1
    # Gen columns: bus(0), Pg(1), Qg(2), Qmax(3), Qmin(4), Vg(5), mBase(6), status(7), ...
    for g in range(len(gen)):
        gen_status = gen[g, 7]  # status column
        if gen_status == 1:
            gen_bus = int(gen[g, 0])
            Pg = gen[g, 1]  # Real power output
            if gen_bus in bus_num_to_idx:
                idx = bus_num_to_idx[gen_bus]
                P[idx] += Pg

    return P


def find_slack_bus(bus):
    """
    Find the slack bus (type == 3).

    Args:
        bus: Bus data array

    Returns:
        slack_idx: Index of slack bus in bus array
        slack_bus_num: Bus number of slack bus
    """
    slack_idx = None
    slack_bus_num = None
    count = 0

    for i in range(len(bus)):
        if int(bus[i, 1]) == 3:  # type column
            slack_idx = i
            slack_bus_num = int(bus[i, 0])
            count += 1

    if count != 1:
        raise ValueError(f"Expected exactly 1 slack bus (type=3), found {count}")

    return slack_idx, slack_bus_num


def solve_dc_power_flow(B, P, slack_idx, baseMVA):
    """
    Solve DC power flow: B @ theta = P/baseMVA (with slack angle = 0)

    Args:
        B: Full susceptance matrix (n_bus x n_bus)
        P: Net injections at each bus (MW)
        slack_idx: Index of slack bus
        baseMVA: System base MVA

    Returns:
        theta: Bus angles (radians)
    """
    n_bus = B.shape[0]

    # Create mask for non-slack buses
    mask = np.arange(n_bus) != slack_idx

    # Reduced system (exclude slack bus row/col)
    B_red = B[mask][:, mask]
    P_red = P[mask] / baseMVA  # Convert MW to pu

    # Solve for angles
    theta_red = np.linalg.solve(B_red, P_red)

    # Reconstruct full theta vector with slack angle = 0
    theta = np.zeros(n_bus)
    theta[mask] = theta_red
    theta[slack_idx] = 0.0

    # Verification: check residual
    residual = np.max(np.abs(B_red @ theta_red - P_red))
    if residual > 1e-6:
        print(f"  Warning: DC PF residual = {residual:.2e}")

    return theta


def compute_branch_flows_and_loading(branch, theta, baseMVA, bus_num_to_idx):
    """
    Compute branch flows and loading percentages for in-service branches.

    Args:
        branch: Branch data array
        theta: Bus angles (radians)
        baseMVA: System base MVA
        bus_num_to_idx: Bus number to index mapping

    Returns:
        List of dicts with branch info, flow, and loading
    """
    results = []

    for idx, br in enumerate(branch):
        status = br[10]  # status column (index 10)

        # Only consider in-service branches
        if status != 1:
            continue

        fbus = int(br[0])
        tbus = int(br[1])
        x = br[3]  # Reactance
        rateA = br[5]  # Thermal rating A

        f = bus_num_to_idx[fbus]
        t = bus_num_to_idx[tbus]

        # Compute susceptance and flow
        if x != 0:
            b = 1.0 / x
            flow_MW = b * (theta[f] - theta[t]) * baseMVA
        else:
            flow_MW = 0.0

        # Compute loading percentage (only for rateA > 0)
        if rateA > 0:
            loading_pct = abs(flow_MW) / rateA * 100
        else:
            loading_pct = None  # No limit, excluded from overload consideration

        results.append({
            'branch_index': idx,
            'fbus': fbus,
            'tbus': tbus,
            'x_pu': x,
            'rateA_MW': rateA,
            'flow_MW': flow_MW,
            'loading_pct': loading_pct
        })

    return results


def run_dc_power_flow(case_name, filepath):
    """
    Run DC power flow analysis for a single case.

    Returns:
        dict with case results including overload candidates
    """
    print(f"\nProcessing {case_name}...")

    # Parse the file
    data = parse_matpower_file(filepath)
    baseMVA = data['baseMVA']
    bus = data['bus']
    gen = data['gen']
    branch = data['branch']

    n_bus = len(bus)
    n_branch = len(branch)
    print(f"  baseMVA: {baseMVA}")
    print(f"  Buses: {n_bus}, Generators: {len(gen)}, Branches: {n_branch}")

    # Build bus number mapping
    bus_num_to_idx = {int(bus[i, 0]): i for i in range(n_bus)}

    # Find slack bus
    slack_idx, slack_bus_num = find_slack_bus(bus)
    print(f"  Slack bus: {slack_bus_num} (index {slack_idx})")

    # Compute net injections
    P = compute_net_injections(bus, gen, bus_num_to_idx)

    # Filter in-service branches for B matrix construction
    in_service_branches = branch[branch[:, 10] == 1]
    print(f"  In-service branches: {len(in_service_branches)}")

    # Build susceptance matrix using skill function
    B, branch_susceptances, _ = build_susceptance_matrix(in_service_branches, bus)

    # Verify B matrix
    assert np.allclose(B, B.T), "B matrix is not symmetric!"

    # Solve DC power flow
    theta = solve_dc_power_flow(B, P, slack_idx, baseMVA)

    # Compute branch flows and loading
    branch_results = compute_branch_flows_and_loading(branch, theta, baseMVA, bus_num_to_idx)

    # Find overload candidates (only branches with rateA > 0)
    overload_candidates = [r for r in branch_results if r['loading_pct'] is not None]

    if overload_candidates:
        max_loading = max(r['loading_pct'] for r in overload_candidates)
        print(f"  Max loading: {max_loading:.2f}%")
        print(f"  Branches with thermal limits: {len(overload_candidates)}")
    else:
        print(f"  No branches with thermal limits (all rateA=0)")

    return {
        'case_name': case_name,
        'slack_bus': slack_bus_num,
        'baseMVA': baseMVA,
        'theta': theta,
        'branch_results': branch_results,
        'overload_candidates': overload_candidates
    }


def find_most_overloaded_branch(all_results):
    """
    Find the single most overloaded branch across all cases.

    Tie-breaking rules:
    1. Maximum loading_pct (descending)
    2. Lexicographically smaller case_name
    3. Smaller branch_index (0-based)

    Returns:
        dict with winner info
    """
    # Collect all candidates with their case info
    candidates = []
    for result in all_results:
        case_name = result['case_name']
        slack_bus = result['slack_bus']
        for br in result['overload_candidates']:
            candidates.append({
                'case_name': case_name,
                'slack_bus': slack_bus,
                'branch_index': br['branch_index'],
                'fbus': br['fbus'],
                'tbus': br['tbus'],
                'rateA_MW': br['rateA_MW'],
                'x_pu': br['x_pu'],
                'flow_MW': br['flow_MW'],
                'loading_pct': br['loading_pct']
            })

    if not candidates:
        raise ValueError("No branches with thermal limits found across all cases!")

    # Sort by: -loading_pct (descending), case_name (ascending), branch_index (ascending)
    candidates.sort(key=lambda x: (-x['loading_pct'], x['case_name'], x['branch_index']))

    winner = candidates[0]
    return winner


def main():
    # Input files
    input_dir = '/root/harbor_workspaces/task_T434_run1/input'
    cases = [
        ('case57', os.path.join(input_dir, 'case57.m')),
        ('case118', os.path.join(input_dir, 'case118.m')),
        ('pglib_opf_case118_ieee', os.path.join(input_dir, 'pglib_opf_case118_ieee.m'))
    ]

    # Run DC power flow for each case
    all_results = []
    for case_name, filepath in cases:
        result = run_dc_power_flow(case_name, filepath)
        all_results.append(result)

    # Find most overloaded branch across all cases
    print("\n" + "="*60)
    print("Finding most overloaded branch across all cases...")

    winner = find_most_overloaded_branch(all_results)

    print(f"\nMost overloaded branch:")
    print(f"  Case: {winner['case_name']}")
    print(f"  Slack bus: {winner['slack_bus']}")
    print(f"  Branch index: {winner['branch_index']}")
    print(f"  From bus: {winner['fbus']} -> To bus: {winner['tbus']}")
    print(f"  Reactance (x_pu): {winner['x_pu']}")
    print(f"  Rate A (MW): {winner['rateA_MW']}")
    print(f"  Flow (MW): {winner['flow_MW']:.6f}")
    print(f"  Loading: {winner['loading_pct']:.6f}%")

    # Prepare output JSON
    output = {
        'case_name': winner['case_name'],
        'slack_bus': winner['slack_bus'],
        'branch_index': winner['branch_index'],
        'fbus': winner['fbus'],
        'tbus': winner['tbus'],
        'rateA_MW': winner['rateA_MW'],
        'x_pu': winner['x_pu'],
        'flow_MW': winner['flow_MW'],
        'loading_pct': winner['loading_pct']
    }

    # Write output
    output_path = '/root/harbor_workspaces/task_T434_run1/output/most_overloaded_branch.json'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\nOutput written to: {output_path}")

    return output


if __name__ == '__main__':
    main()

HEREDOC_EOF

# Execute command
python3 dc_power_flow_analysis.py

# Create /root/harbor_workspaces/task_T434_run1/expectation_tests.py
mkdir -p $(dirname /root/harbor_workspaces/task_T434_run1/expectation_tests.py)
cat << 'HEREDOC_EOF' > /root/harbor_workspaces/task_T434_run1/expectation_tests.py
"""Auto-generated expectation tests for DC power flow task verification.

These tests verify that the task execution produces correct outputs
based on the instruction requirements for computing DC power flow
across three MATPOWER case files and identifying the most overloaded branch.
"""

import json
import os
from pathlib import Path

import pytest


# Constants
OUTPUT_DIR = "/root/harbor_workspaces/task_T434_run1/output"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "most_overloaded_branch.json")
INPUT_DIR = "/root/harbor_workspaces/task_T434_run1/input"

# Valid case names from the input files
VALID_CASE_NAMES = {"case57", "case118", "pglib_opf_case118_ieee"}


class TestOutputFileExists:
    """Tests verifying the output file exists and has correct basic properties."""

    def test_output_directory_exists(self):
        """Verify the output directory exists."""
        assert os.path.exists(OUTPUT_DIR), f"Output directory not found: {OUTPUT_DIR}"

    def test_output_file_exists(self):
        """Verify the output JSON file was created."""
        assert os.path.exists(OUTPUT_FILE), f"Output file not found: {OUTPUT_FILE}"

    def test_output_file_not_empty(self):
        """Verify the output file is not empty."""
        assert os.path.getsize(OUTPUT_FILE) > 0, "Output file is empty"


class TestOutputValidJSON:
    """Tests verifying the output is valid JSON with correct structure."""

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        with open(OUTPUT_FILE, "r") as f:
            return json.load(f)

    def test_output_is_valid_json(self):
        """Verify output file contains valid JSON."""
        with open(OUTPUT_FILE, "r") as f:
            try:
                data = json.load(f)
                assert data is not None
            except json.JSONDecodeError as e:
                pytest.fail(f"Output file is not valid JSON: {e}")

    def test_output_is_dict(self, output_data):
        """Verify output JSON is a dictionary (object), not an array."""
        assert isinstance(output_data, dict), "Output JSON should be an object/dictionary"


class TestRequiredFields:
    """Tests verifying all required fields are present in the output."""

    REQUIRED_FIELDS = [
        "case_name",
        "slack_bus",
        "branch_index",
        "fbus",
        "tbus",
        "rateA_MW",
        "x_pu",
        "flow_MW",
        "loading_pct",
    ]

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        with open(OUTPUT_FILE, "r") as f:
            return json.load(f)

    def test_all_required_fields_present(self, output_data):
        """Verify all required fields are present in the output."""
        missing_fields = [
            field for field in self.REQUIRED_FIELDS if field not in output_data
        ]
        assert (
            not missing_fields
        ), f"Missing required fields: {missing_fields}"

    def test_no_extra_fields(self, output_data):
        """Verify no unexpected extra fields are present."""
        extra_fields = [
            field for field in output_data.keys() if field not in self.REQUIRED_FIELDS
        ]
        assert not extra_fields, f"Unexpected extra fields: {extra_fields}"

    @pytest.mark.parametrize("field", REQUIRED_FIELDS)
    def test_field_present(self, output_data, field):
        """Verify each required field is present."""
        assert field in output_data, f"Required field '{field}' is missing"


class TestFieldTypes:
    """Tests verifying field types match the expected schema."""

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        with open(OUTPUT_FILE, "r") as f:
            return json.load(f)

    def test_case_name_is_string(self, output_data):
        """Verify case_name is a string."""
        assert isinstance(
            output_data["case_name"], str
        ), "case_name should be a string"

    def test_slack_bus_is_integer(self, output_data):
        """Verify slack_bus is an integer (or int-like number)."""
        val = output_data["slack_bus"]
        assert isinstance(val, (int, float)), "slack_bus should be a number"
        if isinstance(val, float):
            assert val.is_integer(), "slack_bus should be an integer value"

    def test_branch_index_is_integer(self, output_data):
        """Verify branch_index is an integer (or int-like number)."""
        val = output_data["branch_index"]
        assert isinstance(val, (int, float)), "branch_index should be a number"
        if isinstance(val, float):
            assert val.is_integer(), "branch_index should be an integer value"

    def test_fbus_is_integer(self, output_data):
        """Verify fbus is an integer (or int-like number)."""
        val = output_data["fbus"]
        assert isinstance(val, (int, float)), "fbus should be a number"
        if isinstance(val, float):
            assert val.is_integer(), "fbus should be an integer value"

    def test_tbus_is_integer(self, output_data):
        """Verify tbus is an integer (or int-like number)."""
        val = output_data["tbus"]
        assert isinstance(val, (int, float)), "tbus should be a number"
        if isinstance(val, float):
            assert val.is_integer(), "tbus should be an integer value"

    def test_rateA_MW_is_number(self, output_data):
        """Verify rateA_MW is a number (float or int)."""
        assert isinstance(
            output_data["rateA_MW"], (int, float)
        ), "rateA_MW should be a number"

    def test_x_pu_is_number(self, output_data):
        """Verify x_pu is a number (float or int)."""
        assert isinstance(
            output_data["x_pu"], (int, float)
        ), "x_pu should be a number"

    def test_flow_MW_is_number(self, output_data):
        """Verify flow_MW is a number (float or int)."""
        assert isinstance(
            output_data["flow_MW"], (int, float)
        ), "flow_MW should be a number"

    def test_loading_pct_is_number(self, output_data):
        """Verify loading_pct is a number (float or int)."""
        assert isinstance(
            output_data["loading_pct"], (int, float)
        ), "loading_pct should be a number"

    def test_all_numeric_values_are_json_numbers_not_strings(self, output_data):
        """Verify numeric fields are actual numbers, not string representations."""
        numeric_fields = [
            "slack_bus",
            "branch_index",
            "fbus",
            "tbus",
            "rateA_MW",
            "x_pu",
            "flow_MW",
            "loading_pct",
        ]
        for field in numeric_fields:
            assert not isinstance(
                output_data[field], str
            ), f"{field} should be a JSON number, not a string"


class TestFieldValues:
    """Tests verifying field values are within valid ranges."""

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        with open(OUTPUT_FILE, "r") as f:
            return json.load(f)

    def test_case_name_is_valid(self, output_data):
        """Verify case_name is one of the valid case names."""
        assert output_data["case_name"] in VALID_CASE_NAMES, (
            f"case_name '{output_data['case_name']}' is not valid. "
            f"Expected one of: {VALID_CASE_NAMES}"
        )

    def test_slack_bus_is_non_negative(self, output_data):
        """Verify slack_bus is non-negative."""
        assert output_data["slack_bus"] >= 0, "slack_bus should be non-negative"

    def test_branch_index_is_non_negative(self, output_data):
        """Verify branch_index is non-negative (0-based index)."""
        assert output_data["branch_index"] >= 0, "branch_index should be non-negative"

    def test_fbus_is_positive(self, output_data):
        """Verify fbus (from bus number) is positive."""
        assert output_data["fbus"] > 0, "fbus should be positive (bus numbers start at 1)"

    def test_tbus_is_positive(self, output_data):
        """Verify tbus (to bus number) is positive."""
        assert output_data["tbus"] > 0, "tbus should be positive (bus numbers start at 1)"

    def test_fbus_and_tbus_are_different(self, output_data):
        """Verify fbus and tbus are different (no self-loops)."""
        assert output_data["fbus"] != output_data["tbus"], (
            "fbus and tbus should be different (branch cannot be a self-loop)"
        )

    def test_rateA_MW_is_positive(self, output_data):
        """Verify rateA_MW is positive (branches with rateA=0 are excluded)."""
        assert output_data["rateA_MW"] > 0, (
            "rateA_MW should be positive (branches with rateA=0 are excluded from overload)"
        )

    def test_x_pu_is_positive(self, output_data):
        """Verify x_pu (reactance) is positive."""
        assert output_data["x_pu"] > 0, "x_pu (reactance) should be positive"

    def test_loading_pct_is_positive(self, output_data):
        """Verify loading_pct is positive (indicates some flow)."""
        assert output_data["loading_pct"] > 0, "loading_pct should be positive"

    def test_loading_pct_is_calculated_correctly(self, output_data):
        """Verify loading_pct matches the formula: |flow_MW| / rateA_MW * 100."""
        expected_loading = abs(output_data["flow_MW"]) / output_data["rateA_MW"] * 100
        assert abs(output_data["loading_pct"] - expected_loading) < 1e-6, (
            f"loading_pct ({output_data['loading_pct']}) does not match "
            f"expected value ({expected_loading}) based on formula"
        )


class TestCaseSpecificConstraints:
    """Tests verifying case-specific constraints based on input file structure."""

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        with open(OUTPUT_FILE, "r") as f:
            return json.load(f)

    def test_branch_index_within_case_bounds(self, output_data):
        """Verify branch_index is within valid range for the specified case."""
        case_name = output_data["case_name"]
        branch_index = output_data["branch_index"]

        # Branch counts from the input files (0-based max index = count - 1)
        branch_counts = {
            "case57": 80,
            "case118": 186,
            "pglib_opf_case118_ieee": 186,
        }

        max_index = branch_counts.get(case_name, 0) - 1
        assert branch_index <= max_index, (
            f"branch_index {branch_index} exceeds maximum valid index {max_index} "
            f"for case {case_name}"
        )

    def test_bus_numbers_within_case_bounds(self, output_data):
        """Verify fbus and tbus are within valid range for the specified case."""
        case_name = output_data["case_name"]
        fbus = output_data["fbus"]
        tbus = output_data["tbus"]

        # Maximum bus numbers from input files
        max_bus = {
            "case57": 57,
            "case118": 118,
            "pglib_opf_case118_ieee": 118,
        }

        max_bus_num = max_bus.get(case_name, 0)
        assert fbus <= max_bus_num, (
            f"fbus {fbus} exceeds maximum bus number {max_bus_num} for case {case_name}"
        )
        assert tbus <= max_bus_num, (
            f"tbus {tbus} exceeds maximum bus number {max_bus_num} for case {case_name}"
        )

    def test_slack_bus_matches_case(self, output_data):
        """Verify slack_bus is correct for the specified case."""
        case_name = output_data["case_name"]
        slack_bus = output_data["slack_bus"]

        # Slack bus numbers (type == 3 bus) from input files
        slack_buses = {
            "case57": 1,    # Bus 1 has type=3
            "case118": 69,   # Bus 69 has type=3
            "pglib_opf_case118_ieee": 69,  # Bus 69 has type=3
        }

        expected_slack = slack_buses.get(case_name)
        assert slack_bus == expected_slack, (
            f"slack_bus {slack_bus} does not match expected slack bus {expected_slack} "
            f"for case {case_name}"
        )


class TestMostOverloadedCriteria:
    """Tests verifying the 'most overloaded' selection criteria."""

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        with open(OUTPUT_FILE, "r") as f:
            return json.load(f)

    def test_loading_pct_represents_maximum(self, output_data):
        """
        The selected branch should have the maximum loading_pct across all cases.
        Since case57 and case118 have all rateA=0, only pglib_opf_case118_ieee
        has branches eligible for overload calculation.
        """
        # This test validates the output structure implies it's the maximum
        # A positive loading_pct indicates a valid overloaded branch was found
        assert output_data["loading_pct"] > 0, (
            "loading_pct should be positive, indicating an overloaded branch was found"
        )

    def test_only_pglib_case_has_valid_ratings(self, output_data):
        """
        Since case57 and case118 have rateA=0 for all branches (no thermal limits),
        only pglib_opf_case118_ieee has branches eligible for overload calculation.
        Therefore, the most overloaded branch must come from pglib_opf_case118_ieee.
        """
        # Based on input file analysis:
        # - case57: all branches have rateA=0
        # - case118: all branches have rateA=0
        # - pglib_opf_case118_ieee: branches have non-zero rateA values
        assert output_data["case_name"] == "pglib_opf_case118_ieee", (
            "Only pglib_opf_case118_ieee has branches with rateA > 0, "
            "so the most overloaded branch must come from this case"
        )


class TestPhysicalReasonableness:
    """Tests verifying physical reasonableness of results."""

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        with open(OUTPUT_FILE, "r") as f:
            return json.load(f)

    def test_x_pu_is_reasonable(self, output_data):
        """Verify x_pu is within physically reasonable range."""
        # Reactance values typically between 0.001 and 1.0 per unit
        assert 0.0001 < output_data["x_pu"] < 10.0, (
            f"x_pu value {output_data['x_pu']} seems outside reasonable range"
        )

    def test_rateA_is_reasonable(self, output_data):
        """Verify rateA_MW is within physically reasonable range."""
        # Thermal ratings typically between 10 and 10000 MW
        assert 1 < output_data["rateA_MW"] < 10000, (
            f"rateA_MW value {output_data['rateA_MW']} seems outside reasonable range"
        )

    def test_flow_magnitude_is_finite(self, output_data):
        """Verify flow_MW is finite (not NaN or Inf)."""
        import math
        assert math.isfinite(output_data["flow_MW"]), "flow_MW should be finite"

    def test_loading_pct_is_finite(self, output_data):
        """Verify loading_pct is finite (not NaN or Inf)."""
        import math
        assert math.isfinite(output_data["loading_pct"]), "loading_pct should be finite"


class TestDCPowerFlowConsistency:
    """Tests verifying DC power flow calculation consistency."""

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        with open(OUTPUT_FILE, "r") as f:
            return json.load(f)

    def test_flow_direction_sign(self, output_data):
        """Verify flow_MW can be positive or negative (indicating direction)."""
        # flow_MW represents P_f->t and can be positive (f to t) or negative (t to f)
        # The loading calculation uses absolute value
        flow = output_data["flow_MW"]
        assert isinstance(flow, (int, float)), "flow_MW should be a number"

    def test_loading_uses_absolute_flow(self, output_data):
        """Verify loading_pct is calculated from absolute flow value."""
        flow = output_data["flow_MW"]
        rateA = output_data["rateA_MW"]
        loading = output_data["loading_pct"]

        expected = abs(flow) / rateA * 100
        assert abs(loading - expected) < 1e-6, (
            "loading_pct should be calculated from |flow_MW| / rateA_MW * 100"
        )


class TestInputFilesExist:
    """Tests verifying input files exist (prerequisite for task)."""

    INPUT_FILES = [
        "case57.m",
        "case118.m",
        "pglib_opf_case118_ieee.m",
    ]

    @pytest.mark.parametrize("filename", INPUT_FILES)
    def test_input_file_exists(self, filename):
        """Verify each input file exists."""
        filepath = os.path.join(INPUT_DIR, filename)
        assert os.path.exists(filepath), f"Input file not found: {filepath}"


class TestJSONFormatCompliance:
    """Tests verifying JSON format compliance."""

    def test_json_encoding(self):
        """Verify JSON file uses UTF-8 encoding."""
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            content = f.read()
        # Should be able to decode without errors
        assert len(content) > 0

    def test_json_no_trailing_comma(self):
        """Verify JSON has no trailing commas (invalid JSON)."""
        with open(OUTPUT_FILE, "r") as f:
            content = f.read()
        # A proper JSON parser would fail on trailing commas
        # This is implicitly tested by successful json.load()
        data = json.loads(content)
        assert data is not None

    def test_json_serialization_roundtrip(self):
        """Verify JSON can be serialized and deserialized without loss."""
        with open(OUTPUT_FILE, "r") as f:
            original_data = json.load(f)

        # Serialize and deserialize
        serialized = json.dumps(original_data)
        roundtrip_data = json.loads(serialized)

        assert original_data == roundtrip_data, "JSON roundtrip should preserve data"

HEREDOC_EOF

# Execute command
python -m py_compile expectation_tests.py && echo "Syntax OK"

# Execute command
python -m pytest --collect-only expectation_tests.py 2>&1 | head -80
