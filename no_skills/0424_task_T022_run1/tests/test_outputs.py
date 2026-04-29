import json
import math
import os

import pytest


class TestIrisSpeciesFactorProfile:
    """Tests for verifying iris species factor profile output."""

    OUTPUT_FILE = "/root/output/iris_species_factor_profile.json"

    EXPECTED_RESULT = {
        "n_factors": 1,
        "species_order": ["setosa", "versicolor", "virginica"],
        "mean_factor_scores": {
            "setosa": [1.301965],
            "versicolor": [-0.236671],
            "virginica": [-1.065294]
        }
    }
    TOLERANCE = 1e-6

    def test_file_exists(self):
        """Verify output file was created."""
        assert os.path.exists(self.OUTPUT_FILE), f"Output file not found: {self.OUTPUT_FILE}"

    def test_valid_json(self):
        """Verify output is valid JSON."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert isinstance(data, dict), "JSON root must be an object"

    def test_has_required_fields(self):
        """Verify all required fields are present."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert "n_factors" in data, "Missing required field: n_factors"
        assert "species_order" in data, "Missing required field: species_order"
        assert "mean_factor_scores" in data, "Missing required field: mean_factor_scores"

    def test_no_extra_keys(self):
        """Verify no extra keys beyond the required schema."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        expected_keys = {"n_factors", "species_order", "mean_factor_scores"}
        actual_keys = set(data.keys())
        assert actual_keys == expected_keys, f"Unexpected keys: {actual_keys - expected_keys}"

    def test_n_factors_value(self):
        """Verify n_factors matches Kaiser criterion result."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert data["n_factors"] == self.EXPECTED_RESULT["n_factors"], \
            f"n_factors mismatch: expected {self.EXPECTED_RESULT['n_factors']}, got {data['n_factors']}"

    def test_n_factors_type(self):
        """Verify n_factors is an integer."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert isinstance(data["n_factors"], int), \
            f"n_factors must be int, got {type(data['n_factors']).__name__}"

    def test_species_order_value(self):
        """Verify species_order is alphabetically sorted as required."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert data["species_order"] == self.EXPECTED_RESULT["species_order"], \
            f"species_order mismatch: expected {self.EXPECTED_RESULT['species_order']}, got {data['species_order']}"

    def test_species_order_type(self):
        """Verify species_order is a list of strings."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert isinstance(data["species_order"], list), "species_order must be a list"
        assert all(isinstance(s, str) for s in data["species_order"]), \
            "All species_order items must be strings"

    def test_mean_factor_scores_has_all_species(self):
        """Verify mean_factor_scores contains all three species."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        expected_species = {"setosa", "versicolor", "virginica"}
        actual_species = set(data["mean_factor_scores"].keys())
        assert actual_species == expected_species, \
            f"Species mismatch in mean_factor_scores: expected {expected_species}, got {actual_species}"

    def test_mean_factor_scores_list_length(self):
        """Verify each species has n_factors values in its list."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        n_factors = data["n_factors"]
        for species, scores in data["mean_factor_scores"].items():
            assert isinstance(scores, list), f"{species} scores must be a list"
            assert len(scores) == n_factors, \
                f"{species} should have {n_factors} scores, got {len(scores)}"

    def test_mean_factor_scores_are_floats(self):
        """Verify all mean factor scores are numeric (float or int)."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        for species, scores in data["mean_factor_scores"].items():
            for i, score in enumerate(scores):
                assert isinstance(score, (int, float)), \
                    f"{species} score[{i}] must be numeric, got {type(score).__name__}"

    def test_setosa_mean_factor_scores(self):
        """Verify setosa mean factor scores match expected values."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        expected = self.EXPECTED_RESULT["mean_factor_scores"]["setosa"]
        actual = data["mean_factor_scores"]["setosa"]
        for i, (exp, act) in enumerate(zip(expected, actual)):
            assert math.isclose(act, exp, rel_tol=self.TOLERANCE), \
                f"setosa Factor{i+1} mismatch: expected {exp}, got {act}"

    def test_versicolor_mean_factor_scores(self):
        """Verify versicolor mean factor scores match expected values."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        expected = self.EXPECTED_RESULT["mean_factor_scores"]["versicolor"]
        actual = data["mean_factor_scores"]["versicolor"]
        for i, (exp, act) in enumerate(zip(expected, actual)):
            assert math.isclose(act, exp, rel_tol=self.TOLERANCE), \
                f"versicolor Factor{i+1} mismatch: expected {exp}, got {act}"

    def test_virginica_mean_factor_scores(self):
        """Verify virginica mean factor scores match expected values."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        expected = self.EXPECTED_RESULT["mean_factor_scores"]["virginica"]
        actual = data["mean_factor_scores"]["virginica"]
        for i, (exp, act) in enumerate(zip(expected, actual)):
            assert math.isclose(act, exp, rel_tol=self.TOLERANCE), \
                f"virginica Factor{i+1} mismatch: expected {exp}, got {act}"

    def test_scores_rounded_to_six_decimals(self):
        """Verify all scores are rounded to at most 6 decimal places."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        for species, scores in data["mean_factor_scores"].items():
            for i, score in enumerate(scores):
                score_str = str(score)
                if '.' in score_str:
                    decimals = len(score_str.split('.')[1])
                    assert decimals <= 6, \
                        f"{species} Factor{i+1} has {decimals} decimals (max 6): {score}"
