Create a **single JSON artifact** that identifies the **most likely adapter/primer motif shared by both datasets** by combining evidence from the small control FASTQ and the large SRR FASTQ.

1) Parse `/root/example.fastq` and compute the **exact consensus sequence** (A/C/G/T only; ties broken lexicographically A<C<G<T) across all reads at each position (reads are equal length). Call this `control_consensus`.

2) Parse `/root/SRR020192.fastq.gz` and, using only reads with **mean Phred quality ≥ 30**, compute the **per-position base frequencies** for positions 1–25 (1-based). For each position, take the most frequent base (ties broken lexicographically) to form a 25-nt string `srr_mode25`.

3) Compute the **longest common substring (contiguous)** between `control_consensus` and `srr_mode25`. If multiple substrings share the same maximum length, choose the one with the **lowest start index in `control_consensus`**, and if still tied, the lowest start index in `srr_mode25`. Call this substring `shared_motif`.

4) Save the following JSON exactly to:
`/root/output/shared_motif.json`

```json
{
  "control_consensus": "STRING",
  "srr_mode25": "STRING",
  "shared_motif": "STRING",
  "control_start_1based": 0,
  "srr_start_1based": 0,
  "motif_length": 0,
  "srr_reads_used": 0
}
```

Where `control_start_1based` and `srr_start_1based` are the 1-based start positions of `shared_motif` within `control_consensus` and `srr_mode25`, respectively, and `srr_reads_used` is the number of SRR reads passing the mean-quality filter. Writing this file is mandatory.