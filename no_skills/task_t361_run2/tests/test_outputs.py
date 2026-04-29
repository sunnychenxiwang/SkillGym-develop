"""Auto-generated expectation tests for DICOM plan match verification.

These tests verify that the task execution produces correct outputs
based on cross-referencing patient/study identifiers across CT, MR,
and RT plan DICOM files.
"""

import json
import os
from pathlib import Path

import pytest

# Expected output file path
OUTPUT_FILE = "/root/dicom_plan_match.json"

# Expected field values from DICOM files
EXPECTED_PLAN_PATIENT_ID = "id00001"
EXPECTED_PLAN_PATIENT_NAME = "Last^First^mid^pre"
EXPECTED_CT_PATIENT_ID = "1CT1"
EXPECTED_CT_PATIENT_NAME = "CompressedSamples^CT1"
EXPECTED_MR_PATIENT_ID = "4MR1"
EXPECTED_MR_PATIENT_NAME = "CompressedSamples^MR1"

# Expected scores based on matching rules:
# CT vs Plan: PatientSex matches ('O' == 'O') = +1, nothing else matches = 1
# MR vs Plan: Nothing matches = 0
EXPECTED_SCORE_CT_VS_PLAN = 1
EXPECTED_SCORE_MR_VS_PLAN = 0
EXPECTED_BEST_MATCH_MODALITY = "CT"  # CT score > MR score

# Required JSON schema keys
REQUIRED_KEYS = [
    "plan_patient_id",
    "plan_patient_name",
    "ct_patient_id",
    "ct_patient_name",
    "mr_patient_id",
    "mr_patient_name",
    "score_ct_vs_plan",
    "score_mr_vs_plan",
    "best_match_modality",
]


class TestOutputFileExists:
    """Tests for output file existence and basic validity."""

    def test_output_file_exists(self):
        """Verify output JSON file was created at the specified path."""
        assert os.path.exists(OUTPUT_FILE), (
            f"Output file not found at {OUTPUT_FILE}"
        )

    def test_output_file_not_empty(self):
        """Verify output file is not empty."""
        assert os.path.exists(OUTPUT_FILE), f"Output file not found at {OUTPUT_FILE}"
        file_size = os.path.getsize(OUTPUT_FILE)
        assert file_size > 0, "Output file is empty"


class TestOutputFormat:
    """Tests for valid JSON format and schema compliance."""

    def test_output_is_valid_json(self):
        """Verify output is valid JSON format."""
        assert os.path.exists(OUTPUT_FILE), f"Output file not found at {OUTPUT_FILE}"
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        assert data is not None, "JSON data is None"
        assert isinstance(data, dict), "JSON root should be an object/dict"

    def test_json_has_all_required_keys(self):
        """Verify all required keys are present in the JSON output."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)

        missing_keys = [key for key in REQUIRED_KEYS if key not in data]
        assert not missing_keys, (
            f"Missing required keys: {missing_keys}"
        )

    def test_json_has_no_extra_keys(self):
        """Verify JSON contains exactly the required keys, no extras."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)

        extra_keys = [key for key in data.keys() if key not in REQUIRED_KEYS]
        assert not extra_keys, (
            f"Extra keys found that should not be present: {extra_keys}"
        )

    def test_json_key_count_matches_schema(self):
        """Verify JSON has exactly 9 keys as specified in schema."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)

        assert len(data) == 9, (
            f"Expected exactly 9 keys, found {len(data)}"
        )


class TestFieldTypes:
    """Tests for correct data types of JSON fields."""

    def test_plan_patient_id_is_string(self):
        """Verify plan_patient_id is a string."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        assert isinstance(data["plan_patient_id"], str), (
            f"plan_patient_id should be string, got {type(data['plan_patient_id'])}"
        )

    def test_plan_patient_name_is_string(self):
        """Verify plan_patient_name is a string."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        assert isinstance(data["plan_patient_name"], str), (
            f"plan_patient_name should be string, got {type(data['plan_patient_name'])}"
        )

    def test_ct_patient_id_is_string(self):
        """Verify ct_patient_id is a string."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        assert isinstance(data["ct_patient_id"], str), (
            f"ct_patient_id should be string, got {type(data['ct_patient_id'])}"
        )

    def test_ct_patient_name_is_string(self):
        """Verify ct_patient_name is a string."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        assert isinstance(data["ct_patient_name"], str), (
            f"ct_patient_name should be string, got {type(data['ct_patient_name'])}"
        )

    def test_mr_patient_id_is_string(self):
        """Verify mr_patient_id is a string."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        assert isinstance(data["mr_patient_id"], str), (
            f"mr_patient_id should be string, got {type(data['mr_patient_id'])}"
        )

    def test_mr_patient_name_is_string(self):
        """Verify mr_patient_name is a string."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        assert isinstance(data["mr_patient_name"], str), (
            f"mr_patient_name should be string, got {type(data['mr_patient_name'])}"
        )

    def test_score_ct_vs_plan_is_integer(self):
        """Verify score_ct_vs_plan is an integer."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        assert isinstance(data["score_ct_vs_plan"], int), (
            f"score_ct_vs_plan should be int, got {type(data['score_ct_vs_plan'])}"
        )

    def test_score_mr_vs_plan_is_integer(self):
        """Verify score_mr_vs_plan is an integer."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        assert isinstance(data["score_mr_vs_plan"], int), (
            f"score_mr_vs_plan should be int, got {type(data['score_mr_vs_plan'])}"
        )

    def test_best_match_modality_is_string(self):
        """Verify best_match_modality is a string."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        assert isinstance(data["best_match_modality"], str), (
            f"best_match_modality should be string, got {type(data['best_match_modality'])}"
        )


class TestFieldValues:
    """Tests for correct values extracted from DICOM files."""

    def test_plan_patient_id_value(self):
        """Verify plan_patient_id matches RT plan DICOM PatientID."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        assert data["plan_patient_id"] == EXPECTED_PLAN_PATIENT_ID, (
            f"Expected plan_patient_id '{EXPECTED_PLAN_PATIENT_ID}', "
            f"got '{data['plan_patient_id']}'"
        )

    def test_plan_patient_name_value(self):
        """Verify plan_patient_name matches RT plan DICOM PatientName."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        assert data["plan_patient_name"] == EXPECTED_PLAN_PATIENT_NAME, (
            f"Expected plan_patient_name '{EXPECTED_PLAN_PATIENT_NAME}', "
            f"got '{data['plan_patient_name']}'"
        )

    def test_ct_patient_id_value(self):
        """Verify ct_patient_id matches CT DICOM PatientID."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        assert data["ct_patient_id"] == EXPECTED_CT_PATIENT_ID, (
            f"Expected ct_patient_id '{EXPECTED_CT_PATIENT_ID}', "
            f"got '{data['ct_patient_id']}'"
        )

    def test_ct_patient_name_value(self):
        """Verify ct_patient_name matches CT DICOM PatientName."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        assert data["ct_patient_name"] == EXPECTED_CT_PATIENT_NAME, (
            f"Expected ct_patient_name '{EXPECTED_CT_PATIENT_NAME}', "
            f"got '{data['ct_patient_name']}'"
        )

    def test_mr_patient_id_value(self):
        """Verify mr_patient_id matches MR DICOM PatientID."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        assert data["mr_patient_id"] == EXPECTED_MR_PATIENT_ID, (
            f"Expected mr_patient_id '{EXPECTED_MR_PATIENT_ID}', "
            f"got '{data['mr_patient_id']}'"
        )

    def test_mr_patient_name_value(self):
        """Verify mr_patient_name matches MR DICOM PatientName."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        assert data["mr_patient_name"] == EXPECTED_MR_PATIENT_NAME, (
            f"Expected mr_patient_name '{EXPECTED_MR_PATIENT_NAME}', "
            f"got '{data['mr_patient_name']}'"
        )


class TestScoringLogic:
    """Tests for correct scoring calculation based on matching rules."""

    def test_score_ct_vs_plan_value(self):
        """Verify score_ct_vs_plan is correctly calculated.

        CT vs Plan matching:
        - PatientID: '1CT1' vs 'id00001' = NO match
        - PatientName: 'CompressedSamples^CT1' vs 'Last^First^mid^pre' = NO match
        - PatientSex: 'O' vs 'O' = MATCH (+1)
        - StudyID: '1CT1' vs 'study1' = NO match
        - StudyInstanceUID: different = NO match
        Total = 1
        """
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        assert data["score_ct_vs_plan"] == EXPECTED_SCORE_CT_VS_PLAN, (
            f"Expected score_ct_vs_plan {EXPECTED_SCORE_CT_VS_PLAN}, "
            f"got {data['score_ct_vs_plan']}"
        )

    def test_score_mr_vs_plan_value(self):
        """Verify score_mr_vs_plan is correctly calculated.

        MR vs Plan matching:
        - PatientID: '4MR1' vs 'id00001' = NO match
        - PatientName: 'CompressedSamples^MR1' vs 'Last^First^mid^pre' = NO match
        - PatientSex: 'F' vs 'O' = NO match
        - StudyID: '4MR1' vs 'study1' = NO match
        - StudyInstanceUID: different = NO match
        Total = 0
        """
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        assert data["score_mr_vs_plan"] == EXPECTED_SCORE_MR_VS_PLAN, (
            f"Expected score_mr_vs_plan {EXPECTED_SCORE_MR_VS_PLAN}, "
            f"got {data['score_mr_vs_plan']}"
        )

    def test_scores_are_non_negative(self):
        """Verify both scores are non-negative integers."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        assert data["score_ct_vs_plan"] >= 0, (
            f"score_ct_vs_plan should be non-negative, got {data['score_ct_vs_plan']}"
        )
        assert data["score_mr_vs_plan"] >= 0, (
            f"score_mr_vs_plan should be non-negative, got {data['score_mr_vs_plan']}"
        )

    def test_scores_within_valid_range(self):
        """Verify scores are within valid range (0-8 max based on scoring rules)."""
        # Max possible score: 3 (PatientID) + 2 (PatientName) + 1 (PatientSex) +
        #                     1 (StudyID) + 1 (StudyInstanceUID) = 8
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        assert 0 <= data["score_ct_vs_plan"] <= 8, (
            f"score_ct_vs_plan {data['score_ct_vs_plan']} out of valid range [0, 8]"
        )
        assert 0 <= data["score_mr_vs_plan"] <= 8, (
            f"score_mr_vs_plan {data['score_mr_vs_plan']} out of valid range [0, 8]"
        )


class TestBestMatchModality:
    """Tests for correct best_match_modality determination."""

    def test_best_match_modality_value(self):
        """Verify best_match_modality is correctly determined.

        Since score_ct_vs_plan (1) > score_mr_vs_plan (0),
        best_match_modality should be 'CT'.
        """
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        assert data["best_match_modality"] == EXPECTED_BEST_MATCH_MODALITY, (
            f"Expected best_match_modality '{EXPECTED_BEST_MATCH_MODALITY}', "
            f"got '{data['best_match_modality']}'"
        )

    def test_best_match_modality_valid_enum(self):
        """Verify best_match_modality is one of the valid values."""
        valid_values = ["CT", "MR", "TIE"]
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
        assert data["best_match_modality"] in valid_values, (
            f"best_match_modality '{data['best_match_modality']}' not in valid values {valid_values}"
        )

    def test_best_match_modality_consistent_with_scores(self):
        """Verify best_match_modality is consistent with the scores."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)

        ct_score = data["score_ct_vs_plan"]
        mr_score = data["score_mr_vs_plan"]
        modality = data["best_match_modality"]

        if ct_score > mr_score:
            expected = "CT"
        elif mr_score > ct_score:
            expected = "MR"
        else:
            expected = "TIE"

        assert modality == expected, (
            f"best_match_modality '{modality}' inconsistent with scores "
            f"(CT={ct_score}, MR={mr_score}). Expected '{expected}'"
        )


class TestDataIntegrity:
    """Tests for overall data integrity and consistency."""

    def test_all_patient_ids_are_nonempty(self):
        """Verify all patient ID fields contain values."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)

        # Based on actual DICOM data, all should have patient IDs
        assert data["plan_patient_id"], "plan_patient_id should not be empty"
        assert data["ct_patient_id"], "ct_patient_id should not be empty"
        assert data["mr_patient_id"], "mr_patient_id should not be empty"

    def test_all_patient_names_are_nonempty(self):
        """Verify all patient name fields contain values."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)

        # Based on actual DICOM data, all should have patient names
        assert data["plan_patient_name"], "plan_patient_name should not be empty"
        assert data["ct_patient_name"], "ct_patient_name should not be empty"
        assert data["mr_patient_name"], "mr_patient_name should not be empty"

    def test_ct_and_mr_have_different_patient_ids(self):
        """Verify CT and MR files have different patient IDs (as per test data)."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)

        assert data["ct_patient_id"] != data["mr_patient_id"], (
            "CT and MR should have different patient IDs based on test DICOM data"
        )

    def test_json_is_well_formed(self):
        """Verify JSON can be loaded and serialized without issues."""
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)

        # Verify round-trip serialization works
        serialized = json.dumps(data)
        reloaded = json.loads(serialized)
        assert data == reloaded, "JSON round-trip serialization failed"
