Load the three AnnData files:

- `/root/pbmc3k.h5ad`
- `/root/pbmc3k_2.h5ad`
- `/root/pbmc_10k_protein_v3.h5ad`

and compute a **single, uniquely defined “cross-dataset gene signature”** as follows:

1. For each dataset, take the **raw counts matrix if `adata.raw` exists**, otherwise use `adata.X`.  
2. Restrict to the **intersection of gene names** across all three datasets (`var_names`), then:
   - compute per-cell library-size normalization to `1e4`,
   - apply `log1p`,
   - compute **mean expression per gene** across cells.
3. Create a single table over the shared genes with three columns: `mean_pbmc3k`, `mean_pbmc3k_2`, `mean_pbmc10k`.
4. For each gene, compute a **replicability score** defined as the **first varimax-rotated factor score** from a `FactorAnalyzer` fit on the standardized (z-scored) 3-column matrix of per-gene means (genes are rows; the three dataset means are features). Use `n_factors=1` and `rotation='varimax'`.
5. Identify the **single gene** with the **maximum** replicability score; break ties deterministically by choosing the lexicographically smallest gene name.

Write the result as a JSON file to:

`/root/output/top_replicable_gene.json`

with exactly this schema:

```json
{
  "gene": "GENE_NAME",
  "replicability_score": 0.0,
  "shared_gene_count": 0
}
```

Where:
- `gene` is the selected gene name,
- `replicability_score` is the corresponding factor score (a float),
- `shared_gene_count` is the number of genes in the 3-way intersection used in the analysis.

Saving this JSON file at the specified path is mandatory.