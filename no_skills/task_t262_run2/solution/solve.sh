#!/bin/bash
set -e

# Auto-generated solution based on execution trajectory
# This script recreates the outputs produced during synthesis

# Execute command
ls -la /root/

# Execute command
which markitdown || pip install markitdown 2>/dev/null; python -m markitdown --help 2>&1 | head -20

# Execute command
python -m markitdown /root/template.docx 2>/dev/null

# Execute command
python -m markitdown /root/Tutorial.docx 2>/dev/null

# Execute command
python -m markitdown /root/sample-word-document.docx 2>/dev/null

# Execute command
python -m markitdown /root/sample.docx 2>/dev/null

# Execute command
mkdir -p /root/output

# Create /root/alignment_analysis.py
mkdir -p $(dirname /root/alignment_analysis.py)
cat << 'HEREDOC_EOF' > /root/alignment_analysis.py
#!/usr/bin/env python3
"""
Alignment analysis: Extract headings from DOCX files and compute alignment scores.
"""

import json
import re
import subprocess
from pathlib import Path


def extract_markdown(docx_path: str) -> str:
    """Extract markdown text from DOCX using markitdown."""
    result = subprocess.run(
        ["python", "-m", "markitdown", docx_path],
        capture_output=True,
        text=True
    )
    return result.stdout


def normalize_heading(text: str) -> str:
    """
    Normalize a heading:
    - lowercase
    - strip punctuation (: ; , . ! ? ( ) [ ] { } " ' etc.)
    - collapse multiple whitespace to single space
    - trim
    """
    text = text.lower()
    # Remove punctuation
    text = re.sub(r'[:\;\,\.\!\?\(\)\[\]\{\}\"\'*_#\-—–]+', ' ', text)
    # Collapse whitespace
    text = re.sub(r'\s+', ' ', text)
    # Trim
    text = text.strip()
    return text


def is_title_cased(line: str) -> bool:
    """Check if a line is approximately title-cased (most words start uppercase)."""
    words = line.split()
    if len(words) == 0:
        return False
    # Count words starting with uppercase
    upper_count = sum(1 for w in words if w and w[0].isupper())
    return upper_count >= len(words) * 0.5


def extract_headings(markdown_text: str) -> list:
    """
    Extract headings from markdown text.

    Identification rules:
    1. Markdown headings: lines starting with # (e.g., ^#{1,6}\s+)
    2. Fallback heuristic:
       - Colon-terminated lines
       - Standalone title-cased short lines surrounded by blank lines
       - Bold text that appears as section markers
    """
    headings = []
    seen = set()
    lines = markdown_text.split('\n')

    for i, line in enumerate(lines):
        original_line = line.strip()
        if not original_line:
            continue

        heading_text = None

        # Rule 1: Markdown headings (# ## ### etc.)
        md_heading_match = re.match(r'^(#{1,6})\s+(.+)$', original_line)
        if md_heading_match:
            heading_text = md_heading_match.group(2)
            # Remove bold markers
            heading_text = re.sub(r'\*\*(.+?)\*\*', r'\1', heading_text)
            heading_text = re.sub(r'\*(.+?)\*', r'\1', heading_text)

        # Rule 2: Bold section markers (standalone bold text like **Resumo**)
        elif re.match(r'^\*\*[A-Za-zÀ-ÿ]', original_line):
            # Extract bold text
            bold_match = re.match(r'^\*\*([^*]+)\*\*\s*$', original_line)
            if bold_match:
                potential = bold_match.group(1).strip()
                # Must be relatively short (likely a heading)
                word_count = len(potential.split())
                if word_count <= 8:
                    heading_text = potential

        # Rule 3: Numbered sections (1. Section Name, 2. Section Name)
        elif re.match(r'^\d+\.\s+[A-Za-zÀ-ÿ]', original_line):
            potential = original_line
            # Check it's relatively short (heading-like)
            word_count = len(potential.split())
            if word_count <= 12:
                heading_text = potential

        # Rule 4: Colon-terminated lines that look like labels
        elif original_line.endswith(':') or original_line.endswith(':**'):
            potential = original_line.rstrip(':*')
            potential = re.sub(r'\*\*(.+?)\*\*', r'\1', potential)
            potential = re.sub(r'\*(.+?)\*', r'\1', potential)
            word_count = len(potential.split())
            if word_count <= 8:
                heading_text = potential

        # Rule 5: Title-cased short lines (fallback)
        elif is_title_cased(original_line) and len(original_line.split()) <= 6:
            # Check if surrounded by blank lines (roughly)
            prev_blank = (i == 0) or (lines[i-1].strip() == '')
            next_blank = (i == len(lines)-1) or (lines[i+1].strip() == '')
            if prev_blank or next_blank:
                heading_text = original_line

        if heading_text:
            # Normalize the heading
            normalized = normalize_heading(heading_text)
            # Skip empty or too short
            if len(normalized) >= 2 and normalized not in seen:
                headings.append(normalized)
                seen.add(normalized)

    return headings


def compute_alignment(template_headings: list, doc_headings: list) -> dict:
    """Compute alignment metrics between template and document headings."""
    template_set = set(template_headings)
    doc_set = set(doc_headings)

    matched_headings = len(template_set & doc_set)
    missing_headings = len(template_set - doc_set)
    extra_headings = len(doc_set - template_set)
    alignment_score = matched_headings * 2 - missing_headings - extra_headings

    return {
        "matched_headings": matched_headings,
        "missing_headings": missing_headings,
        "extra_headings": extra_headings,
        "alignment_score": alignment_score
    }


def main():
    input_dir = Path("/root/input")
    output_path = Path("/root/template_alignment.json")

    # Files to process
    template_file = input_dir / "template.docx"
    candidate_files = [
        "Tutorial.docx",
        "sample-word-document.docx",
        "sample.docx"
    ]

    # Extract markdown from all files
    print("Extracting markdown from template.docx...")
    template_md = extract_markdown(str(template_file))

    # Extract template headings
    print("Extracting template headings...")
    template_headings = extract_headings(template_md)
    print(f"Found {len(template_headings)} template headings:")
    for h in template_headings:
        print(f"  - {h}")

    # Process each candidate document
    documents = []
    for filename in candidate_files:
        filepath = input_dir / filename
        print(f"\nProcessing {filename}...")

        doc_md = extract_markdown(str(filepath))
        doc_headings = extract_headings(doc_md)
        print(f"  Found {len(doc_headings)} headings:")
        for h in doc_headings:
            print(f"    - {h}")

        metrics = compute_alignment(template_headings, doc_headings)
        metrics["filename"] = filename
        documents.append(metrics)

        print(f"  Alignment: matched={metrics['matched_headings']}, "
              f"missing={metrics['missing_headings']}, "
              f"extra={metrics['extra_headings']}, "
              f"score={metrics['alignment_score']}")

    # Determine best match
    max_score = max(d["alignment_score"] for d in documents)
    best_matches = [d for d in documents if d["alignment_score"] == max_score]

    # Tie-break: lexicographically smallest filename
    best_matches.sort(key=lambda d: d["filename"])
    best_match_filename = best_matches[0]["filename"]

    print(f"\nBest match: {best_match_filename} (score={max_score})")

    # Reorder documents list for output
    documents_output = []
    for filename in candidate_files:
        for d in documents:
            if d["filename"] == filename:
                documents_output.append({
                    "filename": d["filename"],
                    "matched_headings": d["matched_headings"],
                    "missing_headings": d["missing_headings"],
                    "extra_headings": d["extra_headings"],
                    "alignment_score": d["alignment_score"]
                })
                break

    # Build final output
    result = {
        "template_headings": template_headings,
        "documents": documents_output,
        "best_match_filename": best_match_filename
    }

    # Write JSON output
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"\nOutput written to: {output_path}")

    # Verify
    print("\nVerification:")
    for d in documents_output:
        assert d["matched_headings"] + d["missing_headings"] == len(template_headings), \
            f"Mismatch for {d['filename']}: matched + missing != template count"
    print("  All checks passed!")


if __name__ == "__main__":
    main()

HEREDOC_EOF

# Execute command
python alignment_analysis.py

# Execute command
python alignment_analysis.py

# Execute command
python -m markitdown /root/template.docx 2>/dev/null | head -60

# Execute command
python alignment_analysis.py

# Execute command
python alignment_analysis.py

# Execute command
python -c "
import json
with open('/root/template_alignment.json') as f:
    data = json.load(f)

# Verify schema
required_keys = {'template_headings', 'documents', 'best_match_filename'}
actual_keys = set(data.keys())
assert actual_keys == required_keys, f'Top-level keys mismatch: {actual_keys}'

# Verify documents structure
expected_filenames = ['Tutorial.docx', 'sample-word-document.docx', 'sample.docx']
for i, doc in enumerate(data['documents']):
    assert doc['filename'] == expected_filenames[i], f'Filename mismatch at index {i}'
    assert doc['matched_headings'] + doc['missing_headings'] == len(data['template_headings'])
    expected_doc_keys = {'filename', 'matched_headings', 'missing_headings', 'extra_headings', 'alignment_score'}
    assert set(doc.keys()) == expected_doc_keys, f'Document keys mismatch: {doc.keys()}'

# Verify best_match is consistent
scores = [(d['filename'], d['alignment_score']) for d in data['documents']]
max_score = max(s[1] for s in scores)
best_candidates = sorted([s[0] for s in scores if s[1] == max_score])
assert data['best_match_filename'] == best_candidates[0], 'Best match inconsistent'

print('All validations passed!')
print(f'Template headings: {len(data[\"template_headings\"])}')
print(f'Best match: {data[\"best_match_filename\"]} (score={max_score})')
for doc in data['documents']:
    print(f'  {doc[\"filename\"]}: matched={doc[\"matched_headings\"]}, missing={doc[\"missing_headings\"]}, extra={doc[\"extra_headings\"]}, score={doc[\"alignment_score\"]}')
"

# Execute command
python -m markitdown input/template.docx 2>/dev/null

# Execute command
python -m markitdown input/Tutorial.docx 2>/dev/null

# Execute command
python -m markitdown input/sample-word-document.docx 2>/dev/null

# Execute command
python -m markitdown input/sample.docx 2>/dev/null

# Create /root/expectation_tests.py
mkdir -p $(dirname /root/expectation_tests.py)
cat << 'HEREDOC_EOF' > /root/expectation_tests.py
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

HEREDOC_EOF

# Execute command
python -m py_compile expectation_tests.py && echo "Syntax OK"
