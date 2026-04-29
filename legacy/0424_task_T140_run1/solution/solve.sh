#!/bin/bash
set -e

# Create the output directory
mkdir -p /root/output

# Create the solution Python script using heredoc
cat << 'EOF' > /root/solve_task.py
import anndata as ad
import scanpy as sc
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
import json
import warnings
warnings.filterwarnings('ignore')

# File paths
INPUT_DIR = "/root"
OUTPUT_PATH = "/root/output/most_consistent_hvg.json"

paths = [
    f"{INPUT_DIR}/pbmc3k.h5ad",
    f"{INPUT_DIR}/pbmc3k_2.h5ad",
    f"{INPUT_DIR}/pbmc_10k_protein_v3.h5ad",
]

# Step 1: Load all three AnnData files and prepare for processing
adatas_raw = []
for i, p in enumerate(paths):
    a = ad.read_h5ad(p)

    if i == 0:
        # Dataset 1: X is already processed, use raw.X which is log1p-normalized
        # Reverse log1p to get back to "counts" for consistent processing
        raw_adata = a.raw.to_adata()
        X_counts = np.expm1(raw_adata.X)
        raw_adata.X = X_counts
        adatas_raw.append(raw_adata)
    else:
        # Datasets 2 and 3: X contains raw counts
        adatas_raw.append(a)

# Step 2: Preprocess each dataset on a copy and compute HVGs
processed = []
hvg_sets = []

for i, a in enumerate(adatas_raw):
    b = a.copy()

    # Filter cells with zero total counts
    cell_counts = np.array(b.X.sum(axis=1)).flatten()
    valid_cells = cell_counts > 0
    if np.sum(~valid_cells) > 0:
        b = b[valid_cells, :].copy()

    # Filter genes with zero counts
    gene_counts = np.array(b.X.sum(axis=0)).flatten()
    valid_genes = gene_counts > 0
    if np.sum(~valid_genes) > 0:
        b = b[:, valid_genes].copy()

    # Apply standard preprocessing
    sc.pp.normalize_total(b, target_sum=1e4)
    sc.pp.log1p(b)

    # Compute HVGs - adjust n_top_genes if fewer genes available
    n_genes = b.n_vars
    n_top = min(2000, n_genes)
    sc.pp.highly_variable_genes(b, n_top_genes=n_top, flavor="seurat")

    processed.append(b)
    hvg_set = set(b.var_names[b.var["highly_variable"]])
    hvg_sets.append(hvg_set)

# Step 3: Compute intersection of HVG gene symbols
hvg_intersection = set.intersection(*hvg_sets)
genes = sorted(hvg_intersection)  # deterministic ordering
intersection_size = len(genes)

# Step 4: For each gene in intersection, build 3-feature vector
disp_series = [p.var["dispersions_norm"] for p in processed]

# Get top 100 genes per dataset by dispersions_norm (over ALL genes, not just HVGs)
top100_sets = []
for s in disp_series:
    top100 = set(s.sort_values(ascending=False).head(100).index)
    top100_sets.append(top100)

rows = []
for g in genes:
    vals = np.array([float(s.loc[g]) for s in disp_series], dtype=float)
    mean_dn = float(vals.mean())
    std_dn = float(vals.std(ddof=0))  # population std for reproducibility
    frac = float(np.mean([g in t for t in top100_sets]))
    rows.append((g, mean_dn, std_dn, frac))

df = pd.DataFrame(rows, columns=["gene", "mean_dn", "std_dn", "top100_fraction"])

# Step 5: Fit LogisticRegression to predict top100_any from mean/std
X = df[["mean_dn", "std_dn"]].to_numpy()
y = (df["top100_fraction"].to_numpy() > 0).astype(int)

clf = LogisticRegression(max_iter=2000)
clf.fit(X, y)

proba = clf.predict_proba(X)[:, 1]
df["predicted_probability"] = proba

# Step 6: Select the single best gene with deterministic tie-break
max_p = df["predicted_probability"].max()
tied = df[df["predicted_probability"] == max_p].copy()

best_gene = sorted(tied["gene"].tolist())[0]
best_row = df[df["gene"] == best_gene].iloc[0]

# Step 7: Write JSON output
out = {
    "gene": str(best_row["gene"]),
    "intersection_size": int(intersection_size),
    "mean_dispersions_norm": float(best_row["mean_dn"]),
    "std_dispersions_norm": float(best_row["std_dn"]),
    "top100_fraction": float(best_row["top100_fraction"]),
    "predicted_probability": float(best_row["predicted_probability"]),
}

with open(OUTPUT_PATH, "w") as f:
    json.dump(out, f, indent=2)

print(f"Output written to: {OUTPUT_PATH}")
EOF

# Execute the script
python3 /root/solve_task.py
