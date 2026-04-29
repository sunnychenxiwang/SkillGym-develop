"""Auto-generated expectation tests for task verification.

These tests verify that the quadratic formula consistency analysis produces
correct outputs based on the instruction requirements.

The task extracts LaTeX math snippets containing the quadratic formula from
three files, normalizes them using SymPy, and verifies equivalence to the
canonical quadratic formula.
"""

import json
import os
from pathlib import Path

import pytest


# Expected output file path
OUTPUT_FILE = "/root/quadratic_formula_consistency.json"

# Expected input files
INPUT_FILES = [
    "01-basic-example.md",
    "sample.md",
    "examples.md",
]


class TestOutputFileExists:
    """Tests verifying the output file was created at the correct location."""

    def test_output_file_exists(self):
        """Verify the output file was created at the exact specified path."""
        assert os.path.exists(OUTPUT_FILE), (
            f"Output file not found at {OUTPUT_FILE}. "
            "The task requires writing to this exact path."
        )

    def test_output_directory_exists(self):
        """Verify the output directory exists."""
        output_dir = os.path.dirname(OUTPUT_FILE)
        assert os.path.isdir(output_dir), (
            f"Output directory {output_dir} does not exist."
        )

    def test_output_file_is_not_empty(self):
        """Verify the output file is not empty."""
        assert os.path.exists(OUTPUT_FILE), f"Output file not found at {OUTPUT_FILE}"
        file_size = os.path.getsize(OUTPUT_FILE)
        assert file_size > 0, "Output file is empty"


class TestOutputFormat:
    """Tests verifying the output file is valid JSON with correct format."""

    def test_output_is_valid_json(self):
        """Verify output is valid JSON format."""
        assert os.path.exists(OUTPUT_FILE), f"Output file not found at {OUTPUT_FILE}"
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            content = f.read()
        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            pytest.fail(f"Output file is not valid JSON: {e}")
        assert data is not None, "Parsed JSON is None"

    def test_json_is_dict(self):
        """Verify the root JSON element is a dictionary/object."""
        assert os.path.exists(OUTPUT_FILE), f"Output file not found at {OUTPUT_FILE}"
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert isinstance(data, dict), (
            f"Expected JSON root to be a dict, got {type(data).__name__}"
        )


class TestSchemaStructure:
    """Tests verifying the JSON schema matches the required structure exactly."""

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        assert os.path.exists(OUTPUT_FILE), f"Output file not found at {OUTPUT_FILE}"
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def test_has_canonical_latex_key(self, output_data):
        """Verify 'canonical_latex' key exists at root level."""
        assert "canonical_latex" in output_data, (
            "Missing required key 'canonical_latex' in JSON output"
        )

    def test_has_files_key(self, output_data):
        """Verify 'files' key exists at root level."""
        assert "files" in output_data, (
            "Missing required key 'files' in JSON output"
        )

    def test_has_total_snippets_found_key(self, output_data):
        """Verify 'total_snippets_found' key exists at root level."""
        assert "total_snippets_found" in output_data, (
            "Missing required key 'total_snippets_found' in JSON output"
        )

    def test_has_total_snippets_equivalent_key(self, output_data):
        """Verify 'total_snippets_equivalent' key exists at root level."""
        assert "total_snippets_equivalent" in output_data, (
            "Missing required key 'total_snippets_equivalent' in JSON output"
        )

    def test_only_expected_root_keys(self, output_data):
        """Verify only the expected keys exist at root level (no extra keys)."""
        expected_keys = {
            "canonical_latex",
            "files",
            "total_snippets_found",
            "total_snippets_equivalent",
        }
        actual_keys = set(output_data.keys())
        extra_keys = actual_keys - expected_keys
        assert not extra_keys, (
            f"Unexpected extra keys in JSON output: {extra_keys}. "
            f"Only these keys are allowed: {expected_keys}"
        )

    def test_files_is_dict(self, output_data):
        """Verify 'files' value is a dictionary."""
        assert isinstance(output_data["files"], dict), (
            f"Expected 'files' to be a dict, got {type(output_data['files']).__name__}"
        )


class TestFilesEntries:
    """Tests verifying each file entry has the correct structure."""

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        assert os.path.exists(OUTPUT_FILE), f"Output file not found at {OUTPUT_FILE}"
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    @pytest.fixture
    def files_data(self, output_data):
        """Get the files dictionary from output data."""
        return output_data.get("files", {})

    def test_all_input_files_present(self, files_data):
        """Verify all three input files are represented in the files dict."""
        for filename in INPUT_FILES:
            assert filename in files_data, (
                f"Missing file entry for '{filename}' in 'files' dict. "
                f"All three input files must be represented."
            )

    def test_no_extra_files(self, files_data):
        """Verify only the three expected files are in the files dict."""
        expected_files = set(INPUT_FILES)
        actual_files = set(files_data.keys())
        extra_files = actual_files - expected_files
        assert not extra_files, (
            f"Unexpected extra file entries: {extra_files}. "
            f"Only these files should be present: {expected_files}"
        )

    @pytest.mark.parametrize("filename", INPUT_FILES)
    def test_file_entry_is_dict(self, files_data, filename):
        """Verify each file entry is a dictionary."""
        if filename not in files_data:
            pytest.skip(f"File '{filename}' not present in output")
        assert isinstance(files_data[filename], dict), (
            f"Expected files['{filename}'] to be a dict, "
            f"got {type(files_data[filename]).__name__}"
        )

    @pytest.mark.parametrize("filename", INPUT_FILES)
    def test_file_entry_has_snippets_found(self, files_data, filename):
        """Verify each file entry has 'snippets_found' key."""
        if filename not in files_data:
            pytest.skip(f"File '{filename}' not present in output")
        assert "snippets_found" in files_data[filename], (
            f"Missing 'snippets_found' key in files['{filename}']"
        )

    @pytest.mark.parametrize("filename", INPUT_FILES)
    def test_file_entry_has_snippets_equivalent(self, files_data, filename):
        """Verify each file entry has 'snippets_equivalent' key."""
        if filename not in files_data:
            pytest.skip(f"File '{filename}' not present in output")
        assert "snippets_equivalent" in files_data[filename], (
            f"Missing 'snippets_equivalent' key in files['{filename}']"
        )

    @pytest.mark.parametrize("filename", INPUT_FILES)
    def test_file_entry_only_expected_keys(self, files_data, filename):
        """Verify each file entry has only the expected keys."""
        if filename not in files_data:
            pytest.skip(f"File '{filename}' not present in output")
        expected_keys = {"snippets_found", "snippets_equivalent"}
        actual_keys = set(files_data[filename].keys())
        extra_keys = actual_keys - expected_keys
        assert not extra_keys, (
            f"Unexpected extra keys in files['{filename}']: {extra_keys}"
        )


class TestDataTypes:
    """Tests verifying the data types of all values."""

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        assert os.path.exists(OUTPUT_FILE), f"Output file not found at {OUTPUT_FILE}"
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def test_canonical_latex_is_string(self, output_data):
        """Verify 'canonical_latex' is a string."""
        assert isinstance(output_data.get("canonical_latex"), str), (
            f"Expected 'canonical_latex' to be a string, "
            f"got {type(output_data.get('canonical_latex')).__name__}"
        )

    def test_total_snippets_found_is_integer(self, output_data):
        """Verify 'total_snippets_found' is an integer."""
        value = output_data.get("total_snippets_found")
        assert isinstance(value, int), (
            f"Expected 'total_snippets_found' to be an integer, "
            f"got {type(value).__name__}"
        )

    def test_total_snippets_equivalent_is_integer(self, output_data):
        """Verify 'total_snippets_equivalent' is an integer."""
        value = output_data.get("total_snippets_equivalent")
        assert isinstance(value, int), (
            f"Expected 'total_snippets_equivalent' to be an integer, "
            f"got {type(value).__name__}"
        )

    @pytest.mark.parametrize("filename", INPUT_FILES)
    def test_snippets_found_is_integer(self, output_data, filename):
        """Verify each file's 'snippets_found' is an integer."""
        files_data = output_data.get("files", {})
        if filename not in files_data:
            pytest.skip(f"File '{filename}' not present in output")
        value = files_data[filename].get("snippets_found")
        assert isinstance(value, int), (
            f"Expected files['{filename}']['snippets_found'] to be an integer, "
            f"got {type(value).__name__}"
        )

    @pytest.mark.parametrize("filename", INPUT_FILES)
    def test_snippets_equivalent_is_integer(self, output_data, filename):
        """Verify each file's 'snippets_equivalent' is an integer."""
        files_data = output_data.get("files", {})
        if filename not in files_data:
            pytest.skip(f"File '{filename}' not present in output")
        value = files_data[filename].get("snippets_equivalent")
        assert isinstance(value, int), (
            f"Expected files['{filename}']['snippets_equivalent'] to be an integer, "
            f"got {type(value).__name__}"
        )


class TestDataConstraints:
    """Tests verifying logical constraints on the data values."""

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        assert os.path.exists(OUTPUT_FILE), f"Output file not found at {OUTPUT_FILE}"
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def test_total_snippets_found_non_negative(self, output_data):
        """Verify 'total_snippets_found' is non-negative."""
        value = output_data.get("total_snippets_found", -1)
        assert value >= 0, (
            f"'total_snippets_found' should be non-negative, got {value}"
        )

    def test_total_snippets_equivalent_non_negative(self, output_data):
        """Verify 'total_snippets_equivalent' is non-negative."""
        value = output_data.get("total_snippets_equivalent", -1)
        assert value >= 0, (
            f"'total_snippets_equivalent' should be non-negative, got {value}"
        )

    def test_equivalent_not_more_than_found(self, output_data):
        """Verify total equivalent snippets <= total found snippets."""
        found = output_data.get("total_snippets_found", 0)
        equivalent = output_data.get("total_snippets_equivalent", 0)
        assert equivalent <= found, (
            f"total_snippets_equivalent ({equivalent}) cannot exceed "
            f"total_snippets_found ({found})"
        )

    @pytest.mark.parametrize("filename", INPUT_FILES)
    def test_per_file_snippets_found_non_negative(self, output_data, filename):
        """Verify each file's 'snippets_found' is non-negative."""
        files_data = output_data.get("files", {})
        if filename not in files_data:
            pytest.skip(f"File '{filename}' not present in output")
        value = files_data[filename].get("snippets_found", -1)
        assert value >= 0, (
            f"files['{filename}']['snippets_found'] should be non-negative, got {value}"
        )

    @pytest.mark.parametrize("filename", INPUT_FILES)
    def test_per_file_snippets_equivalent_non_negative(self, output_data, filename):
        """Verify each file's 'snippets_equivalent' is non-negative."""
        files_data = output_data.get("files", {})
        if filename not in files_data:
            pytest.skip(f"File '{filename}' not present in output")
        value = files_data[filename].get("snippets_equivalent", -1)
        assert value >= 0, (
            f"files['{filename}']['snippets_equivalent'] should be non-negative, got {value}"
        )

    @pytest.mark.parametrize("filename", INPUT_FILES)
    def test_per_file_equivalent_not_more_than_found(self, output_data, filename):
        """Verify each file's equivalent snippets <= found snippets."""
        files_data = output_data.get("files", {})
        if filename not in files_data:
            pytest.skip(f"File '{filename}' not present in output")
        found = files_data[filename].get("snippets_found", 0)
        equivalent = files_data[filename].get("snippets_equivalent", 0)
        assert equivalent <= found, (
            f"files['{filename}']['snippets_equivalent'] ({equivalent}) cannot exceed "
            f"'snippets_found' ({found})"
        )


class TestTotalsConsistency:
    """Tests verifying that totals equal the sum of per-file counts."""

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        assert os.path.exists(OUTPUT_FILE), f"Output file not found at {OUTPUT_FILE}"
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def test_total_snippets_found_equals_sum(self, output_data):
        """Verify total_snippets_found equals sum of per-file snippets_found."""
        files_data = output_data.get("files", {})
        total_reported = output_data.get("total_snippets_found", -1)

        sum_from_files = sum(
            file_data.get("snippets_found", 0)
            for file_data in files_data.values()
        )

        assert total_reported == sum_from_files, (
            f"total_snippets_found ({total_reported}) must equal the sum of "
            f"per-file snippets_found values ({sum_from_files})"
        )

    def test_total_snippets_equivalent_equals_sum(self, output_data):
        """Verify total_snippets_equivalent equals sum of per-file snippets_equivalent."""
        files_data = output_data.get("files", {})
        total_reported = output_data.get("total_snippets_equivalent", -1)

        sum_from_files = sum(
            file_data.get("snippets_equivalent", 0)
            for file_data in files_data.values()
        )

        assert total_reported == sum_from_files, (
            f"total_snippets_equivalent ({total_reported}) must equal the sum of "
            f"per-file snippets_equivalent values ({sum_from_files})"
        )


class TestCanonicalLatex:
    """Tests verifying the canonical LaTeX formula."""

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        assert os.path.exists(OUTPUT_FILE), f"Output file not found at {OUTPUT_FILE}"
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def test_canonical_latex_is_not_empty(self, output_data):
        """Verify canonical_latex is not an empty string."""
        canonical = output_data.get("canonical_latex", "")
        assert len(canonical) > 0, "canonical_latex should not be empty"

    def test_canonical_latex_contains_quadratic_formula_elements(self, output_data):
        """Verify canonical_latex contains essential quadratic formula elements."""
        canonical = output_data.get("canonical_latex", "")

        # Check for key mathematical elements of the quadratic formula
        assert "x" in canonical, "canonical_latex should contain 'x'"
        assert "=" in canonical, "canonical_latex should contain '='"
        assert "\\pm" in canonical or "pm" in canonical, (
            "canonical_latex should contain '\\pm' (plus-minus)"
        )
        assert "\\sqrt" in canonical or "sqrt" in canonical, (
            "canonical_latex should contain '\\sqrt' (square root)"
        )
        assert "\\frac" in canonical or "frac" in canonical, (
            "canonical_latex should contain '\\frac' (fraction)"
        )

    def test_canonical_latex_contains_coefficients(self, output_data):
        """Verify canonical_latex references a, b, c coefficients."""
        canonical = output_data.get("canonical_latex", "")

        # The quadratic formula should reference coefficients a, b, c
        assert "a" in canonical, "canonical_latex should contain coefficient 'a'"
        assert "b" in canonical, "canonical_latex should contain coefficient 'b'"
        assert "c" in canonical, "canonical_latex should contain coefficient 'c'"

    def test_canonical_latex_matches_expected(self, output_data):
        """Verify canonical_latex matches the expected formula."""
        canonical = output_data.get("canonical_latex", "")
        expected = r"x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}"

        # Normalize whitespace for comparison
        canonical_normalized = "".join(canonical.split())
        expected_normalized = "".join(expected.split())

        assert canonical_normalized == expected_normalized, (
            f"canonical_latex should be '{expected}', "
            f"got '{canonical}'"
        )


class TestBasicExampleFile:
    """Tests specific to the 01-basic-example.md file which contains quadratic formulas."""

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        assert os.path.exists(OUTPUT_FILE), f"Output file not found at {OUTPUT_FILE}"
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def test_basic_example_has_snippets(self, output_data):
        """Verify 01-basic-example.md has at least one snippet found.

        This file contains multiple quadratic formula snippets in different
        LaTeX formats, so snippets_found should be >= 1.
        """
        files_data = output_data.get("files", {})
        basic_example = files_data.get("01-basic-example.md", {})
        snippets_found = basic_example.get("snippets_found", 0)

        assert snippets_found >= 1, (
            "01-basic-example.md contains quadratic formula snippets, "
            f"but snippets_found is {snippets_found}"
        )

    def test_basic_example_equivalence_count(self, output_data):
        """Verify 01-basic-example.md has equivalent snippets if any are found.

        If snippets are found, at least some should be equivalent to the
        canonical quadratic formula (since the file contains standard formulas).
        """
        files_data = output_data.get("files", {})
        basic_example = files_data.get("01-basic-example.md", {})
        snippets_found = basic_example.get("snippets_found", 0)
        snippets_equivalent = basic_example.get("snippets_equivalent", 0)

        if snippets_found > 0:
            assert snippets_equivalent >= 1, (
                f"01-basic-example.md has {snippets_found} snippets found, "
                f"but {snippets_equivalent} equivalent. Expected at least some "
                "to be equivalent to the canonical formula."
            )
