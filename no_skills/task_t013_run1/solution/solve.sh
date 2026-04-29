#!/bin/bash
set -euo pipefail

# Input/output at /root (Harbor local environment symlinks files here)
IN_DIR="/root"
OUT_DIR="/root"

python3 << 'PYEOF'
import pysam
import json
import os
import re

IN_DIR = "/root"
OUT_DIR = "/root"

BAM_PATH = os.path.join(IN_DIR, "ex1.bam")
LEARNING_FILE = os.path.join(IN_DIR, "learning_bam_file")
OUTPUT_PATH = os.path.join(OUT_DIR, "contig_max_unmapped_fraction.json")

# Step 1: Extract UNMAP FLAG bit from learning_bam_file
with open(LEARNING_FILE, "r", encoding="utf-8", errors="replace") as f:
    content = f.read()

# Pattern matches: ##    0x4     4  UNMAP          segment unmapped
pattern = r"##\s+0x([0-9a-fA-F]+)\s+(\d+)\s+UNMAP\b"
matches = re.findall(pattern, content)

if not matches:
    raise ValueError("Could not find UNMAP flag documentation in learning_bam_file")

hex_val, dec_val = matches[0]
unmap_bit = int(dec_val)

# Step 2: Read BAM and compute per-contig stats
stats = {}
with pysam.AlignmentFile(BAM_PATH, "rb") as bam:
    # Initialize all references from header
    for ref in bam.references:
        stats[ref] = {"mapped": 0, "unmapped": 0}

    # Count reads - only count those with valid reference_name
    for read in bam.fetch(until_eof=True):
        ref_name = read.reference_name
        if not ref_name or ref_name not in stats:
            continue
        if (read.flag & unmap_bit) != 0:
            stats[ref_name]["unmapped"] += 1
        else:
            stats[ref_name]["mapped"] += 1

# Step 3: Calculate fractions
for ref in stats:
    total = stats[ref]["mapped"] + stats[ref]["unmapped"]
    if total > 0:
        stats[ref]["fraction"] = stats[ref]["unmapped"] / total
    else:
        stats[ref]["fraction"] = 0.0

# Step 4: Find contig with max unmapped fraction (lexicographic tiebreaker)
max_fraction = max(s["fraction"] for s in stats.values())
tied_contigs = [c for c, s in stats.items() if s["fraction"] == max_fraction]
selected_contig = min(tied_contigs)  # lexicographically smallest

# Step 5: Build output
selected_stats = stats[selected_contig]
output = {
    "flag_unmapped_bit_from_doc": unmap_bit,
    "contig": selected_contig,
    "mapped_reads": selected_stats["mapped"],
    "unmapped_reads": selected_stats["unmapped"],
    "unmapped_fraction": round(selected_stats["fraction"], 6),
}

with open(OUTPUT_PATH, "w") as f:
    json.dump(output, f, indent=2)
    f.write("\n")

print(f"Output written to {OUTPUT_PATH}")
PYEOF

echo "solve.sh completed"
