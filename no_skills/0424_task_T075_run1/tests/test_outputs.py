import json
import math
import os

import pytest


class TestIrisDimredWinner:
    """Tests for verifying iris_dimred_winner.json output."""

    OUTPUT_FILE = "/root/output/iris_dimred_winner.json"

    EXPECTED_RESULT = {
        "winner": "PCA",
        "pca_mean_accuracy": 0.9133,
        "varimax_mean_accuracy": 0.86,
    }
    TOLERANCE = 0.0001

    def test_file_exists(self):
        """Verify output file was created."""
        assert os.path.exists(self.OUTPUT_FILE), f"Output file not found: {self.OUTPUT_FILE}"

    def test_valid_json(self):
        """Verify output is valid JSON."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert isinstance(data, dict), "Output should be a JSON object"

    def test_has_required_fields(self):
        """Verify all required fields are present."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert "winner" in data, "Missing required field: winner"
        assert "pca_mean_accuracy" in data, "Missing required field: pca_mean_accuracy"
        assert "varimax_mean_accuracy" in data, "Missing required field: varimax_mean_accuracy"

    def test_winner_value_valid(self):
        """Verify winner is either PCA or VARIMAX."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert data["winner"] in ["PCA", "VARIMAX"], \
            f"winner must be 'PCA' or 'VARIMAX', got '{data['winner']}'"

    def test_winner_correct(self):
        """Verify winner matches expected value."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert data["winner"] == self.EXPECTED_RESULT["winner"], \
            f"winner mismatch: expected {self.EXPECTED_RESULT['winner']}, got {data['winner']}"

    def test_pca_mean_accuracy_type(self):
        """Verify pca_mean_accuracy is a number."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert isinstance(data["pca_mean_accuracy"], (int, float)), \
            f"pca_mean_accuracy should be a number, got {type(data['pca_mean_accuracy'])}"

    def test_varimax_mean_accuracy_type(self):
        """Verify varimax_mean_accuracy is a number."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert isinstance(data["varimax_mean_accuracy"], (int, float)), \
            f"varimax_mean_accuracy should be a number, got {type(data['varimax_mean_accuracy'])}"

    def test_pca_mean_accuracy_value(self):
        """Verify pca_mean_accuracy matches expected value."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert math.isclose(
            data["pca_mean_accuracy"],
            self.EXPECTED_RESULT["pca_mean_accuracy"],
            rel_tol=self.TOLERANCE
        ), f"pca_mean_accuracy mismatch: expected {self.EXPECTED_RESULT['pca_mean_accuracy']}, got {data['pca_mean_accuracy']}"

    def test_varimax_mean_accuracy_value(self):
        """Verify varimax_mean_accuracy matches expected value."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert math.isclose(
            data["varimax_mean_accuracy"],
            self.EXPECTED_RESULT["varimax_mean_accuracy"],
            rel_tol=self.TOLERANCE
        ), f"varimax_mean_accuracy mismatch: expected {self.EXPECTED_RESULT['varimax_mean_accuracy']}, got {data['varimax_mean_accuracy']}"

    def test_accuracy_values_in_valid_range(self):
        """Verify accuracy values are between 0 and 1."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert 0.0 <= data["pca_mean_accuracy"] <= 1.0, \
            f"pca_mean_accuracy should be between 0 and 1, got {data['pca_mean_accuracy']}"
        assert 0.0 <= data["varimax_mean_accuracy"] <= 1.0, \
            f"varimax_mean_accuracy should be between 0 and 1, got {data['varimax_mean_accuracy']}"

    def test_accuracy_rounded_to_4_decimals(self):
        """Verify accuracy values are rounded to at most 4 decimal places."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        pca_acc = data["pca_mean_accuracy"]
        varimax_acc = data["varimax_mean_accuracy"]

        pca_rounded = round(pca_acc, 4)
        varimax_rounded = round(varimax_acc, 4)

        assert pca_acc == pca_rounded, \
            f"pca_mean_accuracy should be rounded to 4 decimals: {pca_acc} != {pca_rounded}"
        assert varimax_acc == varimax_rounded, \
            f"varimax_mean_accuracy should be rounded to 4 decimals: {varimax_acc} != {varimax_rounded}"

    def test_winner_consistent_with_accuracies(self):
        """Verify winner is consistent with accuracy values (higher accuracy wins, PCA on tie)."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        pca_acc = data["pca_mean_accuracy"]
        varimax_acc = data["varimax_mean_accuracy"]
        winner = data["winner"]

        if varimax_acc > pca_acc:
            expected_winner = "VARIMAX"
        else:
            expected_winner = "PCA"

        assert winner == expected_winner, \
            f"winner inconsistent with accuracies: PCA={pca_acc}, VARIMAX={varimax_acc}, winner={winner}"

    def test_no_extra_fields(self):
        """Verify output contains only the expected fields."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        expected_fields = {"winner", "pca_mean_accuracy", "varimax_mean_accuracy"}
        actual_fields = set(data.keys())
        assert actual_fields == expected_fields, \
            f"Unexpected fields: {actual_fields - expected_fields}"
