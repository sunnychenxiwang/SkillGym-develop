#!/bin/bash

set -euo pipefail

copy_if_missing() {
  local target="$1"
  shift
  if [ -e "${target}" ]; then
    return 0
  fi
  for source in "$@"; do
    if [ -e "${source}" ]; then
      cp -f "${source}" "${target}"
      return 0
    fi
  done
}

mkdir -p /root/input

copy_if_missing "/root/ASD-Cyber-Threat-Report-2024.pdf" \
  "/root/input/ASD-Cyber-Threat-Report-2024.pdf" \
  "/root/harbor_workspaces/task_T153_run1/input/ASD-Cyber-Threat-Report-2024.pdf"

copy_if_missing "/root/RedCanary-Threat-Detection-Report-2024.pdf" \
  "/root/input/RedCanary-Threat-Detection-Report-2024.pdf" \
  "/root/harbor_workspaces/task_T153_run1/input/RedCanary-Threat-Detection-Report-2024.pdf"

copy_if_missing "/root/Secureworks-State-of-the-Threat-Report-2024.pdf" \
  "/root/input/Secureworks-State-of-the-Threat-Report-2024.pdf" \
  "/root/harbor_workspaces/task_T153_run1/input/Secureworks-State-of-the-Threat-Report-2024.pdf"

python3 - <<'PY'
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

OUTPUT_FILE = Path("/root/most_common_attack_technique.json")
PDF_FILES = [
    Path("/root/ASD-Cyber-Threat-Report-2024.pdf"),
    Path("/root/RedCanary-Threat-Detection-Report-2024.pdf"),
    Path("/root/Secureworks-State-of-the-Threat-Report-2024.pdf"),
]

TECHNIQUE_RE = re.compile(r"\bT\d{4}(?:\.\d{3})?\b", re.IGNORECASE)


def extract_pdf_text(pdf_path: Path) -> str:
    text_parts = []

    try:
        from pypdf import PdfReader  # type: ignore

        reader = PdfReader(str(pdf_path))
        for page in reader.pages:
            text_parts.append(page.extract_text() or "")
        return "\n".join(text_parts)
    except Exception:
        pass

    try:
        from PyPDF2 import PdfReader  # type: ignore

        reader = PdfReader(str(pdf_path))
        for page in reader.pages:
            text_parts.append(page.extract_text() or "")
        return "\n".join(text_parts)
    except Exception as exc:
        raise RuntimeError(f"Failed to extract text from PDF {pdf_path}: {exc}") from exc


per_doc_counts = {}
doc_frequency = defaultdict(int)
total_occurrences = defaultdict(int)

for pdf_path in PDF_FILES:
    if not pdf_path.exists():
        raise FileNotFoundError(f"Input PDF not found: {pdf_path}")
    if pdf_path.stat().st_size == 0:
        raise ValueError(f"Input PDF is empty: {pdf_path}")

    text = extract_pdf_text(pdf_path)
    matches = [m.upper() for m in TECHNIQUE_RE.findall(text)]
    counts = Counter(matches)
    per_doc_counts[pdf_path.name] = counts

    for technique_id, count in counts.items():
        if count > 0:
            doc_frequency[technique_id] += 1
            total_occurrences[technique_id] += count

if not doc_frequency:
    raise ValueError("No ATT&CK technique IDs were found in the input PDFs")

winner = min(
    doc_frequency.keys(),
    key=lambda tid: (
        -doc_frequency[tid],
        -total_occurrences[tid],
        tid,
    ),
)

per_document = {
    pdf_path.name: (per_doc_counts[pdf_path.name].get(winner, 0) > 0)
    for pdf_path in PDF_FILES
}

result = {
    "technique_id": winner,
    "documents_containing": doc_frequency[winner],
    "per_document": per_document,
}

OUTPUT_FILE.write_text(json.dumps(result, indent=2), encoding="utf-8")
PY
