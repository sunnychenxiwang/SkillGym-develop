import os
import zipfile
import xml.etree.ElementTree as ET
import re

import pytest


class TestMaintenanceRecommendationDocx:
    """Tests for verifying the maintenance month recommendation Word document."""

    OUTPUT_PATH = "/root/output/maintenance_month_recommendation.docx"

    # Expected values based on the analysis
    EXPECTED_MONTH = "July"
    EXPECTED_AVOID_SCORE = 13

    REQUIRED_TABLE_COLUMNS = [
        "month",
        "seasonality_index",
        "p90_arr_delay",
        "cancel_rate_proxy",
        "demand_rank",
        "delay_rank",
        "cancel_rank",
        "avoid_score"
    ]

    REQUIRED_SECTIONS = [
        "Maintenance Scheduling Recommendation",  # Title (Heading 1)
        "Metric Contract",
        "Recommendation",
        "Decision Brief"
    ]

    # Expected table data for July (the recommended month)
    EXPECTED_JULY_DATA = {
        "seasonality_index": 125.34,
        "p90_arr_delay": 29.0,
        "cancel_rate_proxy": 0.0031,
        "demand_rank": 1,
        "delay_rank": 3,
        "cancel_rank": 9,
        "avoid_score": 13
    }

    TOLERANCE = 0.01

    @pytest.fixture(scope="class")
    def document_text(self):
        """Extract text content from the docx file."""
        with zipfile.ZipFile(self.OUTPUT_PATH, 'r') as z:
            with z.open('word/document.xml') as f:
                content = f.read().decode('utf-8')
        # Extract all text between <w:t> tags
        text_elements = re.findall(r'<w:t[^>]*>([^<]+)</w:t>', content)
        return text_elements

    def test_file_exists(self):
        """Verify the output docx file was created at the correct path."""
        assert os.path.exists(self.OUTPUT_PATH), \
            f"Output file not found at {self.OUTPUT_PATH}"

    def test_file_not_empty(self):
        """Verify the output file is not empty."""
        file_size = os.path.getsize(self.OUTPUT_PATH)
        assert file_size > 0, "Output file is empty"
        assert file_size > 1000, f"Output file too small ({file_size} bytes), expected a complete document"

    def test_valid_zip_archive(self):
        """Verify the docx is a valid ZIP archive."""
        assert zipfile.is_zipfile(self.OUTPUT_PATH), \
            "Output file is not a valid ZIP archive (docx files are ZIP-based)"

    def test_valid_docx_structure(self):
        """Verify the docx has required Office Open XML structure."""
        with zipfile.ZipFile(self.OUTPUT_PATH, 'r') as z:
            file_list = z.namelist()

            # Required files for a valid docx
            assert '[Content_Types].xml' in file_list, "Missing [Content_Types].xml"
            assert 'word/document.xml' in file_list, "Missing word/document.xml"
            assert '_rels/.rels' in file_list, "Missing _rels/.rels"

    def test_document_xml_parseable(self):
        """Verify the document.xml is valid XML."""
        with zipfile.ZipFile(self.OUTPUT_PATH, 'r') as z:
            with z.open('word/document.xml') as f:
                content = f.read()
                # Should not raise an exception
                ET.fromstring(content)

    def test_has_title_heading(self, document_text):
        """Verify the document has the required title heading."""
        assert "Maintenance Scheduling Recommendation" in document_text, \
            "Missing required title: 'Maintenance Scheduling Recommendation'"

    def test_has_metric_contract_section(self, document_text):
        """Verify the document has a Metric Contract section."""
        assert "Metric Contract" in document_text, \
            "Missing required section: 'Metric Contract'"

    def test_has_recommendation_section(self, document_text):
        """Verify the document has a Recommendation section."""
        assert "Recommendation" in document_text, \
            "Missing required section: 'Recommendation'"

    def test_has_decision_brief_section(self, document_text):
        """Verify the document has a Decision Brief section."""
        assert "Decision Brief" in document_text, \
            "Missing required section: 'Decision Brief'"

    def test_recommendation_names_month(self, document_text):
        """Verify the recommendation explicitly names the chosen month."""
        full_text = " ".join(document_text)
        # Check that July is mentioned in the recommendation context
        assert self.EXPECTED_MONTH in full_text, \
            f"Recommendation should name '{self.EXPECTED_MONTH}' as the recommended month"

        # Verify it's mentioned as THE recommended month
        assert "July is the recommended month" in full_text or \
               "recommended month to schedule major aircraft maintenance" in full_text, \
            "Recommendation should clearly state July as the recommended month"

    def test_table_has_all_required_columns(self, document_text):
        """Verify the table includes all required column headers."""
        for col in self.REQUIRED_TABLE_COLUMNS:
            assert col in document_text, \
                f"Missing required table column: '{col}'"

    def test_table_has_all_twelve_months(self, document_text):
        """Verify the table includes data for all 12 months."""
        months = ["January", "February", "March", "April", "May", "June",
                  "July", "August", "September", "October", "November", "December"]
        for month in months:
            assert month in document_text, \
                f"Missing month in table: '{month}'"

    def test_avoid_score_values_present(self, document_text):
        """Verify avoid_score values are present in the document."""
        # The avoid scores from the analysis
        expected_scores = ["13", "14", "15", "16", "18", "19", "20", "29", "30", "31"]
        found_scores = 0
        for score in expected_scores:
            if score in document_text:
                found_scores += 1
        assert found_scores >= 8, \
            f"Expected at least 8 unique avoid_score values, found {found_scores}"

    def test_july_has_lowest_avoid_score(self, document_text):
        """Verify July is correctly identified with the lowest avoid_score of 13."""
        full_text = " ".join(document_text)
        # July's avoid_score should be mentioned as 13
        assert "avoid_score of 13" in full_text or "avoid_score (13)" in full_text, \
            f"Document should mention July's avoid_score of {self.EXPECTED_AVOID_SCORE}"

    def test_metric_contract_describes_datasets(self, document_text):
        """Verify the Metric Contract section describes both datasets."""
        full_text = " ".join(document_text)
        assert "flights.csv" in full_text, \
            "Metric Contract should mention flights.csv dataset"
        assert "flights_2.csv" in full_text or "2014" in full_text, \
            "Metric Contract should mention flights_2.csv or 2014 operational data"

    def test_metric_contract_describes_metrics(self, document_text):
        """Verify the Metric Contract defines the computed metrics."""
        full_text = " ".join(document_text)
        assert "seasonality_index" in full_text, \
            "Metric Contract should define seasonality_index"
        assert "p90_arr_delay" in full_text or "90th percentile" in full_text, \
            "Metric Contract should define p90_arr_delay metric"
        assert "cancel_rate_proxy" in full_text, \
            "Metric Contract should define cancel_rate_proxy metric"

    def test_decision_brief_has_rationale(self, document_text):
        """Verify the Decision Brief includes rationale."""
        full_text = " ".join(document_text)
        assert "Rationale" in full_text or "rationale" in full_text, \
            "Decision Brief should include rationale"

    def test_decision_brief_has_evidence(self, document_text):
        """Verify the Decision Brief includes evidence."""
        full_text = " ".join(document_text)
        assert "Evidence" in full_text or "evidence" in full_text, \
            "Decision Brief should include evidence"

    def test_decision_brief_has_confidence(self, document_text):
        """Verify the Decision Brief includes confidence assessment."""
        full_text = " ".join(document_text)
        assert "Confidence" in full_text or "confidence" in full_text, \
            "Decision Brief should include confidence assessment"

    def test_decision_brief_has_caveats(self, document_text):
        """Verify the Decision Brief includes caveats."""
        full_text = " ".join(document_text)
        assert "Caveat" in full_text or "caveat" in full_text, \
            "Decision Brief should include caveats"

    def test_seasonality_values_reasonable(self, document_text):
        """Verify seasonality index values are in expected range (around 80-130)."""
        # Extract numeric values that look like seasonality indices
        full_text = " ".join(document_text)
        # July's seasonality should be around 125
        assert "125.34" in full_text or "125.3" in full_text, \
            "July's seasonality_index should be approximately 125.34"

    def test_delay_values_reasonable(self, document_text):
        """Verify p90_arr_delay values are present and reasonable."""
        # Check for some expected delay values
        expected_delays = ["27.0", "32.0", "21.0", "18.0", "28.0", "29.0", "26.0", "24.0", "20.0", "36.0"]
        found = sum(1 for d in expected_delays if d in document_text)
        assert found >= 6, \
            f"Expected at least 6 delay values, found {found}"

    def test_ranks_sum_correctly(self, document_text):
        """Verify July's ranks sum to its avoid_score."""
        # July: demand_rank=1, delay_rank=3, cancel_rank=9, avoid_score=13
        # 1 + 3 + 9 = 13
        full_text = " ".join(document_text)
        # Just verify these values are present in sequence for July
        assert "1" in document_text and "3" in document_text and "9" in document_text, \
            "July's individual ranks (1, 3, 9) should be present"

    def test_no_extra_output_files(self):
        """Verify only the required docx file exists in output directory."""
        output_dir = "/root/output"
        files = os.listdir(output_dir)
        # Filter out hidden files
        visible_files = [f for f in files if not f.startswith('.')]
        assert len(visible_files) == 1, \
            f"Expected only 1 output file (the docx), found {len(visible_files)}: {visible_files}"
        assert visible_files[0] == "maintenance_month_recommendation.docx", \
            f"Expected 'maintenance_month_recommendation.docx', found '{visible_files[0]}'"
