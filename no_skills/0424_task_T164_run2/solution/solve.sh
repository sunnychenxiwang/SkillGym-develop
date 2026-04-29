#!/bin/bash
set -e

# Create output directory if needed
mkdir -p /root/output

# Create the solution Python script using heredoc
cat << 'EOF' > /root/solve_task.py
import anndata as ad
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from factor_analyzer import FactorAnalyzer
import json

# Input file paths
PBMC3K_PATH = '/root/pbmc3k.h5ad'
PBMC3K_2_PATH = '/root/pbmc3k_2.h5ad'
PBMC10K_PATH = '/root/pbmc_10k_protein_v3.h5ad'
OUTPUT_PATH = '/root/output/top_replicable_gene.json'

def get_matrix_and_genes(adata):
    """Get raw counts matrix if available, otherwise use adata.X"""
    if adata.raw is not None:
        return adata.raw.X, adata.raw.var_names
    else:
        return adata.X, adata.var_names

def preprocess_dataset(X, genes, shared_genes):
    """Normalize, log1p, and compute mean expression per gene"""
    # Create mapping from gene name to index
    gene_to_idx = {g: i for i, g in enumerate(genes)}
    shared_idx = [gene_to_idx[g] for g in shared_genes]

    # Subset to shared genes
    X_shared = X[:, shared_idx]

    # Convert to dense array if sparse
    if hasattr(X_shared, 'toarray'):
        X_shared = X_shared.toarray()
    else:
        X_shared = np.array(X_shared)

    # Library-size normalize to 1e4 per cell
    cell_sums = X_shared.sum(axis=1, keepdims=True)
    cell_sums = np.where(cell_sums == 0, 1, cell_sums)
    X_norm = X_shared / cell_sums * 1e4

    # Apply log1p
    X_log = np.log1p(X_norm)

    # Compute mean expression per gene
    return X_log.mean(axis=0)

def main():
    # Step 1: Load all three AnnData objects
    adata_pbmc3k = ad.read_h5ad(PBMC3K_PATH)
    adata_pbmc3k_2 = ad.read_h5ad(PBMC3K_2_PATH)
    adata_pbmc10k = ad.read_h5ad(PBMC10K_PATH)

    # Step 2: Get matrices and gene names
    X1, genes1 = get_matrix_and_genes(adata_pbmc3k)
    X2, genes2 = get_matrix_and_genes(adata_pbmc3k_2)
    X3, genes3 = get_matrix_and_genes(adata_pbmc10k)

    # Step 3: Compute 3-way intersection of gene names
    shared_genes_set = set(genes1) & set(genes2) & set(genes3)
    shared_genes = sorted(list(shared_genes_set))
    shared_gene_count = len(shared_genes)

    # Step 4: Preprocess each dataset on shared genes
    mean_pbmc3k = preprocess_dataset(X1, genes1, shared_genes)
    mean_pbmc3k_2 = preprocess_dataset(X2, genes2, shared_genes)
    mean_pbmc10k = preprocess_dataset(X3, genes3, shared_genes)

    # Step 5: Build single shared-gene table with three mean columns
    df = pd.DataFrame({
        'mean_pbmc3k': mean_pbmc3k,
        'mean_pbmc3k_2': mean_pbmc3k_2,
        'mean_pbmc10k': mean_pbmc10k
    }, index=shared_genes)

    # Step 6: Standardize the 3-column matrix
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df[['mean_pbmc3k', 'mean_pbmc3k_2', 'mean_pbmc10k']].values)

    # Step 7: Fit FactorAnalyzer with varimax rotation and get factor scores
    fa = FactorAnalyzer(n_factors=1, rotation='varimax')
    fa.fit(X_scaled)
    scores = fa.transform(X_scaled)

    # Step 8: Find gene with maximum replicability score (tie-break by lexicographic order)
    replicability_scores = scores[:, 0]
    s = pd.Series(replicability_scores, index=shared_genes)
    max_val = s.max()
    candidates = sorted(s.index[s == max_val].tolist())
    top_gene = candidates[0]
    top_score = float(s[top_gene])

    # Step 9: Write JSON output
    result = {
        "gene": top_gene,
        "replicability_score": top_score,
        "shared_gene_count": shared_gene_count
    }

    with open(OUTPUT_PATH, 'w') as f:
        json.dump(result, f, indent=2)

if __name__ == '__main__':
    main()
EOF

# Execute the script
python3 /root/solve_task.py
