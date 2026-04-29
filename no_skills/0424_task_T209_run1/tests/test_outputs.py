import json
import math
import os

import pytest


class TestIdentityMap:
    """Tests for verifying identity_map.json output."""

    OUTPUT_PATH = "/root/output/identity_map.json"
    TOLERANCE = 0.001

    EXPECTED_RESULT = {
        "queries": [
            {
                "query_sequence": "ACGTA",
                "source_headers": ["alpha", "alpha"],
                "best_hit": {
                    "reference_id": "gi|2765599|emb|Z78474.1|PKZ78474",
                    "reference_source_file": "ls_orchid.fasta",
                    "alignment_score": 10.0,
                    "aligned_query_span": [0, 5],
                    "aligned_reference_span": [50, 55]
                },
                "read_evidence": {
                    "example.fastq": 0,
                    "SRR020192.fastq.gz": 48
                }
            },
            {
                "query_sequence": "CCGCC",
                "source_headers": ["gamma"],
                "best_hit": {
                    "reference_id": "gi|2765627|emb|Z78502.1|PBZ78502",
                    "reference_source_file": "ls_orchid.fasta",
                    "alignment_score": 10.0,
                    "aligned_query_span": [0, 5],
                    "aligned_reference_span": [48, 53]
                },
                "read_evidence": {
                    "example.fastq": 0,
                    "SRR020192.fastq.gz": 15312
                }
            },
            {
                "query_sequence": "CGCGC",
                "source_headers": ["delta"],
                "best_hit": {
                    "reference_id": "gi|2765566|emb|Z78441.1|PSZ78441",
                    "reference_source_file": "ls_orchid.fasta",
                    "alignment_score": 10.0,
                    "aligned_query_span": [0, 5],
                    "aligned_reference_span": [694, 699]
                },
                "read_evidence": {
                    "example.fastq": 0,
                    "SRR020192.fastq.gz": 10
                }
            },
            {
                "query_sequence": "CGTC",
                "source_headers": ["beta"],
                "best_hit": {
                    "reference_id": "gi|2765587|emb|Z78462.1|PSZ78462",
                    "reference_source_file": "ls_orchid.fasta",
                    "alignment_score": 8.0,
                    "aligned_query_span": [0, 4],
                    "aligned_reference_span": [0, 4]
                },
                "read_evidence": {
                    "example.fastq": 0,
                    "SRR020192.fastq.gz": 24468
                }
            }
        ]
    }

    VALID_REFERENCE_SOURCES = {"ls_orchid.fasta", "lupine.nu"}

    # --- Structural Tests ---

    def test_identity_map_exists(self):
        """Verify identity_map.json file was created."""
        assert os.path.exists(self.OUTPUT_PATH), f"Output file not found: {self.OUTPUT_PATH}"

    def test_identity_map_valid_json(self):
        """Verify output is valid JSON."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        assert isinstance(data, dict), "JSON root should be a dictionary"

    def test_identity_map_has_queries_key(self):
        """Verify top-level 'queries' key exists and is a list."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        assert "queries" in data, "Missing required top-level key: queries"
        assert isinstance(data["queries"], list), "'queries' should be a list"

    def test_identity_map_no_extra_top_level_keys(self):
        """Verify no extra top-level keys exist (schema specifies only 'queries')."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        assert set(data.keys()) == {"queries"}, \
            f"Expected only 'queries' key, got: {set(data.keys())}"

    # --- Content Tests: Required Fields ---

    def test_query_has_required_fields(self):
        """Verify each query entry has all required fields."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)

        required_query_fields = {"query_sequence", "source_headers", "best_hit", "read_evidence"}

        for i, query in enumerate(data["queries"]):
            missing = required_query_fields - set(query.keys())
            assert not missing, f"Query {i} missing required fields: {missing}"

    def test_best_hit_has_required_fields(self):
        """Verify each best_hit has all required fields."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)

        required_best_hit_fields = {
            "reference_id", "reference_source_file", "alignment_score",
            "aligned_query_span", "aligned_reference_span"
        }

        for i, query in enumerate(data["queries"]):
            best_hit = query["best_hit"]
            missing = required_best_hit_fields - set(best_hit.keys())
            assert not missing, f"Query {i} best_hit missing required fields: {missing}"

    def test_read_evidence_has_required_fields(self):
        """Verify each read_evidence has the required FASTQ file counts."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)

        required_read_evidence_fields = {"example.fastq", "SRR020192.fastq.gz"}

        for i, query in enumerate(data["queries"]):
            read_evidence = query["read_evidence"]
            missing = required_read_evidence_fields - set(read_evidence.keys())
            assert not missing, f"Query {i} read_evidence missing required fields: {missing}"

    # --- Content Tests: Data Types ---

    def test_query_sequence_is_string(self):
        """Verify query_sequence is a string."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)

        for i, query in enumerate(data["queries"]):
            assert isinstance(query["query_sequence"], str), \
                f"Query {i}: query_sequence should be a string"

    def test_source_headers_is_list_of_strings(self):
        """Verify source_headers is a list of strings."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)

        for i, query in enumerate(data["queries"]):
            assert isinstance(query["source_headers"], list), \
                f"Query {i}: source_headers should be a list"
            for j, header in enumerate(query["source_headers"]):
                assert isinstance(header, str), \
                    f"Query {i}, header {j}: should be a string"

    def test_alignment_score_is_numeric(self):
        """Verify alignment_score is a numeric value."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)

        for i, query in enumerate(data["queries"]):
            score = query["best_hit"]["alignment_score"]
            assert isinstance(score, (int, float)), \
                f"Query {i}: alignment_score should be numeric, got {type(score)}"

    def test_spans_are_two_element_lists(self):
        """Verify aligned spans are two-element lists of integers."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)

        for i, query in enumerate(data["queries"]):
            best_hit = query["best_hit"]

            q_span = best_hit["aligned_query_span"]
            assert isinstance(q_span, list) and len(q_span) == 2, \
                f"Query {i}: aligned_query_span should be a 2-element list"
            assert all(isinstance(x, int) for x in q_span), \
                f"Query {i}: aligned_query_span elements should be integers"

            r_span = best_hit["aligned_reference_span"]
            assert isinstance(r_span, list) and len(r_span) == 2, \
                f"Query {i}: aligned_reference_span should be a 2-element list"
            assert all(isinstance(x, int) for x in r_span), \
                f"Query {i}: aligned_reference_span elements should be integers"

    def test_read_evidence_counts_are_integers(self):
        """Verify read evidence counts are integers."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)

        for i, query in enumerate(data["queries"]):
            for key, value in query["read_evidence"].items():
                assert isinstance(value, int), \
                    f"Query {i}: read_evidence[{key}] should be int, got {type(value)}"

    # --- Content Tests: Constraints ---

    def test_reference_source_file_is_valid(self):
        """Verify reference_source_file is one of the valid options."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)

        for i, query in enumerate(data["queries"]):
            src_file = query["best_hit"]["reference_source_file"]
            assert src_file in self.VALID_REFERENCE_SOURCES, \
                f"Query {i}: invalid reference_source_file '{src_file}', must be one of {self.VALID_REFERENCE_SOURCES}"

    def test_spans_are_zero_based_end_exclusive(self):
        """Verify spans are 0-based, end-exclusive (start < end, start >= 0)."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)

        for i, query in enumerate(data["queries"]):
            best_hit = query["best_hit"]

            q_span = best_hit["aligned_query_span"]
            assert q_span[0] >= 0, f"Query {i}: query span start should be >= 0"
            assert q_span[0] < q_span[1], f"Query {i}: query span start should be < end"

            r_span = best_hit["aligned_reference_span"]
            assert r_span[0] >= 0, f"Query {i}: reference span start should be >= 0"
            assert r_span[0] < r_span[1], f"Query {i}: reference span start should be < end"

    def test_query_span_within_sequence_length(self):
        """Verify query span end does not exceed query sequence length."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)

        for i, query in enumerate(data["queries"]):
            seq_len = len(query["query_sequence"])
            q_span = query["best_hit"]["aligned_query_span"]
            assert q_span[1] <= seq_len, \
                f"Query {i}: query span end ({q_span[1]}) exceeds sequence length ({seq_len})"

    def test_queries_sorted_by_query_sequence(self):
        """Verify queries are sorted by query_sequence ascending."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)

        sequences = [q["query_sequence"] for q in data["queries"]]
        assert sequences == sorted(sequences), \
            f"Queries not sorted by query_sequence ascending: {sequences}"

    def test_read_evidence_counts_non_negative(self):
        """Verify read evidence counts are non-negative."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)

        for i, query in enumerate(data["queries"]):
            for key, value in query["read_evidence"].items():
                assert value >= 0, \
                    f"Query {i}: read_evidence[{key}] should be non-negative, got {value}"

    # --- Value Tests: Exact Matches ---

    def test_query_count(self):
        """Verify the correct number of query entries."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)

        expected_count = len(self.EXPECTED_RESULT["queries"])
        actual_count = len(data["queries"])
        assert actual_count == expected_count, \
            f"Expected {expected_count} queries, got {actual_count}"

    def test_query_sequences(self):
        """Verify exact query sequences."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)

        expected_seqs = [q["query_sequence"] for q in self.EXPECTED_RESULT["queries"]]
        actual_seqs = [q["query_sequence"] for q in data["queries"]]
        assert actual_seqs == expected_seqs, \
            f"Query sequences mismatch: expected {expected_seqs}, got {actual_seqs}"

    def test_source_headers(self):
        """Verify source_headers for each query."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)

        for i, (expected, actual) in enumerate(zip(
            self.EXPECTED_RESULT["queries"], data["queries"]
        )):
            assert actual["source_headers"] == expected["source_headers"], \
                f"Query {i} ({actual['query_sequence']}): source_headers mismatch - " \
                f"expected {expected['source_headers']}, got {actual['source_headers']}"

    def test_best_hit_reference_ids(self):
        """Verify best_hit reference_id for each query."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)

        for i, (expected, actual) in enumerate(zip(
            self.EXPECTED_RESULT["queries"], data["queries"]
        )):
            expected_id = expected["best_hit"]["reference_id"]
            actual_id = actual["best_hit"]["reference_id"]
            assert actual_id == expected_id, \
                f"Query {i} ({actual['query_sequence']}): reference_id mismatch - " \
                f"expected '{expected_id}', got '{actual_id}'"

    def test_best_hit_source_files(self):
        """Verify best_hit reference_source_file for each query."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)

        for i, (expected, actual) in enumerate(zip(
            self.EXPECTED_RESULT["queries"], data["queries"]
        )):
            expected_src = expected["best_hit"]["reference_source_file"]
            actual_src = actual["best_hit"]["reference_source_file"]
            assert actual_src == expected_src, \
                f"Query {i} ({actual['query_sequence']}): reference_source_file mismatch - " \
                f"expected '{expected_src}', got '{actual_src}'"

    def test_alignment_scores(self):
        """Verify alignment_score for each query."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)

        for i, (expected, actual) in enumerate(zip(
            self.EXPECTED_RESULT["queries"], data["queries"]
        )):
            expected_score = expected["best_hit"]["alignment_score"]
            actual_score = actual["best_hit"]["alignment_score"]
            assert math.isclose(actual_score, expected_score, rel_tol=self.TOLERANCE), \
                f"Query {i} ({actual['query_sequence']}): alignment_score mismatch - " \
                f"expected {expected_score}, got {actual_score}"

    def test_aligned_query_spans(self):
        """Verify aligned_query_span for each query."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)

        for i, (expected, actual) in enumerate(zip(
            self.EXPECTED_RESULT["queries"], data["queries"]
        )):
            expected_span = expected["best_hit"]["aligned_query_span"]
            actual_span = actual["best_hit"]["aligned_query_span"]
            assert actual_span == expected_span, \
                f"Query {i} ({actual['query_sequence']}): aligned_query_span mismatch - " \
                f"expected {expected_span}, got {actual_span}"

    def test_aligned_reference_spans(self):
        """Verify aligned_reference_span for each query."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)

        for i, (expected, actual) in enumerate(zip(
            self.EXPECTED_RESULT["queries"], data["queries"]
        )):
            expected_span = expected["best_hit"]["aligned_reference_span"]
            actual_span = actual["best_hit"]["aligned_reference_span"]
            assert actual_span == expected_span, \
                f"Query {i} ({actual['query_sequence']}): aligned_reference_span mismatch - " \
                f"expected {expected_span}, got {actual_span}"

    def test_read_evidence_example_fastq(self):
        """Verify read evidence counts from example.fastq."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)

        for i, (expected, actual) in enumerate(zip(
            self.EXPECTED_RESULT["queries"], data["queries"]
        )):
            expected_count = expected["read_evidence"]["example.fastq"]
            actual_count = actual["read_evidence"]["example.fastq"]
            assert actual_count == expected_count, \
                f"Query {i} ({actual['query_sequence']}): example.fastq count mismatch - " \
                f"expected {expected_count}, got {actual_count}"

    def test_read_evidence_srr_fastq(self):
        """Verify read evidence counts from SRR020192.fastq.gz."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)

        for i, (expected, actual) in enumerate(zip(
            self.EXPECTED_RESULT["queries"], data["queries"]
        )):
            expected_count = expected["read_evidence"]["SRR020192.fastq.gz"]
            actual_count = actual["read_evidence"]["SRR020192.fastq.gz"]
            assert actual_count == expected_count, \
                f"Query {i} ({actual['query_sequence']}): SRR020192.fastq.gz count mismatch - " \
                f"expected {expected_count}, got {actual_count}"

    # --- Individual Query Value Tests ---

    def test_acgta_query_values(self):
        """Verify complete values for ACGTA query."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)

        query = next((q for q in data["queries"] if q["query_sequence"] == "ACGTA"), None)
        assert query is not None, "ACGTA query not found"

        assert query["source_headers"] == ["alpha", "alpha"]
        assert query["best_hit"]["reference_id"] == "gi|2765599|emb|Z78474.1|PKZ78474"
        assert query["best_hit"]["reference_source_file"] == "ls_orchid.fasta"
        assert math.isclose(query["best_hit"]["alignment_score"], 10.0, rel_tol=self.TOLERANCE)
        assert query["best_hit"]["aligned_query_span"] == [0, 5]
        assert query["best_hit"]["aligned_reference_span"] == [50, 55]
        assert query["read_evidence"]["example.fastq"] == 0
        assert query["read_evidence"]["SRR020192.fastq.gz"] == 48

    def test_ccgcc_query_values(self):
        """Verify complete values for CCGCC query."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)

        query = next((q for q in data["queries"] if q["query_sequence"] == "CCGCC"), None)
        assert query is not None, "CCGCC query not found"

        assert query["source_headers"] == ["gamma"]
        assert query["best_hit"]["reference_id"] == "gi|2765627|emb|Z78502.1|PBZ78502"
        assert query["best_hit"]["reference_source_file"] == "ls_orchid.fasta"
        assert math.isclose(query["best_hit"]["alignment_score"], 10.0, rel_tol=self.TOLERANCE)
        assert query["best_hit"]["aligned_query_span"] == [0, 5]
        assert query["best_hit"]["aligned_reference_span"] == [48, 53]
        assert query["read_evidence"]["example.fastq"] == 0
        assert query["read_evidence"]["SRR020192.fastq.gz"] == 15312

    def test_cgcgc_query_values(self):
        """Verify complete values for CGCGC query."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)

        query = next((q for q in data["queries"] if q["query_sequence"] == "CGCGC"), None)
        assert query is not None, "CGCGC query not found"

        assert query["source_headers"] == ["delta"]
        assert query["best_hit"]["reference_id"] == "gi|2765566|emb|Z78441.1|PSZ78441"
        assert query["best_hit"]["reference_source_file"] == "ls_orchid.fasta"
        assert math.isclose(query["best_hit"]["alignment_score"], 10.0, rel_tol=self.TOLERANCE)
        assert query["best_hit"]["aligned_query_span"] == [0, 5]
        assert query["best_hit"]["aligned_reference_span"] == [694, 699]
        assert query["read_evidence"]["example.fastq"] == 0
        assert query["read_evidence"]["SRR020192.fastq.gz"] == 10

    def test_cgtc_query_values(self):
        """Verify complete values for CGTC query."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)

        query = next((q for q in data["queries"] if q["query_sequence"] == "CGTC"), None)
        assert query is not None, "CGTC query not found"

        assert query["source_headers"] == ["beta"]
        assert query["best_hit"]["reference_id"] == "gi|2765587|emb|Z78462.1|PSZ78462"
        assert query["best_hit"]["reference_source_file"] == "ls_orchid.fasta"
        assert math.isclose(query["best_hit"]["alignment_score"], 8.0, rel_tol=self.TOLERANCE)
        assert query["best_hit"]["aligned_query_span"] == [0, 4]
        assert query["best_hit"]["aligned_reference_span"] == [0, 4]
        assert query["read_evidence"]["example.fastq"] == 0
        assert query["read_evidence"]["SRR020192.fastq.gz"] == 24468
