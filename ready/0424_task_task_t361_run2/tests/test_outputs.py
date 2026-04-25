import math
import os
import re
import subprocess
import zipfile

import pytest


class TestImagingRTPlanCard:
    """Tests for verifying the Imaging & RT Plan Consistency Card PowerPoint."""

    PPTX_PATH = "/root/output/imaging_rtplan_card.pptx"
    TOLERANCE = 0.000001

    EXPECTED_RESULT = {
        "title": "Imaging & RT Plan Consistency Card",
        "fov_area_ratio_ct_over_mr": 17.921635,
        "max_beam_energy_mv": 6.0,
        "cohens_d": None,
        "ct": {
            "modality": "CT",
            "manufacturer": "GE MEDICAL SYSTEMS",
            "rows": 128,
            "columns": 128,
            "pixel_spacing": [0.661468, 0.661468],
            "study_date": "20040119",
        },
        "mr": {
            "modality": "MR",
            "manufacturer": "TOSHIBA_MEC",
            "rows": 64,
            "columns": 64,
            "pixel_spacing": [0.3125, 0.3125],
            "study_date": "20040826",
        },
        "rtplan": {
            "plan_name": "Plan1",
            "plan_date": "20030903",
            "patient_position": "HFS",
        },
    }

    @pytest.fixture(scope="class")
    def pptx_content(self):
        """Extract PPTX content using markitdown."""
        result = subprocess.run(
            ["python", "-m", "markitdown", self.PPTX_PATH],
            capture_output=True,
            text=True,
        )
        return result.stdout

    def test_pptx_file_exists(self):
        """Verify the PowerPoint file was created at the specified path."""
        assert os.path.exists(self.PPTX_PATH), f"Output file not found: {self.PPTX_PATH}"

    def test_pptx_file_not_empty(self):
        """Verify the PowerPoint file has content."""
        file_size = os.path.getsize(self.PPTX_PATH)
        assert file_size > 0, "PowerPoint file is empty"
        assert file_size > 10000, f"PowerPoint file seems too small: {file_size} bytes"

    def test_pptx_valid_zip_format(self):
        """Verify the PowerPoint file is a valid ZIP archive (OOXML format)."""
        assert zipfile.is_zipfile(self.PPTX_PATH), "File is not a valid ZIP/PPTX format"

    def test_pptx_contains_required_parts(self):
        """Verify the PPTX contains required OOXML parts."""
        with zipfile.ZipFile(self.PPTX_PATH, "r") as zf:
            namelist = zf.namelist()
            assert "[Content_Types].xml" in namelist, "Missing [Content_Types].xml"
            assert any("slide1.xml" in name for name in namelist), "Missing slide1.xml"
            assert any("presentation.xml" in name for name in namelist), "Missing presentation.xml"

    def test_has_correct_title(self, pptx_content):
        """Verify the slide contains the correct title."""
        assert self.EXPECTED_RESULT["title"] in pptx_content, (
            f"Title '{self.EXPECTED_RESULT['title']}' not found in presentation"
        )

    def test_has_ct_row_data(self, pptx_content):
        """Verify CT row data is present in the table."""
        ct = self.EXPECTED_RESULT["ct"]
        assert "CT" in pptx_content, "CT modality not found"
        assert ct["manufacturer"] in pptx_content, f"CT manufacturer '{ct['manufacturer']}' not found"
        assert str(ct["rows"]) in pptx_content, f"CT rows '{ct['rows']}' not found"
        assert str(ct["columns"]) in pptx_content, f"CT columns '{ct['columns']}' not found"
        assert ct["study_date"] in pptx_content, f"CT study date '{ct['study_date']}' not found"

    def test_has_mr_row_data(self, pptx_content):
        """Verify MR row data is present in the table."""
        mr = self.EXPECTED_RESULT["mr"]
        assert "MR" in pptx_content, "MR modality not found"
        assert mr["manufacturer"].replace("_", "\\_") in pptx_content or mr["manufacturer"] in pptx_content, (
            f"MR manufacturer '{mr['manufacturer']}' not found"
        )
        assert str(mr["rows"]) in pptx_content, f"MR rows '{mr['rows']}' not found"
        assert str(mr["columns"]) in pptx_content, f"MR columns '{mr['columns']}' not found"
        assert mr["study_date"] in pptx_content, f"MR study date '{mr['study_date']}' not found"

    def test_has_rtplan_row_data(self, pptx_content):
        """Verify RTPLAN row data is present in the table."""
        rp = self.EXPECTED_RESULT["rtplan"]
        assert "RTPLAN" in pptx_content, "RTPLAN type not found"
        assert rp["plan_name"] in pptx_content, f"Plan name '{rp['plan_name']}' not found"
        assert rp["plan_date"] in pptx_content, f"Plan date '{rp['plan_date']}' not found"
        assert rp["patient_position"] in pptx_content, f"Patient position '{rp['patient_position']}' not found"

    def test_fov_area_ratio_value(self, pptx_content):
        """Verify the FOV area ratio value is correct."""
        pattern = r"FOV_area_ratio_CT_over_MR:\s*([\d.]+)"
        match = re.search(pattern, pptx_content)
        assert match, "FOV_area_ratio_CT_over_MR not found in presentation"

        actual_value = float(match.group(1))
        expected_value = self.EXPECTED_RESULT["fov_area_ratio_ct_over_mr"]
        assert math.isclose(actual_value, expected_value, rel_tol=self.TOLERANCE), (
            f"FOV_area_ratio_CT_over_MR mismatch: expected {expected_value}, got {actual_value}"
        )

    def test_max_beam_energy_value(self, pptx_content):
        """Verify the MaxBeamEnergy_MV value is correct."""
        pattern = r"MaxBeamEnergy_MV:\s*([\d.]+)"
        match = re.search(pattern, pptx_content)
        assert match, "MaxBeamEnergy_MV not found in presentation"

        actual_value = float(match.group(1))
        expected_value = self.EXPECTED_RESULT["max_beam_energy_mv"]
        assert math.isclose(actual_value, expected_value, rel_tol=self.TOLERANCE), (
            f"MaxBeamEnergy_MV mismatch: expected {expected_value}, got {actual_value}"
        )

    def test_cohens_d_value(self, pptx_content):
        """Verify the Cohen's d value is null (as expected with n=1 per group)."""
        pattern = r"cohens_d:\s*(\w+)"
        match = re.search(pattern, pptx_content)
        assert match, "cohens_d not found in presentation"

        actual_value = match.group(1)
        assert actual_value == "null", f"cohens_d should be 'null', got '{actual_value}'"

    def test_has_three_data_rows(self, pptx_content):
        """Verify the table has exactly three data rows (CT, MR, RTPLAN)."""
        lines = pptx_content.split("\n")
        table_rows = [line for line in lines if line.startswith("|") and "---" not in line]
        data_rows = [row for row in table_rows if "Type" not in row]
        assert len(data_rows) == 3, f"Expected 3 data rows (CT, MR, RTPLAN), found {len(data_rows)}"

    def test_pixel_spacing_ct_format(self, pptx_content):
        """Verify CT pixel spacing values are present."""
        ct_ps = self.EXPECTED_RESULT["ct"]["pixel_spacing"]
        ps_str = f"{ct_ps[0]}"
        assert ps_str in pptx_content or ps_str.replace(".", "\\.") in pptx_content, (
            f"CT PixelSpacing value '{ps_str}' not found"
        )

    def test_pixel_spacing_mr_format(self, pptx_content):
        """Verify MR pixel spacing values are present."""
        mr_ps = self.EXPECTED_RESULT["mr"]["pixel_spacing"]
        ps_str = f"{mr_ps[0]}"
        assert ps_str in pptx_content or ps_str.replace(".", "\\.") in pptx_content, (
            f"MR PixelSpacing value '{ps_str}' not found"
        )

    def test_computed_fov_area_ratio_derivation(self):
        """Verify the FOV area ratio is correctly derived from DICOM values."""
        ct = self.EXPECTED_RESULT["ct"]
        mr = self.EXPECTED_RESULT["mr"]

        ct_fov_x = ct["columns"] * ct["pixel_spacing"][0]
        ct_fov_y = ct["rows"] * ct["pixel_spacing"][1]
        ct_area = ct_fov_x * ct_fov_y

        mr_fov_x = mr["columns"] * mr["pixel_spacing"][0]
        mr_fov_y = mr["rows"] * mr["pixel_spacing"][1]
        mr_area = mr_fov_x * mr_fov_y

        expected_ratio = round(ct_area / mr_area, 6)
        assert math.isclose(expected_ratio, self.EXPECTED_RESULT["fov_area_ratio_ct_over_mr"], rel_tol=self.TOLERANCE), (
            f"Ratio derivation mismatch: computed {expected_ratio}, expected {self.EXPECTED_RESULT['fov_area_ratio_ct_over_mr']}"
        )

    def test_single_slide(self):
        """Verify the presentation has exactly one slide."""
        with zipfile.ZipFile(self.PPTX_PATH, "r") as zf:
            slides = [name for name in zf.namelist() if re.match(r"ppt/slides/slide\d+\.xml", name)]
            assert len(slides) == 1, f"Expected 1 slide, found {len(slides)}"

    def test_highlighted_box_content_format(self, pptx_content):
        """Verify all three computed values are present in the highlighted text box."""
        assert "FOV_area_ratio_CT_over_MR:" in pptx_content, "Missing FOV_area_ratio_CT_over_MR label"
        assert "MaxBeamEnergy_MV:" in pptx_content, "Missing MaxBeamEnergy_MV label"
        assert "cohens_d:" in pptx_content, "Missing cohens_d label"
