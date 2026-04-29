"""Auto-generated expectation tests for task verification.

These tests verify that the task execution produces correct outputs
based on the instruction requirements for matching mp-6930 to a CIF file.
"""

import json
import os
from pathlib import Path

import pytest


# Constants for expected file paths
OUTPUT_DIR = "/root"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "mp6930_cif_match.json")

# Valid CIF filename options
VALID_CIF_FILENAMES = ["SiO2-Quartz-alpha.cif", "SiO2-Cristobalite.cif"]

# Valid match status options
VALID_MATCH_STATUSES = ["match", "ambiguous", "no_match"]

# Required JSON keys
REQUIRED_KEYS = [
    "mp_id",
    "html_reduced_formula",
    "html_spacegroup_symbol",
    "html_spacegroup_number",
    "matched_cif_filename",
    "matched_cif_reduced_formula",
    "matched_cif_spacegroup_symbol",
    "matched_cif_spacegroup_number",
    "match_status"
]


class TestOutputFileExists:
    """Tests for verifying output file existence."""

    def test_output_directory_exists(self):
        """Verify output directory was created."""
        assert os.path.isdir(OUTPUT_DIR), f"Output directory not found: {OUTPUT_DIR}"

    def test_output_file_exists(self):
        """Verify output JSON file was created."""
        assert os.path.isfile(OUTPUT_FILE), f"Output file not found: {OUTPUT_FILE}"

    def test_output_file_not_empty(self):
        """Verify output file is not empty."""
        assert os.path.getsize(OUTPUT_FILE) > 0, "Output file is empty"


class TestOutputFormat:
    """Tests for verifying output format validity."""

    def test_output_is_valid_json(self):
        """Verify output is valid JSON format."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        assert data is not None, "JSON data should not be None"

    def test_output_is_dict(self):
        """Verify output JSON is a dictionary (object)."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        assert isinstance(data, dict), "Output should be a JSON object (dict)"

    def test_all_required_keys_present(self):
        """Verify all required keys are present in the JSON output."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)

        missing_keys = [key for key in REQUIRED_KEYS if key not in data]
        assert not missing_keys, f"Missing required keys: {missing_keys}"

    def test_no_extra_keys(self):
        """Verify there are no unexpected keys in the output."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)

        extra_keys = [key for key in data.keys() if key not in REQUIRED_KEYS]
        # Note: Extra keys are allowed but we document them
        if extra_keys:
            pytest.skip(f"Found extra keys (allowed but noted): {extra_keys}")


class TestFieldTypes:
    """Tests for verifying field value types."""

    def test_mp_id_is_string(self):
        """Verify mp_id is a string."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        assert isinstance(data["mp_id"], str), "mp_id should be a string"

    def test_html_reduced_formula_is_string(self):
        """Verify html_reduced_formula is a string."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        assert isinstance(data["html_reduced_formula"], str), "html_reduced_formula should be a string"

    def test_html_spacegroup_symbol_is_string(self):
        """Verify html_spacegroup_symbol is a string."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        assert isinstance(data["html_spacegroup_symbol"], str), "html_spacegroup_symbol should be a string"

    def test_html_spacegroup_number_is_int(self):
        """Verify html_spacegroup_number is an integer."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        assert isinstance(data["html_spacegroup_number"], int), "html_spacegroup_number should be an integer"

    def test_matched_cif_filename_is_string(self):
        """Verify matched_cif_filename is a string."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        assert isinstance(data["matched_cif_filename"], str), "matched_cif_filename should be a string"

    def test_matched_cif_reduced_formula_is_string(self):
        """Verify matched_cif_reduced_formula is a string."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        assert isinstance(data["matched_cif_reduced_formula"], str), "matched_cif_reduced_formula should be a string"

    def test_matched_cif_spacegroup_symbol_is_string(self):
        """Verify matched_cif_spacegroup_symbol is a string."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        assert isinstance(data["matched_cif_spacegroup_symbol"], str), "matched_cif_spacegroup_symbol should be a string"

    def test_matched_cif_spacegroup_number_is_int(self):
        """Verify matched_cif_spacegroup_number is an integer."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        assert isinstance(data["matched_cif_spacegroup_number"], int), "matched_cif_spacegroup_number should be an integer"

    def test_match_status_is_string(self):
        """Verify match_status is a string."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        assert isinstance(data["match_status"], str), "match_status should be a string"


class TestFieldValues:
    """Tests for verifying field value correctness."""

    def test_mp_id_value(self):
        """Verify mp_id is correctly set to mp-6930."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        assert data["mp_id"] == "mp-6930", f"mp_id should be 'mp-6930', got '{data['mp_id']}'"

    def test_matched_cif_filename_is_valid_option(self):
        """Verify matched_cif_filename is one of the valid CIF files."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        assert data["matched_cif_filename"] in VALID_CIF_FILENAMES, \
            f"matched_cif_filename must be one of {VALID_CIF_FILENAMES}, got '{data['matched_cif_filename']}'"

    def test_match_status_is_valid(self):
        """Verify match_status is one of the valid options."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        assert data["match_status"] in VALID_MATCH_STATUSES, \
            f"match_status must be one of {VALID_MATCH_STATUSES}, got '{data['match_status']}'"

    def test_html_spacegroup_number_positive(self):
        """Verify html_spacegroup_number is a positive integer (1-230 range)."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        assert 1 <= data["html_spacegroup_number"] <= 230, \
            f"html_spacegroup_number should be between 1-230, got {data['html_spacegroup_number']}"

    def test_matched_cif_spacegroup_number_positive(self):
        """Verify matched_cif_spacegroup_number is a positive integer (1-230 range)."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        assert 1 <= data["matched_cif_spacegroup_number"] <= 230, \
            f"matched_cif_spacegroup_number should be between 1-230, got {data['matched_cif_spacegroup_number']}"

    def test_formula_contains_expected_elements(self):
        """Verify reduced formulas contain Si and O (expected for SiO2)."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)

        # Check HTML formula
        html_formula = data["html_reduced_formula"]
        assert "Si" in html_formula or "si" in html_formula.lower(), \
            f"html_reduced_formula should contain Si, got '{html_formula}'"
        assert "O" in html_formula or "o" in html_formula.lower(), \
            f"html_reduced_formula should contain O, got '{html_formula}'"

        # Check CIF formula
        cif_formula = data["matched_cif_reduced_formula"]
        assert "Si" in cif_formula or "si" in cif_formula.lower(), \
            f"matched_cif_reduced_formula should contain Si, got '{cif_formula}'"
        assert "O" in cif_formula or "o" in cif_formula.lower(), \
            f"matched_cif_reduced_formula should contain O, got '{cif_formula}'"

    def test_spacegroup_symbol_not_empty(self):
        """Verify spacegroup symbols are not empty strings."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)

        assert len(data["html_spacegroup_symbol"].strip()) > 0, \
            "html_spacegroup_symbol should not be empty"
        assert len(data["matched_cif_spacegroup_symbol"].strip()) > 0, \
            "matched_cif_spacegroup_symbol should not be empty"


class TestMatchConsistency:
    """Tests for verifying consistency of match results."""

    def test_match_status_consistency_with_values(self):
        """Verify match_status is consistent with formula and spacegroup agreement."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)

        if data["match_status"] == "match":
            # If status is match, spacegroup numbers should match
            assert data["html_spacegroup_number"] == data["matched_cif_spacegroup_number"], \
                "When match_status is 'match', spacegroup numbers should be equal"

    def test_quartz_expected_for_spacegroup_154(self):
        """Verify that if space group 154 is matched, the CIF should be Quartz."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)

        if data["html_spacegroup_number"] == 154 and data["match_status"] == "match":
            # Space group 154 (P3_221) corresponds to alpha-quartz, not cristobalite
            # This tests the task-specific expected output
            assert data["matched_cif_filename"] == "SiO2-Quartz-alpha.cif", \
                "Space group 154 (P3_221) should match Quartz, not Cristobalite"

    def test_cristobalite_not_matched_for_spacegroup_154(self):
        """Verify cristobalite (spacegroup 92) is not matched when expecting 154."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)

        # Cristobalite has space group 92, mp-6930 has 154
        # If matched CIF is Cristobalite, status should not be "match" if HTML shows 154
        if data["matched_cif_filename"] == "SiO2-Cristobalite.cif":
            if data["html_spacegroup_number"] == 154:
                assert data["match_status"] != "match", \
                    "Cristobalite (SG 92) should not have match status when HTML expects SG 154"


class TestHTMLParsedValues:
    """Tests verifying values parsed from the HTML file match expected values."""

    def test_html_mp_id_from_page(self):
        """Verify mp_id matches what's in the HTML file."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)

        # The HTML file clearly shows mp-6930 in the og:title meta tag
        assert data["mp_id"] == "mp-6930", \
            "mp_id should be 'mp-6930' as shown in the HTML meta tags"

    def test_html_spacegroup_number_from_page(self):
        """Verify html_spacegroup_number matches what's in the HTML file."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)

        # The HTML meta tag shows: "mp-6930: SiO2 (Trigonal, P3_221, 154)"
        assert data["html_spacegroup_number"] == 154, \
            "html_spacegroup_number should be 154 as shown in HTML meta tags"

    def test_html_formula_is_sio2(self):
        """Verify html_reduced_formula is SiO2 as shown in HTML."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)

        # The HTML shows the formula as SiO2
        # Accept common variations: "SiO2", "Si1O2", etc.
        formula = data["html_reduced_formula"]
        # Normalize by removing spaces and converting to a common form
        assert "Si" in formula and "O" in formula, \
            f"html_reduced_formula should be a form of SiO2, got '{formula}'"


class TestExpectedOutcome:
    """Tests verifying the expected correct outcome of the task."""

    def test_expected_match_is_quartz(self):
        """Verify the expected correct match is SiO2-Quartz-alpha.cif.

        Based on analysis:
        - HTML (mp-6930): P3_221 (space group 154), SiO2
        - Quartz CIF: P 32 2 1 = P3_221 (space group 154), SiO2
        - Cristobalite CIF: P 41 21 2 (space group 92), SiO2

        Only Quartz matches both criteria.
        """
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)

        assert data["matched_cif_filename"] == "SiO2-Quartz-alpha.cif", \
            "Expected match is SiO2-Quartz-alpha.cif (space group 154 matches mp-6930)"

    def test_expected_match_status_is_match(self):
        """Verify match_status is 'match' since exactly one CIF matches."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)

        assert data["match_status"] == "match", \
            "match_status should be 'match' since Quartz uniquely matches mp-6930"

    def test_matched_spacegroup_is_154(self):
        """Verify the matched CIF has space group 154."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)

        assert data["matched_cif_spacegroup_number"] == 154, \
            f"matched_cif_spacegroup_number should be 154, got {data['matched_cif_spacegroup_number']}"

    def test_spacegroup_symbol_contains_p3(self):
        """Verify the matched spacegroup symbol indicates P3_221 type."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)

        symbol = data["matched_cif_spacegroup_symbol"]
        # The symbol could be "P3_221", "P 32 2 1", "P3221", etc.
        # Should contain "3" and "2" for the trigonal space group
        normalized = symbol.replace(" ", "").replace("_", "")
        assert "3" in normalized and "2" in normalized, \
            f"matched_cif_spacegroup_symbol should indicate P3_221 type, got '{symbol}'"
