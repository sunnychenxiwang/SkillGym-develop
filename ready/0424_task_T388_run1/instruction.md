Create a single Excel QC workbook that links read-level evidence from the FASTQ files to alignment-level evidence from the BAM file, and includes one uniquely checkable “best-supported read” result.

Using **all four provided input files**:

1. **From `/root/example.fastq` (Biopython):**  
   Parse all reads and compute each read’s GC fraction and mean Phred quality. Keep their read IDs exactly as in the FASTQ headers.

2. **From `/root/SRR020192.fastq.gz` (Biopython):**  
   Stream-parse the gzipped FASTQ and find the **first read (in file order)** whose sequence starts with either `GATGACGGTGT` or `GACGACGGTGT`. For that single read, compute GC fraction and mean Phred quality.

3. **From `/root/ex1.bam` (pysam):**  
   Index the BAM if needed, then for each read ID obtained in steps (1) and (2), look up alignments in the BAM and compute:
   - `is_aligned` (true if at least one non-unmapped alignment exists)
   - `best_mapq` (maximum MAPQ across its alignments; 0 if none)
   - `best_ref` and `best_pos0` (reference name and 0-based start of the alignment achieving `best_mapq`; blank if none)

4. **From `/root/learning_bam_file` (HTML):**  
   Extract the repository title text from the HTML (the human-readable repo name shown on the page, e.g., “learning_bam_file”), and use that exact extracted string as the Excel workbook’s “Source” field.

5. **Primary objective (requires pydeseq2 + xlsx):**  
   Build a small, deterministic scoring model to select **exactly one** “best-supported read” across the combined candidate set (all reads from `example.fastq` plus the single primer-matching read from `SRR020192.fastq.gz`):
   - Create a count matrix where each candidate read is a “gene” and there are exactly two “samples”: `fastq_metrics` and `bam_metrics`.
   - Define counts deterministically as:
     - `fastq_metrics` count = `round(mean_phred * 100)` (integer)
     - `bam_metrics` count = `best_mapq` (integer)
   - Run `pydeseq2` with design `~ sample_type` and contrast `['sample_type','bam_metrics','fastq_metrics']`.
   - Choose the single “best-supported read” as the candidate with the **smallest adjusted p-value (`padj`)**, breaking ties by higher `log2FoldChange`, then by lexicographically smallest read ID.

6. **Write the final deliverable (mandatory) to:**  
   `/root/output/read_alignment_qc.xlsx`

The Excel file must contain exactly these sheets and required cells/columns:

- Sheet **`Summary`**
  - Cell `A1`: `Source`
  - Cell `B1`: the extracted repo title string from `learning_bam_file`
  - Cell `A2`: `best_supported_read_id`
  - Cell `B2`: the selected read ID (from step 5)
  - Cell `A3`: `best_supported_read_padj`
  - Cell `B3`: the selected read’s `padj` value (as a number)

- Sheet **`Candidates`** with a header row and one row per candidate read, containing columns (in this order):
  1. `read_id`
  2. `origin` (either `example.fastq` or `SRR020192.fastq.gz`)
  3. `sequence_length`
  4. `gc_fraction`
  5. `mean_phred`
  6. `is_aligned`
  7. `best_mapq`
  8. `best_ref`
  9. `best_pos0`
  10. `deseq2_log2FoldChange`
  11. `deseq2_padj`

Apply Excel formatting:
- Freeze the header row in `Candidates`.
- Make the header row bold with an autofilter enabled over all populated columns.

The workbook content must be fully reproducible from the provided files, and the “best-supported read” must be uniquely determined by the specified rules.