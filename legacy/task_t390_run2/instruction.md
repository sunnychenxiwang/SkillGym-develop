Create a single JSON artifact that verifies whether `/root/ex1.bam` is structurally consistent with the BAM/SAM specification described in the saved GitHub HTML page `/root/learning_bam_file`.

Specifically:

1. **From the HTML file** (`learning_bam_file`), extract the canonical BAM “magic” identifier string that the spec says must appear at the start of a BAM file (the 4-byte ASCII magic).
2. **From the BAM file** (`ex1.bam`), read the first 4 bytes (after BGZF decompression via `pysam`) and interpret them as an ASCII string.
3. Compare the two strings and write the result to:

`/root/harbor_workspaces/task_T390_run2/output/bam_magic_check.json`

with exactly this schema:

```json
{
  "spec_magic": "....",
  "observed_magic": "....",
  "matches": true
}
```

Constraints:
- The task is complete only if the JSON file is written to the exact path above.
- `spec_magic` must come from the HTML content (not from prior knowledge).
- `observed_magic` must come from programmatically reading `ex1.bam` using available bioinformatics tooling (e.g., `pysam`), not by treating the BAM as plain text.