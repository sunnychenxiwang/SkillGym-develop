#!/bin/bash
set -e

# Create the solution Python script using heredoc
cat << 'EOF' > /root/solve_task.py
#!/usr/bin/env python3
"""
Build a cross-dataset sequence identity map linking short test sequences
to real biological sequences and read evidence.
"""

import json
import gzip
import os
from collections import OrderedDict
from Bio import SeqIO
from skbio import DNA
from skbio.alignment import local_pairwise_align_nucleotide

# File paths
DUPS_FASTA = "/root/dups.fasta"
ORCHID_FASTA = "/root/ls_orchid.fasta"
LUPINE_FASTA = "/root/lupine.nu"
EXAMPLE_FASTQ = "/root/example.fastq"
SRR_FASTQ_GZ = "/root/SRR020192.fastq.gz"
OUTPUT_PATH = "/root/output/identity_map.json"

# Create a substitution matrix that includes N (ambiguous base)
def make_nucleotide_substitution_matrix(match_score=2, mismatch_score=-3):
    """Create nucleotide substitution matrix that handles N characters."""
    chars = 'ACGTN'
    sub_matrix = {}
    for c1 in chars:
        sub_matrix[c1] = {}
        for c2 in chars:
            if c1 == c2:
                sub_matrix[c1][c2] = match_score if c1 != 'N' else 0
            elif c1 == 'N' or c2 == 'N':
                sub_matrix[c1][c2] = 0  # N vs anything is neutral
            else:
                sub_matrix[c1][c2] = mismatch_score
    return sub_matrix

SUBSTITUTION_MATRIX = make_nucleotide_substitution_matrix()


def parse_and_collapse_queries(fasta_path):
    """
    Parse FASTA file and collapse duplicate records by sequence (not header).
    Returns list of dicts with query_sequence and source_headers.
    """
    queries = OrderedDict()
    for rec in SeqIO.parse(fasta_path, "fasta"):
        seq = str(rec.seq).upper()
        if seq not in queries:
            queries[seq] = {"query_sequence": seq, "source_headers": []}
        queries[seq]["source_headers"].append(rec.id)
    return list(queries.values())


def parse_references(paths_with_names):
    """
    Parse reference FASTA files.
    Returns list of dicts with reference_id, reference_source_file, sequence.
    """
    refs = []
    for src_path, src_name in paths_with_names:
        for rec in SeqIO.parse(src_path, "fasta"):
            refs.append({
                "reference_id": rec.id,
                "reference_source_file": src_name,
                "sequence": str(rec.seq).upper()
            })
    return refs


def find_best_hit(query_seq, refs):
    """
    Find the single best local alignment hit across all references.
    Tie-break: highest score, then highest aligned length, then lexicographically smallest reference_id.
    """
    qdna = DNA(query_seq)
    best = None
    best_key = None

    for r in refs:
        rdna = DNA(r["sequence"])
        msa, score, spans = local_pairwise_align_nucleotide(qdna, rdna, substitution_matrix=SUBSTITUTION_MATRIX)
        (q0, q1_incl), (r0, r1_incl) = spans
        # Convert to integers and make end-exclusive (task requires 0-based, end-exclusive)
        q0, q1 = int(q0), int(q1_incl) + 1
        r0, r1 = int(r0), int(r1_incl) + 1
        aln_len = q1 - q0

        cand = {
            "reference_id": r["reference_id"],
            "reference_source_file": r["reference_source_file"],
            "alignment_score": float(score),
            "aligned_query_span": [q0, q1],
            "aligned_reference_span": [r0, r1],
        }

        # Key for deterministic tie-break: (-score, -aln_len, reference_id)
        key = (-score, -aln_len, r["reference_id"])

        if best is None or key < best_key:
            best = cand
            best_key = key

    return best


def count_reads_containing(query_seq, fastq_path, gz=False):
    """
    Count how many reads contain the query sequence as an exact substring (case-insensitive).
    N is treated as a literal character (only matches N).
    """
    q = query_seq.upper()
    opener = gzip.open if gz else open
    count = 0
    with opener(fastq_path, "rt") as fh:
        for rec in SeqIO.parse(fh, "fastq"):
            if q in str(rec.seq).upper():
                count += 1
    return count


def main():
    # Step 1: Parse and collapse query sequences
    collapsed_queries = parse_and_collapse_queries(DUPS_FASTA)

    # Step 2: Parse reference sequences
    refs = parse_references([
        (ORCHID_FASTA, "ls_orchid.fasta"),
        (LUPINE_FASTA, "lupine.nu")
    ])

    # Step 3: Find best hit and count read evidence for each query
    results = []
    for q in collapsed_queries:
        qseq = q["query_sequence"]
        best_hit = find_best_hit(qseq, refs)

        example_count = count_reads_containing(qseq, EXAMPLE_FASTQ, gz=False)
        srr_count = count_reads_containing(qseq, SRR_FASTQ_GZ, gz=True)

        results.append({
            "query_sequence": qseq,
            "source_headers": q["source_headers"],
            "best_hit": best_hit,
            "read_evidence": {
                "example.fastq": example_count,
                "SRR020192.fastq.gz": srr_count
            }
        })

    # Step 4: Sort by query_sequence ascending and write output
    results.sort(key=lambda d: d["query_sequence"])

    output = {"queries": results}

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2)


if __name__ == "__main__":
    main()
EOF

# Execute the script
python3 /root/solve_task.py
