Load **all three** AnnData files:

- `/root/pbmc3k.h5ad`
- `/root/pbmc3k_2.h5ad`
- `/root/pbmc_10k_protein_v3.h5ad`

and determine the **single gene symbol** that is the most consistently “highly variable” across datasets under a unified, reproducible definition:

1. For each dataset, run a minimal Scanpy-style preprocessing on a copy of the data:  
   - normalize total counts to 1e4, `log1p`, then compute `highly_variable_genes(n_top_genes=2000, flavor="seurat")`.  
2. Compute the **intersection** of the three resulting HVG gene sets (by `adata.var_names`).
3. For each gene in that intersection, build a 3-feature vector using the **per-dataset HVG statistics** from `adata.var`:
   - mean of `dispersions_norm` across the 3 datasets  
   - standard deviation of `dispersions_norm` across the 3 datasets  
   - fraction of datasets (0–1) where the gene is in the top **100** by `dispersions_norm` (within that dataset)
4. Fit a scikit-learn `LogisticRegression` model (no regularization tuning; use default solver but set `max_iter=2000`) to predict the binary label “top100_any” (1 if fraction>0 else 0) from the first two features (mean and std). Use the fitted model to compute the predicted probability for every gene in the intersection.
5. Select the **single** gene with the **highest predicted probability**; break ties deterministically by choosing the lexicographically smallest gene symbol.

Write exactly one JSON file to:

`/root/output/most_consistent_hvg.json`

with this schema (and no extra keys):

```json
{
  "gene": "GENE_SYMBOL",
  "intersection_size": 0,
  "mean_dispersions_norm": 0.0,
  "std_dispersions_norm": 0.0,
  "top100_fraction": 0.0,
  "predicted_probability": 0.0
}
```

All numeric values must be real numbers (not strings) and computed from the procedure above. Writing this file is mandatory for completion.