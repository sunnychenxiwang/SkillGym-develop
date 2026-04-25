import json
import os

import pytest


class TestSharedMathFingerprint:
    """Tests for verifying shared_math_fingerprint.json output."""

    OUTPUT_PATH = "/root/output/shared_math_fingerprint.json"

    EXPECTED_RESULT = {
        "normalized_expression": "x = \\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}",
        "simplified_expression": "(-b + sqrt(-4*a*c + b**2))/(2*a)",
        "sum_distinct_integer_constants": -3,
    }

    REQUIRED_FIELDS = [
        "normalized_expression",
        "simplified_expression",
        "sum_distinct_integer_constants",
    ]

    def test_file_exists(self):
        """Verify output file was created at the specified path."""
        assert os.path.exists(self.OUTPUT_PATH), (
            f"Output file not found at {self.OUTPUT_PATH}"
        )

    def test_valid_json(self):
        """Verify output is valid JSON."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        assert isinstance(data, dict), "JSON root should be an object"

    def test_has_required_fields(self):
        """Verify all required fields are present."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        for field in self.REQUIRED_FIELDS:
            assert field in data, f"Missing required field: {field}"

    def test_no_extra_fields(self):
        """Verify no unexpected fields are present."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        expected_keys = set(self.REQUIRED_FIELDS)
        actual_keys = set(data.keys())
        extra_keys = actual_keys - expected_keys
        assert not extra_keys, f"Unexpected fields found: {extra_keys}"

    def test_field_types(self):
        """Verify field data types are correct."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)

        assert isinstance(data["normalized_expression"], str), (
            "normalized_expression should be a string"
        )
        assert isinstance(data["simplified_expression"], str), (
            "simplified_expression should be a string"
        )
        assert isinstance(data["sum_distinct_integer_constants"], int), (
            "sum_distinct_integer_constants should be an integer"
        )

    def test_normalized_expression_value(self):
        """Verify normalized_expression matches expected value."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)

        expected = self.EXPECTED_RESULT["normalized_expression"]
        actual = data["normalized_expression"]
        assert actual == expected, (
            f"normalized_expression mismatch: expected {repr(expected)}, got {repr(actual)}"
        )

    def test_simplified_expression_value(self):
        """Verify simplified_expression matches expected value."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)

        expected = self.EXPECTED_RESULT["simplified_expression"]
        actual = data["simplified_expression"]
        assert actual == expected, (
            f"simplified_expression mismatch: expected {repr(expected)}, got {repr(actual)}"
        )

    def test_sum_distinct_integer_constants_value(self):
        """Verify sum_distinct_integer_constants matches expected value."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)

        expected = self.EXPECTED_RESULT["sum_distinct_integer_constants"]
        actual = data["sum_distinct_integer_constants"]
        assert actual == expected, (
            f"sum_distinct_integer_constants mismatch: expected {expected}, got {actual}"
        )

    def test_normalized_expression_is_latex(self):
        """Verify normalized_expression contains valid LaTeX math notation."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)

        expr = data["normalized_expression"]
        assert "\\frac" in expr, "LaTeX expression should contain \\frac"
        assert "\\sqrt" in expr, "LaTeX expression should contain \\sqrt"

    def test_simplified_expression_is_sympy_format(self):
        """Verify simplified_expression is in SymPy string format."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)

        expr = data["simplified_expression"]
        assert "sqrt" in expr, "SymPy expression should contain sqrt function"
        assert "**" in expr or "*" in expr, "SymPy expression should use Python operators"

    def test_key_order(self):
        """Verify JSON keys are in the exact order specified."""
        with open(self.OUTPUT_PATH) as f:
            content = f.read()
            data = json.loads(content)

        expected_order = [
            "normalized_expression",
            "simplified_expression",
            "sum_distinct_integer_constants",
        ]
        actual_order = list(data.keys())
        assert actual_order == expected_order, (
            f"Key order mismatch: expected {expected_order}, got {actual_order}"
        )

    def test_file_is_not_empty(self):
        """Verify output file is not empty."""
        file_size = os.path.getsize(self.OUTPUT_PATH)
        assert file_size > 0, "Output file should not be empty"

    def test_json_roundtrip(self):
        """Verify JSON can be loaded and dumped without data loss."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)

        roundtrip = json.loads(json.dumps(data))
        assert data == roundtrip, "JSON roundtrip should preserve data"
