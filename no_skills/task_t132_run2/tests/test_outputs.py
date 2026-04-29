"""Auto-generated expectation tests for task verification.

These tests verify that the task execution produces correct outputs
based on the instruction requirements for finding the most common
MITRE ATT&CK technique ID across three PDF threat reports.
"""

import json
import os
import re
from pathlib import Path

import pytest


# Constants
OUTPUT_FILE = "/root/most_common_attack_technique.json"
INPUT_DIR = "/root/input"

# Expected document filenames (exact names required in per_document)
EXPECTED_DOCUMENTS = [
    "ASD-Cyber-Threat-Report-2024.pdf",
    "RedCanary-Threat-Detection-Report-2024.pdf",
    "Secureworks-State-of-the-Threat-Report-2024.pdf",
]

# MITRE ATT&CK technique ID pattern (T#### or T####.###)
TECHNIQUE_ID_PATTERN = re.compile(r"^T\d{4}(?:\.\d{3})?$")


class TestOutputFileExists:
    """Tests for verifying the output file was created."""

    def test_output_file_exists(self):
        """Verify the output JSON file was created at the expected path."""
        assert os.path.exists(OUTPUT_FILE), (
            f"Output file not found at {OUTPUT_FILE}. "
            "The task must write the JSON file to this exact path."
        )

    def test_output_file_is_not_empty(self):
        """Verify the output file is not empty."""
        assert os.path.exists(OUTPUT_FILE), f"Output file not found: {OUTPUT_FILE}"
        file_size = os.path.getsize(OUTPUT_FILE)
        assert file_size > 0, "Output file exists but is empty"

    def test_output_directory_exists(self):
        """Verify the output directory exists."""
        output_dir = os.path.dirname(OUTPUT_FILE)
        assert os.path.isdir(output_dir), f"Output directory not found: {output_dir}"


class TestOutputJsonFormat:
    """Tests for verifying the output is valid JSON with correct structure."""

    @pytest.fixture
    def output_data(self):
        """Load and return the output JSON data."""
        assert os.path.exists(OUTPUT_FILE), f"Output file not found: {OUTPUT_FILE}"
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def test_output_is_valid_json(self):
        """Verify output file contains valid JSON."""
        assert os.path.exists(OUTPUT_FILE), f"Output file not found: {OUTPUT_FILE}"
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                pytest.fail(f"Output file is not valid JSON: {e}")
        assert data is not None, "JSON parsed but result is None"

    def test_output_is_dict(self, output_data):
        """Verify the root JSON element is an object/dict."""
        assert isinstance(output_data, dict), (
            f"Expected JSON object at root level, got {type(output_data).__name__}"
        )

    def test_has_required_keys(self, output_data):
        """Verify all required top-level keys are present."""
        required_keys = {"technique_id", "documents_containing", "per_document"}
        actual_keys = set(output_data.keys())
        missing_keys = required_keys - actual_keys
        assert not missing_keys, f"Missing required keys: {missing_keys}"

    def test_no_extra_top_level_keys(self, output_data):
        """Verify no unexpected top-level keys are present."""
        expected_keys = {"technique_id", "documents_containing", "per_document"}
        actual_keys = set(output_data.keys())
        extra_keys = actual_keys - expected_keys
        assert not extra_keys, f"Unexpected extra keys found: {extra_keys}"


class TestTechniqueId:
    """Tests for verifying the technique_id field."""

    @pytest.fixture
    def output_data(self):
        """Load and return the output JSON data."""
        assert os.path.exists(OUTPUT_FILE), f"Output file not found: {OUTPUT_FILE}"
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def test_technique_id_is_string(self, output_data):
        """Verify technique_id is a string."""
        technique_id = output_data.get("technique_id")
        assert isinstance(technique_id, str), (
            f"technique_id must be a string, got {type(technique_id).__name__}"
        )

    def test_technique_id_matches_pattern(self, output_data):
        """Verify technique_id matches MITRE ATT&CK format (T#### or T####.###)."""
        technique_id = output_data.get("technique_id")
        assert technique_id is not None, "technique_id is missing"
        assert TECHNIQUE_ID_PATTERN.match(technique_id), (
            f"technique_id '{technique_id}' does not match expected pattern. "
            "Must be T followed by 4 digits, optionally followed by .### (e.g., T1059 or T1059.001)"
        )

    def test_technique_id_starts_with_t(self, output_data):
        """Verify technique_id starts with 'T'."""
        technique_id = output_data.get("technique_id")
        assert technique_id is not None, "technique_id is missing"
        assert technique_id.startswith("T"), (
            f"technique_id must start with 'T', got '{technique_id}'"
        )

    def test_technique_id_not_empty(self, output_data):
        """Verify technique_id is not an empty string."""
        technique_id = output_data.get("technique_id")
        assert technique_id, "technique_id is empty or missing"


class TestDocumentsContaining:
    """Tests for verifying the documents_containing field."""

    @pytest.fixture
    def output_data(self):
        """Load and return the output JSON data."""
        assert os.path.exists(OUTPUT_FILE), f"Output file not found: {OUTPUT_FILE}"
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def test_documents_containing_is_integer(self, output_data):
        """Verify documents_containing is an integer."""
        docs_count = output_data.get("documents_containing")
        assert isinstance(docs_count, int), (
            f"documents_containing must be an integer, got {type(docs_count).__name__}"
        )

    def test_documents_containing_in_valid_range(self, output_data):
        """Verify documents_containing is between 1 and 3."""
        docs_count = output_data.get("documents_containing")
        assert docs_count is not None, "documents_containing is missing"
        assert 1 <= docs_count <= 3, (
            f"documents_containing must be between 1 and 3, got {docs_count}"
        )

    def test_documents_containing_not_zero(self, output_data):
        """Verify documents_containing is not zero (at least one doc must contain it)."""
        docs_count = output_data.get("documents_containing")
        assert docs_count != 0, (
            "documents_containing cannot be 0 - the selected technique must appear in at least one document"
        )

    def test_documents_containing_not_negative(self, output_data):
        """Verify documents_containing is not negative."""
        docs_count = output_data.get("documents_containing")
        assert docs_count is not None, "documents_containing is missing"
        assert docs_count >= 0, f"documents_containing cannot be negative, got {docs_count}"


class TestPerDocument:
    """Tests for verifying the per_document field."""

    @pytest.fixture
    def output_data(self):
        """Load and return the output JSON data."""
        assert os.path.exists(OUTPUT_FILE), f"Output file not found: {OUTPUT_FILE}"
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def test_per_document_is_dict(self, output_data):
        """Verify per_document is a dictionary/object."""
        per_doc = output_data.get("per_document")
        assert isinstance(per_doc, dict), (
            f"per_document must be a dict/object, got {type(per_doc).__name__}"
        )

    def test_per_document_has_all_expected_documents(self, output_data):
        """Verify per_document contains all three expected document filenames."""
        per_doc = output_data.get("per_document", {})
        for doc_name in EXPECTED_DOCUMENTS:
            assert doc_name in per_doc, (
                f"Missing document '{doc_name}' in per_document. "
                f"Found keys: {list(per_doc.keys())}"
            )

    def test_per_document_has_exactly_three_entries(self, output_data):
        """Verify per_document has exactly three entries."""
        per_doc = output_data.get("per_document", {})
        assert len(per_doc) == 3, (
            f"per_document must have exactly 3 entries, got {len(per_doc)}"
        )

    def test_per_document_no_extra_documents(self, output_data):
        """Verify per_document contains only the expected document filenames."""
        per_doc = output_data.get("per_document", {})
        expected_set = set(EXPECTED_DOCUMENTS)
        actual_set = set(per_doc.keys())
        extra_docs = actual_set - expected_set
        assert not extra_docs, f"Unexpected documents in per_document: {extra_docs}"

    def test_per_document_values_are_booleans(self, output_data):
        """Verify all values in per_document are booleans."""
        per_doc = output_data.get("per_document", {})
        for doc_name, value in per_doc.items():
            assert isinstance(value, bool), (
                f"per_document['{doc_name}'] must be a boolean, "
                f"got {type(value).__name__}: {value}"
            )

    def test_per_document_asd_key_exists(self, output_data):
        """Verify ASD document key exists in per_document."""
        per_doc = output_data.get("per_document", {})
        assert "ASD-Cyber-Threat-Report-2024.pdf" in per_doc, (
            "Missing 'ASD-Cyber-Threat-Report-2024.pdf' key in per_document"
        )

    def test_per_document_redcanary_key_exists(self, output_data):
        """Verify RedCanary document key exists in per_document."""
        per_doc = output_data.get("per_document", {})
        assert "RedCanary-Threat-Detection-Report-2024.pdf" in per_doc, (
            "Missing 'RedCanary-Threat-Detection-Report-2024.pdf' key in per_document"
        )

    def test_per_document_secureworks_key_exists(self, output_data):
        """Verify Secureworks document key exists in per_document."""
        per_doc = output_data.get("per_document", {})
        assert "Secureworks-State-of-the-Threat-Report-2024.pdf" in per_doc, (
            "Missing 'Secureworks-State-of-the-Threat-Report-2024.pdf' key in per_document"
        )


class TestDataConsistency:
    """Tests for verifying logical consistency between fields."""

    @pytest.fixture
    def output_data(self):
        """Load and return the output JSON data."""
        assert os.path.exists(OUTPUT_FILE), f"Output file not found: {OUTPUT_FILE}"
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def test_documents_containing_matches_true_count(self, output_data):
        """Verify documents_containing equals the count of True values in per_document."""
        docs_count = output_data.get("documents_containing")
        per_doc = output_data.get("per_document", {})

        true_count = sum(1 for v in per_doc.values() if v is True)

        assert docs_count == true_count, (
            f"documents_containing ({docs_count}) does not match "
            f"the count of True values in per_document ({true_count}). "
            f"per_document values: {per_doc}"
        )

    def test_at_least_one_document_is_true(self, output_data):
        """Verify at least one document has a True value."""
        per_doc = output_data.get("per_document", {})
        true_count = sum(1 for v in per_doc.values() if v is True)
        assert true_count >= 1, (
            "At least one document must contain the technique (have True value). "
            f"All values are False: {per_doc}"
        )

    def test_documents_containing_consistent_with_per_document(self, output_data):
        """Verify documents_containing is consistent with per_document boolean values."""
        docs_count = output_data.get("documents_containing", 0)
        per_doc = output_data.get("per_document", {})

        # Count True values
        true_docs = [k for k, v in per_doc.items() if v is True]
        false_docs = [k for k, v in per_doc.items() if v is False]

        assert len(true_docs) == docs_count, (
            f"Inconsistency: documents_containing is {docs_count} but "
            f"{len(true_docs)} documents have True value. "
            f"True docs: {true_docs}, False docs: {false_docs}"
        )


class TestInputFilesExist:
    """Tests to verify input files exist (prerequisite for task)."""

    def test_input_directory_exists(self):
        """Verify the input directory exists."""
        assert os.path.isdir(INPUT_DIR), f"Input directory not found: {INPUT_DIR}"

    def test_asd_pdf_exists(self):
        """Verify ASD PDF input file exists."""
        pdf_path = os.path.join(INPUT_DIR, "ASD-Cyber-Threat-Report-2024.pdf")
        assert os.path.exists(pdf_path), f"Input file not found: {pdf_path}"

    def test_redcanary_pdf_exists(self):
        """Verify RedCanary PDF input file exists."""
        pdf_path = os.path.join(INPUT_DIR, "RedCanary-Threat-Detection-Report-2024.pdf")
        assert os.path.exists(pdf_path), f"Input file not found: {pdf_path}"

    def test_secureworks_pdf_exists(self):
        """Verify Secureworks PDF input file exists."""
        pdf_path = os.path.join(INPUT_DIR, "Secureworks-State-of-the-Threat-Report-2024.pdf")
        assert os.path.exists(pdf_path), f"Input file not found: {pdf_path}"

    def test_all_input_files_are_pdfs(self):
        """Verify all input files have .pdf extension."""
        for doc_name in EXPECTED_DOCUMENTS:
            assert doc_name.endswith(".pdf"), f"Expected PDF file, got: {doc_name}"


class TestJsonFormatting:
    """Tests for JSON file formatting and encoding."""

    def test_output_file_is_utf8(self):
        """Verify output file can be read as UTF-8."""
        assert os.path.exists(OUTPUT_FILE), f"Output file not found: {OUTPUT_FILE}"
        try:
            with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
                f.read()
        except UnicodeDecodeError as e:
            pytest.fail(f"Output file is not valid UTF-8: {e}")

    def test_json_is_readable(self):
        """Verify JSON can be loaded without errors."""
        assert os.path.exists(OUTPUT_FILE), f"Output file not found: {OUTPUT_FILE}"
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            content = f.read()

        # Should not raise an exception
        data = json.loads(content)
        assert data is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
