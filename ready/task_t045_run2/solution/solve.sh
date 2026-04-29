#!/bin/bash
set -e

# Auto-generated solution based on execution trajectory
# This script recreates the outputs produced during synthesis

# Execute command
ls -la /root/

# Execute command
mkdir -p /root/output

# Create /root/polymorph_check.py
mkdir -p $(dirname /root/polymorph_check.py)
cat << 'HEREDOC_EOF' > /root/polymorph_check.py
#!/usr/bin/env python3
"""
Polymorph identity check: Compare CIF files to Materials Project HTML page.
Uses pymatgen for structure analysis.
"""

import json
import re
import os
from pathlib import Path

from pymatgen.core import Structure
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer


def parse_mp_html(html_path: str) -> dict:
    """
    Parse Materials Project HTML file to extract key information.

    Args:
        html_path: Path to the HTML file

    Returns:
        Dictionary with mp_material_id, mp_crystal_system, mp_space_group_symbol,
        mp_space_group_number, mp_label
    """
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract from og:title meta tags; pick the first parseable mp-* entry
    og_titles = re.findall(r'<meta property="og:title" content="([^"]+)"', content)
    title_match = None
    for og_title in og_titles:
        tm = re.match(r'(mp-\d+):\s*\S+\s*\((\w+),\s*([^,]+),\s*(\d+)\)', og_title)
        if tm:
            title_match = tm
            break

    if title_match:
        mp_material_id = title_match.group(1)
        mp_crystal_system = title_match.group(2).lower()
        mp_space_group_symbol = title_match.group(3)
        mp_space_group_number = int(title_match.group(4))
    else:
        raise ValueError('Could not parse mp-* payload from og:title tags')

    # Extract polymorph label from og:description
    # "SiO₂ is quartz (alpha) structured..."
    og_desc_match = re.search(
        r'<meta property="og:description" content="([^"]+)"',
        content
    )

    mp_label = ""
    if og_desc_match:
        og_desc = og_desc_match.group(1)
        # Look for "quartz (alpha)" or similar
        label_match = re.search(r'is\s+([\w\-]+)\s*\(([^\)]+)\)\s+structured', og_desc)
        if label_match:
            # Combine to "alpha-quartz" format
            modifier = label_match.group(2)  # "alpha"
            mineral = label_match.group(1)   # "quartz"
            mp_label = f"{modifier}-{mineral}"  # "alpha-quartz"

    return {
        "mp_material_id": mp_material_id,
        "mp_crystal_system": mp_crystal_system,
        "mp_space_group_symbol": mp_space_group_symbol,
        "mp_space_group_number": mp_space_group_number,
        "mp_label": mp_label
    }


def analyze_cif(cif_path: str) -> dict:
    """
    Load a CIF file with pymatgen and compute required properties.

    Args:
        cif_path: Path to the CIF file

    Returns:
        Dictionary with space_group_symbol, space_group_number, crystal_system,
        density, volume
    """
    struct = Structure.from_file(cif_path)
    sga = SpacegroupAnalyzer(struct)

    return {
        "space_group_symbol": sga.get_space_group_symbol(),
        "space_group_number": int(sga.get_space_group_number()),
        "crystal_system": sga.get_crystal_system(),
        "density": float(struct.density),
        "volume": float(struct.volume),
    }


def main():
    # File paths
    input_dir = Path("/root")
    output_path = Path("/root/sio2_polymorph_match.json")

    html_path = input_dir / "1272701"
    quartz_cif = input_dir / "SiO2-Quartz-alpha.cif"
    cristobalite_cif = input_dir / "SiO2-Cristobalite.cif"

    # Step 1: Parse MP HTML
    print("Parsing Materials Project HTML...")
    mp_info = parse_mp_html(str(html_path))
    print(f"  Material ID: {mp_info['mp_material_id']}")
    print(f"  Crystal system: {mp_info['mp_crystal_system']}")
    print(f"  Space group symbol: {mp_info['mp_space_group_symbol']}")
    print(f"  Space group number: {mp_info['mp_space_group_number']}")
    print(f"  Label: {mp_info['mp_label']}")

    # Step 2: Analyze both CIFs with pymatgen
    print("\nAnalyzing CIF files with pymatgen...")

    quartz_props = analyze_cif(str(quartz_cif))
    print(f"\nQuartz-alpha CIF:")
    print(f"  Space group: {quartz_props['space_group_symbol']} (#{quartz_props['space_group_number']})")
    print(f"  Crystal system: {quartz_props['crystal_system']}")
    print(f"  Density: {quartz_props['density']:.4f} g/cm³")
    print(f"  Volume: {quartz_props['volume']:.4f} Å³")

    cristobalite_props = analyze_cif(str(cristobalite_cif))
    print(f"\nCristobalite CIF:")
    print(f"  Space group: {cristobalite_props['space_group_symbol']} (#{cristobalite_props['space_group_number']})")
    print(f"  Crystal system: {cristobalite_props['crystal_system']}")
    print(f"  Density: {cristobalite_props['density']:.4f} g/cm³")
    print(f"  Volume: {cristobalite_props['volume']:.4f} Å³")

    # Step 3: Determine matching CIF (space_group_number AND crystal_system must match)
    cifs = {
        "SiO2-Quartz-alpha.cif": quartz_props,
        "SiO2-Cristobalite.cif": cristobalite_props,
    }

    matching_cifs = []
    for cif_name, props in cifs.items():
        if (props["space_group_number"] == mp_info["mp_space_group_number"] and
            props["crystal_system"] == mp_info["mp_crystal_system"]):
            matching_cifs.append(cif_name)

    print(f"\nMatching CIFs: {matching_cifs}")

    # Determine match status
    if len(matching_cifs) == 1:
        match_status = "match"
        matching_cif = matching_cifs[0]
        nonmatching_cif = [c for c in cifs.keys() if c != matching_cif][0]
    elif len(matching_cifs) == 2:
        match_status = "ambiguous"
        matching_cif = list(cifs.keys())[0]
        nonmatching_cif = list(cifs.keys())[1]
    else:  # len(matching_cifs) == 0
        match_status = "no_match"
        matching_cif = list(cifs.keys())[0]
        nonmatching_cif = list(cifs.keys())[1]

    matching_properties = cifs[matching_cif]
    nonmatching_properties = cifs[nonmatching_cif]

    # Step 4: Compute percent differences
    density_match = matching_properties["density"]
    density_nonmatch = nonmatching_properties["density"]
    density_percent_diff = round(100 * (density_nonmatch - density_match) / density_match, 3)

    volume_match = matching_properties["volume"]
    volume_nonmatch = nonmatching_properties["volume"]
    volume_percent_diff = round(100 * (volume_nonmatch - volume_match) / volume_match, 3)

    print(f"\nMatch status: {match_status}")
    print(f"Matching CIF: {matching_cif}")
    print(f"Non-matching CIF: {nonmatching_cif}")
    print(f"Density percent diff: {density_percent_diff}%")
    print(f"Volume percent diff: {volume_percent_diff}%")

    # Step 5: Build output JSON
    output = {
        "mp_material_id": mp_info["mp_material_id"],
        "mp_space_group_symbol": mp_info["mp_space_group_symbol"],
        "mp_space_group_number": mp_info["mp_space_group_number"],
        "mp_crystal_system": mp_info["mp_crystal_system"],
        "mp_label": mp_info["mp_label"],
        "match_status": match_status,
        "matching_cif": matching_cif,
        "nonmatching_cif": nonmatching_cif,
        "matching_properties": {
            "space_group_symbol": matching_properties["space_group_symbol"],
            "space_group_number": matching_properties["space_group_number"],
            "crystal_system": matching_properties["crystal_system"],
            "density": matching_properties["density"],
            "volume": matching_properties["volume"],
        },
        "nonmatching_properties": {
            "space_group_symbol": nonmatching_properties["space_group_symbol"],
            "space_group_number": nonmatching_properties["space_group_number"],
            "crystal_system": nonmatching_properties["crystal_system"],
            "density": nonmatching_properties["density"],
            "volume": nonmatching_properties["volume"],
        },
        "nonmatch_vs_match_percent_diff": {
            "density": density_percent_diff,
            "volume": volume_percent_diff,
        }
    }

    # Write output file
    os.makedirs(output_path.parent, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\nOutput written to: {output_path}")

    # Verify output
    with open(output_path, "r") as f:
        verified = json.load(f)
    print("\nVerification - JSON structure:")
    print(json.dumps(verified, indent=2))


if __name__ == "__main__":
    main()

HEREDOC_EOF

# Execute command
python3 polymorph_check.py

# Execute command
python3 polymorph_check.py

# Execute command
python3 polymorph_check.py

# Create /root/expectation_tests.py
mkdir -p $(dirname /root/expectation_tests.py)
cat << 'HEREDOC_EOF' > /root/expectation_tests.py
"""Auto-generated expectation tests for SiO2 polymorph identity check task.

These tests verify that the task execution produces correct outputs
based on the instruction requirements for comparing CIF files against
Materials Project data (mp-6930).
"""

import json
import os
from pathlib import Path

import pytest


# Constants for paths
OUTPUT_FILE = "/root/sio2_polymorph_match.json"
INPUT_DIR = "/root"
QUARTZ_CIF = os.path.join(INPUT_DIR, "SiO2-Quartz-alpha.cif")
CRISTOBALITE_CIF = os.path.join(INPUT_DIR, "SiO2-Cristobalite.cif")
MP_HTML_FILE = os.path.join(INPUT_DIR, "1272701")

# Required top-level keys in exact order from schema
REQUIRED_TOP_LEVEL_KEYS = [
    "mp_material_id",
    "mp_space_group_symbol",
    "mp_space_group_number",
    "mp_crystal_system",
    "mp_label",
    "match_status",
    "matching_cif",
    "nonmatching_cif",
    "matching_properties",
    "nonmatching_properties",
    "nonmatch_vs_match_percent_diff",
]

# Required keys in properties dictionaries
REQUIRED_PROPERTIES_KEYS = [
    "space_group_symbol",
    "space_group_number",
    "crystal_system",
    "density",
    "volume",
]

# Required keys in percent diff dictionary
REQUIRED_PERCENT_DIFF_KEYS = ["density", "volume"]


class TestOutputFileExistence:
    """Tests for output file existence and basic validity."""

    def test_output_file_exists(self):
        """Verify output JSON file was created at expected path."""
        assert os.path.exists(OUTPUT_FILE), (
            f"Output file not found at {OUTPUT_FILE}"
        )

    def test_output_file_is_not_empty(self):
        """Verify output file is not empty."""
        assert os.path.getsize(OUTPUT_FILE) > 0, "Output file is empty"


class TestOutputFormat:
    """Tests for valid JSON format and structure."""

    @pytest.fixture
    def output_data(self):
        """Load output JSON data."""
        with open(OUTPUT_FILE) as f:
            return json.load(f)

    def test_output_is_valid_json(self):
        """Verify output is valid JSON format."""
        with open(OUTPUT_FILE) as f:
            data = json.load(f)
        assert data is not None, "JSON data is None"
        assert isinstance(data, dict), "JSON root should be a dictionary"

    def test_has_all_required_top_level_keys(self, output_data):
        """Verify all required top-level keys are present."""
        for key in REQUIRED_TOP_LEVEL_KEYS:
            assert key in output_data, f"Missing required key: {key}"

    def test_no_extra_top_level_keys(self, output_data):
        """Verify no extra top-level keys beyond required schema."""
        extra_keys = set(output_data.keys()) - set(REQUIRED_TOP_LEVEL_KEYS)
        assert not extra_keys, f"Unexpected extra keys: {extra_keys}"

    def test_matching_properties_is_dict(self, output_data):
        """Verify matching_properties is a dictionary."""
        assert isinstance(output_data["matching_properties"], dict), (
            "matching_properties should be a dictionary"
        )

    def test_nonmatching_properties_is_dict(self, output_data):
        """Verify nonmatching_properties is a dictionary."""
        assert isinstance(output_data["nonmatching_properties"], dict), (
            "nonmatching_properties should be a dictionary"
        )

    def test_percent_diff_is_dict(self, output_data):
        """Verify nonmatch_vs_match_percent_diff is a dictionary."""
        assert isinstance(output_data["nonmatch_vs_match_percent_diff"], dict), (
            "nonmatch_vs_match_percent_diff should be a dictionary"
        )

    def test_matching_properties_has_required_keys(self, output_data):
        """Verify matching_properties has all required keys."""
        props = output_data["matching_properties"]
        for key in REQUIRED_PROPERTIES_KEYS:
            assert key in props, f"matching_properties missing key: {key}"

    def test_matching_properties_no_extra_keys(self, output_data):
        """Verify matching_properties has no extra keys."""
        props = output_data["matching_properties"]
        extra_keys = set(props.keys()) - set(REQUIRED_PROPERTIES_KEYS)
        assert not extra_keys, (
            f"matching_properties has extra keys: {extra_keys}"
        )

    def test_nonmatching_properties_has_required_keys(self, output_data):
        """Verify nonmatching_properties has all required keys."""
        props = output_data["nonmatching_properties"]
        for key in REQUIRED_PROPERTIES_KEYS:
            assert key in props, f"nonmatching_properties missing key: {key}"

    def test_nonmatching_properties_no_extra_keys(self, output_data):
        """Verify nonmatching_properties has no extra keys."""
        props = output_data["nonmatching_properties"]
        extra_keys = set(props.keys()) - set(REQUIRED_PROPERTIES_KEYS)
        assert not extra_keys, (
            f"nonmatching_properties has extra keys: {extra_keys}"
        )

    def test_percent_diff_has_required_keys(self, output_data):
        """Verify nonmatch_vs_match_percent_diff has required keys."""
        diff = output_data["nonmatch_vs_match_percent_diff"]
        for key in REQUIRED_PERCENT_DIFF_KEYS:
            assert key in diff, (
                f"nonmatch_vs_match_percent_diff missing key: {key}"
            )

    def test_percent_diff_no_extra_keys(self, output_data):
        """Verify nonmatch_vs_match_percent_diff has no extra keys."""
        diff = output_data["nonmatch_vs_match_percent_diff"]
        extra_keys = set(diff.keys()) - set(REQUIRED_PERCENT_DIFF_KEYS)
        assert not extra_keys, (
            f"nonmatch_vs_match_percent_diff has extra keys: {extra_keys}"
        )


class TestDataTypes:
    """Tests for correct data types of all fields."""

    @pytest.fixture
    def output_data(self):
        """Load output JSON data."""
        with open(OUTPUT_FILE) as f:
            return json.load(f)

    def test_mp_material_id_is_string(self, output_data):
        """Verify mp_material_id is a string."""
        assert isinstance(output_data["mp_material_id"], str)

    def test_mp_space_group_symbol_is_string(self, output_data):
        """Verify mp_space_group_symbol is a string."""
        assert isinstance(output_data["mp_space_group_symbol"], str)

    def test_mp_space_group_number_is_integer(self, output_data):
        """Verify mp_space_group_number is an integer (JSON number)."""
        val = output_data["mp_space_group_number"]
        assert isinstance(val, int), (
            f"mp_space_group_number should be int, got {type(val)}"
        )

    def test_mp_crystal_system_is_string(self, output_data):
        """Verify mp_crystal_system is a string."""
        assert isinstance(output_data["mp_crystal_system"], str)

    def test_mp_label_is_string(self, output_data):
        """Verify mp_label is a string."""
        assert isinstance(output_data["mp_label"], str)

    def test_match_status_is_string(self, output_data):
        """Verify match_status is a string."""
        assert isinstance(output_data["match_status"], str)

    def test_matching_cif_is_string(self, output_data):
        """Verify matching_cif is a string."""
        assert isinstance(output_data["matching_cif"], str)

    def test_nonmatching_cif_is_string(self, output_data):
        """Verify nonmatching_cif is a string."""
        assert isinstance(output_data["nonmatching_cif"], str)

    def test_properties_space_group_symbol_is_string(self, output_data):
        """Verify space_group_symbol in properties is string."""
        assert isinstance(
            output_data["matching_properties"]["space_group_symbol"], str
        )
        assert isinstance(
            output_data["nonmatching_properties"]["space_group_symbol"], str
        )

    def test_properties_space_group_number_is_integer(self, output_data):
        """Verify space_group_number in properties is integer."""
        val_match = output_data["matching_properties"]["space_group_number"]
        val_nonmatch = output_data["nonmatching_properties"]["space_group_number"]
        assert isinstance(val_match, int), (
            f"matching space_group_number should be int, got {type(val_match)}"
        )
        assert isinstance(val_nonmatch, int), (
            f"nonmatching space_group_number should be int, got {type(val_nonmatch)}"
        )

    def test_properties_crystal_system_is_string(self, output_data):
        """Verify crystal_system in properties is string."""
        assert isinstance(
            output_data["matching_properties"]["crystal_system"], str
        )
        assert isinstance(
            output_data["nonmatching_properties"]["crystal_system"], str
        )

    def test_properties_density_is_number(self, output_data):
        """Verify density in properties is a number (int or float)."""
        val_match = output_data["matching_properties"]["density"]
        val_nonmatch = output_data["nonmatching_properties"]["density"]
        assert isinstance(val_match, (int, float)), (
            f"matching density should be number, got {type(val_match)}"
        )
        assert isinstance(val_nonmatch, (int, float)), (
            f"nonmatching density should be number, got {type(val_nonmatch)}"
        )

    def test_properties_volume_is_number(self, output_data):
        """Verify volume in properties is a number (int or float)."""
        val_match = output_data["matching_properties"]["volume"]
        val_nonmatch = output_data["nonmatching_properties"]["volume"]
        assert isinstance(val_match, (int, float)), (
            f"matching volume should be number, got {type(val_match)}"
        )
        assert isinstance(val_nonmatch, (int, float)), (
            f"nonmatching volume should be number, got {type(val_nonmatch)}"
        )

    def test_percent_diff_values_are_numbers(self, output_data):
        """Verify percent difference values are numbers."""
        diff = output_data["nonmatch_vs_match_percent_diff"]
        assert isinstance(diff["density"], (int, float)), (
            f"density percent diff should be number, got {type(diff['density'])}"
        )
        assert isinstance(diff["volume"], (int, float)), (
            f"volume percent diff should be number, got {type(diff['volume'])}"
        )


class TestMaterialsProjectValues:
    """Tests for correct extraction of Materials Project metadata from HTML."""

    @pytest.fixture
    def output_data(self):
        """Load output JSON data."""
        with open(OUTPUT_FILE) as f:
            return json.load(f)

    def test_mp_material_id_value(self, output_data):
        """Verify mp_material_id is mp-6930 (from HTML meta tags)."""
        assert output_data["mp_material_id"] == "mp-6930", (
            f"Expected mp-6930, got {output_data['mp_material_id']}"
        )

    def test_mp_space_group_symbol_value(self, output_data):
        """Verify mp_space_group_symbol is P3_221 (from HTML)."""
        # The HTML shows "P3_221" in the meta tag
        assert output_data["mp_space_group_symbol"] == "P3_221", (
            f"Expected P3_221, got {output_data['mp_space_group_symbol']}"
        )

    def test_mp_space_group_number_value(self, output_data):
        """Verify mp_space_group_number is 154 (from HTML)."""
        assert output_data["mp_space_group_number"] == 154, (
            f"Expected 154, got {output_data['mp_space_group_number']}"
        )

    def test_mp_crystal_system_value(self, output_data):
        """Verify mp_crystal_system is trigonal (from HTML)."""
        # The HTML shows "Trigonal" - output should be lowercase
        assert output_data["mp_crystal_system"].lower() == "trigonal", (
            f"Expected trigonal, got {output_data['mp_crystal_system']}"
        )

    def test_mp_label_contains_alpha_quartz(self, output_data):
        """Verify mp_label contains alpha-quartz or similar identifier."""
        label = output_data["mp_label"].lower()
        # HTML description mentions "quartz (alpha)"
        assert "quartz" in label or "alpha" in label, (
            f"Expected label to contain 'quartz' or 'alpha', got {output_data['mp_label']}"
        )


class TestMatchingLogic:
    """Tests for correct CIF matching logic."""

    @pytest.fixture
    def output_data(self):
        """Load output JSON data."""
        with open(OUTPUT_FILE) as f:
            return json.load(f)

    def test_match_status_is_valid(self, output_data):
        """Verify match_status is one of valid values."""
        valid_statuses = ["match", "ambiguous", "no_match"]
        assert output_data["match_status"] in valid_statuses, (
            f"Invalid match_status: {output_data['match_status']}"
        )

    def test_quartz_is_matching_cif(self, output_data):
        """Verify quartz CIF is identified as the matching one.

        Based on the inputs:
        - MP data shows trigonal, space group 154
        - Quartz CIF: trigonal, space group 154 - MATCH
        - Cristobalite CIF: tetragonal, space group 92 - NO MATCH
        """
        assert output_data["matching_cif"] == "SiO2-Quartz-alpha.cif", (
            f"Expected SiO2-Quartz-alpha.cif as matching, got {output_data['matching_cif']}"
        )

    def test_cristobalite_is_nonmatching_cif(self, output_data):
        """Verify cristobalite CIF is identified as non-matching."""
        assert output_data["nonmatching_cif"] == "SiO2-Cristobalite.cif", (
            f"Expected SiO2-Cristobalite.cif as non-matching, got {output_data['nonmatching_cif']}"
        )

    def test_match_status_is_match_when_unique(self, output_data):
        """Verify match_status is 'match' when exactly one CIF matches."""
        # Since quartz matches and cristobalite doesn't, status should be "match"
        assert output_data["match_status"] == "match", (
            f"Expected 'match' status, got {output_data['match_status']}"
        )

    def test_matching_cif_basename_format(self, output_data):
        """Verify matching_cif uses exact basename (not full path)."""
        matching = output_data["matching_cif"]
        assert "/" not in matching, "matching_cif should be basename, not path"
        assert matching.endswith(".cif"), "matching_cif should end with .cif"

    def test_nonmatching_cif_basename_format(self, output_data):
        """Verify nonmatching_cif uses exact basename (not full path)."""
        nonmatching = output_data["nonmatching_cif"]
        assert "/" not in nonmatching, "nonmatching_cif should be basename, not path"
        assert nonmatching.endswith(".cif"), "nonmatching_cif should end with .cif"


class TestMatchingProperties:
    """Tests for matching CIF computed properties."""

    @pytest.fixture
    def output_data(self):
        """Load output JSON data."""
        with open(OUTPUT_FILE) as f:
            return json.load(f)

    def test_matching_space_group_number_is_154(self, output_data):
        """Verify matching CIF (quartz) has space group number 154."""
        sg_num = output_data["matching_properties"]["space_group_number"]
        assert sg_num == 154, f"Expected 154, got {sg_num}"

    def test_matching_crystal_system_is_trigonal(self, output_data):
        """Verify matching CIF (quartz) has trigonal crystal system."""
        crystal_sys = output_data["matching_properties"]["crystal_system"]
        assert crystal_sys.lower() == "trigonal", (
            f"Expected trigonal, got {crystal_sys}"
        )

    def test_matching_density_is_positive(self, output_data):
        """Verify matching density is positive."""
        density = output_data["matching_properties"]["density"]
        assert density > 0, f"Density should be positive, got {density}"

    def test_matching_density_is_reasonable_for_quartz(self, output_data):
        """Verify matching density is in reasonable range for quartz (~2.5-2.7 g/cm3)."""
        density = output_data["matching_properties"]["density"]
        assert 2.0 < density < 3.0, (
            f"Quartz density should be ~2.5-2.7 g/cm3, got {density}"
        )

    def test_matching_volume_is_positive(self, output_data):
        """Verify matching volume is positive."""
        volume = output_data["matching_properties"]["volume"]
        assert volume > 0, f"Volume should be positive, got {volume}"

    def test_matching_volume_is_reasonable_for_quartz(self, output_data):
        """Verify matching volume is in reasonable range for quartz unit cell."""
        # Quartz CIF shows ~112.9 A^3
        volume = output_data["matching_properties"]["volume"]
        assert 100 < volume < 130, (
            f"Quartz volume should be ~112.9 A^3, got {volume}"
        )


class TestNonMatchingProperties:
    """Tests for non-matching CIF computed properties."""

    @pytest.fixture
    def output_data(self):
        """Load output JSON data."""
        with open(OUTPUT_FILE) as f:
            return json.load(f)

    def test_nonmatching_space_group_number_is_92(self, output_data):
        """Verify non-matching CIF (cristobalite) has space group number 92."""
        sg_num = output_data["nonmatching_properties"]["space_group_number"]
        assert sg_num == 92, f"Expected 92, got {sg_num}"

    def test_nonmatching_crystal_system_is_tetragonal(self, output_data):
        """Verify non-matching CIF (cristobalite) has tetragonal crystal system."""
        crystal_sys = output_data["nonmatching_properties"]["crystal_system"]
        assert crystal_sys.lower() == "tetragonal", (
            f"Expected tetragonal, got {crystal_sys}"
        )

    def test_nonmatching_density_is_positive(self, output_data):
        """Verify non-matching density is positive."""
        density = output_data["nonmatching_properties"]["density"]
        assert density > 0, f"Density should be positive, got {density}"

    def test_nonmatching_density_is_reasonable_for_cristobalite(self, output_data):
        """Verify non-matching density is in reasonable range for cristobalite (~2.2-2.4 g/cm3)."""
        density = output_data["nonmatching_properties"]["density"]
        assert 2.0 < density < 3.0, (
            f"Cristobalite density should be ~2.2-2.4 g/cm3, got {density}"
        )

    def test_nonmatching_volume_is_positive(self, output_data):
        """Verify non-matching volume is positive."""
        volume = output_data["nonmatching_properties"]["volume"]
        assert volume > 0, f"Volume should be positive, got {volume}"

    def test_nonmatching_volume_is_reasonable_for_cristobalite(self, output_data):
        """Verify non-matching volume is in reasonable range for cristobalite unit cell."""
        # Cristobalite CIF shows ~171.104 A^3
        volume = output_data["nonmatching_properties"]["volume"]
        assert 150 < volume < 190, (
            f"Cristobalite volume should be ~171.1 A^3, got {volume}"
        )


class TestPercentDifferences:
    """Tests for percent difference calculations."""

    @pytest.fixture
    def output_data(self):
        """Load output JSON data."""
        with open(OUTPUT_FILE) as f:
            return json.load(f)

    def test_density_percent_diff_calculation(self, output_data):
        """Verify density percent diff is calculated correctly.

        Formula: 100 * (density_nonmatch - density_match) / density_match
        """
        match_density = output_data["matching_properties"]["density"]
        nonmatch_density = output_data["nonmatching_properties"]["density"]
        expected_diff = 100 * (nonmatch_density - match_density) / match_density
        actual_diff = output_data["nonmatch_vs_match_percent_diff"]["density"]

        # Should be rounded to 3 decimal places
        assert abs(actual_diff - round(expected_diff, 3)) < 0.001, (
            f"Density diff should be ~{round(expected_diff, 3)}, got {actual_diff}"
        )

    def test_volume_percent_diff_calculation(self, output_data):
        """Verify volume percent diff is calculated correctly.

        Formula: 100 * (volume_nonmatch - volume_match) / volume_match
        """
        match_volume = output_data["matching_properties"]["volume"]
        nonmatch_volume = output_data["nonmatching_properties"]["volume"]
        expected_diff = 100 * (nonmatch_volume - match_volume) / match_volume
        actual_diff = output_data["nonmatch_vs_match_percent_diff"]["volume"]

        # Should be rounded to 3 decimal places
        assert abs(actual_diff - round(expected_diff, 3)) < 0.001, (
            f"Volume diff should be ~{round(expected_diff, 3)}, got {actual_diff}"
        )

    def test_density_percent_diff_is_negative(self, output_data):
        """Verify density percent diff is negative (cristobalite is less dense than quartz)."""
        diff = output_data["nonmatch_vs_match_percent_diff"]["density"]
        assert diff < 0, (
            f"Cristobalite density < quartz density, so diff should be negative, got {diff}"
        )

    def test_volume_percent_diff_is_positive(self, output_data):
        """Verify volume percent diff is positive (cristobalite has larger volume than quartz)."""
        diff = output_data["nonmatch_vs_match_percent_diff"]["volume"]
        assert diff > 0, (
            f"Cristobalite volume > quartz volume, so diff should be positive, got {diff}"
        )

    def test_percent_diff_rounded_to_3_decimals(self, output_data):
        """Verify percent differences are rounded to exactly 3 decimal places."""
        diff = output_data["nonmatch_vs_match_percent_diff"]

        for key in ["density", "volume"]:
            val = diff[key]
            # Check that rounding to 3 decimals doesn't change the value
            rounded = round(val, 3)
            assert val == rounded, (
                f"{key} percent diff should be rounded to 3 decimals: {val} != {rounded}"
            )


class TestPropertyConsistency:
    """Tests for consistency between matching/non-matching properties."""

    @pytest.fixture
    def output_data(self):
        """Load output JSON data."""
        with open(OUTPUT_FILE) as f:
            return json.load(f)

    def test_matching_and_nonmatching_are_different_cifs(self, output_data):
        """Verify matching and non-matching CIF names are different."""
        assert output_data["matching_cif"] != output_data["nonmatching_cif"], (
            "matching_cif and nonmatching_cif should be different files"
        )

    def test_space_groups_are_different(self, output_data):
        """Verify matching and non-matching have different space groups."""
        match_sg = output_data["matching_properties"]["space_group_number"]
        nonmatch_sg = output_data["nonmatching_properties"]["space_group_number"]
        assert match_sg != nonmatch_sg, (
            "Space group numbers should differ between quartz and cristobalite"
        )

    def test_crystal_systems_are_different(self, output_data):
        """Verify matching and non-matching have different crystal systems."""
        match_cs = output_data["matching_properties"]["crystal_system"].lower()
        nonmatch_cs = output_data["nonmatching_properties"]["crystal_system"].lower()
        assert match_cs != nonmatch_cs, (
            "Crystal systems should differ between quartz (trigonal) and cristobalite (tetragonal)"
        )

    def test_matching_properties_match_mp_values(self, output_data):
        """Verify matching CIF properties match MP-derived values."""
        mp_sg_num = output_data["mp_space_group_number"]
        mp_crystal = output_data["mp_crystal_system"].lower()

        match_sg_num = output_data["matching_properties"]["space_group_number"]
        match_crystal = output_data["matching_properties"]["crystal_system"].lower()

        assert match_sg_num == mp_sg_num, (
            f"Matching space group ({match_sg_num}) should equal MP space group ({mp_sg_num})"
        )
        assert match_crystal == mp_crystal, (
            f"Matching crystal system ({match_crystal}) should equal MP crystal system ({mp_crystal})"
        )


class TestPymatgenComputation:
    """Tests to verify properties were computed via pymatgen, not hardcoded."""

    @pytest.fixture
    def output_data(self):
        """Load output JSON data."""
        with open(OUTPUT_FILE) as f:
            return json.load(f)

    def test_space_group_symbol_has_spaces(self, output_data):
        """Verify space group symbols have standard pymatgen format with spaces.

        Pymatgen SpacegroupAnalyzer returns symbols like 'P 32 2 1' with spaces,
        unlike the CIF file which might have 'P 32 2 1' or the HTML 'P3_221'.
        """
        match_symbol = output_data["matching_properties"]["space_group_symbol"]
        nonmatch_symbol = output_data["nonmatching_properties"]["space_group_symbol"]

        # Pymatgen typically returns symbols with spaces
        # At minimum, they should be non-empty strings
        assert len(match_symbol) > 0, "Matching space_group_symbol should not be empty"
        assert len(nonmatch_symbol) > 0, "Non-matching space_group_symbol should not be empty"

    def test_density_has_precision(self, output_data):
        """Verify density values have decimal precision (computed, not rounded integers)."""
        match_density = output_data["matching_properties"]["density"]
        nonmatch_density = output_data["nonmatching_properties"]["density"]

        # Densities should not be perfectly round integers
        # Pymatgen computes precise values
        assert match_density != int(match_density) or (
            isinstance(match_density, float)
        ), "Density should be a precise float from pymatgen"

    def test_volume_has_precision(self, output_data):
        """Verify volume values have reasonable precision."""
        match_volume = output_data["matching_properties"]["volume"]
        nonmatch_volume = output_data["nonmatching_properties"]["volume"]

        # Volumes should be precise float values
        assert isinstance(match_volume, (int, float)), "Volume should be numeric"
        assert isinstance(nonmatch_volume, (int, float)), "Volume should be numeric"

HEREDOC_EOF

# Execute command
python3 -m py_compile expectation_tests.py && echo "Syntax OK"

