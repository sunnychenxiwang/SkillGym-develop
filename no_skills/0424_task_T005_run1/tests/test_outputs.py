"""
Pytest tests for verifying the PyDESeq2 pseudo-bulk differential expression analysis output.

Task: Load three AnnData files (pbmc3k, pbmc3k_2, pbmc_10k_protein_v3), create pseudo-bulk
samples by summing counts across cells over the intersection of genes, run PyDESeq2 with
design ~dataset, extract results for contrast pbmc_10k_protein_v3 vs pbmc3k, and find the
gene with smallest adjusted p-value (ties broken by lexicographically smallest gene name).

Output schema:
{
  "gene": "GENE_NAME",
  "padj": 0.0,
  "log2FoldChange": 0.0
}
"""

import json
import math
import os
import warnings

import pytest

warnings.filterwarnings("ignore")


# =============================================================================
# Constants
# =============================================================================

OUTPUT_FILE = "/root/output/top_de_gene_pbmc10k_vs_pbmc3k.json"
INPUT_DIR = "/root"

INPUT_FILES = {
    "pbmc3k": os.path.join(INPUT_DIR, "pbmc3k.h5ad"),
    "pbmc3k_2": os.path.join(INPUT_DIR, "pbmc3k_2.h5ad"),
    "pbmc_10k_protein_v3": os.path.join(INPUT_DIR, "pbmc_10k_protein_v3.h5ad"),
}


class TestOutputs:
    """Tests for verifying task outputs."""

    EXPECTED_RESULT = {
        "gene": "MATR3",
        "padj": 9.331870807240807e-20,
        "log2FoldChange": -9.766598188716994,
    }
    TOLERANCE = 1e-6

    # =========================================================================
    # Structural Tests
    # =========================================================================

    def test_output_file_exists(self):
        """Verify output file was created at the specified path."""
        assert os.path.exists(OUTPUT_FILE), f"Output file not found: {OUTPUT_FILE}"

    def test_output_file_not_empty(self):
        """Verify output file is not empty."""
        assert os.path.getsize(OUTPUT_FILE) > 0, "Output file is empty"

    def test_output_valid_json(self):
        """Verify output is valid JSON."""
        with open(OUTPUT_FILE) as f:
            data = json.load(f)
        assert isinstance(data, dict), "Output should be a JSON object"

    def test_output_is_json_object(self):
        """Verify output is a JSON object (not array or primitive)."""
        with open(OUTPUT_FILE) as f:
            data = json.load(f)
        assert isinstance(data, dict), "Output must be a JSON object"

    # =========================================================================
    # Schema Tests
    # =========================================================================

    def test_has_exactly_required_fields(self):
        """Verify output has exactly the three required fields."""
        with open(OUTPUT_FILE) as f:
            data = json.load(f)
        required_fields = {"gene", "padj", "log2FoldChange"}
        actual_fields = set(data.keys())
        assert actual_fields == required_fields, \
            f"Expected fields {required_fields}, got {actual_fields}"

    def test_gene_field_is_string(self):
        """Verify gene field is a non-empty string."""
        with open(OUTPUT_FILE) as f:
            data = json.load(f)
        assert "gene" in data, "Missing required field: gene"
        assert isinstance(data["gene"], str), "gene must be a string"
        assert len(data["gene"]) > 0, "gene must not be empty"

    def test_padj_field_is_number(self):
        """Verify padj field is a numeric value."""
        with open(OUTPUT_FILE) as f:
            data = json.load(f)
        assert "padj" in data, "Missing required field: padj"
        assert isinstance(data["padj"], (int, float)), "padj must be numeric"

    def test_log2foldchange_field_is_number(self):
        """Verify log2FoldChange field is a numeric value."""
        with open(OUTPUT_FILE) as f:
            data = json.load(f)
        assert "log2FoldChange" in data, "Missing required field: log2FoldChange"
        assert isinstance(data["log2FoldChange"], (int, float)), "log2FoldChange must be numeric"

    # =========================================================================
    # Value Tests
    # =========================================================================

    def test_gene_value_correct(self):
        """Verify gene field has the expected value."""
        with open(OUTPUT_FILE) as f:
            data = json.load(f)
        assert data["gene"] == self.EXPECTED_RESULT["gene"], \
            f"gene mismatch: expected '{self.EXPECTED_RESULT['gene']}', got '{data['gene']}'"

    def test_padj_value_correct(self):
        """Verify padj field matches expected value within tolerance."""
        with open(OUTPUT_FILE) as f:
            data = json.load(f)
        expected = self.EXPECTED_RESULT["padj"]
        actual = data["padj"]
        assert math.isclose(actual, expected, rel_tol=self.TOLERANCE), \
            f"padj mismatch: expected {expected}, got {actual}"

    def test_log2foldchange_value_correct(self):
        """Verify log2FoldChange field matches expected value within tolerance."""
        with open(OUTPUT_FILE) as f:
            data = json.load(f)
        expected = self.EXPECTED_RESULT["log2FoldChange"]
        actual = data["log2FoldChange"]
        assert math.isclose(actual, expected, rel_tol=self.TOLERANCE), \
            f"log2FoldChange mismatch: expected {expected}, got {actual}"

    # =========================================================================
    # Content Validity Tests
    # =========================================================================

    def test_padj_is_valid_pvalue(self):
        """Verify padj is a valid adjusted p-value (0 < padj <= 1)."""
        with open(OUTPUT_FILE) as f:
            data = json.load(f)
        padj = data["padj"]
        assert 0 < padj <= 1, f"padj should be in (0, 1], got {padj}"

    def test_padj_is_finite(self):
        """Verify padj is a finite number (not NaN or Inf)."""
        with open(OUTPUT_FILE) as f:
            data = json.load(f)
        assert math.isfinite(data["padj"]), "padj must be finite (not NaN or Inf)"

    def test_log2foldchange_is_finite(self):
        """Verify log2FoldChange is a finite number."""
        with open(OUTPUT_FILE) as f:
            data = json.load(f)
        assert math.isfinite(data["log2FoldChange"]), "log2FoldChange must be finite"

    def test_log2foldchange_has_reasonable_magnitude(self):
        """Verify log2FoldChange is within biologically reasonable range."""
        with open(OUTPUT_FILE) as f:
            data = json.load(f)
        lfc = abs(data["log2FoldChange"])
        assert lfc < 50, f"|log2FoldChange| should be < 50, got {lfc}"


class TestInputFiles:
    """Tests verifying input files are accessible."""

    @pytest.mark.parametrize("name,path", list(INPUT_FILES.items()))
    def test_input_file_exists(self, name, path):
        """Verify each input AnnData file exists."""
        assert os.path.exists(path), f"Input file not found: {path}"


class TestGeneValidity:
    """Tests verifying the reported gene is valid."""

    def test_gene_exists_in_all_datasets(self):
        """Verify the reported gene exists in the intersection of all three datasets."""
        import anndata as ad

        with open(OUTPUT_FILE) as f:
            data = json.load(f)
        gene = data["gene"]

        gene_sets = []
        for name, path in INPUT_FILES.items():
            adata = ad.read_h5ad(path)
            if adata.raw is not None:
                gene_sets.append(set(adata.raw.var_names))
            else:
                gene_sets.append(set(adata.var_names))

        common_genes = gene_sets[0].intersection(gene_sets[1]).intersection(gene_sets[2])
        assert gene in common_genes, \
            f"Gene '{gene}' not found in the intersection of all datasets"

    def test_gene_is_valid_symbol(self):
        """Verify gene name is a valid gene symbol format."""
        with open(OUTPUT_FILE) as f:
            data = json.load(f)
        gene = data["gene"]
        assert gene == gene.strip(), "Gene symbol should not have leading/trailing whitespace"
        assert len(gene) >= 2, "Gene symbol should be at least 2 characters"

    def test_gene_has_nonzero_expression(self):
        """Verify the reported gene has non-zero expression in datasets."""
        import anndata as ad
        import numpy as np

        with open(OUTPUT_FILE) as f:
            data = json.load(f)
        gene = data["gene"]

        for name, path in INPUT_FILES.items():
            adata = ad.read_h5ad(path)
            if adata.raw is not None:
                genes = list(adata.raw.var_names)
                X = adata.raw.X
            else:
                genes = list(adata.var_names)
                X = adata.X

            if gene in genes:
                idx = genes.index(gene)
                total_expr = np.asarray(X[:, idx].sum()).item()
                assert total_expr > 0, \
                    f"Gene '{gene}' has zero total expression in {name}"


class TestStatisticalValidity:
    """Tests verifying statistical properties of the result."""

    def test_padj_is_highly_significant(self):
        """Verify the top gene has a highly significant padj (< 0.05)."""
        with open(OUTPUT_FILE) as f:
            data = json.load(f)
        assert data["padj"] < 0.05, \
            f"Top DE gene should have padj < 0.05, got {data['padj']}"

    def test_padj_is_extremely_significant(self):
        """Verify the top gene has extremely small padj (< 1e-10)."""
        with open(OUTPUT_FILE) as f:
            data = json.load(f)
        assert data["padj"] < 1e-10, \
            f"Top DE gene should have padj < 1e-10, got {data['padj']}"

    def test_log2foldchange_indicates_downregulation(self):
        """Verify log2FoldChange is negative (gene downregulated in pbmc_10k vs pbmc3k)."""
        with open(OUTPUT_FILE) as f:
            data = json.load(f)
        assert data["log2FoldChange"] < 0, \
            f"Expected negative log2FoldChange (downregulation), got {data['log2FoldChange']}"

    def test_log2foldchange_is_large(self):
        """Verify |log2FoldChange| indicates substantial differential expression."""
        with open(OUTPUT_FILE) as f:
            data = json.load(f)
        assert abs(data["log2FoldChange"]) > 1.0, \
            f"|log2FoldChange| should be > 1 (2-fold change), got {abs(data['log2FoldChange'])}"


class TestDataIntegrity:
    """Tests for data integrity and consistency."""

    EXPECTED_GENE = "MATR3"
    EXPECTED_PADJ = 9.331870807240807e-20
    EXPECTED_LOG2FC = -9.766598188716994

    def test_all_values_match_expected(self):
        """Comprehensive check that all output values match expected."""
        with open(OUTPUT_FILE) as f:
            data = json.load(f)

        assert data["gene"] == self.EXPECTED_GENE, \
            f"Gene: expected '{self.EXPECTED_GENE}', got '{data['gene']}'"

        assert math.isclose(data["padj"], self.EXPECTED_PADJ, rel_tol=1e-6), \
            f"padj: expected {self.EXPECTED_PADJ}, got {data['padj']}"

        assert math.isclose(data["log2FoldChange"], self.EXPECTED_LOG2FC, rel_tol=1e-6), \
            f"log2FoldChange: expected {self.EXPECTED_LOG2FC}, got {data['log2FoldChange']}"

    def test_no_nan_values(self):
        """Verify no NaN values in output."""
        with open(OUTPUT_FILE) as f:
            data = json.load(f)

        for key, value in data.items():
            if isinstance(value, float):
                assert not math.isnan(value), f"{key} is NaN"

    def test_no_infinity_values(self):
        """Verify no infinity values in output."""
        with open(OUTPUT_FILE) as f:
            data = json.load(f)

        for key, value in data.items():
            if isinstance(value, float):
                assert not math.isinf(value), f"{key} is infinity"


class TestGeneIntersection:
    """Tests verifying gene intersection computation."""

    EXPECTED_COMMON_GENES = 11506

    def test_common_genes_count(self):
        """Verify the expected number of common genes across datasets."""
        import anndata as ad

        gene_sets = []
        for path in INPUT_FILES.values():
            adata = ad.read_h5ad(path)
            if adata.raw is not None:
                gene_sets.append(set(adata.raw.var_names))
            else:
                gene_sets.append(set(adata.var_names))

        common = gene_sets[0].intersection(gene_sets[1]).intersection(gene_sets[2])
        assert len(common) == self.EXPECTED_COMMON_GENES, \
            f"Expected {self.EXPECTED_COMMON_GENES} common genes, got {len(common)}"

    def test_matr3_in_common_genes(self):
        """Verify MATR3 is in the gene intersection."""
        import anndata as ad

        gene_sets = []
        for path in INPUT_FILES.values():
            adata = ad.read_h5ad(path)
            if adata.raw is not None:
                gene_sets.append(set(adata.raw.var_names))
            else:
                gene_sets.append(set(adata.var_names))

        common = gene_sets[0].intersection(gene_sets[1]).intersection(gene_sets[2])
        assert "MATR3" in common, "MATR3 should be in the common gene set"
