"""Auto-generated expectation tests for RT Plan imaging reference check verification.

These tests verify that the task execution produces correct outputs
based on the instruction requirements for creating a JSON consistency check
artifact proving RT Plan's referenced imaging context matches the provided DICOM files.
"""

import json
import os
from pathlib import Path

import pytest

# Constants
OUTPUT_FILE = "/root/rtplan_imaging_reference_check.json"
INPUT_DIR = "/root/harbor_workspaces/task_T446_run2/input"
CT_FILE = os.path.join(INPUT_DIR, "CT_small.dcm")
MR_FILE = os.path.join(INPUT_DIR, "MR_small.dcm")
RTPLAN_FILE = os.path.join(INPUT_DIR, "rtplan.dcm")


class TestOutputFileExists:
    """Tests for output file existence and accessibility."""

    def test_output_file_exists(self):
        """Verify output file was created at the specified path."""
        assert os.path.exists(OUTPUT_FILE), (
            f"Output file not found at {OUTPUT_FILE}. "
            "The task requires writing the JSON to this exact path."
        )

    def test_output_file_is_file(self):
        """Verify output path is a file, not a directory."""
        assert os.path.isfile(OUTPUT_FILE), (
            f"Output path {OUTPUT_FILE} exists but is not a file."
        )

    def test_output_file_not_empty(self):
        """Verify output file is not empty."""
        assert os.path.getsize(OUTPUT_FILE) > 0, (
            "Output file exists but is empty."
        )


class TestOutputFormatValidity:
    """Tests for valid JSON format and structure."""

    def test_output_is_valid_json(self):
        """Verify output is valid, parseable JSON."""
        with open(OUTPUT_FILE, "r") as f:
            content = f.read()
        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            pytest.fail(f"Output file is not valid JSON: {e}")
        assert data is not None, "JSON parsed to None"

    def test_output_is_json_object(self):
        """Verify output is a JSON object (dict), not array or primitive."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        assert isinstance(data, dict), (
            f"Output should be a JSON object, got {type(data).__name__}"
        )


class TestRequiredFields:
    """Tests for required schema fields presence."""

    @pytest.fixture
    def output_data(self):
        """Load output JSON data."""
        with open(OUTPUT_FILE, "r") as f:
            return json.load(f)

    def test_has_ct_sop_instance_uid(self, output_data):
        """Verify ct_sop_instance_uid field exists."""
        assert "ct_sop_instance_uid" in output_data, (
            "Missing required field: ct_sop_instance_uid"
        )

    def test_has_mr_sop_instance_uid(self, output_data):
        """Verify mr_sop_instance_uid field exists."""
        assert "mr_sop_instance_uid" in output_data, (
            "Missing required field: mr_sop_instance_uid"
        )

    def test_has_rtplan_total_reference_count(self, output_data):
        """Verify rtplan_total_reference_count field exists."""
        assert "rtplan_total_reference_count" in output_data, (
            "Missing required field: rtplan_total_reference_count"
        )

    def test_has_ct_is_referenced_by_rtplan(self, output_data):
        """Verify ct_is_referenced_by_rtplan field exists."""
        assert "ct_is_referenced_by_rtplan" in output_data, (
            "Missing required field: ct_is_referenced_by_rtplan"
        )

    def test_has_mr_is_referenced_by_rtplan(self, output_data):
        """Verify mr_is_referenced_by_rtplan field exists."""
        assert "mr_is_referenced_by_rtplan" in output_data, (
            "Missing required field: mr_is_referenced_by_rtplan"
        )

    def test_has_referenced_match_count(self, output_data):
        """Verify referenced_match_count field exists."""
        assert "referenced_match_count" in output_data, (
            "Missing required field: referenced_match_count"
        )


class TestFieldTypes:
    """Tests for correct data types of all fields."""

    @pytest.fixture
    def output_data(self):
        """Load output JSON data."""
        with open(OUTPUT_FILE, "r") as f:
            return json.load(f)

    def test_ct_sop_instance_uid_is_string(self, output_data):
        """Verify ct_sop_instance_uid is a string."""
        assert isinstance(output_data["ct_sop_instance_uid"], str), (
            f"ct_sop_instance_uid should be string, got {type(output_data['ct_sop_instance_uid']).__name__}"
        )

    def test_mr_sop_instance_uid_is_string(self, output_data):
        """Verify mr_sop_instance_uid is a string."""
        assert isinstance(output_data["mr_sop_instance_uid"], str), (
            f"mr_sop_instance_uid should be string, got {type(output_data['mr_sop_instance_uid']).__name__}"
        )

    def test_rtplan_total_reference_count_is_integer(self, output_data):
        """Verify rtplan_total_reference_count is an integer."""
        assert isinstance(output_data["rtplan_total_reference_count"], int), (
            f"rtplan_total_reference_count should be int, got {type(output_data['rtplan_total_reference_count']).__name__}"
        )

    def test_ct_is_referenced_by_rtplan_is_boolean(self, output_data):
        """Verify ct_is_referenced_by_rtplan is a boolean."""
        assert isinstance(output_data["ct_is_referenced_by_rtplan"], bool), (
            f"ct_is_referenced_by_rtplan should be bool, got {type(output_data['ct_is_referenced_by_rtplan']).__name__}"
        )

    def test_mr_is_referenced_by_rtplan_is_boolean(self, output_data):
        """Verify mr_is_referenced_by_rtplan is a boolean."""
        assert isinstance(output_data["mr_is_referenced_by_rtplan"], bool), (
            f"mr_is_referenced_by_rtplan should be bool, got {type(output_data['mr_is_referenced_by_rtplan']).__name__}"
        )

    def test_referenced_match_count_is_integer(self, output_data):
        """Verify referenced_match_count is an integer."""
        assert isinstance(output_data["referenced_match_count"], int), (
            f"referenced_match_count should be int, got {type(output_data['referenced_match_count']).__name__}"
        )


class TestSchemaConstraints:
    """Tests for schema-level constraints and no extra fields."""

    EXPECTED_KEYS = {
        "ct_sop_instance_uid",
        "mr_sop_instance_uid",
        "rtplan_total_reference_count",
        "ct_is_referenced_by_rtplan",
        "mr_is_referenced_by_rtplan",
        "referenced_match_count",
    }

    @pytest.fixture
    def output_data(self):
        """Load output JSON data."""
        with open(OUTPUT_FILE, "r") as f:
            return json.load(f)

    def test_no_extra_keys(self, output_data):
        """Verify no extra keys beyond the required schema."""
        actual_keys = set(output_data.keys())
        extra_keys = actual_keys - self.EXPECTED_KEYS
        assert len(extra_keys) == 0, (
            f"Output contains extra keys not in schema: {extra_keys}"
        )

    def test_exact_key_count(self, output_data):
        """Verify output has exactly 6 keys as specified in schema."""
        assert len(output_data) == 6, (
            f"Output should have exactly 6 keys, has {len(output_data)}"
        )


class TestValueConstraints:
    """Tests for logical value constraints."""

    @pytest.fixture
    def output_data(self):
        """Load output JSON data."""
        with open(OUTPUT_FILE, "r") as f:
            return json.load(f)

    def test_sop_instance_uid_not_empty(self, output_data):
        """Verify SOP Instance UIDs are not empty strings."""
        assert len(output_data["ct_sop_instance_uid"]) > 0, (
            "ct_sop_instance_uid should not be empty"
        )
        assert len(output_data["mr_sop_instance_uid"]) > 0, (
            "mr_sop_instance_uid should not be empty"
        )

    def test_sop_instance_uid_format(self, output_data):
        """Verify SOP Instance UIDs follow DICOM UID format (dot-separated numbers)."""
        ct_uid = output_data["ct_sop_instance_uid"]
        mr_uid = output_data["mr_sop_instance_uid"]

        # DICOM UIDs consist of numeric components separated by dots
        for uid, name in [(ct_uid, "ct_sop_instance_uid"), (mr_uid, "mr_sop_instance_uid")]:
            parts = uid.split(".")
            assert len(parts) >= 2, f"{name} should have dot-separated format"
            for part in parts:
                assert part.isdigit() or part == "", (
                    f"{name} contains non-numeric component: {part}"
                )

    def test_ct_and_mr_uids_are_different(self, output_data):
        """Verify CT and MR have different SOP Instance UIDs."""
        assert output_data["ct_sop_instance_uid"] != output_data["mr_sop_instance_uid"], (
            "CT and MR should have different SOP Instance UIDs"
        )

    def test_rtplan_total_reference_count_non_negative(self, output_data):
        """Verify rtplan_total_reference_count is non-negative."""
        assert output_data["rtplan_total_reference_count"] >= 0, (
            f"rtplan_total_reference_count should be >= 0, got {output_data['rtplan_total_reference_count']}"
        )

    def test_referenced_match_count_valid_range(self, output_data):
        """Verify referenced_match_count is between 0 and 2 (can only match CT, MR, or both)."""
        count = output_data["referenced_match_count"]
        assert 0 <= count <= 2, (
            f"referenced_match_count should be 0, 1, or 2, got {count}"
        )

    def test_referenced_match_count_consistency(self, output_data):
        """Verify referenced_match_count equals sum of boolean reference flags."""
        ct_ref = output_data["ct_is_referenced_by_rtplan"]
        mr_ref = output_data["mr_is_referenced_by_rtplan"]
        expected_count = int(ct_ref) + int(mr_ref)
        actual_count = output_data["referenced_match_count"]
        assert actual_count == expected_count, (
            f"referenced_match_count ({actual_count}) should equal sum of "
            f"ct_is_referenced ({ct_ref}) + mr_is_referenced ({mr_ref}) = {expected_count}"
        )

    def test_referenced_match_count_not_greater_than_total(self, output_data):
        """Verify referenced_match_count is not greater than rtplan_total_reference_count."""
        match_count = output_data["referenced_match_count"]
        total_count = output_data["rtplan_total_reference_count"]
        # Note: It's possible to have 0 matches even with many references
        # But if there are matches, total should be at least that many
        if match_count > 0:
            assert total_count >= match_count, (
                f"rtplan_total_reference_count ({total_count}) should be >= "
                f"referenced_match_count ({match_count})"
            )


class TestDeterminism:
    """Tests for deterministic output (no randomness, no timestamps)."""

    @pytest.fixture
    def output_data(self):
        """Load output JSON data."""
        with open(OUTPUT_FILE, "r") as f:
            return json.load(f)

    def test_no_timestamp_fields(self, output_data):
        """Verify output contains no timestamp-related fields."""
        timestamp_keywords = ["timestamp", "time", "date", "created", "modified"]
        for key in output_data.keys():
            key_lower = key.lower()
            for kw in timestamp_keywords:
                assert kw not in key_lower, (
                    f"Field '{key}' appears to be timestamp-related, violating determinism requirement"
                )

    def test_no_random_fields(self, output_data):
        """Verify output contains no random/uuid fields beyond SOP Instance UIDs."""
        random_keywords = ["random", "uuid", "guid"]
        for key in output_data.keys():
            key_lower = key.lower()
            # SOP Instance UIDs are allowed even though they contain 'uid'
            if "sop_instance_uid" in key_lower:
                continue
            for kw in random_keywords:
                assert kw not in key_lower, (
                    f"Field '{key}' appears to be random-related, violating determinism requirement"
                )


class TestDICOMConsistency:
    """Tests that verify output values match actual DICOM file contents using pydicom."""

    @pytest.fixture
    def output_data(self):
        """Load output JSON data."""
        with open(OUTPUT_FILE, "r") as f:
            return json.load(f)

    def test_ct_uid_matches_dicom_file(self, output_data):
        """Verify ct_sop_instance_uid matches actual CT DICOM file."""
        try:
            import pydicom
        except ImportError:
            pytest.skip("pydicom not installed, skipping DICOM verification")

        ds = pydicom.dcmread(CT_FILE)
        actual_uid = str(ds.SOPInstanceUID)
        output_uid = output_data["ct_sop_instance_uid"]

        assert output_uid == actual_uid, (
            f"ct_sop_instance_uid mismatch: output has '{output_uid}', "
            f"but CT DICOM file has '{actual_uid}'"
        )

    def test_mr_uid_matches_dicom_file(self, output_data):
        """Verify mr_sop_instance_uid matches actual MR DICOM file."""
        try:
            import pydicom
        except ImportError:
            pytest.skip("pydicom not installed, skipping DICOM verification")

        ds = pydicom.dcmread(MR_FILE)
        actual_uid = str(ds.SOPInstanceUID)
        output_uid = output_data["mr_sop_instance_uid"]

        assert output_uid == actual_uid, (
            f"mr_sop_instance_uid mismatch: output has '{output_uid}', "
            f"but MR DICOM file has '{actual_uid}'"
        )

    def test_ct_reference_flag_correctness(self, output_data):
        """Verify ct_is_referenced_by_rtplan is correct based on RT Plan references."""
        try:
            import pydicom
        except ImportError:
            pytest.skip("pydicom not installed, skipping DICOM verification")

        # Get CT SOP Instance UID
        ct_ds = pydicom.dcmread(CT_FILE)
        ct_uid = str(ct_ds.SOPInstanceUID)

        # Get all referenced SOP Instance UIDs from RT Plan
        rtplan_ds = pydicom.dcmread(RTPLAN_FILE)
        referenced_uids = self._extract_all_referenced_sop_uids(rtplan_ds)

        expected_flag = ct_uid in referenced_uids
        actual_flag = output_data["ct_is_referenced_by_rtplan"]

        assert actual_flag == expected_flag, (
            f"ct_is_referenced_by_rtplan is {actual_flag}, but CT UID '{ct_uid}' "
            f"{'is' if expected_flag else 'is not'} in RT Plan references"
        )

    def test_mr_reference_flag_correctness(self, output_data):
        """Verify mr_is_referenced_by_rtplan is correct based on RT Plan references."""
        try:
            import pydicom
        except ImportError:
            pytest.skip("pydicom not installed, skipping DICOM verification")

        # Get MR SOP Instance UID
        mr_ds = pydicom.dcmread(MR_FILE)
        mr_uid = str(mr_ds.SOPInstanceUID)

        # Get all referenced SOP Instance UIDs from RT Plan
        rtplan_ds = pydicom.dcmread(RTPLAN_FILE)
        referenced_uids = self._extract_all_referenced_sop_uids(rtplan_ds)

        expected_flag = mr_uid in referenced_uids
        actual_flag = output_data["mr_is_referenced_by_rtplan"]

        assert actual_flag == expected_flag, (
            f"mr_is_referenced_by_rtplan is {actual_flag}, but MR UID '{mr_uid}' "
            f"{'is' if expected_flag else 'is not'} in RT Plan references"
        )

    def test_total_reference_count_correctness(self, output_data):
        """Verify rtplan_total_reference_count matches actual RT Plan reference count."""
        try:
            import pydicom
        except ImportError:
            pytest.skip("pydicom not installed, skipping DICOM verification")

        rtplan_ds = pydicom.dcmread(RTPLAN_FILE)
        referenced_uids = self._extract_all_referenced_sop_uids(rtplan_ds)

        expected_count = len(referenced_uids)
        actual_count = output_data["rtplan_total_reference_count"]

        assert actual_count == expected_count, (
            f"rtplan_total_reference_count is {actual_count}, but RT Plan has "
            f"{expected_count} unique referenced SOP Instance UIDs"
        )

    def _extract_all_referenced_sop_uids(self, ds):
        """Recursively extract all Referenced SOP Instance UIDs from a DICOM dataset."""
        referenced_uids = set()

        def recurse(element):
            """Recursively search for ReferencedSOPInstanceUID in sequences."""
            if hasattr(element, "value") and isinstance(element.value, pydicom.sequence.Sequence):
                for item in element.value:
                    for sub_elem in item:
                        recurse(sub_elem)
                    # Check for ReferencedSOPInstanceUID in this sequence item
                    if hasattr(item, "ReferencedSOPInstanceUID"):
                        referenced_uids.add(str(item.ReferencedSOPInstanceUID))

        try:
            import pydicom
        except ImportError:
            return set()

        # Iterate through all elements
        for elem in ds:
            # Check if this element name contains "Referenced" and "Sequence"
            if hasattr(elem, "keyword") and "Sequence" in elem.keyword:
                recurse(elem)
            # Also check for direct ReferencedSOPInstanceUID (unlikely at top level but safe)
            if hasattr(elem, "keyword") and elem.keyword == "ReferencedSOPInstanceUID":
                referenced_uids.add(str(elem.value))

        return referenced_uids


class TestInputFilesExist:
    """Tests that verify input files exist (pre-condition checks)."""

    def test_ct_input_file_exists(self):
        """Verify CT input DICOM file exists."""
        assert os.path.exists(CT_FILE), f"Input file not found: {CT_FILE}"

    def test_mr_input_file_exists(self):
        """Verify MR input DICOM file exists."""
        assert os.path.exists(MR_FILE), f"Input file not found: {MR_FILE}"

    def test_rtplan_input_file_exists(self):
        """Verify RT Plan input DICOM file exists."""
        assert os.path.exists(RTPLAN_FILE), f"Input file not found: {RTPLAN_FILE}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
