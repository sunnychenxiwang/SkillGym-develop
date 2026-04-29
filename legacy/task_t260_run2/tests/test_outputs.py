"""Auto-generated expectation tests for task verification.

These tests verify that the task execution produces correct outputs
based on the instruction requirements for extracting SharpDocx TOC sections
and checking keyword presence in other DOCX files.
"""

import json
import os
from pathlib import Path

import pytest


# Constants
OUTPUT_FILE = "/root/sharpdocx_toc_and_keyword_check.json"

# Expected TOC sections from Tutorial.docx (14 sections)
EXPECTED_TOC_SECTIONS = [
    "The basics",
    "The Write method",
    "Conditional content",
    "Text block limitations",
    "Loops",
    "Nested loops",
    "Loops, tables and the AppendRow method",
    "Combining loops, text blocks and tables",
    "Images",
    "Replacing text",
    "Referencing assemblies and importing namespaces",
    "Notes",
    "The Map",
    "The SharpDocx solution",
]

# Expected files in keyword check (in specified order)
EXPECTED_OTHER_FILES = [
    "sample-word-document.docx",
    "sample.docx",
    "template.docx",
]


class TestOutputFileExistence:
    """Tests for output file existence and basic structure."""

    def test_output_file_exists(self):
        """Verify output file was created at the specified path."""
        assert os.path.exists(OUTPUT_FILE), (
            f"Output file not found at {OUTPUT_FILE}"
        )

    def test_output_file_is_not_empty(self):
        """Verify output file has content."""
        assert os.path.getsize(OUTPUT_FILE) > 0, "Output file is empty"


class TestJsonValidity:
    """Tests for JSON format validity."""

    def test_output_is_valid_json(self):
        """Verify output is valid JSON format."""
        with open(OUTPUT_FILE) as f:
            data = json.load(f)
        assert data is not None, "JSON data should not be None"

    def test_output_is_dict(self):
        """Verify output JSON is a dictionary."""
        with open(OUTPUT_FILE) as f:
            data = json.load(f)
        assert isinstance(data, dict), "Output JSON should be a dictionary"


class TestSchemaStructure:
    """Tests for JSON schema structure compliance."""

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        with open(OUTPUT_FILE) as f:
            return json.load(f)

    def test_has_tutorial_toc_key(self, output_data):
        """Verify output contains 'tutorial_toc' key."""
        assert "tutorial_toc" in output_data, (
            "Missing required key 'tutorial_toc'"
        )

    def test_has_other_files_keyword_check_key(self, output_data):
        """Verify output contains 'other_files_keyword_check' key."""
        assert "other_files_keyword_check" in output_data, (
            "Missing required key 'other_files_keyword_check'"
        )

    def test_no_extra_top_level_keys(self, output_data):
        """Verify no extra keys in top-level JSON (only tutorial_toc and other_files_keyword_check)."""
        expected_keys = {"tutorial_toc", "other_files_keyword_check"}
        actual_keys = set(output_data.keys())
        extra_keys = actual_keys - expected_keys
        assert not extra_keys, f"Unexpected extra keys in JSON: {extra_keys}"


class TestTutorialTocStructure:
    """Tests for tutorial_toc section structure."""

    @pytest.fixture
    def tutorial_toc(self):
        """Load the tutorial_toc section."""
        with open(OUTPUT_FILE) as f:
            data = json.load(f)
        return data.get("tutorial_toc", {})

    def test_tutorial_toc_has_section_count(self, tutorial_toc):
        """Verify tutorial_toc contains 'section_count' key."""
        assert "section_count" in tutorial_toc, (
            "Missing 'section_count' in tutorial_toc"
        )

    def test_tutorial_toc_has_sections(self, tutorial_toc):
        """Verify tutorial_toc contains 'sections' key."""
        assert "sections" in tutorial_toc, (
            "Missing 'sections' in tutorial_toc"
        )

    def test_section_count_is_integer(self, tutorial_toc):
        """Verify section_count is an integer."""
        assert isinstance(tutorial_toc["section_count"], int), (
            "section_count should be an integer"
        )

    def test_sections_is_list(self, tutorial_toc):
        """Verify sections is a list."""
        assert isinstance(tutorial_toc["sections"], list), (
            "sections should be a list"
        )

    def test_no_extra_keys_in_tutorial_toc(self, tutorial_toc):
        """Verify no extra keys in tutorial_toc."""
        expected_keys = {"section_count", "sections"}
        actual_keys = set(tutorial_toc.keys())
        extra_keys = actual_keys - expected_keys
        assert not extra_keys, f"Unexpected keys in tutorial_toc: {extra_keys}"


class TestTutorialTocContent:
    """Tests for tutorial_toc content validity."""

    @pytest.fixture
    def tutorial_toc(self):
        """Load the tutorial_toc section."""
        with open(OUTPUT_FILE) as f:
            data = json.load(f)
        return data.get("tutorial_toc", {})

    def test_section_count_equals_14(self, tutorial_toc):
        """Verify section_count is exactly 14."""
        assert tutorial_toc["section_count"] == 14, (
            f"section_count must be 14, got {tutorial_toc['section_count']}"
        )

    def test_sections_list_has_14_items(self, tutorial_toc):
        """Verify sections list has exactly 14 items."""
        sections = tutorial_toc["sections"]
        assert len(sections) == 14, (
            f"sections list must have 14 items, got {len(sections)}"
        )

    def test_section_count_equals_sections_length(self, tutorial_toc):
        """Verify section_count equals the length of sections array."""
        section_count = tutorial_toc["section_count"]
        sections_length = len(tutorial_toc["sections"])
        assert section_count == sections_length, (
            f"section_count ({section_count}) must equal length of sections ({sections_length})"
        )

    def test_all_sections_are_strings(self, tutorial_toc):
        """Verify all section titles are strings."""
        for i, section in enumerate(tutorial_toc["sections"]):
            assert isinstance(section, str), (
                f"Section at index {i} should be a string, got {type(section)}"
            )

    def test_all_sections_are_non_empty(self, tutorial_toc):
        """Verify all section titles are non-empty strings."""
        for i, section in enumerate(tutorial_toc["sections"]):
            assert section.strip(), (
                f"Section at index {i} should not be empty"
            )

    def test_sections_match_expected_titles(self, tutorial_toc):
        """Verify sections contain the expected TOC titles."""
        sections = tutorial_toc["sections"]
        assert sections == EXPECTED_TOC_SECTIONS, (
            f"Sections do not match expected TOC titles.\n"
            f"Expected: {EXPECTED_TOC_SECTIONS}\n"
            f"Got: {sections}"
        )

    def test_first_section_is_the_basics(self, tutorial_toc):
        """Verify first section is 'The basics'."""
        assert tutorial_toc["sections"][0] == "The basics", (
            f"First section should be 'The basics', got '{tutorial_toc['sections'][0]}'"
        )

    def test_last_section_is_the_sharpdocx_solution(self, tutorial_toc):
        """Verify last section is 'The SharpDocx solution'."""
        assert tutorial_toc["sections"][-1] == "The SharpDocx solution", (
            f"Last section should be 'The SharpDocx solution', got '{tutorial_toc['sections'][-1]}'"
        )


class TestOtherFilesKeywordCheckStructure:
    """Tests for other_files_keyword_check structure."""

    @pytest.fixture
    def keyword_check(self):
        """Load the other_files_keyword_check section."""
        with open(OUTPUT_FILE) as f:
            data = json.load(f)
        return data.get("other_files_keyword_check", [])

    def test_keyword_check_is_list(self, keyword_check):
        """Verify other_files_keyword_check is a list."""
        assert isinstance(keyword_check, list), (
            "other_files_keyword_check should be a list"
        )

    def test_keyword_check_has_3_items(self, keyword_check):
        """Verify other_files_keyword_check has exactly 3 items."""
        assert len(keyword_check) == 3, (
            f"other_files_keyword_check must have 3 items, got {len(keyword_check)}"
        )

    def test_each_item_has_file_key(self, keyword_check):
        """Verify each item has 'file' key."""
        for i, item in enumerate(keyword_check):
            assert "file" in item, (
                f"Item at index {i} missing 'file' key"
            )

    def test_each_item_has_contains_sharpdocx_keyword_key(self, keyword_check):
        """Verify each item has 'contains_sharpdocx_keyword' key."""
        for i, item in enumerate(keyword_check):
            assert "contains_sharpdocx_keyword" in item, (
                f"Item at index {i} missing 'contains_sharpdocx_keyword' key"
            )

    def test_no_extra_keys_in_items(self, keyword_check):
        """Verify no extra keys in each item."""
        expected_keys = {"file", "contains_sharpdocx_keyword"}
        for i, item in enumerate(keyword_check):
            actual_keys = set(item.keys())
            extra_keys = actual_keys - expected_keys
            assert not extra_keys, (
                f"Item at index {i} has unexpected keys: {extra_keys}"
            )

    def test_file_values_are_strings(self, keyword_check):
        """Verify file values are strings."""
        for i, item in enumerate(keyword_check):
            assert isinstance(item["file"], str), (
                f"Item at index {i} 'file' should be string"
            )

    def test_contains_sharpdocx_keyword_values_are_booleans(self, keyword_check):
        """Verify contains_sharpdocx_keyword values are booleans."""
        for i, item in enumerate(keyword_check):
            assert isinstance(item["contains_sharpdocx_keyword"], bool), (
                f"Item at index {i} 'contains_sharpdocx_keyword' should be boolean, "
                f"got {type(item['contains_sharpdocx_keyword'])}"
            )


class TestOtherFilesKeywordCheckContent:
    """Tests for other_files_keyword_check content validity."""

    @pytest.fixture
    def keyword_check(self):
        """Load the other_files_keyword_check section."""
        with open(OUTPUT_FILE) as f:
            data = json.load(f)
        return data.get("other_files_keyword_check", [])

    def test_files_in_correct_order(self, keyword_check):
        """Verify files are listed in the exact order specified."""
        file_names = [item["file"] for item in keyword_check]
        assert file_names == EXPECTED_OTHER_FILES, (
            f"Files must be in order {EXPECTED_OTHER_FILES}, got {file_names}"
        )

    def test_first_file_is_sample_word_document(self, keyword_check):
        """Verify first file is sample-word-document.docx."""
        assert keyword_check[0]["file"] == "sample-word-document.docx", (
            f"First file should be 'sample-word-document.docx', "
            f"got '{keyword_check[0]['file']}'"
        )

    def test_second_file_is_sample(self, keyword_check):
        """Verify second file is sample.docx."""
        assert keyword_check[1]["file"] == "sample.docx", (
            f"Second file should be 'sample.docx', "
            f"got '{keyword_check[1]['file']}'"
        )

    def test_third_file_is_template(self, keyword_check):
        """Verify third file is template.docx."""
        assert keyword_check[2]["file"] == "template.docx", (
            f"Third file should be 'template.docx', "
            f"got '{keyword_check[2]['file']}'"
        )

    def test_sample_word_document_contains_no_sharpdocx(self, keyword_check):
        """Verify sample-word-document.docx does not contain sharpdocx keyword."""
        assert keyword_check[0]["contains_sharpdocx_keyword"] is False, (
            "sample-word-document.docx should have contains_sharpdocx_keyword=false"
        )

    def test_sample_contains_no_sharpdocx(self, keyword_check):
        """Verify sample.docx does not contain sharpdocx keyword."""
        assert keyword_check[1]["contains_sharpdocx_keyword"] is False, (
            "sample.docx should have contains_sharpdocx_keyword=false"
        )

    def test_template_contains_no_sharpdocx(self, keyword_check):
        """Verify template.docx does not contain sharpdocx keyword."""
        assert keyword_check[2]["contains_sharpdocx_keyword"] is False, (
            "template.docx should have contains_sharpdocx_keyword=false"
        )

    def test_all_files_have_false_keyword_check(self, keyword_check):
        """Verify all three files have contains_sharpdocx_keyword=false."""
        for item in keyword_check:
            assert item["contains_sharpdocx_keyword"] is False, (
                f"File '{item['file']}' should have contains_sharpdocx_keyword=false, "
                f"but got {item['contains_sharpdocx_keyword']}"
            )


class TestJsonFormatting:
    """Tests for JSON file formatting and encoding."""

    def test_output_file_is_utf8(self):
        """Verify output file is UTF-8 encoded."""
        with open(OUTPUT_FILE, 'rb') as f:
            content = f.read()
        # Try to decode as UTF-8
        try:
            content.decode('utf-8')
        except UnicodeDecodeError:
            pytest.fail("Output file is not valid UTF-8")

    def test_json_uses_double_quotes(self):
        """Verify JSON uses double quotes (not single quotes)."""
        with open(OUTPUT_FILE) as f:
            content = f.read()
        # Valid JSON should parse correctly (uses double quotes)
        data = json.loads(content)
        assert data is not None


class TestInputFilesExistence:
    """Tests to verify input files exist (sanity checks)."""

    INPUT_DIR = "/root/input"

    def test_tutorial_docx_exists(self):
        """Verify Tutorial.docx input file exists."""
        filepath = os.path.join(self.INPUT_DIR, "Tutorial.docx")
        assert os.path.exists(filepath), f"Input file not found: {filepath}"

    def test_sample_word_document_exists(self):
        """Verify sample-word-document.docx input file exists."""
        filepath = os.path.join(self.INPUT_DIR, "sample-word-document.docx")
        assert os.path.exists(filepath), f"Input file not found: {filepath}"

    def test_sample_docx_exists(self):
        """Verify sample.docx input file exists."""
        filepath = os.path.join(self.INPUT_DIR, "sample.docx")
        assert os.path.exists(filepath), f"Input file not found: {filepath}"

    def test_template_docx_exists(self):
        """Verify template.docx input file exists."""
        filepath = os.path.join(self.INPUT_DIR, "template.docx")
        assert os.path.exists(filepath), f"Input file not found: {filepath}"
