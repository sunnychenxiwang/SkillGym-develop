#!/bin/bash
set -e

# Auto-generated solution based on execution trajectory
# This script recreates the outputs produced during synthesis

# Execute command
ls -la /root/

# Execute command
ls -la /root/ 2>/dev/null || echo "Output directory does not exist yet"

# Create /root/expectation_tests.py
mkdir -p $(dirname /root/expectation_tests.py)
cat << 'HEREDOC_EOF' > /root/expectation_tests.py
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

HEREDOC_EOF

# Execute command
python -m py_compile expectation_tests.py && echo "Syntax OK"

# Execute command
python -m pytest expectation_tests.py --collect-only 2>&1 | head -60

# Execute command
ls -la /root/

# Execute command
mkdir -p /root/output

# Execute command
python3 -c "import pdfplumber; print('pdfplumber available')" 2>&1 || pip install pdfplumber -q

# Execute command
cat << 'EOF' > /root/extract_attack_techniques.py
import pdfplumber
import pypdf
import re
import json
from collections import Counter, defaultdict

# Define input files
INPUT_DIR = "/root/input"
OUTPUT_PATH = "/root/most_common_attack_technique.json"

FILES = {
    "ASD-Cyber-Threat-Report-2024.pdf": f"{INPUT_DIR}/ASD-Cyber-Threat-Report-2024.pdf",
    "RedCanary-Threat-Detection-Report-2024.pdf": f"{INPUT_DIR}/RedCanary-Threat-Detection-Report-2024.pdf",
    "Secureworks-State-of-the-Threat-Report-2024.pdf": f"{INPUT_DIR}/Secureworks-State-of-the-Threat-Report-2024.pdf",
}

# Regex for ATT&CK technique IDs
PATTERN = re.compile(r"\bT\d{4}(?:\.\d{3})?\b")

def extract_text_pdfplumber(filepath):
    """Extract text using pdfplumber."""
    texts = []
    try:
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                texts.append(page_text)
    except Exception as e:
        print(f"pdfplumber error for {filepath}: {e}")
        return None
    return "\n".join(texts)

def extract_text_pypdf(filepath):
    """Fallback: extract text using pypdf."""
    texts = []
    try:
        reader = pypdf.PdfReader(filepath)
        for page in reader.pages:
            page_text = page.extract_text() or ""
            texts.append(page_text)
    except Exception as e:
        print(f"pypdf error for {filepath}: {e}")
        return ""
    return "\n".join(texts)

def extract_text(filepath):
    """Extract text with pdfplumber, fallback to pypdf if needed."""
    text = extract_text_pdfplumber(filepath)
    if text is None or len(text.strip()) < 1000:
        print(f"Falling back to pypdf for {filepath}")
        text = extract_text_pypdf(filepath)
    return text

# Data structures
per_doc_counts = {}  # {filename: Counter of technique -> count}
global_total = Counter()  # technique -> total mentions
global_doc_presence = defaultdict(set)  # technique -> set of doc names

# Process each PDF
for filename, filepath in FILES.items():
    print(f"Processing: {filename}")
    text = extract_text(filepath)
    print(f"  Extracted text length: {len(text)} chars")
    
    # Find all ATT&CK technique IDs
    matches = PATTERN.findall(text)
    print(f"  Found {len(matches)} technique mentions")
    
    # Count per document
    doc_counter = Counter(matches)
    per_doc_counts[filename] = doc_counter
    
    # Update global aggregates
    for tech in doc_counter:
        global_doc_presence[tech].add(filename)
    global_total.update(doc_counter)
    
    # Show top techniques for this doc
    if doc_counter:
        print(f"  Top 5 techniques: {doc_counter.most_common(5)}")

print(f"\nTotal unique techniques found: {len(global_total)}")

# Select winner using tie-breakers
# Sort by: (-doc_count, -total_mentions, technique_id)
if global_total:
    candidates = []
    for tech, total in global_total.items():
        doc_count = len(global_doc_presence[tech])
        candidates.append((tech, doc_count, total))
    
    # Sort with tie-breakers
    candidates.sort(key=lambda x: (-x[1], -x[2], x[0]))
    
    winner = candidates[0][0]
    winner_doc_count = candidates[0][1]
    winner_total = candidates[0][2]
    
    print(f"\nWinner technique: {winner}")
    print(f"  doc_count: {winner_doc_count}")
    print(f"  total_mentions: {winner_total}")
    
    # Build result
    result = {
        "technique_id": winner,
        "doc_count": winner_doc_count,
        "total_mentions": winner_total,
        "per_document_mentions": {
            "ASD-Cyber-Threat-Report-2024.pdf": per_doc_counts["ASD-Cyber-Threat-Report-2024.pdf"].get(winner, 0),
            "RedCanary-Threat-Detection-Report-2024.pdf": per_doc_counts["RedCanary-Threat-Detection-Report-2024.pdf"].get(winner, 0),
            "Secureworks-State-of-the-Threat-Report-2024.pdf": per_doc_counts["Secureworks-State-of-the-Threat-Report-2024.pdf"].get(winner, 0),
        }
    }
    
    # Print top candidates for verification
    print("\nTop 10 candidates:")
    for tech, dc, tot in candidates[:10]:
        docs = list(global_doc_presence[tech])
        print(f"  {tech}: doc_count={dc}, total={tot}, in docs: {docs}")
    
    # Write output
    with open(OUTPUT_PATH, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\nResult written to: {OUTPUT_PATH}")
    print(json.dumps(result, indent=2))
else:
    print("No ATT&CK techniques found!")
EOF
python3 /root/extract_attack_techniques.py

# Execute command
python3 << 'EOF'
import pdfplumber
import pypdf
import re

# Check ASD report for potential ATT&CK references
filepath = "/root/ASD-Cyber-Threat-Report-2024.pdf"
print("=== ASD Report Investigation ===")

# Extract with pdfplumber
with pdfplumber.open(filepath) as pdf:
    text = "\n".join(p.extract_text() or "" for p in pdf.pages)

# Look for "T1" patterns more broadly
t1_pattern = re.compile(r'T1\d+', re.IGNORECASE)
matches = t1_pattern.findall(text)
print(f"Broader T1 pattern matches: {matches[:20]}")

# Look for "ATT&CK" or "MITRE" references
if "ATT&CK" in text or "ATTACK" in text:
    print("Contains ATT&CK references")
if "MITRE" in text:
    print("Contains MITRE references")
    
# Look for technique-like patterns
technique_pattern = re.compile(r'[Tt]echnique\s*[#:]?\s*\d+')
tech_matches = technique_pattern.findall(text)
print(f"Technique pattern matches: {tech_matches[:10]}")

# Sample some text to see format
print("\nSample of extracted text (chars 50000-51000):")
print(text[50000:51000] if len(text) > 51000 else text[:1000])
EOF

# Execute command
python3 << 'EOF'
import pdfplumber
import re

# Check Secureworks report
filepath = "/root/Secureworks-State-of-the-Threat-Report-2024.pdf"
print("=== Secureworks Report Investigation ===")

with pdfplumber.open(filepath) as pdf:
    text = "\n".join(p.extract_text() or "" for p in pdf.pages)

# Look for "T1" patterns broadly
t1_pattern = re.compile(r'T1\d+', re.IGNORECASE)
matches = t1_pattern.findall(text)
print(f"Broader T1 pattern matches: {matches[:20]}")

# Look for ATT&CK or MITRE references
if "ATT&CK" in text or "ATTACK" in text:
    print("Contains ATT&CK references")
if "MITRE" in text:
    print("Contains MITRE references")

# Sample text
print("\nSample of extracted text (chars 50000-51000):")
print(text[50000:51000] if len(text) > 51000 else text[:1000])
EOF

# Execute command
python3 << 'EOF'
import pdfplumber
import re

# Check RedCanary report format
filepath = "/root/RedCanary-Threat-Detection-Report-2024.pdf"
print("=== RedCanary Report Investigation ===")

with pdfplumber.open(filepath) as pdf:
    text = "\n".join(p.extract_text() or "" for p in pdf.pages)

# Find actual technique IDs
PATTERN = re.compile(r"\bT\d{4}(?:\.\d{3})?\b")
matches = PATTERN.findall(text)
print(f"Valid ATT&CK technique ID matches: {len(matches)}")
print(f"Unique techniques: {sorted(set(matches))}")

# Show some context around matches
for m in re.finditer(r".{20}\bT\d{4}(?:\.\d{3})?\b.{20}", text):
    print(f"Context: '{m.group()}'")
    break
EOF

# Execute command
python3 << 'EOF'
# Try pypdf as alternative extractor for ASD and Secureworks
import pypdf
import re

PATTERN = re.compile(r"\bT\d{4}(?:\.\d{3})?\b")

for name, path in [
    ("ASD", "/root/ASD-Cyber-Threat-Report-2024.pdf"),
    ("Secureworks", "/root/Secureworks-State-of-the-Threat-Report-2024.pdf")
]:
    print(f"\n=== {name} with pypdf ===")
    reader = pypdf.PdfReader(path)
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    print(f"Text length: {len(text)}")
    
    matches = PATTERN.findall(text)
    print(f"ATT&CK technique matches: {len(matches)}")
    if matches:
        print(f"Found: {sorted(set(matches))[:10]}")
EOF

# Execute command
cat /root/most_common_attack_technique.json

# Execute command
python3 -c "import json; data = json.load(open('/root/most_common_attack_technique.json')); print('JSON valid:', all(k in data for k in ['technique_id', 'doc_count', 'total_mentions', 'per_document_mentions']))"

