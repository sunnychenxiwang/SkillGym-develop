"""Auto-generated expectation tests for task verification.

These tests verify that the template alignment task produces correct outputs
based on the instruction requirements. The task analyzes DOCX files to find
which document best matches the structure of a template.
"""

import json
import os
from pathlib import Path

import pytest


OUTPUT_FILE = "/root/template_alignment.json"
EXPECTED_DOCUMENT_FILENAMES = ["Tutorial.docx", "sample-word-document.docx", "sample.docx"]


class TestOutputFileExists:
    """Tests for verifying the output file was created."""

    def test_output_file_exists(self):
        """Verify output file was created at the specified path."""
        assert os.path.exists(OUTPUT_FILE), (
            f"Output file not found at {OUTPUT_FILE}. "
            "The task should create template_alignment.json in the output directory."
        )

    def test_output_file_not_empty(self):
        """Verify output file is not empty."""
        assert os.path.getsize(OUTPUT_FILE) > 0, (
            "Output file exists but is empty. "
            "The file should contain JSON content."
        )


class TestOutputIsValidJSON:
    """Tests for verifying the output is valid JSON format."""

    def test_output_is_valid_json(self):
        """Verify output file contains valid JSON."""
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            content = f.read()

        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            pytest.fail(f"Output file is not valid JSON: {e}")

        assert data is not None, "JSON parsed to None"

    def test_output_is_dict(self):
        """Verify output JSON is a dictionary (object), not array or primitive."""
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert isinstance(data, dict), (
            f"Output should be a JSON object (dict), got {type(data).__name__}"
        )


class TestSchemaRequirements:
    """Tests for verifying the JSON schema matches requirements."""

    @pytest.fixture
    def output_data(self):
        """Load and return the output JSON data."""
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def test_has_template_headings_key(self, output_data):
        """Verify 'template_headings' key exists."""
        assert "template_headings" in output_data, (
            "Missing required key 'template_headings' in output JSON"
        )

    def test_template_headings_is_list(self, output_data):
        """Verify 'template_headings' is a list."""
        assert isinstance(output_data["template_headings"], list), (
            f"'template_headings' should be a list, got {type(output_data['template_headings']).__name__}"
        )

    def test_template_headings_contains_strings(self, output_data):
        """Verify all items in 'template_headings' are strings."""
        for i, heading in enumerate(output_data["template_headings"]):
            assert isinstance(heading, str), (
                f"template_headings[{i}] should be a string, got {type(heading).__name__}"
            )

    def test_has_documents_key(self, output_data):
        """Verify 'documents' key exists."""
        assert "documents" in output_data, (
            "Missing required key 'documents' in output JSON"
        )

    def test_documents_is_list(self, output_data):
        """Verify 'documents' is a list."""
        assert isinstance(output_data["documents"], list), (
            f"'documents' should be a list, got {type(output_data['documents']).__name__}"
        )

    def test_documents_has_exactly_three_entries(self, output_data):
        """Verify 'documents' contains exactly 3 entries (one per non-template doc)."""
        assert len(output_data["documents"]) == 3, (
            f"'documents' should contain exactly 3 entries, got {len(output_data['documents'])}"
        )

    def test_has_best_match_filename_key(self, output_data):
        """Verify 'best_match_filename' key exists."""
        assert "best_match_filename" in output_data, (
            "Missing required key 'best_match_filename' in output JSON"
        )

    def test_best_match_filename_is_string(self, output_data):
        """Verify 'best_match_filename' is a string."""
        assert isinstance(output_data["best_match_filename"], str), (
            f"'best_match_filename' should be a string, got {type(output_data['best_match_filename']).__name__}"
        )

    def test_no_additional_top_level_keys(self, output_data):
        """Verify no additional top-level keys beyond the required ones."""
        allowed_keys = {"template_headings", "documents", "best_match_filename"}
        actual_keys = set(output_data.keys())
        extra_keys = actual_keys - allowed_keys

        assert not extra_keys, (
            f"Output contains unexpected top-level keys: {extra_keys}. "
            f"Only {allowed_keys} are allowed."
        )


class TestDocumentEntrySchema:
    """Tests for verifying each document entry has the correct schema."""

    @pytest.fixture
    def output_data(self):
        """Load and return the output JSON data."""
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    @pytest.fixture
    def documents(self, output_data):
        """Return the documents list."""
        return output_data["documents"]

    def test_each_document_has_filename(self, documents):
        """Verify each document entry has 'filename' key."""
        for i, doc in enumerate(documents):
            assert "filename" in doc, (
                f"documents[{i}] missing required key 'filename'"
            )
            assert isinstance(doc["filename"], str), (
                f"documents[{i}]['filename'] should be a string"
            )

    def test_each_document_has_matched_headings(self, documents):
        """Verify each document entry has 'matched_headings' key with integer value."""
        for i, doc in enumerate(documents):
            assert "matched_headings" in doc, (
                f"documents[{i}] missing required key 'matched_headings'"
            )
            assert isinstance(doc["matched_headings"], int), (
                f"documents[{i}]['matched_headings'] should be an integer, "
                f"got {type(doc['matched_headings']).__name__}"
            )
            assert doc["matched_headings"] >= 0, (
                f"documents[{i}]['matched_headings'] should be non-negative"
            )

    def test_each_document_has_missing_headings(self, documents):
        """Verify each document entry has 'missing_headings' key with integer value."""
        for i, doc in enumerate(documents):
            assert "missing_headings" in doc, (
                f"documents[{i}] missing required key 'missing_headings'"
            )
            assert isinstance(doc["missing_headings"], int), (
                f"documents[{i}]['missing_headings'] should be an integer, "
                f"got {type(doc['missing_headings']).__name__}"
            )
            assert doc["missing_headings"] >= 0, (
                f"documents[{i}]['missing_headings'] should be non-negative"
            )

    def test_each_document_has_extra_headings(self, documents):
        """Verify each document entry has 'extra_headings' key with integer value."""
        for i, doc in enumerate(documents):
            assert "extra_headings" in doc, (
                f"documents[{i}] missing required key 'extra_headings'"
            )
            assert isinstance(doc["extra_headings"], int), (
                f"documents[{i}]['extra_headings'] should be an integer, "
                f"got {type(doc['extra_headings']).__name__}"
            )
            assert doc["extra_headings"] >= 0, (
                f"documents[{i}]['extra_headings'] should be non-negative"
            )

    def test_each_document_has_alignment_score(self, documents):
        """Verify each document entry has 'alignment_score' key with integer value."""
        for i, doc in enumerate(documents):
            assert "alignment_score" in doc, (
                f"documents[{i}] missing required key 'alignment_score'"
            )
            assert isinstance(doc["alignment_score"], int), (
                f"documents[{i}]['alignment_score'] should be an integer, "
                f"got {type(doc['alignment_score']).__name__}"
            )

    def test_document_entries_have_no_extra_keys(self, documents):
        """Verify document entries have no keys beyond the required ones."""
        required_keys = {"filename", "matched_headings", "missing_headings",
                        "extra_headings", "alignment_score"}

        for i, doc in enumerate(documents):
            actual_keys = set(doc.keys())
            extra_keys = actual_keys - required_keys
            missing_keys = required_keys - actual_keys

            assert not extra_keys, (
                f"documents[{i}] contains unexpected keys: {extra_keys}"
            )
            assert not missing_keys, (
                f"documents[{i}] missing required keys: {missing_keys}"
            )


class TestDocumentFilenames:
    """Tests for verifying document filenames are correct."""

    @pytest.fixture
    def output_data(self):
        """Load and return the output JSON data."""
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    @pytest.fixture
    def documents(self, output_data):
        """Return the documents list."""
        return output_data["documents"]

    def test_all_expected_documents_present(self, documents):
        """Verify all three expected document filenames are present."""
        filenames = {doc["filename"] for doc in documents}
        expected = set(EXPECTED_DOCUMENT_FILENAMES)

        assert filenames == expected, (
            f"Expected documents {expected}, got {filenames}. "
            f"Missing: {expected - filenames}, Extra: {filenames - expected}"
        )

    def test_no_duplicate_filenames(self, documents):
        """Verify no duplicate filenames in documents list."""
        filenames = [doc["filename"] for doc in documents]
        assert len(filenames) == len(set(filenames)), (
            f"Duplicate filenames found in documents: {filenames}"
        )

    def test_best_match_is_valid_document(self, output_data):
        """Verify best_match_filename is one of the analyzed documents."""
        best_match = output_data["best_match_filename"]
        assert best_match in EXPECTED_DOCUMENT_FILENAMES, (
            f"best_match_filename '{best_match}' is not one of the expected documents: "
            f"{EXPECTED_DOCUMENT_FILENAMES}"
        )


class TestAlignmentScoreConsistency:
    """Tests for verifying alignment score calculations are consistent."""

    @pytest.fixture
    def output_data(self):
        """Load and return the output JSON data."""
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    @pytest.fixture
    def documents(self, output_data):
        """Return the documents list."""
        return output_data["documents"]

    def test_alignment_score_formula(self, documents, output_data):
        """Verify alignment_score = matched_headings * 2 - missing_headings - extra_headings."""
        template_heading_count = len(output_data["template_headings"])

        for doc in documents:
            expected_score = (
                doc["matched_headings"] * 2
                - doc["missing_headings"]
                - doc["extra_headings"]
            )
            assert doc["alignment_score"] == expected_score, (
                f"Document '{doc['filename']}' has incorrect alignment_score. "
                f"Expected: {expected_score} (matched*2 - missing - extra = "
                f"{doc['matched_headings']}*2 - {doc['missing_headings']} - {doc['extra_headings']}), "
                f"Got: {doc['alignment_score']}"
            )

    def test_matched_plus_missing_equals_template_count(self, documents, output_data):
        """Verify matched_headings + missing_headings equals template heading count."""
        template_count = len(output_data["template_headings"])

        for doc in documents:
            total = doc["matched_headings"] + doc["missing_headings"]
            assert total == template_count, (
                f"Document '{doc['filename']}': matched_headings ({doc['matched_headings']}) + "
                f"missing_headings ({doc['missing_headings']}) = {total}, "
                f"but should equal template_headings count ({template_count})"
            )

    def test_best_match_has_highest_score(self, documents, output_data):
        """Verify best_match_filename has the highest alignment_score."""
        best_match = output_data["best_match_filename"]
        best_match_doc = next(d for d in documents if d["filename"] == best_match)
        best_score = best_match_doc["alignment_score"]

        for doc in documents:
            assert doc["alignment_score"] <= best_score, (
                f"Document '{doc['filename']}' has score {doc['alignment_score']} "
                f"which is higher than best_match '{best_match}' with score {best_score}"
            )

    def test_tiebreaker_lexicographic(self, documents, output_data):
        """Verify ties are broken by lexicographically smallest filename."""
        best_match = output_data["best_match_filename"]
        best_match_doc = next(d for d in documents if d["filename"] == best_match)
        best_score = best_match_doc["alignment_score"]

        # Find all documents with the same highest score
        tied_docs = [d for d in documents if d["alignment_score"] == best_score]

        if len(tied_docs) > 1:
            # There's a tie - best_match should be lexicographically smallest
            tied_filenames = sorted([d["filename"] for d in tied_docs])
            assert best_match == tied_filenames[0], (
                f"Tie between documents {tied_filenames} with score {best_score}. "
                f"Expected lexicographically smallest '{tied_filenames[0]}' as best_match, "
                f"got '{best_match}'"
            )


class TestTemplateHeadingsExtraction:
    """Tests for verifying template headings were properly extracted."""

    @pytest.fixture
    def output_data(self):
        """Load and return the output JSON data."""
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def test_template_headings_not_empty(self, output_data):
        """Verify template_headings list is not empty."""
        assert len(output_data["template_headings"]) > 0, (
            "template_headings should not be empty. "
            "The template document contains section headings that should be extracted."
        )

    def test_template_headings_are_normalized(self, output_data):
        """Verify template headings are normalized (lowercase, no extra whitespace)."""
        for heading in output_data["template_headings"]:
            # Check lowercase
            assert heading == heading.lower(), (
                f"Heading '{heading}' should be normalized to lowercase"
            )
            # Check no leading/trailing whitespace
            assert heading == heading.strip(), (
                f"Heading '{heading}' should have no leading/trailing whitespace"
            )
            # Check no multiple consecutive spaces
            assert "  " not in heading, (
                f"Heading '{heading}' should not have multiple consecutive spaces"
            )

    def test_template_headings_no_duplicates(self, output_data):
        """Verify no duplicate headings in template_headings."""
        headings = output_data["template_headings"]
        assert len(headings) == len(set(headings)), (
            f"Duplicate headings found in template_headings: "
            f"{[h for h in headings if headings.count(h) > 1]}"
        )

    def test_template_headings_non_empty_strings(self, output_data):
        """Verify all template headings are non-empty strings."""
        for i, heading in enumerate(output_data["template_headings"]):
            assert len(heading) > 0, (
                f"template_headings[{i}] is an empty string"
            )


class TestOutputDirectory:
    """Tests for verifying output directory structure."""

    def test_output_directory_exists(self):
        """Verify output directory exists."""
        output_dir = os.path.dirname(OUTPUT_FILE)
        assert os.path.isdir(output_dir), (
            f"Output directory {output_dir} does not exist"
        )

    def test_output_file_is_json_extension(self):
        """Verify output file has .json extension."""
        assert OUTPUT_FILE.endswith(".json"), (
            f"Output file should have .json extension: {OUTPUT_FILE}"
        )

    def test_output_filename_is_correct(self):
        """Verify output filename is exactly 'template_alignment.json'."""
        filename = os.path.basename(OUTPUT_FILE)
        assert filename == "template_alignment.json", (
            f"Output filename should be 'template_alignment.json', got '{filename}'"
        )


class TestDataIntegrity:
    """Tests for verifying data integrity and logical consistency."""

    @pytest.fixture
    def output_data(self):
        """Load and return the output JSON data."""
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def test_matched_headings_not_greater_than_template_count(self, output_data):
        """Verify no document has more matched headings than total template headings."""
        template_count = len(output_data["template_headings"])

        for doc in output_data["documents"]:
            assert doc["matched_headings"] <= template_count, (
                f"Document '{doc['filename']}' has {doc['matched_headings']} matched headings "
                f"but template only has {template_count} headings"
            )

    def test_missing_headings_not_greater_than_template_count(self, output_data):
        """Verify no document has more missing headings than total template headings."""
        template_count = len(output_data["template_headings"])

        for doc in output_data["documents"]:
            assert doc["missing_headings"] <= template_count, (
                f"Document '{doc['filename']}' has {doc['missing_headings']} missing headings "
                f"but template only has {template_count} headings"
            )

    def test_scores_are_reasonable(self, output_data):
        """Verify alignment scores are within reasonable bounds."""
        template_count = len(output_data["template_headings"])

        # Maximum possible score: all headings matched, no extras
        # = template_count * 2 - 0 - 0 = template_count * 2
        max_possible = template_count * 2

        for doc in output_data["documents"]:
            assert doc["alignment_score"] <= max_possible, (
                f"Document '{doc['filename']}' has alignment_score {doc['alignment_score']} "
                f"which exceeds maximum possible score {max_possible}"
            )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
