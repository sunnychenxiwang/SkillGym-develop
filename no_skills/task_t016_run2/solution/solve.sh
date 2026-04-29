#!/bin/bash
set -e

# HARBOR_PATH_FIX_START
BASE_FIX="/root/harbor_workspaces/task_T016_run2"
mkdir -p "$BASE_FIX/input" "$BASE_FIX/output"
if [ ! -e "$BASE_FIX/input/dups.fasta" ] && [ -e "/root/dups.fasta" ]; then cp -f "/root/dups.fasta" "$BASE_FIX/input/dups.fasta"; fi
if [ ! -e "$BASE_FIX/input/ls_orchid.fasta" ] && [ -e "/root/ls_orchid.fasta" ]; then cp -f "/root/ls_orchid.fasta" "$BASE_FIX/input/ls_orchid.fasta"; fi
if [ ! -e "$BASE_FIX/input/lupine.nu" ] && [ -e "/root/lupine.nu" ]; then cp -f "/root/lupine.nu" "$BASE_FIX/input/lupine.nu"; fi
# HARBOR_PATH_FIX_END

#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="/root/harbor_workspaces/task_T016_run2"
INPUT_DIR="$BASE_DIR/input"
OUTPUT_DIR="$BASE_DIR/output"
OUTPUT_FILE="$OUTPUT_DIR/alpha_best_kmer_match.json"

DUPS_FASTA="$INPUT_DIR/dups.fasta"
ORCHID_FASTA="$INPUT_DIR/ls_orchid.fasta"
LUPINE_FASTA="$INPUT_DIR/lupine.nu"

mkdir -p "$OUTPUT_DIR"

python3 - <<'PY'
import json
from collections import defaultdict
from pathlib import Path

from Bio import SeqIO
from skbio import DNA
from skbio.sequence.distance import kmer_distance

OUTPUT_FILE = "/root/harbor_workspaces/task_T016_run2/output/alpha_best_kmer_match.json"
OUTPUT_DIR = "/root/harbor_workspaces/task_T016_run2/output"
INPUT_FILES = [
    "/root/harbor_workspaces/task_T016_run2/input/dups.fasta",
    "/root/harbor_workspaces/task_T016_run2/input/ls_orchid.fasta",
    "/root/harbor_workspaces/task_T016_run2/input/lupine.nu",
]

dups_fp, orchid_fp, lupine_fp = INPUT_FILES

def read_fasta(path):
    out = []
    for rec in SeqIO.parse(path, "fasta"):
        rid = rec.id  # identifier up to first whitespace
        seq = str(rec.seq).upper()
        out.append((rid, seq))
    return out

# Step 2: collapse dups.fasta by ID; verify only duplicated ID is alpha and sequences identical.
dups = read_fasta(dups_fp)
by_id = defaultdict(list)
for rid, seq in dups:
    by_id[rid].append(seq)

duplicated_ids = sorted([rid for rid, seqs in by_id.items() if len(seqs) > 1])
if duplicated_ids != ["alpha"]:
    raise SystemExit(f"Expected only duplicated ID ['alpha'], got {duplicated_ids}")

alpha_seqs = by_id["alpha"]
if len(set(alpha_seqs)) != 1:
    raise SystemExit("Duplicate 'alpha' sequences are not identical")

query_id = "alpha"
query_seq = alpha_seqs[0]
q = DNA(query_seq)

# Step 3: compute min k-mer distance over k=2,3,4 for each target in orchid + lupine
targets = []
for rid, seq in read_fasta(orchid_fp):
    targets.append((rid, seq, "ls_orchid.fasta"))

lup = read_fasta(lupine_fp)
if len(lup) != 1:
    raise SystemExit(f"Expected single record in lupine.nu, got {len(lup)}")
targets.append((lup[0][0], lup[0][1], "lupine.nu"))

def all_k_distances(tseq: str):
    t = DNA(tseq)
    d2 = float(kmer_distance(q, t, k=2))
    d3 = float(kmer_distance(q, t, k=3))
    d4 = float(kmer_distance(q, t, k=4))
    return {2: d2, 3: d3, 4: d4}

best_tid = None
best_score = None
best_src = None
best_tseq = None
best_d = None

for tid, tseq, src in targets:
    d = all_k_distances(tseq)
    score = min(d.values())
    if best_score is None or score < best_score or (score == best_score and tid < best_tid):
        best_score = score
        best_tid = tid
        best_src = src
        best_tseq = tseq
        best_d = d

# best_k/best_distance correspond to the minimum among all_k_distances; break ties by smallest k
best_k = min(best_d.keys(), key=lambda k: (best_d[k], k))
best_distance = float(best_d[best_k])

out = {
    "query_id": query_id,
    "query_sequence": query_seq,
    "query_source_file": "dups.fasta",
    "target_id": best_tid,
    "target_source_file": best_src,
    "target_length": int(len(best_tseq)),
    "best_k": int(best_k),
    "best_distance": float(best_distance),
    "all_k_distances": {"2": float(best_d[2]), "3": float(best_d[3]), "4": float(best_d[4])},
}

Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
with open(OUTPUT_FILE, "w") as f:
    json.dump(out, f, indent=2)
    f.write("\n")
PY

test -s "$OUTPUT_FILE"

# HARBOR_OUTPUT_FIX_START
if [ -f "/root/harbor_workspaces/task_T016_run2/output/alpha_best_kmer_match.json" ]; then cp -f "/root/harbor_workspaces/task_T016_run2/output/alpha_best_kmer_match.json" "/root/alpha_best_kmer_match.json"; fi
# HARBOR_OUTPUT_FIX_END
