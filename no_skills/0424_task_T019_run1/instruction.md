Load the three AnnData files:

- `/root/pbmc3k.h5ad`
- `/root/pbmc3k_2.h5ad`
- `/root/pbmc_10k_protein_v3.h5ad`

For each dataset, compute a **deterministic “top marker genes” table** as follows:

1. **Preprocess (per dataset, independently)**  
   - Work on the **raw count matrix** if present (`adata.raw.X` / `adata.raw.var`); otherwise use `adata.X` / `adata.var`.  
   - Filter cells with `min_genes=200` and genes with `min_cells=3`.  
   - Normalize total counts to `1e4` per cell, then `log1p`.  
   - Select **highly variable genes** with `n_top_genes=2000` (if the dataset has fewer than 2000 genes after filtering, use all remaining genes).  
   - Run PCA with `n_comps=50` (or the maximum allowed by remaining dimensions if smaller).

2. **Define groups for marker scoring (per dataset)**  
   - If `adata.obs` contains a column named `louvain`, use it as the group label.  
   - Else if it contains `leiden`, use that.  
   - Else, create a group label called `pseudo_cluster` by binning `n_genes` into **exactly 5 quantile bins** (use `pandas.qcut`, dropping duplicate bin edges deterministically if needed).

3. **Marker score (per dataset, per group)**  
   For each group *g* and each gene *j* in the post-HVG expression matrix, compute:

   \[
   score(g,j) = mean_{cells \in g}(X_{log1p}) - mean_{cells \notin g}(X_{log1p})
   \]

   Then, for each group, pick the **single gene with the maximum score**. Break ties by choosing the lexicographically smallest gene name.

4. **Cross-dataset consolidation (must use all 3 files)**  
   - Create one combined table with exactly **one row per dataset per group** (so rows = sum of group counts across the 3 datasets).  
   - Add a final column `is_shared_top_marker` that is `true` if that selected top-marker gene appears as a selected top-marker gene in **at least one of the other two datasets** (same gene name string match), else `false`.

5. **Deliverable (mandatory file artifact)**  
   Save the combined result as a JSON file at:

`/root/output/top_marker_summary.json`

with this exact schema:

```json
{
  "datasets": [
    {
      "dataset_name": "pbmc3k.h5ad",
      "groups": [
        {
          "group": "0",
          "top_gene": "LYZ",
          "score": 0.123456,
          "is_shared_top_marker": true
        }
      ]
    }
  ]
}
```

Requirements:
- `dataset_name` must be exactly the input filename (not the full path).
- `groups` must be sorted by `group` as a string (ascending).
- `datasets` must be ordered: `pbmc3k.h5ad`, `pbmc3k_2.h5ad`, `pbmc_10k_protein_v3.h5ad`.
- `score` must be a JSON number rounded to **6 decimal places**.
- The output must be fully reproducible (no randomness; if any method has a random state, set it to 0).