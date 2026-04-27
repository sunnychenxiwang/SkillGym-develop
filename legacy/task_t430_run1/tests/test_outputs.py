"""Auto-generated expectation tests for task verification.

These tests verify that the task execution produces correct outputs
based on the instruction requirements for finding the transmission branch
with the largest absolute percentage change in series reactance between
two 118-bus MATPOWER datasets, filtered by branches existing in case57.
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional

import pytest


OUTPUT_FILE = "/root/max_reactance_change.json"
INPUT_CASE57 = "/root/case57.m"
INPUT_CASE118 = "/root/case118.m"
INPUT_PGLIB = "/root/pglib_opf_case118_ieee.m"

FLOAT_TOLERANCE = 1e-12


def strip_matlab_comments(content: str) -> str:
    """Remove MATLAB comments (% to end of line) robustly.

    Handles various comment styles including inline comments.
    """
    lines = []
    for line in content.split('\n'):
        if '%' in line:
            line = line[:line.index('%')]
        lines.append(line)
    return '\n'.join(lines)


def parse_matpower_branches(filepath: str) -> Dict[Tuple[int, int], List[float]]:
    """Parse MATPOWER file and extract branch data with robust handling.

    Returns dict mapping (min_bus, max_bus) -> list of x values.

    This parser handles:
    - MATLAB comments (%)
    - Multi-line matrix definitions
    - Various whitespace patterns (tabs, multiple spaces)
    - Trailing semicolons on data rows
    - Scientific notation in numbers
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"MATPOWER file not found: {filepath}")

    with open(filepath, 'r') as f:
        content = f.read()

    content_no_comments = strip_matlab_comments(content)

    branch_pattern = r'mpc\.branch\s*=\s*\[(.*?)\];'
    branch_match = re.search(branch_pattern, content_no_comments, re.DOTALL)

    if not branch_match:
        raise ValueError(
            f"Could not find 'mpc.branch = [ ... ];' block in {filepath}. "
            "Check that the file is a valid MATPOWER case file with branch data."
        )

    branch_data = branch_match.group(1)
    branches: Dict[Tuple[int, int], List[float]] = {}

    float_pattern = re.compile(r'[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?')

    for line in branch_data.strip().split('\n'):
        line = line.strip()
        if not line:
            continue

        line = line.rstrip(';').strip()
        if not line:
            continue

        numbers = float_pattern.findall(line)

        if len(numbers) >= 4:
            try:
                fbus = int(float(numbers[0]))
                tbus = int(float(numbers[1]))
                x = float(numbers[3])

                pair = (min(fbus, tbus), max(fbus, tbus))
                if pair not in branches:
                    branches[pair] = []
                branches[pair].append(x)
            except (ValueError, IndexError):
                continue

    return branches


def compute_mean_x(x_values: List[float]) -> float:
    """Compute mean of x values for parallel branches."""
    if not x_values:
        raise ValueError("Cannot compute mean of empty list")
    return sum(x_values) / len(x_values)


def compute_pct_change(x_case118: float, x_pglib: float) -> float:
    """Compute percentage change: abs(x_pglib - x_case118) / abs(x_case118)."""
    if x_case118 == 0:
        raise ValueError("Cannot compute percentage change with zero denominator")
    return abs(x_pglib - x_case118) / abs(x_case118)


def floats_equal(a: float, b: float, tol: float = FLOAT_TOLERANCE) -> bool:
    """Check if two floats are equal within tolerance."""
    return abs(a - b) < tol


def find_max_pct_change_pair(
    case57_branches: Dict[Tuple[int, int], List[float]],
    case118_branches: Dict[Tuple[int, int], List[float]],
    pglib_branches: Dict[Tuple[int, int], List[float]]
) -> Optional[Tuple[Tuple[int, int], float, float, float]]:
    """Find the pair with maximum percentage change.

    Returns (pair, x_case118, x_pglib, pct_change) or None if no valid pairs.
    Uses lexicographic ordering for tie-breaking.
    """
    common_pairs = (
        set(case57_branches.keys()) &
        set(case118_branches.keys()) &
        set(pglib_branches.keys())
    )

    if not common_pairs:
        return None

    max_pct = -1.0
    max_pair = None
    max_x_case118 = None
    max_x_pglib = None

    for pair in sorted(common_pairs):
        x_case118 = compute_mean_x(case118_branches[pair])
        x_pglib = compute_mean_x(pglib_branches[pair])

        if x_case118 == 0:
            continue

        pct_change = compute_pct_change(x_case118, x_pglib)

        if pct_change > max_pct + FLOAT_TOLERANCE:
            max_pct = pct_change
            max_pair = pair
            max_x_case118 = x_case118
            max_x_pglib = x_pglib
        elif floats_equal(pct_change, max_pct) and (max_pair is None or pair < max_pair):
            max_pct = pct_change
            max_pair = pair
            max_x_case118 = x_case118
            max_x_pglib = x_pglib

    if max_pair is None:
        return None

    return (max_pair, max_x_case118, max_x_pglib, max_pct)


class TestInputFilesExist:
    """Tests for input file existence (prerequisites)."""

    def test_case57_exists(self):
        """Verify case57.m input file exists."""
        assert os.path.exists(INPUT_CASE57), f"Input file not found: {INPUT_CASE57}"

    def test_case118_exists(self):
        """Verify case118.m input file exists."""
        assert os.path.exists(INPUT_CASE118), f"Input file not found: {INPUT_CASE118}"

    def test_pglib_exists(self):
        """Verify pglib_opf_case118_ieee.m input file exists."""
        assert os.path.exists(INPUT_PGLIB), f"Input file not found: {INPUT_PGLIB}"


class TestParserRobustness:
    """Tests for parser robustness and sanity checks."""

    def test_case57_branches_parsed(self):
        """Verify case57.m branches are parsed successfully with non-zero count."""
        branches = parse_matpower_branches(INPUT_CASE57)
        assert len(branches) > 0, (
            f"Parser returned 0 branches for {INPUT_CASE57}. "
            "Check that the mpc.branch block regex is matching correctly."
        )
        assert len(branches) >= 70, (
            f"Expected at least 70 branch pairs in case57, got {len(branches)}. "
            "The IEEE 57-bus case should have ~80 branches."
        )

    def test_case118_branches_parsed(self):
        """Verify case118.m branches are parsed successfully with non-zero count."""
        branches = parse_matpower_branches(INPUT_CASE118)
        assert len(branches) > 0, (
            f"Parser returned 0 branches for {INPUT_CASE118}. "
            "Check that the mpc.branch block regex is matching correctly."
        )
        assert len(branches) >= 150, (
            f"Expected at least 150 branch pairs in case118, got {len(branches)}. "
            "The IEEE 118-bus case should have ~186 branches."
        )

    def test_pglib_branches_parsed(self):
        """Verify pglib_opf_case118_ieee.m branches are parsed successfully."""
        branches = parse_matpower_branches(INPUT_PGLIB)
        assert len(branches) > 0, (
            f"Parser returned 0 branches for {INPUT_PGLIB}. "
            "Check that the mpc.branch block regex is matching correctly."
        )
        assert len(branches) >= 150, (
            f"Expected at least 150 branch pairs in pglib, got {len(branches)}. "
            "The pglib IEEE 118-bus case should have ~186 branches."
        )

    def test_common_pairs_exist(self):
        """Verify there are common pairs among all three files."""
        case57_branches = parse_matpower_branches(INPUT_CASE57)
        case118_branches = parse_matpower_branches(INPUT_CASE118)
        pglib_branches = parse_matpower_branches(INPUT_PGLIB)

        common_pairs = (
            set(case57_branches.keys()) &
            set(case118_branches.keys()) &
            set(pglib_branches.keys())
        )

        assert len(common_pairs) > 0, (
            "No common branch pairs found among all three input files. "
            f"case57 pairs: {len(case57_branches)}, "
            f"case118 pairs: {len(case118_branches)}, "
            f"pglib pairs: {len(pglib_branches)}. "
            "This suggests a parsing error or incompatible test cases."
        )

    def test_parallel_branches_detected_in_case57(self):
        """Verify parser detects parallel branches (multiple x values per pair)."""
        branches = parse_matpower_branches(INPUT_CASE57)

        assert (4, 18) in branches, "Expected pair (4, 18) in case57"
        assert len(branches[(4, 18)]) == 2, (
            f"Expected 2 parallel branches for (4, 18) in case57, "
            f"got {len(branches[(4, 18)])}"
        )

        assert (24, 25) in branches, "Expected pair (24, 25) in case57"
        assert len(branches[(24, 25)]) == 2, (
            f"Expected 2 parallel branches for (24, 25) in case57, "
            f"got {len(branches[(24, 25)])}"
        )


class TestOutputFileExists:
    """Tests for output file existence and basic structure."""

    def test_output_file_exists(self):
        """Verify output file was created at the specified path."""
        assert os.path.exists(OUTPUT_FILE), (
            f"Output file not found at {OUTPUT_FILE}. "
            "Ensure the task execution completed successfully."
        )

    def test_output_file_is_not_empty(self):
        """Verify output file is not empty."""
        assert os.path.exists(OUTPUT_FILE), "Output file not found"
        size = os.path.getsize(OUTPUT_FILE)
        assert size > 0, f"Output file is empty (size: {size} bytes)"


class TestOutputFormat:
    """Tests for output format validity."""

    def test_output_is_valid_json(self):
        """Verify output is valid JSON format."""
        assert os.path.exists(OUTPUT_FILE), "Output file not found"
        with open(OUTPUT_FILE) as f:
            content = f.read()
        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            pytest.fail(f"Output file is not valid JSON: {e}")
        assert data is not None

    def test_output_has_required_keys(self):
        """Verify output contains all required keys."""
        assert os.path.exists(OUTPUT_FILE), "Output file not found"
        with open(OUTPUT_FILE) as f:
            data = json.load(f)

        required_keys = ["bus_i", "bus_j", "x_case118", "x_pglib", "pct_change"]
        missing_keys = [key for key in required_keys if key not in data]
        assert not missing_keys, (
            f"Missing required keys in output: {missing_keys}. "
            f"Found keys: {list(data.keys())}"
        )

    def test_output_has_no_extra_keys(self):
        """Verify output contains only the specified keys."""
        assert os.path.exists(OUTPUT_FILE), "Output file not found"
        with open(OUTPUT_FILE) as f:
            data = json.load(f)

        expected_keys = {"bus_i", "bus_j", "x_case118", "x_pglib", "pct_change"}
        actual_keys = set(data.keys())
        extra_keys = actual_keys - expected_keys
        assert not extra_keys, (
            f"Unexpected keys in output: {extra_keys}. "
            f"Expected only: {expected_keys}"
        )


class TestOutputValueTypes:
    """Tests for output value types."""

    def test_bus_i_is_integer(self):
        """Verify bus_i is a JSON number (integer)."""
        assert os.path.exists(OUTPUT_FILE), "Output file not found"
        with open(OUTPUT_FILE) as f:
            data = json.load(f)

        assert isinstance(data["bus_i"], int), (
            f"bus_i should be an integer, got {type(data['bus_i']).__name__}: {data['bus_i']}"
        )

    def test_bus_j_is_integer(self):
        """Verify bus_j is a JSON number (integer)."""
        assert os.path.exists(OUTPUT_FILE), "Output file not found"
        with open(OUTPUT_FILE) as f:
            data = json.load(f)

        assert isinstance(data["bus_j"], int), (
            f"bus_j should be an integer, got {type(data['bus_j']).__name__}: {data['bus_j']}"
        )

    def test_x_case118_is_number(self):
        """Verify x_case118 is a JSON number."""
        assert os.path.exists(OUTPUT_FILE), "Output file not found"
        with open(OUTPUT_FILE) as f:
            data = json.load(f)

        assert isinstance(data["x_case118"], (int, float)), (
            f"x_case118 should be a number, got {type(data['x_case118']).__name__}: {data['x_case118']}"
        )

    def test_x_pglib_is_number(self):
        """Verify x_pglib is a JSON number."""
        assert os.path.exists(OUTPUT_FILE), "Output file not found"
        with open(OUTPUT_FILE) as f:
            data = json.load(f)

        assert isinstance(data["x_pglib"], (int, float)), (
            f"x_pglib should be a number, got {type(data['x_pglib']).__name__}: {data['x_pglib']}"
        )

    def test_pct_change_is_number(self):
        """Verify pct_change is a JSON number."""
        assert os.path.exists(OUTPUT_FILE), "Output file not found"
        with open(OUTPUT_FILE) as f:
            data = json.load(f)

        assert isinstance(data["pct_change"], (int, float)), (
            f"pct_change should be a number, got {type(data['pct_change']).__name__}: {data['pct_change']}"
        )

    def test_values_are_not_strings(self):
        """Verify no values are stored as strings."""
        assert os.path.exists(OUTPUT_FILE), "Output file not found"
        with open(OUTPUT_FILE) as f:
            data = json.load(f)

        string_values = [(k, v) for k, v in data.items() if isinstance(v, str)]
        assert not string_values, (
            f"Found string values that should be numbers: {string_values}"
        )


class TestOutputValueConstraints:
    """Tests for output value constraints and business logic."""

    def test_bus_i_less_than_bus_j(self):
        """Verify unordered pair convention: bus_i < bus_j."""
        assert os.path.exists(OUTPUT_FILE), "Output file not found"
        with open(OUTPUT_FILE) as f:
            data = json.load(f)

        assert data["bus_i"] < data["bus_j"], (
            f"bus_i ({data['bus_i']}) should be less than bus_j ({data['bus_j']}) "
            "for unordered pair convention"
        )

    def test_bus_numbers_are_positive(self):
        """Verify bus numbers are positive integers."""
        assert os.path.exists(OUTPUT_FILE), "Output file not found"
        with open(OUTPUT_FILE) as f:
            data = json.load(f)

        assert data["bus_i"] > 0, f"bus_i should be positive, got {data['bus_i']}"
        assert data["bus_j"] > 0, f"bus_j should be positive, got {data['bus_j']}"

    def test_pct_change_is_non_negative(self):
        """Verify pct_change is non-negative (absolute value)."""
        assert os.path.exists(OUTPUT_FILE), "Output file not found"
        with open(OUTPUT_FILE) as f:
            data = json.load(f)

        assert data["pct_change"] >= 0, (
            f"pct_change should be non-negative (absolute), got {data['pct_change']}"
        )

    def test_x_case118_is_nonzero(self):
        """Verify x_case118 is non-zero (division by zero excluded)."""
        assert os.path.exists(OUTPUT_FILE), "Output file not found"
        with open(OUTPUT_FILE) as f:
            data = json.load(f)

        assert data["x_case118"] != 0, (
            "x_case118 should not be zero (pairs with zero x_case118 are excluded)"
        )


class TestBusPairExistsInAllFiles:
    """Tests verifying the bus pair exists in all three input files."""

    def test_pair_exists_in_case57(self):
        """Verify the output bus pair exists in case57.m."""
        assert os.path.exists(OUTPUT_FILE), "Output file not found"
        assert os.path.exists(INPUT_CASE57), "Input case57.m not found"

        with open(OUTPUT_FILE) as f:
            data = json.load(f)

        branches = parse_matpower_branches(INPUT_CASE57)
        pair = (data["bus_i"], data["bus_j"])

        assert pair in branches, (
            f"Bus pair {pair} not found in case57.m. "
            f"Available pairs in case57 (first 10): {list(branches.keys())[:10]}... "
            "The pair must exist in the 57-bus case to be valid."
        )

    def test_pair_exists_in_case118(self):
        """Verify the output bus pair exists in case118.m."""
        assert os.path.exists(OUTPUT_FILE), "Output file not found"
        assert os.path.exists(INPUT_CASE118), "Input case118.m not found"

        with open(OUTPUT_FILE) as f:
            data = json.load(f)

        branches = parse_matpower_branches(INPUT_CASE118)
        pair = (data["bus_i"], data["bus_j"])

        assert pair in branches, (
            f"Bus pair {pair} not found in case118.m. "
            "The pair must exist in the 118-bus case."
        )

    def test_pair_exists_in_pglib(self):
        """Verify the output bus pair exists in pglib_opf_case118_ieee.m."""
        assert os.path.exists(OUTPUT_FILE), "Output file not found"
        assert os.path.exists(INPUT_PGLIB), "Input pglib_opf_case118_ieee.m not found"

        with open(OUTPUT_FILE) as f:
            data = json.load(f)

        branches = parse_matpower_branches(INPUT_PGLIB)
        pair = (data["bus_i"], data["bus_j"])

        assert pair in branches, (
            f"Bus pair {pair} not found in pglib_opf_case118_ieee.m. "
            "The pair must exist in the pglib case."
        )


class TestPctChangeCalculation:
    """Tests verifying the percentage change calculation."""

    def test_pct_change_formula_matches(self):
        """Verify pct_change matches the formula: abs(x_pglib - x_case118) / abs(x_case118)."""
        assert os.path.exists(OUTPUT_FILE), "Output file not found"

        with open(OUTPUT_FILE) as f:
            data = json.load(f)

        expected_pct = abs(data["x_pglib"] - data["x_case118"]) / abs(data["x_case118"])

        assert floats_equal(data["pct_change"], expected_pct), (
            f"pct_change ({data['pct_change']:.15g}) does not match expected "
            f"calculation ({expected_pct:.15g}) based on formula: "
            f"abs({data['x_pglib']} - {data['x_case118']}) / abs({data['x_case118']})"
        )

    def test_x_values_match_input_files(self):
        """Verify x_case118 and x_pglib match mean values from input files."""
        assert os.path.exists(OUTPUT_FILE), "Output file not found"
        assert os.path.exists(INPUT_CASE118), "Input case118.m not found"
        assert os.path.exists(INPUT_PGLIB), "Input pglib_opf_case118_ieee.m not found"

        with open(OUTPUT_FILE) as f:
            data = json.load(f)

        pair = (data["bus_i"], data["bus_j"])

        case118_branches = parse_matpower_branches(INPUT_CASE118)
        assert pair in case118_branches, f"Pair {pair} not in case118"
        expected_x_case118 = compute_mean_x(case118_branches[pair])
        assert floats_equal(data["x_case118"], expected_x_case118), (
            f"x_case118 ({data['x_case118']:.15g}) does not match mean from file "
            f"({expected_x_case118:.15g}) for pair {pair}. "
            f"Raw x values in case118: {case118_branches[pair]}"
        )

        pglib_branches = parse_matpower_branches(INPUT_PGLIB)
        assert pair in pglib_branches, f"Pair {pair} not in pglib"
        expected_x_pglib = compute_mean_x(pglib_branches[pair])
        assert floats_equal(data["x_pglib"], expected_x_pglib), (
            f"x_pglib ({data['x_pglib']:.15g}) does not match mean from file "
            f"({expected_x_pglib:.15g}) for pair {pair}. "
            f"Raw x values in pglib: {pglib_branches[pair]}"
        )


class TestParallelBranchAveraging:
    """Tests verifying parallel branch x values are averaged correctly."""

    def test_parallel_branches_averaged_in_case118(self):
        """Verify parallel branches are averaged when computing x_case118."""
        assert os.path.exists(OUTPUT_FILE), "Output file not found"
        assert os.path.exists(INPUT_CASE118), "Input case118.m not found"

        with open(OUTPUT_FILE) as f:
            data = json.load(f)

        case118_branches = parse_matpower_branches(INPUT_CASE118)
        pair = (data["bus_i"], data["bus_j"])

        if pair in case118_branches and len(case118_branches[pair]) > 1:
            x_values = case118_branches[pair]
            expected_mean = sum(x_values) / len(x_values)
            assert floats_equal(data["x_case118"], expected_mean), (
                f"For parallel branch pair {pair} in case118, x_case118 should be "
                f"the mean of {x_values} = {expected_mean:.15g}, "
                f"but got {data['x_case118']:.15g}"
            )

    def test_parallel_branches_averaged_in_pglib(self):
        """Verify parallel branches are averaged when computing x_pglib."""
        assert os.path.exists(OUTPUT_FILE), "Output file not found"
        assert os.path.exists(INPUT_PGLIB), "Input pglib_opf_case118_ieee.m not found"

        with open(OUTPUT_FILE) as f:
            data = json.load(f)

        pglib_branches = parse_matpower_branches(INPUT_PGLIB)
        pair = (data["bus_i"], data["bus_j"])

        if pair in pglib_branches and len(pglib_branches[pair]) > 1:
            x_values = pglib_branches[pair]
            expected_mean = sum(x_values) / len(x_values)
            assert floats_equal(data["x_pglib"], expected_mean), (
                f"For parallel branch pair {pair} in pglib, x_pglib should be "
                f"the mean of {x_values} = {expected_mean:.15g}, "
                f"but got {data['x_pglib']:.15g}"
            )

    def test_known_parallel_branch_pair_42_49(self):
        """Verify the known parallel branch (42, 49) is handled correctly if it's common."""
        case118_branches = parse_matpower_branches(INPUT_CASE118)

        pair = (42, 49)

        if pair in case118_branches:
            assert len(case118_branches[pair]) == 2, (
                f"Expected 2 parallel branches for (42, 49) in case118, "
                f"got {len(case118_branches[pair])}"
            )
            x_values = case118_branches[pair]
            assert all(abs(x - 0.323) < 0.001 for x in x_values), (
                f"Expected x values ~0.323 for (42, 49) in case118, got {x_values}"
            )


class TestMaximumPctChange:
    """Tests verifying the output has the maximum percentage change."""

    def test_pct_change_is_maximum(self):
        """Verify the reported pair has the maximum pct_change among valid pairs."""
        assert os.path.exists(OUTPUT_FILE), "Output file not found"

        with open(OUTPUT_FILE) as f:
            data = json.load(f)

        case57_branches = parse_matpower_branches(INPUT_CASE57)
        case118_branches = parse_matpower_branches(INPUT_CASE118)
        pglib_branches = parse_matpower_branches(INPUT_PGLIB)

        result = find_max_pct_change_pair(case57_branches, case118_branches, pglib_branches)
        assert result is not None, "Could not find any valid pairs with non-zero x_case118"

        expected_pair, expected_x_case118, expected_x_pglib, expected_pct = result
        reported_pair = (data["bus_i"], data["bus_j"])

        assert reported_pair == expected_pair, (
            f"Reported pair {reported_pair} with pct_change {data['pct_change']:.15g} "
            f"is not the maximum. Expected pair {expected_pair} with pct_change {expected_pct:.15g}. "
            f"Expected x_case118={expected_x_case118:.15g}, x_pglib={expected_x_pglib:.15g}"
        )

    def test_no_larger_pct_change_exists(self):
        """Verify no other valid pair has a larger pct_change (with tolerance)."""
        assert os.path.exists(OUTPUT_FILE), "Output file not found"

        with open(OUTPUT_FILE) as f:
            data = json.load(f)

        reported_pct = data["pct_change"]
        reported_pair = (data["bus_i"], data["bus_j"])

        case57_branches = parse_matpower_branches(INPUT_CASE57)
        case118_branches = parse_matpower_branches(INPUT_CASE118)
        pglib_branches = parse_matpower_branches(INPUT_PGLIB)

        common_pairs = (
            set(case57_branches.keys()) &
            set(case118_branches.keys()) &
            set(pglib_branches.keys())
        )

        violations = []
        for pair in common_pairs:
            x_case118 = compute_mean_x(case118_branches[pair])
            x_pglib = compute_mean_x(pglib_branches[pair])

            if x_case118 == 0:
                continue

            pct_change = compute_pct_change(x_case118, x_pglib)

            if pct_change > reported_pct + FLOAT_TOLERANCE:
                violations.append((pair, pct_change, x_case118, x_pglib))

            if floats_equal(pct_change, reported_pct) and pair < reported_pair:
                violations.append((pair, pct_change, x_case118, x_pglib, "tie-break"))

        assert not violations, (
            f"Found pairs with larger pct_change than reported {reported_pair} "
            f"(pct={reported_pct:.15g}):\n" +
            "\n".join(
                f"  {v[0]}: pct={v[1]:.15g}, x_case118={v[2]:.15g}, x_pglib={v[3]:.15g}"
                + (f" ({v[4]})" if len(v) > 4 else "")
                for v in violations[:5]
            )
        )

    def test_tiebreaker_lexicographic(self):
        """Verify tie-breaking uses lexicographic ordering (smallest pair wins)."""
        assert os.path.exists(OUTPUT_FILE), "Output file not found"

        with open(OUTPUT_FILE) as f:
            data = json.load(f)

        reported_pct = data["pct_change"]
        reported_pair = (data["bus_i"], data["bus_j"])

        case57_branches = parse_matpower_branches(INPUT_CASE57)
        case118_branches = parse_matpower_branches(INPUT_CASE118)
        pglib_branches = parse_matpower_branches(INPUT_PGLIB)

        common_pairs = (
            set(case57_branches.keys()) &
            set(case118_branches.keys()) &
            set(pglib_branches.keys())
        )

        tied_pairs = []
        for pair in common_pairs:
            x_case118 = compute_mean_x(case118_branches[pair])
            x_pglib = compute_mean_x(pglib_branches[pair])

            if x_case118 == 0:
                continue

            pct_change = compute_pct_change(x_case118, x_pglib)

            if floats_equal(pct_change, reported_pct):
                tied_pairs.append(pair)

        if len(tied_pairs) > 1:
            smallest_pair = min(tied_pairs)
            assert reported_pair == smallest_pair, (
                f"Multiple pairs tied with pct_change ~{reported_pct:.15g}: {sorted(tied_pairs)}. "
                f"Reported pair {reported_pair} should be the lexicographically smallest: {smallest_pair}"
            )


class TestGoldenValues:
    """Golden value tests with independently verified expected results."""

    def test_output_consistency_with_independent_calculation(self):
        """Verify output matches an independently calculated result."""
        assert os.path.exists(OUTPUT_FILE), "Output file not found"

        with open(OUTPUT_FILE) as f:
            data = json.load(f)

        case57_branches = parse_matpower_branches(INPUT_CASE57)
        case118_branches = parse_matpower_branches(INPUT_CASE118)
        pglib_branches = parse_matpower_branches(INPUT_PGLIB)

        result = find_max_pct_change_pair(case57_branches, case118_branches, pglib_branches)
        assert result is not None, "Independent calculation found no valid pairs"

        expected_pair, expected_x_case118, expected_x_pglib, expected_pct = result

        assert (data["bus_i"], data["bus_j"]) == expected_pair, (
            f"Bus pair mismatch: output={data['bus_i'], data['bus_j']}, expected={expected_pair}"
        )
        assert floats_equal(data["x_case118"], expected_x_case118), (
            f"x_case118 mismatch: output={data['x_case118']:.15g}, expected={expected_x_case118:.15g}"
        )
        assert floats_equal(data["x_pglib"], expected_x_pglib), (
            f"x_pglib mismatch: output={data['x_pglib']:.15g}, expected={expected_x_pglib:.15g}"
        )
        assert floats_equal(data["pct_change"], expected_pct), (
            f"pct_change mismatch: output={data['pct_change']:.15g}, expected={expected_pct:.15g}"
        )

    def test_known_branch_x_values(self):
        """Verify known branch x values from input files are parsed correctly."""
        case118_branches = parse_matpower_branches(INPUT_CASE118)

        assert floats_equal(case118_branches[(1, 2)][0], 0.0999, tol=1e-6), (
            f"Expected x=0.0999 for (1,2) in case118, got {case118_branches[(1, 2)]}"
        )
        assert floats_equal(case118_branches[(1, 3)][0], 0.0424, tol=1e-6), (
            f"Expected x=0.0424 for (1,3) in case118, got {case118_branches[(1, 3)]}"
        )

        pglib_branches = parse_matpower_branches(INPUT_PGLIB)

        assert floats_equal(pglib_branches[(1, 2)][0], 0.0999, tol=1e-6), (
            f"Expected x=0.0999 for (1,2) in pglib, got {pglib_branches[(1, 2)]}"
        )


class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""

    def test_output_handles_small_x_values(self):
        """Verify the solution handles small but non-zero x values correctly."""
        assert os.path.exists(OUTPUT_FILE), "Output file not found"

        with open(OUTPUT_FILE) as f:
            data = json.load(f)

        assert data["x_case118"] > 1e-10 or data["x_case118"] < -1e-10, (
            f"x_case118 ({data['x_case118']}) is suspiciously close to zero"
        )

    def test_pct_change_is_finite(self):
        """Verify pct_change is a finite number (not inf or nan)."""
        assert os.path.exists(OUTPUT_FILE), "Output file not found"

        with open(OUTPUT_FILE) as f:
            data = json.load(f)

        import math
        assert math.isfinite(data["pct_change"]), (
            f"pct_change should be finite, got {data['pct_change']}"
        )

    def test_all_values_finite(self):
        """Verify all numeric values are finite."""
        assert os.path.exists(OUTPUT_FILE), "Output file not found"

        with open(OUTPUT_FILE) as f:
            data = json.load(f)

        import math
        for key in ["x_case118", "x_pglib", "pct_change"]:
            assert math.isfinite(data[key]), (
                f"{key} should be finite, got {data[key]}"
            )