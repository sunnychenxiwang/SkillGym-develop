#!/bin/bash
set -e

# Create output directory
mkdir -p /root/output

# Create the solution Python script using heredoc
cat << 'EOF' > /root/solve_task.py
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from factor_analyzer import FactorAnalyzer
import json

# Input and output paths
INPUT_PATH = '/root/iris.csv'
OUTPUT_PATH = '/root/output/iris_species_factor_profile.json'

# Species order - alphabetically sorted as required
SPECIES_ORDER = ["setosa", "versicolor", "virginica"]

# Numeric measurement columns
NUMERIC_COLS = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']

def main():
    # Step 1: Load the CSV
    df = pd.read_csv(INPUT_PATH)

    # Step 2: Select the 4 numeric measurement columns
    X = df[NUMERIC_COLS].values

    # Step 3: Standardize numeric columns
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Step 4: Kaiser criterion - unrotated FactorAnalyzer to get eigenvalues
    fa_check = FactorAnalyzer(n_factors=X_scaled.shape[1], rotation=None)
    fa_check.fit(X_scaled)
    eigenvalues, _ = fa_check.get_eigenvalues()

    # Count eigenvalues > 1 for Kaiser criterion
    n_factors = int((eigenvalues > 1).sum())

    # Step 5: Fit final varimax-rotated FactorAnalyzer
    fa = FactorAnalyzer(n_factors=n_factors, rotation='varimax')
    fa.fit(X_scaled)
    scores = fa.transform(X_scaled)

    # Step 6: Compute mean factor scores per species
    for j in range(n_factors):
        df[f'Factor{j+1}'] = scores[:, j]

    factor_cols = [f'Factor{k+1}' for k in range(n_factors)]
    mean_scores_df = df.groupby('species')[factor_cols].mean()
    mean_scores_df = mean_scores_df.loc[SPECIES_ORDER]

    # Step 7: Build JSON object with required schema and rounding to 6 decimals
    mean_factor_scores = {
        sp: [round(float(v), 6) for v in mean_scores_df.loc[sp].values.tolist()]
        for sp in SPECIES_ORDER
    }

    out = {
        "n_factors": n_factors,
        "species_order": SPECIES_ORDER,
        "mean_factor_scores": mean_factor_scores
    }

    # Write to JSON file
    with open(OUTPUT_PATH, 'w') as f:
        json.dump(out, f)

if __name__ == '__main__':
    main()
EOF

# Execute the script
python3 /root/solve_task.py
