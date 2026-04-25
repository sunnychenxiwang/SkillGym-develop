import json
import math
import os

import pytest


class TestBestFloodModel:
    """Tests for verifying best_flood_model.json output."""

    OUTPUT_FILE = "/root/output/best_flood_model.json"

    EXPECTED_RESULT = {
        "rocket_test_accuracy": 0.8400407539480387,
        "logit_test_accuracy": 0.9898115129903209,
        "best_model": "logit",
        "n_train_samples": 4578,
        "n_test_samples": 1963,
    }
    TOLERANCE = 1e-6

    # Structural Tests

    def test_best_flood_model_exists(self):
        """Verify output file was created."""
        assert os.path.exists(self.OUTPUT_FILE), f"Output file not found: {self.OUTPUT_FILE}"

    def test_best_flood_model_valid_json(self):
        """Verify output is valid JSON."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert isinstance(data, dict), "Output should be a JSON object"

    def test_best_flood_model_no_extra_keys(self):
        """Verify output contains exactly the required keys and no extras."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        expected_keys = {"rocket_test_accuracy", "logit_test_accuracy", "best_model", "n_train_samples", "n_test_samples"}
        actual_keys = set(data.keys())
        assert actual_keys == expected_keys, f"Keys mismatch: expected {expected_keys}, got {actual_keys}"

    # Content Tests - Required Fields

    def test_has_rocket_test_accuracy(self):
        """Verify rocket_test_accuracy field is present."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert "rocket_test_accuracy" in data, "Missing required field: rocket_test_accuracy"

    def test_has_logit_test_accuracy(self):
        """Verify logit_test_accuracy field is present."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert "logit_test_accuracy" in data, "Missing required field: logit_test_accuracy"

    def test_has_best_model(self):
        """Verify best_model field is present."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert "best_model" in data, "Missing required field: best_model"

    def test_has_n_train_samples(self):
        """Verify n_train_samples field is present."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert "n_train_samples" in data, "Missing required field: n_train_samples"

    def test_has_n_test_samples(self):
        """Verify n_test_samples field is present."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert "n_test_samples" in data, "Missing required field: n_test_samples"

    # Content Tests - Data Types

    def test_rocket_test_accuracy_is_float(self):
        """Verify rocket_test_accuracy is a float."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert isinstance(data["rocket_test_accuracy"], float), "rocket_test_accuracy should be a float"

    def test_logit_test_accuracy_is_float(self):
        """Verify logit_test_accuracy is a float."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert isinstance(data["logit_test_accuracy"], float), "logit_test_accuracy should be a float"

    def test_best_model_is_string(self):
        """Verify best_model is a string."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert isinstance(data["best_model"], str), "best_model should be a string"

    def test_n_train_samples_is_int(self):
        """Verify n_train_samples is an integer."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert isinstance(data["n_train_samples"], int), "n_train_samples should be an integer"

    def test_n_test_samples_is_int(self):
        """Verify n_test_samples is an integer."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert isinstance(data["n_test_samples"], int), "n_test_samples should be an integer"

    # Content Tests - Value Constraints

    def test_best_model_valid_value(self):
        """Verify best_model is either 'rocket' or 'logit'."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert data["best_model"] in ("rocket", "logit"), \
            f"best_model must be 'rocket' or 'logit', got '{data['best_model']}'"

    def test_rocket_accuracy_in_range(self):
        """Verify rocket_test_accuracy is between 0 and 1."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        acc = data["rocket_test_accuracy"]
        assert 0.0 <= acc <= 1.0, f"rocket_test_accuracy should be between 0 and 1, got {acc}"

    def test_logit_accuracy_in_range(self):
        """Verify logit_test_accuracy is between 0 and 1."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        acc = data["logit_test_accuracy"]
        assert 0.0 <= acc <= 1.0, f"logit_test_accuracy should be between 0 and 1, got {acc}"

    def test_n_train_samples_positive(self):
        """Verify n_train_samples is a positive integer."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert data["n_train_samples"] > 0, "n_train_samples should be positive"

    def test_n_test_samples_positive(self):
        """Verify n_test_samples is a positive integer."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert data["n_test_samples"] > 0, "n_test_samples should be positive"

    # Value Tests - Exact Values

    def test_rocket_test_accuracy_value(self):
        """Verify rocket_test_accuracy matches expected value."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        expected = self.EXPECTED_RESULT["rocket_test_accuracy"]
        actual = data["rocket_test_accuracy"]
        assert math.isclose(actual, expected, rel_tol=self.TOLERANCE), \
            f"rocket_test_accuracy mismatch: expected {expected}, got {actual}"

    def test_logit_test_accuracy_value(self):
        """Verify logit_test_accuracy matches expected value."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        expected = self.EXPECTED_RESULT["logit_test_accuracy"]
        actual = data["logit_test_accuracy"]
        assert math.isclose(actual, expected, rel_tol=self.TOLERANCE), \
            f"logit_test_accuracy mismatch: expected {expected}, got {actual}"

    def test_best_model_value(self):
        """Verify best_model matches expected value."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        expected = self.EXPECTED_RESULT["best_model"]
        actual = data["best_model"]
        assert actual == expected, f"best_model mismatch: expected '{expected}', got '{actual}'"

    def test_n_train_samples_value(self):
        """Verify n_train_samples matches expected value."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        expected = self.EXPECTED_RESULT["n_train_samples"]
        actual = data["n_train_samples"]
        assert actual == expected, f"n_train_samples mismatch: expected {expected}, got {actual}"

    def test_n_test_samples_value(self):
        """Verify n_test_samples matches expected value."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        expected = self.EXPECTED_RESULT["n_test_samples"]
        actual = data["n_test_samples"]
        assert actual == expected, f"n_test_samples mismatch: expected {expected}, got {actual}"

    # Value Tests - Model Selection Logic

    def test_best_model_selection_logic(self):
        """Verify best_model is correctly selected based on accuracy comparison."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        rocket_acc = data["rocket_test_accuracy"]
        logit_acc = data["logit_test_accuracy"]
        best_model = data["best_model"]

        if rocket_acc > logit_acc + 1e-12:
            expected_best = "rocket"
        else:
            expected_best = "logit"

        assert best_model == expected_best, \
            f"best_model selection incorrect: rocket_acc={rocket_acc}, logit_acc={logit_acc}, " \
            f"expected '{expected_best}', got '{best_model}'"
