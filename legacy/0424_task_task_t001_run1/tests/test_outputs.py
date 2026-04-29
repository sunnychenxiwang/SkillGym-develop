import json
import math
import os

import pytest


class TestQuadraticCommonJson:
    """Tests for verifying quadratic_common.json output."""

    OUTPUT_FILE = "/root/output/quadratic_common.json"

    EXPECTED_RESULT = {
        "common_expr": r"x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}",
        "roots_real_proved": True,
        "signature": 6000,
    }

    TOLERANCE = 0.001

    def test_quadratic_common_json_exists(self):
        """Verify output file was created at the specified path."""
        assert os.path.exists(self.OUTPUT_FILE), \
            f"Output file not found: {self.OUTPUT_FILE}"

    def test_quadratic_common_json_valid_json(self):
        """Verify output is valid JSON format."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert isinstance(data, dict), "Output should be a JSON object"

    def test_quadratic_common_json_has_required_fields(self):
        """Verify all required fields are present."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        assert "common_expr" in data, "Missing required field: common_expr"
        assert "roots_real_proved" in data, "Missing required field: roots_real_proved"
        assert "signature" in data, "Missing required field: signature"

    def test_quadratic_common_json_no_extra_keys(self):
        """Verify no extra keys beyond the required schema."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        expected_keys = {"common_expr", "roots_real_proved", "signature"}
        actual_keys = set(data.keys())

        assert actual_keys == expected_keys, \
            f"Expected keys {expected_keys}, got {actual_keys}"

    def test_quadratic_common_json_field_types(self):
        """Verify field data types are correct."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        assert isinstance(data["common_expr"], str), \
            f"common_expr should be a string, got {type(data['common_expr'])}"
        assert isinstance(data["roots_real_proved"], bool), \
            f"roots_real_proved should be a boolean, got {type(data['roots_real_proved'])}"
        assert isinstance(data["signature"], int), \
            f"signature should be an integer, got {type(data['signature'])}"

    def test_quadratic_common_json_common_expr_value(self):
        """Verify common_expr contains the normalized quadratic formula."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        assert data["common_expr"] == self.EXPECTED_RESULT["common_expr"], \
            f"common_expr mismatch: expected '{self.EXPECTED_RESULT['common_expr']}', " \
            f"got '{data['common_expr']}'"

    def test_quadratic_common_json_roots_real_proved_value(self):
        """Verify roots_real_proved is true (Z3 established the theorem)."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        assert data["roots_real_proved"] == self.EXPECTED_RESULT["roots_real_proved"], \
            f"roots_real_proved mismatch: expected {self.EXPECTED_RESULT['roots_real_proved']}, " \
            f"got {data['roots_real_proved']}"

    def test_quadratic_common_json_signature_value(self):
        """Verify signature is correctly computed as round(product_of_roots * 1000)."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        assert data["signature"] == self.EXPECTED_RESULT["signature"], \
            f"signature mismatch: expected {self.EXPECTED_RESULT['signature']}, " \
            f"got {data['signature']}"

    def test_quadratic_common_json_common_expr_is_quadratic_formula(self):
        """Verify common_expr represents the quadratic formula structure."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        expr = data["common_expr"]
        assert "frac" in expr, "Expression should contain fraction (frac)"
        assert "sqrt" in expr, "Expression should contain square root (sqrt)"
        assert "pm" in expr, "Expression should contain plus-minus (pm)"
        assert "2a" in expr, "Expression should contain denominator 2a"
        assert "-b" in expr, "Expression should contain -b"
        assert "4ac" in expr, "Expression should contain 4ac in discriminant"

    def test_quadratic_common_json_signature_is_positive(self):
        """Verify signature is a positive integer (product of roots with a=1,b=5,c=6)."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        assert data["signature"] > 0, \
            f"signature should be positive, got {data['signature']}"

    def test_quadratic_common_json_signature_is_integer_multiple_of_1000(self):
        """Verify signature computation: product of roots (-2 * -3 = 6) times 1000."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        expected_product = 6
        expected_signature = expected_product * 1000

        assert data["signature"] == expected_signature, \
            f"signature should be {expected_signature} (product {expected_product} * 1000), " \
            f"got {data['signature']}"
