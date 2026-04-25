#!/bin/bash
set -e

# Create output directory
mkdir -p /root/output

# Create the solution Python script using heredoc
cat << 'EOF' > /root/solve_task.py
#!/usr/bin/env python3
"""
Generate SiO2 polymorph fingerprint JSON matching mp-6930.
"""

import json
import re
import numpy as np
from pathlib import Path

from pymatgen.core import Structure
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
from pymatgen.analysis.local_env import CrystalNN
from pymatgen.analysis.diffraction.xrd import XRDCalculator
from sklearn.preprocessing import StandardScaler
from factor_analyzer import FactorAnalyzer

BASE_DIR = Path("/root")
INPUT_DIR = BASE_DIR 
OUTPUT_DIR = BASE_DIR / "output"

def round6(x):
    """Round a float to 6 decimal places, avoiding negative zero."""
    result = float(f"{x:.6f}")
    return 0.0 if result == 0.0 else result


def parse_html_reference(html_path):
    """Parse Materials Project HTML file for reference symmetry descriptors."""
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Pattern for: content="mp-6930: SiO2 (Trigonal, P3_221, 154)"
    pattern = r'<meta property="og:title" content="(mp-\d+): [^(]+\(([^,]+),\s*([^,]+),\s*(\d+)\)"'
    match = re.search(pattern, html_content)

    if not match:
        raise ValueError("Could not parse reference descriptors from HTML")

    return {
        "material_id": match.group(1),
        "crystal_system": match.group(2).strip(),
        "spacegroup_symbol": match.group(3).strip(),
        "spacegroup_number": int(match.group(4))
    }


def analyze_cif(cif_path):
    """Load CIF and compute all required structural properties."""
    struct = Structure.from_file(cif_path)

    # Symmetry analysis
    sga = SpacegroupAnalyzer(struct)
    spg_symbol = sga.get_space_group_symbol()
    spg_number = sga.get_space_group_number()
    crystal_system = sga.get_crystal_system()

    # Basic properties
    volume = struct.volume
    density = struct.density

    # Mean Si-O bond length via CrystalNN
    cnn = CrystalNN()
    si_o_distances = []

    for i, site in enumerate(struct):
        if site.specie.symbol == "Si":
            neighbors = cnn.get_nn_info(struct, n=i)
            for nn in neighbors:
                if nn["site"].specie.symbol == "O":
                    dist = site.distance(nn["site"])
                    si_o_distances.append(dist)

    if not si_o_distances:
        raise ValueError(f"No Si-O bonds found in {cif_path}")

    mean_si_o_bond = sum(si_o_distances) / len(si_o_distances)

    # XRD pattern analysis
    xrd = XRDCalculator()
    pattern = xrd.get_pattern(struct, two_theta_range=(10, 80))

    peak_count = len(pattern.x)
    max_intensity_idx = int(np.argmax(pattern.y))
    max_intensity_2theta = float(pattern.x[max_intensity_idx])

    return {
        "file": Path(cif_path).name,
        "spacegroup_symbol": spg_symbol,
        "spacegroup_number": spg_number,
        "crystal_system": crystal_system,
        "volume": volume,
        "density": density,
        "mean_si_o_bond": mean_si_o_bond,
        "peak_count": peak_count,
        "max_intensity_2theta": max_intensity_2theta
    }


def main():
    # Step 1: Parse HTML reference
    html_path = INPUT_DIR / "1272701"
    reference = parse_html_reference(html_path)

    # Step 2: Analyze both CIF files (fixed order: Quartz-alpha first, Cristobalite second)
    quartz_path = INPUT_DIR / "SiO2-Quartz-alpha.cif"
    cristobalite_path = INPUT_DIR / "SiO2-Cristobalite.cif"

    quartz_data = analyze_cif(quartz_path)
    cristobalite_data = analyze_cif(cristobalite_path)

    structures = [quartz_data, cristobalite_data]

    # Step 3: Match CIF to mp-6930 by exact match of (space group number AND symbol)
    ref_sym = reference["spacegroup_symbol"]
    ref_num = reference["spacegroup_number"]

    matches = []
    for s in structures:
        sym_match = (s["spacegroup_symbol"].replace(" ", "") == ref_sym.replace(" ", "") or
                     s["spacegroup_symbol"] == ref_sym)
        num_match = s["spacegroup_number"] == ref_num

        if sym_match and num_match:
            matches.append(s["file"])

    if len(matches) != 1:
        # Try more flexible symbol matching
        matches = []
        for s in structures:
            if s["spacegroup_number"] == ref_num:
                s_sym_norm = s["spacegroup_symbol"].replace(" ", "").replace("_", "")
                ref_sym_norm = ref_sym.replace(" ", "").replace("_", "")
                if s_sym_norm == ref_sym_norm:
                    matches.append(s["file"])

        if len(matches) != 1:
            raise ValueError(f"Expected exactly 1 match for mp-6930, got {len(matches)}: {matches}")

    mp6930_match_file = matches[0]

    # Step 4: Build 2x5 feature table and run FactorAnalyzer
    # Column order: volume, density, mean_si_o_bond, peak_count, max_intensity_2theta
    feature_matrix = np.array([
        [s["volume"], s["density"], s["mean_si_o_bond"], s["peak_count"], s["max_intensity_2theta"]]
        for s in structures
    ])

    # Standardize
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(feature_matrix)

    # Factor analysis with n_factors=1, rotation=None
    # With only 2 samples, use 'principal' method to avoid singular matrix
    fa = FactorAnalyzer(n_factors=1, rotation=None, method='principal')
    fa.fit(X_scaled)

    # Get scores
    scores = fa.transform(X_scaled)

    # Get eigenvalues (full length-5 list)
    eigenvalues, _ = fa.get_eigenvalues()
    eigenvalues_list = list(eigenvalues)

    # Compute PCA separation
    pca_separation = abs(scores[0, 0] - scores[1, 0])

    # Add factor scores to structure data
    structures[0]["factor_score_1d"] = scores[0, 0]
    structures[1]["factor_score_1d"] = scores[1, 0]

    # Step 5: Build final JSON with exact schema and rounding
    output_json = {
        "reference_from_html": {
            "material_id": reference["material_id"],
            "crystal_system": reference["crystal_system"],
            "spacegroup_symbol": reference["spacegroup_symbol"],
            "spacegroup_number": reference["spacegroup_number"]
        },
        "structures": [
            {
                "file": s["file"],
                "spacegroup_symbol": s["spacegroup_symbol"],
                "spacegroup_number": s["spacegroup_number"],
                "crystal_system": s["crystal_system"],
                "volume": round6(s["volume"]),
                "density": round6(s["density"]),
                "mean_si_o_bond": round6(s["mean_si_o_bond"]),
                "peak_count": s["peak_count"],
                "max_intensity_2theta": round6(s["max_intensity_2theta"]),
                "factor_score_1d": round6(s["factor_score_1d"])
            }
            for s in structures
        ],
        "mp6930_match_file": mp6930_match_file,
        "factor_analysis": {
            "n_factors": 1,
            "rotation": None,
            "eigenvalues": [round6(e) for e in eigenvalues_list],
            "pca_separation": round6(pca_separation)
        }
    }

    # Write output JSON
    output_path = OUTPUT_DIR / "sio2_polymorph_fingerprint.json"
    with open(output_path, 'w') as f:
        json.dump(output_json, f, indent=2)

    print(f"Output written to: {output_path}")


if __name__ == "__main__":
    main()
EOF

# Execute the script
python3 /root/solve_task.py
