#!/bin/bash
set -e

# Create the solution Python script using heredoc
cat << 'EOF' > /root/solve_task.py
#!/usr/bin/env python3
import gzip
import json
import os
from collections import defaultdict
from Bio import SeqIO

INPUT_DIR = '/root'
OUTPUT_PATH = '/root/output/shared_motif.json'

def compute_control_consensus(fastq_path):
    """Compute consensus from control FASTQ. Ties broken lexicographically A<C<G<T."""
    base_order = ['A', 'C', 'G', 'T']
    sequences = []

    for record in SeqIO.parse(fastq_path, "fastq"):
        sequences.append(str(record.seq).upper())

    seq_len = len(sequences[0])
    consensus = []
    for pos in range(seq_len):
        counts = defaultdict(int)
        for seq in sequences:
            base = seq[pos]
            if base in base_order:
                counts[base] += 1

        max_count = 0
        chosen_base = 'A'
        for base in base_order:
            if counts[base] > max_count:
                max_count = counts[base]
                chosen_base = base
        consensus.append(chosen_base)

    return ''.join(consensus)

def compute_srr_mode25(fastq_gz_path, min_mean_quality=30):
    """Compute mode for positions 1-25 from high-quality SRR reads."""
    base_order = ['A', 'C', 'G', 'T']
    counts = [[0, 0, 0, 0] for _ in range(25)]
    base_idx = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
    reads_used = 0

    with gzip.open(fastq_gz_path, "rt") as handle:
        for record in SeqIO.parse(handle, "fastq"):
            quals = record.letter_annotations["phred_quality"]
            mean_qual = sum(quals) / len(quals)

            if mean_qual < min_mean_quality:
                continue

            seq = str(record.seq).upper()
            if len(seq) < 25:
                continue

            reads_used += 1
            for pos in range(25):
                base = seq[pos]
                if base in base_idx:
                    counts[pos][base_idx[base]] += 1

    mode25 = []
    for pos in range(25):
        max_count = max(counts[pos])
        for i, base in enumerate(base_order):
            if counts[pos][i] == max_count:
                mode25.append(base)
                break

    return ''.join(mode25), reads_used

def longest_common_substring(s1, s2):
    """Find LCS with tie-breaking: max length, then lowest s1 start, then lowest s2 start."""
    len1, len2 = len(s1), len(s2)

    for length in range(min(len1, len2), 0, -1):
        for i in range(len1 - length + 1):
            substr = s1[i:i+length]
            for j in range(len2 - length + 1):
                if s2[j:j+length] == substr:
                    return substr, i, j

    return "", 0, 0

def main():
    control_path = os.path.join(INPUT_DIR, "example.fastq")
    srr_path = os.path.join(INPUT_DIR, "SRR020192.fastq.gz")

    control_consensus = compute_control_consensus(control_path)
    srr_mode25, srr_reads_used = compute_srr_mode25(srr_path)
    shared_motif, ctrl_start, srr_start = longest_common_substring(control_consensus, srr_mode25)

    result = {
        "control_consensus": control_consensus,
        "srr_mode25": srr_mode25,
        "shared_motif": shared_motif,
        "control_start_1based": ctrl_start + 1,
        "srr_start_1based": srr_start + 1,
        "motif_length": len(shared_motif),
        "srr_reads_used": srr_reads_used
    }

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(result, f, indent=2)

if __name__ == "__main__":
    main()
EOF

# Execute the script
python3 /root/solve_task.py
