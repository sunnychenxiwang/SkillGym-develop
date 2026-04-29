"""Auto-generated expectation tests for task verification.

These tests verify that the task execution produces correct outputs
for the sequence identity reconciliation task using k-mer distance analysis.

The task requires:
1. Parse three FASTA files (dups.fasta, ls_orchid.fasta, lupine.nu)
2. Find the duplicate 'alpha' ID in dups.fasta with identical sequences
3. Compute k-mer distances (k=2,3,4) between alpha and all targets
4. Find the best match (lowest minimum k-mer distance)
5. Output JSON with specific schema

The tests re-implement the required algorithm to verify correctness,
rather than just checking schema and ranges.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Tuple, Set

import pytest
from skbio import DNA
from skbio.sequence.distance import kmer_distance


# Constants for the expected output
OUTPUT_FILE = "/root/alpha_best_kmer_match.json"
OUTPUT_DIR = "/root/harbor_workspaces/task_T016_run2/output"
INPUT_DIR = "/root/harbor_workspaces/task_T016_run2/input"
INPUT_FILES = [
    "/root/dups.fasta",
    "/root/ls_orchid.fasta",
    "/root/lupine.nu",
]


def parse_fasta(filepath: str) -> Dict[str, List[str]]:
    """
    Parse a FASTA file and return a dict mapping ID to list of sequences.

    Multiple entries with the same ID will have multiple sequences in the list.
    """
    sequences = {}
    current_id = None
    current_seq = []

    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                # Save previous sequence
                if current_id is not None:
                    seq = ''.join(current_seq)
                    if current_id not in sequences:
                        sequences[current_id] = []
                    sequences[current_id].append(seq)
                # Start new record - extract ID (first word after '>')
                current_id = line[1:].split()[0]
                current_seq = []
            elif line:
                current_seq.append(line)

        # Save last sequence
        if current_id is not None:
            seq = ''.join(current_seq)
            if current_id not in sequences:
                sequences[current_id] = []
            sequences[current_id].append(seq)

    return sequences


def parse_fasta_single(filepath: str) -> Dict[str, str]:
    """
    Parse a FASTA file and return a dict mapping ID to sequence.

    For files without duplicates - takes first sequence for each ID.
    """
    multi = parse_fasta(filepath)
    return {k: v[0] for k, v in multi.items()}


def parse_fasta_as_list(filepath: str, source_file: str) -> List[Tuple[str, str, str]]:
    """
    Parse a FASTA file and return a list of (id, sequence, source_file) tuples.

    This preserves all records including potential duplicates for proper handling.
    """
    records = []
    current_id = None
    current_seq = []

    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                if current_id is not None:
                    seq = ''.join(current_seq)
                    records.append((current_id, seq, source_file))
                current_id = line[1:].split()[0]
                current_seq = []
            elif line:
                current_seq.append(line)

        if current_id is not None:
            seq = ''.join(current_seq)
            records.append((current_id, seq, source_file))

    return records


def compute_kmer_distance_safe(seq1: str, seq2: str, k: int) -> float:
    """
    Compute k-mer distance between two sequences using scikit-bio.

    Handles degenerate bases (N) by converting to DNA with validation disabled.
    """
    dna1 = DNA(seq1.upper(), validate=False)
    dna2 = DNA(seq2.upper(), validate=False)

    return kmer_distance(dna1, dna2, k=k)


def find_duplicates_in_fasta(filepath: str) -> Dict[str, List[str]]:
    """
    Find IDs that appear more than once in a FASTA file.

    Returns dict mapping duplicated IDs to their sequences.
    """
    sequences = parse_fasta(filepath)
    return {k: v for k, v in sequences.items() if len(v) > 1}


def compute_best_match_from_list(
    query_seq: str,
    targets: List[Tuple[str, str, str]],  # list of (id, sequence, source_file)
    k_values: List[int] = [2, 3, 4]
) -> Tuple[str, str, int, float, Dict[str, float], int]:
    """
    Compute the best k-mer match for a query sequence against all targets.

    For each target, computes k-mer distance for k=2,3,4 and takes the minimum.
    Returns the target with the globally minimum distance.
    Ties are broken lexicographically by target ID.

    Note: best_k is ANY k that achieves the minimum distance (spec doesn't
    require choosing smallest k on ties).

    Returns:
        (target_id, source_file, best_k, best_distance, all_k_distances, target_length)
    """
    best_target_id = None
    best_source_file = None
    best_k = None
    best_distance = float('inf')
    best_all_k_distances = None
    best_target_length = None

    for target_id, target_seq, source_file in targets:
        # Compute distances for all k values
        k_distances = {}
        for k in k_values:
            dist = compute_kmer_distance_safe(query_seq, target_seq, k)
            k_distances[str(k)] = dist

        # Find minimum distance for this target
        min_dist = min(k_distances.values())
        # Get any k that achieves the minimum (not necessarily smallest k)
        min_k = next(k for k in k_values if abs(k_distances[str(k)] - min_dist) < 1e-10)

        # Check if this is the best match (or tie-break lexicographically)
        is_better = False
        if min_dist < best_distance - 1e-10:
            is_better = True
        elif abs(min_dist - best_distance) < 1e-10:
            # Tie-break: choose lexicographically smaller target_id
            if best_target_id is None or target_id < best_target_id:
                is_better = True

        if is_better:
            best_target_id = target_id
            best_source_file = source_file
            best_k = min_k
            best_distance = min_dist
            best_all_k_distances = k_distances
            best_target_length = len(target_seq)

    return (
        best_target_id,
        best_source_file,
        best_k,
        best_distance,
        best_all_k_distances,
        best_target_length
    )


@pytest.fixture(scope="module")
def output_data():
    """Load and return the output JSON data."""
    with open(OUTPUT_FILE, 'r') as f:
        return json.load(f)


@pytest.fixture(scope="module")
def dups_data():
    """Parse and return the dups.fasta data."""
    return parse_fasta(os.path.join(INPUT_DIR, "dups.fasta"))


@pytest.fixture(scope="module")
def orchid_data():
    """Parse and return the ls_orchid.fasta data."""
    return parse_fasta_single(os.path.join(INPUT_DIR, "ls_orchid.fasta"))


@pytest.fixture(scope="module")
def lupine_data():
    """Parse and return the lupine.nu data."""
    return parse_fasta_single(os.path.join(INPUT_DIR, "lupine.nu"))


@pytest.fixture(scope="module")
def orchid_records():
    """Parse orchid file as list of (id, seq, source) tuples."""
    return parse_fasta_as_list(
        os.path.join(INPUT_DIR, "ls_orchid.fasta"),
        "ls_orchid.fasta"
    )


@pytest.fixture(scope="module")
def lupine_records():
    """Parse lupine file as list of (id, seq, source) tuples."""
    return parse_fasta_as_list(
        os.path.join(INPUT_DIR, "lupine.nu"),
        "lupine.nu"
    )


@pytest.fixture(scope="module")
def all_target_records(orchid_records, lupine_records):
    """
    Combine all target sequences as list of (id, seq, source) tuples.

    Using a list instead of dict to preserve all records and detect ID collisions.
    """
    return orchid_records + lupine_records


@pytest.fixture(scope="module")
def all_targets(orchid_data, lupine_data):
    """
    Combine all target sequences with their source files.

    Note: This dict-based version will overwrite on ID collision.
    Use all_target_records for collision-safe handling.
    """
    targets = {}
    for seq_id, seq in orchid_data.items():
        targets[seq_id] = (seq, "ls_orchid.fasta")
    for seq_id, seq in lupine_data.items():
        targets[seq_id] = (seq, "lupine.nu")
    return targets


@pytest.fixture(scope="module")
def expected_alpha_sequence(dups_data):
    """
    Derive the expected alpha sequence from dups.fasta.

    Verifies that alpha is duplicated and all copies are identical.
    """
    assert "alpha" in dups_data, "alpha ID not found in dups.fasta"
    alpha_seqs = dups_data["alpha"]
    assert len(alpha_seqs) >= 2, f"Expected alpha to be duplicated, found {len(alpha_seqs)} entries"

    # Check all sequences are identical with detailed error message
    unique_seqs = set(alpha_seqs)
    if len(unique_seqs) > 1:
        # Find first mismatch for diagnostic message
        first_seq = alpha_seqs[0]
        for i, seq in enumerate(alpha_seqs[1:], 1):
            if seq != first_seq:
                # Find first differing position
                diff_pos = next(
                    (j for j in range(min(len(first_seq), len(seq)))
                     if first_seq[j] != seq[j]),
                    min(len(first_seq), len(seq))
                )
                pytest.fail(
                    f"Alpha sequences are not identical. "
                    f"Entry 0 vs entry {i} differ at position {diff_pos}. "
                    f"Seq 0: '{first_seq[:50]}...', Seq {i}: '{seq[:50]}...'. "
                    f"Found {len(unique_seqs)} unique sequences among {len(alpha_seqs)} entries."
                )
    return alpha_seqs[0]


@pytest.fixture(scope="module")
def expected_best_match(expected_alpha_sequence, all_target_records):
    """Compute the expected best match using the reference algorithm."""
    return compute_best_match_from_list(expected_alpha_sequence, all_target_records)


@pytest.fixture(scope="module")
def orchid_only_best_match(expected_alpha_sequence, orchid_records):
    """Compute the best match considering only orchid targets."""
    return compute_best_match_from_list(expected_alpha_sequence, orchid_records)


@pytest.fixture(scope="module")
def lupine_only_best_match(expected_alpha_sequence, lupine_records):
    """Compute the best match considering only lupine targets."""
    return compute_best_match_from_list(expected_alpha_sequence, lupine_records)


class TestOutputFileExists:
    """Tests for verifying the output file exists and is accessible."""

    def test_output_directory_exists(self):
        """Verify output directory was created."""
        assert os.path.isdir(OUTPUT_DIR), (
            f"Output directory {OUTPUT_DIR} does not exist"
        )

    def test_output_file_exists(self):
        """Verify output file was created at the expected path."""
        assert os.path.exists(OUTPUT_FILE), (
            f"Output file not found at {OUTPUT_FILE}"
        )

    def test_output_file_is_not_empty(self):
        """Verify output file is not empty."""
        assert os.path.getsize(OUTPUT_FILE) > 0, (
            "Output file exists but is empty"
        )


class TestOutputIsValidJson:
    """Tests for verifying the output is valid JSON format."""

    def test_output_is_valid_json_dict(self):
        """Verify output file contains valid JSON that is a dictionary."""
        with open(OUTPUT_FILE, 'r') as f:
            data = json.load(f)
        assert data is not None, "JSON parsed as None"
        assert isinstance(data, dict), (
            f"Expected JSON object, got {type(data).__name__}"
        )


class TestRequiredFields:
    """Tests for verifying all required fields are present in the output."""

    def test_all_required_fields_present(self, output_data):
        """Verify all required fields are present."""
        required_fields = {
            "query_id", "query_sequence", "query_source_file",
            "target_id", "target_source_file", "target_length",
            "best_k", "best_distance", "all_k_distances"
        }
        actual_fields = set(output_data.keys())
        missing = required_fields - actual_fields
        assert not missing, f"Missing required fields: {missing}"


class TestQueryFieldValues:
    """Tests for verifying the query-related field values are correct."""

    def test_query_id_is_alpha(self, output_data):
        """Verify query_id is 'alpha' as specified in the task."""
        assert output_data["query_id"] == "alpha", (
            f"Expected query_id='alpha', got '{output_data['query_id']}'"
        )

    def test_query_sequence_matches_dups_fasta(self, output_data, expected_alpha_sequence):
        """
        Verify query_sequence matches the alpha sequence derived from dups.fasta.
        """
        actual = output_data["query_sequence"]
        expected = expected_alpha_sequence
        if actual != expected:
            # Find first difference for diagnostic
            diff_pos = next(
                (i for i in range(min(len(actual), len(expected)))
                 if actual[i] != expected[i]),
                min(len(actual), len(expected))
            )
            pytest.fail(
                f"query_sequence mismatch with dups.fasta alpha. "
                f"First difference at position {diff_pos}. "
                f"Expected length {len(expected)}, got length {len(actual)}. "
                f"Expected: '{expected[:50]}...', Got: '{actual[:50]}...'"
            )

    def test_query_source_file_is_dups_fasta(self, output_data):
        """Verify query_source_file is 'dups.fasta'."""
        assert output_data["query_source_file"] == "dups.fasta", (
            f"Expected query_source_file='dups.fasta', got '{output_data['query_source_file']}'"
        )

    def test_query_sequence_is_string(self, output_data):
        """Verify query_sequence is a string type."""
        assert isinstance(output_data["query_sequence"], str), (
            f"Expected query_sequence to be string, got {type(output_data['query_sequence']).__name__}"
        )


class TestInputFilesIntegrity:
    """Tests to verify input files exist and have expected structure."""

    def test_dups_fasta_exists(self):
        """Verify dups.fasta input file exists."""
        path = os.path.join(INPUT_DIR, "dups.fasta")
        assert os.path.exists(path), f"Input file not found: {path}"

    def test_ls_orchid_fasta_exists(self):
        """Verify ls_orchid.fasta input file exists."""
        path = os.path.join(INPUT_DIR, "ls_orchid.fasta")
        assert os.path.exists(path), f"Input file not found: {path}"

    def test_lupine_nu_exists(self):
        """Verify lupine.nu input file exists."""
        path = os.path.join(INPUT_DIR, "lupine.nu")
        assert os.path.exists(path), f"Input file not found: {path}"

    def test_lupine_nu_has_exactly_one_record(self, lupine_data):
        """
        Verify lupine.nu contains exactly one record as required by the task.

        The task specification requires lupine.nu to be a single-record FASTA file.
        """
        record_count = len(lupine_data)
        assert record_count == 1, (
            f"lupine.nu must contain exactly 1 record as per task spec, "
            f"but found {record_count} records: {list(lupine_data.keys())}"
        )

    def test_dups_fasta_has_alpha_duplicate(self, dups_data):
        """Verify dups.fasta contains duplicate alpha entries with identical sequences."""
        assert "alpha" in dups_data, "alpha ID not found in dups.fasta"
        alpha_sequences = dups_data["alpha"]

        assert len(alpha_sequences) >= 2, (
            f"Expected at least 2 alpha entries, found {len(alpha_sequences)}"
        )

        unique_seqs = set(alpha_sequences)
        assert len(unique_seqs) == 1, (
            f"All alpha sequences should be identical, but found {len(unique_seqs)} "
            f"unique sequences among {len(alpha_sequences)} entries. "
            f"Unique sequence lengths: {[len(s) for s in unique_seqs]}"
        )

    def test_dups_fasta_alpha_is_only_duplicate(self, dups_data):
        """
        Verify that alpha is the only duplicated ID in dups.fasta.
        """
        duplicated_ids = {k for k, v in dups_data.items() if len(v) > 1}

        assert duplicated_ids == {"alpha"}, (
            f"Expected only 'alpha' to be duplicated, but found: {duplicated_ids}"
        )


class TestCrossFileIdCollisions:
    """Tests to detect and handle ID collisions across input files."""

    def test_no_id_collision_between_orchid_and_lupine(self, orchid_data, lupine_data):
        """
        Detect if any IDs appear in both orchid and lupine files.

        ID collisions could cause silent overwrites in dict-based merging.
        This test ensures we're aware of any collisions in the test data.
        """
        orchid_ids = set(orchid_data.keys())
        lupine_ids = set(lupine_data.keys())
        colliding_ids = orchid_ids & lupine_ids

        if colliding_ids:
            # If there are collisions, document them clearly
            collision_details = []
            for cid in colliding_ids:
                orchid_len = len(orchid_data[cid])
                lupine_len = len(lupine_data[cid])
                collision_details.append(
                    f"ID '{cid}': orchid seq len={orchid_len}, lupine seq len={lupine_len}"
                )
            pytest.fail(
                f"Found {len(colliding_ids)} ID collision(s) between orchid and lupine files. "
                f"This could cause silent overwrites in implementations using dicts. "
                f"Collisions: {'; '.join(collision_details)}"
            )

    def test_all_target_records_preserves_all_entries(
        self, all_target_records, orchid_records, lupine_records
    ):
        """Verify the combined target list has all records from both files."""
        expected_count = len(orchid_records) + len(lupine_records)
        actual_count = len(all_target_records)
        assert actual_count == expected_count, (
            f"Expected {expected_count} total target records "
            f"(orchid: {len(orchid_records)} + lupine: {len(lupine_records)}), "
            f"but got {actual_count}"
        )


class TestTargetFieldValues:
    """Tests for verifying the target-related field values are valid."""

    def test_target_id_is_string(self, output_data):
        """Verify target_id is a non-empty string."""
        assert isinstance(output_data["target_id"], str), (
            f"Expected target_id to be string, got {type(output_data['target_id']).__name__}"
        )
        assert len(output_data["target_id"]) > 0, "target_id is empty string"

    def test_target_source_file_is_valid(self, output_data):
        """Verify target_source_file is either ls_orchid.fasta or lupine.nu."""
        valid_sources = {"ls_orchid.fasta", "lupine.nu"}
        assert output_data["target_source_file"] in valid_sources, (
            f"Expected target_source_file in {valid_sources}, "
            f"got '{output_data['target_source_file']}'"
        )

    def test_target_length_is_positive_integer(self, output_data):
        """Verify target_length is a positive integer."""
        target_length = output_data["target_length"]
        assert isinstance(target_length, int), (
            f"Expected target_length to be int, got {type(target_length).__name__}"
        )
        assert target_length > 0, f"target_length must be positive, got {target_length}"

    def test_target_id_exists_in_source_file(self, output_data, all_target_records):
        """Verify the target_id exists in the corresponding source file."""
        target_id = output_data["target_id"]
        source_file = output_data["target_source_file"]

        # Find all records matching target_id
        matching_records = [
            (tid, seq, src) for tid, seq, src in all_target_records
            if tid == target_id
        ]

        assert len(matching_records) > 0, (
            f"target_id '{target_id}' not found in any target file"
        )

        # Check that at least one matching record is from the claimed source
        sources_for_id = {src for _, _, src in matching_records}
        assert source_file in sources_for_id, (
            f"target_id '{target_id}' found in {sources_for_id}, "
            f"but output claims {source_file}"
        )

    def test_target_length_matches_actual_sequence(self, output_data, all_target_records):
        """Verify target_length matches the actual sequence length in source file."""
        target_id = output_data["target_id"]
        source_file = output_data["target_source_file"]
        expected_length = output_data["target_length"]

        # Find the specific record
        matching = [
            (tid, seq, src) for tid, seq, src in all_target_records
            if tid == target_id and src == source_file
        ]

        assert len(matching) > 0, (
            f"target_id '{target_id}' from '{source_file}' not found"
        )

        actual_length = len(matching[0][1])
        assert actual_length == expected_length, (
            f"target_length ({expected_length}) doesn't match actual "
            f"sequence length ({actual_length}) for target '{target_id}'"
        )


class TestDistanceFieldValues:
    """Tests for verifying the distance-related field values are valid."""

    def test_best_k_is_valid_value(self, output_data):
        """Verify best_k is 2, 3, or 4 as specified in the task."""
        valid_k_values = {2, 3, 4}
        assert output_data["best_k"] in valid_k_values, (
            f"Expected best_k in {valid_k_values}, got {output_data['best_k']}"
        )

    def test_best_k_is_integer(self, output_data):
        """Verify best_k is an integer."""
        assert isinstance(output_data["best_k"], int), (
            f"Expected best_k to be int, got {type(output_data['best_k']).__name__}"
        )

    def test_best_distance_is_numeric(self, output_data):
        """Verify best_distance is a numeric type."""
        best_distance = output_data["best_distance"]
        assert isinstance(best_distance, (int, float)), (
            f"Expected best_distance to be numeric, got {type(best_distance).__name__}"
        )

    def test_best_distance_is_non_negative(self, output_data):
        """Verify best_distance is non-negative (distance cannot be negative)."""
        assert output_data["best_distance"] >= 0, (
            f"Distance cannot be negative, got {output_data['best_distance']}"
        )

    def test_best_distance_is_bounded(self, output_data):
        """Verify best_distance is bounded by 1 (k-mer distance range is [0, 1])."""
        assert output_data["best_distance"] <= 1, (
            f"K-mer distance should be <= 1, got {output_data['best_distance']}"
        )


class TestAllKDistances:
    """Tests for verifying the all_k_distances field structure and values."""

    def test_all_k_distances_is_dict(self, output_data):
        """Verify all_k_distances is a dictionary."""
        assert isinstance(output_data["all_k_distances"], dict), (
            f"Expected all_k_distances to be dict, "
            f"got {type(output_data['all_k_distances']).__name__}"
        )

    def test_all_k_distances_has_required_keys(self, output_data):
        """Verify all_k_distances has keys for k=2, 3, 4."""
        all_k_distances = output_data["all_k_distances"]
        required_keys = {"2", "3", "4"}
        actual_keys = set(all_k_distances.keys())
        assert required_keys == actual_keys, (
            f"Expected keys {required_keys}, got {actual_keys}"
        )

    def test_all_k_distances_values_are_valid(self, output_data):
        """Verify all distance values are numeric, non-negative, and bounded by 1."""
        for k, distance in output_data["all_k_distances"].items():
            assert isinstance(distance, (int, float)), (
                f"Expected distance for k={k} to be numeric, got {type(distance).__name__}"
            )
            assert 0 <= distance <= 1, (
                f"Distance for k={k} ({distance}) is out of valid range [0, 1]"
            )

    def test_best_distance_matches_minimum(self, output_data):
        """Verify best_distance equals the minimum of all_k_distances."""
        all_distances = output_data["all_k_distances"]
        min_distance = min(all_distances.values())
        assert abs(output_data["best_distance"] - min_distance) < 1e-10, (
            f"best_distance ({output_data['best_distance']}) should equal "
            f"min of all_k_distances ({min_distance}). "
            f"All distances: {all_distances}"
        )

    def test_best_k_corresponds_to_minimum_distance(self, output_data):
        """
        Verify best_k corresponds to a k value that achieves the minimum distance.

        Note: The spec does not require choosing the smallest k when multiple ks tie.
        Any k that achieves the minimum distance is valid.
        """
        all_distances = output_data["all_k_distances"]
        min_distance = min(all_distances.values())

        # Find which k value(s) have the minimum distance
        k_values_with_min = [
            int(k) for k, d in all_distances.items()
            if abs(d - min_distance) < 1e-10
        ]

        assert output_data["best_k"] in k_values_with_min, (
            f"best_k ({output_data['best_k']}) should be one of the k values "
            f"with minimum distance: {k_values_with_min}. "
            f"All distances: {all_distances}"
        )


class TestSchemaCompliance:
    """Tests to verify the output matches the exact required schema."""

    def test_no_extra_fields(self, output_data):
        """Verify no unexpected extra fields are present."""
        expected_fields = {
            "query_id", "query_sequence", "query_source_file",
            "target_id", "target_source_file", "target_length",
            "best_k", "best_distance", "all_k_distances"
        }
        actual_fields = set(output_data.keys())
        extra_fields = actual_fields - expected_fields
        assert not extra_fields, f"Unexpected extra fields: {extra_fields}"

    def test_exact_field_count(self, output_data):
        """Verify the output has exactly 9 fields."""
        assert len(output_data) == 9, (
            f"Expected exactly 9 fields, got {len(output_data)}: {list(output_data.keys())}"
        )

    def test_all_k_distances_has_exactly_three_keys(self, output_data):
        """Verify all_k_distances has exactly 3 keys (2, 3, 4)."""
        all_k = output_data["all_k_distances"]
        assert len(all_k) == 3, (
            f"Expected exactly 3 keys in all_k_distances, got {len(all_k)}: {list(all_k.keys())}"
        )


class TestGlobalBestMatchCorrectness:
    """
    Tests verifying the solution considered ALL input files and found the global best.

    These tests ensure the implementation actually parsed both orchid and lupine files,
    not just one of them.
    """

    def test_target_is_global_best_across_both_files(
        self, output_data, expected_alpha_sequence, all_target_records,
        orchid_only_best_match, lupine_only_best_match
    ):
        """
        Verify the selected target is the global best across BOTH orchid and lupine.

        This test computes the best match for each file separately and then
        verifies the output matches the true global best.
        """
        # Global best from combined targets
        global_best = compute_best_match_from_list(
            expected_alpha_sequence, all_target_records
        )
        global_best_id = global_best[0]
        global_best_distance = global_best[3]

        # Best from each file separately
        orchid_best_id = orchid_only_best_match[0]
        orchid_best_distance = orchid_only_best_match[3]
        lupine_best_id = lupine_only_best_match[0]
        lupine_best_distance = lupine_only_best_match[3]

        # Determine which file the global best comes from
        if orchid_best_distance < lupine_best_distance - 1e-10:
            expected_source = "ls_orchid.fasta"
            expected_id = orchid_best_id
        elif lupine_best_distance < orchid_best_distance - 1e-10:
            expected_source = "lupine.nu"
            expected_id = lupine_best_id
        else:
            # Tie - use lexicographic tie-break
            if orchid_best_id <= lupine_best_id:
                expected_source = "ls_orchid.fasta"
                expected_id = orchid_best_id
            else:
                expected_source = "lupine.nu"
                expected_id = lupine_best_id

        assert output_data["target_id"] == global_best_id, (
            f"Expected target_id='{global_best_id}' (global best), "
            f"got '{output_data['target_id']}'. "
            f"Orchid best: '{orchid_best_id}' (dist={orchid_best_distance:.6f}), "
            f"Lupine best: '{lupine_best_id}' (dist={lupine_best_distance:.6f})"
        )

    def test_target_source_correctly_identifies_origin(
        self, output_data, orchid_only_best_match, lupine_only_best_match
    ):
        """
        Verify target_source_file correctly indicates which file the target came from.

        If global best comes from lupine, target_source_file must be 'lupine.nu'.
        If global best comes from orchid, target_source_file must be 'ls_orchid.fasta'.
        """
        orchid_best_distance = orchid_only_best_match[3]
        lupine_best_distance = lupine_only_best_match[3]

        # Determine expected source based on which file has the better match
        if lupine_best_distance < orchid_best_distance - 1e-10:
            expected_source = "lupine.nu"
        elif orchid_best_distance < lupine_best_distance - 1e-10:
            expected_source = "ls_orchid.fasta"
        else:
            # Tie - either source is valid if IDs also match
            orchid_best_id = orchid_only_best_match[0]
            lupine_best_id = lupine_only_best_match[0]
            if orchid_best_id <= lupine_best_id:
                expected_source = "ls_orchid.fasta"
            else:
                expected_source = "lupine.nu"

        assert output_data["target_source_file"] == expected_source, (
            f"Expected target_source_file='{expected_source}', "
            f"got '{output_data['target_source_file']}'. "
            f"Orchid best distance: {orchid_best_distance:.6f}, "
            f"Lupine best distance: {lupine_best_distance:.6f}"
        )


class TestKmerDistanceCorrectness:
    """
    Tests for verifying the k-mer distance computation is correct.

    These tests re-implement the required algorithm using scikit-bio
    and verify that the output matches the expected values.
    """

    def test_target_is_global_best_match(
        self, output_data, expected_alpha_sequence, all_target_records
    ):
        """
        Verify the selected target is the global best match.
        """
        expected = compute_best_match_from_list(
            expected_alpha_sequence, all_target_records
        )
        expected_target_id = expected[0]

        assert output_data["target_id"] == expected_target_id, (
            f"Expected target_id='{expected_target_id}' (computed global best match), "
            f"got '{output_data['target_id']}'"
        )

    def test_target_source_file_matches_computed(
        self, output_data, expected_best_match
    ):
        """Verify target_source_file matches the computed best match."""
        expected_source = expected_best_match[1]

        assert output_data["target_source_file"] == expected_source, (
            f"Expected target_source_file='{expected_source}', "
            f"got '{output_data['target_source_file']}'"
        )

    def test_best_k_is_valid_for_minimum_distance(
        self, output_data, expected_best_match
    ):
        """
        Verify best_k corresponds to the minimum distance for the chosen target.

        Note: The spec does not require choosing the smallest k on ties.
        We only verify that best_k achieves the minimum distance.
        """
        expected_all_k = expected_best_match[4]
        expected_min_distance = min(expected_all_k.values())

        # Get which k values achieve the minimum
        valid_k_values = [
            int(k) for k, d in expected_all_k.items()
            if abs(d - expected_min_distance) < 1e-10
        ]

        assert output_data["best_k"] in valid_k_values, (
            f"best_k ({output_data['best_k']}) should be one of {valid_k_values} "
            f"(k values that achieve minimum distance {expected_min_distance:.6f}). "
            f"All distances: {expected_all_k}"
        )

    def test_best_distance_matches_computed(self, output_data, expected_best_match):
        """
        Verify best_distance matches the computed best match.
        """
        expected_distance = expected_best_match[3]
        actual_distance = output_data["best_distance"]

        assert abs(actual_distance - expected_distance) < 1e-9, (
            f"Expected best_distance={expected_distance:.9f} (computed via scikit-bio), "
            f"got {actual_distance:.9f}, diff={abs(actual_distance - expected_distance):.2e}"
        )

    def test_all_k_distances_match_computed(self, output_data, expected_best_match):
        """
        Verify all_k_distances match the computed values for the chosen target.
        """
        expected_distances = expected_best_match[4]
        actual_distances = output_data["all_k_distances"]

        errors = []
        for k in ["2", "3", "4"]:
            expected = expected_distances[k]
            actual = actual_distances[k]
            if abs(actual - expected) >= 1e-9:
                errors.append(
                    f"k={k}: expected {expected:.9f}, got {actual:.9f}, "
                    f"diff={abs(actual - expected):.2e}"
                )

        assert not errors, (
            f"Distance mismatches for all_k_distances:\n" +
            "\n".join(f"  - {e}" for e in errors)
        )

    def test_target_length_matches_computed(self, output_data, expected_best_match):
        """Verify target_length matches the computed best match."""
        expected_length = expected_best_match[5]

        assert output_data["target_length"] == expected_length, (
            f"Expected target_length={expected_length}, "
            f"got {output_data['target_length']}"
        )

    def test_best_distance_is_global_minimum(
        self, output_data, expected_alpha_sequence, all_target_records
    ):
        """
        Verify best_distance is truly the global minimum across all targets.
        """
        reported_best_distance = output_data["best_distance"]

        for target_id, target_seq, source_file in all_target_records:
            for k in [2, 3, 4]:
                dist = compute_kmer_distance_safe(
                    expected_alpha_sequence, target_seq, k
                )
                if dist < reported_best_distance - 1e-9:
                    pytest.fail(
                        f"Found target '{target_id}' from '{source_file}' "
                        f"with distance {dist:.9f} (k={k}) "
                        f"which is lower than reported best_distance {reported_best_distance:.9f}"
                    )


class TestTieBreaking:
    """
    Tests for verifying tie-breaking behavior.

    When multiple targets have the same minimum distance, the implementation
    should use lexicographic ordering on target IDs for deterministic selection.
    """

    def test_deterministic_selection_on_ties(
        self, output_data, expected_alpha_sequence, all_target_records
    ):
        """
        Verify tie-breaking is deterministic using lexicographic order.
        """
        reported_best_distance = output_data["best_distance"]
        reported_target_id = output_data["target_id"]

        # Find all targets with the same minimum distance
        tied_targets = []
        for target_id, target_seq, source_file in all_target_records:
            min_dist = float('inf')
            for k in [2, 3, 4]:
                dist = compute_kmer_distance_safe(
                    expected_alpha_sequence, target_seq, k
                )
                min_dist = min(min_dist, dist)

            if abs(min_dist - reported_best_distance) < 1e-9:
                tied_targets.append(target_id)

        if len(tied_targets) > 1:
            # There are ties - verify lexicographic selection
            expected_winner = min(tied_targets)
            assert reported_target_id == expected_winner, (
                f"Tie-break should select lexicographically smallest ID. "
                f"Tied targets: {sorted(tied_targets)}, "
                f"expected '{expected_winner}', got '{reported_target_id}'"
            )
        else:
            # No ties - just verify the single best was selected
            assert len(tied_targets) == 1, "Should have at least one best target"
            assert reported_target_id == tied_targets[0], (
                f"Expected target '{tied_targets[0]}', got '{reported_target_id}'"
            )


class TestKmerDistanceInternalConsistency:
    """Tests for k-mer distance computation logic validation."""

    def test_best_distance_is_consistent_with_all_k_distances(self, output_data):
        """Verify best_distance value is actually found in all_k_distances."""
        best_dist = output_data["best_distance"]
        all_distances = list(output_data["all_k_distances"].values())

        matches = [d for d in all_distances if abs(d - best_dist) < 1e-10]
        assert len(matches) >= 1, (
            f"best_distance ({best_dist:.9f}) not found in all_k_distances values: "
            f"{[f'{d:.9f}' for d in all_distances]}"
        )

    def test_best_k_corresponds_to_best_distance(self, output_data):
        """Verify best_k's distance in all_k_distances equals best_distance."""
        best_k = output_data["best_k"]
        best_dist = output_data["best_distance"]
        k_str = str(best_k)

        actual_dist = output_data["all_k_distances"].get(k_str)
        assert actual_dist is not None, (
            f"best_k ({best_k}) not found as key in all_k_distances"
        )
        assert abs(actual_dist - best_dist) < 1e-10, (
            f"Distance for best_k={best_k} ({actual_dist:.9f}) doesn't match "
            f"best_distance ({best_dist:.9f})"
        )


class TestReproducibility:
    """Tests to verify the results are reproducible."""

    def test_recompute_matches_output(
        self, output_data, expected_alpha_sequence, all_target_records
    ):
        """
        Fully re-compute the expected output and verify all fields match.
        """
        # Re-compute the best match
        (
            expected_target_id,
            expected_source,
            expected_k,
            expected_distance,
            expected_all_k,
            expected_length
        ) = compute_best_match_from_list(expected_alpha_sequence, all_target_records)

        # Collect all errors
        errors = []

        if output_data["query_id"] != "alpha":
            errors.append(f"query_id: expected 'alpha', got '{output_data['query_id']}'")

        if output_data["query_sequence"] != expected_alpha_sequence:
            errors.append(
                f"query_sequence: length mismatch (expected {len(expected_alpha_sequence)}, "
                f"got {len(output_data['query_sequence'])})"
            )

        if output_data["query_source_file"] != "dups.fasta":
            errors.append(
                f"query_source_file: expected 'dups.fasta', "
                f"got '{output_data['query_source_file']}'"
            )

        if output_data["target_id"] != expected_target_id:
            errors.append(
                f"target_id: expected '{expected_target_id}', "
                f"got '{output_data['target_id']}'"
            )

        if output_data["target_source_file"] != expected_source:
            errors.append(
                f"target_source_file: expected '{expected_source}', "
                f"got '{output_data['target_source_file']}'"
            )

        if output_data["target_length"] != expected_length:
            errors.append(
                f"target_length: expected {expected_length}, "
                f"got {output_data['target_length']}"
            )

        # For best_k, only require it achieves minimum distance (spec allows any k on tie)
        actual_best_k_distance = output_data["all_k_distances"].get(str(output_data["best_k"]))
        if actual_best_k_distance is None:
            errors.append(f"best_k ({output_data['best_k']}) not found in all_k_distances")
        elif abs(actual_best_k_distance - expected_distance) >= 1e-9:
            errors.append(
                f"best_k ({output_data['best_k']}) does not achieve minimum distance: "
                f"distance for this k is {actual_best_k_distance:.9f}, "
                f"but minimum is {expected_distance:.9f}"
            )

        if abs(output_data["best_distance"] - expected_distance) >= 1e-9:
            errors.append(
                f"best_distance: expected {expected_distance:.9f}, "
                f"got {output_data['best_distance']:.9f}"
            )

        for k in ["2", "3", "4"]:
            if abs(output_data["all_k_distances"][k] - expected_all_k[k]) >= 1e-9:
                errors.append(
                    f"all_k_distances[{k}]: expected {expected_all_k[k]:.9f}, "
                    f"got {output_data['all_k_distances'][k]:.9f}"
                )

        assert not errors, (
            "Output does not match re-computed expected values:\n" +
            "\n".join(f"  - {e}" for e in errors)
        )
