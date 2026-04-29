#!/bin/bash
set -e

# Auto-generated solution based on execution trajectory
# This script recreates the outputs produced during synthesis

# Execute command
head -c 5000 /root/countries.geo.json | python3 -c "import json, sys; data = json.loads(sys.stdin.read()[:4900] + ']}'); print('Type:', data.get('type')); print('Num features:', len(data.get('features', []))); f = data['features'][0] if data.get('features') else {}; print('Feature keys:', list(f.keys()) if f else 'N/A'); print('Properties:', list(f.get('properties', {}).keys()) if f else 'N/A')" 2>/dev/null || head -c 3000 /root/countries.geo.json

# Execute command
head -c 5000 /root/countries.geojson | python3 -c "import json, sys; data = json.loads(sys.stdin.read()[:4900] + ']}'); print('Type:', data.get('type')); print('Num features:', len(data.get('features', []))); f = data['features'][0] if data.get('features') else {}; print('Feature keys:', list(f.keys()) if f else 'N/A'); print('Properties:', list(f.get('properties', {}).keys()) if f else 'N/A')" 2>/dev/null || head -c 3000 /root/countries.geojson

# Execute command
python3 << 'EOF'
import json

# Check countries.geo.json
with open('/root/countries.geo.json', 'r') as f:
    data = json.load(f)
    print("=== countries.geo.json ===")
    print(f"Number of features: {len(data['features'])}")
    # Get first 3 features' properties
    for i, feat in enumerate(data['features'][:3]):
        print(f"Feature {i} id: {feat.get('id')}, props: {feat.get('properties')}")

print()

# Check countries.geojson
with open('/root/countries.geojson', 'r') as f:
    data2 = json.load(f)
    print("=== countries.geojson ===")
    print(f"Number of features: {len(data2['features'])}")
    props = data2['features'][0].get('properties', {})
    # Show key fields that could be used for matching
    match_candidates = ['iso_a3', 'ISO_A3', 'iso_a2', 'ISO_A2', 'sov_a3', 'adm0_a3', 'name', 'NAME']
    print("First feature matching candidates:")
    for key in props.keys():
        if any(mc.lower() in key.lower() for mc in ['iso', 'a3', 'a2', 'code', 'id']):
            print(f"  {key}: {props[key]}")
EOF

# Create /root/expectation_tests.py
mkdir -p $(dirname /root/expectation_tests.py)
cat << 'HEREDOC_EOF' > /root/expectation_tests.py
"""Auto-generated expectation tests for task verification.

These tests verify that the task execution produces correct outputs
for identifying the country with the largest boundary change between
two GeoJSON datasets.
"""

import json
import os
import re
from pathlib import Path

import pytest


# Constants for the expected paths
OUTPUT_FILE = "/root/largest_boundary_change.json"
INPUT_GEO_JSON = "/root/countries.geo.json"
INPUT_GEOJSON = "/root/countries.geojson"
INPUT_HTML = "/root/geo-countries"


class TestOutputFileExists:
    """Tests for output file existence and basic structure."""

    def test_output_file_exists(self):
        """Verify output file was created at the specified path."""
        assert os.path.exists(OUTPUT_FILE), (
            f"Output file not found at {OUTPUT_FILE}. "
            "The task requires writing the result to this exact path."
        )

    def test_output_file_is_not_empty(self):
        """Verify output file has content."""
        assert os.path.exists(OUTPUT_FILE), f"Output file not found at {OUTPUT_FILE}"
        file_size = os.path.getsize(OUTPUT_FILE)
        assert file_size > 0, "Output file is empty"

    def test_output_is_valid_json(self):
        """Verify output is valid JSON format."""
        assert os.path.exists(OUTPUT_FILE), f"Output file not found at {OUTPUT_FILE}"
        with open(OUTPUT_FILE, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                pytest.fail(f"Output file is not valid JSON: {e}")
        assert data is not None


class TestOutputSchema:
    """Tests for verifying the output JSON schema matches requirements."""

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        if not os.path.exists(OUTPUT_FILE):
            pytest.skip(f"Output file not found at {OUTPUT_FILE}")
        with open(OUTPUT_FILE, "r") as f:
            return json.load(f)

    def test_has_source_repo_field(self, output_data):
        """Verify source_repo field exists."""
        assert "source_repo" in output_data, (
            "Missing required field 'source_repo'. "
            "Output must include the GitHub repository identifier extracted from the HTML file."
        )

    def test_has_match_key_field(self, output_data):
        """Verify match_key field exists."""
        assert "match_key" in output_data, (
            "Missing required field 'match_key'. "
            "Output must specify which field was used to match countries between datasets."
        )

    def test_has_country_id_field(self, output_data):
        """Verify country_id field exists."""
        assert "country_id" in output_data, (
            "Missing required field 'country_id'. "
            "Output must include the identifier of the country with the largest boundary change."
        )

    def test_has_country_name_field(self, output_data):
        """Verify country_name field exists."""
        assert "country_name" in output_data, (
            "Missing required field 'country_name'. "
            "Output must include the name of the country with the largest boundary change."
        )

    def test_has_sym_diff_area_km2_field(self, output_data):
        """Verify sym_diff_area_km2 field exists."""
        assert "sym_diff_area_km2" in output_data, (
            "Missing required field 'sym_diff_area_km2'. "
            "Output must include the symmetric difference area in square kilometers."
        )

    def test_no_extra_fields(self, output_data):
        """Verify output contains exactly the required fields."""
        required_fields = {"source_repo", "match_key", "country_id", "country_name", "sym_diff_area_km2"}
        actual_fields = set(output_data.keys())
        extra_fields = actual_fields - required_fields
        assert not extra_fields, (
            f"Output contains unexpected extra fields: {extra_fields}. "
            "Output should contain exactly: source_repo, match_key, country_id, country_name, sym_diff_area_km2"
        )


class TestSourceRepoField:
    """Tests for the source_repo field content and format."""

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        if not os.path.exists(OUTPUT_FILE):
            pytest.skip(f"Output file not found at {OUTPUT_FILE}")
        with open(OUTPUT_FILE, "r") as f:
            return json.load(f)

    def test_source_repo_is_string(self, output_data):
        """Verify source_repo is a string."""
        source_repo = output_data.get("source_repo")
        assert isinstance(source_repo, str), (
            f"source_repo must be a string, got {type(source_repo).__name__}"
        )

    def test_source_repo_format_owner_repo(self, output_data):
        """Verify source_repo follows OWNER/REPO format."""
        source_repo = output_data.get("source_repo", "")
        # Should match pattern like "owner/repo" or "owner-name/repo-name"
        pattern = r"^[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+$"
        assert re.match(pattern, source_repo), (
            f"source_repo '{source_repo}' does not follow OWNER/REPO format. "
            "Expected format like 'datasets/geo-countries'"
        )

    def test_source_repo_matches_html_content(self, output_data):
        """Verify source_repo was correctly extracted from the HTML file."""
        source_repo = output_data.get("source_repo", "")
        # The HTML file title contains: "GitHub - datasets/geo-countries: Country polygons..."
        assert source_repo == "datasets/geo-countries", (
            f"source_repo should be 'datasets/geo-countries' (extracted from HTML file), "
            f"but got '{source_repo}'"
        )


class TestMatchKeyField:
    """Tests for the match_key field content and validity."""

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        if not os.path.exists(OUTPUT_FILE):
            pytest.skip(f"Output file not found at {OUTPUT_FILE}")
        with open(OUTPUT_FILE, "r") as f:
            return json.load(f)

    def test_match_key_is_string(self, output_data):
        """Verify match_key is a string."""
        match_key = output_data.get("match_key")
        assert isinstance(match_key, str), (
            f"match_key must be a string, got {type(match_key).__name__}"
        )

    def test_match_key_is_not_empty(self, output_data):
        """Verify match_key is not empty."""
        match_key = output_data.get("match_key", "")
        assert match_key.strip(), "match_key cannot be empty"

    def test_match_key_is_valid_field_name(self, output_data):
        """Verify match_key is a plausible field name (alphanumeric with underscores)."""
        match_key = output_data.get("match_key", "")
        # Field names typically use alphanumeric characters and underscores
        pattern = r"^[a-zA-Z_][a-zA-Z0-9_]*$"
        assert re.match(pattern, match_key), (
            f"match_key '{match_key}' is not a valid field name format"
        )

    def test_match_key_is_reasonable_for_country_matching(self, output_data):
        """Verify match_key is a sensible choice for country matching."""
        match_key = output_data.get("match_key", "").lower()
        # The task suggests ISO_A3 or similar identifiers
        reasonable_keys = [
            "iso_a3", "iso_a2", "id", "adm0_a3", "sov_a3", "gu_a3",
            "su_a3", "brk_a3", "wb_a3", "un_a3", "iso_n3"
        ]
        is_reasonable = any(key in match_key for key in reasonable_keys)
        assert is_reasonable, (
            f"match_key '{output_data.get('match_key')}' does not appear to be a "
            "standard country identifier field. Expected something like ISO_A3, id, etc."
        )


class TestCountryIdField:
    """Tests for the country_id field content and validity."""

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        if not os.path.exists(OUTPUT_FILE):
            pytest.skip(f"Output file not found at {OUTPUT_FILE}")
        with open(OUTPUT_FILE, "r") as f:
            return json.load(f)

    def test_country_id_is_string(self, output_data):
        """Verify country_id is a string."""
        country_id = output_data.get("country_id")
        assert isinstance(country_id, str), (
            f"country_id must be a string, got {type(country_id).__name__}"
        )

    def test_country_id_is_not_empty(self, output_data):
        """Verify country_id is not empty."""
        country_id = output_data.get("country_id", "")
        assert country_id.strip(), "country_id cannot be empty"

    def test_country_id_exists_in_input_data(self, output_data):
        """Verify country_id exists in at least one of the input GeoJSON files."""
        country_id = output_data.get("country_id", "")
        match_key = output_data.get("match_key", "")

        found_in_geo_json = False
        found_in_geojson = False

        # Check countries.geo.json (uses 'id' field at feature level)
        if os.path.exists(INPUT_GEO_JSON):
            with open(INPUT_GEO_JSON, "r") as f:
                data = json.load(f)
                for feature in data.get("features", []):
                    if feature.get("id") == country_id:
                        found_in_geo_json = True
                        break
                    props = feature.get("properties", {})
                    if props.get(match_key) == country_id or props.get("name") == country_id:
                        found_in_geo_json = True
                        break

        # Check countries.geojson (uses properties for matching)
        if os.path.exists(INPUT_GEOJSON):
            with open(INPUT_GEOJSON, "r") as f:
                data = json.load(f)
                for feature in data.get("features", []):
                    props = feature.get("properties", {})
                    if props.get(match_key) == country_id:
                        found_in_geojson = True
                        break
                    # Also check common ID fields
                    for field in ["iso_a3", "adm0_a3", "sov_a3"]:
                        if props.get(field) == country_id:
                            found_in_geojson = True
                            break

        assert found_in_geo_json or found_in_geojson, (
            f"country_id '{country_id}' was not found in either input GeoJSON file. "
            "The result should identify a country that exists in the input data."
        )


class TestCountryNameField:
    """Tests for the country_name field content."""

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        if not os.path.exists(OUTPUT_FILE):
            pytest.skip(f"Output file not found at {OUTPUT_FILE}")
        with open(OUTPUT_FILE, "r") as f:
            return json.load(f)

    def test_country_name_is_string(self, output_data):
        """Verify country_name is a string."""
        country_name = output_data.get("country_name")
        assert isinstance(country_name, str), (
            f"country_name must be a string, got {type(country_name).__name__}"
        )

    def test_country_name_is_not_empty(self, output_data):
        """Verify country_name is not empty."""
        country_name = output_data.get("country_name", "")
        assert country_name.strip(), "country_name cannot be empty"

    def test_country_name_is_reasonable_length(self, output_data):
        """Verify country_name has a reasonable length for a country name."""
        country_name = output_data.get("country_name", "")
        assert 2 <= len(country_name) <= 100, (
            f"country_name '{country_name}' has unexpected length {len(country_name)}. "
            "Country names are typically 2-100 characters."
        )

    def test_country_name_exists_in_input_data(self, output_data):
        """Verify country_name exists in at least one of the input GeoJSON files."""
        country_name = output_data.get("country_name", "")

        found = False

        # Check both files for the country name
        for input_file in [INPUT_GEO_JSON, INPUT_GEOJSON]:
            if os.path.exists(input_file):
                with open(input_file, "r") as f:
                    data = json.load(f)
                    for feature in data.get("features", []):
                        props = feature.get("properties", {})
                        # Check various name fields
                        for name_field in ["name", "NAME", "name_long", "admin", "sovereignt"]:
                            if props.get(name_field) == country_name:
                                found = True
                                break
                        if found:
                            break
            if found:
                break

        assert found, (
            f"country_name '{country_name}' was not found in the input GeoJSON files. "
            "The result should include a country name from the source data."
        )


class TestSymDiffAreaField:
    """Tests for the sym_diff_area_km2 field content and validity."""

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        if not os.path.exists(OUTPUT_FILE):
            pytest.skip(f"Output file not found at {OUTPUT_FILE}")
        with open(OUTPUT_FILE, "r") as f:
            return json.load(f)

    def test_sym_diff_area_is_numeric(self, output_data):
        """Verify sym_diff_area_km2 is a number."""
        area = output_data.get("sym_diff_area_km2")
        assert isinstance(area, (int, float)), (
            f"sym_diff_area_km2 must be a number, got {type(area).__name__}"
        )

    def test_sym_diff_area_is_not_nan(self, output_data):
        """Verify sym_diff_area_km2 is not NaN."""
        import math
        area = output_data.get("sym_diff_area_km2")
        if isinstance(area, float):
            assert not math.isnan(area), "sym_diff_area_km2 cannot be NaN"

    def test_sym_diff_area_is_not_infinite(self, output_data):
        """Verify sym_diff_area_km2 is not infinite."""
        import math
        area = output_data.get("sym_diff_area_km2")
        if isinstance(area, float):
            assert not math.isinf(area), "sym_diff_area_km2 cannot be infinite"

    def test_sym_diff_area_is_positive(self, output_data):
        """Verify sym_diff_area_km2 is positive (there must be some difference)."""
        area = output_data.get("sym_diff_area_km2", 0)
        assert area > 0, (
            f"sym_diff_area_km2 must be positive (got {area}). "
            "The largest boundary change should have a non-zero symmetric difference area."
        )

    def test_sym_diff_area_is_reasonable(self, output_data):
        """Verify sym_diff_area_km2 is within reasonable bounds for geographic changes."""
        area = output_data.get("sym_diff_area_km2", 0)
        # The largest country (Russia) is ~17 million km2
        # A reasonable symmetric difference for boundary changes would be
        # much smaller than a full country, but could still be substantial
        # Max reasonable value: smaller than Earth's land area (~150 million km2)
        assert area < 150_000_000, (
            f"sym_diff_area_km2 ({area}) exceeds Earth's total land area. "
            "This suggests a calculation error."
        )
        # Minimum: should be at least some measurable difference
        # Even tiny boundary changes should be > 0.0001 km2 (100 m2)
        assert area >= 0.0001, (
            f"sym_diff_area_km2 ({area}) is suspiciously small. "
            "Even minor boundary differences should be measurable."
        )


class TestDeterminism:
    """Tests to verify the result is deterministic and unique."""

    @pytest.fixture
    def output_data(self):
        """Load the output JSON data."""
        if not os.path.exists(OUTPUT_FILE):
            pytest.skip(f"Output file not found at {OUTPUT_FILE}")
        with open(OUTPUT_FILE, "r") as f:
            return json.load(f)

    def test_single_country_result(self, output_data):
        """Verify the output identifies exactly one country."""
        # The output should be a single object, not a list
        assert isinstance(output_data, dict), (
            "Output should be a single JSON object identifying one country, not a list"
        )

        # Verify country_id is a single value, not a list
        country_id = output_data.get("country_id")
        assert not isinstance(country_id, (list, dict)), (
            "country_id should identify a single country, not multiple"
        )

    def test_country_id_and_name_consistent(self, output_data):
        """Verify country_id and country_name refer to the same country."""
        country_id = output_data.get("country_id", "")
        country_name = output_data.get("country_name", "")

        # Check in input files that the ID corresponds to the name
        matched = False

        for input_file in [INPUT_GEO_JSON, INPUT_GEOJSON]:
            if not os.path.exists(input_file):
                continue
            with open(input_file, "r") as f:
                data = json.load(f)
                for feature in data.get("features", []):
                    props = feature.get("properties", {})
                    feature_id = feature.get("id")

                    # Check if this feature matches the country_id
                    id_match = (
                        feature_id == country_id or
                        props.get("iso_a3") == country_id or
                        props.get("adm0_a3") == country_id or
                        props.get("sov_a3") == country_id
                    )

                    if id_match:
                        # Verify the name matches
                        feature_name = props.get("name", props.get("NAME", ""))
                        if feature_name == country_name:
                            matched = True
                            break
                if matched:
                    break

        assert matched, (
            f"country_id '{country_id}' and country_name '{country_name}' "
            "do not appear to refer to the same country in the input data."
        )


class TestInputFilesUsed:
    """Tests to verify all three input files were properly used."""

    def test_input_files_exist(self):
        """Verify all required input files exist."""
        assert os.path.exists(INPUT_GEO_JSON), f"Input file missing: {INPUT_GEO_JSON}"
        assert os.path.exists(INPUT_GEOJSON), f"Input file missing: {INPUT_GEOJSON}"
        assert os.path.exists(INPUT_HTML), f"Input file missing: {INPUT_HTML}"

    def test_both_geojson_files_are_valid(self):
        """Verify both GeoJSON input files are valid."""
        for input_file in [INPUT_GEO_JSON, INPUT_GEOJSON]:
            with open(input_file, "r") as f:
                try:
                    data = json.load(f)
                    assert "type" in data, f"{input_file} missing 'type' field"
                    assert "features" in data, f"{input_file} missing 'features' field"
                    assert data["type"] == "FeatureCollection", (
                        f"{input_file} is not a FeatureCollection"
                    )
                except json.JSONDecodeError as e:
                    pytest.fail(f"{input_file} is not valid JSON: {e}")

    def test_html_file_contains_repo_info(self):
        """Verify HTML file contains the expected repository information."""
        with open(INPUT_HTML, "r") as f:
            content = f.read()
        assert "datasets/geo-countries" in content, (
            "HTML file does not contain expected repository identifier 'datasets/geo-countries'"
        )

HEREDOC_EOF

# Execute command
python3 -m py_compile expectation_tests.py && echo "Syntax OK"

# Execute command
python3 -m pytest expectation_tests.py --collect-only -q 2>/dev/null | head -40

# Execute command
python3 -m pytest expectation_tests.py --collect-only 2>&1 | head -60

# Execute command
pip install pytest -q && python3 -m pytest expectation_tests.py --collect-only 2>&1 | head -60

# Execute command
ls -la /root/output 2>/dev/null || mkdir -p /root/output && echo "Output directory ready"

# Execute command
head -200 /root/geo-countries | grep -E "(datasets/geo-countries|owner|repo)" | head -20

# Execute command
head -10 /root/countries.geojson

# Execute command
head -10 /root/countries.geo.json

# Create /root/analyze_boundary_changes.py
mkdir -p $(dirname /root/analyze_boundary_changes.py)
cat << 'HEREDOC_EOF' > /root/analyze_boundary_changes.py
#!/usr/bin/env python3
"""
Analyze boundary changes between two GeoJSON datasets.
Identifies the country with the largest symmetric difference in boundaries.
"""

import geopandas as gpd
import json
import re
from pathlib import Path

# File paths
INPUT_DIR = Path("/root")
OUTPUT_DIR = Path("/root")
OUTPUT_FILE = OUTPUT_DIR / "largest_boundary_change.json"

# Step 1: Load both GeoJSON datasets
print("Step 1: Loading GeoJSON datasets...")
g1 = gpd.read_file(INPUT_DIR / "countries.geojson")
g2 = gpd.read_file(INPUT_DIR / "countries.geo.json")
print(f"  Dataset 1 (countries.geojson): {len(g1)} features")
print(f"  Dataset 2 (countries.geo.json): {len(g2)} features")

# Step 2: Extract source_repo from the saved GitHub HTML
print("\nStep 2: Extracting source_repo from HTML...")
html_path = INPUT_DIR / "geo-countries"
with open(html_path, "r", encoding="utf-8") as f:
    html_content = f.read()

# Search for the repo pattern in the HTML
repo_patterns = [
    r'datasets/geo-countries',  # Most likely pattern
    r'github\.com/([^/"]+/[^/"]+)',  # General GitHub repo pattern
]

source_repo = None
for pattern in repo_patterns:
    match = re.search(pattern, html_content)
    if match:
        source_repo = match.group(0) if "/" in match.group(0) else match.group(1)
        if source_repo.startswith("github.com/"):
            source_repo = source_repo.replace("github.com/", "")
        break

# Clean up the source_repo
if source_repo and source_repo == "datasets/geo-countries":
    pass  # Already correct
elif "datasets/geo-countries" in html_content:
    source_repo = "datasets/geo-countries"

print(f"  source_repo: {source_repo}")

# Step 3: Choose a match key and build a one-to-one matched table
print("\nStep 3: Finding common match key...")

# Examine columns in both datasets
print(f"  Dataset 1 columns: {list(g1.columns)[:15]}...")
print(f"  Dataset 2 columns: {list(g2.columns)}")

# For g1 (countries.geojson): use iso_a3 field
# For g2 (countries.geo.json): the 'id' field at feature level contains ISO_A3 codes
#   GeoJSON Feature IDs get loaded into index or special handling

# Check if g2 has an 'id' column (GeoJSON feature ids get handled differently)
if 'id' in g2.columns:
    print("  Dataset 2 has 'id' column")
else:
    # Try reading with fiona to get feature IDs
    import fiona
    with fiona.open(INPUT_DIR / "countries.geo.json") as src:
        feature_ids = [f['id'] for f in src if 'id' in f]
    if feature_ids:
        g2['feature_id'] = feature_ids
        print(f"  Added feature_id column to dataset 2: {len(feature_ids)} IDs")

# Determine the match key
# Dataset 1 uses 'iso_a3' for ISO-3166-1 alpha-3 codes
# Dataset 2 uses feature 'id' or 'feature_id'

match_key_g1 = 'iso_a3'
match_key_g2 = 'feature_id' if 'feature_id' in g2.columns else 'id'

print(f"  Match key for dataset 1: {match_key_g1}")
print(f"  Match key for dataset 2: {match_key_g2}")

# Filter out missing geometries and missing match keys
g1v = g1[g1.geometry.notna() & g1[match_key_g1].notna()].copy()
g2v = g2[g2.geometry.notna() & g2[match_key_g2].notna()].copy()

print(f"  After filtering: g1 has {len(g1v)} features, g2 has {len(g2v)} features")

# Enforce uniqueness: count occurrences and keep only unique keys
g1_key_counts = g1v[match_key_g1].value_counts()
g2_key_counts = g2v[match_key_g2].value_counts()

g1_unique_keys = set(g1_key_counts[g1_key_counts == 1].index)
g2_unique_keys = set(g2_key_counts[g2_key_counts == 1].index)

# Filter to unique keys
g1u = g1v[g1v[match_key_g1].isin(g1_unique_keys)].copy()
g2u = g2v[g2v[match_key_g2].isin(g2_unique_keys)].copy()

print(f"  After uniqueness filter: g1 has {len(g1u)} features, g2 has {len(g2u)} features")

# Create common match key column in both
g1u['match_id'] = g1u[match_key_g1]
g2u['match_id'] = g2u[match_key_g2]

# Find common keys
common_keys = set(g1u['match_id']) & set(g2u['match_id'])
print(f"  Common matched keys: {len(common_keys)}")

# Filter to only common keys
g1_matched = g1u[g1u['match_id'].isin(common_keys)].copy()
g2_matched = g2u[g2u['match_id'].isin(common_keys)].copy()

# Step 4: Reproject to metric CRS for area
print("\nStep 4: Reprojecting to EPSG:4087 (metric CRS)...")
METRIC_CRS = "EPSG:4087"
g1_proj = g1_matched.to_crs(METRIC_CRS)
g2_proj = g2_matched.to_crs(METRIC_CRS)
print(f"  Reprojected both datasets to {METRIC_CRS}")

# Step 5: Compute symmetric difference area per matched country
print("\nStep 5: Computing symmetric difference areas...")

# Set index for easy lookup
g1_proj = g1_proj.set_index('match_id')
g2_proj = g2_proj.set_index('match_id')

results = []
errors = []

for match_id in common_keys:
    try:
        geom1 = g1_proj.loc[match_id, 'geometry']
        geom2 = g2_proj.loc[match_id, 'geometry']

        # Compute symmetric difference
        sym_diff = geom1.symmetric_difference(geom2)
        area_m2 = sym_diff.area
        area_km2 = area_m2 / 1_000_000.0

        # Get country name from g1 (original dataset)
        if 'admin' in g1_proj.columns:
            country_name = g1_proj.loc[match_id, 'admin']
        elif 'name' in g1_proj.columns:
            country_name = g1_proj.loc[match_id, 'name']
        else:
            country_name = match_id

        results.append({
            'match_id': match_id,
            'country_name': country_name,
            'sym_diff_area_km2': area_km2
        })
    except Exception as e:
        errors.append((match_id, str(e)))

print(f"  Computed areas for {len(results)} countries")
if errors:
    print(f"  Errors for {len(errors)} countries: {errors[:5]}...")

# Step 6: Select the single deterministic winner
print("\nStep 6: Finding country with maximum boundary change...")

# Sort by sym_diff_area_km2 descending, then match_id ascending (for tie-breaking)
results_sorted = sorted(results, key=lambda x: (-x['sym_diff_area_km2'], x['match_id']))

if not results_sorted:
    raise ValueError("No results to process!")

winner = results_sorted[0]
print(f"  Winner: {winner['match_id']} ({winner['country_name']})")
print(f"  Symmetric difference area: {winner['sym_diff_area_km2']:.4f} km²")

# Check for ties
ties = [r for r in results_sorted if r['sym_diff_area_km2'] == winner['sym_diff_area_km2']]
if len(ties) > 1:
    print(f"  Note: {len(ties)} countries tied at max area, selected {winner['match_id']} (lexicographically smallest)")

# Step 7: Write the required JSON output file
print("\nStep 7: Writing output JSON file...")

output_data = {
    "source_repo": source_repo,
    "match_key": match_key_g1,  # The field used for matching
    "country_id": winner['match_id'],
    "country_name": winner['country_name'],
    "sym_diff_area_km2": float(winner['sym_diff_area_km2'])
}

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
with open(OUTPUT_FILE, 'w') as f:
    json.dump(output_data, f, indent=2)

print(f"  Output written to: {OUTPUT_FILE}")
print("\nFinal output:")
print(json.dumps(output_data, indent=2))

HEREDOC_EOF

# Execute command
python3 analyze_boundary_changes.py 2>&1

