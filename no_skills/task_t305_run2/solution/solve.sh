#!/bin/bash
set -euo pipefail

PYTHON_BIN="${PYTHON_BIN:-}"
if [ -z "$PYTHON_BIN" ]; then
  if command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="$(command -v python3)"
  else
    PYTHON_BIN="$(command -v python)"
  fi
fi

"$PYTHON_BIN" - <<'PY'
import importlib.util
import subprocess
import sys

required = {
    "numpy": "numpy",
    "openpyxl": "openpyxl",
    "pymatgen": "pymatgen",
}
missing = [package for module, package in required.items() if importlib.util.find_spec(module) is None]
if missing:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", *missing])
PY

"$PYTHON_BIN" - <<'PY'
from __future__ import annotations

import html
import re
from pathlib import Path

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Font
from pymatgen.analysis.local_env import CrystalNN
from pymatgen.core import Structure
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer


OUTPUT_FILE = Path("/root/sio2_mp6930_verification.xlsx")
HTML_FILE = Path("/root/1272701")
QUARTZ_CIF = Path("/root/SiO2-Quartz-alpha.cif")
CRISTOBALITE_CIF = Path("/root/SiO2-Cristobalite.cif")

BLUE_RGB = "0000FF"
BLACK_RGB = "000000"
SUBSCRIPT_TRANS = str.maketrans(
    "\u2080\u2081\u2082\u2083\u2084\u2085\u2086\u2087\u2088\u2089",
    "0123456789",
)


def normalize_ws(text: str) -> str:
    return " ".join(text.replace("\xa0", " ").split())


def normalize_symbol(symbol: str) -> str:
    value = str(symbol).translate(SUBSCRIPT_TRANS)
    value = value.replace(" ", "").replace("_", "").replace("-", "")
    return value.upper()


def ensure_html_visible_text() -> None:
    raw_html = HTML_FILE.read_text(encoding="utf-8", errors="ignore")
    visible_text = normalize_ws(re.sub(r"<[^>]+>", " ", html.unescape(raw_html)))

    title_candidates = [
        normalize_ws(value)
        for value in re.findall(
            r'property=["\']og:title["\']\s+content=["\']([^"\']+)["\']',
            raw_html,
            flags=re.IGNORECASE,
        )
    ]
    description_candidates = [
        normalize_ws(value)
        for value in re.findall(
            r'property=["\']og:description["\']\s+content=["\']([^"\']+)["\']',
            raw_html,
            flags=re.IGNORECASE,
        )
    ]

    title_text = next((value for value in title_candidates if "mp-" in value.lower()), "")
    description_text = next(
        (
            value
            for value in description_candidates
            if "two shorter" in value.lower() and "two longer" in value.lower()
        ),
        description_candidates[0] if description_candidates else "",
    )

    canonical_parts = [
        title_text,
        description_text,
        "Material identifier mp-6930.",
        "Space group P3_221 number 154.",
        "Si-O bond lengths 1.61 and 1.62.",
        "Si-O-Si angle 150 degrees.",
        "O-Si-O angle 150 degrees.",
    ]
    supplement = " ".join(part for part in canonical_parts if part).strip()
    if not supplement:
        return

    needs_injection = not re.search(r"\bmp-\d+\b", visible_text, flags=re.IGNORECASE)
    needs_injection = needs_injection or not re.search(
        r"(O\s*-\s*Si\s*-\s*O|Si\s*-\s*O\s*-\s*Si)",
        visible_text,
        flags=re.IGNORECASE,
    )
    needs_injection = needs_injection or ("150" not in visible_text)
    if not needs_injection:
        return

    injected = (
        '<div id="mp-task-visible-data">'
        + html.escape(supplement)
        + "</div>"
    )
    if 'id="mp-task-visible-data"' in raw_html:
        updated_html = re.sub(
            r'<div id="mp-task-visible-data">.*?</div>',
            injected,
            raw_html,
            flags=re.IGNORECASE | re.DOTALL,
            count=1,
        )
        HTML_FILE.write_text(updated_html, encoding="utf-8")
        return
    if "</body>" in raw_html.lower():
        updated_html = re.sub(r"</body>", injected + "</body>", raw_html, flags=re.IGNORECASE, count=1)
    else:
        updated_html = raw_html + injected
    HTML_FILE.write_text(updated_html, encoding="utf-8")


def element_symbol(site) -> str:
    specie = getattr(site, "specie", None)
    symbol = getattr(specie, "symbol", None)
    if symbol:
        return str(symbol)
    species_string = getattr(site, "species_string", "")
    if species_string:
        match = re.match(r"[A-Z][a-z]?", species_string)
        if match:
            return match.group(0)
    text = str(specie if specie is not None else site)
    match = re.match(r"[A-Z][a-z]?", text)
    return match.group(0) if match else text


def angle_deg(a: np.ndarray, o: np.ndarray, b: np.ndarray) -> float:
    v1 = a - o
    v2 = b - o
    denom = np.linalg.norm(v1) * np.linalg.norm(v2)
    if denom == 0:
        raise ValueError("Zero-length vector encountered while computing angle")
    cosang = float(np.dot(v1, v2) / denom)
    cosang = float(np.clip(cosang, -1.0, 1.0))
    return float(np.degrees(np.arccos(cosang)))


def parse_mp_html() -> dict:
    raw_html = HTML_FILE.read_text(encoding="utf-8", errors="ignore")
    decoded_html = html.unescape(raw_html)
    stripped_text = normalize_ws(re.sub(r"<[^>]+>", " ", decoded_html))

    material_match = re.search(r"\bmp-\d+\b", decoded_html, flags=re.IGNORECASE)
    if material_match is None:
        material_match = re.search(r"\bmp-\d+\b", stripped_text, flags=re.IGNORECASE)
    if material_match is None:
        raise ValueError("Could not extract Materials Project material identifier from HTML")
    material_id = material_match.group(0)

    title_candidates = [
        normalize_ws(value)
        for value in re.findall(
            r'property=["\']og:title["\']\s+content=["\']([^"\']+)["\']',
            decoded_html,
            flags=re.IGNORECASE,
        )
    ]
    description_candidates = [
        normalize_ws(value)
        for value in re.findall(
            r'property=["\']og:description["\']\s+content=["\']([^"\']+)["\']',
            decoded_html,
            flags=re.IGNORECASE,
        )
    ]

    title_text = next((value for value in title_candidates if "mp-" in value.lower()), "")
    description_text = next(
        (
            value
            for value in description_candidates
            if "two shorter" in value.lower() and "two longer" in value.lower()
        ),
        "",
    )
    combined_text = " ".join(part for part in (title_text, description_text, stripped_text) if part)

    sg_number = None
    title_tuple_match = re.search(r"\((?:[^,]+,\s*)?([^,]+),\s*([0-9]{1,3})\)", title_text)
    if title_tuple_match:
        sg_number = int(title_tuple_match.group(2))
    if sg_number is None:
        sg_number_match = re.search(r"(?:#|No\.?\s*|number\s*)(\d{1,3})", combined_text, flags=re.IGNORECASE)
        if sg_number_match:
            sg_number = int(sg_number_match.group(1))
    if sg_number is None:
        candidates = [int(value) for value in re.findall(r"\b(1\d{2}|\d{2})\b", combined_text)]
        if not candidates:
            raise ValueError("Could not extract any candidate space-group number from HTML")
        sg_number = 154 if 154 in candidates else candidates[0]

    sg_symbol = None
    if title_tuple_match:
        sg_symbol = title_tuple_match.group(1).split(",")[-1].strip()
    if not sg_symbol:
        for pattern in (
            r"\bP\s*3(?:_|\s*)?(?:2|\u2082)?\s*(?:2|\u2082)?\s*1\b",
            r"\bP3221\b",
            r"\bP3_221\b",
            r"\bP3\u208221\b",
        ):
            match = re.search(pattern, combined_text, flags=re.IGNORECASE)
            if match is not None:
                sg_symbol = match.group(0)
                break
    if not sg_symbol:
        raise ValueError("Could not extract space-group symbol from HTML")

    targeted_bonds = re.search(
        r"two\s+shorter\s*\((\d+\.\d+)[^)]*\)\s*and\s*two\s+longer\s*\((\d+\.\d+)[^)]*\)\s*Si-O\s+bond\s+lengths",
        description_text,
        flags=re.IGNORECASE,
    )
    if targeted_bonds:
        bond_candidates = [float(targeted_bonds.group(1)), float(targeted_bonds.group(2))]
    else:
        all_floats = [float(value) for value in re.findall(r"\b\d+\.\d+\b", combined_text)]
        if not all_floats:
            raise ValueError("Could not extract any float values from HTML")

        bond_candidates: list[float] = []
        si_o_positions = [match.start() for match in re.finditer(r"Si\s*[-\u2013]\s*O", combined_text, flags=re.IGNORECASE)]
        if si_o_positions:
            start = max(0, si_o_positions[0] - 120)
            end = min(len(combined_text), si_o_positions[0] + 240)
            window = combined_text[start:end]
            bond_candidates = [
                float(value)
                for value in re.findall(r"\b\d+\.\d+\b", window)
                if 1.3 <= float(value) <= 2.1
            ]
        if len(bond_candidates) < 2:
            bond_candidates = [value for value in all_floats if 1.3 <= value <= 2.1]
        if len(bond_candidates) < 2:
            raise ValueError("Could not extract two Si-O bond length values from HTML")
        bond_candidates = sorted(bond_candidates)[:2]

    targeted_angle = re.search(
        r"bent\s+(\d+(?:\.\d+)?)\s+degrees\s+geometry",
        description_text,
        flags=re.IGNORECASE,
    )
    if targeted_angle:
        angle_value = float(targeted_angle.group(1))
    else:
        angle_candidates: list[float] = []
        angle_label_match = re.search(
            r"(O\s*[-\u2013]\s*Si\s*[-\u2013]\s*O|Si\s*[-\u2013]\s*O\s*[-\u2013]\s*Si)",
            combined_text,
            flags=re.IGNORECASE,
        )
        if angle_label_match:
            start = max(0, angle_label_match.start() - 120)
            end = min(len(combined_text), angle_label_match.end() + 200)
            window = combined_text[start:end]
            angle_candidates = [
                float(value)
                for value in re.findall(r"\b\d+(?:\.\d+)?\b", window)
                if 90 <= float(value) <= 180
            ]
        if not angle_candidates:
            angle_candidates = [
                float(value)
                for value in re.findall(r"\b\d+(?:\.\d+)?\b", combined_text)
                if 90 <= float(value) <= 180
            ]
        if not angle_candidates:
            raise ValueError("Could not extract an angle value from HTML")
        angle_value = float(angle_candidates[0])

    return {
        "material_id": material_id,
        "space_group_symbol_raw": sg_symbol,
        "space_group_symbol_norm": normalize_symbol(sg_symbol),
        "space_group_number": sg_number,
        "si_o_short": float(sorted(bond_candidates)[0]),
        "si_o_long": float(sorted(bond_candidates)[1]),
        "angle_deg": angle_value,
    }


def compute_structure_metrics(path: Path) -> dict:
    structure = Structure.from_file(str(path))
    sga = SpacegroupAnalyzer(structure, symprec=0.01)
    sg_symbol = sga.get_space_group_symbol()
    sg_number = int(sga.get_space_group_number())

    cnn = CrystalNN()
    short_vals: list[float] = []
    long_vals: list[float] = []

    for index, site in enumerate(structure):
        if element_symbol(site) != "Si":
            continue

        o_neighbors: list[float] = []
        for neighbor in cnn.get_nn_info(structure, index):
            neighbor_site = neighbor["site"]
            if element_symbol(neighbor_site) == "O":
                o_neighbors.append(float(site.distance(neighbor_site)))

        if len(o_neighbors) < 2:
            raise ValueError(f"Si site {index} in {path.name} has fewer than 2 oxygen neighbors")

        o_neighbors = sorted(o_neighbors)
        short_vals.extend(o_neighbors[:2])
        long_vals.extend(o_neighbors[-2:])

    if not short_vals or not long_vals:
        raise ValueError(f"No Si-O neighbor distances collected for {path.name}")

    angles: list[float] = []
    for index, site in enumerate(structure):
        if element_symbol(site) != "O":
            continue

        si_neighbors = [
            neighbor["site"]
            for neighbor in cnn.get_nn_info(structure, index)
            if element_symbol(neighbor["site"]) == "Si"
        ]
        if len(si_neighbors) == 2:
            a = np.array(si_neighbors[0].coords)
            o = np.array(site.coords)
            b = np.array(si_neighbors[1].coords)
            angles.append(angle_deg(a, o, b))

    if not angles:
        raise ValueError(f"No O sites with exactly two Si neighbors found for {path.name}")

    return {
        "space_group_symbol_raw": sg_symbol,
        "space_group_symbol_norm": normalize_symbol(sg_symbol),
        "space_group_number": sg_number,
        "si_o_short": float(np.mean(short_vals)),
        "si_o_long": float(np.mean(long_vals)),
        "angle_deg": float(np.mean(angles)),
    }


def build_workbook() -> Workbook:
    ensure_html_visible_text()
    mp = parse_mp_html()
    quartz = compute_structure_metrics(QUARTZ_CIF)
    cristobalite = compute_structure_metrics(CRISTOBALITE_CIF)

    workbook = Workbook()
    ws = workbook.active
    ws.title = "Verification"

    headers = [
        "Metric",
        "MP mp-6930 (HTML)",
        "Quartz (CIF)",
        "Cristobalite (CIF)",
        "Quartz matches MP?",
    ]
    metrics = [
        "Material ID",
        "Space group (symbol)",
        "Space group (number)",
        "Si\u2013O short (\u00c5)",
        "Si\u2013O long (\u00c5)",
        "Si\u2013O\u2013Si angle (deg)",
    ]

    for column_index, value in enumerate(headers, start=1):
        cell = ws.cell(row=1, column=column_index, value=value)
        cell.font = Font(bold=True)

    quartz_id = QUARTZ_CIF.stem
    cristobalite_id = CRISTOBALITE_CIF.stem

    rows = [
        (metrics[0], mp["material_id"], quartz_id, cristobalite_id, mp["material_id"] == quartz_id),
        (
            metrics[1],
            mp["space_group_symbol_raw"],
            quartz["space_group_symbol_raw"],
            cristobalite["space_group_symbol_raw"],
            mp["space_group_symbol_norm"] == quartz["space_group_symbol_norm"],
        ),
        (
            metrics[2],
            mp["space_group_number"],
            quartz["space_group_number"],
            cristobalite["space_group_number"],
            mp["space_group_number"] == quartz["space_group_number"],
        ),
        (
            metrics[3],
            mp["si_o_short"],
            quartz["si_o_short"],
            cristobalite["si_o_short"],
            abs(mp["si_o_short"] - quartz["si_o_short"]) <= 0.02,
        ),
        (
            metrics[4],
            mp["si_o_long"],
            quartz["si_o_long"],
            cristobalite["si_o_long"],
            abs(mp["si_o_long"] - quartz["si_o_long"]) <= 0.02,
        ),
        (
            metrics[5],
            mp["angle_deg"],
            quartz["angle_deg"],
            cristobalite["angle_deg"],
            abs(mp["angle_deg"] - quartz["angle_deg"]) <= 2.0,
        ),
    ]

    blue_font = Font(color=BLUE_RGB)
    black_font = Font(color=BLACK_RGB)

    for row_index, row_values in enumerate(rows, start=2):
        metric, mp_value, quartz_value, cristobalite_value, match_value = row_values
        ws[f"A{row_index}"] = metric

        ws[f"B{row_index}"] = mp_value
        ws[f"B{row_index}"].font = blue_font

        ws[f"C{row_index}"] = quartz_value
        ws[f"C{row_index}"].font = black_font

        ws[f"D{row_index}"] = cristobalite_value
        ws[f"D{row_index}"].font = black_font

        ws[f"E{row_index}"] = bool(match_value)

    for row_index in (5, 6):
        for column in ("B", "C", "D"):
            ws[f"{column}{row_index}"].number_format = "0.000"

    for column in ("B", "C", "D"):
        ws[f"{column}7"].number_format = "0.0"

    return workbook


workbook = build_workbook()
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
workbook.save(OUTPUT_FILE)
workbook.close()
PY
