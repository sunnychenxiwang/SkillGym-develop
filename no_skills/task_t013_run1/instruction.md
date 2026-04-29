Using **both** `/root/ex1.bam` and `/root/learning_bam_file`, create a single JSON artifact that answers this question:

**“Which reference sequence (contig) in `ex1.bam` has the highest fraction of unmapped reads, and what is that fraction?”**

Requirements (must all be met):

1. **Use `learning_bam_file` to determine the correct interpretation of “unmapped read” from the SAM/BAM FLAG field** (i.e., identify the exact bit value for unmapped and apply it when classifying reads from the BAM).  
2. **Use `pysam` to read `ex1.bam` and compute, for each contig present in the BAM header**:
   - `mapped_reads`: number of reads mapped to that contig (exclude unmapped)
   - `unmapped_reads`: number of reads whose FLAG indicates unmapped **and** whose `reference_name` equals that contig (i.e., unmapped reads assigned to that reference in the BAM; do not count reads with no reference name)
   - `unmapped_fraction = unmapped_reads / (mapped_reads + unmapped_reads)`
3. Select the single contig with the **maximum** `unmapped_fraction`. Break ties deterministically by choosing the lexicographically smallest contig name.
4. Write the result to **exactly** this path (writing the file is mandatory):  
   `/root/contig_max_unmapped_fraction.json`

The JSON must have this exact schema:

```json
{
  "flag_unmapped_bit_from_doc": 4,
  "contig": "chr1",
  "mapped_reads": 0,
  "unmapped_reads": 0,
  "unmapped_fraction": 0.0
}
```

Notes:
- `flag_unmapped_bit_from_doc` must be the integer bit value you extracted from `learning_bam_file` (not hardcoded without verifying it in that file).
- `unmapped_fraction` must be a floating-point number rounded to **6 decimal places**.