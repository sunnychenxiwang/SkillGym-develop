import json
import math
import os

import pytest


class TestMostConsistentHVG:
    """Tests for verifying most_consistent_hvg.json output."""

    OUTPUT_PATH = "/root/output/most_consistent_hvg.json"

    EXPECTED_RESULT = {
        "gene": "PPBP",
        "intersection_size": 339,
        "mean_dispersions_norm": 10.100319226582846,
        "std_dispersions_norm": 6.480325220061221,
        "top100_fraction": 1.0,
        "predicted_probability": 0.9999999999998781,
    }

    TOLERANCE = 1e-6

    REQUIRED_FIELDS = [
        "gene",
        "intersection_size",
        "mean_dispersions_norm",
        "std_dispersions_norm",
        "top100_fraction",
        "predicted_probability",
    ]

    # --- Structural Tests ---

    def test_most_consistent_hvg_exists(self):
        """Verify most_consistent_hvg.json file was created."""
        assert os.path.exists(self.OUTPUT_PATH), f"Output file not found: {self.OUTPUT_PATH}"

    def test_most_consistent_hvg_valid_json(self):
        """Verify output is valid JSON."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        assert isinstance(data, dict), "Output should be a JSON object"

    def test_most_consistent_hvg_no_extra_keys(self):
        """Verify no extra keys beyond the required schema."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        extra_keys = set(data.keys()) - set(self.REQUIRED_FIELDS)
        assert len(extra_keys) == 0, f"Extra keys found: {extra_keys}"

    # --- Content Tests ---

    def test_has_required_fields(self):
        """Verify all required fields are present."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        for field in self.REQUIRED_FIELDS:
            assert field in data, f"Missing required field: {field}"

    def test_field_types(self):
        """Verify all fields have correct data types."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)

        assert isinstance(data["gene"], str), "gene should be a string"
        assert isinstance(data["intersection_size"], int), "intersection_size should be an integer"
        assert isinstance(data["mean_dispersions_norm"], (int, float)), "mean_dispersions_norm should be a number"
        assert isinstance(data["std_dispersions_norm"], (int, float)), "std_dispersions_norm should be a number"
        assert isinstance(data["top100_fraction"], (int, float)), "top100_fraction should be a number"
        assert isinstance(data["predicted_probability"], (int, float)), "predicted_probability should be a number"

    def test_gene_is_valid_symbol(self):
        """Verify gene is a non-empty string."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        assert len(data["gene"]) > 0, "gene should be a non-empty string"

    def test_intersection_size_positive(self):
        """Verify intersection_size is positive."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        assert data["intersection_size"] > 0, "intersection_size should be positive"

    def test_top100_fraction_in_range(self):
        """Verify top100_fraction is between 0 and 1."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        assert 0.0 <= data["top100_fraction"] <= 1.0, "top100_fraction should be between 0 and 1"

    def test_predicted_probability_in_range(self):
        """Verify predicted_probability is between 0 and 1."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        assert 0.0 <= data["predicted_probability"] <= 1.0, "predicted_probability should be between 0 and 1"

    def test_dispersions_norm_positive(self):
        """Verify mean_dispersions_norm is positive (expected for HVGs)."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        assert data["mean_dispersions_norm"] > 0, "mean_dispersions_norm should be positive"

    def test_std_dispersions_norm_non_negative(self):
        """Verify std_dispersions_norm is non-negative."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        assert data["std_dispersions_norm"] >= 0, "std_dispersions_norm should be non-negative"

    # --- Value Tests ---

    def test_gene_value(self):
        """Verify gene matches expected value."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        assert data["gene"] == self.EXPECTED_RESULT["gene"], \
            f"gene mismatch: expected {self.EXPECTED_RESULT['gene']}, got {data['gene']}"

    def test_intersection_size_value(self):
        """Verify intersection_size matches expected value."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        assert data["intersection_size"] == self.EXPECTED_RESULT["intersection_size"], \
            f"intersection_size mismatch: expected {self.EXPECTED_RESULT['intersection_size']}, got {data['intersection_size']}"

    def test_mean_dispersions_norm_value(self):
        """Verify mean_dispersions_norm matches expected value within tolerance."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        assert math.isclose(
            data["mean_dispersions_norm"],
            self.EXPECTED_RESULT["mean_dispersions_norm"],
            rel_tol=self.TOLERANCE
        ), f"mean_dispersions_norm mismatch: expected {self.EXPECTED_RESULT['mean_dispersions_norm']}, got {data['mean_dispersions_norm']}"

    def test_std_dispersions_norm_value(self):
        """Verify std_dispersions_norm matches expected value within tolerance."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        assert math.isclose(
            data["std_dispersions_norm"],
            self.EXPECTED_RESULT["std_dispersions_norm"],
            rel_tol=self.TOLERANCE
        ), f"std_dispersions_norm mismatch: expected {self.EXPECTED_RESULT['std_dispersions_norm']}, got {data['std_dispersions_norm']}"

    def test_top100_fraction_value(self):
        """Verify top100_fraction matches expected value within tolerance."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        assert math.isclose(
            data["top100_fraction"],
            self.EXPECTED_RESULT["top100_fraction"],
            rel_tol=self.TOLERANCE
        ), f"top100_fraction mismatch: expected {self.EXPECTED_RESULT['top100_fraction']}, got {data['top100_fraction']}"

    def test_predicted_probability_value(self):
        """Verify predicted_probability matches expected value within tolerance."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        assert math.isclose(
            data["predicted_probability"],
            self.EXPECTED_RESULT["predicted_probability"],
            rel_tol=self.TOLERANCE
        ), f"predicted_probability mismatch: expected {self.EXPECTED_RESULT['predicted_probability']}, got {data['predicted_probability']}"

    def test_numeric_values_are_real_numbers(self):
        """Verify all numeric values are real numbers (not strings or null)."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)

        numeric_fields = [
            "intersection_size",
            "mean_dispersions_norm",
            "std_dispersions_norm",
            "top100_fraction",
            "predicted_probability",
        ]

        for field in numeric_fields:
            value = data[field]
            assert value is not None, f"{field} should not be null"
            assert not isinstance(value, str), f"{field} should not be a string"
            assert not math.isnan(value) if isinstance(value, float) else True, f"{field} should not be NaN"
            assert not math.isinf(value) if isinstance(value, float) else True, f"{field} should not be infinite"
