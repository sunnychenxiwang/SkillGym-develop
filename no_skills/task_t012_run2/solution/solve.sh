#!/bin/bash
set -e

# Auto-generated solution based on execution trajectory
# This script recreates the outputs produced during synthesis

# Create /root/expectation_tests.py
mkdir -p $(dirname /root/expectation_tests.py)
cat << 'HEREDOC_EOF' > /root/expectation_tests.py
"""Auto-generated expectation tests for task verification.

These tests verify that the task execution produces correct outputs
based on the instruction requirements for identifying the most critical
transmission corridor across three MATPOWER case files.
"""

import json
import os
import re
from pathlib import Path

import pytest


# Constants
OUTPUT_PATH = "/root/shared_critical_corridor.json"
EXPECTED_CASE_NAMES = ["case57.m", "case118.m", "pglib_opf_case118_ieee.m"]


class TestOutputFileExists:
    """Tests for verifying the output file was created."""

    def test_output_file_exists(self):
        """Verify the output JSON file was created at the expected path."""
        assert os.path.exists(OUTPUT_PATH), (
            f"Output file not found at {OUTPUT_PATH}. "
            "The task requires writing the JSON result to this exact path."
        )

    def test_output_file_is_not_empty(self):
        """Verify the output file is not empty."""
        assert os.path.exists(OUTPUT_PATH), f"Output file not found at {OUTPUT_PATH}"
        assert os.path.getsize(OUTPUT_PATH) > 0, "Output file exists but is empty"


class TestOutputFormat:
    """Tests for verifying the output format is valid JSON."""

    def test_output_is_valid_json(self):
        """Verify the output file contains valid JSON."""
        assert os.path.exists(OUTPUT_PATH), f"Output file not found at {OUTPUT_PATH}"
        with open(OUTPUT_PATH, 'r') as f:
            content = f.read()
        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            pytest.fail(f"Output file is not valid JSON: {e}")
        assert data is not None, "JSON parsed but result was None"

    def test_output_is_json_object(self):
        """Verify the output JSON is an object (dict), not array or primitive."""
        assert os.path.exists(OUTPUT_PATH), f"Output file not found at {OUTPUT_PATH}"
        with open(OUTPUT_PATH, 'r') as f:
            data = json.load(f)
        assert isinstance(data, dict), (
            f"Output JSON should be an object (dict), got {type(data).__name__}"
        )


class TestOutputSchema:
    """Tests for verifying the output JSON schema matches requirements."""

    @pytest.fixture
    def output_data(self):
        """Load and return the output JSON data."""
        if not os.path.exists(OUTPUT_PATH):
            pytest.skip(f"Output file not found at {OUTPUT_PATH}")
        with open(OUTPUT_PATH, 'r') as f:
            return json.load(f)

    def test_has_winner_edge_field(self, output_data):
        """Verify the output has a 'winner_edge' field."""
        assert "winner_edge" in output_data, (
            "Output JSON missing required 'winner_edge' field"
        )

    def test_has_cases_field(self, output_data):
        """Verify the output has a 'cases' field."""
        assert "cases" in output_data, (
            "Output JSON missing required 'cases' field"
        )

    def test_has_intersection_size_field(self, output_data):
        """Verify the output has an 'intersection_size' field."""
        assert "intersection_size" in output_data, (
            "Output JSON missing required 'intersection_size' field"
        )

    def test_no_extra_top_level_fields(self, output_data):
        """Verify only expected top-level fields are present."""
        expected_fields = {"winner_edge", "cases", "intersection_size"}
        actual_fields = set(output_data.keys())
        extra_fields = actual_fields - expected_fields
        assert not extra_fields, (
            f"Unexpected top-level fields in output: {extra_fields}"
        )


class TestWinnerEdgeField:
    """Tests for the winner_edge field format and validity."""

    @pytest.fixture
    def output_data(self):
        """Load and return the output JSON data."""
        if not os.path.exists(OUTPUT_PATH):
            pytest.skip(f"Output file not found at {OUTPUT_PATH}")
        with open(OUTPUT_PATH, 'r') as f:
            return json.load(f)

    def test_winner_edge_is_string(self, output_data):
        """Verify winner_edge is a string."""
        winner_edge = output_data.get("winner_edge")
        assert isinstance(winner_edge, str), (
            f"winner_edge should be a string, got {type(winner_edge).__name__}"
        )

    def test_winner_edge_format(self, output_data):
        """Verify winner_edge follows 'X-Y' format with integers."""
        winner_edge = output_data.get("winner_edge")
        assert winner_edge is not None, "winner_edge is None"

        # Check format: "X-Y" where X and Y are integers
        pattern = r"^\d+-\d+$"
        assert re.match(pattern, winner_edge), (
            f"winner_edge '{winner_edge}' does not match expected format 'X-Y' "
            "where X and Y are bus numbers"
        )

    def test_winner_edge_is_canonical(self, output_data):
        """Verify winner_edge is in canonical form (minBus-maxBus)."""
        winner_edge = output_data.get("winner_edge")
        assert winner_edge is not None, "winner_edge is None"

        parts = winner_edge.split("-")
        assert len(parts) == 2, f"winner_edge should have format 'X-Y', got '{winner_edge}'"

        try:
            bus1 = int(parts[0])
            bus2 = int(parts[1])
        except ValueError:
            pytest.fail(f"Bus numbers in winner_edge must be integers: '{winner_edge}'")

        assert bus1 < bus2, (
            f"winner_edge should be canonical (minBus-maxBus), but {bus1} >= {bus2} "
            f"in '{winner_edge}'"
        )

    def test_winner_edge_buses_are_positive(self, output_data):
        """Verify bus numbers in winner_edge are positive integers."""
        winner_edge = output_data.get("winner_edge")
        assert winner_edge is not None, "winner_edge is None"

        parts = winner_edge.split("-")
        bus1 = int(parts[0])
        bus2 = int(parts[1])

        assert bus1 > 0, f"First bus number must be positive, got {bus1}"
        assert bus2 > 0, f"Second bus number must be positive, got {bus2}"


class TestCasesField:
    """Tests for the cases field structure and content."""

    @pytest.fixture
    def output_data(self):
        """Load and return the output JSON data."""
        if not os.path.exists(OUTPUT_PATH):
            pytest.skip(f"Output file not found at {OUTPUT_PATH}")
        with open(OUTPUT_PATH, 'r') as f:
            return json.load(f)

    def test_cases_is_object(self, output_data):
        """Verify cases field is an object (dict)."""
        cases = output_data.get("cases")
        assert isinstance(cases, dict), (
            f"cases should be an object (dict), got {type(cases).__name__}"
        )

    def test_cases_has_all_case_files(self, output_data):
        """Verify all three case files are present in cases."""
        cases = output_data.get("cases", {})
        for case_name in EXPECTED_CASE_NAMES:
            assert case_name in cases, (
                f"cases is missing entry for '{case_name}'"
            )

    def test_cases_has_exactly_three_entries(self, output_data):
        """Verify cases has exactly three entries (one per case file)."""
        cases = output_data.get("cases", {})
        assert len(cases) == 3, (
            f"cases should have exactly 3 entries, got {len(cases)}"
        )

    @pytest.mark.parametrize("case_name", EXPECTED_CASE_NAMES)
    def test_case_entry_has_centrality(self, output_data, case_name):
        """Verify each case entry has a 'centrality' field."""
        cases = output_data.get("cases", {})
        if case_name not in cases:
            pytest.skip(f"Case '{case_name}' not in output")

        case_data = cases[case_name]
        assert "centrality" in case_data, (
            f"Case '{case_name}' missing 'centrality' field"
        )

    @pytest.mark.parametrize("case_name", EXPECTED_CASE_NAMES)
    def test_case_entry_has_rank(self, output_data, case_name):
        """Verify each case entry has a 'rank' field."""
        cases = output_data.get("cases", {})
        if case_name not in cases:
            pytest.skip(f"Case '{case_name}' not in output")

        case_data = cases[case_name]
        assert "rank" in case_data, (
            f"Case '{case_name}' missing 'rank' field"
        )

    @pytest.mark.parametrize("case_name", EXPECTED_CASE_NAMES)
    def test_centrality_is_number(self, output_data, case_name):
        """Verify centrality is a number (int or float)."""
        cases = output_data.get("cases", {})
        if case_name not in cases:
            pytest.skip(f"Case '{case_name}' not in output")

        centrality = cases[case_name].get("centrality")
        assert isinstance(centrality, (int, float)), (
            f"centrality for '{case_name}' should be a number, "
            f"got {type(centrality).__name__}"
        )

    @pytest.mark.parametrize("case_name", EXPECTED_CASE_NAMES)
    def test_centrality_is_normalized(self, output_data, case_name):
        """Verify centrality is between 0 and 1 (normalized)."""
        cases = output_data.get("cases", {})
        if case_name not in cases:
            pytest.skip(f"Case '{case_name}' not in output")

        centrality = cases[case_name].get("centrality")
        if centrality is None:
            pytest.skip(f"Centrality not found for '{case_name}'")

        assert 0 <= centrality <= 1, (
            f"centrality for '{case_name}' should be normalized (0-1), got {centrality}"
        )

    @pytest.mark.parametrize("case_name", EXPECTED_CASE_NAMES)
    def test_rank_is_integer(self, output_data, case_name):
        """Verify rank is an integer."""
        cases = output_data.get("cases", {})
        if case_name not in cases:
            pytest.skip(f"Case '{case_name}' not in output")

        rank = cases[case_name].get("rank")
        assert isinstance(rank, int), (
            f"rank for '{case_name}' should be an integer, got {type(rank).__name__}"
        )

    @pytest.mark.parametrize("case_name", EXPECTED_CASE_NAMES)
    def test_rank_is_in_valid_range(self, output_data, case_name):
        """Verify rank is between 1 and 10 (top-10 list)."""
        cases = output_data.get("cases", {})
        if case_name not in cases:
            pytest.skip(f"Case '{case_name}' not in output")

        rank = cases[case_name].get("rank")
        if rank is None:
            pytest.skip(f"Rank not found for '{case_name}'")

        assert 1 <= rank <= 10, (
            f"rank for '{case_name}' should be between 1 and 10, got {rank}"
        )


class TestIntersectionSizeField:
    """Tests for the intersection_size field."""

    @pytest.fixture
    def output_data(self):
        """Load and return the output JSON data."""
        if not os.path.exists(OUTPUT_PATH):
            pytest.skip(f"Output file not found at {OUTPUT_PATH}")
        with open(OUTPUT_PATH, 'r') as f:
            return json.load(f)

    def test_intersection_size_is_integer(self, output_data):
        """Verify intersection_size is an integer."""
        intersection_size = output_data.get("intersection_size")
        assert isinstance(intersection_size, int), (
            f"intersection_size should be an integer, "
            f"got {type(intersection_size).__name__}"
        )

    def test_intersection_size_is_positive(self, output_data):
        """Verify intersection_size is at least 1 (task requires non-empty intersection)."""
        intersection_size = output_data.get("intersection_size")
        assert intersection_size >= 1, (
            f"intersection_size must be >= 1 (non-empty intersection required), "
            f"got {intersection_size}"
        )

    def test_intersection_size_is_at_most_ten(self, output_data):
        """Verify intersection_size is at most 10 (max possible for top-10 intersection)."""
        intersection_size = output_data.get("intersection_size")
        assert intersection_size <= 10, (
            f"intersection_size cannot exceed 10 (top-10 intersection), "
            f"got {intersection_size}"
        )


class TestDataConsistency:
    """Tests for internal data consistency."""

    @pytest.fixture
    def output_data(self):
        """Load and return the output JSON data."""
        if not os.path.exists(OUTPUT_PATH):
            pytest.skip(f"Output file not found at {OUTPUT_PATH}")
        with open(OUTPUT_PATH, 'r') as f:
            return json.load(f)

    def test_winner_edge_appears_in_all_cases(self, output_data):
        """Verify the winner edge is present in the top-10 of all cases (has rank)."""
        winner_edge = output_data.get("winner_edge")
        cases = output_data.get("cases", {})

        if not winner_edge or not cases:
            pytest.skip("Missing winner_edge or cases data")

        for case_name in EXPECTED_CASE_NAMES:
            if case_name not in cases:
                continue
            case_data = cases[case_name]
            rank = case_data.get("rank")
            assert rank is not None and 1 <= rank <= 10, (
                f"Winner edge '{winner_edge}' should have rank 1-10 in '{case_name}', "
                f"got rank={rank}"
            )

    def test_centrality_values_are_distinct_or_reasonable(self, output_data):
        """Verify centrality values are reasonable (not all identical unless expected)."""
        cases = output_data.get("cases", {})
        centralities = [
            cases[name].get("centrality")
            for name in EXPECTED_CASE_NAMES
            if name in cases and cases[name].get("centrality") is not None
        ]

        if len(centralities) < 2:
            pytest.skip("Not enough centrality values to compare")

        # At least check they are all valid numbers
        for c in centralities:
            assert isinstance(c, (int, float)) and 0 <= c <= 1, (
                f"Invalid centrality value: {c}"
            )

    def test_ranks_sum_is_reasonable(self, output_data):
        """Verify the sum of ranks makes sense (winner has best average rank)."""
        cases = output_data.get("cases", {})
        ranks = [
            cases[name].get("rank")
            for name in EXPECTED_CASE_NAMES
            if name in cases and cases[name].get("rank") is not None
        ]

        if len(ranks) != 3:
            pytest.skip("Not all ranks available")

        # Average rank should be between 1 and 10
        avg_rank = sum(ranks) / len(ranks)
        assert 1 <= avg_rank <= 10, (
            f"Average rank should be between 1 and 10, got {avg_rank}"
        )


class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""

    @pytest.fixture
    def output_data(self):
        """Load and return the output JSON data."""
        if not os.path.exists(OUTPUT_PATH):
            pytest.skip(f"Output file not found at {OUTPUT_PATH}")
        with open(OUTPUT_PATH, 'r') as f:
            return json.load(f)

    def test_centrality_not_zero_for_critical_edge(self, output_data):
        """Verify the winner edge has non-zero centrality in all cases."""
        cases = output_data.get("cases", {})

        for case_name in EXPECTED_CASE_NAMES:
            if case_name not in cases:
                continue
            centrality = cases[case_name].get("centrality")
            if centrality is not None:
                assert centrality > 0, (
                    f"Winner edge should have positive centrality in '{case_name}', "
                    f"got {centrality}"
                )

    def test_winner_edge_not_self_loop(self, output_data):
        """Verify the winner edge is not a self-loop (X != Y)."""
        winner_edge = output_data.get("winner_edge")
        if not winner_edge:
            pytest.skip("winner_edge not found")

        parts = winner_edge.split("-")
        if len(parts) != 2:
            pytest.skip(f"Invalid winner_edge format: {winner_edge}")

        assert parts[0] != parts[1], (
            f"Winner edge cannot be a self-loop: {winner_edge}"
        )

    def test_no_null_values_in_case_entries(self, output_data):
        """Verify no case entry has null/None values for required fields."""
        cases = output_data.get("cases", {})

        for case_name, case_data in cases.items():
            assert case_data.get("centrality") is not None, (
                f"centrality is null for '{case_name}'"
            )
            assert case_data.get("rank") is not None, (
                f"rank is null for '{case_name}'"
            )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

HEREDOC_EOF

# Execute command
python3 -m py_compile expectation_tests.py && echo "Syntax OK"

# Execute command
python3 -m pytest expectation_tests.py --collect-only -q 2>&1 | head -50

# Execute command
ls -la /root/

# Create /root/analyze_critical_corridor.py
mkdir -p $(dirname /root/analyze_critical_corridor.py)
cat << 'HEREDOC_EOF' > /root/analyze_critical_corridor.py
#!/usr/bin/env python3
"""
Analyze critical transmission corridors across MATPOWER case files.
Identifies the most critical edge that is consistently critical across all cases
using edge betweenness centrality analysis.
"""

import json
import re
import numpy as np
import networkx as nx
from pathlib import Path


def parse_matpower_case(filepath):
    """
    Parse a MATPOWER .m case file and extract bus and branch data.

    Args:
        filepath: Path to the .m file

    Returns:
        dict with 'bus' and 'branch' as numpy arrays
    """
    with open(filepath, 'r') as f:
        content = f.read()

    # Parse mpc.bus matrix
    bus_match = re.search(r'mpc\.bus\s*=\s*\[(.*?)\];', content, re.DOTALL)
    if not bus_match:
        raise ValueError(f"Could not find mpc.bus in {filepath}")

    bus_data = []
    for line in bus_match.group(1).strip().split('\n'):
        # Remove comments and whitespace
        line = line.split('%')[0].strip()
        if line and not line.startswith('%'):
            # Remove trailing semicolon if present
            line = line.rstrip(';').strip()
            if line:
                values = [float(x) for x in line.split()]
                if values:
                    bus_data.append(values)

    # Parse mpc.branch matrix
    branch_match = re.search(r'mpc\.branch\s*=\s*\[(.*?)\];', content, re.DOTALL)
    if not branch_match:
        raise ValueError(f"Could not find mpc.branch in {filepath}")

    branch_data = []
    for line in branch_match.group(1).strip().split('\n'):
        # Remove comments and whitespace
        line = line.split('%')[0].strip()
        if line and not line.startswith('%'):
            # Remove trailing semicolon if present
            line = line.rstrip(';').strip()
            if line:
                values = [float(x) for x in line.split()]
                if values:
                    branch_data.append(values)

    return {
        'bus': np.array(bus_data),
        'branch': np.array(branch_data)
    }


def build_graph(data):
    """
    Build an undirected simple graph from MATPOWER case data.

    Args:
        data: dict with 'bus' and 'branch' numpy arrays

    Returns:
        NetworkX Graph object
    """
    buses = data['bus']
    branches = data['branch']

    G = nx.Graph()

    # Add nodes from bus data (column 0 is bus_i)
    for row in buses:
        G.add_node(int(row[0]))

    # Add edges from branch data (only in-service branches)
    # Column 0 = fbus, Column 1 = tbus, Column 10 = status
    for row in branches:
        status = row[10] if len(row) > 10 else 1  # Default to in-service
        if status == 1:
            fbus = int(row[0])
            tbus = int(row[1])
            # nx.Graph() automatically handles parallel edges (keeps only one)
            G.add_edge(fbus, tbus)

    return G


def get_top10_edges_with_centrality(G):
    """
    Compute edge betweenness centrality and return top 10 edges.

    Args:
        G: NetworkX Graph

    Returns:
        tuple: (top10_list, centrality_map, rank_map)
        - top10_list: List of canonical edge strings in rank order
        - centrality_map: dict mapping canonical edge string to centrality value
        - rank_map: dict mapping canonical edge string to rank (1-10)
    """
    # Compute edge betweenness centrality (normalized)
    ebc = nx.edge_betweenness_centrality(G, normalized=True)

    # Sort by centrality descending
    sorted_items = sorted(ebc.items(), key=lambda kv: kv[1], reverse=True)

    # Take top 10
    top10_items = sorted_items[:10]

    # Create canonical edge strings and maps
    top10_list = []
    centrality_map = {}
    rank_map = {}

    for rank, ((u, v), centrality) in enumerate(top10_items, start=1):
        # Canonical form: "min-max"
        edge_str = f"{min(u, v)}-{max(u, v)}"
        top10_list.append(edge_str)
        centrality_map[edge_str] = centrality
        rank_map[edge_str] = rank

    return top10_list, centrality_map, rank_map


def main():
    # Define input files
    input_dir = Path('/root')
    case_files = {
        'case57.m': input_dir / 'case57.m',
        'case118.m': input_dir / 'case118.m',
        'pglib_opf_case118_ieee.m': input_dir / 'pglib_opf_case118_ieee.m'
    }

    # Store results for each case
    results = {}

    print("=" * 60)
    print("Parsing MATPOWER case files and computing edge betweenness centrality")
    print("=" * 60)

    for case_name, filepath in case_files.items():
        print(f"\nProcessing {case_name}...")

        # Step 1: Parse the MATPOWER case file
        data = parse_matpower_case(filepath)
        n_buses = data['bus'].shape[0]
        n_branches = data['branch'].shape[0]
        print(f"  Parsed: {n_buses} buses, {n_branches} branches")

        # Verify branch data has correct number of columns
        if data['branch'].shape[1] < 11:
            raise ValueError(f"Branch data has only {data['branch'].shape[1]} columns, expected at least 11")

        # Step 2: Build the undirected simple graph
        G = build_graph(data)
        print(f"  Graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

        # Check connectivity
        is_connected = nx.is_connected(G)
        print(f"  Connected: {is_connected}")

        # Step 3: Compute edge betweenness centrality and get top 10
        top10_list, centrality_map, rank_map = get_top10_edges_with_centrality(G)

        print(f"  Top 10 edges by betweenness centrality:")
        for i, edge in enumerate(top10_list, start=1):
            print(f"    {i}. {edge}: {centrality_map[edge]:.10f}")

        results[case_name] = {
            'top10_list': top10_list,
            'centrality_map': centrality_map,
            'rank_map': rank_map
        }

    # Step 4: Compute intersection of top-10 sets
    print("\n" + "=" * 60)
    print("Computing intersection of top-10 sets")
    print("=" * 60)

    sets = [set(results[name]['top10_list']) for name in case_files.keys()]
    intersection = sets[0] & sets[1] & sets[2]

    print(f"\nIntersection size: {len(intersection)}")
    print(f"Intersection edges: {sorted(intersection)}")

    if len(intersection) == 0:
        raise ValueError("Task failed: intersection is empty")

    # Step 5: Select winner by average rank (lowest wins), lexicographic tie-break
    print("\n" + "=" * 60)
    print("Selecting winner edge")
    print("=" * 60)

    case_names = list(case_files.keys())

    candidates = []
    for edge in intersection:
        ranks = [results[name]['rank_map'][edge] for name in case_names]
        avg_rank = sum(ranks) / len(ranks)
        candidates.append((edge, avg_rank, ranks))
        print(f"  {edge}: ranks={ranks}, avg_rank={avg_rank:.4f}")

    # Sort by average rank (ascending), then by edge string (lexicographic)
    candidates.sort(key=lambda x: (x[1], x[0]))

    winner_edge = candidates[0][0]
    print(f"\nWinner: {winner_edge} (avg_rank={candidates[0][1]:.4f})")

    # Step 6: Build output JSON
    output = {
        "winner_edge": winner_edge,
        "cases": {},
        "intersection_size": len(intersection)
    }

    for case_name in case_names:
        output["cases"][case_name] = {
            "centrality": results[case_name]['centrality_map'][winner_edge],
            "rank": results[case_name]['rank_map'][winner_edge]
        }

    # Step 7: Write output JSON
    output_dir = Path('/root')
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / 'shared_critical_corridor.json'

    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\n" + "=" * 60)
    print(f"Output written to: {output_path}")
    print("=" * 60)
    print("\nFinal JSON output:")
    print(json.dumps(output, indent=2))

    return output


if __name__ == '__main__':
    main()

HEREDOC_EOF

# Execute command
python3 analyze_critical_corridor.py

