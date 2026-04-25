import json
import math
import os

import pytest


class TestTopReplicableGene:
    """Tests for verifying the cross-dataset gene signature output."""

    OUTPUT_FILE = "/root/output/top_replicable_gene.json"

    EXPECTED_RESULT = {
        "gene": "CDC6",
        "replicability_score": 0.40472693951888583,
        "shared_gene_count": 11506,
    }
    TOLERANCE = 1e-6

    # ==================== Structural Tests ====================

    def test_output_file_exists(self):
        """Verify the output JSON file was created."""
        assert os.path.exists(self.OUTPUT_FILE), \
            f"Output file not found: {self.OUTPUT_FILE}"

    def test_output_file_valid_json(self):
        """Verify output file contains valid JSON."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert isinstance(data, dict), "Output JSON should be an object/dictionary"

    # ==================== Content Tests ====================

    def test_has_gene_field(self):
        """Verify 'gene' field is present."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert "gene" in data, "Missing required field: gene"

    def test_has_replicability_score_field(self):
        """Verify 'replicability_score' field is present."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert "replicability_score" in data, "Missing required field: replicability_score"

    def test_has_shared_gene_count_field(self):
        """Verify 'shared_gene_count' field is present."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert "shared_gene_count" in data, "Missing required field: shared_gene_count"

    def test_gene_is_string(self):
        """Verify 'gene' field is a string."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert isinstance(data["gene"], str), \
            f"'gene' should be a string, got {type(data['gene']).__name__}"

    def test_replicability_score_is_float(self):
        """Verify 'replicability_score' field is a float or int."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert isinstance(data["replicability_score"], (int, float)), \
            f"'replicability_score' should be numeric, got {type(data['replicability_score']).__name__}"

    def test_shared_gene_count_is_integer(self):
        """Verify 'shared_gene_count' field is an integer."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert isinstance(data["shared_gene_count"], int), \
            f"'shared_gene_count' should be an integer, got {type(data['shared_gene_count']).__name__}"

    def test_gene_is_nonempty(self):
        """Verify 'gene' field is non-empty."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert len(data["gene"]) > 0, "'gene' should be a non-empty string"

    def test_shared_gene_count_positive(self):
        """Verify 'shared_gene_count' is a positive integer."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert data["shared_gene_count"] > 0, \
            f"'shared_gene_count' should be positive, got {data['shared_gene_count']}"

    # ==================== Value Tests ====================

    def test_gene_value_correct(self):
        """Verify the selected gene matches expected value."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert data["gene"] == self.EXPECTED_RESULT["gene"], \
            f"gene mismatch: expected '{self.EXPECTED_RESULT['gene']}', got '{data['gene']}'"

    def test_replicability_score_value_correct(self):
        """Verify replicability score matches expected value within tolerance."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert math.isclose(
            data["replicability_score"],
            self.EXPECTED_RESULT["replicability_score"],
            rel_tol=self.TOLERANCE
        ), (
            f"replicability_score mismatch: expected {self.EXPECTED_RESULT['replicability_score']}, "
            f"got {data['replicability_score']}"
        )

    def test_shared_gene_count_value_correct(self):
        """Verify shared gene count matches expected value."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert data["shared_gene_count"] == self.EXPECTED_RESULT["shared_gene_count"], \
            f"shared_gene_count mismatch: expected {self.EXPECTED_RESULT['shared_gene_count']}, got {data['shared_gene_count']}"

    def test_only_expected_fields_present(self):
        """Verify JSON contains exactly the expected fields (no extra fields)."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        expected_fields = {"gene", "replicability_score", "shared_gene_count"}
        actual_fields = set(data.keys())
        assert actual_fields == expected_fields, \
            f"Unexpected fields in output. Expected: {expected_fields}, Got: {actual_fields}"
