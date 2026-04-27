import os
import re
import zipfile

import pytest


class TestSeaPdxDelayPptx:
    """Tests for verifying the SEA->PDX delay PowerPoint output."""

    OUTPUT_PATH = "/root/output/sea_pdx_worst_avg_arrival_delay.pptx"

    EXPECTED_RESULT = {
        "carrier_code": "OO",
        "airline_name": "SkyWest Airlines Inc.",
        "mean_arr_delay": 8.62,
        "ols_r_squared": 0.0000,
        "title": "SEA→PDX (Jan 2014): Worst Average Arrival Delay",
        "table_columns": ["carrier", "airline_name", "mean_arr_delay"],
    }
    TOLERANCE = 0.01

    def test_file_exists(self):
        """Verify output PPTX file was created."""
        assert os.path.exists(self.OUTPUT_PATH), f"Output file not found: {self.OUTPUT_PATH}"

    def test_file_not_empty(self):
        """Verify output file is not empty."""
        assert os.path.getsize(self.OUTPUT_PATH) > 0, "Output file is empty"

    def test_valid_pptx_format(self):
        """Verify output is a valid PPTX file (ZIP archive with correct structure)."""
        assert zipfile.is_zipfile(self.OUTPUT_PATH), "File is not a valid ZIP/PPTX archive"

        with zipfile.ZipFile(self.OUTPUT_PATH, 'r') as z:
            namelist = z.namelist()
            assert any("ppt/slides/" in name for name in namelist), "Missing ppt/slides/ directory"
            assert any("[Content_Types].xml" in name for name in namelist), "Missing [Content_Types].xml"
            assert any("ppt/presentation.xml" in name for name in namelist), "Missing ppt/presentation.xml"

    def test_has_single_slide(self):
        """Verify presentation has exactly one slide."""
        with zipfile.ZipFile(self.OUTPUT_PATH, 'r') as z:
            namelist = z.namelist()
            slide_files = [n for n in namelist if re.match(r"ppt/slides/slide\d+\.xml", n)]
            assert len(slide_files) == 1, f"Expected 1 slide, found {len(slide_files)}"

    def _extract_text_content(self):
        """Extract text content from the PPTX file using markitdown."""
        import subprocess
        result = subprocess.run(
            ["python", "-m", "markitdown", self.OUTPUT_PATH],
            capture_output=True,
            text=True
        )
        return result.stdout

    def test_title_present(self):
        """Verify slide has correct title."""
        content = self._extract_text_content()
        assert self.EXPECTED_RESULT["title"] in content, \
            f"Title not found: expected '{self.EXPECTED_RESULT['title']}'"

    def test_carrier_code_present(self):
        """Verify carrier code is present in content."""
        content = self._extract_text_content()
        assert self.EXPECTED_RESULT["carrier_code"] in content, \
            f"Carrier code '{self.EXPECTED_RESULT['carrier_code']}' not found"

    def test_airline_name_present(self):
        """Verify airline name is present in content."""
        content = self._extract_text_content()
        assert self.EXPECTED_RESULT["airline_name"] in content, \
            f"Airline name '{self.EXPECTED_RESULT['airline_name']}' not found"

    def test_mean_delay_value(self):
        """Verify mean arrival delay value is correct."""
        content = self._extract_text_content()
        expected_delay_str = f"{self.EXPECTED_RESULT['mean_arr_delay']:.2f}"
        assert expected_delay_str in content, \
            f"Mean delay value '{expected_delay_str}' not found in content"

    def test_ols_r_squared_present(self):
        """Verify OLS R² value is present and correctly formatted."""
        content = self._extract_text_content()
        expected_r2_str = f"{self.EXPECTED_RESULT['ols_r_squared']:.4f}"
        assert "R²" in content or "R2" in content, "R² notation not found"
        assert expected_r2_str in content, \
            f"R² value '{expected_r2_str}' not found in content"

    def test_table_structure(self):
        """Verify table has required columns."""
        content = self._extract_text_content()
        for col in self.EXPECTED_RESULT["table_columns"]:
            col_escaped = col.replace("_", r"\_")
            assert col in content or col_escaped in content, \
                f"Table column '{col}' not found"

    def test_table_has_data_row(self):
        """Verify table contains the data row with carrier info."""
        content = self._extract_text_content()
        lines = content.split('\n')
        table_lines = [l for l in lines if '|' in l and self.EXPECTED_RESULT["carrier_code"] in l]
        assert len(table_lines) >= 1, "Data row with carrier code not found in table"

    def test_sentence_format(self):
        """Verify the sentence contains all required elements."""
        content = self._extract_text_content()
        carrier = self.EXPECTED_RESULT["carrier_code"]
        airline = self.EXPECTED_RESULT["airline_name"]
        delay = f"{self.EXPECTED_RESULT['mean_arr_delay']:.2f}"

        assert carrier in content, f"Carrier code {carrier} missing from sentence"
        assert airline in content, f"Airline name {airline} missing from sentence"
        assert delay in content, f"Delay value {delay} missing from sentence"

    def test_content_integrity(self):
        """Verify all key content elements are present together."""
        content = self._extract_text_content()

        checks = [
            ("Title", self.EXPECTED_RESULT["title"]),
            ("Carrier code", self.EXPECTED_RESULT["carrier_code"]),
            ("Airline name", self.EXPECTED_RESULT["airline_name"]),
            ("Mean delay", f"{self.EXPECTED_RESULT['mean_arr_delay']:.2f}"),
            ("R² value", f"{self.EXPECTED_RESULT['ols_r_squared']:.4f}"),
        ]

        missing = []
        for name, value in checks:
            if value not in content:
                missing.append(f"{name}: {value}")

        assert not missing, f"Missing content elements: {missing}"
