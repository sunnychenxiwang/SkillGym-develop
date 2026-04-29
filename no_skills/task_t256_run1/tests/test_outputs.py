"""Auto-generated expectation tests for task verification.

These tests verify that the task execution produces correct outputs
based on the instruction requirements for identifying the most common
MITRE ATT&CK technique across three cyber threat PDF reports.
"""

import json
import os
import re
from pathlib import Path

import pytest


# Expected paths
OUTPUT_FILE = "/root/most_common_attack_technique.json"
INPUT_DIR = "/root/input"

# Expected document names (exact filenames as specified in the schema)
EXPECTED_DOCUMENTS = [
    "ASD-Cyber-Threat-Report-2024.pdf",
    "RedCanary-Threat-Detection-Report-2024.pdf",
    "Secureworks-State-of-the-Threat-Report-2024.pdf",
]

# ATT&CK technique ID regex pattern
ATTACK_TECHNIQUE_PATTERN = r"^T\d{4}(?:\.\d{3})?$"


class TestOutputFileExists:
    """Tests for verifying output file existence."""

    def test_output_file_exists(self):
        """Verify the output JSON file was created at the expected path."""
        assert os.path.exists(OUTPUT_FILE), (
            f"Output file not found at {OUTPUT_FILE}. "
            "The task must create this file."
        )

    def test_output_file_is_not_empty(self):
        """Verify the output file is not empty."""
        assert os.path.exists(OUTPUT_FILE), f"Output file not found at {OUTPUT_FILE}"
        file_size = os.path.getsize(OUTPUT_FILE)
        assert file_size > 0, "Output file is empty"


class TestOutputJsonValidity:
    """Tests for verifying JSON format validity."""

    def test_output_is_valid_json(self):
        """Verify output is valid JSON format."""
        assert os.path.exists(OUTPUT_FILE), f"Output file not found at {OUTPUT_FILE}"
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                pytest.fail(f"Output file is not valid JSON: {e}")
        assert data is not None, "JSON parsed to None"

    def test_output_is_json_object(self):
        """Verify output is a JSON object (dict), not an array or primitive."""
        assert os.path.exists(OUTPUT_FILE), f"Output file not found at {OUTPUT_FILE}"
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert isinstance(data, dict), (
            f"Output must be a JSON object, got {type(data).__name__}"
        )


class TestRequiredKeys:
    """Tests for verifying all required keys are present."""

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        assert os.path.exists(OUTPUT_FILE), f"Output file not found at {OUTPUT_FILE}"
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def test_has_technique_id_key(self, output_data):
        """Verify 'technique_id' key is present."""
        assert "technique_id" in output_data, (
            "Required key 'technique_id' is missing from output"
        )

    def test_has_doc_count_key(self, output_data):
        """Verify 'doc_count' key is present."""
        assert "doc_count" in output_data, (
            "Required key 'doc_count' is missing from output"
        )

    def test_has_total_mentions_key(self, output_data):
        """Verify 'total_mentions' key is present."""
        assert "total_mentions" in output_data, (
            "Required key 'total_mentions' is missing from output"
        )

    def test_has_per_document_mentions_key(self, output_data):
        """Verify 'per_document_mentions' key is present."""
        assert "per_document_mentions" in output_data, (
            "Required key 'per_document_mentions' is missing from output"
        )


class TestTechniqueIdFormat:
    """Tests for verifying technique_id format."""

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        assert os.path.exists(OUTPUT_FILE), f"Output file not found at {OUTPUT_FILE}"
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def test_technique_id_is_string(self, output_data):
        """Verify technique_id is a string."""
        technique_id = output_data.get("technique_id")
        assert isinstance(technique_id, str), (
            f"technique_id must be a string, got {type(technique_id).__name__}"
        )

    def test_technique_id_matches_attack_format(self, output_data):
        """Verify technique_id matches MITRE ATT&CK format (T#### or T####.###)."""
        technique_id = output_data.get("technique_id")
        assert technique_id is not None, "technique_id is None"
        assert re.match(ATTACK_TECHNIQUE_PATTERN, technique_id), (
            f"technique_id '{technique_id}' does not match expected ATT&CK format "
            f"(T#### or T####.###). Pattern: {ATTACK_TECHNIQUE_PATTERN}"
        )

    def test_technique_id_starts_with_t(self, output_data):
        """Verify technique_id starts with 'T'."""
        technique_id = output_data.get("technique_id", "")
        assert technique_id.startswith("T"), (
            f"technique_id must start with 'T', got '{technique_id}'"
        )


class TestDocCountConstraints:
    """Tests for verifying doc_count constraints."""

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        assert os.path.exists(OUTPUT_FILE), f"Output file not found at {OUTPUT_FILE}"
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def test_doc_count_is_integer(self, output_data):
        """Verify doc_count is an integer."""
        doc_count = output_data.get("doc_count")
        assert isinstance(doc_count, int), (
            f"doc_count must be an integer, got {type(doc_count).__name__}"
        )

    def test_doc_count_minimum(self, output_data):
        """Verify doc_count is at least 1 (technique must appear in at least one doc)."""
        doc_count = output_data.get("doc_count")
        assert doc_count >= 1, (
            f"doc_count must be at least 1, got {doc_count}"
        )

    def test_doc_count_maximum(self, output_data):
        """Verify doc_count is at most 3 (there are only 3 documents)."""
        doc_count = output_data.get("doc_count")
        assert doc_count <= 3, (
            f"doc_count cannot exceed 3 (number of input documents), got {doc_count}"
        )


class TestTotalMentionsConstraints:
    """Tests for verifying total_mentions constraints."""

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        assert os.path.exists(OUTPUT_FILE), f"Output file not found at {OUTPUT_FILE}"
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def test_total_mentions_is_integer(self, output_data):
        """Verify total_mentions is an integer."""
        total_mentions = output_data.get("total_mentions")
        assert isinstance(total_mentions, int), (
            f"total_mentions must be an integer, got {type(total_mentions).__name__}"
        )

    def test_total_mentions_positive(self, output_data):
        """Verify total_mentions is positive (at least 1)."""
        total_mentions = output_data.get("total_mentions")
        assert total_mentions >= 1, (
            f"total_mentions must be at least 1, got {total_mentions}"
        )

    def test_total_mentions_at_least_doc_count(self, output_data):
        """Verify total_mentions >= doc_count (at least one mention per document)."""
        total_mentions = output_data.get("total_mentions", 0)
        doc_count = output_data.get("doc_count", 0)
        assert total_mentions >= doc_count, (
            f"total_mentions ({total_mentions}) must be >= doc_count ({doc_count})"
        )


class TestPerDocumentMentions:
    """Tests for verifying per_document_mentions structure and values."""

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        assert os.path.exists(OUTPUT_FILE), f"Output file not found at {OUTPUT_FILE}"
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def test_per_document_mentions_is_dict(self, output_data):
        """Verify per_document_mentions is a dictionary."""
        per_doc = output_data.get("per_document_mentions")
        assert isinstance(per_doc, dict), (
            f"per_document_mentions must be a dict, got {type(per_doc).__name__}"
        )

    def test_per_document_mentions_has_all_documents(self, output_data):
        """Verify per_document_mentions contains all three expected document names."""
        per_doc = output_data.get("per_document_mentions", {})
        for doc_name in EXPECTED_DOCUMENTS:
            assert doc_name in per_doc, (
                f"per_document_mentions is missing required document: '{doc_name}'"
            )

    def test_per_document_mentions_has_only_expected_documents(self, output_data):
        """Verify per_document_mentions contains only the expected document names."""
        per_doc = output_data.get("per_document_mentions", {})
        unexpected_docs = set(per_doc.keys()) - set(EXPECTED_DOCUMENTS)
        assert len(unexpected_docs) == 0, (
            f"per_document_mentions contains unexpected documents: {unexpected_docs}"
        )

    def test_per_document_mentions_values_are_integers(self, output_data):
        """Verify all per_document_mentions values are integers."""
        per_doc = output_data.get("per_document_mentions", {})
        for doc_name, count in per_doc.items():
            assert isinstance(count, int), (
                f"per_document_mentions['{doc_name}'] must be an integer, "
                f"got {type(count).__name__}"
            )

    def test_per_document_mentions_values_non_negative(self, output_data):
        """Verify all per_document_mentions values are non-negative."""
        per_doc = output_data.get("per_document_mentions", {})
        for doc_name, count in per_doc.items():
            assert count >= 0, (
                f"per_document_mentions['{doc_name}'] must be >= 0, got {count}"
            )


class TestDataConsistency:
    """Tests for verifying internal data consistency."""

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        assert os.path.exists(OUTPUT_FILE), f"Output file not found at {OUTPUT_FILE}"
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def test_doc_count_matches_documents_with_mentions(self, output_data):
        """Verify doc_count equals the number of documents with mentions > 0."""
        per_doc = output_data.get("per_document_mentions", {})
        doc_count = output_data.get("doc_count", 0)

        docs_with_mentions = sum(1 for count in per_doc.values() if count > 0)
        assert doc_count == docs_with_mentions, (
            f"doc_count ({doc_count}) does not match number of documents with "
            f"mentions > 0 ({docs_with_mentions}). per_document_mentions: {per_doc}"
        )

    def test_total_mentions_equals_sum_of_per_document(self, output_data):
        """Verify total_mentions equals sum of all per_document_mentions values."""
        per_doc = output_data.get("per_document_mentions", {})
        total_mentions = output_data.get("total_mentions", 0)

        calculated_total = sum(per_doc.values())
        assert total_mentions == calculated_total, (
            f"total_mentions ({total_mentions}) does not match sum of "
            f"per_document_mentions ({calculated_total}). per_document_mentions: {per_doc}"
        )


class TestInputFilesExist:
    """Tests to verify input files exist (sanity check)."""

    @pytest.mark.parametrize("doc_name", EXPECTED_DOCUMENTS)
    def test_input_pdf_exists(self, doc_name):
        """Verify each input PDF file exists."""
        input_path = os.path.join(INPUT_DIR, doc_name)
        assert os.path.exists(input_path), (
            f"Input PDF file not found: {input_path}"
        )


class TestOutputJsonSchema:
    """Comprehensive schema validation test."""

    def test_complete_json_schema(self):
        """Verify output matches the complete expected JSON schema."""
        assert os.path.exists(OUTPUT_FILE), f"Output file not found at {OUTPUT_FILE}"

        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Check all required top-level keys
        required_keys = {"technique_id", "doc_count", "total_mentions", "per_document_mentions"}
        actual_keys = set(data.keys())
        missing_keys = required_keys - actual_keys
        extra_keys = actual_keys - required_keys

        assert len(missing_keys) == 0, f"Missing required keys: {missing_keys}"
        assert len(extra_keys) == 0, f"Unexpected extra keys: {extra_keys}"

        # Validate types
        assert isinstance(data["technique_id"], str), "technique_id must be string"
        assert isinstance(data["doc_count"], int), "doc_count must be int"
        assert isinstance(data["total_mentions"], int), "total_mentions must be int"
        assert isinstance(data["per_document_mentions"], dict), "per_document_mentions must be dict"

        # Validate technique_id format
        assert re.match(ATTACK_TECHNIQUE_PATTERN, data["technique_id"]), (
            f"technique_id '{data['technique_id']}' does not match ATT&CK format"
        )

        # Validate per_document_mentions has exactly the expected documents
        expected_doc_set = set(EXPECTED_DOCUMENTS)
        actual_doc_set = set(data["per_document_mentions"].keys())
        assert expected_doc_set == actual_doc_set, (
            f"per_document_mentions keys mismatch. "
            f"Expected: {expected_doc_set}, Got: {actual_doc_set}"
        )

        # Validate all per_document_mentions values are non-negative integers
        for doc_name, count in data["per_document_mentions"].items():
            assert isinstance(count, int) and count >= 0, (
                f"per_document_mentions['{doc_name}'] must be non-negative int, got {count}"
            )

        # Validate consistency
        docs_with_mentions = sum(1 for c in data["per_document_mentions"].values() if c > 0)
        assert data["doc_count"] == docs_with_mentions, (
            f"doc_count inconsistent with per_document_mentions"
        )

        calculated_total = sum(data["per_document_mentions"].values())
        assert data["total_mentions"] == calculated_total, (
            f"total_mentions inconsistent with per_document_mentions"
        )
