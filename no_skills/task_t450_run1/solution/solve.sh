#!/bin/bash
set -e

# HARBOR_RUNTIME_PATH_FIX: align synthetic workspace paths with Harbor runtime layout
TASK_DIR="$(grep -Eo '/root/harbor_workspaces/task_[A-Za-z0-9_]+' "$0" | head -n1 || true)"
if [ -n "$TASK_DIR" ]; then
  mkdir -p "$TASK_DIR"
  [ -e "$TASK_DIR/input" ] || ln -s /root "$TASK_DIR/input"
  mkdir -p "$TASK_DIR/output"
  for d in .claude .codex .opencode .goose .factory .agents .gemini; do
    [ -e "$TASK_DIR/$d" ] || ln -s "/root/$d" "$TASK_DIR/$d"
  done
  cd "$TASK_DIR"
fi

if [ -d /root/.claude/skills/dc-power-flow/scripts ]; then
  export PYTHONPATH="/root/.claude/skills/dc-power-flow/scripts:${PYTHONPATH:-}"
fi

# Generated scripts sometimes call `python`; map it to python3.
python() { python3 "$@"; }

# Some trajectories contain optional xsv diagnostics; skip if xsv is unavailable.
if ! command -v xsv >/dev/null 2>&1; then
  xsv() { return 0; }
fi

# Auto-generated solution based on execution trajectory
# This script recreates the outputs produced during synthesis

# Create /root/harbor_workspaces/task_T450_run1/expectation_tests.py
mkdir -p $(dirname /root/harbor_workspaces/task_T450_run1/expectation_tests.py)
cat << 'HEREDOC_EOF' > /root/harbor_workspaces/task_T450_run1/expectation_tests.py
"""Auto-generated expectation tests for DICOM study fingerprint task verification.

These tests verify that the task execution produces a correct JSON output file
that uniquely characterizes the three DICOM objects as specified in the task instruction.
"""

import hashlib
import json
import os
from pathlib import Path

import pytest

# Constants
OUTPUT_FILE = "/root/dicom_study_fingerprint.json"
INPUT_DIR = "/root/harbor_workspaces/task_T450_run1/input"

# Expected file keys in the output JSON
EXPECTED_FILE_KEYS = ["CT_small.dcm", "MR_small.dcm", "rtplan.dcm", "cross_file_checks"]

# Image files (have pixel data)
IMAGE_FILES = ["CT_small.dcm", "MR_small.dcm"]

# RT Plan file (no pixel data)
RTPLAN_FILE = "rtplan.dcm"


class TestOutputFileExists:
    """Tests for output file existence and basic validity."""

    def test_output_file_exists(self):
        """Verify the output JSON file was created at the expected path."""
        assert os.path.exists(OUTPUT_FILE), (
            f"Output file not found at {OUTPUT_FILE}. "
            "The task must create this file for completion."
        )

    def test_output_file_not_empty(self):
        """Verify the output file is not empty."""
        assert os.path.exists(OUTPUT_FILE), f"Output file not found at {OUTPUT_FILE}"
        file_size = os.path.getsize(OUTPUT_FILE)
        assert file_size > 0, "Output file is empty"

    def test_output_is_valid_json(self):
        """Verify the output file contains valid JSON."""
        assert os.path.exists(OUTPUT_FILE), f"Output file not found at {OUTPUT_FILE}"
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                pytest.fail(f"Output file is not valid JSON: {e}")
        assert data is not None, "JSON parsed to None"


class TestOutputJsonSchema:
    """Tests for JSON schema compliance."""

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        if not os.path.exists(OUTPUT_FILE):
            pytest.skip(f"Output file not found at {OUTPUT_FILE}")
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def test_has_all_required_top_level_keys(self, output_data):
        """Verify all required top-level keys are present."""
        for key in EXPECTED_FILE_KEYS:
            assert key in output_data, f"Missing required top-level key: '{key}'"

    def test_no_extra_top_level_keys(self, output_data):
        """Verify no unexpected top-level keys are present."""
        extra_keys = set(output_data.keys()) - set(EXPECTED_FILE_KEYS)
        assert not extra_keys, f"Unexpected top-level keys found: {extra_keys}"

    def test_file_entries_are_dicts(self, output_data):
        """Verify each file entry is a dictionary."""
        for key in ["CT_small.dcm", "MR_small.dcm", "rtplan.dcm"]:
            assert isinstance(output_data[key], dict), (
                f"Entry for '{key}' should be a dictionary, got {type(output_data[key])}"
            )

    def test_cross_file_checks_is_dict(self, output_data):
        """Verify cross_file_checks is a dictionary."""
        assert isinstance(output_data["cross_file_checks"], dict), (
            "cross_file_checks should be a dictionary"
        )


class TestImageFileMetadata:
    """Tests for CT and MR image file metadata fields."""

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        if not os.path.exists(OUTPUT_FILE):
            pytest.skip(f"Output file not found at {OUTPUT_FILE}")
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    # Required metadata fields for image files
    IMAGE_METADATA_FIELDS = [
        "Modality",
        "Manufacturer",
        "PatientID",
        "StudyDate",
        "Rows",
        "Columns",
        "PixelSpacing",
        "SliceThickness",
    ]

    @pytest.mark.parametrize("filename", IMAGE_FILES)
    def test_image_has_all_metadata_fields(self, output_data, filename):
        """Verify image files have all required metadata fields."""
        file_data = output_data[filename]
        for field in self.IMAGE_METADATA_FIELDS:
            assert field in file_data, (
                f"Missing metadata field '{field}' in {filename}"
            )

    def test_ct_modality_is_ct(self, output_data):
        """Verify CT file has Modality='CT'."""
        assert output_data["CT_small.dcm"]["Modality"] == "CT", (
            "CT file should have Modality='CT'"
        )

    def test_mr_modality_is_mr(self, output_data):
        """Verify MR file has Modality='MR'."""
        assert output_data["MR_small.dcm"]["Modality"] == "MR", (
            "MR file should have Modality='MR'"
        )

    @pytest.mark.parametrize("filename", IMAGE_FILES)
    def test_rows_is_positive_integer(self, output_data, filename):
        """Verify Rows is a positive integer."""
        rows = output_data[filename]["Rows"]
        assert isinstance(rows, int), f"Rows should be int, got {type(rows)}"
        assert rows > 0, f"Rows should be positive, got {rows}"

    @pytest.mark.parametrize("filename", IMAGE_FILES)
    def test_columns_is_positive_integer(self, output_data, filename):
        """Verify Columns is a positive integer."""
        cols = output_data[filename]["Columns"]
        assert isinstance(cols, int), f"Columns should be int, got {type(cols)}"
        assert cols > 0, f"Columns should be positive, got {cols}"

    @pytest.mark.parametrize("filename", IMAGE_FILES)
    def test_pixel_spacing_format(self, output_data, filename):
        """Verify PixelSpacing is a list of two numbers or None."""
        ps = output_data[filename]["PixelSpacing"]
        if ps is not None:
            assert isinstance(ps, list), f"PixelSpacing should be list, got {type(ps)}"
            assert len(ps) == 2, f"PixelSpacing should have 2 elements, got {len(ps)}"
            for i, val in enumerate(ps):
                assert isinstance(val, (int, float)), (
                    f"PixelSpacing[{i}] should be numeric, got {type(val)}"
                )


class TestImageFilePixelStatistics:
    """Tests for pixel statistics in CT and MR files."""

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        if not os.path.exists(OUTPUT_FILE):
            pytest.skip(f"Output file not found at {OUTPUT_FILE}")
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    # Required pixel statistics fields
    PIXEL_STATS_FIELDS = ["min", "max", "mean", "std", "nonzero_count", "pixel_md5"]

    @pytest.mark.parametrize("filename", IMAGE_FILES)
    def test_image_has_all_pixel_stats_fields(self, output_data, filename):
        """Verify image files have all required pixel statistics fields."""
        file_data = output_data[filename]
        for field in self.PIXEL_STATS_FIELDS:
            assert field in file_data, (
                f"Missing pixel statistics field '{field}' in {filename}"
            )

    @pytest.mark.parametrize("filename", IMAGE_FILES)
    def test_min_is_numeric(self, output_data, filename):
        """Verify min is a number."""
        min_val = output_data[filename]["min"]
        assert isinstance(min_val, (int, float)), (
            f"min should be numeric, got {type(min_val)}"
        )

    @pytest.mark.parametrize("filename", IMAGE_FILES)
    def test_max_is_numeric(self, output_data, filename):
        """Verify max is a number."""
        max_val = output_data[filename]["max"]
        assert isinstance(max_val, (int, float)), (
            f"max should be numeric, got {type(max_val)}"
        )

    @pytest.mark.parametrize("filename", IMAGE_FILES)
    def test_min_less_than_or_equal_max(self, output_data, filename):
        """Verify min <= max."""
        min_val = output_data[filename]["min"]
        max_val = output_data[filename]["max"]
        assert min_val <= max_val, f"min ({min_val}) should be <= max ({max_val})"

    @pytest.mark.parametrize("filename", IMAGE_FILES)
    def test_mean_is_numeric(self, output_data, filename):
        """Verify mean is a number."""
        mean_val = output_data[filename]["mean"]
        assert isinstance(mean_val, (int, float)), (
            f"mean should be numeric, got {type(mean_val)}"
        )

    @pytest.mark.parametrize("filename", IMAGE_FILES)
    def test_mean_between_min_max(self, output_data, filename):
        """Verify min <= mean <= max."""
        min_val = output_data[filename]["min"]
        max_val = output_data[filename]["max"]
        mean_val = output_data[filename]["mean"]
        assert min_val <= mean_val <= max_val, (
            f"mean ({mean_val}) should be between min ({min_val}) and max ({max_val})"
        )

    @pytest.mark.parametrize("filename", IMAGE_FILES)
    def test_std_is_non_negative(self, output_data, filename):
        """Verify std is non-negative."""
        std_val = output_data[filename]["std"]
        assert isinstance(std_val, (int, float)), (
            f"std should be numeric, got {type(std_val)}"
        )
        assert std_val >= 0, f"std should be non-negative, got {std_val}"

    @pytest.mark.parametrize("filename", IMAGE_FILES)
    def test_nonzero_count_is_non_negative_integer(self, output_data, filename):
        """Verify nonzero_count is a non-negative integer."""
        nz_count = output_data[filename]["nonzero_count"]
        assert isinstance(nz_count, int), (
            f"nonzero_count should be int, got {type(nz_count)}"
        )
        assert nz_count >= 0, f"nonzero_count should be non-negative, got {nz_count}"

    @pytest.mark.parametrize("filename", IMAGE_FILES)
    def test_pixel_md5_is_valid_hex_string(self, output_data, filename):
        """Verify pixel_md5 is a valid 32-character hex string."""
        md5_val = output_data[filename]["pixel_md5"]
        assert isinstance(md5_val, str), f"pixel_md5 should be string, got {type(md5_val)}"
        assert len(md5_val) == 32, (
            f"pixel_md5 should be 32 characters, got {len(md5_val)}"
        )
        # Verify it's a valid hex string
        try:
            int(md5_val, 16)
        except ValueError:
            pytest.fail(f"pixel_md5 '{md5_val}' is not a valid hex string")


class TestRTPlanMetadata:
    """Tests for RT Plan file metadata fields."""

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        if not os.path.exists(OUTPUT_FILE):
            pytest.skip(f"Output file not found at {OUTPUT_FILE}")
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    # Required semantic fields for RT Plan
    RTPLAN_FIELDS = [
        "Modality",
        "RTPlanName",
        "ApprovalStatus",
        "PatientID",
        "PatientPosition",
        "BeamCount",
        "TotalMeterset",
    ]

    def test_rtplan_has_all_required_fields(self, output_data):
        """Verify RT Plan file has all required semantic fields."""
        rtplan_data = output_data[RTPLAN_FILE]
        for field in self.RTPLAN_FIELDS:
            assert field in rtplan_data, (
                f"Missing field '{field}' in {RTPLAN_FILE}"
            )

    def test_rtplan_modality_is_rtplan(self, output_data):
        """Verify RT Plan file has Modality='RTPLAN'."""
        assert output_data[RTPLAN_FILE]["Modality"] == "RTPLAN", (
            "RT Plan file should have Modality='RTPLAN'"
        )

    def test_rtplan_beam_count_is_non_negative_integer(self, output_data):
        """Verify BeamCount is a non-negative integer."""
        bc = output_data[RTPLAN_FILE]["BeamCount"]
        assert isinstance(bc, int), f"BeamCount should be int, got {type(bc)}"
        assert bc >= 0, f"BeamCount should be non-negative, got {bc}"

    def test_rtplan_total_meterset_is_numeric(self, output_data):
        """Verify TotalMeterset is a float or int."""
        tm = output_data[RTPLAN_FILE]["TotalMeterset"]
        assert isinstance(tm, (int, float)), (
            f"TotalMeterset should be numeric, got {type(tm)}"
        )

    def test_rtplan_has_no_pixel_stats(self, output_data):
        """Verify RT Plan file does NOT have pixel statistics fields."""
        rtplan_data = output_data[RTPLAN_FILE]
        pixel_stats = ["min", "max", "mean", "std", "nonzero_count", "pixel_md5"]
        for field in pixel_stats:
            assert field not in rtplan_data, (
                f"RT Plan should not have pixel statistics field '{field}'"
            )

    def test_rtplan_name_is_string(self, output_data):
        """Verify RTPlanName is a string or None."""
        name = output_data[RTPLAN_FILE]["RTPlanName"]
        assert name is None or isinstance(name, str), (
            f"RTPlanName should be string or None, got {type(name)}"
        )

    def test_rtplan_approval_status_is_string(self, output_data):
        """Verify ApprovalStatus is a string or None."""
        status = output_data[RTPLAN_FILE]["ApprovalStatus"]
        assert status is None or isinstance(status, str), (
            f"ApprovalStatus should be string or None, got {type(status)}"
        )


class TestCrossFileChecks:
    """Tests for cross_file_checks section."""

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        if not os.path.exists(OUTPUT_FILE):
            pytest.skip(f"Output file not found at {OUTPUT_FILE}")
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    CROSS_FILE_FIELDS = ["patient_id_all_equal", "modalities", "earliest_study_date"]

    def test_has_all_cross_file_check_fields(self, output_data):
        """Verify all required cross_file_checks fields are present."""
        checks = output_data["cross_file_checks"]
        for field in self.CROSS_FILE_FIELDS:
            assert field in checks, f"Missing cross_file_checks field: '{field}'"

    def test_patient_id_all_equal_is_boolean(self, output_data):
        """Verify patient_id_all_equal is a boolean."""
        val = output_data["cross_file_checks"]["patient_id_all_equal"]
        assert isinstance(val, bool), (
            f"patient_id_all_equal should be bool, got {type(val)}"
        )

    def test_modalities_is_list(self, output_data):
        """Verify modalities is a list."""
        mods = output_data["cross_file_checks"]["modalities"]
        assert isinstance(mods, list), f"modalities should be list, got {type(mods)}"

    def test_modalities_contains_expected_values(self, output_data):
        """Verify modalities contains CT, MR, and RTPLAN."""
        mods = output_data["cross_file_checks"]["modalities"]
        expected = {"CT", "MR", "RTPLAN"}
        actual = set(mods)
        assert actual == expected, (
            f"modalities should contain exactly {expected}, got {actual}"
        )

    def test_modalities_is_sorted(self, output_data):
        """Verify modalities list is sorted."""
        mods = output_data["cross_file_checks"]["modalities"]
        assert mods == sorted(mods), (
            f"modalities should be sorted, got {mods}"
        )

    def test_modalities_has_unique_values(self, output_data):
        """Verify modalities list has unique values."""
        mods = output_data["cross_file_checks"]["modalities"]
        assert len(mods) == len(set(mods)), (
            f"modalities should have unique values, got {mods}"
        )

    def test_earliest_study_date_is_string(self, output_data):
        """Verify earliest_study_date is a string."""
        date = output_data["cross_file_checks"]["earliest_study_date"]
        assert isinstance(date, str), (
            f"earliest_study_date should be string, got {type(date)}"
        )

    def test_earliest_study_date_format(self, output_data):
        """Verify earliest_study_date is in YYYYMMDD format."""
        date = output_data["cross_file_checks"]["earliest_study_date"]
        # Should be 8 digits in YYYYMMDD format
        assert len(date) == 8, (
            f"earliest_study_date should be 8 characters (YYYYMMDD), got {len(date)}"
        )
        assert date.isdigit(), (
            f"earliest_study_date should be all digits, got '{date}'"
        )
        # Basic date validation
        year = int(date[:4])
        month = int(date[4:6])
        day = int(date[6:8])
        assert 1900 <= year <= 2100, f"Invalid year in date: {year}"
        assert 1 <= month <= 12, f"Invalid month in date: {month}"
        assert 1 <= day <= 31, f"Invalid day in date: {day}"


class TestDataConsistency:
    """Tests for data consistency across the output."""

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        if not os.path.exists(OUTPUT_FILE):
            pytest.skip(f"Output file not found at {OUTPUT_FILE}")
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def test_patient_id_consistency_check(self, output_data):
        """Verify patient_id_all_equal matches actual PatientID comparison."""
        patient_ids = []
        for filename in ["CT_small.dcm", "MR_small.dcm", "rtplan.dcm"]:
            pid = output_data[filename].get("PatientID")
            patient_ids.append(pid)

        # If any is None, they're not all equal
        if None in patient_ids:
            expected_equal = False
        else:
            expected_equal = len(set(patient_ids)) == 1

        actual_equal = output_data["cross_file_checks"]["patient_id_all_equal"]
        assert actual_equal == expected_equal, (
            f"patient_id_all_equal ({actual_equal}) doesn't match actual PatientIDs: {patient_ids}"
        )

    def test_modalities_match_file_entries(self, output_data):
        """Verify modalities list matches the Modality fields in file entries."""
        collected_modalities = set()
        for filename in ["CT_small.dcm", "MR_small.dcm", "rtplan.dcm"]:
            mod = output_data[filename].get("Modality")
            if mod:
                collected_modalities.add(mod)

        cross_modalities = set(output_data["cross_file_checks"]["modalities"])
        assert collected_modalities == cross_modalities, (
            f"Modalities in cross_file_checks ({cross_modalities}) "
            f"don't match file entries ({collected_modalities})"
        )

    def test_earliest_date_is_minimum(self, output_data):
        """Verify earliest_study_date is the minimum of all StudyDate values."""
        study_dates = []
        for filename in ["CT_small.dcm", "MR_small.dcm", "rtplan.dcm"]:
            date = output_data[filename].get("StudyDate")
            if date is not None:
                study_dates.append(date)

        if study_dates:
            expected_earliest = min(study_dates)
            actual_earliest = output_data["cross_file_checks"]["earliest_study_date"]
            assert actual_earliest == expected_earliest, (
                f"earliest_study_date ({actual_earliest}) should be min of {study_dates}"
            )


class TestJsonFormatting:
    """Tests for JSON formatting requirements."""

    def test_file_is_utf8_encoded(self):
        """Verify the file is UTF-8 encoded."""
        if not os.path.exists(OUTPUT_FILE):
            pytest.skip(f"Output file not found at {OUTPUT_FILE}")
        with open(OUTPUT_FILE, "rb") as f:
            content = f.read()
        try:
            content.decode("utf-8")
        except UnicodeDecodeError:
            pytest.fail("Output file is not valid UTF-8")

    def test_json_is_pretty_printed(self):
        """Verify the JSON uses pretty-printing (multiple lines, indentation)."""
        if not os.path.exists(OUTPUT_FILE):
            pytest.skip(f"Output file not found at {OUTPUT_FILE}")
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            content = f.read()

        # Pretty-printed JSON should have multiple lines
        lines = content.strip().split("\n")
        assert len(lines) > 1, "JSON should be pretty-printed with multiple lines"

    def test_json_uses_two_space_indentation(self):
        """Verify the JSON uses 2-space indentation."""
        if not os.path.exists(OUTPUT_FILE):
            pytest.skip(f"Output file not found at {OUTPUT_FILE}")
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            content = f.read()

        # Check for 2-space indentation pattern
        # Lines should be indented with multiples of 2 spaces
        lines = content.split("\n")
        for line in lines:
            if line and not line.startswith("{") and not line.startswith("}"):
                stripped = line.lstrip(" ")
                spaces = len(line) - len(stripped)
                if spaces > 0:
                    # Indentation should be multiple of 2
                    assert spaces % 2 == 0, (
                        f"Expected 2-space indentation, found {spaces} spaces in line: '{line}'"
                    )
                    break  # Just check first indented line


class TestSpecificExpectedValues:
    """Tests for specific expected values based on the DICOM file contents."""

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        if not os.path.exists(OUTPUT_FILE):
            pytest.skip(f"Output file not found at {OUTPUT_FILE}")
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def test_ct_manufacturer_is_ge(self, output_data):
        """Verify CT file Manufacturer is GE MEDICAL SYSTEMS."""
        manufacturer = output_data["CT_small.dcm"]["Manufacturer"]
        assert manufacturer is not None, "CT Manufacturer should not be None"
        assert "GE" in manufacturer.upper(), (
            f"CT Manufacturer should contain 'GE', got '{manufacturer}'"
        )

    def test_mr_manufacturer_is_toshiba(self, output_data):
        """Verify MR file Manufacturer is TOSHIBA."""
        manufacturer = output_data["MR_small.dcm"]["Manufacturer"]
        assert manufacturer is not None, "MR Manufacturer should not be None"
        assert "TOSHIBA" in manufacturer.upper(), (
            f"MR Manufacturer should contain 'TOSHIBA', got '{manufacturer}'"
        )

    def test_patient_ids_are_different(self, output_data):
        """Verify the three files have different PatientIDs."""
        ct_pid = output_data["CT_small.dcm"].get("PatientID")
        mr_pid = output_data["MR_small.dcm"].get("PatientID")
        rt_pid = output_data["rtplan.dcm"].get("PatientID")

        # Based on the DICOM files, they should have different patient IDs
        patient_ids = {ct_pid, mr_pid, rt_pid}
        # Remove None if present
        patient_ids.discard(None)

        # At least some should be different
        assert len(patient_ids) > 1 or None in [ct_pid, mr_pid, rt_pid], (
            "Expected different PatientIDs across files"
        )

    def test_patient_id_all_equal_is_false(self, output_data):
        """Verify patient_id_all_equal is False (files have different PatientIDs)."""
        # Based on visible DICOM data: CT has 1CT1, MR has 4MR1, RT has id00001
        assert output_data["cross_file_checks"]["patient_id_all_equal"] is False, (
            "patient_id_all_equal should be False as files have different PatientIDs"
        )

    def test_rtplan_has_beam_sequence(self, output_data):
        """Verify RT Plan BeamCount is at least 1 (visible in rtplan.dcm)."""
        beam_count = output_data["rtplan.dcm"]["BeamCount"]
        assert beam_count >= 1, (
            f"RT Plan should have at least 1 beam, got {beam_count}"
        )

    def test_ct_has_reasonable_dimensions(self, output_data):
        """Verify CT image has reasonable dimensions."""
        rows = output_data["CT_small.dcm"]["Rows"]
        cols = output_data["CT_small.dcm"]["Columns"]
        # CT_small.dcm appears to be a small test image
        assert rows > 0 and cols > 0, "CT should have positive dimensions"
        assert rows <= 1024 and cols <= 1024, "CT dimensions seem too large for 'small' image"

    def test_mr_has_reasonable_dimensions(self, output_data):
        """Verify MR image has reasonable dimensions."""
        rows = output_data["MR_small.dcm"]["Rows"]
        cols = output_data["MR_small.dcm"]["Columns"]
        # MR_small.dcm appears to be a small test image
        assert rows > 0 and cols > 0, "MR should have positive dimensions"
        assert rows <= 1024 and cols <= 1024, "MR dimensions seem too large for 'small' image"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

HEREDOC_EOF

# Execute command
ls -la /root/harbor_workspaces/task_T450_run1/output 2>/dev/null || mkdir -p /root/harbor_workspaces/task_T450_run1/output && echo "Output directory ready"

# Create /root/harbor_workspaces/task_T450_run1/generate_fingerprint.py
mkdir -p $(dirname /root/harbor_workspaces/task_T450_run1/generate_fingerprint.py)
cat << 'HEREDOC_EOF' > /root/harbor_workspaces/task_T450_run1/generate_fingerprint.py
#!/usr/bin/env python3
"""
Generate a DICOM study fingerprint JSON from three DICOM files.
"""

import json
import hashlib
import numpy as np
import pydicom


def extract_image_metadata(ds):
    """Extract metadata fields for CT/MR image objects."""
    fields = [
        'Modality', 'Manufacturer', 'PatientID', 'StudyDate',
        'Rows', 'Columns', 'PixelSpacing', 'SliceThickness'
    ]
    metadata = {}
    for field in fields:
        value = getattr(ds, field, None)
        # Convert pydicom types to native Python types for JSON serialization
        if value is not None:
            if isinstance(value, pydicom.multival.MultiValue):
                # PixelSpacing is a list of floats
                metadata[field] = [float(v) for v in value]
            elif isinstance(value, (int, float, str)):
                metadata[field] = value
            elif hasattr(value, 'original_string'):
                # For DSfloat, DSdecimal, etc.
                metadata[field] = float(value)
            elif hasattr(value, '__int__'):
                metadata[field] = int(value)
            else:
                metadata[field] = str(value)
        else:
            metadata[field] = None
    return metadata


def compute_pixel_stats(ds):
    """Compute pixel statistics from ds.pixel_array."""
    try:
        # Try to decompress if needed
        try:
            arr = ds.pixel_array
        except Exception:
            ds.decompress()
            arr = ds.pixel_array

        stats = {
            "min": int(arr.min()),
            "max": int(arr.max()),
            "mean": float(arr.mean()),
            "std": float(np.std(arr, ddof=0)),  # population std
            "nonzero_count": int(np.count_nonzero(arr))
        }
        return stats
    except Exception as e:
        print(f"Warning: Could not compute pixel stats: {e}")
        return None


def compute_pixel_md5(ds):
    """Compute MD5 hash of raw PixelData bytes."""
    if hasattr(ds, 'PixelData'):
        pixel_data = ds.PixelData
        return hashlib.md5(pixel_data).hexdigest()
    return None


def extract_rtplan_metadata(ds):
    """Extract semantic fields for RT Plan object."""
    metadata = {}

    # Basic fields
    for field in ['Modality', 'RTPlanName', 'ApprovalStatus', 'PatientID', 'PatientPosition']:
        value = getattr(ds, field, None)
        if value is not None:
            metadata[field] = str(value)
        else:
            metadata[field] = None

    # BeamCount
    beam_seq = getattr(ds, 'BeamSequence', None)
    if beam_seq is not None:
        metadata['BeamCount'] = len(beam_seq)

        # TotalMeterset - sum of FinalCumulativeMetersetWeight across all beams
        total_meterset = 0.0
        for beam in beam_seq:
            fcmw = getattr(beam, 'FinalCumulativeMetersetWeight', None)
            if fcmw is not None:
                total_meterset += float(fcmw)
        metadata['TotalMeterset'] = total_meterset
    else:
        metadata['BeamCount'] = 0
        metadata['TotalMeterset'] = 0.0

    return metadata


def build_cross_file_checks(datasets):
    """Build cross-file checks from extracted datasets."""
    ct_data, mr_data, rp_data = datasets

    # patient_id_all_equal
    patient_ids = [
        ct_data.get('PatientID'),
        mr_data.get('PatientID'),
        rp_data.get('PatientID')
    ]

    if any(pid is None for pid in patient_ids):
        patient_id_all_equal = False
    else:
        patient_id_all_equal = (patient_ids[0] == patient_ids[1] == patient_ids[2])

    # modalities - sorted unique list
    modalities = []
    for data in [ct_data, mr_data, rp_data]:
        mod = data.get('Modality')
        if mod is not None:
            modalities.append(mod)
    modalities = sorted(set(modalities))

    # earliest_study_date
    study_dates = []
    for data in [ct_data, mr_data, rp_data]:
        sd = data.get('StudyDate')
        if sd is not None:
            study_dates.append(sd)

    if study_dates:
        earliest_study_date = min(study_dates)
    else:
        earliest_study_date = None

    return {
        "patient_id_all_equal": patient_id_all_equal,
        "modalities": modalities,
        "earliest_study_date": earliest_study_date
    }


def main():
    # File paths
    ct_path = "/root/CT_small.dcm"
    mr_path = "/root/MR_small.dcm"
    rp_path = "/root/rtplan.dcm"
    output_path = "/root/dicom_study_fingerprint.json"

    # Read DICOM files
    print("Reading DICOM files...")
    ct = pydicom.dcmread(ct_path)
    mr = pydicom.dcmread(mr_path)
    rp = pydicom.dcmread(rp_path)

    # Process CT
    print("Processing CT...")
    ct_result = extract_image_metadata(ct)
    ct_stats = compute_pixel_stats(ct)
    if ct_stats:
        ct_result.update(ct_stats)
    ct_result['pixel_md5'] = compute_pixel_md5(ct)

    # Process MR
    print("Processing MR...")
    mr_result = extract_image_metadata(mr)
    mr_stats = compute_pixel_stats(mr)
    if mr_stats:
        mr_result.update(mr_stats)
    mr_result['pixel_md5'] = compute_pixel_md5(mr)

    # Process RT Plan
    print("Processing RT Plan...")
    rp_result = extract_rtplan_metadata(rp)

    # Build cross-file checks
    print("Building cross-file checks...")
    cross_checks = build_cross_file_checks([ct_result, mr_result, rp_result])

    # Combine into final output with required ordering
    # Use a regular dict (Python 3.7+ preserves insertion order)
    output = {
        "CT_small.dcm": ct_result,
        "MR_small.dcm": mr_result,
        "rtplan.dcm": rp_result,
        "cross_file_checks": cross_checks
    }

    # Write output JSON
    print(f"Writing output to {output_path}...")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, sort_keys=False)
        f.write("\n")

    print("Done!")

    # Verify the output
    print("\n--- Output Preview ---")
    with open(output_path, "r", encoding="utf-8") as f:
        print(f.read())


if __name__ == "__main__":
    main()

HEREDOC_EOF

# Execute command
pip3 install pydicom numpy --quiet 2>/dev/null || true; python3 generate_fingerprint.py

# Execute command
python -c "import json; json.load(open('/root/dicom_study_fingerprint.json')); print('JSON is valid')"
