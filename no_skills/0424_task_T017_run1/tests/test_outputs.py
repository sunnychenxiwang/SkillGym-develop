"""Auto-generated pytest tests for verifying task outputs.

These tests verify that the Iris species classifier task produces correct outputs
matching the instruction requirements:
- Pipeline with StandardScaler and LogisticRegression(max_iter=1000, multi_class="auto", random_state=42)
- Train/test split with test_size=0.2, random_state=42, stratify=y
- Output JSON with: label_encoder_classes, test_accuracy, confusion_matrix, classification_report
"""

import json
import math
import os

import numpy as np
import pandas as pd
import pytest
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, StandardScaler


OUTPUT_FILE = "/root/output/iris_logreg_eval.json"
INPUT_FILE = "/root/iris.csv"


class TestIrisLogregEval:
    """Tests for verifying iris_logreg_eval.json output."""

    # Expected values based on the deterministic procedure specified in the task
    EXPECTED_RESULT = {
        "label_encoder_classes": ["setosa", "versicolor", "virginica"],
        "test_accuracy": 0.9333333333333333,
        "confusion_matrix": [
            [10, 0, 0],
            [0, 9, 1],
            [0, 1, 9]
        ],
    }
    TOLERANCE = 1e-9
    NUM_CLASSES = 3
    TEST_SIZE = 30  # 20% of 150 = 30

    # Structural Tests

    def test_output_file_exists(self):
        """Verify output file was created at the expected path."""
        assert os.path.exists(OUTPUT_FILE), f"Output file not found at {OUTPUT_FILE}"

    def test_output_file_not_empty(self):
        """Verify output file is not empty."""
        assert os.path.getsize(OUTPUT_FILE) > 0, "Output file is empty"

    def test_output_is_valid_json(self):
        """Verify output is valid JSON format."""
        with open(OUTPUT_FILE) as f:
            data = json.load(f)
        assert data is not None, "JSON data is None"
        assert isinstance(data, dict), "JSON root should be a dictionary"

    # Schema Tests

    def test_has_required_fields(self):
        """Verify all required fields are present."""
        with open(OUTPUT_FILE) as f:
            data = json.load(f)

        required_fields = ["label_encoder_classes", "test_accuracy", "confusion_matrix", "classification_report"]
        for field in required_fields:
            assert field in data, f"Missing required field: {field}"

    def test_no_extra_top_level_keys(self):
        """Verify no unexpected extra top-level keys are present."""
        with open(OUTPUT_FILE) as f:
            data = json.load(f)

        expected_keys = {"label_encoder_classes", "test_accuracy", "confusion_matrix", "classification_report"}
        actual_keys = set(data.keys())
        extra_keys = actual_keys - expected_keys
        assert len(extra_keys) == 0, f"Unexpected extra top-level keys: {extra_keys}"

    def test_has_exactly_four_top_level_keys(self):
        """Verify output has exactly 4 top-level keys."""
        with open(OUTPUT_FILE) as f:
            data = json.load(f)

        assert len(data.keys()) == 4, f"Expected exactly 4 top-level keys, got {len(data.keys())}"

    # Data Type Tests

    def test_label_encoder_classes_is_list(self):
        """Verify label_encoder_classes is a list."""
        with open(OUTPUT_FILE) as f:
            data = json.load(f)

        assert isinstance(data["label_encoder_classes"], list), (
            f"label_encoder_classes should be list, got {type(data['label_encoder_classes']).__name__}"
        )

    def test_test_accuracy_is_float(self):
        """Verify test_accuracy is a numeric float (not a string)."""
        with open(OUTPUT_FILE) as f:
            data = json.load(f)

        assert isinstance(data["test_accuracy"], (int, float)), (
            f"test_accuracy should be numeric, got {type(data['test_accuracy']).__name__}"
        )
        assert not isinstance(data["test_accuracy"], bool), "test_accuracy should not be boolean"
        assert not isinstance(data["test_accuracy"], str), "test_accuracy must be a float, not a string"

    def test_confusion_matrix_is_nested_list(self):
        """Verify confusion_matrix is a 3x3 nested list."""
        with open(OUTPUT_FILE) as f:
            data = json.load(f)

        cm = data["confusion_matrix"]
        assert isinstance(cm, list), f"confusion_matrix should be list, got {type(cm).__name__}"
        assert len(cm) == self.NUM_CLASSES, f"confusion_matrix should have {self.NUM_CLASSES} rows, got {len(cm)}"
        for i, row in enumerate(cm):
            assert isinstance(row, list), f"confusion_matrix[{i}] should be list"
            assert len(row) == self.NUM_CLASSES, f"confusion_matrix[{i}] should have {self.NUM_CLASSES} elements"

    def test_classification_report_is_dict(self):
        """Verify classification_report is a dictionary."""
        with open(OUTPUT_FILE) as f:
            data = json.load(f)

        assert isinstance(data["classification_report"], dict), (
            f"classification_report should be dict, got {type(data['classification_report']).__name__}"
        )

    # Value Tests - label_encoder_classes

    def test_label_encoder_classes_exact_values(self):
        """Verify label_encoder_classes matches expected ordered list."""
        with open(OUTPUT_FILE) as f:
            data = json.load(f)

        assert data["label_encoder_classes"] == self.EXPECTED_RESULT["label_encoder_classes"], (
            f"label_encoder_classes mismatch.\n"
            f"Expected: {self.EXPECTED_RESULT['label_encoder_classes']}\n"
            f"Actual: {data['label_encoder_classes']}"
        )

    def test_label_encoder_classes_has_three_species(self):
        """Verify label_encoder_classes has exactly 3 species."""
        with open(OUTPUT_FILE) as f:
            data = json.load(f)

        assert len(data["label_encoder_classes"]) == 3, (
            f"label_encoder_classes should have 3 elements, got {len(data['label_encoder_classes'])}"
        )

    def test_label_encoder_classes_contains_valid_species(self):
        """Verify all entries in label_encoder_classes are valid iris species."""
        with open(OUTPUT_FILE) as f:
            data = json.load(f)

        valid_species = {"setosa", "versicolor", "virginica"}
        for species in data["label_encoder_classes"]:
            assert species in valid_species, f"Invalid species: {species}"

    # Value Tests - test_accuracy

    def test_test_accuracy_exact_value(self):
        """Verify test_accuracy matches expected value (28/30 = 0.9333...)."""
        with open(OUTPUT_FILE) as f:
            data = json.load(f)

        assert math.isclose(data["test_accuracy"], self.EXPECTED_RESULT["test_accuracy"], rel_tol=self.TOLERANCE), (
            f"test_accuracy mismatch.\n"
            f"Expected: {self.EXPECTED_RESULT['test_accuracy']}\n"
            f"Actual: {data['test_accuracy']}"
        )

    def test_test_accuracy_in_valid_range(self):
        """Verify test_accuracy is between 0 and 1."""
        with open(OUTPUT_FILE) as f:
            data = json.load(f)

        assert 0.0 <= data["test_accuracy"] <= 1.0, (
            f"test_accuracy should be between 0 and 1, got {data['test_accuracy']}"
        )

    def test_test_accuracy_reasonable_for_iris(self):
        """Verify test_accuracy is reasonable for Iris dataset (>0.8)."""
        with open(OUTPUT_FILE) as f:
            data = json.load(f)

        assert data["test_accuracy"] > 0.8, (
            f"test_accuracy {data['test_accuracy']} is suspiciously low for Iris dataset"
        )

    # Value Tests - confusion_matrix

    def test_confusion_matrix_exact_values(self):
        """Verify confusion_matrix matches expected 3x3 values."""
        with open(OUTPUT_FILE) as f:
            data = json.load(f)

        assert data["confusion_matrix"] == self.EXPECTED_RESULT["confusion_matrix"], (
            f"confusion_matrix mismatch.\n"
            f"Expected:\n{self.EXPECTED_RESULT['confusion_matrix']}\n"
            f"Actual:\n{data['confusion_matrix']}"
        )

    def test_confusion_matrix_contains_integers(self):
        """Verify all confusion_matrix elements are integers."""
        with open(OUTPUT_FILE) as f:
            data = json.load(f)

        cm = data["confusion_matrix"]
        for i, row in enumerate(cm):
            for j, val in enumerate(row):
                assert isinstance(val, int), (
                    f"confusion_matrix[{i}][{j}] should be int, got {type(val).__name__} with value {val}"
                )

    def test_confusion_matrix_non_negative(self):
        """Verify all confusion_matrix elements are non-negative."""
        with open(OUTPUT_FILE) as f:
            data = json.load(f)

        cm = data["confusion_matrix"]
        for i, row in enumerate(cm):
            for j, val in enumerate(row):
                assert val >= 0, f"confusion_matrix[{i}][{j}] = {val} should be non-negative"

    def test_confusion_matrix_sum_equals_test_size(self):
        """Verify confusion_matrix sums to test set size (30 samples)."""
        with open(OUTPUT_FILE) as f:
            data = json.load(f)

        cm = data["confusion_matrix"]
        total = sum(sum(row) for row in cm)
        assert total == self.TEST_SIZE, (
            f"confusion_matrix sum should be {self.TEST_SIZE}, got {total}"
        )

    def test_confusion_matrix_row_sums_equal_10(self):
        """Verify each row sums to 10 (stratified 10 samples per class in test set)."""
        with open(OUTPUT_FILE) as f:
            data = json.load(f)

        cm = data["confusion_matrix"]
        samples_per_class = self.TEST_SIZE // self.NUM_CLASSES  # 10
        expected_classes = self.EXPECTED_RESULT["label_encoder_classes"]
        for i, row in enumerate(cm):
            row_sum = sum(row)
            assert row_sum == samples_per_class, (
                f"Row {i} ({expected_classes[i]}) sum should be {samples_per_class}, got {row_sum}"
            )

    def test_confusion_matrix_diagonal_dominant(self):
        """Verify diagonal elements are dominant (correct predictions > errors)."""
        with open(OUTPUT_FILE) as f:
            data = json.load(f)

        cm = data["confusion_matrix"]
        for i, row in enumerate(cm):
            diagonal_val = row[i]
            off_diagonal_sum = sum(row) - diagonal_val
            assert diagonal_val >= off_diagonal_sum, (
                f"Row {i}: diagonal ({diagonal_val}) should be >= off-diagonal sum ({off_diagonal_sum})"
            )

    # Value Tests - classification_report

    def test_classification_report_has_accuracy_key(self):
        """Verify classification_report contains 'accuracy' key."""
        with open(OUTPUT_FILE) as f:
            data = json.load(f)

        assert "accuracy" in data["classification_report"], (
            "classification_report should contain 'accuracy' key"
        )

    def test_classification_report_accuracy_matches_test_accuracy(self):
        """Verify classification_report accuracy matches test_accuracy."""
        with open(OUTPUT_FILE) as f:
            data = json.load(f)

        report_accuracy = data["classification_report"]["accuracy"]
        test_accuracy = data["test_accuracy"]
        assert math.isclose(report_accuracy, test_accuracy, rel_tol=self.TOLERANCE), (
            f"classification_report accuracy ({report_accuracy}) should match test_accuracy ({test_accuracy})"
        )

    def test_classification_report_has_per_class_metrics(self):
        """Verify classification_report has metrics for each encoded class."""
        with open(OUTPUT_FILE) as f:
            data = json.load(f)

        report = data["classification_report"]
        # Classes are encoded as integers 0, 1, 2 - stored as string keys
        for class_idx in ["0", "1", "2"]:
            assert class_idx in report, f"Missing class {class_idx} in classification_report"
            assert "precision" in report[class_idx], f"Missing precision for class {class_idx}"
            assert "recall" in report[class_idx], f"Missing recall for class {class_idx}"
            assert "f1-score" in report[class_idx], f"Missing f1-score for class {class_idx}"
            assert "support" in report[class_idx], f"Missing support for class {class_idx}"

    def test_classification_report_has_macro_avg(self):
        """Verify classification_report has macro avg."""
        with open(OUTPUT_FILE) as f:
            data = json.load(f)

        assert "macro avg" in data["classification_report"], (
            "classification_report should contain 'macro avg'"
        )

    def test_classification_report_has_weighted_avg(self):
        """Verify classification_report has weighted avg."""
        with open(OUTPUT_FILE) as f:
            data = json.load(f)

        assert "weighted avg" in data["classification_report"], (
            "classification_report should contain 'weighted avg'"
        )

    # Consistency Tests

    def test_accuracy_consistent_with_confusion_matrix(self):
        """Verify test_accuracy equals sum of diagonal / total from confusion matrix."""
        with open(OUTPUT_FILE) as f:
            data = json.load(f)

        cm = data["confusion_matrix"]
        diagonal_sum = sum(cm[i][i] for i in range(self.NUM_CLASSES))
        total = sum(sum(row) for row in cm)
        cm_accuracy = diagonal_sum / total

        assert math.isclose(data["test_accuracy"], cm_accuracy, rel_tol=self.TOLERANCE), (
            f"test_accuracy ({data['test_accuracy']}) should match accuracy from confusion matrix ({cm_accuracy})"
        )

    def test_setosa_perfectly_classified(self):
        """Verify setosa (class 0) is perfectly classified (all diagonal)."""
        with open(OUTPUT_FILE) as f:
            data = json.load(f)

        cm = data["confusion_matrix"]
        setosa_row = cm[0]
        assert setosa_row == [10, 0, 0], (
            f"Setosa row should be [10, 0, 0], got {setosa_row}"
        )


class TestReproducibility:
    """Tests to verify results match recomputation using exact specified procedure."""

    def test_recomputed_results_match(self):
        """Verify output matches results from rerunning the exact procedure."""
        # Load input data
        df = pd.read_csv(INPUT_FILE)
        feature_cols = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
        X = df[feature_cols]

        # Encode labels
        le = LabelEncoder()
        y = le.fit_transform(df["species"])

        # Split with exact parameters
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        # Build pipeline with exact parameters
        pipe = Pipeline([
            ("scaler", StandardScaler()),
            ("model", LogisticRegression(max_iter=1000,  random_state=42))
        ])

        # Fit and predict
        pipe.fit(X_train, y_train)
        y_pred = pipe.predict(X_test)

        # Compute metrics
        expected_accuracy = accuracy_score(y_test, y_pred)
        expected_cm = confusion_matrix(y_test, y_pred, labels=[0, 1, 2]).tolist()
        expected_classes = le.classes_.tolist()

        # Load output and verify
        with open(OUTPUT_FILE) as f:
            data = json.load(f)

        assert data["label_encoder_classes"] == expected_classes, (
            f"label_encoder_classes mismatch with recomputation"
        )
        assert math.isclose(data["test_accuracy"], expected_accuracy, rel_tol=1e-9), (
            f"test_accuracy mismatch: expected {expected_accuracy}, got {data['test_accuracy']}"
        )
        assert data["confusion_matrix"] == expected_cm, (
            f"confusion_matrix mismatch with recomputation"
        )


class TestInputFileIntegrity:
    """Tests to verify the input file matches expected structure."""

    def test_input_file_exists(self):
        """Verify input file exists."""
        assert os.path.exists(INPUT_FILE), f"Input file not found: {INPUT_FILE}"

    def test_input_has_expected_columns(self):
        """Verify input CSV has the expected columns."""
        df = pd.read_csv(INPUT_FILE)
        expected_columns = ["sepal_length", "sepal_width", "petal_length", "petal_width", "species"]
        assert list(df.columns) == expected_columns, (
            f"Expected columns {expected_columns}, got {list(df.columns)}"
        )

    def test_input_has_150_rows(self):
        """Verify input has exactly 150 rows (standard Iris dataset)."""
        df = pd.read_csv(INPUT_FILE)
        assert len(df) == 150, f"Expected 150 rows, got {len(df)}"

    def test_input_has_three_species(self):
        """Verify input has exactly 3 species."""
        df = pd.read_csv(INPUT_FILE)
        species = df["species"].unique()
        assert len(species) == 3, f"Expected 3 species, got {len(species)}"
        expected_species = {"setosa", "versicolor", "virginica"}
        assert set(species) == expected_species, (
            f"Expected species {expected_species}, got {set(species)}"
        )

    def test_input_has_50_samples_per_class(self):
        """Verify input has exactly 50 samples per class."""
        df = pd.read_csv(INPUT_FILE)
        class_counts = df["species"].value_counts()
        for species in ["setosa", "versicolor", "virginica"]:
            assert class_counts[species] == 50, (
                f"Expected 50 samples for {species}, got {class_counts[species]}"
            )


class TestDataIntegrity:
    """Tests to verify data integrity of the output."""

    def test_output_can_be_reloaded(self):
        """Verify output file can be loaded multiple times without error."""
        for _ in range(3):
            with open(OUTPUT_FILE) as f:
                data = json.load(f)
            assert data is not None

    def test_json_roundtrip_preserves_data(self):
        """Verify JSON can be loaded, dumped, and loaded again without loss."""
        with open(OUTPUT_FILE) as f:
            data1 = json.load(f)

        json_str = json.dumps(data1)
        data2 = json.loads(json_str)

        assert data1 == data2, "JSON roundtrip changed the data"
