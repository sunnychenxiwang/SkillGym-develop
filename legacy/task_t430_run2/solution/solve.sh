#!/bin/bash
set -e

# HARBOR_PATH_FIX_START
BASE_FIX="/root/harbor_workspaces/task_T430_run2"
mkdir -p "$BASE_FIX/input" "$BASE_FIX/output"
if [ ! -e "$BASE_FIX/input/case57.m" ] && [ -e "/root/case57.m" ]; then cp -f "/root/case57.m" "$BASE_FIX/input/case57.m"; fi
if [ ! -e "$BASE_FIX/input/case118.m" ] && [ -e "/root/case118.m" ]; then cp -f "/root/case118.m" "$BASE_FIX/input/case118.m"; fi
if [ ! -e "$BASE_FIX/input/pglib_opf_case118_ieee.m" ] && [ -e "/root/pglib_opf_case118_ieee.m" ]; then cp -f "/root/pglib_opf_case118_ieee.m" "$BASE_FIX/input/pglib_opf_case118_ieee.m"; fi
# HARBOR_PATH_FIX_END

#!/usr/bin/env bash
set -euo pipefail

ROOT="/root/harbor_workspaces/task_T430_run2"
IN="$ROOT/input"
OUT="$ROOT/output"

mkdir -p "$OUT"

# Create compute_signatures.py (self-contained; parses MATPOWER .m files and computes signatures/distances)
cat > "$ROOT/compute_signatures.py" <<'PY'
#!/usr/bin/env python3
import json
import os
import re
from collections import defaultdict

ROOT = "/root/harbor_workspaces/task_T430_run2"
IN_DIR = os.path.join(ROOT, "input")
OUT_PATH = os.path.join(ROOT, "output", "degree_signature_result.json")

FILES = ["case57.m", "case118.m", "pglib_opf_case118_ieee.m"]

def strip_comments(s: str) -> str:
    # Remove MATLAB comments (%) to end of line
    return re.sub(r"%.*?$", "", s, flags=re.M)

def extract_block(text: str, name: str) -> str:
    # Extract "mpc.<name> = [ ... ];" block content inside brackets
    # Allow whitespace/newlines; non-greedy until first matching "];"
    m = re.search(rf"\bmpc\.{re.escape(name)}\s*=\s*\[(.*?)\]\s*;", text, flags=re.S)
    if not m:
        raise ValueError(f"Could not find block mpc.{name} = [ ... ];")
    return m.group(1)

def parse_matrix(block: str):
    # Convert MATLAB matrix text into list of rows of floats.
    # Rows separated by ';' or newlines; columns by whitespace/commas.
    block = strip_comments(block)
    rows = []
    for raw_row in re.split(r";|\n", block):
        raw_row = raw_row.strip()
        if not raw_row:
            continue
        raw_row = raw_row.replace(",", " ")
        parts = [p for p in raw_row.split() if p]
        if not parts:
            continue
        try:
            row = [float(p) for p in parts]
        except ValueError as e:
            raise ValueError(f"Failed parsing row: {raw_row}") from e
        rows.append(row)
    return rows

def parse_baseMVA(text: str) -> float:
    text_nc = strip_comments(text)
    m = re.search(r"\bmpc\.baseMVA\s*=\s*([0-9.+-eE]+)\s*;", text_nc)
    if not m:
        raise ValueError("Could not find mpc.baseMVA")
    return float(m.group(1))

def compute_signature(path: str):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    baseMVA = parse_baseMVA(text)  # required to read, though not used further
    bus_block = extract_block(text, "bus")
    branch_block = extract_block(text, "branch")

    bus = parse_matrix(bus_block)
    branch = parse_matrix(branch_block)

    # Bus numbers may be non-contiguous; use actual IDs from first column
    bus_ids = [int(round(r[0])) for r in bus]
    degrees = {bid: 0 for bid in bus_ids}

    in_service = 0
    for r in branch:
        if len(r) < 11:
            raise ValueError("Branch row has fewer than 11 columns; cannot read status")
        fbus = int(round(r[0]))
        tbus = int(round(r[1]))
        status = int(round(r[10]))
        if status != 1:
            continue
        in_service += 1
        # undirected multigraph: count multiplicity
        if fbus not in degrees:
            degrees[fbus] = 0
        if tbus not in degrees:
            degrees[tbus] = 0
        degrees[fbus] += 1
        degrees[tbus] += 1

    hist = defaultdict(int)
    for bid in bus_ids:
        hist[degrees.get(bid, 0)] += 1

    # JSON requires string keys
    hist_json = {str(k): int(v) for k, v in sorted(hist.items(), key=lambda kv: kv[0])}

    return {
        "n_buses": int(len(bus_ids)),
        "n_in_service_branches": int(in_service),
        "degree_histogram": hist_json,
    }

def l1_distance(histA, histB) -> int:
    # histA/histB are dict with string keys
    keys = set(histA.keys()) | set(histB.keys())
    dist = 0
    for k in keys:
        dist += abs(int(histA.get(k, 0)) - int(histB.get(k, 0)))
    return int(dist)

def main():
    case_signatures = {}
    for fn in FILES:
        case_signatures[fn] = compute_signature(os.path.join(IN_DIR, fn))

    pairs = [
        ("case57.m", "case118.m"),
        ("case57.m", "pglib_opf_case118_ieee.m"),
        ("case118.m", "pglib_opf_case118_ieee.m"),
    ]
    pairwise = {}
    for a, b in pairs:
        key = f"{a}__{b}"
        pairwise[key] = l1_distance(case_signatures[a]["degree_histogram"],
                                    case_signatures[b]["degree_histogram"])

    # Select smallest distance; break ties by lexicographic order of pair key
    best_key = sorted(pairwise.items(), key=lambda kv: (kv[1], kv[0]))[0][0]
    a, b = best_key.split("__")
    most_similar = {"files": [a, b], "distance": int(pairwise[best_key])}

    out = {
        "case_signatures": case_signatures,
        "pairwise_L1_distances": pairwise,
        "most_similar_pair": most_similar,
    }

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, sort_keys=True)
        f.write("\n")

if __name__ == "__main__":
    main()
PY
chmod +x "$ROOT/compute_signatures.py"

# Create expectation_tests.py (self-contained; validates schema + invariants; does NOT drive computation)
cat > "$ROOT/expectation_tests.py" <<'PY'
#!/usr/bin/env python3
import json
import os
import sys

ROOT = "/root/harbor_workspaces/task_T430_run2"
OUT_PATH = os.path.join(ROOT, "output", "degree_signature_result.json")

FILES = ["case57.m", "case118.m", "pglib_opf_case118_ieee.m"]
PAIR_KEYS = [
    "case57.m__case118.m",
    "case57.m__pglib_opf_case118_ieee.m",
    "case118.m__pglib_opf_case118_ieee.m",
]

def die(msg):
    raise AssertionError(msg)

def load():
    if not os.path.exists(OUT_PATH):
        die(f"Missing output JSON: {OUT_PATH}")
    with open(OUT_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def as_int(x, ctx="value"):
    if isinstance(x, bool):
        die(f"{ctx} must be int, got bool")
    if isinstance(x, int):
        return x
    die(f"{ctx} must be int, got {type(x).__name__}")

def main():
    data = load()

    if not isinstance(data, dict):
        die("Top-level JSON must be an object")

    for k in ["case_signatures", "pairwise_L1_distances", "most_similar_pair"]:
        if k not in data:
            die(f"Missing top-level key: {k}")

    cs = data["case_signatures"]
    if not isinstance(cs, dict):
        die("case_signatures must be an object")
    for fn in FILES:
        if fn not in cs:
            die(f"case_signatures missing {fn}")
        entry = cs[fn]
        if not isinstance(entry, dict):
            die(f"case_signatures[{fn}] must be an object")
        for k in ["n_buses", "n_in_service_branches", "degree_histogram"]:
            if k not in entry:
                die(f"case_signatures[{fn}] missing {k}")
        n_buses = as_int(entry["n_buses"], f"{fn}.n_buses")
        n_br = as_int(entry["n_in_service_branches"], f"{fn}.n_in_service_branches")
        if n_buses <= 0:
            die(f"{fn}: n_buses must be > 0")
        if n_br < 0:
            die(f"{fn}: n_in_service_branches must be >= 0")

        hist = entry["degree_histogram"]
        if not isinstance(hist, dict) or not hist:
            die(f"{fn}: degree_histogram must be a non-empty object")

        # Keys must be strings of non-negative ints; values must be non-negative ints
        sum_buses = 0
        sum_deg = 0
        for k, v in hist.items():
            if not isinstance(k, str) or not k.isdigit():
                die(f"{fn}: histogram key must be digit string, got {k!r}")
            deg = int(k)
            cnt = as_int(v, f"{fn}.degree_histogram[{k}]")
            if cnt < 0:
                die(f"{fn}: histogram count must be >= 0")
            sum_buses += cnt
            sum_deg += deg * cnt

        if sum_buses != n_buses:
            die(f"{fn}: histogram counts sum to {sum_buses}, expected n_buses {n_buses}")

        # Degree sum invariant for undirected multigraph: sum(deg) = 2 * |E|
        if sum_deg != 2 * n_br:
            die(f"{fn}: sum(degree)={sum_deg} != 2*n_in_service_branches={2*n_br}")

    pd = data["pairwise_L1_distances"]
    if not isinstance(pd, dict):
        die("pairwise_L1_distances must be an object")
    for pk in PAIR_KEYS:
        if pk not in pd:
            die(f"pairwise_L1_distances missing {pk}")
        d = as_int(pd[pk], f"pairwise_L1_distances[{pk}]")
        if d < 0:
            die(f"{pk}: distance must be >= 0")

    msp = data["most_similar_pair"]
    if not isinstance(msp, dict):
        die("most_similar_pair must be an object")
    if "files" not in msp or "distance" not in msp:
        die("most_similar_pair must contain files and distance")
    files = msp["files"]
    if not (isinstance(files, list) and len(files) == 2 and all(isinstance(x, str) for x in files)):
        die("most_similar_pair.files must be a list of two strings")
    dist = as_int(msp["distance"], "most_similar_pair.distance")
    if dist < 0:
        die("most_similar_pair.distance must be >= 0")

    # Ensure chosen pair is minimal with lexicographic tie-break on pair key
    best_key = sorted(((k, as_int(v, f"pairwise_L1_distances[{k}]")) for k, v in pd.items()),
                      key=lambda kv: (kv[1], kv[0]))[0][0]
    expected_files = best_key.split("__")
    if files != expected_files:
        die(f"most_similar_pair.files {files} != expected {expected_files}")
    if dist != pd[best_key]:
        die(f"most_similar_pair.distance {dist} != expected {pd[best_key]}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"TEST FAILURE: {e}", file=sys.stderr)
        sys.exit(1)
    print("All expectation tests passed.")
PY
chmod +x "$ROOT/expectation_tests.py"

# Run computation to produce the required JSON output
python3 "$ROOT/compute_signatures.py"

# Optional sanity: ensure JSON exists
test -s "$OUT/degree_signature_result.json"

# HARBOR_OUTPUT_FIX_START
if [ -f "/root/harbor_workspaces/task_T430_run2/output/degree_signature_result.json" ]; then cp -f "/root/harbor_workspaces/task_T430_run2/output/degree_signature_result.json" "/root/degree_signature_result.json"; fi
# HARBOR_OUTPUT_FIX_END
