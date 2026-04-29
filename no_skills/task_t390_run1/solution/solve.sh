#!/bin/bash
set -e

# HARBOR_RUNTIME_PATH_FIX: align synthetic workspace paths with Harbor runtime layout
TASK_DIR="$(grep -Eo '/root/harbor_workspaces/task_[A-Za-z0-9_]+' "$0" | head -n1 || true)"
if [ -n "$TASK_DIR" ]; then
  mkdir -p "$TASK_DIR"
  [ -e "$TASK_DIR/input" ] || ln -s /root "$TASK_DIR/input"
  [ -e "$TASK_DIR/output" ] || ln -s /root "$TASK_DIR/output"
  cd "$TASK_DIR"
fi

# Generated scripts sometimes call `python`; map it to python3.
python() { python3 "$@"; }

# Some trajectories contain optional xsv diagnostics; skip if xsv is unavailable.
if ! command -v xsv >/dev/null 2>&1; then
  xsv() { return 0; }
fi

# Auto-generated solution based on execution trajectory
# This script recreates the outputs produced during synthesis

# Execute command
ls -la /root/harbor_workspaces/task_T390_run1/input/

# Execute command
python3 -c "
import pysam
bam = pysam.AlignmentFile('input/ex1.bam', 'rb')
print('Header dict:', dict(bam.header))
print('References:', bam.references)
print('Lengths:', bam.lengths)
print('N references:', bam.nreferences)
bam.close()
"

# Create /root/harbor_workspaces/task_T390_run1/expectation_tests.py
mkdir -p $(dirname /root/harbor_workspaces/task_T390_run1/expectation_tests.py)
cat << 'HEREDOC_EOF' > /root/harbor_workspaces/task_T390_run1/expectation_tests.py
"""Auto-generated expectation tests for BAM format consistency task.

These tests verify that the task execution produces correct outputs
based on the instruction requirements:
1. Parse HTML to extract repo description
2. Use pysam to extract BAM header @SQ entries
3. Compute format consistency based on deterministic rules
4. Output a JSON file with exact schema
"""

import json
import os
from pathlib import Path

import pytest

# Constants
OUTPUT_FILE = "/root/bam_format_consistency.json"
INPUT_BAM = "/root/ex1.bam"
INPUT_HTML = "/root/learning_bam_file"

# Expected schema keys (exactly these, no more, no less)
EXPECTED_KEYS = {"repo_description", "n_references", "reference_names_sorted", "is_format_consistent"}


class TestOutputFileExists:
    """Tests for output file existence and basic validity."""

    def test_output_file_exists(self):
        """Verify output JSON file was created at the exact specified path."""
        assert os.path.exists(OUTPUT_FILE), (
            f"Output file not found at {OUTPUT_FILE}. "
            "The task must save output to this exact path."
        )

    def test_output_file_is_not_empty(self):
        """Verify output file has content."""
        assert os.path.exists(OUTPUT_FILE), f"Output file not found: {OUTPUT_FILE}"
        file_size = os.path.getsize(OUTPUT_FILE)
        assert file_size > 0, "Output file exists but is empty"

    def test_output_directory_exists(self):
        """Verify output directory exists."""
        output_dir = os.path.dirname(OUTPUT_FILE)
        assert os.path.isdir(output_dir), f"Output directory does not exist: {output_dir}"


class TestOutputIsValidJson:
    """Tests for JSON format validity."""

    def test_output_is_valid_json(self):
        """Verify output file contains valid JSON."""
        assert os.path.exists(OUTPUT_FILE), f"Output file not found: {OUTPUT_FILE}"
        with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                pytest.fail(f"Output file is not valid JSON: {e}")
        assert data is not None, "JSON parsed to None"

    def test_output_is_json_object(self):
        """Verify output JSON is an object (dict), not array or primitive."""
        with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        assert isinstance(data, dict), (
            f"Output JSON must be an object (dict), got {type(data).__name__}"
        )


class TestJsonSchema:
    """Tests for exact JSON schema compliance."""

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)

    def test_has_all_required_keys(self, output_data):
        """Verify all required keys are present."""
        missing_keys = EXPECTED_KEYS - set(output_data.keys())
        assert not missing_keys, f"Missing required keys: {missing_keys}"

    def test_no_extra_keys(self, output_data):
        """Verify no extra keys beyond the required schema."""
        extra_keys = set(output_data.keys()) - EXPECTED_KEYS
        assert not extra_keys, (
            f"Extra keys found beyond required schema: {extra_keys}. "
            f"Expected exactly: {EXPECTED_KEYS}"
        )

    def test_exact_schema_match(self, output_data):
        """Verify output has exactly the required keys."""
        assert set(output_data.keys()) == EXPECTED_KEYS, (
            f"Schema mismatch. Expected keys: {EXPECTED_KEYS}, "
            f"Got keys: {set(output_data.keys())}"
        )


class TestRepoDescription:
    """Tests for repo_description field."""

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)

    def test_repo_description_is_string(self, output_data):
        """Verify repo_description is a string."""
        assert isinstance(output_data["repo_description"], str), (
            f"repo_description must be a string, got {type(output_data['repo_description']).__name__}"
        )

    def test_repo_description_not_empty(self, output_data):
        """Verify repo_description is not empty."""
        assert output_data["repo_description"].strip(), "repo_description cannot be empty or whitespace-only"

    def test_repo_description_is_reasonable_length(self, output_data):
        """Verify repo_description has reasonable length for a one-line description."""
        desc = output_data["repo_description"]
        assert len(desc) < 500, f"repo_description seems too long ({len(desc)} chars) for a one-line description"
        assert len(desc) > 5, f"repo_description seems too short ({len(desc)} chars)"

    def test_repo_description_extracted_from_html(self, output_data):
        """Verify repo_description contains expected content from the HTML."""
        desc = output_data["repo_description"].lower()
        # The HTML describes a repo about SAM/BAM format learning
        assert any(keyword in desc for keyword in ["sequence", "alignment", "bam", "sam", "map"]), (
            f"repo_description '{output_data['repo_description']}' does not appear to contain "
            "expected keywords related to the repository's SAM/BAM format purpose"
        )


class TestNReferences:
    """Tests for n_references field."""

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)

    def test_n_references_is_integer(self, output_data):
        """Verify n_references is an integer."""
        assert isinstance(output_data["n_references"], int), (
            f"n_references must be an integer, got {type(output_data['n_references']).__name__}"
        )

    def test_n_references_is_non_negative(self, output_data):
        """Verify n_references is non-negative."""
        assert output_data["n_references"] >= 0, (
            f"n_references cannot be negative, got {output_data['n_references']}"
        )

    def test_n_references_matches_bam_file(self, output_data):
        """Verify n_references matches the actual BAM file header."""
        # The ex1.bam file has 2 references (seq1, seq2) based on our analysis
        assert output_data["n_references"] == 2, (
            f"n_references should be 2 based on the input BAM file, got {output_data['n_references']}"
        )


class TestReferenceNamesSorted:
    """Tests for reference_names_sorted field."""

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)

    def test_reference_names_is_list(self, output_data):
        """Verify reference_names_sorted is a list."""
        assert isinstance(output_data["reference_names_sorted"], list), (
            f"reference_names_sorted must be a list, got {type(output_data['reference_names_sorted']).__name__}"
        )

    def test_reference_names_all_strings(self, output_data):
        """Verify all elements in reference_names_sorted are strings."""
        for i, name in enumerate(output_data["reference_names_sorted"]):
            assert isinstance(name, str), (
                f"Element at index {i} in reference_names_sorted must be a string, got {type(name).__name__}"
            )

    def test_reference_names_is_sorted(self, output_data):
        """Verify reference_names_sorted is actually sorted lexicographically."""
        names = output_data["reference_names_sorted"]
        assert names == sorted(names), (
            f"reference_names_sorted must be lexicographically sorted. "
            f"Got: {names}, Expected: {sorted(names)}"
        )

    def test_reference_names_count_matches_n_references(self, output_data):
        """Verify the count of reference names matches n_references."""
        n_refs = output_data["n_references"]
        n_names = len(output_data["reference_names_sorted"])
        assert n_refs == n_names, (
            f"n_references ({n_refs}) must match length of reference_names_sorted ({n_names})"
        )

    def test_reference_names_no_duplicates(self, output_data):
        """Verify there are no duplicate reference names."""
        names = output_data["reference_names_sorted"]
        assert len(names) == len(set(names)), (
            f"reference_names_sorted contains duplicates: {names}"
        )

    def test_reference_names_match_bam_file(self, output_data):
        """Verify reference names match the actual BAM file."""
        # The ex1.bam file has references 'seq1' and 'seq2'
        expected_sorted = ["seq1", "seq2"]
        assert output_data["reference_names_sorted"] == expected_sorted, (
            f"reference_names_sorted should be {expected_sorted}, got {output_data['reference_names_sorted']}"
        )


class TestIsFormatConsistent:
    """Tests for is_format_consistent field."""

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)

    def test_is_format_consistent_is_boolean(self, output_data):
        """Verify is_format_consistent is a boolean."""
        assert isinstance(output_data["is_format_consistent"], bool), (
            f"is_format_consistent must be a boolean, got {type(output_data['is_format_consistent']).__name__}"
        )

    def test_is_format_consistent_follows_rule(self, output_data):
        """Verify is_format_consistent follows the deterministic rule.

        Rule: is_format_consistent = true iff (n_references > 0) AND
              (every @SQ entry has both SN and LN fields present)
        """
        n_refs = output_data["n_references"]
        is_consistent = output_data["is_format_consistent"]

        # If n_references > 0 and we have valid reference names, consistency should be true
        # (The BAM file ex1.bam has proper SN and LN fields in its header)
        if n_refs > 0:
            # Given the actual BAM file has proper SQ entries with SN and LN
            assert is_consistent is True, (
                f"With n_references={n_refs} and valid SN/LN fields, "
                f"is_format_consistent should be True"
            )
        else:
            assert is_consistent is False, (
                f"With n_references=0, is_format_consistent should be False"
            )

    def test_is_format_consistent_expected_value(self, output_data):
        """Verify is_format_consistent has expected value for the given BAM file.

        The ex1.bam file has:
        - 2 references (n_references > 0)
        - Both @SQ entries have SN and LN fields
        Therefore is_format_consistent should be True.
        """
        assert output_data["is_format_consistent"] is True, (
            "For ex1.bam, is_format_consistent should be True because "
            "n_references > 0 and all @SQ entries have SN and LN fields"
        )


class TestInputFilesAvailable:
    """Tests to verify input files are accessible for validation context."""

    def test_input_bam_exists(self):
        """Verify the input BAM file exists."""
        assert os.path.exists(INPUT_BAM), f"Input BAM file not found: {INPUT_BAM}"

    def test_input_html_exists(self):
        """Verify the input HTML file exists."""
        assert os.path.exists(INPUT_HTML), f"Input HTML file not found: {INPUT_HTML}"


class TestDataConsistency:
    """Cross-field consistency tests."""

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)

    def test_empty_references_implies_inconsistent(self, output_data):
        """If n_references is 0, is_format_consistent must be False."""
        if output_data["n_references"] == 0:
            assert output_data["is_format_consistent"] is False, (
                "When n_references=0, is_format_consistent must be False per the rule"
            )
            assert output_data["reference_names_sorted"] == [], (
                "When n_references=0, reference_names_sorted must be empty"
            )

    def test_positive_references_with_consistency_check(self, output_data):
        """Verify consistency logic for positive reference counts."""
        n_refs = output_data["n_references"]
        is_consistent = output_data["is_format_consistent"]
        names = output_data["reference_names_sorted"]

        if n_refs > 0:
            assert len(names) > 0, "With n_references > 0, reference_names_sorted cannot be empty"
            # Consistency depends on whether all @SQ entries have SN and LN
            # This is a format-level check, not just count check

    def test_all_fields_populated(self, output_data):
        """Verify no field is None."""
        for key in EXPECTED_KEYS:
            assert output_data[key] is not None, f"Field '{key}' should not be None"

HEREDOC_EOF

# Execute command
python3 -m py_compile expectation_tests.py && echo "Syntax OK"

# Execute command
python3 -m pytest expectation_tests.py --collect-only 2>&1 | head -60

# Execute command
ls -la /root/harbor_workspaces/task_T390_run1/output 2>/dev/null || mkdir -p /root/harbor_workspaces/task_T390_run1/output && echo "Output directory ready"

# Execute command
python3 -c "import pysam; print(pysam.__version__)" 2>/dev/null || pip install pysam -q && python3 -c "import pysam; print('pysam installed successfully')"

# Create /root/harbor_workspaces/task_T390_run1/process_bam.py
mkdir -p $(dirname /root/harbor_workspaces/task_T390_run1/process_bam.py)
cat << 'HEREDOC_EOF' > /root/harbor_workspaces/task_T390_run1/process_bam.py
#!/usr/bin/env python3
"""
Script to validate BAM file format consistency against BAM/SAM format expectations.
Uses pysam to parse BAM headers and extracts repo description from HTML snapshot.
"""

import json
import re
import pysam


def extract_repo_description(html_path: str) -> str:
    """Extract the repository one-line description from the GitHub HTML snapshot."""
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Look for the meta description tag which contains the repo description
    # Format: <meta name="description" content="Learning the Sequence Alignment/Map format. Contribute to...">
    meta_match = re.search(
        r'<meta\s+name="description"\s+content="([^"]+)"',
        content
    )

    if meta_match:
        full_desc = meta_match.group(1)
        # The repo description is the first sentence before "Contribute to..."
        # Split at ". Contribute" to get just the repo-specific description
        if ". Contribute to" in full_desc:
            repo_desc = full_desc.split(". Contribute to")[0]
            return repo_desc
        return full_desc

    # Fallback: look for the title tag
    title_match = re.search(
        r'<title>GitHub - [^:]+: ([^·]+)·',
        content
    )
    if title_match:
        return title_match.group(1).strip()

    raise ValueError("Could not extract repository description from HTML")


def extract_bam_sq_info(bam_path: str) -> dict:
    """Extract @SQ reference sequence dictionary information using pysam."""
    samfile = pysam.AlignmentFile(bam_path, "rb")

    try:
        # Get the header
        header = samfile.header

        # Get the SQ entries from the header
        sq_entries = header.get("SQ", [])

        # Count references
        n_references = len(sq_entries)

        # Extract reference names and sort lexicographically
        reference_names = [sq["SN"] for sq in sq_entries if "SN" in sq]
        reference_names_sorted = sorted(reference_names)

        # Check format consistency:
        # is_format_consistent = true iff (n_references > 0) AND (every @SQ entry has both SN and LN)
        if n_references > 0:
            all_have_sn_and_ln = all(("SN" in sq) and ("LN" in sq) for sq in sq_entries)
            is_format_consistent = all_have_sn_and_ln
        else:
            is_format_consistent = False

        return {
            "n_references": n_references,
            "reference_names_sorted": reference_names_sorted,
            "is_format_consistent": is_format_consistent
        }
    finally:
        samfile.close()


def main():
    # File paths
    html_path = "/root/learning_bam_file"
    bam_path = "/root/ex1.bam"
    output_path = "/root/bam_format_consistency.json"

    # Step 1: Extract repo description from HTML
    repo_description = extract_repo_description(html_path)
    print(f"Extracted repo description: {repo_description}")

    # Step 2: Extract BAM SQ information using pysam
    bam_info = extract_bam_sq_info(bam_path)
    print(f"Number of references: {bam_info['n_references']}")
    print(f"Reference names (sorted): {bam_info['reference_names_sorted']}")
    print(f"Format consistent: {bam_info['is_format_consistent']}")

    # Step 3: Build the output JSON with exactly the required schema
    result = {
        "repo_description": repo_description,
        "n_references": bam_info["n_references"],
        "reference_names_sorted": bam_info["reference_names_sorted"],
        "is_format_consistent": bam_info["is_format_consistent"]
    }

    # Step 4: Write JSON output
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2)

    print(f"\nOutput written to: {output_path}")

    # Verify output
    with open(output_path, 'r') as f:
        verified = json.load(f)
    print(f"\nVerified JSON content:")
    print(json.dumps(verified, indent=2))


if __name__ == "__main__":
    main()

HEREDOC_EOF

# Execute command
python3 process_bam.py

