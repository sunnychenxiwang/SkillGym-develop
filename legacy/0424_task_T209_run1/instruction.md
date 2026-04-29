Build a single, reproducible “cross-dataset sequence identity map” that links short test sequences to real biological sequences and to read evidence.

Using **all five input files**:

1. Parse **`/root/dups.fasta`** and collapse duplicate records by sequence (not by header): treat identical sequences as one query, but keep a list of all headers that shared that sequence.
2. Parse **`/root/ls_orchid.fasta`** and **`/root/lupine.nu`** as the reference set (each FASTA record is a reference sequence).
3. For each collapsed query sequence from (1), find the **single best** reference hit across the combined reference set (orchids + lupine) using **local nucleotide alignment**; break ties deterministically by: higher alignment score, then higher aligned length, then lexicographically smallest reference record id.
4. Validate the alignment-derived best hit by checking read evidence:
   - From **`/root/example.fastq`** and **`/root/SRR020192.fastq.gz`**, count how many reads contain the query sequence as an exact substring (case-insensitive; treat `N` in reads as a literal character, i.e., it only matches `N`).
   - Report counts separately for `example.fastq` and `SRR020192.fastq.gz`.
5. Write exactly one JSON file to **`/root/output/identity_map.json`** with this schema (and no extra top-level keys), where `queries` is sorted by `query_sequence` ascending:

```json
{
  "queries": [
    {
      "query_sequence": "ACGTA",
      "source_headers": ["alpha", "alpha"],
      "best_hit": {
        "reference_id": "gi|...|emb|...|...",
        "reference_source_file": "ls_orchid.fasta",
        "alignment_score": 123.0,
        "aligned_query_span": [0, 5],
        "aligned_reference_span": [456, 461]
      },
      "read_evidence": {
        "example.fastq": 0,
        "SRR020192.fastq.gz": 17
      }
    }
  ]
}
```

Notes:
- `aligned_*_span` must be **0-based, end-exclusive** coordinates on the original (unaligned) sequences.
- `alignment_score` must be a numeric value exactly as produced by your alignment implementation (don’t round).
- `reference_source_file` must be exactly one of: `"ls_orchid.fasta"` or `"lupine.nu"`.
- The task is complete only if the JSON file is written to the specified path and is fully derivable from the provided inputs.