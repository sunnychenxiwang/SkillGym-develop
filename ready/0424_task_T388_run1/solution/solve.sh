#!/bin/bash
set -e

# Create output directory
mkdir -p /root/output

# Create the solution Python script using heredoc
cat << 'EOF' > /root/solve_task.py
#!/usr/bin/env python3
"""QC Pipeline: FASTQ + BAM analysis with DESeq2-based best-read selection."""

import gzip
import os
import re
import math
from pathlib import Path

import pandas as pd
import numpy as np
from Bio import SeqIO
from Bio.SeqUtils import gc_fraction
import pysam
from pydeseq2.dds import DeseqDataSet
from pydeseq2.ds import DeseqStats
from openpyxl import Workbook
from openpyxl.styles import Font

BASE_DIR = Path("/root")
INPUT_DIR = BASE_DIR 
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_PATH = OUTPUT_DIR / "read_alignment_qc.xlsx"

def parse_example_fastq():
    """Parse example.fastq and compute GC fraction and mean Phred quality."""
    candidates = []
    for record in SeqIO.parse(INPUT_DIR / "example.fastq", "fastq"):
        read_id = record.id
        seq_len = len(record)
        gc_frac = gc_fraction(record.seq)
        qualities = record.letter_annotations["phred_quality"]
        mean_phred = sum(qualities) / len(qualities)
        candidates.append({
            "read_id": read_id,
            "origin": "example.fastq",
            "sequence_length": seq_len,
            "gc_fraction": gc_frac,
            "mean_phred": mean_phred
        })
    return candidates

def parse_gz_fastq():
    """Stream-parse SRR020192.fastq.gz for first primer-matching read."""
    primers = ("GATGACGGTGT", "GACGACGGTGT")
    with gzip.open(INPUT_DIR / "SRR020192.fastq.gz", "rt") as handle:
        for record in SeqIO.parse(handle, "fastq"):
            seq_str = str(record.seq)
            if seq_str.startswith(primers):
                gc_frac = gc_fraction(record.seq)
                qualities = record.letter_annotations["phred_quality"]
                mean_phred = sum(qualities) / len(qualities)
                return {
                    "read_id": record.id,
                    "origin": "SRR020192.fastq.gz",
                    "sequence_length": len(record),
                    "gc_fraction": gc_frac,
                    "mean_phred": mean_phred
                }
    raise ValueError("No primer-matching read found in SRR020192.fastq.gz")

def get_bam_metrics(candidates, bam_path):
    """Query BAM for alignment metrics for each candidate read."""
    bai_path = str(bam_path) + ".bai"
    if not os.path.exists(bai_path):
        pysam.index(str(bam_path))

    target_ids = {c["read_id"] for c in candidates}
    alignments_by_read = {rid: [] for rid in target_ids}

    samfile = pysam.AlignmentFile(str(bam_path), "rb")
    for read in samfile.fetch(until_eof=True):
        if read.query_name in target_ids:
            alignments_by_read[read.query_name].append(read)
    samfile.close()

    for c in candidates:
        rid = c["read_id"]
        alns = alignments_by_read[rid]
        non_unmapped = [a for a in alns if not a.is_unmapped]

        if non_unmapped:
            c["is_aligned"] = True
            best_aln = max(non_unmapped, key=lambda a: a.mapping_quality)
            c["best_mapq"] = best_aln.mapping_quality
            c["best_ref"] = best_aln.reference_name
            c["best_pos0"] = best_aln.reference_start
        else:
            c["is_aligned"] = False
            c["best_mapq"] = 0
            c["best_ref"] = ""
            c["best_pos0"] = ""

    return candidates

def extract_repo_title():
    """Extract repository title from HTML file."""
    html_path = INPUT_DIR / "learning_bam_file"
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Look for itemprop="name" pattern
    match = re.search(r'itemprop="name"[^>]*>.*?<a[^>]*>([^<]+)</a>', content, re.DOTALL)
    if match:
        return match.group(1).strip()

    # Fallback: extract from title tag
    match = re.search(r'<title>GitHub - [^/]+/([^:]+):', content)
    if match:
        return match.group(1).strip()

    return "learning_bam_file"

def run_deseq2(candidates):
    """Run pydeseq2 analysis with technical replicates."""
    read_ids = [c["read_id"] for c in candidates]

    # Create counts: fastq_metrics = round(mean_phred * 100), bam_metrics = best_mapq
    fastq_counts = [round(c["mean_phred"] * 100) for c in candidates]
    bam_counts = [int(c["best_mapq"]) for c in candidates]

    # DESeq2 requires replicates - create technical replicates
    counts_df = pd.DataFrame(
        [fastq_counts, fastq_counts, bam_counts, bam_counts],
        index=["fastq_metrics_1", "fastq_metrics_2", "bam_metrics_1", "bam_metrics_2"],
        columns=read_ids
    ).astype(int)

    # Add pseudo-count to avoid all-zero issues
    counts_df = counts_df + 1

    # Metadata with sample_type factor
    metadata = pd.DataFrame(
        {"sample_type": ["fastq_metrics", "fastq_metrics", "bam_metrics", "bam_metrics"]},
        index=["fastq_metrics_1", "fastq_metrics_2", "bam_metrics_1", "bam_metrics_2"]
    )

    # Run DESeq2
    dds = DeseqDataSet(
        counts=counts_df,
        metadata=metadata,
        design="~ sample_type",
        refit_cooks=False
    )
    dds.deseq2()

    ds = DeseqStats(dds, contrast=["sample_type", "bam_metrics", "fastq_metrics"])
    ds.summary()

    results = ds.results_df

    # Join results back to candidates
    for c in candidates:
        rid = c["read_id"]
        if rid in results.index:
            c["deseq2_log2FoldChange"] = results.loc[rid, "log2FoldChange"]
            c["deseq2_padj"] = results.loc[rid, "padj"]
        else:
            c["deseq2_log2FoldChange"] = float("nan")
            c["deseq2_padj"] = float("nan")

    return candidates, results

def select_best_read(candidates):
    """Select best-supported read: smallest padj, then higher log2FoldChange, then lexicographic."""
    def sort_key(c):
        padj = c["deseq2_padj"]
        lfc = c["deseq2_log2FoldChange"]
        rid = c["read_id"]

        padj_is_nan = 1 if (pd.isna(padj) or math.isnan(padj)) else 0
        padj_val = padj if not padj_is_nan else float("inf")

        lfc_is_nan = 1 if (pd.isna(lfc) or math.isnan(lfc)) else 0
        lfc_val = -lfc if not lfc_is_nan else float("inf")

        return (padj_is_nan, padj_val, lfc_is_nan, lfc_val, rid)

    sorted_candidates = sorted(candidates, key=sort_key)
    return sorted_candidates[0]

def write_excel(candidates, best_read, repo_title, output_path):
    """Write Excel workbook with Summary and Candidates sheets."""
    wb = Workbook()

    # Summary sheet
    ws_summary = wb.active
    ws_summary.title = "Summary"
    ws_summary["A1"] = "Source"
    ws_summary["B1"] = repo_title
    ws_summary["A2"] = "best_supported_read_id"
    ws_summary["B2"] = best_read["read_id"]
    ws_summary["A3"] = "best_supported_read_padj"
    padj_val = best_read["deseq2_padj"]
    ws_summary["B3"] = padj_val if not (pd.isna(padj_val) or math.isnan(padj_val)) else ""

    # Candidates sheet
    ws_candidates = wb.create_sheet("Candidates")
    headers = [
        "read_id", "origin", "sequence_length", "gc_fraction", "mean_phred",
        "is_aligned", "best_mapq", "best_ref", "best_pos0",
        "deseq2_log2FoldChange", "deseq2_padj"
    ]

    # Write header row with bold font
    for col_idx, header in enumerate(headers, 1):
        cell = ws_candidates.cell(row=1, column=col_idx, value=header)
        cell.font = Font(bold=True)

    # Write data rows
    for row_idx, c in enumerate(candidates, 2):
        ws_candidates.cell(row=row_idx, column=1, value=c["read_id"])
        ws_candidates.cell(row=row_idx, column=2, value=c["origin"])
        ws_candidates.cell(row=row_idx, column=3, value=c["sequence_length"])
        ws_candidates.cell(row=row_idx, column=4, value=c["gc_fraction"])
        ws_candidates.cell(row=row_idx, column=5, value=c["mean_phred"])
        ws_candidates.cell(row=row_idx, column=6, value=c["is_aligned"])
        ws_candidates.cell(row=row_idx, column=7, value=c["best_mapq"])
        ws_candidates.cell(row=row_idx, column=8, value=c["best_ref"] if c["best_ref"] != "" else None)
        ws_candidates.cell(row=row_idx, column=9, value=c["best_pos0"] if c["best_pos0"] != "" else None)

        lfc = c["deseq2_log2FoldChange"]
        ws_candidates.cell(row=row_idx, column=10, value=lfc if not (pd.isna(lfc) or math.isnan(lfc)) else None)

        padj = c["deseq2_padj"]
        ws_candidates.cell(row=row_idx, column=11, value=padj if not (pd.isna(padj) or math.isnan(padj)) else None)

    # Freeze header row
    ws_candidates.freeze_panes = "A2"

    # Add autofilter over all populated columns
    last_row = len(candidates) + 1
    ws_candidates.auto_filter.ref = f"A1:K{last_row}"

    wb.save(output_path)
    return output_path

def main():
    # Step 1: Parse example.fastq
    candidates = parse_example_fastq()

    # Step 2: Parse SRR020192.fastq.gz for primer-matching read
    gz_read = parse_gz_fastq()
    candidates.append(gz_read)

    # Step 3: Get BAM alignment metrics
    bam_path = INPUT_DIR / "ex1.bam"
    candidates = get_bam_metrics(candidates, bam_path)

    # Step 4: Extract repo title from HTML
    repo_title = extract_repo_title()

    # Step 5: Run pydeseq2 analysis
    candidates, results = run_deseq2(candidates)

    # Step 5b: Select best-supported read
    best_read = select_best_read(candidates)

    # Step 6: Write Excel workbook
    write_excel(candidates, best_read, repo_title, OUTPUT_PATH)

if __name__ == "__main__":
    main()
EOF

# Execute the script
python3 /root/solve_task.py
