"""Strong expectation tests for the most common ATT&CK technique task.

This test suite recomputes the expected answer directly from the three PDF files:
- /root/ASD-Cyber-Threat-Report-2024.pdf
- /root/RedCanary-Threat-Detection-Report-2024.pdf
- /root/Secureworks-State-of-the-Threat-Report-2024.pdf

It verifies:
1. The output file exists at the exact required path.
2. The JSON matches the exact required schema.
3. The winning technique_id is correct based on:
   - highest number of distinct documents containing it
   - then highest total occurrence count across all three documents
   - then lexicographically smallest technique ID
4. The per-document booleans are exactly correct.
"""

from __future__ import annotations

import json
import os
import re
from collections import Counter, defaultdict
from pathlib import Path

import pytest

OUTPUT_FILE = Path("/root/most_common_attack_technique.json")
PDF_FILES = [
    Path("/root/ASD-Cyber-Threat-Report-2024.pdf"),
    Path("/root/RedCanary-Threat-Detection-Report-2024.pdf"),
    Path("/root/Secureworks-State-of-the-Threat-Report-2024.pdf"),
]

TECHNIQUE_RE = re.compile(r"\bT\d{4}(?:\.\d{3})?\b", re.IGNORECASE)


def extract_pdf_text(pdf_path: Path) -> str:
    """Extract text from a PDF using an available Python PDF library."""
    assert pdf_path.exists(), f"Input PDF not found: {pdf_path}"
    assert pdf_path.stat().st_size > 0, f"Input PDF is empty: {pdf_path}"

    text_parts = []

    # Try pypdf first
    try:
        from pypdf import PdfReader  # type: ignore

        reader = PdfReader(str(pdf_path))
        for page in reader.pages:
            page_text = page.extract_text() or ""
            text_parts.append(page_text)
        return "\n".join(text_parts)
    except Exception:
        pass

    # Fallback to PyPDF2
    try:
        from PyPDF2 import PdfReader  # type: ignore

        reader = PdfReader(str(pdf_path))
        for page in reader.pages:
            page_text = page.extract_text() or ""
            text_parts.append(page_text)
        return "\n".join(text_parts)
    except Exception as e:
        pytest.fail(f"Failed to extract text from PDF {pdf_path}: {e}")


def compute_expected_result() -> dict:
    """Recompute the exact expected winner from the PDFs."""
    per_doc_counts: dict[str, Counter[str]] = {}
    doc_frequency: defaultdict[str, int] = defaultdict(int)
    total_occurrences: defaultdict[str, int] = defaultdict(int)

    for pdf_path in PDF_FILES:
        text = extract_pdf_text(pdf_path)
        matches = [m.upper() for m in TECHNIQUE_RE.findall(text)]
        counts = Counter(matches)
        per_doc_counts[pdf_path.name] = counts

        for technique_id, count in counts.items():
            if count > 0:
                doc_frequency[technique_id] += 1
                total_occurrences[technique_id] += count

    assert doc_frequency, "No ATT&CK technique IDs were found in the input PDFs"

    winner = min(
        doc_frequency.keys(),
        key=lambda tid: (
            -doc_frequency[tid],
            -total_occurrences[tid],
            tid,
        ),
    )

    per_document = {
        pdf_path.name: (per_doc_counts[pdf_path.name].get(winner, 0) > 0)
        for pdf_path in PDF_FILES
    }

    return {
        "technique_id": winner,
        "documents_containing": doc_frequency[winner],
        "per_document": per_document,
    }


@pytest.fixture(scope="module")
def output_data():
    assert OUTPUT_FILE.exists(), f"Output file not found at {OUTPUT_FILE}"
    assert OUTPUT_FILE.stat().st_size > 0, f"Output file is empty: {OUTPUT_FILE}"

    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert isinstance(data, dict), f"JSON root must be an object, got {type(data).__name__}"
    return data


@pytest.fixture(scope="module")
def expected_data():
    return compute_expected_result()


class TestInputFilesExist:
    def test_all_input_pdfs_exist(self):
        for pdf_path in PDF_FILES:
            assert pdf_path.exists(), f"Missing input PDF: {pdf_path}"

    def test_all_input_pdfs_nonempty(self):
        for pdf_path in PDF_FILES:
            assert pdf_path.stat().st_size > 0, f"Input PDF is empty: {pdf_path}"


class TestOutputFileExists:
    def test_output_file_exists(self):
        assert OUTPUT_FILE.exists(), f"Output file not found at {OUTPUT_FILE}"

    def test_output_file_nonempty(self):
        assert OUTPUT_FILE.stat().st_size > 0, f"Output file is empty: {OUTPUT_FILE}"


class TestOutputJsonValidity:
    def test_output_is_valid_json(self):
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert data is not None

    def test_output_root_is_object(self, output_data):
        assert isinstance(output_data, dict), "JSON root must be an object"


class TestExactSchema:
    def test_exact_top_level_keys(self, output_data):
        expected_keys = {"technique_id", "documents_containing", "per_document"}
        assert set(output_data.keys()) == expected_keys, (
            f"Top-level keys must be exactly {expected_keys}, got {set(output_data.keys())}"
        )

    def test_technique_id_type_and_format(self, output_data):
        assert isinstance(output_data["technique_id"], str), "technique_id must be a string"
        assert re.fullmatch(r"T\d{4}(?:\.\d{3})?", output_data["technique_id"]), (
            f"Invalid technique_id format: {output_data['technique_id']}"
        )

    def test_documents_containing_type_and_range(self, output_data):
        assert isinstance(output_data["documents_containing"], int), "documents_containing must be an integer"
        assert 1 <= output_data["documents_containing"] <= 3, (
            f"documents_containing must be between 1 and 3, got {output_data['documents_containing']}"
        )

    def test_per_document_type(self, output_data):
        assert isinstance(output_data["per_document"], dict), "per_document must be an object/dict"

    def test_exact_per_document_keys(self, output_data):
        expected_doc_keys = {pdf_path.name for pdf_path in PDF_FILES}
        actual_doc_keys = set(output_data["per_document"].keys())
        assert actual_doc_keys == expected_doc_keys, (
            f"per_document keys must be exactly {expected_doc_keys}, got {actual_doc_keys}"
        )

    def test_per_document_values_are_bools(self, output_data):
        for doc_name, value in output_data["per_document"].items():
            assert isinstance(value, bool), f"per_document[{doc_name!r}] must be boolean, got {type(value).__name__}"


class TestInternalConsistency:
    def test_documents_containing_matches_true_count(self, output_data):
        true_count = sum(1 for v in output_data["per_document"].values() if v is True)
        assert output_data["documents_containing"] == true_count, (
            f"documents_containing ({output_data['documents_containing']}) must equal "
            f"the number of true values in per_document ({true_count})"
        )


class TestExactCorrectness:
    def test_technique_id_is_correct(self, output_data, expected_data):
        assert output_data["technique_id"] == expected_data["technique_id"], (
            f"Wrong winning technique_id. Expected {expected_data['technique_id']}, "
            f"got {output_data['technique_id']}"
        )

    def test_documents_containing_is_correct(self, output_data, expected_data):
        assert output_data["documents_containing"] == expected_data["documents_containing"], (
            f"Wrong documents_containing. Expected {expected_data['documents_containing']}, "
            f"got {output_data['documents_containing']}"
        )

    def test_per_document_is_correct(self, output_data, expected_data):
        assert output_data["per_document"] == expected_data["per_document"], (
            f"Wrong per_document mapping. Expected {expected_data['per_document']}, "
            f"got {output_data['per_document']}"
        )


class TestWinnerSelectionRules:
    def test_output_obeys_distinct_document_maximization(self, output_data, expected_data):
        assert output_data["documents_containing"] == expected_data["documents_containing"], (
            "Winner does not have the maximum distinct-document count"
        )

    def test_output_obeys_full_tie_break_logic(self, output_data, expected_data):
        assert output_data["technique_id"] == expected_data["technique_id"], (
            "Winner does not match the exact tie-break result after recomputation"
        )