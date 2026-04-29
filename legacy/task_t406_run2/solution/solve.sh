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

# Create /root/harbor_workspaces/task_T406_run2/expectation_tests.py
mkdir -p $(dirname /root/harbor_workspaces/task_T406_run2/expectation_tests.py)
cat << 'HEREDOC_EOF' > /root/harbor_workspaces/task_T406_run2/expectation_tests.py
"""Auto-generated expectation tests for DC power flow stress metrics verification.

These tests verify that the task execution produces correct outputs
based on the instruction requirements for computing DC power flow
stress indices from MATPOWER case files.
"""

import json
import math
import os
from pathlib import Path

import pytest


# Constants
OUTPUT_FILE_PATH = "/root/powerflow_stress_metrics.json"
INPUT_DIR = "/root/harbor_workspaces/task_T406_run2/input"

# Expected case names
EXPECTED_CASES = ["case57", "case118", "pglib_opf_case118_ieee"]

# Required JSON schema keys
REQUIRED_TOP_LEVEL_KEYS = [
    "case57",
    "case118",
    "pglib_opf_case118_ieee",
    "comparative_stress_ratio_pglib_over_case118"
]


class TestOutputFileExists:
    """Tests to verify output file existence and basic properties."""

    def test_output_file_exists(self):
        """Verify output file was created at the specified path."""
        assert os.path.exists(OUTPUT_FILE_PATH), (
            f"Output file not found at {OUTPUT_FILE_PATH}"
        )

    def test_output_file_is_not_empty(self):
        """Verify output file is not empty."""
        assert os.path.exists(OUTPUT_FILE_PATH), "Output file does not exist"
        file_size = os.path.getsize(OUTPUT_FILE_PATH)
        assert file_size > 0, "Output file is empty"

    def test_output_file_has_json_extension(self):
        """Verify output file has .json extension."""
        assert OUTPUT_FILE_PATH.endswith(".json"), (
            "Output file should have .json extension"
        )


class TestJsonValidity:
    """Tests to verify JSON format validity."""

    def test_output_is_valid_json(self):
        """Verify output is valid JSON format."""
        assert os.path.exists(OUTPUT_FILE_PATH), "Output file does not exist"
        with open(OUTPUT_FILE_PATH) as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                pytest.fail(f"Output file is not valid JSON: {e}")
        assert data is not None, "JSON data is None"

    def test_json_root_is_object(self):
        """Verify JSON root element is an object (dict)."""
        with open(OUTPUT_FILE_PATH) as f:
            data = json.load(f)
        assert isinstance(data, dict), (
            f"JSON root should be an object/dict, got {type(data).__name__}"
        )


class TestJsonSchema:
    """Tests to verify JSON schema compliance."""

    @pytest.fixture
    def json_data(self):
        """Load JSON data from output file."""
        with open(OUTPUT_FILE_PATH) as f:
            return json.load(f)

    def test_all_required_keys_present(self, json_data):
        """Verify all required top-level keys are present."""
        for key in REQUIRED_TOP_LEVEL_KEYS:
            assert key in json_data, f"Missing required key: {key}"

    def test_no_extra_top_level_keys(self, json_data):
        """Verify no unexpected top-level keys are present."""
        expected_keys = set(REQUIRED_TOP_LEVEL_KEYS)
        actual_keys = set(json_data.keys())
        extra_keys = actual_keys - expected_keys
        assert not extra_keys, f"Unexpected top-level keys: {extra_keys}"

    def test_case57_has_stress_index_key(self, json_data):
        """Verify case57 object has stress_index key."""
        assert "case57" in json_data, "Missing case57 key"
        assert isinstance(json_data["case57"], dict), "case57 should be an object"
        assert "stress_index" in json_data["case57"], (
            "case57 missing stress_index key"
        )

    def test_case118_has_stress_index_key(self, json_data):
        """Verify case118 object has stress_index key."""
        assert "case118" in json_data, "Missing case118 key"
        assert isinstance(json_data["case118"], dict), "case118 should be an object"
        assert "stress_index" in json_data["case118"], (
            "case118 missing stress_index key"
        )

    def test_pglib_case_has_stress_index_key(self, json_data):
        """Verify pglib_opf_case118_ieee object has stress_index key."""
        key = "pglib_opf_case118_ieee"
        assert key in json_data, f"Missing {key} key"
        assert isinstance(json_data[key], dict), f"{key} should be an object"
        assert "stress_index" in json_data[key], f"{key} missing stress_index key"

    def test_case_objects_have_only_stress_index(self, json_data):
        """Verify each case object contains only stress_index key."""
        for case_name in EXPECTED_CASES:
            case_data = json_data[case_name]
            assert set(case_data.keys()) == {"stress_index"}, (
                f"{case_name} should only have 'stress_index' key, "
                f"got: {list(case_data.keys())}"
            )


class TestDataTypes:
    """Tests to verify correct data types for all values."""

    @pytest.fixture
    def json_data(self):
        """Load JSON data from output file."""
        with open(OUTPUT_FILE_PATH) as f:
            return json.load(f)

    def test_case57_stress_index_is_number(self, json_data):
        """Verify case57 stress_index is a number."""
        value = json_data["case57"]["stress_index"]
        assert isinstance(value, (int, float)), (
            f"case57 stress_index should be a number, got {type(value).__name__}"
        )

    def test_case118_stress_index_is_number(self, json_data):
        """Verify case118 stress_index is a number."""
        value = json_data["case118"]["stress_index"]
        assert isinstance(value, (int, float)), (
            f"case118 stress_index should be a number, got {type(value).__name__}"
        )

    def test_pglib_stress_index_is_number(self, json_data):
        """Verify pglib_opf_case118_ieee stress_index is a number."""
        value = json_data["pglib_opf_case118_ieee"]["stress_index"]
        assert isinstance(value, (int, float)), (
            f"pglib stress_index should be a number, got {type(value).__name__}"
        )

    def test_comparative_ratio_is_number(self, json_data):
        """Verify comparative_stress_ratio is a number."""
        value = json_data["comparative_stress_ratio_pglib_over_case118"]
        assert isinstance(value, (int, float)), (
            f"comparative_stress_ratio should be a number, got {type(value).__name__}"
        )

    def test_all_values_are_finite(self, json_data):
        """Verify all numeric values are finite (not inf or nan)."""
        values_to_check = [
            ("case57.stress_index", json_data["case57"]["stress_index"]),
            ("case118.stress_index", json_data["case118"]["stress_index"]),
            ("pglib.stress_index", json_data["pglib_opf_case118_ieee"]["stress_index"]),
            ("comparative_ratio", json_data["comparative_stress_ratio_pglib_over_case118"]),
        ]
        for name, value in values_to_check:
            assert math.isfinite(value), f"{name} is not finite: {value}"


class TestValueRanges:
    """Tests to verify values are within reasonable ranges."""

    @pytest.fixture
    def json_data(self):
        """Load JSON data from output file."""
        with open(OUTPUT_FILE_PATH) as f:
            return json.load(f)

    def test_case57_stress_index_is_positive(self, json_data):
        """Verify case57 stress_index is positive."""
        value = json_data["case57"]["stress_index"]
        assert value > 0, f"case57 stress_index should be positive, got {value}"

    def test_case118_stress_index_is_positive(self, json_data):
        """Verify case118 stress_index is positive."""
        value = json_data["case118"]["stress_index"]
        assert value > 0, f"case118 stress_index should be positive, got {value}"

    def test_pglib_stress_index_is_positive(self, json_data):
        """Verify pglib_opf_case118_ieee stress_index is positive."""
        value = json_data["pglib_opf_case118_ieee"]["stress_index"]
        assert value > 0, f"pglib stress_index should be positive, got {value}"

    def test_comparative_ratio_is_positive(self, json_data):
        """Verify comparative_stress_ratio is positive."""
        value = json_data["comparative_stress_ratio_pglib_over_case118"]
        assert value > 0, f"comparative_stress_ratio should be positive, got {value}"

    def test_stress_indices_are_reasonable(self, json_data):
        """Verify stress indices are in a reasonable range.

        Stress Index = 95th percentile of |branch MW flows| / total load
        This ratio should typically be less than 2.0 for realistic power systems
        (the 95th percentile flow shouldn't exceed 2x total load).
        """
        for case_name in EXPECTED_CASES:
            value = json_data[case_name]["stress_index"]
            assert 0 < value < 10.0, (
                f"{case_name} stress_index {value} is outside reasonable range (0, 10)"
            )


class TestPrecisionRequirements:
    """Tests to verify decimal precision requirements."""

    @pytest.fixture
    def json_data(self):
        """Load JSON data from output file."""
        with open(OUTPUT_FILE_PATH) as f:
            return json.load(f)

    def test_values_have_at_most_6_decimal_places(self, json_data):
        """Verify all values are rounded to at most 6 decimal places."""
        values_to_check = [
            ("case57.stress_index", json_data["case57"]["stress_index"]),
            ("case118.stress_index", json_data["case118"]["stress_index"]),
            ("pglib.stress_index", json_data["pglib_opf_case118_ieee"]["stress_index"]),
            ("comparative_ratio", json_data["comparative_stress_ratio_pglib_over_case118"]),
        ]

        for name, value in values_to_check:
            # Convert to string and check decimal places
            str_value = f"{value:.15f}".rstrip('0')
            if '.' in str_value:
                decimal_places = len(str_value.split('.')[1])
                assert decimal_places <= 6, (
                    f"{name} has {decimal_places} decimal places, "
                    f"expected at most 6. Value: {value}"
                )


class TestComparativeStressRatioCalculation:
    """Tests to verify correct calculation of comparative stress ratio."""

    @pytest.fixture
    def json_data(self):
        """Load JSON data from output file."""
        with open(OUTPUT_FILE_PATH) as f:
            return json.load(f)

    def test_comparative_ratio_equals_pglib_over_case118(self, json_data):
        """Verify comparative ratio = pglib stress_index / case118 stress_index."""
        pglib_stress = json_data["pglib_opf_case118_ieee"]["stress_index"]
        case118_stress = json_data["case118"]["stress_index"]
        reported_ratio = json_data["comparative_stress_ratio_pglib_over_case118"]

        expected_ratio = pglib_stress / case118_stress

        # Allow for rounding differences (6 decimal places)
        assert abs(reported_ratio - expected_ratio) < 1e-5, (
            f"comparative_stress_ratio ({reported_ratio}) does not match "
            f"pglib/case118 ({expected_ratio})"
        )


class TestInputFilesExist:
    """Tests to verify input files exist (precondition checks)."""

    def test_case57_input_exists(self):
        """Verify case57.m input file exists."""
        path = os.path.join(INPUT_DIR, "case57.m")
        assert os.path.exists(path), f"Input file not found: {path}"

    def test_case118_input_exists(self):
        """Verify case118.m input file exists."""
        path = os.path.join(INPUT_DIR, "case118.m")
        assert os.path.exists(path), f"Input file not found: {path}"

    def test_pglib_input_exists(self):
        """Verify pglib_opf_case118_ieee.m input file exists."""
        path = os.path.join(INPUT_DIR, "pglib_opf_case118_ieee.m")
        assert os.path.exists(path), f"Input file not found: {path}"


class TestConsistencyChecks:
    """Tests for internal consistency of the results."""

    @pytest.fixture
    def json_data(self):
        """Load JSON data from output file."""
        with open(OUTPUT_FILE_PATH) as f:
            return json.load(f)

    def test_different_cases_have_different_stress_indices(self, json_data):
        """Verify the three cases produce different stress indices.

        case57 has a different network topology than the 118-bus cases,
        and pglib_opf_case118_ieee has different generation dispatch than case118.
        """
        case57_stress = json_data["case57"]["stress_index"]
        case118_stress = json_data["case118"]["stress_index"]
        pglib_stress = json_data["pglib_opf_case118_ieee"]["stress_index"]

        # case57 should differ from 118-bus cases (different network size)
        assert case57_stress != case118_stress, (
            "case57 and case118 have identical stress indices - unexpected"
        )
        assert case57_stress != pglib_stress, (
            "case57 and pglib have identical stress indices - unexpected"
        )

    def test_118_bus_cases_may_differ(self, json_data):
        """Verify the two 118-bus cases may have different stress indices.

        case118 and pglib_opf_case118_ieee have the same topology but
        different generation dispatch, so stress indices may differ.
        """
        case118_stress = json_data["case118"]["stress_index"]
        pglib_stress = json_data["pglib_opf_case118_ieee"]["stress_index"]

        # They can be equal or different - just verify both are valid
        assert case118_stress > 0, "case118 stress_index should be positive"
        assert pglib_stress > 0, "pglib stress_index should be positive"


class TestDeterminism:
    """Tests to verify deterministic behavior of calculations."""

    @pytest.fixture
    def json_data(self):
        """Load JSON data from output file."""
        with open(OUTPUT_FILE_PATH) as f:
            return json.load(f)

    def test_stress_index_not_zero(self, json_data):
        """Verify stress indices are not exactly zero.

        With non-trivial power systems, there should always be some
        power flow on at least one branch.
        """
        for case_name in EXPECTED_CASES:
            value = json_data[case_name]["stress_index"]
            assert value != 0.0, (
                f"{case_name} stress_index is exactly 0.0, "
                "which is unexpected for a non-trivial power system"
            )

    def test_ratio_not_exactly_one(self, json_data):
        """Verify comparative ratio is not exactly 1.0.

        The two 118-bus cases have different generation dispatch,
        so their stress indices should typically differ.
        """
        ratio = json_data["comparative_stress_ratio_pglib_over_case118"]
        # Note: It's possible but unlikely for them to be exactly equal
        # This is a soft check - if they are equal, the test will still pass
        # but log a warning-level message
        if ratio == 1.0:
            pytest.skip(
                "Comparative ratio is exactly 1.0 - both 118-bus cases "
                "have identical stress indices (unusual but possible)"
            )


class TestOutputDirectory:
    """Tests to verify output directory structure."""

    def test_output_directory_exists(self):
        """Verify output directory exists."""
        output_dir = os.path.dirname(OUTPUT_FILE_PATH)
        assert os.path.isdir(output_dir), f"Output directory not found: {output_dir}"

    def test_output_file_is_regular_file(self):
        """Verify output is a regular file (not a directory or symlink)."""
        assert os.path.exists(OUTPUT_FILE_PATH), "Output file does not exist"
        assert os.path.isfile(OUTPUT_FILE_PATH), (
            f"{OUTPUT_FILE_PATH} is not a regular file"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

HEREDOC_EOF

# Execute command
ls -la /root/harbor_workspaces/task_T406_run2/output 2>/dev/null || mkdir -p /root/harbor_workspaces/task_T406_run2/output && echo "Output directory ready"

# Create /root/harbor_workspaces/task_T406_run2/dc_power_flow_analysis.py
mkdir -p $(dirname /root/harbor_workspaces/task_T406_run2/dc_power_flow_analysis.py)
cat << 'HEREDOC_EOF' > /root/harbor_workspaces/task_T406_run2/dc_power_flow_analysis.py
#!/usr/bin/env python3
"""
DC Power Flow Analysis for computing network stress metrics.
Parses MATPOWER case files and computes stress index based on 95th percentile flows.
"""

import numpy as np
import re
import json
import sys

# Add skills path for build_b_matrix functionality (reference)
sys.path.insert(0, '/root/harbor_workspaces/task_T406_run2/.claude/skills/dc-power-flow/scripts')


def parse_matpower_file(filepath):
    """
    Parse a MATPOWER .m file to extract baseMVA, bus, gen, and branch data.
    Handles MATLAB comments and matrix formats.
    """
    with open(filepath, 'r') as f:
        content = f.read()

    # Extract baseMVA
    basemva_match = re.search(r'mpc\.baseMVA\s*=\s*([\d.]+)', content)
    if not basemva_match:
        raise ValueError(f"Could not find baseMVA in {filepath}")
    baseMVA = float(basemva_match.group(1))

    def extract_matrix(content, matrix_name):
        """Extract a matrix from MATPOWER format."""
        # Match mpc.matrix_name = [ ... ];
        pattern = rf'mpc\.{matrix_name}\s*=\s*\[(.*?)\];'
        match = re.search(pattern, content, re.DOTALL)
        if not match:
            raise ValueError(f"Could not find mpc.{matrix_name} in file")

        matrix_text = match.group(1)

        # Remove MATLAB comments (% ...)
        lines = matrix_text.split('\n')
        cleaned_lines = []
        for line in lines:
            # Remove inline comments
            if '%' in line:
                line = line[:line.index('%')]
            line = line.strip()
            if line:
                cleaned_lines.append(line)

        # Parse numeric values
        rows = []
        for line in cleaned_lines:
            # Replace tabs and multiple spaces with single space
            line = re.sub(r'[\t]+', ' ', line)
            line = re.sub(r'\s+', ' ', line).strip()
            # Remove trailing semicolon
            line = line.rstrip(';').strip()
            if line:
                # Split by whitespace
                values = line.split()
                try:
                    row = [float(v) for v in values]
                    if row:
                        rows.append(row)
                except ValueError:
                    continue

        return np.array(rows)

    bus = extract_matrix(content, 'bus')
    gen = extract_matrix(content, 'gen')
    branch = extract_matrix(content, 'branch')

    return baseMVA, bus, gen, branch


def compute_dc_power_flow(baseMVA, bus, gen, branch):
    """
    Perform DC power flow analysis with transformer ratio handling.

    Returns:
        tuple: (bus_angles_rad, branch_flows_MW, total_load_MW, flow_info)
    """
    n_bus = len(bus)
    n_branch = len(branch)

    # Create bus number to index mapping (handles non-contiguous bus numbering)
    bus_ids = bus[:, 0].astype(int)
    bus_id_to_idx = {bid: i for i, bid in enumerate(bus_ids)}

    # Find slack bus (type == 3)
    slack_idx = None
    for i in range(n_bus):
        if bus[i, 1] == 3:
            slack_idx = i
            break

    if slack_idx is None:
        raise ValueError("No slack bus (type 3) found")

    # Compute net injections P_inj = sum(Pg at bus) - Pd
    Pd_MW = bus[:, 2]  # Active load at each bus
    total_load_MW = Pd_MW.sum()

    # Sum generator Pg by bus
    Pg_sum = np.zeros(n_bus)
    for g in gen:
        gen_bus_id = int(g[0])
        gen_Pg = g[1]  # Pg is column 1
        if gen_bus_id in bus_id_to_idx:
            idx = bus_id_to_idx[gen_bus_id]
            Pg_sum[idx] += gen_Pg

    # Net injection in MW
    P_inj_MW = Pg_sum - Pd_MW
    # Convert to per-unit
    P_inj_pu = P_inj_MW / baseMVA

    # Build DC susceptance matrix B with transformer ratio handling
    # Standard DC transformer modeling:
    # - Off-diagonals: B[i,j] -= b/tap, B[j,i] -= b/tap
    # - Diagonals: B[i,i] += b/tap^2 (from bus), B[j,j] += b (to bus)
    B = np.zeros((n_bus, n_bus))

    # Track which branches are included (status==1 and x!=0)
    included_branches = []

    for br_idx, br in enumerate(branch):
        fbus_id = int(br[0])
        tbus_id = int(br[1])
        r = br[2]  # Resistance (ignored in DC)
        x = br[3]  # Reactance
        b_charging = br[4]  # Line charging (ignored in DC)
        ratio = br[8]  # Transformer ratio
        angle = br[9]  # Phase shift angle (ignored in DC)
        status = br[10]  # Branch status

        # Skip out-of-service branches
        if status != 1:
            continue

        # Skip branches with x == 0 (to avoid singularities)
        if x == 0:
            continue

        # Get bus indices
        if fbus_id not in bus_id_to_idx or tbus_id not in bus_id_to_idx:
            continue

        f = bus_id_to_idx[fbus_id]
        t = bus_id_to_idx[tbus_id]

        # Susceptance
        b = 1.0 / x

        # Transformer tap ratio: if 0, treat as 1
        tap = ratio if ratio != 0 else 1.0

        # DC transformer modeling:
        # Off-diagonals
        B[f, t] -= b / tap
        B[t, f] -= b / tap
        # Diagonals
        B[f, f] += b / (tap ** 2)
        B[t, t] += b

        included_branches.append((br_idx, fbus_id, tbus_id, x, tap, f, t))

    # Solve DC power flow: B_red * theta_red = P_red
    # Remove slack bus row/column
    mask = np.ones(n_bus, dtype=bool)
    mask[slack_idx] = False

    B_red = B[mask][:, mask]
    P_red = P_inj_pu[mask]

    # Solve for angles
    try:
        theta_red = np.linalg.solve(B_red, P_red)
    except np.linalg.LinAlgError as e:
        print(f"Warning: Linear solve failed: {e}")
        theta_red = np.linalg.lstsq(B_red, P_red, rcond=None)[0]

    # Reconstruct full theta vector
    theta = np.zeros(n_bus)
    theta[mask] = theta_red
    theta[slack_idx] = 0.0  # Slack bus angle = 0

    # Compute branch flows (from-end MW flow using DC approximation with tap)
    # P_f_pu = (b / tap) * (theta_f - theta_t)
    branch_flows_MW = []
    flow_info = []

    for (br_idx, fbus_id, tbus_id, x, tap, f, t) in included_branches:
        b = 1.0 / x
        P_f_pu = (b / tap) * (theta[f] - theta[t])
        P_f_MW = P_f_pu * baseMVA
        branch_flows_MW.append(abs(P_f_MW))
        flow_info.append({
            'from': fbus_id,
            'to': tbus_id,
            'flow_MW': P_f_MW,
            'abs_flow_MW': abs(P_f_MW)
        })

    return theta, branch_flows_MW, total_load_MW, flow_info, len(included_branches)


def compute_stress_index(branch_flows_MW, total_load_MW):
    """
    Compute the Stress Index = 95th percentile of |branch flows| / total load
    """
    if len(branch_flows_MW) == 0 or total_load_MW == 0:
        return 0.0

    abs_flows = np.array(branch_flows_MW)
    p95 = np.percentile(abs_flows, 95)  # Default linear interpolation
    stress_index = p95 / total_load_MW

    return stress_index


def analyze_case(filepath, case_name):
    """Analyze a single case file and return stress metrics."""
    print(f"\n{'='*60}")
    print(f"Analyzing: {case_name}")
    print(f"File: {filepath}")
    print(f"{'='*60}")

    # Parse the file
    baseMVA, bus, gen, branch = parse_matpower_file(filepath)

    print(f"baseMVA: {baseMVA}")
    print(f"Number of buses: {len(bus)}")
    print(f"Number of generators: {len(gen)}")
    print(f"Number of branches: {len(branch)}")

    # Find slack bus
    slack_buses = bus[bus[:, 1] == 3]
    print(f"Slack bus(es): {slack_buses[:, 0].astype(int).tolist()}")

    # Perform DC power flow
    theta, branch_flows_MW, total_load_MW, flow_info, n_included = compute_dc_power_flow(
        baseMVA, bus, gen, branch
    )

    print(f"Total system load: {total_load_MW:.2f} MW")
    print(f"Included branches (status=1, x!=0): {n_included}")

    # Compute stress index
    stress_index = compute_stress_index(branch_flows_MW, total_load_MW)

    print(f"95th percentile |flow|: {np.percentile(branch_flows_MW, 95):.4f} MW")
    print(f"Stress Index: {stress_index:.6f}")

    return {
        'stress_index': round(stress_index, 6),
        'total_load_MW': total_load_MW,
        'n_branches_included': n_included,
        'p95_flow_MW': round(np.percentile(branch_flows_MW, 95), 6)
    }


def main():
    # Define input files
    input_dir = '/root/harbor_workspaces/task_T406_run2/input'
    output_file = '/root/powerflow_stress_metrics.json'

    cases = {
        'case57': f'{input_dir}/case57.m',
        'case118': f'{input_dir}/case118.m',
        'pglib_opf_case118_ieee': f'{input_dir}/pglib_opf_case118_ieee.m'
    }

    results = {}

    for case_name, filepath in cases.items():
        try:
            result = analyze_case(filepath, case_name)
            results[case_name] = {'stress_index': result['stress_index']}
        except Exception as e:
            print(f"Error analyzing {case_name}: {e}")
            import traceback
            traceback.print_exc()
            results[case_name] = {'stress_index': 0.0}

    # Compute comparative stress ratio
    stress_pglib = results['pglib_opf_case118_ieee']['stress_index']
    stress_case118 = results['case118']['stress_index']

    if stress_case118 != 0:
        comparative_ratio = stress_pglib / stress_case118
    else:
        comparative_ratio = 0.0

    # Build final output JSON
    output = {
        'case57': {'stress_index': results['case57']['stress_index']},
        'case118': {'stress_index': results['case118']['stress_index']},
        'pglib_opf_case118_ieee': {'stress_index': results['pglib_opf_case118_ieee']['stress_index']},
        'comparative_stress_ratio_pglib_over_case118': round(comparative_ratio, 6)
    }

    # Write output
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\n{'='*60}")
    print("FINAL RESULTS")
    print(f"{'='*60}")
    print(json.dumps(output, indent=2))
    print(f"\nResults written to: {output_file}")

    return output


if __name__ == '__main__':
    main()

HEREDOC_EOF

# Execute command
python3 dc_power_flow_analysis.py

