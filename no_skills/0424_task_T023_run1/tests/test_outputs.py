import json
import os

import pytest


class TestSharedMotifOutput:
    """Tests for verifying shared_motif.json output."""

    OUTPUT_PATH = "/root/output/shared_motif.json"

    EXPECTED_RESULT = {
        "control_consensus": "CTCGCATCCCAAGCAGGATGGATCA",
        "srr_mode25": "GTCCCAGGTTTCGGATTTGTCCGCC",
        "shared_motif": "TCCCA",
        "control_start_1based": 7,
        "srr_start_1based": 2,
        "motif_length": 5,
        "srr_reads_used": 40020,
    }

    REQUIRED_FIELDS = [
        "control_consensus",
        "srr_mode25",
        "shared_motif",
        "control_start_1based",
        "srr_start_1based",
        "motif_length",
        "srr_reads_used",
    ]

    # --- Structural Tests ---

    def test_shared_motif_json_exists(self):
        """Verify shared_motif.json output file was created."""
        assert os.path.exists(self.OUTPUT_PATH), f"Output file not found: {self.OUTPUT_PATH}"

    def test_shared_motif_valid_json(self):
        """Verify output is valid JSON format."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        assert isinstance(data, dict), "Output should be a JSON object"

    # --- Content Tests (required fields and data types) ---

    def test_has_required_fields(self):
        """Verify all required fields are present."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        for field in self.REQUIRED_FIELDS:
            assert field in data, f"Missing required field: {field}"

    def test_control_consensus_is_string(self):
        """Verify control_consensus is a string."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        assert isinstance(data["control_consensus"], str), "control_consensus should be a string"

    def test_srr_mode25_is_string(self):
        """Verify srr_mode25 is a string."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        assert isinstance(data["srr_mode25"], str), "srr_mode25 should be a string"

    def test_shared_motif_is_string(self):
        """Verify shared_motif is a string."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        assert isinstance(data["shared_motif"], str), "shared_motif should be a string"

    def test_control_start_1based_is_integer(self):
        """Verify control_start_1based is an integer."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        assert isinstance(data["control_start_1based"], int), "control_start_1based should be an integer"

    def test_srr_start_1based_is_integer(self):
        """Verify srr_start_1based is an integer."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        assert isinstance(data["srr_start_1based"], int), "srr_start_1based should be an integer"

    def test_motif_length_is_integer(self):
        """Verify motif_length is an integer."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        assert isinstance(data["motif_length"], int), "motif_length should be an integer"

    def test_srr_reads_used_is_integer(self):
        """Verify srr_reads_used is an integer."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        assert isinstance(data["srr_reads_used"], int), "srr_reads_used should be an integer"

    # --- Value Tests (exact match) ---

    def test_control_consensus_value(self):
        """Verify control_consensus matches expected value."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        expected = self.EXPECTED_RESULT["control_consensus"]
        assert data["control_consensus"] == expected, (
            f"control_consensus mismatch: expected {expected}, got {data['control_consensus']}"
        )

    def test_srr_mode25_value(self):
        """Verify srr_mode25 matches expected value."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        expected = self.EXPECTED_RESULT["srr_mode25"]
        assert data["srr_mode25"] == expected, (
            f"srr_mode25 mismatch: expected {expected}, got {data['srr_mode25']}"
        )

    def test_shared_motif_value(self):
        """Verify shared_motif matches expected value."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        expected = self.EXPECTED_RESULT["shared_motif"]
        assert data["shared_motif"] == expected, (
            f"shared_motif mismatch: expected {expected}, got {data['shared_motif']}"
        )

    def test_control_start_1based_value(self):
        """Verify control_start_1based matches expected value."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        expected = self.EXPECTED_RESULT["control_start_1based"]
        assert data["control_start_1based"] == expected, (
            f"control_start_1based mismatch: expected {expected}, got {data['control_start_1based']}"
        )

    def test_srr_start_1based_value(self):
        """Verify srr_start_1based matches expected value."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        expected = self.EXPECTED_RESULT["srr_start_1based"]
        assert data["srr_start_1based"] == expected, (
            f"srr_start_1based mismatch: expected {expected}, got {data['srr_start_1based']}"
        )

    def test_motif_length_value(self):
        """Verify motif_length matches expected value."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        expected = self.EXPECTED_RESULT["motif_length"]
        assert data["motif_length"] == expected, (
            f"motif_length mismatch: expected {expected}, got {data['motif_length']}"
        )

    def test_srr_reads_used_value(self):
        """Verify srr_reads_used matches expected value."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        expected = self.EXPECTED_RESULT["srr_reads_used"]
        assert data["srr_reads_used"] == expected, (
            f"srr_reads_used mismatch: expected {expected}, got {data['srr_reads_used']}"
        )

    # --- Data Integrity Tests ---

    def test_control_consensus_length_is_25(self):
        """Verify control_consensus is exactly 25 nucleotides."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        assert len(data["control_consensus"]) == 25, (
            f"control_consensus should be 25 nt, got {len(data['control_consensus'])}"
        )

    def test_srr_mode25_length_is_25(self):
        """Verify srr_mode25 is exactly 25 nucleotides."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        assert len(data["srr_mode25"]) == 25, (
            f"srr_mode25 should be 25 nt, got {len(data['srr_mode25'])}"
        )

    def test_control_consensus_valid_bases(self):
        """Verify control_consensus contains only A/C/G/T."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        valid_bases = set("ACGT")
        actual_bases = set(data["control_consensus"])
        assert actual_bases.issubset(valid_bases), (
            f"control_consensus contains invalid bases: {actual_bases - valid_bases}"
        )

    def test_srr_mode25_valid_bases(self):
        """Verify srr_mode25 contains only A/C/G/T."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        valid_bases = set("ACGT")
        actual_bases = set(data["srr_mode25"])
        assert actual_bases.issubset(valid_bases), (
            f"srr_mode25 contains invalid bases: {actual_bases - valid_bases}"
        )

    def test_shared_motif_valid_bases(self):
        """Verify shared_motif contains only A/C/G/T."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        valid_bases = set("ACGT")
        actual_bases = set(data["shared_motif"])
        assert actual_bases.issubset(valid_bases), (
            f"shared_motif contains invalid bases: {actual_bases - valid_bases}"
        )

    def test_motif_length_matches_shared_motif(self):
        """Verify motif_length equals length of shared_motif string."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        assert data["motif_length"] == len(data["shared_motif"]), (
            f"motif_length ({data['motif_length']}) does not match "
            f"len(shared_motif) ({len(data['shared_motif'])})"
        )

    def test_shared_motif_in_control_at_correct_position(self):
        """Verify shared_motif appears in control_consensus at control_start_1based."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        start_idx = data["control_start_1based"] - 1
        end_idx = start_idx + data["motif_length"]
        extracted = data["control_consensus"][start_idx:end_idx]
        assert extracted == data["shared_motif"], (
            f"Motif at control position mismatch: expected '{data['shared_motif']}', "
            f"found '{extracted}' at position {data['control_start_1based']}"
        )

    def test_shared_motif_in_srr_at_correct_position(self):
        """Verify shared_motif appears in srr_mode25 at srr_start_1based."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        start_idx = data["srr_start_1based"] - 1
        end_idx = start_idx + data["motif_length"]
        extracted = data["srr_mode25"][start_idx:end_idx]
        assert extracted == data["shared_motif"], (
            f"Motif at SRR position mismatch: expected '{data['shared_motif']}', "
            f"found '{extracted}' at position {data['srr_start_1based']}"
        )

    def test_srr_reads_used_positive(self):
        """Verify srr_reads_used is a positive integer."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        assert data["srr_reads_used"] > 0, (
            f"srr_reads_used should be positive, got {data['srr_reads_used']}"
        )

    def test_control_start_1based_positive(self):
        """Verify control_start_1based is a positive integer (1-based index)."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        assert data["control_start_1based"] >= 1, (
            f"control_start_1based should be >= 1, got {data['control_start_1based']}"
        )

    def test_srr_start_1based_positive(self):
        """Verify srr_start_1based is a positive integer (1-based index)."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        assert data["srr_start_1based"] >= 1, (
            f"srr_start_1based should be >= 1, got {data['srr_start_1based']}"
        )

    def test_motif_length_positive(self):
        """Verify motif_length is a positive integer."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        assert data["motif_length"] > 0, (
            f"motif_length should be positive, got {data['motif_length']}"
        )
