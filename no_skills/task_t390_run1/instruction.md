Create a single JSON artifact that **validates whether the BAM file `/root/ex1.bam` is consistent with the BAM/SAM format expectations described in the GitHub HTML snapshot `/root/learning_bam_file`**, by extracting and cross-checking **exactly these three format-level facts**:

1) From `learning_bam_file` (HTML): extract the repository’s **one-line description text** (the string shown on the page describing what the repo is about).  
2) From `ex1.bam` (using `pysam`): extract the BAM header’s **SQ reference sequence dictionary** and compute:
   - `n_references` = number of `@SQ` entries
   - `reference_names_sorted` = the list of reference names sorted lexicographically
3) Using both files together: determine whether the BAM’s header content is semantically aligned with the educational “SAM/BAM format” purpose indicated by the HTML description by applying this deterministic rule:
   - `is_format_consistent = true` iff (`n_references > 0`) AND (every `@SQ` entry has both `SN` and `LN` fields present in the parsed header)

Save the result **as a single JSON file** at:

`/root/bam_format_consistency.json`

with exactly this schema (no extra keys):

```json
{
  "repo_description": "…",
  "n_references": 0,
  "reference_names_sorted": ["…"],
  "is_format_consistent": false
}
```

Notes:
- You must parse the HTML locally from the provided snapshot file (do not use the network).
- You must read the BAM using `pysam` (do not shell out to external tools).
- The final deliverable is the JSON file at the exact path above.