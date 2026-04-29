"""Auto-generated expectation tests for task verification.

These tests verify that the task execution produces correct outputs
for the topological signature analysis of MATPOWER case files.

Task: Parse three MATPOWER case files, compute degree histograms,
calculate L1 distances, and identify most similar pair.
"""

import json
import os
import re
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

import pytest


OUTPUT_FILE = "/root/degree_signature_result.json"
INPUT_DIR = "/root/harbor_workspaces/task_T430_run2/input"
EXPECTED_CASES = ["case57.m", "case118.m", "pglib_opf_case118_ieee.m"]


def parse_matpower_file(filepath: str) -> Tuple[List[int], List[Tuple[int, int, int]]]:
    """
    Parse a MATPOWER file to extract bus IDs and branch data.

    Returns:
        Tuple of (bus_ids, branches) where:
        - bus_ids: List of bus IDs from mpc.bus
        - branches: List of (from_bus, to_bus, status) tuples from mpc.branch
    """
    with open(filepath, 'r') as f:
        content = f.read()

    # Extract mpc.bus data
    bus_match = re.search(r'mpc\.bus\s*=\s*\[(.*?)\];', content, re.DOTALL)
    if not bus_match:
        raise ValueError(f"Could not find mpc.bus in {filepath}")

    bus_data = bus_match.group(1)
    bus_ids = []
    for line in bus_data.strip().split('\n'):
        line = line.strip()
        if not line or line.startswith('%'):
            continue
        # Remove trailing semicolon and comments
        line = re.sub(r';.*$', '', line).strip()
        line = re.sub(r'%.*$', '', line).strip()
        if not line:
            continue
        parts = line.split()
        if parts:
            try:
                bus_id = int(float(parts[0]))
                bus_ids.append(bus_id)
            except (ValueError, IndexError):
                continue

    # Extract mpc.branch data
    branch_match = re.search(r'mpc\.branch\s*=\s*\[(.*?)\];', content, re.DOTALL)
    if not branch_match:
        raise ValueError(f"Could not find mpc.branch in {filepath}")

    branch_data = branch_match.group(1)
    branches = []
    for line in branch_data.strip().split('\n'):
        line = line.strip()
        if not line or line.startswith('%'):
            continue
        # Remove trailing semicolon and comments
        line = re.sub(r';.*$', '', line).strip()
        line = re.sub(r'%.*$', '', line).strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) >= 11:
            try:
                fbus = int(float(parts[0]))
                tbus = int(float(parts[1]))
                status = int(float(parts[10]))
                branches.append((fbus, tbus, status))
            except (ValueError, IndexError):
                continue

    return bus_ids, branches


def compute_degree_histogram(bus_ids: List[int], branches: List[Tuple[int, int, int]]) -> Dict[int, int]:
    """
    Compute degree histogram from bus IDs and branches.

    Only counts in-service branches (status == 1).
    Degrees are keyed by actual bus ID, not row index.
    """
    # Initialize degree count for all buses
    degree_count = {bus_id: 0 for bus_id in bus_ids}

    # Count degrees from in-service branches only
    for fbus, tbus, status in branches:
        if status == 1:  # Only in-service branches
            if fbus in degree_count:
                degree_count[fbus] += 1
            if tbus in degree_count:
                degree_count[tbus] += 1

    # Build histogram: degree -> count of buses with that degree
    histogram = defaultdict(int)
    for bus_id, degree in degree_count.items():
        histogram[degree] += 1

    # Remove degrees with zero count (per specification)
    return {k: v for k, v in histogram.items() if v > 0}


def compute_l1_distance(hist1: Dict[int, int], hist2: Dict[int, int]) -> int:
    """
    Compute L1 distance between two histograms.

    L1 = sum over union of keys of |hist1[k] - hist2[k]|
    Missing keys are treated as 0.
    """
    all_keys = set(hist1.keys()) | set(hist2.keys())
    distance = 0
    for k in all_keys:
        v1 = hist1.get(k, 0)
        v2 = hist2.get(k, 0)
        distance += abs(v1 - v2)
    return distance


def get_ground_truth():
    """Compute ground truth values from MATPOWER input files."""
    ground_truth = {}

    for case in EXPECTED_CASES:
        filepath = os.path.join(INPUT_DIR, case)
        bus_ids, branches = parse_matpower_file(filepath)

        # Count in-service branches
        in_service_branches = sum(1 for _, _, status in branches if status == 1)

        # Compute degree histogram
        histogram = compute_degree_histogram(bus_ids, branches)

        ground_truth[case] = {
            "n_buses": len(bus_ids),
            "n_in_service_branches": in_service_branches,
            "degree_histogram": histogram,
            "bus_ids": bus_ids,
            "branches": branches
        }

    return ground_truth


# Compute ground truth once at module load
GROUND_TRUTH = get_ground_truth()


class TestOutputFileExists:
    """Tests for verifying output file existence and format."""

    def test_output_file_exists(self):
        """Verify output file was created at expected path."""
        assert os.path.exists(OUTPUT_FILE), (
            f"Output file not found at {OUTPUT_FILE}"
        )

    def test_output_file_not_empty(self):
        """Verify output file is not empty."""
        if os.path.exists(OUTPUT_FILE):
            assert os.path.getsize(OUTPUT_FILE) > 0, "Output file is empty"

    def test_output_is_valid_json(self):
        """Verify output is valid JSON format."""
        with open(OUTPUT_FILE) as f:
            data = json.load(f)
        assert data is not None, "JSON data should not be None"
        assert isinstance(data, dict), "JSON root should be a dictionary"


class TestSchemaCompliance:
    """Tests for verifying the output JSON schema matches specification."""

    @pytest.fixture
    def result_data(self):
        """Load the result JSON data."""
        with open(OUTPUT_FILE) as f:
            return json.load(f)

    def test_has_case_signatures_key(self, result_data):
        """Verify case_signatures key exists."""
        assert "case_signatures" in result_data, (
            "Missing required key: case_signatures"
        )

    def test_has_pairwise_distances_key(self, result_data):
        """Verify pairwise_L1_distances key exists."""
        assert "pairwise_L1_distances" in result_data, (
            "Missing required key: pairwise_L1_distances"
        )

    def test_has_most_similar_pair_key(self, result_data):
        """Verify most_similar_pair key exists."""
        assert "most_similar_pair" in result_data, (
            "Missing required key: most_similar_pair"
        )

    def test_case_signatures_has_all_cases(self, result_data):
        """Verify all three case files are in case_signatures."""
        signatures = result_data["case_signatures"]
        for case in EXPECTED_CASES:
            assert case in signatures, f"Missing case: {case} in case_signatures"

    def test_case_signature_structure(self, result_data):
        """Verify each case signature has required fields."""
        signatures = result_data["case_signatures"]
        required_fields = ["n_buses", "n_in_service_branches", "degree_histogram"]

        for case in EXPECTED_CASES:
            sig = signatures[case]
            for field in required_fields:
                assert field in sig, (
                    f"Missing field '{field}' in signature for {case}"
                )

    def test_pairwise_distances_has_all_pairs(self, result_data):
        """Verify all three pairwise distances are present."""
        distances = result_data["pairwise_L1_distances"]
        expected_pairs = [
            "case57.m__case118.m",
            "case57.m__pglib_opf_case118_ieee.m",
            "case118.m__pglib_opf_case118_ieee.m"
        ]
        for pair in expected_pairs:
            assert pair in distances, f"Missing pairwise distance: {pair}"

    def test_most_similar_pair_structure(self, result_data):
        """Verify most_similar_pair has required fields."""
        msp = result_data["most_similar_pair"]
        assert "files" in msp, "Missing 'files' in most_similar_pair"
        assert "distance" in msp, "Missing 'distance' in most_similar_pair"
        assert isinstance(msp["files"], list), "'files' should be a list"
        assert len(msp["files"]) == 2, "'files' should contain exactly 2 items"


class TestDataTypes:
    """Tests for verifying correct data types in the output."""

    @pytest.fixture
    def result_data(self):
        """Load the result JSON data."""
        with open(OUTPUT_FILE) as f:
            return json.load(f)

    def test_n_buses_is_integer(self, result_data):
        """Verify n_buses values are integers."""
        for case in EXPECTED_CASES:
            n_buses = result_data["case_signatures"][case]["n_buses"]
            assert isinstance(n_buses, int), (
                f"n_buses for {case} should be integer, got {type(n_buses).__name__}"
            )

    def test_n_in_service_branches_is_integer(self, result_data):
        """Verify n_in_service_branches values are integers."""
        for case in EXPECTED_CASES:
            n_branches = result_data["case_signatures"][case]["n_in_service_branches"]
            assert isinstance(n_branches, int), (
                f"n_in_service_branches for {case} should be integer, got {type(n_branches).__name__}"
            )

    def test_degree_histogram_is_dict(self, result_data):
        """Verify degree_histogram is a dictionary."""
        for case in EXPECTED_CASES:
            hist = result_data["case_signatures"][case]["degree_histogram"]
            assert isinstance(hist, dict), (
                f"degree_histogram for {case} should be dict, got {type(hist).__name__}"
            )

    def test_degree_histogram_keys_are_numeric_strings(self, result_data):
        """Verify degree_histogram keys represent integers."""
        for case in EXPECTED_CASES:
            hist = result_data["case_signatures"][case]["degree_histogram"]
            for key in hist.keys():
                try:
                    int(key)
                except ValueError:
                    pytest.fail(f"Histogram key '{key}' in {case} is not a valid integer")

    def test_degree_histogram_values_are_non_negative_integers(self, result_data):
        """Verify degree_histogram values are non-negative integers."""
        for case in EXPECTED_CASES:
            hist = result_data["case_signatures"][case]["degree_histogram"]
            for key, value in hist.items():
                assert isinstance(value, int), (
                    f"Histogram value for degree {key} in {case} should be int, got {type(value).__name__}"
                )
                assert value >= 0, (
                    f"Histogram value for degree {key} in {case} should be non-negative, got {value}"
                )

    def test_pairwise_distances_are_non_negative_integers(self, result_data):
        """Verify pairwise distances are non-negative integers."""
        distances = result_data["pairwise_L1_distances"]
        for pair, dist in distances.items():
            assert isinstance(dist, int), (
                f"Distance for {pair} should be integer, got {type(dist).__name__}"
            )
            assert dist >= 0, f"Distance for {pair} should be non-negative, got {dist}"

    def test_most_similar_distance_is_non_negative_integer(self, result_data):
        """Verify most_similar_pair distance is a non-negative integer."""
        dist = result_data["most_similar_pair"]["distance"]
        assert isinstance(dist, int), (
            f"most_similar_pair distance should be integer, got {type(dist).__name__}"
        )
        assert dist >= 0, f"most_similar_pair distance should be non-negative, got {dist}"


class TestExactBusAndBranchCounts:
    """Tests verifying exact bus and branch counts from parsed input files."""

    @pytest.fixture
    def result_data(self):
        """Load the result JSON data."""
        with open(OUTPUT_FILE) as f:
            return json.load(f)

    def test_case57_bus_count(self, result_data):
        """Verify case57.m bus count matches ground truth."""
        expected = GROUND_TRUTH["case57.m"]["n_buses"]
        actual = result_data["case_signatures"]["case57.m"]["n_buses"]
        assert actual == expected, (
            f"case57.m: expected {expected} buses, got {actual}"
        )

    def test_case118_bus_count(self, result_data):
        """Verify case118.m bus count matches ground truth."""
        expected = GROUND_TRUTH["case118.m"]["n_buses"]
        actual = result_data["case_signatures"]["case118.m"]["n_buses"]
        assert actual == expected, (
            f"case118.m: expected {expected} buses, got {actual}"
        )

    def test_pglib_case118_bus_count(self, result_data):
        """Verify pglib_opf_case118_ieee.m bus count matches ground truth."""
        expected = GROUND_TRUTH["pglib_opf_case118_ieee.m"]["n_buses"]
        actual = result_data["case_signatures"]["pglib_opf_case118_ieee.m"]["n_buses"]
        assert actual == expected, (
            f"pglib_opf_case118_ieee.m: expected {expected} buses, got {actual}"
        )

    def test_case57_branch_count(self, result_data):
        """Verify case57.m in-service branch count matches ground truth."""
        expected = GROUND_TRUTH["case57.m"]["n_in_service_branches"]
        actual = result_data["case_signatures"]["case57.m"]["n_in_service_branches"]
        assert actual == expected, (
            f"case57.m: expected {expected} in-service branches, got {actual}"
        )

    def test_case118_branch_count(self, result_data):
        """Verify case118.m in-service branch count matches ground truth."""
        expected = GROUND_TRUTH["case118.m"]["n_in_service_branches"]
        actual = result_data["case_signatures"]["case118.m"]["n_in_service_branches"]
        assert actual == expected, (
            f"case118.m: expected {expected} in-service branches, got {actual}"
        )

    def test_pglib_case118_branch_count(self, result_data):
        """Verify pglib_opf_case118_ieee.m in-service branch count matches ground truth."""
        expected = GROUND_TRUTH["pglib_opf_case118_ieee.m"]["n_in_service_branches"]
        actual = result_data["case_signatures"]["pglib_opf_case118_ieee.m"]["n_in_service_branches"]
        assert actual == expected, (
            f"pglib_opf_case118_ieee.m: expected {expected} in-service branches, got {actual}"
        )


class TestExactDegreeHistograms:
    """Tests verifying exact degree histogram contents against ground truth."""

    @pytest.fixture
    def result_data(self):
        """Load the result JSON data."""
        with open(OUTPUT_FILE) as f:
            return json.load(f)

    def test_case57_exact_histogram(self, result_data):
        """Verify case57.m degree histogram matches ground truth exactly."""
        expected = GROUND_TRUTH["case57.m"]["degree_histogram"]
        actual_raw = result_data["case_signatures"]["case57.m"]["degree_histogram"]
        actual = {int(k): v for k, v in actual_raw.items()}

        assert actual == expected, (
            f"case57.m histogram mismatch:\n"
            f"Expected: {dict(sorted(expected.items()))}\n"
            f"Actual: {dict(sorted(actual.items()))}"
        )

    def test_case118_exact_histogram(self, result_data):
        """Verify case118.m degree histogram matches ground truth exactly."""
        expected = GROUND_TRUTH["case118.m"]["degree_histogram"]
        actual_raw = result_data["case_signatures"]["case118.m"]["degree_histogram"]
        actual = {int(k): v for k, v in actual_raw.items()}

        assert actual == expected, (
            f"case118.m histogram mismatch:\n"
            f"Expected: {dict(sorted(expected.items()))}\n"
            f"Actual: {dict(sorted(actual.items()))}"
        )

    def test_pglib_case118_exact_histogram(self, result_data):
        """Verify pglib_opf_case118_ieee.m degree histogram matches ground truth exactly."""
        expected = GROUND_TRUTH["pglib_opf_case118_ieee.m"]["degree_histogram"]
        actual_raw = result_data["case_signatures"]["pglib_opf_case118_ieee.m"]["degree_histogram"]
        actual = {int(k): v for k, v in actual_raw.items()}

        assert actual == expected, (
            f"pglib_opf_case118_ieee.m histogram mismatch:\n"
            f"Expected: {dict(sorted(expected.items()))}\n"
            f"Actual: {dict(sorted(actual.items()))}"
        )


class TestDegreeHistogramConsistency:
    """Tests for verifying degree histogram mathematical consistency."""

    @pytest.fixture
    def result_data(self):
        """Load the result JSON data."""
        with open(OUTPUT_FILE) as f:
            return json.load(f)

    def test_histogram_sum_equals_bus_count(self, result_data):
        """Verify sum of histogram counts equals number of buses."""
        for case in EXPECTED_CASES:
            sig = result_data["case_signatures"][case]
            hist = sig["degree_histogram"]
            n_buses = sig["n_buses"]

            hist_sum = sum(hist.values())
            assert hist_sum == n_buses, (
                f"For {case}: sum of histogram ({hist_sum}) != n_buses ({n_buses})"
            )

    def test_weighted_degree_sum_equals_twice_branches(self, result_data):
        """Verify sum(degree * count) = 2 * n_branches (handshaking lemma)."""
        for case in EXPECTED_CASES:
            sig = result_data["case_signatures"][case]
            hist = sig["degree_histogram"]
            n_branches = sig["n_in_service_branches"]

            weighted_sum = sum(int(k) * v for k, v in hist.items())
            expected = 2 * n_branches
            assert weighted_sum == expected, (
                f"For {case}: weighted degree sum ({weighted_sum}) != "
                f"2 * n_branches ({expected})"
            )


class TestExactPairwiseDistances:
    """Tests verifying exact L1 distances computed from ground truth histograms."""

    @pytest.fixture
    def result_data(self):
        """Load the result JSON data."""
        with open(OUTPUT_FILE) as f:
            return json.load(f)

    def test_case57_case118_distance(self, result_data):
        """Verify L1 distance between case57.m and case118.m."""
        hist1 = GROUND_TRUTH["case57.m"]["degree_histogram"]
        hist2 = GROUND_TRUTH["case118.m"]["degree_histogram"]
        expected = compute_l1_distance(hist1, hist2)

        actual = result_data["pairwise_L1_distances"]["case57.m__case118.m"]
        assert actual == expected, (
            f"case57.m__case118.m distance: expected {expected}, got {actual}"
        )

    def test_case57_pglib_distance(self, result_data):
        """Verify L1 distance between case57.m and pglib_opf_case118_ieee.m."""
        hist1 = GROUND_TRUTH["case57.m"]["degree_histogram"]
        hist2 = GROUND_TRUTH["pglib_opf_case118_ieee.m"]["degree_histogram"]
        expected = compute_l1_distance(hist1, hist2)

        actual = result_data["pairwise_L1_distances"]["case57.m__pglib_opf_case118_ieee.m"]
        assert actual == expected, (
            f"case57.m__pglib_opf_case118_ieee.m distance: expected {expected}, got {actual}"
        )

    def test_case118_pglib_distance(self, result_data):
        """Verify L1 distance between case118.m and pglib_opf_case118_ieee.m."""
        hist1 = GROUND_TRUTH["case118.m"]["degree_histogram"]
        hist2 = GROUND_TRUTH["pglib_opf_case118_ieee.m"]["degree_histogram"]
        expected = compute_l1_distance(hist1, hist2)

        actual = result_data["pairwise_L1_distances"]["case118.m__pglib_opf_case118_ieee.m"]
        assert actual == expected, (
            f"case118.m__pglib_opf_case118_ieee.m distance: expected {expected}, got {actual}"
        )


class TestPairwiseDistanceConsistency:
    """Tests for verifying pairwise distance mathematical properties."""

    @pytest.fixture
    def result_data(self):
        """Load the result JSON data."""
        with open(OUTPUT_FILE) as f:
            return json.load(f)

    def test_symmetric_distance_property(self, result_data):
        """L1 distance is symmetric: d(A,B) = d(B,A)."""
        distances = result_data["pairwise_L1_distances"]

        # Verify exact key format (lexicographic ordering)
        assert "case118.m__pglib_opf_case118_ieee.m" in distances
        assert "case57.m__case118.m" in distances
        assert "case57.m__pglib_opf_case118_ieee.m" in distances

    def test_triangle_inequality(self, result_data):
        """Verify triangle inequality: d(A,C) <= d(A,B) + d(B,C)."""
        distances = result_data["pairwise_L1_distances"]

        d_57_118 = distances["case57.m__case118.m"]
        d_57_pglib = distances["case57.m__pglib_opf_case118_ieee.m"]
        d_118_pglib = distances["case118.m__pglib_opf_case118_ieee.m"]

        # All three triangle inequalities with informative messages
        assert d_57_pglib <= d_57_118 + d_118_pglib, (
            f"Triangle inequality violated: d(57,pglib)={d_57_pglib} > "
            f"d(57,118)={d_57_118} + d(118,pglib)={d_118_pglib} = {d_57_118 + d_118_pglib}"
        )
        assert d_57_118 <= d_57_pglib + d_118_pglib, (
            f"Triangle inequality violated: d(57,118)={d_57_118} > "
            f"d(57,pglib)={d_57_pglib} + d(118,pglib)={d_118_pglib} = {d_57_pglib + d_118_pglib}"
        )
        assert d_118_pglib <= d_57_118 + d_57_pglib, (
            f"Triangle inequality violated: d(118,pglib)={d_118_pglib} > "
            f"d(57,118)={d_57_118} + d(57,pglib)={d_57_pglib} = {d_57_118 + d_57_pglib}"
        )


class TestMostSimilarPair:
    """Tests for verifying the most similar pair determination."""

    @pytest.fixture
    def result_data(self):
        """Load the result JSON data."""
        with open(OUTPUT_FILE) as f:
            return json.load(f)

    def test_most_similar_files_are_valid(self, result_data):
        """Verify most similar pair files are from expected cases."""
        files = result_data["most_similar_pair"]["files"]
        for f in files:
            assert f in EXPECTED_CASES, f"Invalid file in most_similar_pair: {f}"

    def test_most_similar_distance_is_minimum(self, result_data):
        """Verify most_similar_pair distance is the minimum of all pairwise distances."""
        distances = result_data["pairwise_L1_distances"]
        msp = result_data["most_similar_pair"]

        min_distance = min(distances.values())
        assert msp["distance"] == min_distance, (
            f"most_similar_pair distance ({msp['distance']}) is not the minimum "
            f"pairwise distance ({min_distance}). All distances: {distances}"
        )

    def test_most_similar_pair_matches_distance(self, result_data):
        """Verify the pair matches the stated distance."""
        distances = result_data["pairwise_L1_distances"]
        msp = result_data["most_similar_pair"]

        # Get the sorted file pair to form the key
        pair_key = "__".join(sorted(msp["files"]))

        assert pair_key in distances, f"Pair key {pair_key} not found in distances"
        assert distances[pair_key] == msp["distance"], (
            f"Distance mismatch: most_similar_pair states distance={msp['distance']}, "
            f"but pairwise_L1_distances['{pair_key}']={distances[pair_key]}"
        )

    def test_case118_variants_are_most_similar(self, result_data):
        """Verify case118.m and pglib_opf_case118_ieee.m are identified as most similar."""
        msp = result_data["most_similar_pair"]
        files_set = set(msp["files"])
        expected_set = {"case118.m", "pglib_opf_case118_ieee.m"}

        assert files_set == expected_set, (
            f"Expected most similar pair to be {expected_set}, got {files_set}"
        )

    def test_most_similar_distance_matches_ground_truth(self, result_data):
        """Verify most similar pair distance matches computed ground truth."""
        # Compute expected distance from ground truth
        hist1 = GROUND_TRUTH["case118.m"]["degree_histogram"]
        hist2 = GROUND_TRUTH["pglib_opf_case118_ieee.m"]["degree_histogram"]
        expected = compute_l1_distance(hist1, hist2)

        msp = result_data["most_similar_pair"]
        assert msp["distance"] == expected, (
            f"Expected most similar pair distance {expected}, got {msp['distance']}"
        )


class TestCase118TopologyEquivalence:
    """Tests specifically for the case118 variants topology comparison."""

    @pytest.fixture
    def result_data(self):
        """Load the result JSON data."""
        with open(OUTPUT_FILE) as f:
            return json.load(f)

    def test_same_bus_count(self, result_data):
        """case118.m and pglib_opf_case118_ieee.m should have same bus count."""
        n1 = result_data["case_signatures"]["case118.m"]["n_buses"]
        n2 = result_data["case_signatures"]["pglib_opf_case118_ieee.m"]["n_buses"]
        assert n1 == n2, f"Bus counts differ: case118.m={n1} vs pglib={n2}"

    def test_same_branch_count(self, result_data):
        """case118.m and pglib_opf_case118_ieee.m should have same branch count."""
        n1 = result_data["case_signatures"]["case118.m"]["n_in_service_branches"]
        n2 = result_data["case_signatures"]["pglib_opf_case118_ieee.m"]["n_in_service_branches"]
        assert n1 == n2, f"Branch counts differ: case118.m={n1} vs pglib={n2}"

    def test_identical_histograms(self, result_data):
        """case118.m and pglib_opf_case118_ieee.m should have identical histograms."""
        h1 = result_data["case_signatures"]["case118.m"]["degree_histogram"]
        h2 = result_data["case_signatures"]["pglib_opf_case118_ieee.m"]["degree_histogram"]

        # Convert keys to int for comparison
        h1_normalized = {int(k): v for k, v in h1.items()}
        h2_normalized = {int(k): v for k, v in h2.items()}

        assert h1_normalized == h2_normalized, (
            f"Histograms should be identical:\n"
            f"case118.m: {dict(sorted(h1_normalized.items()))}\n"
            f"pglib: {dict(sorted(h2_normalized.items()))}"
        )


class TestBusIdMapping:
    """Tests verifying correct bus ID mapping (non-contiguous bus numbers)."""

    @pytest.fixture
    def result_data(self):
        """Load the result JSON data."""
        with open(OUTPUT_FILE) as f:
            return json.load(f)

    def test_degrees_computed_by_bus_id_not_index(self, result_data):
        """
        Verify degrees are computed using actual bus IDs, not row indices.

        This test computes degrees independently using bus IDs from the MATPOWER
        files and compares to the output. A bug that uses row indices instead
        of bus IDs would produce different results for non-contiguous bus numbering.
        """
        for case in EXPECTED_CASES:
            gt = GROUND_TRUTH[case]
            bus_ids = gt["bus_ids"]
            branches = gt["branches"]

            # Compute degree for each bus by ID
            degree_by_id = {bus_id: 0 for bus_id in bus_ids}
            for fbus, tbus, status in branches:
                if status == 1:
                    if fbus in degree_by_id:
                        degree_by_id[fbus] += 1
                    if tbus in degree_by_id:
                        degree_by_id[tbus] += 1

            # Build histogram from degrees
            expected_hist = defaultdict(int)
            for degree in degree_by_id.values():
                expected_hist[degree] += 1
            expected_hist = {k: v for k, v in expected_hist.items() if v > 0}

            # Compare to output
            actual_raw = result_data["case_signatures"][case]["degree_histogram"]
            actual_hist = {int(k): v for k, v in actual_raw.items()}

            assert actual_hist == expected_hist, (
                f"{case}: Degree histogram mismatch - possible bug in bus ID mapping.\n"
                f"Expected (computed by bus ID): {dict(sorted(expected_hist.items()))}\n"
                f"Actual: {dict(sorted(actual_hist.items()))}"
            )

    def test_all_buses_accounted_for(self, result_data):
        """Verify histogram accounts for all buses in each case."""
        for case in EXPECTED_CASES:
            expected_bus_count = GROUND_TRUTH[case]["n_buses"]
            hist = result_data["case_signatures"][case]["degree_histogram"]
            actual_bus_count = sum(hist.values())

            assert actual_bus_count == expected_bus_count, (
                f"{case}: Histogram sum ({actual_bus_count}) != "
                f"expected bus count ({expected_bus_count})"
            )


class TestBranchStatusFiltering:
    """Tests verifying correct filtering of in-service vs out-of-service branches."""

    @pytest.fixture
    def result_data(self):
        """Load the result JSON data."""
        with open(OUTPUT_FILE) as f:
            return json.load(f)

    def test_in_service_branch_count_from_status(self, result_data):
        """Verify in-service branch counts are computed from status column."""
        for case in EXPECTED_CASES:
            gt = GROUND_TRUTH[case]
            branches = gt["branches"]

            # Count branches with status == 1
            expected_in_service = sum(1 for _, _, status in branches if status == 1)
            actual = result_data["case_signatures"][case]["n_in_service_branches"]

            assert actual == expected_in_service, (
                f"{case}: in-service branch count mismatch. "
                f"Expected {expected_in_service} (from status==1), got {actual}"
            )


class TestDeterminism:
    """Tests for verifying the output is deterministic."""

    @pytest.fixture
    def result_data(self):
        """Load the result JSON data."""
        with open(OUTPUT_FILE) as f:
            return json.load(f)

    def test_no_placeholder_values(self, result_data):
        """Verify there are no placeholder values in the output."""
        json_str = json.dumps(result_data)

        placeholder_patterns = ["TODO", "PLACEHOLDER", "N/A", "TBD"]
        for pattern in placeholder_patterns:
            assert pattern not in json_str, (
                f"Found placeholder pattern '{pattern}' in output"
            )

    def test_histogram_keys_are_valid_integers(self, result_data):
        """Verify histogram keys can be deterministically converted to integers."""
        for case in EXPECTED_CASES:
            hist = result_data["case_signatures"][case]["degree_histogram"]
            keys = [int(k) for k in hist.keys()]
            assert all(isinstance(k, int) for k in keys), (
                f"All histogram keys for {case} should be convertible to integers"
            )

    def test_files_array_sorted_lexicographically(self, result_data):
        """Verify files array in most_similar_pair is sorted lexicographically."""
        files = result_data["most_similar_pair"]["files"]
        assert files == sorted(files), (
            f"Files array should be sorted lexicographically: {files}"
        )


class TestGroundTruthConsistency:
    """Tests verifying our ground truth computation is internally consistent."""

    def test_ground_truth_handshaking_lemma(self):
        """Verify ground truth satisfies handshaking lemma."""
        for case in EXPECTED_CASES:
            gt = GROUND_TRUTH[case]
            hist = gt["degree_histogram"]
            n_branches = gt["n_in_service_branches"]

            weighted_sum = sum(degree * count for degree, count in hist.items())
            expected = 2 * n_branches

            assert weighted_sum == expected, (
                f"Ground truth for {case} fails handshaking lemma: "
                f"sum(degree*count)={weighted_sum} != 2*branches={expected}"
            )

    def test_ground_truth_histogram_sum(self):
        """Verify ground truth histogram sums equal bus counts."""
        for case in EXPECTED_CASES:
            gt = GROUND_TRUTH[case]
            hist = gt["degree_histogram"]
            n_buses = gt["n_buses"]

            hist_sum = sum(hist.values())
            assert hist_sum == n_buses, (
                f"Ground truth for {case}: histogram sum {hist_sum} != n_buses {n_buses}"
            )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
