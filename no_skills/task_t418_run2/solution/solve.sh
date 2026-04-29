#!/bin/bash
set -e

# HARBOR_PATH_FIX_START
BASE_FIX="/root/harbor_workspaces/task_T418_run2"
mkdir -p "$BASE_FIX/input" "$BASE_FIX/output"
if [ ! -e "$BASE_FIX/input/ftp.pcap" ] && [ -e "/root/ftp.pcap" ]; then cp -f "/root/ftp.pcap" "$BASE_FIX/input/ftp.pcap"; fi
if [ ! -e "$BASE_FIX/input/bruteforce.pcap" ] && [ -e "/root/bruteforce.pcap" ]; then cp -f "/root/bruteforce.pcap" "$BASE_FIX/input/bruteforce.pcap"; fi
if [ ! -e "$BASE_FIX/input/samplecaptures" ] && [ -e "/root/samplecaptures" ]; then cp -f "/root/samplecaptures" "$BASE_FIX/input/samplecaptures"; fi
# HARBOR_PATH_FIX_END

#!/usr/bin/env bash
set -euo pipefail

BASE="/root/harbor_workspaces/task_T418_run2"
IN="$BASE/input"
OUT="$BASE/output"

mkdir -p "$OUT"

# Create process_ftp.py (self-contained; derives everything from the three input files)
cat > "$BASE/process_ftp.py" <<'PY'
import re
from collections import Counter
from html.parser import HTMLParser

from scapy.all import rdpcap, TCP, Raw  # scapy is available in the environment
from openpyxl import Workbook

IN_FTP = "/root/harbor_workspaces/task_T418_run2/input/ftp.pcap"
IN_BRUTE = "/root/harbor_workspaces/task_T418_run2/input/bruteforce.pcap"
IN_HTML = "/root/harbor_workspaces/task_T418_run2/input/samplecaptures"
OUT_XLSX = "/root/harbor_workspaces/task_T418_run2/output/ftp_command_comparison.xlsx"

VERB_RE = re.compile(r"^([A-Za-z]{3,10})\b")

class TitleParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self._in_title = False
        self._chunks = []
    def handle_starttag(self, tag, attrs):
        if tag.lower() == "title":
            self._in_title = True
    def handle_endtag(self, tag):
        if tag.lower() == "title":
            self._in_title = False
    def handle_data(self, data):
        if self._in_title:
            self._chunks.append(data)

def extract_title(html_path: str) -> str:
    with open(html_path, "rb") as f:
        raw = f.read()
    # best-effort decode
    for enc in ("utf-8", "latin-1"):
        try:
            text = raw.decode(enc)
            break
        except Exception:
            continue
    else:
        text = raw.decode("utf-8", errors="replace")
    p = TitleParser()
    p.feed(text)
    title = "".join(p._chunks).strip()
    return title

def extract_client_ftp_verbs_from_pcap(pcap_path: str):
    """
    Extract ASCII FTP command verbs sent client->server on TCP port 21.
    Ignore server responses and ignore non-21 ports.
    Deterministic: count each command line found in client payloads.
    """
    pkts = rdpcap(pcap_path)
    counts = Counter()
    total = 0

    for pkt in pkts:
        if not pkt.haslayer(TCP):
            continue
        tcp = pkt[TCP]
        if tcp.dport != 21:
            continue  # only client->server control channel
        if not pkt.haslayer(Raw):
            continue
        payload = bytes(pkt[Raw].load)
        if not payload:
            continue

        # Decode as ASCII-ish; FTP commands are ASCII. Replace errors deterministically.
        text = payload.decode("ascii", errors="ignore")
        if not text:
            continue

        # Split into lines; count each line that looks like a command verb.
        # Some packets may contain multiple commands.
        for line in re.split(r"\r\n|\n|\r", text):
            line = line.strip()
            if not line:
                continue
            m = VERB_RE.match(line)
            if not m:
                continue
            verb = m.group(1).upper()
            counts[verb] += 1
            total += 1

    return counts, total

def sorted_table(counter: Counter):
    # Sort by count desc, then verb asc
    return sorted(counter.items(), key=lambda kv: (-kv[1], kv[0]))

def top_verb(counter: Counter):
    if not counter:
        return ""
    # highest count; tie-break alphabetical
    max_count = max(counter.values())
    candidates = sorted([v for v, c in counter.items() if c == max_count])
    return candidates[0]

def write_freq_sheet(ws, counter: Counter):
    ws["A1"] = "verb"
    ws["B1"] = "count"
    row = 2
    for verb, cnt in sorted_table(counter):
        ws.cell(row=row, column=1, value=verb)
        ws.cell(row=row, column=2, value=cnt)
        row += 1

def main():
    title = extract_title(IN_HTML)

    ftp_counts, ftp_total = extract_client_ftp_verbs_from_pcap(IN_FTP)
    brute_counts, brute_total = extract_client_ftp_verbs_from_pcap(IN_BRUTE)

    wb = Workbook()
    ws_sum = wb.active
    ws_sum.title = "Summary"

    # Summary header
    ws_sum["A1"] = "Reference Page Title"
    ws_sum["B1"] = title

    ws_sum["A3"] = "pcap"
    ws_sum["B3"] = "total_commands"
    ws_sum["C3"] = "unique_verbs"
    ws_sum["D3"] = "top_verb"

    # Row 4: ftp.pcap
    ws_sum["A4"] = "ftp.pcap"
    ws_sum["B4"] = int(ftp_total)
    ws_sum["C4"] = int(len(ftp_counts))
    ws_sum["D4"] = top_verb(ftp_counts)

    # Row 5: bruteforce.pcap
    ws_sum["A5"] = "bruteforce.pcap"
    ws_sum["B5"] = int(brute_total)
    ws_sum["C5"] = int(len(brute_counts))
    ws_sum["D5"] = top_verb(brute_counts)

    # Frequency sheets
    ws_ftp = wb.create_sheet("ftp_pcap")
    write_freq_sheet(ws_ftp, ftp_counts)

    ws_brute = wb.create_sheet("bruteforce_pcap")
    write_freq_sheet(ws_brute, brute_counts)

    wb.save(OUT_XLSX)

if __name__ == "__main__":
    main()
PY

# Create expectation_tests.py (self-contained; independently derives expected values from inputs)
cat > "$BASE/expectation_tests.py" <<'PY'
import os
import re
from collections import Counter
from html.parser import HTMLParser

import pytest
from scapy.all import rdpcap, TCP, Raw
from openpyxl import load_workbook

BASE = "/root/harbor_workspaces/task_T418_run2"
IN_FTP = f"{BASE}/input/ftp.pcap"
IN_BRUTE = f"{BASE}/input/bruteforce.pcap"
IN_HTML = f"{BASE}/input/samplecaptures"
OUT_XLSX = f"{BASE}/output/ftp_command_comparison.xlsx"

VERB_RE = re.compile(r"^([A-Za-z]{3,10})\b")

class TitleParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self._in_title = False
        self._chunks = []
    def handle_starttag(self, tag, attrs):
        if tag.lower() == "title":
            self._in_title = True
    def handle_endtag(self, tag):
        if tag.lower() == "title":
            self._in_title = False
    def handle_data(self, data):
        if self._in_title:
            self._chunks.append(data)

def extract_title(html_path: str) -> str:
    with open(html_path, "rb") as f:
        raw = f.read()
    for enc in ("utf-8", "latin-1"):
        try:
            text = raw.decode(enc)
            break
        except Exception:
            continue
    else:
        text = raw.decode("utf-8", errors="replace")
    p = TitleParser()
    p.feed(text)
    return "".join(p._chunks).strip()

def extract_counts(pcap_path: str):
    pkts = rdpcap(pcap_path)
    counts = Counter()
    total = 0
    for pkt in pkts:
        if not pkt.haslayer(TCP):
            continue
        tcp = pkt[TCP]
        if tcp.dport != 21:
            continue
        if not pkt.haslayer(Raw):
            continue
        payload = bytes(pkt[Raw].load)
        if not payload:
            continue
        text = payload.decode("ascii", errors="ignore")
        if not text:
            continue
        for line in re.split(r"\r\n|\n|\r", text):
            line = line.strip()
            if not line:
                continue
            m = VERB_RE.match(line)
            if not m:
                continue
            verb = m.group(1).upper()
            counts[verb] += 1
            total += 1
    return counts, total

def sorted_table(counter: Counter):
    return sorted(counter.items(), key=lambda kv: (-kv[1], kv[0]))

def top_verb(counter: Counter):
    if not counter:
        return ""
    max_count = max(counter.values())
    return sorted([v for v, c in counter.items() if c == max_count])[0]

@pytest.mark.order(1)
def test_output_exists():
    assert os.path.exists(OUT_XLSX), f"Missing output Excel: {OUT_XLSX}"

@pytest.mark.order(2)
def test_workbook_structure_and_reference_title():
    wb = load_workbook(OUT_XLSX)
    assert wb.sheetnames == ["Summary", "ftp_pcap", "bruteforce_pcap"]
    ws = wb["Summary"]
    assert ws["A1"].value == "Reference Page Title"
    assert ws["B1"].value == extract_title(IN_HTML)

@pytest.mark.order(3)
def test_summary_values_match_pcap_derivation():
    ftp_counts, ftp_total = extract_counts(IN_FTP)
    brute_counts, brute_total = extract_counts(IN_BRUTE)

    wb = load_workbook(OUT_XLSX)
    ws = wb["Summary"]

    # Header row
    assert [ws["A3"].value, ws["B3"].value, ws["C3"].value, ws["D3"].value] == [
        "pcap", "total_commands", "unique_verbs", "top_verb"
    ]

    # ftp.pcap row
    assert ws["A4"].value == "ftp.pcap"
    assert int(ws["B4"].value) == int(ftp_total)
    assert int(ws["C4"].value) == int(len(ftp_counts))
    assert ws["D4"].value == top_verb(ftp_counts)

    # bruteforce.pcap row
    assert ws["A5"].value == "bruteforce.pcap"
    assert int(ws["B5"].value) == int(brute_total)
    assert int(ws["C5"].value) == int(len(brute_counts))
    assert ws["D5"].value == top_verb(brute_counts)

@pytest.mark.order(4)
def test_frequency_sheets_match_sorted_tables():
    ftp_counts, _ = extract_counts(IN_FTP)
    brute_counts, _ = extract_counts(IN_BRUTE)

    wb = load_workbook(OUT_XLSX)
    ws_ftp = wb["ftp_pcap"]
    ws_brute = wb["bruteforce_pcap"]

    # Headers
    assert ws_ftp["A1"].value == "verb"
    assert ws_ftp["B1"].value == "count"
    assert ws_brute["A1"].value == "verb"
    assert ws_brute["B1"].value == "count"

    # Read tables
    def read_table(ws):
        rows = []
        r = 2
        while True:
            v = ws.cell(row=r, column=1).value
            c = ws.cell(row=r, column=2).value
            if v is None and c is None:
                break
            rows.append((str(v), int(c)))
            r += 1
        return rows

    got_ftp = read_table(ws_ftp)
    got_brute = read_table(ws_brute)

    exp_ftp = sorted_table(ftp_counts)
    exp_brute = sorted_table(brute_counts)

    assert got_ftp == exp_ftp
    assert got_brute == exp_brute
PY

# Ensure dependencies exist (quietly). scapy is assumed available; openpyxl may not be.
python3 - <<'PY'
import sys, subprocess
def ensure(pkg):
    try:
        __import__(pkg)
    except Exception:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", pkg])
ensure("openpyxl")
PY

# Generate the required Excel output
python3 "$BASE/process_ftp.py"

# Sanity: ensure file exists at exact path
test -f "$OUT/ftp_command_comparison.xlsx"

# HARBOR_OUTPUT_FIX_START
if [ -f "/root/harbor_workspaces/task_T418_run2/output/ftp_command_comparison.xlsx" ]; then cp -f "/root/harbor_workspaces/task_T418_run2/output/ftp_command_comparison.xlsx" "/root/ftp_command_comparison.xlsx"; fi
# HARBOR_OUTPUT_FIX_END
