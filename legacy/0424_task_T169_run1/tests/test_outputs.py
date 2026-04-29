import json
import math
import os

import pytest


class TestMostConfidentCorrect:
    """Tests for verifying most_confident_correct.json output."""

    OUTPUT_PATH = "/root/output/most_confident_correct.json"

    EXPECTED_RESULT = {
        "row_id": 32,
        "true_species": "setosa",
        "pred_species": "setosa",
        "confidence": 0.9971130007126864,
        "features": {
            "sepal_length": 5.2,
            "sepal_width": 4.1,
            "petal_length": 1.5,
            "petal_width": 0.1
        }
    }
    TOLERANCE = 1e-6

    # =========================================================================
    # Structural Tests
    # =========================================================================

    def test_output_file_exists(self):
        """Verify output file was created at the specified path."""
        assert os.path.exists(self.OUTPUT_PATH), \
            f"Output file not found at {self.OUTPUT_PATH}"

    def test_valid_json(self):
        """Verify output file contains valid JSON."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        assert isinstance(data, dict), "JSON root should be an object"

    # =========================================================================
    # Content Tests - Required Fields
    # =========================================================================

    def test_has_required_top_level_fields(self):
        """Verify all required top-level fields are present."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)

        required_fields = ["row_id", "true_species", "pred_species", "confidence", "features"]
        for field in required_fields:
            assert field in data, f"Missing required field: {field}"

    def test_has_required_feature_fields(self):
        """Verify all required feature fields are present."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)

        required_features = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
        for feature in required_features:
            assert feature in data["features"], f"Missing required feature: {feature}"

    # =========================================================================
    # Content Tests - Data Types
    # =========================================================================

    def test_row_id_is_integer(self):
        """Verify row_id is an integer."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        assert isinstance(data["row_id"], int), \
            f"row_id should be an integer, got {type(data['row_id']).__name__}"

    def test_true_species_is_string(self):
        """Verify true_species is a string."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        assert isinstance(data["true_species"], str), \
            f"true_species should be a string, got {type(data['true_species']).__name__}"

    def test_pred_species_is_string(self):
        """Verify pred_species is a string."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        assert isinstance(data["pred_species"], str), \
            f"pred_species should be a string, got {type(data['pred_species']).__name__}"

    def test_confidence_is_float(self):
        """Verify confidence is a floating-point number (not a string)."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        assert isinstance(data["confidence"], float), \
            f"confidence should be a float, got {type(data['confidence']).__name__}"

    def test_features_is_dict(self):
        """Verify features is a dictionary."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        assert isinstance(data["features"], dict), \
            f"features should be a dict, got {type(data['features']).__name__}"

    def test_feature_values_are_floats(self):
        """Verify all feature values are floats."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)

        for feature, value in data["features"].items():
            assert isinstance(value, (int, float)), \
                f"Feature {feature} should be numeric, got {type(value).__name__}"

    # =========================================================================
    # Content Tests - Value Ranges and Validity
    # =========================================================================

    def test_row_id_non_negative(self):
        """Verify row_id is a valid non-negative integer."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        assert data["row_id"] >= 0, \
            f"row_id should be non-negative, got {data['row_id']}"

    def test_row_id_valid_for_iris_dataset(self):
        """Verify row_id is within valid range for Iris dataset (0-149)."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        assert 0 <= data["row_id"] <= 149, \
            f"row_id should be 0-149 for Iris dataset, got {data['row_id']}"

    def test_confidence_in_valid_range(self):
        """Verify confidence is a probability between 0 and 1."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        assert 0.0 <= data["confidence"] <= 1.0, \
            f"confidence should be in [0, 1], got {data['confidence']}"

    def test_species_is_valid_iris_species(self):
        """Verify species values are valid Iris species names."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)

        valid_species = {"setosa", "versicolor", "virginica"}
        assert data["true_species"] in valid_species, \
            f"true_species '{data['true_species']}' not a valid Iris species"
        assert data["pred_species"] in valid_species, \
            f"pred_species '{data['pred_species']}' not a valid Iris species"

    def test_prediction_is_correct(self):
        """Verify this is a correct prediction (true_species == pred_species)."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        assert data["true_species"] == data["pred_species"], \
            f"Prediction should be correct, but true={data['true_species']} != pred={data['pred_species']}"

    # =========================================================================
    # Value Tests - Exact Values
    # =========================================================================

    def test_row_id_value(self):
        """Verify row_id matches expected value."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        assert data["row_id"] == self.EXPECTED_RESULT["row_id"], \
            f"row_id mismatch: expected {self.EXPECTED_RESULT['row_id']}, got {data['row_id']}"

    def test_true_species_value(self):
        """Verify true_species matches expected value."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        assert data["true_species"] == self.EXPECTED_RESULT["true_species"], \
            f"true_species mismatch: expected {self.EXPECTED_RESULT['true_species']}, got {data['true_species']}"

    def test_pred_species_value(self):
        """Verify pred_species matches expected value."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        assert data["pred_species"] == self.EXPECTED_RESULT["pred_species"], \
            f"pred_species mismatch: expected {self.EXPECTED_RESULT['pred_species']}, got {data['pred_species']}"

    def test_confidence_value(self):
        """Verify confidence matches expected value within tolerance."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        assert math.isclose(data["confidence"], self.EXPECTED_RESULT["confidence"], rel_tol=self.TOLERANCE), \
            f"confidence mismatch: expected {self.EXPECTED_RESULT['confidence']}, got {data['confidence']}"

    def test_sepal_length_value(self):
        """Verify sepal_length matches expected value."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        expected = self.EXPECTED_RESULT["features"]["sepal_length"]
        actual = data["features"]["sepal_length"]
        assert math.isclose(actual, expected, rel_tol=self.TOLERANCE), \
            f"sepal_length mismatch: expected {expected}, got {actual}"

    def test_sepal_width_value(self):
        """Verify sepal_width matches expected value."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        expected = self.EXPECTED_RESULT["features"]["sepal_width"]
        actual = data["features"]["sepal_width"]
        assert math.isclose(actual, expected, rel_tol=self.TOLERANCE), \
            f"sepal_width mismatch: expected {expected}, got {actual}"

    def test_petal_length_value(self):
        """Verify petal_length matches expected value."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        expected = self.EXPECTED_RESULT["features"]["petal_length"]
        actual = data["features"]["petal_length"]
        assert math.isclose(actual, expected, rel_tol=self.TOLERANCE), \
            f"petal_length mismatch: expected {expected}, got {actual}"

    def test_petal_width_value(self):
        """Verify petal_width matches expected value."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        expected = self.EXPECTED_RESULT["features"]["petal_width"]
        actual = data["features"]["petal_width"]
        assert math.isclose(actual, expected, rel_tol=self.TOLERANCE), \
            f"petal_width mismatch: expected {expected}, got {actual}"

    def test_all_features_values(self):
        """Verify all feature values match expected in one test."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)

        for feature, expected in self.EXPECTED_RESULT["features"].items():
            actual = data["features"][feature]
            assert math.isclose(actual, expected, rel_tol=self.TOLERANCE), \
                f"Feature {feature} mismatch: expected {expected}, got {actual}"

    # =========================================================================
    # Content Tests - No Extra Fields
    # =========================================================================

    def test_no_unexpected_top_level_fields(self):
        """Verify no unexpected top-level fields are present."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)

        expected_fields = {"row_id", "true_species", "pred_species", "confidence", "features"}
        actual_fields = set(data.keys())
        unexpected = actual_fields - expected_fields
        assert not unexpected, f"Unexpected fields found: {unexpected}"

    def test_no_unexpected_feature_fields(self):
        """Verify no unexpected feature fields are present."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)

        expected_features = {"sepal_length", "sepal_width", "petal_length", "petal_width"}
        actual_features = set(data["features"].keys())
        unexpected = actual_features - expected_features
        assert not unexpected, f"Unexpected feature fields found: {unexpected}"
