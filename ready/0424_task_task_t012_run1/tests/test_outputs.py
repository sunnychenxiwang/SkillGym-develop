import json
import math
import os

import pytest


class TestMostCriticalCorridor:
    """Tests for verifying the most_critical_corridor.json output."""

    OUTPUT_FILE = "/root/output/most_critical_corridor.json"
    TOLERANCE = 0.001

    EXPECTED_OVERALL_WINNER = {
        "source_file": "pglib_opf_case118_ieee.m",
        "bus_u": 38,
        "bus_v": 65,
        "mw_flow_abs": 353.11266121412024,
        "edge_betweenness": 0.2574439527829361,
        "severity": 90.90671928066487,
        "total_load_mw": 4242.0,
        "normalized_severity": 0.021430155417412746
    }

    EXPECTED_PER_FILE_WINNERS = [
        {
            "source_file": "case57.m",
            "bus_u": 8,
            "bus_v": 9,
            "mw_flow_abs": 177.1093222897914,
            "edge_betweenness": 0.14184941520467834,
            "severity": 25.122853794103815,
            "total_load_mw": 1250.7999999999993,
            "normalized_severity": 0.02008542836113194
        },
        {
            "source_file": "case118.m",
            "bus_u": 38,
            "bus_v": 65,
            "mw_flow_abs": 160.24340089106227,
            "edge_betweenness": 0.2574439527829361,
            "severity": 41.25369453277573,
            "total_load_mw": 4242.0,
            "normalized_severity": 0.009725057645633129
        },
        {
            "source_file": "pglib_opf_case118_ieee.m",
            "bus_u": 38,
            "bus_v": 65,
            "mw_flow_abs": 353.11266121412024,
            "edge_betweenness": 0.2574439527829361,
            "severity": 90.90671928066487,
            "total_load_mw": 4242.0,
            "normalized_severity": 0.021430155417412746
        }
    ]

    REQUIRED_WINNER_FIELDS = [
        "source_file", "bus_u", "bus_v", "mw_flow_abs",
        "edge_betweenness", "severity", "total_load_mw", "normalized_severity"
    ]

    VALID_SOURCE_FILES = ["case57.m", "case118.m", "pglib_opf_case118_ieee.m"]

    # --- Structural Tests ---

    def test_file_exists(self):
        """Verify output file was created."""
        assert os.path.exists(self.OUTPUT_FILE), f"Output file not found: {self.OUTPUT_FILE}"

    def test_valid_json(self):
        """Verify output is valid JSON."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert isinstance(data, dict), "Output should be a JSON object"

    def test_has_overall_winner_key(self):
        """Verify overall_winner key exists."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert "overall_winner" in data, "Missing required key: overall_winner"

    def test_has_per_file_winners_key(self):
        """Verify per_file_winners key exists."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert "per_file_winners" in data, "Missing required key: per_file_winners"

    def test_per_file_winners_is_list(self):
        """Verify per_file_winners is a list."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert isinstance(data["per_file_winners"], list), "per_file_winners should be a list"

    def test_per_file_winners_count(self):
        """Verify per_file_winners has exactly 3 entries (one per input file)."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert len(data["per_file_winners"]) == 3, \
            f"Expected 3 per_file_winners, got {len(data['per_file_winners'])}"

    # --- Content Tests: Required Fields ---

    def test_overall_winner_has_required_fields(self):
        """Verify overall_winner has all required fields."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        overall_winner = data["overall_winner"]
        for field in self.REQUIRED_WINNER_FIELDS:
            assert field in overall_winner, f"Missing required field in overall_winner: {field}"

    def test_per_file_winners_have_required_fields(self):
        """Verify each per_file_winner has all required fields."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        for i, winner in enumerate(data["per_file_winners"]):
            for field in self.REQUIRED_WINNER_FIELDS:
                assert field in winner, \
                    f"Missing required field '{field}' in per_file_winners[{i}]"

    # --- Content Tests: Data Types ---

    def test_overall_winner_field_types(self):
        """Verify overall_winner fields have correct data types."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        ow = data["overall_winner"]
        assert isinstance(ow["source_file"], str), "source_file should be a string"
        assert isinstance(ow["bus_u"], int), "bus_u should be an integer"
        assert isinstance(ow["bus_v"], int), "bus_v should be an integer"
        assert isinstance(ow["mw_flow_abs"], (int, float)), "mw_flow_abs should be a number"
        assert isinstance(ow["edge_betweenness"], (int, float)), "edge_betweenness should be a number"
        assert isinstance(ow["severity"], (int, float)), "severity should be a number"
        assert isinstance(ow["total_load_mw"], (int, float)), "total_load_mw should be a number"
        assert isinstance(ow["normalized_severity"], (int, float)), "normalized_severity should be a number"

    def test_per_file_winners_field_types(self):
        """Verify per_file_winners fields have correct data types."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        for i, winner in enumerate(data["per_file_winners"]):
            assert isinstance(winner["source_file"], str), \
                f"per_file_winners[{i}].source_file should be a string"
            assert isinstance(winner["bus_u"], int), \
                f"per_file_winners[{i}].bus_u should be an integer"
            assert isinstance(winner["bus_v"], int), \
                f"per_file_winners[{i}].bus_v should be an integer"
            assert isinstance(winner["mw_flow_abs"], (int, float)), \
                f"per_file_winners[{i}].mw_flow_abs should be a number"
            assert isinstance(winner["edge_betweenness"], (int, float)), \
                f"per_file_winners[{i}].edge_betweenness should be a number"
            assert isinstance(winner["severity"], (int, float)), \
                f"per_file_winners[{i}].severity should be a number"
            assert isinstance(winner["total_load_mw"], (int, float)), \
                f"per_file_winners[{i}].total_load_mw should be a number"
            assert isinstance(winner["normalized_severity"], (int, float)), \
                f"per_file_winners[{i}].normalized_severity should be a number"

    # --- Content Tests: Valid Values ---

    def test_overall_winner_source_file_valid(self):
        """Verify overall_winner source_file is one of the valid input files."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        source_file = data["overall_winner"]["source_file"]
        assert source_file in self.VALID_SOURCE_FILES, \
            f"Invalid source_file: {source_file}. Expected one of {self.VALID_SOURCE_FILES}"

    def test_per_file_winners_source_files_valid(self):
        """Verify each per_file_winner has a valid source_file."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        for i, winner in enumerate(data["per_file_winners"]):
            assert winner["source_file"] in self.VALID_SOURCE_FILES, \
                f"Invalid source_file in per_file_winners[{i}]: {winner['source_file']}"

    def test_per_file_winners_order(self):
        """Verify per_file_winners are in correct order: case57.m, case118.m, pglib_opf_case118_ieee.m."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        expected_order = ["case57.m", "case118.m", "pglib_opf_case118_ieee.m"]
        actual_order = [w["source_file"] for w in data["per_file_winners"]]
        assert actual_order == expected_order, \
            f"Incorrect per_file_winners order. Expected {expected_order}, got {actual_order}"

    def test_bus_ordering_convention(self):
        """Verify bus_u < bus_v (direction-independent ordering)."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        ow = data["overall_winner"]
        assert ow["bus_u"] < ow["bus_v"], \
            f"Overall winner should have bus_u < bus_v, got ({ow['bus_u']}, {ow['bus_v']})"
        for i, winner in enumerate(data["per_file_winners"]):
            assert winner["bus_u"] < winner["bus_v"], \
                f"per_file_winners[{i}] should have bus_u < bus_v, got ({winner['bus_u']}, {winner['bus_v']})"

    def test_positive_numeric_values(self):
        """Verify all numeric values are positive (MW flow, betweenness, severity, load)."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        ow = data["overall_winner"]
        assert ow["mw_flow_abs"] > 0, "mw_flow_abs should be positive"
        assert ow["edge_betweenness"] > 0, "edge_betweenness should be positive"
        assert ow["severity"] > 0, "severity should be positive"
        assert ow["total_load_mw"] > 0, "total_load_mw should be positive"
        assert ow["normalized_severity"] > 0, "normalized_severity should be positive"

    # --- Value Tests: Overall Winner ---

    def test_overall_winner_source_file(self):
        """Verify overall_winner source_file matches expected."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert data["overall_winner"]["source_file"] == self.EXPECTED_OVERALL_WINNER["source_file"], \
            f"Unexpected overall_winner source_file: {data['overall_winner']['source_file']}"

    def test_overall_winner_bus_u(self):
        """Verify overall_winner bus_u matches expected."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert data["overall_winner"]["bus_u"] == self.EXPECTED_OVERALL_WINNER["bus_u"], \
            f"Expected bus_u={self.EXPECTED_OVERALL_WINNER['bus_u']}, got {data['overall_winner']['bus_u']}"

    def test_overall_winner_bus_v(self):
        """Verify overall_winner bus_v matches expected."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert data["overall_winner"]["bus_v"] == self.EXPECTED_OVERALL_WINNER["bus_v"], \
            f"Expected bus_v={self.EXPECTED_OVERALL_WINNER['bus_v']}, got {data['overall_winner']['bus_v']}"

    def test_overall_winner_mw_flow_abs(self):
        """Verify overall_winner mw_flow_abs matches expected within tolerance."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert math.isclose(
            data["overall_winner"]["mw_flow_abs"],
            self.EXPECTED_OVERALL_WINNER["mw_flow_abs"],
            rel_tol=self.TOLERANCE
        ), f"mw_flow_abs mismatch: expected {self.EXPECTED_OVERALL_WINNER['mw_flow_abs']}, " \
           f"got {data['overall_winner']['mw_flow_abs']}"

    def test_overall_winner_edge_betweenness(self):
        """Verify overall_winner edge_betweenness matches expected within tolerance."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert math.isclose(
            data["overall_winner"]["edge_betweenness"],
            self.EXPECTED_OVERALL_WINNER["edge_betweenness"],
            rel_tol=self.TOLERANCE
        ), f"edge_betweenness mismatch: expected {self.EXPECTED_OVERALL_WINNER['edge_betweenness']}, " \
           f"got {data['overall_winner']['edge_betweenness']}"

    def test_overall_winner_severity(self):
        """Verify overall_winner severity matches expected within tolerance."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert math.isclose(
            data["overall_winner"]["severity"],
            self.EXPECTED_OVERALL_WINNER["severity"],
            rel_tol=self.TOLERANCE
        ), f"severity mismatch: expected {self.EXPECTED_OVERALL_WINNER['severity']}, " \
           f"got {data['overall_winner']['severity']}"

    def test_overall_winner_total_load_mw(self):
        """Verify overall_winner total_load_mw matches expected within tolerance."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert math.isclose(
            data["overall_winner"]["total_load_mw"],
            self.EXPECTED_OVERALL_WINNER["total_load_mw"],
            rel_tol=self.TOLERANCE
        ), f"total_load_mw mismatch: expected {self.EXPECTED_OVERALL_WINNER['total_load_mw']}, " \
           f"got {data['overall_winner']['total_load_mw']}"

    def test_overall_winner_normalized_severity(self):
        """Verify overall_winner normalized_severity matches expected within tolerance."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert math.isclose(
            data["overall_winner"]["normalized_severity"],
            self.EXPECTED_OVERALL_WINNER["normalized_severity"],
            rel_tol=self.TOLERANCE
        ), f"normalized_severity mismatch: expected {self.EXPECTED_OVERALL_WINNER['normalized_severity']}, " \
           f"got {data['overall_winner']['normalized_severity']}"

    # --- Value Tests: Per-File Winners ---

    def test_case57_winner_values(self):
        """Verify case57.m per_file_winner values match expected."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        winner = data["per_file_winners"][0]
        expected = self.EXPECTED_PER_FILE_WINNERS[0]

        assert winner["source_file"] == expected["source_file"]
        assert winner["bus_u"] == expected["bus_u"]
        assert winner["bus_v"] == expected["bus_v"]
        assert math.isclose(winner["mw_flow_abs"], expected["mw_flow_abs"], rel_tol=self.TOLERANCE)
        assert math.isclose(winner["edge_betweenness"], expected["edge_betweenness"], rel_tol=self.TOLERANCE)
        assert math.isclose(winner["severity"], expected["severity"], rel_tol=self.TOLERANCE)
        assert math.isclose(winner["total_load_mw"], expected["total_load_mw"], rel_tol=self.TOLERANCE)
        assert math.isclose(winner["normalized_severity"], expected["normalized_severity"], rel_tol=self.TOLERANCE)

    def test_case118_winner_values(self):
        """Verify case118.m per_file_winner values match expected."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        winner = data["per_file_winners"][1]
        expected = self.EXPECTED_PER_FILE_WINNERS[1]

        assert winner["source_file"] == expected["source_file"]
        assert winner["bus_u"] == expected["bus_u"]
        assert winner["bus_v"] == expected["bus_v"]
        assert math.isclose(winner["mw_flow_abs"], expected["mw_flow_abs"], rel_tol=self.TOLERANCE)
        assert math.isclose(winner["edge_betweenness"], expected["edge_betweenness"], rel_tol=self.TOLERANCE)
        assert math.isclose(winner["severity"], expected["severity"], rel_tol=self.TOLERANCE)
        assert math.isclose(winner["total_load_mw"], expected["total_load_mw"], rel_tol=self.TOLERANCE)
        assert math.isclose(winner["normalized_severity"], expected["normalized_severity"], rel_tol=self.TOLERANCE)

    def test_pglib_case118_winner_values(self):
        """Verify pglib_opf_case118_ieee.m per_file_winner values match expected."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        winner = data["per_file_winners"][2]
        expected = self.EXPECTED_PER_FILE_WINNERS[2]

        assert winner["source_file"] == expected["source_file"]
        assert winner["bus_u"] == expected["bus_u"]
        assert winner["bus_v"] == expected["bus_v"]
        assert math.isclose(winner["mw_flow_abs"], expected["mw_flow_abs"], rel_tol=self.TOLERANCE)
        assert math.isclose(winner["edge_betweenness"], expected["edge_betweenness"], rel_tol=self.TOLERANCE)
        assert math.isclose(winner["severity"], expected["severity"], rel_tol=self.TOLERANCE)
        assert math.isclose(winner["total_load_mw"], expected["total_load_mw"], rel_tol=self.TOLERANCE)
        assert math.isclose(winner["normalized_severity"], expected["normalized_severity"], rel_tol=self.TOLERANCE)

    # --- Integrity Tests: Consistency Checks ---

    def test_severity_formula_consistency(self):
        """Verify severity = |mw_flow| * edge_betweenness for all winners."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        ow = data["overall_winner"]
        calculated_severity = ow["mw_flow_abs"] * ow["edge_betweenness"]
        assert math.isclose(ow["severity"], calculated_severity, rel_tol=self.TOLERANCE), \
            f"Overall winner severity formula mismatch: {ow['severity']} != {calculated_severity}"

        for i, winner in enumerate(data["per_file_winners"]):
            calculated_severity = winner["mw_flow_abs"] * winner["edge_betweenness"]
            assert math.isclose(winner["severity"], calculated_severity, rel_tol=self.TOLERANCE), \
                f"per_file_winners[{i}] severity formula mismatch: {winner['severity']} != {calculated_severity}"

    def test_normalized_severity_formula_consistency(self):
        """Verify normalized_severity = severity / total_load_mw for all winners."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        ow = data["overall_winner"]
        calculated_norm = ow["severity"] / ow["total_load_mw"]
        assert math.isclose(ow["normalized_severity"], calculated_norm, rel_tol=self.TOLERANCE), \
            f"Overall winner normalized_severity formula mismatch"

        for i, winner in enumerate(data["per_file_winners"]):
            calculated_norm = winner["severity"] / winner["total_load_mw"]
            assert math.isclose(winner["normalized_severity"], calculated_norm, rel_tol=self.TOLERANCE), \
                f"per_file_winners[{i}] normalized_severity formula mismatch"

    def test_overall_winner_has_highest_normalized_severity(self):
        """Verify overall_winner has the highest normalized_severity among all per_file_winners."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        overall_norm = data["overall_winner"]["normalized_severity"]
        for i, winner in enumerate(data["per_file_winners"]):
            assert overall_norm >= winner["normalized_severity"] - self.TOLERANCE, \
                f"Overall winner normalized_severity ({overall_norm}) should be >= " \
                f"per_file_winners[{i}] ({winner['normalized_severity']})"

    def test_overall_winner_matches_one_per_file_winner(self):
        """Verify overall_winner corresponds to one of the per_file_winners."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        ow = data["overall_winner"]
        match_found = False
        for winner in data["per_file_winners"]:
            if (winner["source_file"] == ow["source_file"] and
                winner["bus_u"] == ow["bus_u"] and
                winner["bus_v"] == ow["bus_v"]):
                match_found = True
                assert math.isclose(winner["severity"], ow["severity"], rel_tol=self.TOLERANCE), \
                    "Overall winner severity should match its per_file_winner entry"
                break

        assert match_found, "Overall winner should match one of the per_file_winners"
