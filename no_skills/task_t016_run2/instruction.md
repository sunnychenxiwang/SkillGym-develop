Create a single JSON “sequence identity reconciliation” artifact that links the **duplicate test FASTA** to the **real biological sequences** and reports the uniquely determined closest match.

1) Parse **all three** input files as nucleotide FASTA:
- `/root/dups.fasta`
- `/root/ls_orchid.fasta`
- `/root/lupine.nu`

2) From `dups.fasta`, collapse records by ID and verify that the only duplicated ID is `alpha` and that all its sequences are identical. Use the **unique** `alpha` DNA sequence as the query.

3) For every record in `ls_orchid.fasta` **and** the single record in `lupine.nu`, compute the **minimum k-mer distance** between the query and the target over **k = 2, 3, 4** (use scikit-bio `kmer_distance`; for each target take `min(distance_k2, distance_k3, distance_k4)` as that target’s score). Compare sequences as-is (do not reverse-complement, trim, or align).

4) Identify the single target record (across both files) with the **lowest** score. If there is a tie, break it deterministically by choosing the lexicographically smallest target record ID (full FASTA identifier up to first whitespace).

5) Write the result to **exactly** this file path:
`/root/alpha_best_kmer_match.json`

The JSON must have this exact schema (numbers as JSON numbers):
```json
{
  "query_id": "alpha",
  "query_sequence": "ACGTA",
  "query_source_file": "dups.fasta",
  "target_id": "<best_id>",
  "target_source_file": "<ls_orchid.fasta|lupine.nu>",
  "target_length": <int>,
  "best_k": <2|3|4>,
  "best_distance": <float>,
  "all_k_distances": { "2": <float>, "3": <float>, "4": <float> }
}
```
Where `all_k_distances` are the distances for the chosen best target, and `best_k/best_distance` correspond to the minimum among them.