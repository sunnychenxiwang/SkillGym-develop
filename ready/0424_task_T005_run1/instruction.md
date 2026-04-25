Load the three AnnData files:

- `/root/pbmc3k.h5ad`
- `/root/pbmc3k_2.h5ad`
- `/root/pbmc_10k_protein_v3.h5ad`

Using each file’s **raw count matrix** (prefer `adata.raw.X` if present; otherwise use `adata.layers["counts"]` if present; otherwise fall back to `adata.X`), do the following:

1. For each dataset independently, compute **pseudobulk samples** by summing counts across all cells (i.e., one pseudobulk “sample” per dataset) over the **intersection of gene names shared by all three datasets**.
2. Build a single PyDESeq2 analysis where the three pseudobulk samples are the observations and the design is `~ dataset`, with `dataset` having exactly these three levels: `pbmc3k`, `pbmc3k_2`, `pbmc_10k_protein_v3`.
3. Run DESeq2 and extract the differential expression results for the contrast:
   - `pbmc_10k_protein_v3` vs `pbmc3k`
4. From that results table, identify the **single gene** with the **smallest adjusted p-value (`padj`)**; break ties deterministically by choosing the lexicographically smallest gene name among tied genes. If `padj` is NA for some genes, exclude those genes from consideration.

Write a JSON file to **exactly** this path:

`/root/output/top_de_gene_pbmc10k_vs_pbmc3k.json`

with the following fixed schema:

```json
{
  "gene": "GENE_NAME",
  "padj": 0.0,
  "log2FoldChange": 0.0
}
```

Where `gene` is the selected gene symbol/name (matching the AnnData var index), and `padj` and `log2FoldChange` are the corresponding values from the PyDESeq2 results for the specified contrast. Writing this file is mandatory for completion.