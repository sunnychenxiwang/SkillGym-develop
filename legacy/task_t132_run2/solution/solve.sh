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

HEREDOC_EOF

# Execute command
python3 -m py_compile expectation_tests.py && echo "Syntax check passed"

# Execute command
python3 -m pytest expectation_tests.py --collect-only 2>&1 | head -60

# Execute command
python3 -c "import expectation_tests; print('Import successful')" 2>&1

# Execute command
ls -la /root/

# Execute command
mkdir -p /root/output

# Create /root/extract_techniques.py
mkdir -p $(dirname /root/extract_techniques.py)
cat << 'HEREDOC_EOF' > /root/extract_techniques.py
#!/usr/bin/env python3
"""
Extract MITRE ATT&CK technique IDs from three PDF reports and find the most common one.
"""

import pdfplumber
import re
import json
from collections import Counter
from pathlib import Path

# Define file paths
INPUT_DIR = Path("/root/input")
OUTPUT_FILE = Path("/root/most_common_attack_technique.json")

PDF_FILES = [
    "ASD-Cyber-Threat-Report-2024.pdf",
    "RedCanary-Threat-Detection-Report-2024.pdf",
    "Secureworks-State-of-the-Threat-Report-2024.pdf",
]

# Regex pattern for MITRE ATT&CK technique IDs
TECHNIQUE_PATTERN = re.compile(r"\bT\d{4}(?:\.\d{3})?\b")


def extract_pdf_text(pdf_path: Path) -> str:
    """Extract all text from a PDF using pdfplumber."""
    chunks = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            print(f"  Processing {pdf_path.name}: {len(pdf.pages)} pages")
            for i, page in enumerate(pdf.pages):
                txt = page.extract_text()
                if txt:
                    chunks.append(txt)
                # Try with layout if regular extraction yields nothing
                elif not txt:
                    txt = page.extract_text(layout=True)
                    if txt:
                        chunks.append(txt)
    except Exception as e:
        print(f"  ERROR extracting text from {pdf_path.name}: {e}")
        return ""

    full_text = "\n".join(chunks)
    print(f"  Extracted {len(full_text):,} characters from {pdf_path.name}")
    return full_text


def find_technique_ids(text: str) -> list:
    """Find all MITRE ATT&CK technique IDs in text using the required regex."""
    return TECHNIQUE_PATTERN.findall(text)


def main():
    print("=" * 60)
    print("MITRE ATT&CK Technique ID Extraction")
    print("=" * 60)

    # Dictionary to store results per document
    # doc_techniques[filename] = list of all technique IDs found
    doc_techniques = {}

    # Extract text and find technique IDs for each PDF
    for pdf_name in PDF_FILES:
        pdf_path = INPUT_DIR / pdf_name
        print(f"\nProcessing: {pdf_name}")

        if not pdf_path.exists():
            print(f"  ERROR: File not found: {pdf_path}")
            doc_techniques[pdf_name] = []
            continue

        text = extract_pdf_text(pdf_path)
        technique_ids = find_technique_ids(text)
        doc_techniques[pdf_name] = technique_ids

        # Show summary
        unique_ids = set(technique_ids)
        print(f"  Found {len(technique_ids)} total occurrences of {len(unique_ids)} unique technique IDs")
        if unique_ids:
            # Show top 5 most frequent
            counter = Counter(technique_ids)
            top5 = counter.most_common(5)
            print(f"  Top 5: {top5}")

    # Compute per-technique statistics
    print("\n" + "=" * 60)
    print("Aggregating Results")
    print("=" * 60)

    # Get all unique technique IDs across all documents
    all_technique_ids = set()
    for ids in doc_techniques.values():
        all_technique_ids.update(ids)

    print(f"\nTotal unique technique IDs across all documents: {len(all_technique_ids)}")

    # For each technique ID, compute:
    # - documents_containing: how many documents contain it
    # - total_occurrences: sum of occurrences across all documents
    technique_stats = {}
    for tid in all_technique_ids:
        docs_with_tid = []
        total_count = 0
        for pdf_name, ids in doc_techniques.items():
            if tid in ids:
                docs_with_tid.append(pdf_name)
                total_count += ids.count(tid)

        technique_stats[tid] = {
            "documents_containing": len(docs_with_tid),
            "total_occurrences": total_count,
            "documents": docs_with_tid
        }

    # Apply selection rules:
    # 1. Highest documents_containing
    # 2. If tie, highest total_occurrences
    # 3. If tie, lexicographically smallest technique ID

    if not technique_stats:
        print("ERROR: No technique IDs found in any document!")
        return

    # Sort by selection criteria
    sorted_techniques = sorted(
        technique_stats.items(),
        key=lambda x: (
            -x[1]["documents_containing"],  # Higher is better (negative for descending)
            -x[1]["total_occurrences"],     # Higher is better (negative for descending)
            x[0]                             # Lexicographically smallest (ascending)
        )
    )

    # The winner
    winner_id = sorted_techniques[0][0]
    winner_stats = sorted_techniques[0][1]

    print(f"\nSelected technique: {winner_id}")
    print(f"  Documents containing: {winner_stats['documents_containing']}")
    print(f"  Total occurrences: {winner_stats['total_occurrences']}")
    print(f"  Found in: {winner_stats['documents']}")

    # Show runners-up for verification
    print("\nTop 10 techniques by selection criteria:")
    for i, (tid, stats) in enumerate(sorted_techniques[:10]):
        print(f"  {i+1}. {tid}: docs={stats['documents_containing']}, total={stats['total_occurrences']}")

    # Build the output JSON
    per_document = {}
    for pdf_name in PDF_FILES:
        per_document[pdf_name] = winner_id in doc_techniques[pdf_name]

    output = {
        "technique_id": winner_id,
        "documents_containing": winner_stats["documents_containing"],
        "per_document": per_document
    }

    # Write to file
    print(f"\nWriting output to: {OUTPUT_FILE}")
    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=2)

    print("\nFinal output:")
    print(json.dumps(output, indent=2))

    # Verification
    print("\n" + "=" * 60)
    print("Verification")
    print("=" * 60)
    assert sum(per_document.values()) == winner_stats["documents_containing"], "Document count mismatch!"
    print("PASS: documents_containing matches sum of per_document booleans")

    # Verify selection is correct
    for tid, stats in sorted_techniques[1:]:
        if stats["documents_containing"] > winner_stats["documents_containing"]:
            print(f"FAIL: {tid} has more documents!")
            break
        elif stats["documents_containing"] == winner_stats["documents_containing"]:
            if stats["total_occurrences"] > winner_stats["total_occurrences"]:
                print(f"FAIL: {tid} has same docs but more occurrences!")
                break
            elif stats["total_occurrences"] == winner_stats["total_occurrences"]:
                if tid < winner_id:
                    print(f"FAIL: {tid} is lexicographically smaller!")
                    break
    else:
        print("PASS: Selection criteria verified")

    print("\nDone!")


if __name__ == "__main__":
    main()

HEREDOC_EOF

# Execute command
python3 extract_techniques.py

# Execute command
python3 << 'EOF'
import pdfplumber
from pathlib import Path

# Check a sample of text from each PDF to verify extraction quality
INPUT_DIR = Path("/root/input")

for pdf_name in ["ASD-Cyber-Threat-Report-2024.pdf", "Secureworks-State-of-the-Threat-Report-2024.pdf"]:
    pdf_path = INPUT_DIR / pdf_name
    print(f"\n{'='*60}")
    print(f"Checking {pdf_name}")
    print('='*60)
    
    with pdfplumber.open(pdf_path) as pdf:
        # Extract text from a few pages and search for patterns
        full_text = ""
        for page in pdf.pages:
            txt = page.extract_text()
            if txt:
                full_text += txt + "\n"
        
        # Check for any T followed by numbers pattern
        import re
        
        # Look for "T1" patterns which might be technique references
        t_patterns = re.findall(r"T1\d{1,4}", full_text)
        print(f"Patterns matching T1xxx: {set(t_patterns)[:20] if t_patterns else 'None found'}")
        
        # Look for MITRE mentions
        mitre_mentions = len(re.findall(r"MITRE", full_text, re.IGNORECASE))
        print(f"MITRE mentions: {mitre_mentions}")
        
        # Look for ATT&CK mentions
        attack_mentions = len(re.findall(r"ATT&CK|ATT\s*&\s*CK", full_text, re.IGNORECASE))
        print(f"ATT&CK mentions: {attack_mentions}")
        
        # Look for "technique" mentions
        technique_mentions = len(re.findall(r"technique", full_text, re.IGNORECASE))
        print(f"Technique mentions: {technique_mentions}")
        
        # Check for potential technique IDs in different formats
        print("\nSample text snippets with potential technique references:")
        lines = full_text.split("\n")
        for line in lines:
            if "T1" in line and len(line) < 300:
                print(f"  - {line.strip()[:150]}")
                break
EOF

# Execute command
python3 << 'EOF'
import pdfplumber
from pathlib import Path
import re

INPUT_DIR = Path("/root/input")

pdf_path = INPUT_DIR / "Secureworks-State-of-the-Threat-Report-2024.pdf"
print(f"Checking {pdf_path.name}")

with pdfplumber.open(pdf_path) as pdf:
    full_text = ""
    for page in pdf.pages:
        txt = page.extract_text()
        if txt:
            full_text += txt + "\n"
    
    # Look for various patterns
    print(f"Total text length: {len(full_text)}")
    
    # Look for MITRE mentions
    mitre_mentions = len(re.findall(r"MITRE", full_text, re.IGNORECASE))
    print(f"MITRE mentions: {mitre_mentions}")
    
    # Look for ATT&CK mentions (including HTML encoded &)
    attack_mentions = re.findall(r"ATT.{0,5}CK", full_text, re.IGNORECASE)
    print(f"ATT&CK patterns found: {set(attack_mentions)}")
    
    # Look for "T1" patterns more broadly
    t_patterns = re.findall(r"T1\d{2,4}", full_text)
    print(f"T1xxx patterns found: {sorted(set(t_patterns))}")
    
    # Check for technique IDs with the exact regex
    technique_ids = re.findall(r"\bT\d{4}(?:\.\d{3})?\b", full_text)
    print(f"Exact technique ID regex matches: {sorted(set(technique_ids))}")
    
    # Print some context around any T1 mentions
    if t_patterns:
        print("\nContext around T1 mentions:")
        for match in re.finditer(r".{0,50}T1\d{2,4}.{0,50}", full_text[:50000]):
            print(f"  {match.group(0).strip()[:100]}")
            if len(list(re.finditer(r".{0,50}T1\d{2,4}.{0,50}", full_text[:50000]))) > 5:
                break
EOF

# Execute command
python3 << 'EOF'
import pdfplumber
from pathlib import Path
import re

INPUT_DIR = Path("/root/input")

# Try layout extraction for ASD and Secureworks
for pdf_name in ["ASD-Cyber-Threat-Report-2024.pdf", "Secureworks-State-of-the-Threat-Report-2024.pdf"]:
    pdf_path = INPUT_DIR / pdf_name
    print(f"\n{'='*50}")
    print(f"Layout extraction: {pdf_name}")
    print('='*50)
    
    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        for page in pdf.pages:
            try:
                txt = page.extract_text(layout=True)
                if txt:
                    full_text += txt + "\n"
            except:
                txt = page.extract_text()
                if txt:
                    full_text += txt + "\n"
        
        print(f"Total text length: {len(full_text)}")
        
        # Look for MITRE technique IDs
        technique_ids = re.findall(r"\bT\d{4}(?:\.\d{3})?\b", full_text)
        print(f"Technique IDs found: {sorted(set(technique_ids)) if technique_ids else 'None'}")
        
        # Look for T followed by digits more broadly
        t_patterns = re.findall(r"T\d{4}", full_text)
        print(f"T followed by 4 digits: {sorted(set(t_patterns)) if t_patterns else 'None'}")
EOF

# Execute command
python3 << 'EOF'
import pdfplumber
from pathlib import Path
import re
from collections import Counter

pdf_path = Path("/root/RedCanary-Threat-Detection-Report-2024.pdf")

with pdfplumber.open(pdf_path) as pdf:
    full_text = ""
    for page in pdf.pages:
        txt = page.extract_text()
        if txt:
            full_text += txt + "\n"
    
    # Find all technique IDs
    technique_ids = re.findall(r"\bT\d{4}(?:\.\d{3})?\b", full_text)
    
    print(f"Total occurrences: {len(technique_ids)}")
    print(f"Unique techniques: {len(set(technique_ids))}")
    
    # Count occurrences
    counter = Counter(technique_ids)
    
    print("\nAll technique IDs sorted by count:")
    for tid, count in counter.most_common():
        print(f"  {tid}: {count}")
EOF

