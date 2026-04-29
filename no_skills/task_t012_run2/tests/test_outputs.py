"""Stronger expectation tests for task verification.

This version recomputes the expected result directly from the three MATPOWER
case files, instead of only checking output schema/typing.

Note:
- The task instruction specifies deterministic selection of the final winner,
  but does not explicitly define how to break per-case ties among edges with
  identical betweenness centrality when producing each case's top-10 ranking.
- For deterministic verification, these tests break per-case ties by the
  lexicographically smallest canonical edge string ("minBus-maxBus").
"""

from __future__ import annotations

import json
import math
import os
import re
from pathlib import Path

import pytest

nx = pytest.importorskip("networkx")


# Constants
OUTPUT_PATH = Path("/root/shared_critical_corridor.json")
CASE_PATHS = {
    "case57.m": Path("/root/case57.m"),
    "case118.m": Path("/root/case118.m"),
    "pglib_opf_case118_ieee.m": Path("/root/pglib_opf_case118_ieee.m"),
}
EXPECTED_TOP_LEVEL_FIELDS = {"winner_edge", "cases", "intersection_size"}
EXPECTED_CASE_FIELDS = {"centrality", "rank"}


def canonical_edge(u: int, v: int) -> str:
    a, b = sorted((int(u), int(v)))
    return f"{a}-{b}"


def parse_matpower_matrix(file_text: str, matrix_name: str) -> list[list[float]]:
    """Extract a MATPOWER matrix block like mpc.bus = [ ... ]; or mpc.branch = [ ... ];"""
    pattern = rf"mpc\.{re.escape(matrix_name)}\s*=\s*\[(.*?)\];"
    match = re.search(pattern, file_text, flags=re.DOTALL)
    assert match is not None, f"Could not find 'mpc.{matrix_name} = [ ... ];' block"

    block = match.group(1)
    rows: list[list[float]] = []

    for raw_line in block.splitlines():
        # Strip MATLAB comments
        line = raw_line.split("%", 1)[0].strip()
        if not line:
            continue

        # Remove trailing semicolons, then split on whitespace
        line = line.replace(";", " ").strip()
        if not line:
            continue

        parts = line.split()
        try:
            row = [float(part) for part in parts]
        except ValueError as exc:
            raise AssertionError(
                f"Failed to parse numeric row in mpc.{matrix_name}: {raw_line!r}"
            ) from exc

        rows.append(row)

    assert rows, f"Parsed mpc.{matrix_name} but found no numeric rows"

    width = len(rows[0])
    for i, row in enumerate(rows, start=1):
        assert len(row) == width, (
            f"Inconsistent column count in mpc.{matrix_name}: "
            f"row 1 has {width} columns but row {i} has {len(row)}"
        )

    return rows


def build_graph_from_case(case_path: Path):
    """Parse one MATPOWER case and build the undirected simple graph required by the task."""
    assert case_path.exists(), f"Missing required case file: {case_path}"
    text = case_path.read_text(encoding="utf-8", errors="replace")

    bus_rows = parse_matpower_matrix(text, "bus")
    branch_rows = parse_matpower_matrix(text, "branch")

    g = nx.Graph()

    # Nodes = bus_i
    for row in bus_rows:
        bus_i = int(row[0])
        g.add_node(bus_i)

    # Edges = in-service branches only, using a simple undirected graph
    # branch[:, 10] == 1  -> zero-based index 10
    for row in branch_rows:
        assert len(row) > 10, (
            "Each branch row must have at least 11 columns so branch[:, 10] exists"
        )
        status = int(row[10])
        if status != 1:
            continue

        fbus = int(row[0])
        tbus = int(row[1])
        g.add_edge(fbus, tbus)  # nx.Graph collapses parallel edges automatically

    return g


def compute_case_analysis(case_path: Path) -> dict:
    """Compute edge betweenness centrality and deterministic top-10 ranking for one case."""
    g = build_graph_from_case(case_path)
    centrality_raw = nx.edge_betweenness_centrality(g, normalized=True)

    # Convert edge keys to canonical "minBus-maxBus" strings
    centrality_by_edge = {
        canonical_edge(u, v): value for (u, v), value in centrality_raw.items()
    }

    # Deterministic ranking: descending centrality, then lexicographic edge string
    ranked_edges = sorted(
        centrality_by_edge.items(),
        key=lambda item: (-item[1], item[0]),
    )
    top10 = ranked_edges[:10]

    return {
        "centrality_by_edge": centrality_by_edge,
        "top10": top10,
        "top10_set": {edge for edge, _ in top10},
        "ranks": {edge: rank for rank, (edge, _) in enumerate(top10, start=1)},
    }


@pytest.fixture(scope="module")
def expected_result():
    """Recompute the exact expected output from the three case files."""
    per_case = {
        case_name: compute_case_analysis(case_path)
        for case_name, case_path in CASE_PATHS.items()
    }

    intersection = set.intersection(*(data["top10_set"] for data in per_case.values()))
    assert intersection, (
        "The recomputed top-10 intersection is empty, but the task specification "
        "requires a non-empty intersection for successful completion."
    )

    def average_rank(edge: str) -> float:
        return sum(per_case[name]["ranks"][edge] for name in CASE_PATHS) / len(CASE_PATHS)

    winner_edge = min(intersection, key=lambda edge: (average_rank(edge), edge))

    cases_payload = {
        case_name: {
            "centrality": per_case[case_name]["centrality_by_edge"][winner_edge],
            "rank": per_case[case_name]["ranks"][winner_edge],
        }
        for case_name in CASE_PATHS
    }

    return {
        "winner_edge": winner_edge,
        "cases": cases_payload,
        "intersection_size": len(intersection),
        "per_case": per_case,
        "intersection": intersection,
    }


@pytest.fixture(scope="module")
def output_data():
    """Load and validate that the output JSON file exists and is parseable."""
    assert OUTPUT_PATH.exists(), (
        f"Output file not found at {OUTPUT_PATH}. "
        "The task requires writing the JSON result to this exact path."
    )
    assert OUTPUT_PATH.stat().st_size > 0, "Output file exists but is empty"

    with OUTPUT_PATH.open("r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as exc:
            pytest.fail(f"Output file is not valid JSON: {exc}")

    assert isinstance(data, dict), (
        f"Output JSON should be an object (dict), got {type(data).__name__}"
    )
    return data


class TestOutputSchema:
    def test_top_level_fields_exact(self, output_data):
        assert set(output_data.keys()) == EXPECTED_TOP_LEVEL_FIELDS, (
            f"Top-level fields must be exactly {EXPECTED_TOP_LEVEL_FIELDS}, "
            f"got {set(output_data.keys())}"
        )

    def test_cases_object_exists(self, output_data):
        assert isinstance(output_data["cases"], dict), (
            f"'cases' must be an object (dict), got {type(output_data['cases']).__name__}"
        )

    def test_cases_has_exact_case_names(self, output_data):
        assert set(output_data["cases"].keys()) == set(CASE_PATHS.keys()), (
            f"'cases' must contain exactly these keys: {set(CASE_PATHS.keys())}, "
            f"got {set(output_data['cases'].keys())}"
        )

    @pytest.mark.parametrize("case_name", CASE_PATHS.keys())
    def test_each_case_has_exact_fields(self, output_data, case_name):
        case_data = output_data["cases"][case_name]
        assert isinstance(case_data, dict), (
            f"cases['{case_name}'] must be an object, got {type(case_data).__name__}"
        )
        assert set(case_data.keys()) == EXPECTED_CASE_FIELDS, (
            f"cases['{case_name}'] must contain exactly {EXPECTED_CASE_FIELDS}, "
            f"got {set(case_data.keys())}"
        )


class TestWinnerEdgeField:
    def test_winner_edge_is_string(self, output_data):
        assert isinstance(output_data["winner_edge"], str), (
            f"winner_edge should be a string, got {type(output_data['winner_edge']).__name__}"
        )

    def test_winner_edge_format(self, output_data):
        winner_edge = output_data["winner_edge"]
        assert re.fullmatch(r"\d+-\d+", winner_edge), (
            f"winner_edge '{winner_edge}' does not match expected format 'X-Y'"
        )

    def test_winner_edge_is_canonical(self, output_data):
        winner_edge = output_data["winner_edge"]
        a_str, b_str = winner_edge.split("-")
        a = int(a_str)
        b = int(b_str)
        assert a > 0 and b > 0, f"Bus numbers must be positive, got '{winner_edge}'"
        assert a < b, f"winner_edge must be canonical minBus-maxBus, got '{winner_edge}'"

    def test_winner_edge_matches_recomputed_expected(self, output_data, expected_result):
        assert output_data["winner_edge"] == expected_result["winner_edge"], (
            "winner_edge does not match the recomputed expected result. "
            f"Expected '{expected_result['winner_edge']}', got '{output_data['winner_edge']}'."
        )


class TestIntersectionSize:
    def test_intersection_size_is_int(self, output_data):
        assert isinstance(output_data["intersection_size"], int), (
            f"intersection_size should be an int, got {type(output_data['intersection_size']).__name__}"
        )

    def test_intersection_size_matches_recomputed_expected(self, output_data, expected_result):
        assert output_data["intersection_size"] == expected_result["intersection_size"], (
            "intersection_size does not match the recomputed expected result. "
            f"Expected {expected_result['intersection_size']}, got {output_data['intersection_size']}."
        )

    def test_intersection_size_in_valid_range(self, output_data):
        assert 1 <= output_data["intersection_size"] <= 10, (
            f"intersection_size must be between 1 and 10, got {output_data['intersection_size']}"
        )


class TestPerCaseValues:
    @pytest.mark.parametrize("case_name", CASE_PATHS.keys())
    def test_case_centrality_is_numeric_and_finite(self, output_data, case_name):
        centrality = output_data["cases"][case_name]["centrality"]
        assert isinstance(centrality, (int, float)), (
            f"centrality for '{case_name}' should be numeric, got {type(centrality).__name__}"
        )
        assert math.isfinite(centrality), (
            f"centrality for '{case_name}' must be finite, got {centrality}"
        )

    @pytest.mark.parametrize("case_name", CASE_PATHS.keys())
    def test_case_centrality_matches_recomputed_expected(self, output_data, expected_result, case_name):
        actual = output_data["cases"][case_name]["centrality"]
        expected = expected_result["cases"][case_name]["centrality"]
        assert actual == pytest.approx(expected, rel=1e-12, abs=1e-12), (
            f"centrality for '{case_name}' does not match the recomputed expected value. "
            f"Expected {expected}, got {actual}."
        )

    @pytest.mark.parametrize("case_name", CASE_PATHS.keys())
    def test_case_rank_is_integer(self, output_data, case_name):
        rank = output_data["cases"][case_name]["rank"]
        assert isinstance(rank, int), (
            f"rank for '{case_name}' should be an int, got {type(rank).__name__}"
        )

    @pytest.mark.parametrize("case_name", CASE_PATHS.keys())
    def test_case_rank_in_valid_range(self, output_data, case_name):
        rank = output_data["cases"][case_name]["rank"]
        assert 1 <= rank <= 10, (
            f"rank for '{case_name}' must be between 1 and 10, got {rank}"
        )

    @pytest.mark.parametrize("case_name", CASE_PATHS.keys())
    def test_case_rank_matches_recomputed_expected(self, output_data, expected_result, case_name):
        actual = output_data["cases"][case_name]["rank"]
        expected = expected_result["cases"][case_name]["rank"]
        assert actual == expected, (
            f"rank for '{case_name}' does not match the recomputed expected value. "
            f"Expected {expected}, got {actual}."
        )


class TestAlgorithmicConsistency:
    def test_winner_edge_is_in_true_intersection(self, output_data, expected_result):
        winner_edge = output_data["winner_edge"]
        assert winner_edge in expected_result["intersection"], (
            f"winner_edge '{winner_edge}' is not in the true intersection of the three top-10 sets"
        )

    def test_output_case_values_correspond_to_winner_edge(self, output_data, expected_result):
        winner_edge = output_data["winner_edge"]
        for case_name in CASE_PATHS:
            expected_centrality = expected_result["per_case"][case_name]["centrality_by_edge"][winner_edge]
            expected_rank = expected_result["per_case"][case_name]["ranks"][winner_edge]

            actual_case = output_data["cases"][case_name]
            assert actual_case["centrality"] == pytest.approx(
                expected_centrality, rel=1e-12, abs=1e-12
            ), (
                f"cases['{case_name}']['centrality'] does not correspond to winner_edge '{winner_edge}'"
            )
            assert actual_case["rank"] == expected_rank, (
                f"cases['{case_name}']['rank'] does not correspond to winner_edge '{winner_edge}'"
            )

    def test_reported_winner_is_true_average_rank_winner(self, output_data, expected_result):
        assert output_data["winner_edge"] == expected_result["winner_edge"], (
            "Reported winner_edge is not the true winner after recomputing "
            "top-10 intersections and average ranks from the case files."
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])