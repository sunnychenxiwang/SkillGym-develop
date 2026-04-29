import json
import math
import os

import pytest


class TestTopMarkerSummary:
    """Tests for verifying top_marker_summary.json output."""

    OUTPUT_PATH = "/root/output/top_marker_summary.json"
    TOLERANCE = 1e-6

    EXPECTED_DATASET_ORDER = [
        "pbmc3k.h5ad",
        "pbmc3k_2.h5ad",
        "pbmc_10k_protein_v3.h5ad",
    ]

    EXPECTED_RESULT = {
        "pbmc3k.h5ad": {
            "groups_count": 8,
            "groups": [
                {"group": "B cells", "top_gene": "CD79A", "score": 2.779087, "is_shared_top_marker": False},
                {"group": "CD14+ Monocytes", "top_gene": "S100A9", "score": 3.064833, "is_shared_top_marker": True},
                {"group": "CD4 T cells", "top_gene": "LDHB", "score": 1.470908, "is_shared_top_marker": False},
                {"group": "CD8 T cells", "top_gene": "CCL5", "score": 2.477243, "is_shared_top_marker": True},
                {"group": "Dendritic cells", "top_gene": "FCER1A", "score": 2.121833, "is_shared_top_marker": False},
                {"group": "FCGR3A+ Monocytes", "top_gene": "FCGR3A", "score": 2.368965, "is_shared_top_marker": False},
                {"group": "Megakaryocytes", "top_gene": "PPBP", "score": 4.373156, "is_shared_top_marker": True},
                {"group": "NK cells", "top_gene": "GNLY", "score": 3.031695, "is_shared_top_marker": False},
            ],
        },
        "pbmc3k_2.h5ad": {
            "groups_count": 8,
            "groups": [
                {"group": "B cells", "top_gene": "HLA-DRA", "score": 3.106975, "is_shared_top_marker": False},
                {"group": "CD14+ Monocytes", "top_gene": "S100A9", "score": 4.078328, "is_shared_top_marker": True},
                {"group": "CD4 T cells", "top_gene": "LTB", "score": 1.455931, "is_shared_top_marker": True},
                {"group": "CD8 T cells", "top_gene": "CCL5", "score": 2.871519, "is_shared_top_marker": True},
                {"group": "Dendritic cells", "top_gene": "CST3", "score": 3.047186, "is_shared_top_marker": False},
                {"group": "FCGR3A+ Monocytes", "top_gene": "LST1", "score": 3.024407, "is_shared_top_marker": False},
                {"group": "Megakaryocytes", "top_gene": "PPBP", "score": 5.726899, "is_shared_top_marker": True},
                {"group": "NK cells", "top_gene": "NKG7", "score": 4.064911, "is_shared_top_marker": False},
            ],
        },
        "pbmc_10k_protein_v3.h5ad": {
            "groups_count": 5,
            "groups": [
                {"group": "0", "top_gene": "LTB", "score": 0.51393, "is_shared_top_marker": True},
                {"group": "1", "top_gene": "IL32", "score": 0.492689, "is_shared_top_marker": False},
                {"group": "2", "top_gene": "CCL5", "score": 0.783237, "is_shared_top_marker": True},
                {"group": "3", "top_gene": "S100A4", "score": 0.672231, "is_shared_top_marker": False},
                {"group": "4", "top_gene": "LYZ", "score": 3.495619, "is_shared_top_marker": False},
            ],
        },
    }

    # --- Structural Tests ---

    def test_output_file_exists(self):
        """Verify output file was created at expected path."""
        assert os.path.exists(self.OUTPUT_PATH), f"Output file not found at {self.OUTPUT_PATH}"

    def test_output_is_valid_json(self):
        """Verify output is valid JSON."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        assert isinstance(data, dict), "JSON root should be a dictionary"

    def test_has_datasets_key(self):
        """Verify top-level 'datasets' key exists."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        assert "datasets" in data, "Missing required top-level key: datasets"
        assert isinstance(data["datasets"], list), "datasets should be a list"

    def test_correct_number_of_datasets(self):
        """Verify exactly 3 datasets are present."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        assert len(data["datasets"]) == 3, f"Expected 3 datasets, got {len(data['datasets'])}"

    # --- Value Tests: Dataset Order ---

    def test_dataset_order(self):
        """Verify datasets are in required order: pbmc3k.h5ad, pbmc3k_2.h5ad, pbmc_10k_protein_v3.h5ad."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        actual_order = [ds["dataset_name"] for ds in data["datasets"]]
        assert actual_order == self.EXPECTED_DATASET_ORDER, (
            f"Dataset order mismatch: expected {self.EXPECTED_DATASET_ORDER}, got {actual_order}"
        )

    def test_dataset_names_are_filenames_only(self):
        """Verify dataset_name is just the filename, not full path."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        for ds in data["datasets"]:
            assert "/" not in ds["dataset_name"], (
                f"dataset_name should be filename only, got: {ds['dataset_name']}"
            )
            assert ds["dataset_name"].endswith(".h5ad"), (
                f"dataset_name should end with .h5ad, got: {ds['dataset_name']}"
            )

    # --- Content Tests: Dataset Structure ---

    def test_each_dataset_has_required_fields(self):
        """Verify each dataset has dataset_name and groups fields."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        for i, ds in enumerate(data["datasets"]):
            assert "dataset_name" in ds, f"Dataset {i} missing 'dataset_name'"
            assert "groups" in ds, f"Dataset {i} missing 'groups'"
            assert isinstance(ds["groups"], list), f"Dataset {i} 'groups' should be a list"

    def test_groups_count_per_dataset(self):
        """Verify each dataset has expected number of groups."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        for ds in data["datasets"]:
            ds_name = ds["dataset_name"]
            expected_count = self.EXPECTED_RESULT[ds_name]["groups_count"]
            actual_count = len(ds["groups"])
            assert actual_count == expected_count, (
                f"{ds_name}: expected {expected_count} groups, got {actual_count}"
            )

    # --- Content Tests: Group Structure ---

    def test_each_group_has_required_fields(self):
        """Verify each group has group, top_gene, score, is_shared_top_marker fields."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        required_fields = ["group", "top_gene", "score", "is_shared_top_marker"]
        for ds in data["datasets"]:
            for g in ds["groups"]:
                for field in required_fields:
                    assert field in g, (
                        f"Group in {ds['dataset_name']} missing field: {field}"
                    )

    def test_group_field_types(self):
        """Verify correct data types for group fields."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        for ds in data["datasets"]:
            for g in ds["groups"]:
                assert isinstance(g["group"], str), f"group should be string"
                assert isinstance(g["top_gene"], str), f"top_gene should be string"
                assert isinstance(g["score"], (int, float)), f"score should be numeric"
                assert isinstance(g["is_shared_top_marker"], bool), (
                    f"is_shared_top_marker should be boolean, got {type(g['is_shared_top_marker'])}"
                )

    def test_groups_sorted_by_group_name(self):
        """Verify groups within each dataset are sorted by group name (string ascending)."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        for ds in data["datasets"]:
            group_names = [g["group"] for g in ds["groups"]]
            sorted_names = sorted(group_names)
            assert group_names == sorted_names, (
                f"{ds['dataset_name']}: groups not sorted. Got {group_names}, expected {sorted_names}"
            )

    def test_scores_are_valid_numbers(self):
        """Verify scores are valid numeric values (not NaN or Inf)."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        for ds in data["datasets"]:
            for g in ds["groups"]:
                assert not math.isnan(g["score"]), (
                    f"{ds['dataset_name']} group {g['group']}: score is NaN"
                )
                assert not math.isinf(g["score"]), (
                    f"{ds['dataset_name']} group {g['group']}: score is Inf"
                )

    def test_scores_rounded_to_6_decimals(self):
        """Verify scores are rounded to at most 6 decimal places."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        for ds in data["datasets"]:
            for g in ds["groups"]:
                score_str = str(g["score"])
                if "." in score_str:
                    decimals = len(score_str.split(".")[1])
                    assert decimals <= 6, (
                        f"{ds['dataset_name']} group {g['group']}: "
                        f"score has {decimals} decimals, expected <= 6"
                    )

    # --- Value Tests: Exact Values ---

    def test_pbmc3k_groups_values(self):
        """Verify pbmc3k.h5ad groups have correct values."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        ds = next(d for d in data["datasets"] if d["dataset_name"] == "pbmc3k.h5ad")
        expected = self.EXPECTED_RESULT["pbmc3k.h5ad"]["groups"]

        for exp_g in expected:
            actual_g = next((g for g in ds["groups"] if g["group"] == exp_g["group"]), None)
            assert actual_g is not None, f"Missing group: {exp_g['group']}"
            assert actual_g["top_gene"] == exp_g["top_gene"], (
                f"pbmc3k.h5ad {exp_g['group']}: expected top_gene {exp_g['top_gene']}, "
                f"got {actual_g['top_gene']}"
            )
            assert math.isclose(actual_g["score"], exp_g["score"], rel_tol=self.TOLERANCE), (
                f"pbmc3k.h5ad {exp_g['group']}: expected score {exp_g['score']}, "
                f"got {actual_g['score']}"
            )
            assert actual_g["is_shared_top_marker"] == exp_g["is_shared_top_marker"], (
                f"pbmc3k.h5ad {exp_g['group']}: expected is_shared_top_marker "
                f"{exp_g['is_shared_top_marker']}, got {actual_g['is_shared_top_marker']}"
            )

    def test_pbmc3k_2_groups_values(self):
        """Verify pbmc3k_2.h5ad groups have correct values."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        ds = next(d for d in data["datasets"] if d["dataset_name"] == "pbmc3k_2.h5ad")
        expected = self.EXPECTED_RESULT["pbmc3k_2.h5ad"]["groups"]

        for exp_g in expected:
            actual_g = next((g for g in ds["groups"] if g["group"] == exp_g["group"]), None)
            assert actual_g is not None, f"Missing group: {exp_g['group']}"
            assert actual_g["top_gene"] == exp_g["top_gene"], (
                f"pbmc3k_2.h5ad {exp_g['group']}: expected top_gene {exp_g['top_gene']}, "
                f"got {actual_g['top_gene']}"
            )
            assert math.isclose(actual_g["score"], exp_g["score"], rel_tol=self.TOLERANCE), (
                f"pbmc3k_2.h5ad {exp_g['group']}: expected score {exp_g['score']}, "
                f"got {actual_g['score']}"
            )
            assert actual_g["is_shared_top_marker"] == exp_g["is_shared_top_marker"], (
                f"pbmc3k_2.h5ad {exp_g['group']}: expected is_shared_top_marker "
                f"{exp_g['is_shared_top_marker']}, got {actual_g['is_shared_top_marker']}"
            )

    def test_pbmc_10k_groups_values(self):
        """Verify pbmc_10k_protein_v3.h5ad groups have correct values."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        ds = next(d for d in data["datasets"] if d["dataset_name"] == "pbmc_10k_protein_v3.h5ad")
        expected = self.EXPECTED_RESULT["pbmc_10k_protein_v3.h5ad"]["groups"]

        for exp_g in expected:
            actual_g = next((g for g in ds["groups"] if g["group"] == exp_g["group"]), None)
            assert actual_g is not None, f"Missing group: {exp_g['group']}"
            assert actual_g["top_gene"] == exp_g["top_gene"], (
                f"pbmc_10k_protein_v3.h5ad {exp_g['group']}: expected top_gene {exp_g['top_gene']}, "
                f"got {actual_g['top_gene']}"
            )
            assert math.isclose(actual_g["score"], exp_g["score"], rel_tol=self.TOLERANCE), (
                f"pbmc_10k_protein_v3.h5ad {exp_g['group']}: expected score {exp_g['score']}, "
                f"got {actual_g['score']}"
            )
            assert actual_g["is_shared_top_marker"] == exp_g["is_shared_top_marker"], (
                f"pbmc_10k_protein_v3.h5ad {exp_g['group']}: expected is_shared_top_marker "
                f"{exp_g['is_shared_top_marker']}, got {actual_g['is_shared_top_marker']}"
            )

    # --- Value Tests: Shared Marker Validation ---

    def test_shared_marker_logic_ccl5(self):
        """Verify CCL5 appears as top marker in all 3 datasets and is marked shared."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)

        ccl5_datasets = []
        for ds in data["datasets"]:
            for g in ds["groups"]:
                if g["top_gene"] == "CCL5":
                    ccl5_datasets.append(ds["dataset_name"])
                    assert g["is_shared_top_marker"] is True, (
                        f"CCL5 in {ds['dataset_name']} should have is_shared_top_marker=True"
                    )

        assert len(ccl5_datasets) == 3, (
            f"CCL5 should appear as top marker in all 3 datasets, found in {ccl5_datasets}"
        )

    def test_shared_marker_logic_s100a9(self):
        """Verify S100A9 appears as top marker in pbmc3k and pbmc3k_2, marked shared."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)

        s100a9_datasets = []
        for ds in data["datasets"]:
            for g in ds["groups"]:
                if g["top_gene"] == "S100A9":
                    s100a9_datasets.append(ds["dataset_name"])
                    assert g["is_shared_top_marker"] is True, (
                        f"S100A9 in {ds['dataset_name']} should have is_shared_top_marker=True"
                    )

        assert "pbmc3k.h5ad" in s100a9_datasets, "S100A9 should be top marker in pbmc3k.h5ad"
        assert "pbmc3k_2.h5ad" in s100a9_datasets, "S100A9 should be top marker in pbmc3k_2.h5ad"

    def test_shared_marker_logic_ppbp(self):
        """Verify PPBP appears as top marker in pbmc3k and pbmc3k_2, marked shared."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)

        ppbp_datasets = []
        for ds in data["datasets"]:
            for g in ds["groups"]:
                if g["top_gene"] == "PPBP":
                    ppbp_datasets.append(ds["dataset_name"])
                    assert g["is_shared_top_marker"] is True, (
                        f"PPBP in {ds['dataset_name']} should have is_shared_top_marker=True"
                    )

        assert "pbmc3k.h5ad" in ppbp_datasets, "PPBP should be top marker in pbmc3k.h5ad"
        assert "pbmc3k_2.h5ad" in ppbp_datasets, "PPBP should be top marker in pbmc3k_2.h5ad"

    def test_unshared_markers_not_flagged(self):
        """Verify genes that only appear in one dataset are not marked as shared."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)

        unique_genes = ["CD79A", "FCER1A", "FCGR3A", "GNLY", "LDHB",
                        "HLA-DRA", "CST3", "LST1", "NKG7",
                        "IL32", "S100A4", "LYZ"]

        for ds in data["datasets"]:
            for g in ds["groups"]:
                if g["top_gene"] in unique_genes:
                    assert g["is_shared_top_marker"] is False, (
                        f"{g['top_gene']} in {ds['dataset_name']} should have "
                        f"is_shared_top_marker=False (unique gene)"
                    )

    # --- Content Tests: Total Row Count ---

    def test_total_groups_count(self):
        """Verify total number of group entries across all datasets (8 + 8 + 5 = 21)."""
        with open(self.OUTPUT_PATH) as f:
            data = json.load(f)
        total = sum(len(ds["groups"]) for ds in data["datasets"])
        assert total == 21, f"Expected 21 total group entries (8+8+5), got {total}"
