#!/bin/bash
set -e
mkdir -p /root/output
# Create the solution Python script using heredoc
cat << 'EOF' > /root/solve_task.py
#!/usr/bin/env python3
"""
Top Marker Genes Analysis Pipeline

Processes three AnnData files and computes top marker genes per group,
with cross-dataset consolidation.
"""

import json
import numpy as np
import pandas as pd
import anndata as ad
import scanpy as sc
from scipy.sparse import issparse

# Dataset paths in required order
DATASET_PATHS = [
    "/root/pbmc3k.h5ad",
    "/root/pbmc3k_2.h5ad",
    "/root/pbmc_10k_protein_v3.h5ad",
]

OUTPUT_PATH = "/root/output/top_marker_summary.json"


def get_dataset_name(path: str) -> str:
    """Extract filename from path."""
    return path.split("/")[-1]


def use_raw_if_present(adata: ad.AnnData) -> ad.AnnData:
    """Return AnnData using raw counts if present, otherwise copy of original."""
    if adata.raw is not None:
        return ad.AnnData(
            X=adata.raw.X.copy() if issparse(adata.raw.X) else adata.raw.X.copy(),
            obs=adata.obs.copy(),
            var=adata.raw.var.copy()
        )
    else:
        return adata.copy()


def preprocess_dataset(adata: ad.AnnData) -> ad.AnnData:
    """
    Preprocess: filter cells/genes, normalize, log1p, HVG, PCA.
    Returns processed AnnData.
    """
    # Filter cells with min_genes=200 and genes with min_cells=3
    sc.pp.filter_cells(adata, min_genes=200)
    sc.pp.filter_genes(adata, min_cells=3)

    # Ensure we work with a copy (not a view)
    adata = adata.copy()

    # Normalize total counts to 1e4 per cell
    sc.pp.normalize_total(adata, target_sum=1e4)

    # Log1p transform
    sc.pp.log1p(adata)

    # Select highly variable genes with n_top_genes=2000
    n_genes = adata.n_vars
    if n_genes <= 2000:
        hvg_mask = np.ones(n_genes, dtype=bool)
    else:
        sc.pp.highly_variable_genes(adata, n_top_genes=2000)
        hvg_mask = adata.var["highly_variable"].to_numpy()

    # Subset to HVG
    adata_hvg = adata[:, hvg_mask].copy()

    # Run PCA with capped n_comps
    max_comps = min(50, adata_hvg.n_obs - 1, adata_hvg.n_vars - 1)
    max_comps = max(max_comps, 1)  # Ensure at least 1
    sc.pp.pca(adata_hvg, n_comps=max_comps, random_state=0)

    return adata_hvg


def determine_group_column(adata: ad.AnnData) -> str:
    """
    Determine grouping column: louvain > leiden > pseudo_cluster.
    Creates pseudo_cluster if neither exists.
    """
    if "louvain" in adata.obs.columns:
        return "louvain"
    elif "leiden" in adata.obs.columns:
        return "leiden"
    else:
        # Create pseudo_cluster from n_genes quantile bins
        if "n_genes" not in adata.obs.columns:
            # Calculate n_genes if not present
            if issparse(adata.X):
                adata.obs["n_genes"] = np.array((adata.X > 0).sum(axis=1)).flatten()
            else:
                adata.obs["n_genes"] = (adata.X > 0).sum(axis=1)

        x = adata.obs["n_genes"]

        # Try qcut with 5 bins
        try:
            labels = pd.qcut(x, q=5, labels=False, duplicates="drop")
            n_unique = labels.nunique()
            if n_unique < 5:
                # Fallback: use rank-based qcut
                r = x.rank(method="first")
                labels = pd.qcut(r, q=5, labels=False, duplicates="drop")
        except ValueError:
            # Fallback: use rank-based qcut
            r = x.rank(method="first")
            labels = pd.qcut(r, q=5, labels=False, duplicates="drop")

        adata.obs["pseudo_cluster"] = labels.astype(str)
        return "pseudo_cluster"


def compute_marker_scores(adata: ad.AnnData, group_col: str) -> list:
    """
    Compute marker scores for each group.
    Score = mean_in_group - mean_out_of_group for each gene.
    Returns list of dicts with group, top_gene, score.
    """
    X = adata.X
    genes = np.array(adata.var_names)
    groups = adata.obs[group_col].unique()

    results = []

    for g in groups:
        # Boolean mask for cells in group
        in_group = (adata.obs[group_col] == g).values
        out_group = ~in_group

        # Compute means
        if issparse(X):
            mean_in = np.asarray(X[in_group].mean(axis=0)).ravel()
            mean_out = np.asarray(X[out_group].mean(axis=0)).ravel()
        else:
            mean_in = X[in_group].mean(axis=0)
            mean_out = X[out_group].mean(axis=0)
            if hasattr(mean_in, 'ravel'):
                mean_in = mean_in.ravel()
                mean_out = mean_out.ravel()

        # Score = mean_in - mean_out
        scores = mean_in - mean_out

        # Find max score
        max_score = scores.max()

        # Find all genes with max score (for tie-breaking)
        candidates = genes[scores == max_score]

        # Tie-break: lexicographically smallest gene name
        top_gene = sorted(candidates.tolist())[0]

        results.append({
            "group": str(g),
            "top_gene": top_gene,
            "score": round(float(max_score), 6)
        })

    # Sort by group as string
    results.sort(key=lambda x: x["group"])

    return results


def process_single_dataset(path: str) -> dict:
    """
    Process a single dataset and return results.
    """
    dataset_name = get_dataset_name(path)

    # Load dataset
    adata = ad.read_h5ad(path)

    # Use raw if present
    adata_use = use_raw_if_present(adata)

    # Preprocess
    adata_hvg = preprocess_dataset(adata_use)

    # Determine grouping
    group_col = determine_group_column(adata_hvg)

    # Compute marker scores
    groups_results = compute_marker_scores(adata_hvg, group_col)

    return {
        "dataset_name": dataset_name,
        "groups": groups_results
    }


def add_shared_marker_flags(datasets: list) -> list:
    """
    Add is_shared_top_marker flag to each group result.
    True if the gene appears as top marker in at least one other dataset.
    """
    # Collect top genes per dataset
    dataset_genes = []
    for ds in datasets:
        genes = {g["top_gene"] for g in ds["groups"]}
        dataset_genes.append(genes)

    # For each dataset, check if gene is shared with any other dataset
    for i, ds in enumerate(datasets):
        other_genes = set()
        for j, genes in enumerate(dataset_genes):
            if j != i:
                other_genes.update(genes)

        for group in ds["groups"]:
            group["is_shared_top_marker"] = group["top_gene"] in other_genes

    return datasets


def main():
    # Process each dataset
    all_results = []
    for path in DATASET_PATHS:
        result = process_single_dataset(path)
        all_results.append(result)

    # Add shared marker flags
    all_results = add_shared_marker_flags(all_results)

    # Build output structure
    output = {
        "datasets": all_results
    }

    # Write JSON output
    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2)


if __name__ == "__main__":
    main()
EOF

# Execute the script
python3 /root/solve_task.py
