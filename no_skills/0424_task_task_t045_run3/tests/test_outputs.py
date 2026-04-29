import json
import math
import os

import pytest


class TestSiO2PolymorphFingerprint:
    """Tests for verifying the SiO2 polymorph fingerprint JSON output."""

    OUTPUT_FILE = "/root/output/sio2_polymorph_fingerprint.json"
    TOLERANCE = 1e-5

    EXPECTED_REFERENCE = {
        "material_id": "mp-6930",
        "crystal_system": "Trigonal",
        "spacegroup_symbol": "P3_221",
        "spacegroup_number": 154
    }

    EXPECTED_QUARTZ = {
        "file": "SiO2-Quartz-alpha.cif",
        "spacegroup_symbol": "P3_221",
        "spacegroup_number": 154,
        "crystal_system": "trigonal",
        "volume": 112.93267,
        "density": 2.650402,
        "mean_si_o_bond": 1.608171,
        "peak_count": 22,
        "max_intensity_2theta": 26.668243,
        "factor_score_1d": 5.0
    }

    EXPECTED_CRISTOBALITE = {
        "file": "SiO2-Cristobalite.cif",
        "spacegroup_symbol": "P4_12_12",
        "spacegroup_number": 92,
        "crystal_system": "tetragonal",
        "volume": 171.104033,
        "density": 2.332437,
        "mean_si_o_bond": 1.602977,
        "peak_count": 41,
        "max_intensity_2theta": 22.011862,
        "factor_score_1d": -5.0
    }

    EXPECTED_FACTOR_ANALYSIS = {
        "n_factors": 1,
        "rotation": None,
        "eigenvalues": [5.0, 0.0, 0.0, 0.0, 0.0],
        "pca_separation": 10.0
    }

    EXPECTED_MP6930_MATCH = "SiO2-Quartz-alpha.cif"

    # ==================== STRUCTURAL TESTS ====================

    def test_output_file_exists(self):
        """Verify the output JSON file was created."""
        assert os.path.exists(self.OUTPUT_FILE), \
            f"Output file not found: {self.OUTPUT_FILE}"

    def test_valid_json_format(self):
        """Verify the output is valid JSON."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)
        assert isinstance(data, dict), "Output should be a JSON object"

    def test_top_level_keys_exist(self):
        """Verify all required top-level keys are present."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        required_keys = ["reference_from_html", "structures", "mp6930_match_file", "factor_analysis"]
        for key in required_keys:
            assert key in data, f"Missing required top-level key: {key}"

    def test_no_extra_top_level_keys(self):
        """Verify no extra keys beyond the required schema."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        expected_keys = {"reference_from_html", "structures", "mp6930_match_file", "factor_analysis"}
        actual_keys = set(data.keys())
        extra_keys = actual_keys - expected_keys
        assert not extra_keys, f"Found unexpected top-level keys: {extra_keys}"

    # ==================== REFERENCE FROM HTML TESTS ====================

    def test_reference_has_required_fields(self):
        """Verify reference_from_html has all required fields."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        ref = data["reference_from_html"]
        required_fields = ["material_id", "crystal_system", "spacegroup_symbol", "spacegroup_number"]
        for field in required_fields:
            assert field in ref, f"Missing field in reference_from_html: {field}"

    def test_reference_material_id(self):
        """Verify reference material_id is mp-6930."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        assert data["reference_from_html"]["material_id"] == self.EXPECTED_REFERENCE["material_id"], \
            f"Expected material_id '{self.EXPECTED_REFERENCE['material_id']}', got '{data['reference_from_html']['material_id']}'"

    def test_reference_crystal_system(self):
        """Verify reference crystal system is Trigonal."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        assert data["reference_from_html"]["crystal_system"] == self.EXPECTED_REFERENCE["crystal_system"], \
            f"Expected crystal_system '{self.EXPECTED_REFERENCE['crystal_system']}', got '{data['reference_from_html']['crystal_system']}'"

    def test_reference_spacegroup_symbol(self):
        """Verify reference spacegroup symbol is P3_221."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        assert data["reference_from_html"]["spacegroup_symbol"] == self.EXPECTED_REFERENCE["spacegroup_symbol"], \
            f"Expected spacegroup_symbol '{self.EXPECTED_REFERENCE['spacegroup_symbol']}', got '{data['reference_from_html']['spacegroup_symbol']}'"

    def test_reference_spacegroup_number(self):
        """Verify reference spacegroup number is 154."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        assert data["reference_from_html"]["spacegroup_number"] == self.EXPECTED_REFERENCE["spacegroup_number"], \
            f"Expected spacegroup_number {self.EXPECTED_REFERENCE['spacegroup_number']}, got {data['reference_from_html']['spacegroup_number']}"

    def test_reference_spacegroup_number_is_integer(self):
        """Verify spacegroup_number is an integer type."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        assert isinstance(data["reference_from_html"]["spacegroup_number"], int), \
            f"spacegroup_number should be int, got {type(data['reference_from_html']['spacegroup_number']).__name__}"

    # ==================== STRUCTURES ARRAY TESTS ====================

    def test_structures_is_array(self):
        """Verify structures is a list."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        assert isinstance(data["structures"], list), "structures should be a list"

    def test_structures_has_two_entries(self):
        """Verify structures array has exactly 2 entries."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        assert len(data["structures"]) == 2, \
            f"Expected 2 structures, got {len(data['structures'])}"

    def test_structures_order_quartz_first(self):
        """Verify Quartz-alpha is first in the structures array."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        assert data["structures"][0]["file"] == "SiO2-Quartz-alpha.cif", \
            f"First structure should be Quartz-alpha, got {data['structures'][0]['file']}"

    def test_structures_order_cristobalite_second(self):
        """Verify Cristobalite is second in the structures array."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        assert data["structures"][1]["file"] == "SiO2-Cristobalite.cif", \
            f"Second structure should be Cristobalite, got {data['structures'][1]['file']}"

    def test_structure_has_required_fields(self):
        """Verify each structure has all required fields."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        required_fields = [
            "file", "spacegroup_symbol", "spacegroup_number", "crystal_system",
            "volume", "density", "mean_si_o_bond", "peak_count",
            "max_intensity_2theta", "factor_score_1d"
        ]

        for i, struct in enumerate(data["structures"]):
            for field in required_fields:
                assert field in struct, f"Missing field '{field}' in structure {i}"

    # ==================== QUARTZ VALUES TESTS ====================

    def test_quartz_spacegroup_symbol(self):
        """Verify Quartz spacegroup symbol."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        quartz = data["structures"][0]
        assert quartz["spacegroup_symbol"] == self.EXPECTED_QUARTZ["spacegroup_symbol"], \
            f"Quartz spacegroup_symbol mismatch"

    def test_quartz_spacegroup_number(self):
        """Verify Quartz spacegroup number is 154."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        quartz = data["structures"][0]
        assert quartz["spacegroup_number"] == self.EXPECTED_QUARTZ["spacegroup_number"], \
            f"Expected Quartz spacegroup_number {self.EXPECTED_QUARTZ['spacegroup_number']}, got {quartz['spacegroup_number']}"

    def test_quartz_crystal_system(self):
        """Verify Quartz crystal system is trigonal."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        quartz = data["structures"][0]
        assert quartz["crystal_system"].lower() == self.EXPECTED_QUARTZ["crystal_system"].lower(), \
            f"Quartz crystal_system mismatch"

    def test_quartz_volume(self):
        """Verify Quartz volume value."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        quartz = data["structures"][0]
        assert math.isclose(quartz["volume"], self.EXPECTED_QUARTZ["volume"], rel_tol=self.TOLERANCE), \
            f"Quartz volume mismatch: expected {self.EXPECTED_QUARTZ['volume']}, got {quartz['volume']}"

    def test_quartz_density(self):
        """Verify Quartz density value."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        quartz = data["structures"][0]
        assert math.isclose(quartz["density"], self.EXPECTED_QUARTZ["density"], rel_tol=self.TOLERANCE), \
            f"Quartz density mismatch: expected {self.EXPECTED_QUARTZ['density']}, got {quartz['density']}"

    def test_quartz_mean_si_o_bond(self):
        """Verify Quartz mean Si-O bond length."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        quartz = data["structures"][0]
        assert math.isclose(quartz["mean_si_o_bond"], self.EXPECTED_QUARTZ["mean_si_o_bond"], rel_tol=self.TOLERANCE), \
            f"Quartz mean_si_o_bond mismatch: expected {self.EXPECTED_QUARTZ['mean_si_o_bond']}, got {quartz['mean_si_o_bond']}"

    def test_quartz_peak_count(self):
        """Verify Quartz XRD peak count."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        quartz = data["structures"][0]
        assert quartz["peak_count"] == self.EXPECTED_QUARTZ["peak_count"], \
            f"Quartz peak_count mismatch: expected {self.EXPECTED_QUARTZ['peak_count']}, got {quartz['peak_count']}"

    def test_quartz_peak_count_is_integer(self):
        """Verify Quartz peak_count is an integer type."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        quartz = data["structures"][0]
        assert isinstance(quartz["peak_count"], int), \
            f"peak_count should be int, got {type(quartz['peak_count']).__name__}"

    def test_quartz_max_intensity_2theta(self):
        """Verify Quartz max intensity 2theta value."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        quartz = data["structures"][0]
        assert math.isclose(quartz["max_intensity_2theta"], self.EXPECTED_QUARTZ["max_intensity_2theta"], rel_tol=self.TOLERANCE), \
            f"Quartz max_intensity_2theta mismatch: expected {self.EXPECTED_QUARTZ['max_intensity_2theta']}, got {quartz['max_intensity_2theta']}"

    def test_quartz_factor_score(self):
        """Verify Quartz 1D factor score."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        quartz = data["structures"][0]
        assert math.isclose(quartz["factor_score_1d"], self.EXPECTED_QUARTZ["factor_score_1d"], rel_tol=self.TOLERANCE), \
            f"Quartz factor_score_1d mismatch: expected {self.EXPECTED_QUARTZ['factor_score_1d']}, got {quartz['factor_score_1d']}"

    # ==================== CRISTOBALITE VALUES TESTS ====================

    def test_cristobalite_spacegroup_symbol(self):
        """Verify Cristobalite spacegroup symbol."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        crist = data["structures"][1]
        assert crist["spacegroup_symbol"] == self.EXPECTED_CRISTOBALITE["spacegroup_symbol"], \
            f"Cristobalite spacegroup_symbol mismatch"

    def test_cristobalite_spacegroup_number(self):
        """Verify Cristobalite spacegroup number is 92."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        crist = data["structures"][1]
        assert crist["spacegroup_number"] == self.EXPECTED_CRISTOBALITE["spacegroup_number"], \
            f"Expected Cristobalite spacegroup_number {self.EXPECTED_CRISTOBALITE['spacegroup_number']}, got {crist['spacegroup_number']}"

    def test_cristobalite_crystal_system(self):
        """Verify Cristobalite crystal system is tetragonal."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        crist = data["structures"][1]
        assert crist["crystal_system"].lower() == self.EXPECTED_CRISTOBALITE["crystal_system"].lower(), \
            f"Cristobalite crystal_system mismatch"

    def test_cristobalite_volume(self):
        """Verify Cristobalite volume value."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        crist = data["structures"][1]
        assert math.isclose(crist["volume"], self.EXPECTED_CRISTOBALITE["volume"], rel_tol=self.TOLERANCE), \
            f"Cristobalite volume mismatch: expected {self.EXPECTED_CRISTOBALITE['volume']}, got {crist['volume']}"

    def test_cristobalite_density(self):
        """Verify Cristobalite density value."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        crist = data["structures"][1]
        assert math.isclose(crist["density"], self.EXPECTED_CRISTOBALITE["density"], rel_tol=self.TOLERANCE), \
            f"Cristobalite density mismatch: expected {self.EXPECTED_CRISTOBALITE['density']}, got {crist['density']}"

    def test_cristobalite_mean_si_o_bond(self):
        """Verify Cristobalite mean Si-O bond length."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        crist = data["structures"][1]
        assert math.isclose(crist["mean_si_o_bond"], self.EXPECTED_CRISTOBALITE["mean_si_o_bond"], rel_tol=self.TOLERANCE), \
            f"Cristobalite mean_si_o_bond mismatch: expected {self.EXPECTED_CRISTOBALITE['mean_si_o_bond']}, got {crist['mean_si_o_bond']}"

    def test_cristobalite_peak_count(self):
        """Verify Cristobalite XRD peak count."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        crist = data["structures"][1]
        assert crist["peak_count"] == self.EXPECTED_CRISTOBALITE["peak_count"], \
            f"Cristobalite peak_count mismatch: expected {self.EXPECTED_CRISTOBALITE['peak_count']}, got {crist['peak_count']}"

    def test_cristobalite_max_intensity_2theta(self):
        """Verify Cristobalite max intensity 2theta value."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        crist = data["structures"][1]
        assert math.isclose(crist["max_intensity_2theta"], self.EXPECTED_CRISTOBALITE["max_intensity_2theta"], rel_tol=self.TOLERANCE), \
            f"Cristobalite max_intensity_2theta mismatch: expected {self.EXPECTED_CRISTOBALITE['max_intensity_2theta']}, got {crist['max_intensity_2theta']}"

    def test_cristobalite_factor_score(self):
        """Verify Cristobalite 1D factor score."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        crist = data["structures"][1]
        assert math.isclose(crist["factor_score_1d"], self.EXPECTED_CRISTOBALITE["factor_score_1d"], rel_tol=self.TOLERANCE), \
            f"Cristobalite factor_score_1d mismatch: expected {self.EXPECTED_CRISTOBALITE['factor_score_1d']}, got {crist['factor_score_1d']}"

    # ==================== MP6930 MATCH TESTS ====================

    def test_mp6930_match_file(self):
        """Verify the correct CIF file is identified as mp-6930 match."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        assert data["mp6930_match_file"] == self.EXPECTED_MP6930_MATCH, \
            f"mp6930_match_file mismatch: expected '{self.EXPECTED_MP6930_MATCH}', got '{data['mp6930_match_file']}'"

    def test_mp6930_match_is_quartz(self):
        """Verify that mp6930 matches Quartz-alpha (space group 154, P3_221)."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        match_file = data["mp6930_match_file"]
        assert "Quartz" in match_file, \
            f"mp6930 should match Quartz, got '{match_file}'"

    # ==================== FACTOR ANALYSIS TESTS ====================

    def test_factor_analysis_has_required_fields(self):
        """Verify factor_analysis has all required fields."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        fa = data["factor_analysis"]
        required_fields = ["n_factors", "rotation", "eigenvalues", "pca_separation"]
        for field in required_fields:
            assert field in fa, f"Missing field in factor_analysis: {field}"

    def test_factor_analysis_n_factors(self):
        """Verify n_factors is 1."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        assert data["factor_analysis"]["n_factors"] == self.EXPECTED_FACTOR_ANALYSIS["n_factors"], \
            f"n_factors mismatch: expected {self.EXPECTED_FACTOR_ANALYSIS['n_factors']}, got {data['factor_analysis']['n_factors']}"

    def test_factor_analysis_rotation_is_null(self):
        """Verify rotation is null (None)."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        assert data["factor_analysis"]["rotation"] is None, \
            f"rotation should be null, got {data['factor_analysis']['rotation']}"

    def test_eigenvalues_is_list(self):
        """Verify eigenvalues is a list."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        assert isinstance(data["factor_analysis"]["eigenvalues"], list), \
            "eigenvalues should be a list"

    def test_eigenvalues_has_five_elements(self):
        """Verify eigenvalues list has exactly 5 elements (one per feature)."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        eigenvalues = data["factor_analysis"]["eigenvalues"]
        assert len(eigenvalues) == 5, \
            f"Expected 5 eigenvalues, got {len(eigenvalues)}"

    def test_eigenvalues_first_value(self):
        """Verify the first eigenvalue (should be 5.0)."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        eigenvalues = data["factor_analysis"]["eigenvalues"]
        assert math.isclose(eigenvalues[0], self.EXPECTED_FACTOR_ANALYSIS["eigenvalues"][0], rel_tol=self.TOLERANCE), \
            f"First eigenvalue mismatch: expected {self.EXPECTED_FACTOR_ANALYSIS['eigenvalues'][0]}, got {eigenvalues[0]}"

    def test_eigenvalues_remaining_near_zero(self):
        """Verify remaining eigenvalues are near zero."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        eigenvalues = data["factor_analysis"]["eigenvalues"]
        for i, ev in enumerate(eigenvalues[1:], start=1):
            assert abs(ev) < 0.001, \
                f"Eigenvalue {i} should be near zero, got {ev}"

    def test_pca_separation(self):
        """Verify PCA separation value."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        assert math.isclose(data["factor_analysis"]["pca_separation"], self.EXPECTED_FACTOR_ANALYSIS["pca_separation"], rel_tol=self.TOLERANCE), \
            f"pca_separation mismatch: expected {self.EXPECTED_FACTOR_ANALYSIS['pca_separation']}, got {data['factor_analysis']['pca_separation']}"

    # ==================== CONTENT INTEGRITY TESTS ====================

    def test_floats_rounded_to_six_decimals(self):
        """Verify floating point values are rounded to 6 decimal places."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        for struct in data["structures"]:
            for field in ["volume", "density", "mean_si_o_bond", "max_intensity_2theta", "factor_score_1d"]:
                value = struct[field]
                value_str = str(value)
                if '.' in value_str:
                    decimals = len(value_str.split('.')[1])
                    assert decimals <= 6, \
                        f"{field} has {decimals} decimal places, expected at most 6"

    def test_factor_scores_opposite_signs(self):
        """Verify factor scores have opposite signs for the two polymorphs."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        score1 = data["structures"][0]["factor_score_1d"]
        score2 = data["structures"][1]["factor_score_1d"]

        assert (score1 > 0 and score2 < 0) or (score1 < 0 and score2 > 0), \
            f"Factor scores should have opposite signs: got {score1} and {score2}"

    def test_pca_separation_equals_score_difference(self):
        """Verify pca_separation equals absolute difference of factor scores."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        score1 = data["structures"][0]["factor_score_1d"]
        score2 = data["structures"][1]["factor_score_1d"]
        expected_sep = abs(score1 - score2)

        assert math.isclose(data["factor_analysis"]["pca_separation"], expected_sep, rel_tol=self.TOLERANCE), \
            f"pca_separation should equal |score1 - score2| = {expected_sep}, got {data['factor_analysis']['pca_separation']}"

    def test_quartz_higher_density_than_cristobalite(self):
        """Verify Quartz has higher density than Cristobalite (physical reality)."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        quartz = data["structures"][0]
        crist = data["structures"][1]

        assert quartz["density"] > crist["density"], \
            f"Quartz density ({quartz['density']}) should be higher than Cristobalite ({crist['density']})"

    def test_cristobalite_larger_volume_than_quartz(self):
        """Verify Cristobalite has larger volume than Quartz."""
        with open(self.OUTPUT_FILE) as f:
            data = json.load(f)

        quartz = data["structures"][0]
        crist = data["structures"][1]

        assert crist["volume"] > quartz["volume"], \
            f"Cristobalite volume ({crist['volume']}) should be larger than Quartz ({quartz['volume']})"
