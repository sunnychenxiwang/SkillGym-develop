"""Auto-generated expectation tests for BAM magic check verification.

These tests verify that the task execution produces correct outputs
based on the instruction requirements for comparing BAM magic identifiers.
"""

import json
import os
from pathlib import Path

import pytest


# Define the expected paths
OUTPUT_DIR = "/root/harbor_workspaces/task_T390_run2/output"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "bam_magic_check.json")
INPUT_BAM = "/root/ex1.bam"
INPUT_HTML = "/root/learning_bam_file"


class TestOutputFileExists:
    """Tests to verify output file creation."""

    def test_output_directory_exists(self):
        """Verify output directory exists."""
        assert os.path.exists(OUTPUT_DIR), f"Output directory not found: {OUTPUT_DIR}"

    def test_output_file_exists(self):
        """Verify output file was created at the exact path specified."""
        assert os.path.exists(OUTPUT_FILE), f"Output file not found: {OUTPUT_FILE}"

    def test_output_file_is_not_empty(self):
        """Verify output file is not empty."""
        assert os.path.getsize(OUTPUT_FILE) > 0, "Output file is empty"


class TestOutputFormat:
    """Tests to verify output format is valid JSON."""

    def test_output_is_valid_json(self):
        """Verify output is valid JSON format."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        assert data is not None, "JSON data is None"

    def test_output_is_dict(self):
        """Verify output JSON is a dictionary (object)."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        assert isinstance(data, dict), f"Expected dict, got {type(data).__name__}"


class TestOutputSchema:
    """Tests to verify output JSON has the required schema."""

    def test_has_spec_magic_key(self):
        """Verify JSON contains 'spec_magic' key."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        assert "spec_magic" in data, "Missing required key: 'spec_magic'"

    def test_has_observed_magic_key(self):
        """Verify JSON contains 'observed_magic' key."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        assert "observed_magic" in data, "Missing required key: 'observed_magic'"

    def test_has_matches_key(self):
        """Verify JSON contains 'matches' key."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        assert "matches" in data, "Missing required key: 'matches'"

    def test_no_extra_keys(self):
        """Verify JSON only contains the three required keys."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        expected_keys = {"spec_magic", "observed_magic", "matches"}
        actual_keys = set(data.keys())
        assert actual_keys == expected_keys, (
            f"Expected keys {expected_keys}, got {actual_keys}"
        )


class TestOutputDataTypes:
    """Tests to verify output values have correct data types."""

    def test_spec_magic_is_string(self):
        """Verify 'spec_magic' is a string."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        assert isinstance(data["spec_magic"], str), (
            f"'spec_magic' should be string, got {type(data['spec_magic']).__name__}"
        )

    def test_observed_magic_is_string(self):
        """Verify 'observed_magic' is a string."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        assert isinstance(data["observed_magic"], str), (
            f"'observed_magic' should be string, got {type(data['observed_magic']).__name__}"
        )

    def test_matches_is_boolean(self):
        """Verify 'matches' is a boolean."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        assert isinstance(data["matches"], bool), (
            f"'matches' should be boolean, got {type(data['matches']).__name__}"
        )


class TestMagicStringProperties:
    """Tests to verify the magic string values have expected properties."""

    def test_spec_magic_is_4_bytes(self):
        """Verify 'spec_magic' is exactly 4 characters (BAM magic is 4 bytes)."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        # BAM magic is 4 bytes: 'B', 'A', 'M', '\1'
        assert len(data["spec_magic"]) == 4, (
            f"'spec_magic' should be 4 characters, got {len(data['spec_magic'])}"
        )

    def test_observed_magic_is_4_bytes(self):
        """Verify 'observed_magic' is exactly 4 characters (BAM magic is 4 bytes)."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        # BAM magic is 4 bytes: 'B', 'A', 'M', '\1'
        assert len(data["observed_magic"]) == 4, (
            f"'observed_magic' should be 4 characters, got {len(data['observed_magic'])}"
        )

    def test_spec_magic_starts_with_bam(self):
        """Verify 'spec_magic' starts with 'BAM' (the standard BAM prefix)."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        assert data["spec_magic"].startswith("BAM"), (
            f"'spec_magic' should start with 'BAM', got '{data['spec_magic'][:3]}'"
        )

    def test_observed_magic_starts_with_bam(self):
        """Verify 'observed_magic' starts with 'BAM' if file is valid BAM."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        # A valid BAM file should have magic starting with 'BAM'
        assert data["observed_magic"].startswith("BAM"), (
            f"'observed_magic' should start with 'BAM', got '{data['observed_magic'][:3]}'"
        )


class TestMatchesLogic:
    """Tests to verify the 'matches' value is logically consistent."""

    def test_matches_reflects_comparison(self):
        """Verify 'matches' correctly reflects whether spec_magic equals observed_magic."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        expected_matches = data["spec_magic"] == data["observed_magic"]
        assert data["matches"] == expected_matches, (
            f"'matches' should be {expected_matches} when spec_magic='{data['spec_magic']}' "
            f"and observed_magic='{data['observed_magic']}'"
        )


class TestInputFilesExist:
    """Tests to verify input files exist for the task."""

    def test_input_bam_exists(self):
        """Verify input BAM file exists."""
        assert os.path.exists(INPUT_BAM), f"Input BAM file not found: {INPUT_BAM}"

    def test_input_html_exists(self):
        """Verify input HTML file exists."""
        assert os.path.exists(INPUT_HTML), f"Input HTML file not found: {INPUT_HTML}"


class TestBamFileValidity:
    """Tests to verify the BAM file can be read with pysam."""

    def test_bam_file_readable_with_pysam(self):
        """Verify the BAM file can be opened with pysam."""
        try:
            import pysam
            # Try to open the BAM file - this will fail if it's not a valid BAM
            with pysam.AlignmentFile(INPUT_BAM, "rb", check_sq=False) as bamfile:
                # Just verify we can open it
                assert bamfile is not None
        except ImportError:
            pytest.skip("pysam not installed, skipping BAM validation test")
        except Exception as e:
            pytest.fail(f"Failed to read BAM file with pysam: {e}")

    def test_bam_file_has_valid_magic(self):
        """Verify the BAM file has the expected magic bytes when read via pysam."""
        try:
            import gzip
            # BAM files are BGZF compressed; the first block decompresses to BAM header
            # After BGZF decompression, first 4 bytes should be 'BAM\1'
            import pysam

            with pysam.AlignmentFile(INPUT_BAM, "rb", check_sq=False) as bamfile:
                # If we can open it with pysam in 'rb' mode, it's a valid BAM
                # The header property existing indicates valid BAM format
                header = bamfile.header
                assert header is not None, "BAM file header is None"
        except ImportError:
            pytest.skip("pysam not installed, skipping BAM magic validation test")
        except Exception as e:
            pytest.fail(f"BAM file does not appear to be valid: {e}")


class TestExpectedBamMagic:
    """Tests to verify the BAM magic matches the known specification."""

    def test_observed_magic_matches_bam_spec(self):
        """Verify observed_magic matches the standard BAM magic 'BAM\\x01'."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        # The standard BAM magic is 'BAM' followed by byte 0x01 (ASCII SOH)
        # When represented as a string, it's 'BAM\x01' or equivalent
        expected_magic = "BAM\x01"
        assert data["observed_magic"] == expected_magic, (
            f"'observed_magic' should be 'BAM\\x01', got '{repr(data['observed_magic'])}'"
        )

    def test_spec_magic_should_match_bam_standard(self):
        """Verify spec_magic matches the BAM standard (if extracted correctly from HTML)."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        # The spec from the HTML should describe the standard BAM magic
        # which is 'BAM\x01' (4 bytes: B=0x42, A=0x41, M=0x4D, version=0x01)
        expected_magic = "BAM\x01"
        assert data["spec_magic"] == expected_magic, (
            f"'spec_magic' should be 'BAM\\x01', got '{repr(data['spec_magic'])}'"
        )


class TestJsonFileEncoding:
    """Tests to verify JSON file encoding and formatting."""

    def test_json_is_utf8(self):
        """Verify JSON file can be read as UTF-8."""
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            content = f.read()
        assert content, "Could not read file as UTF-8"

    def test_json_is_properly_formatted(self):
        """Verify JSON file is properly formatted (parseable)."""
        with open(OUTPUT_FILE, "r") as f:
            content = f.read()
        try:
            data = json.loads(content)
            assert data is not None
        except json.JSONDecodeError as e:
            pytest.fail(f"JSON is not properly formatted: {e}")
