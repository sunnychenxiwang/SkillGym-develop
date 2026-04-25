#!/bin/bash
set -e

# Create output directory
mkdir -p /root/output

# Create the solution Python script using heredoc
cat << 'EOF' > /root/solve_task.py
"""
Deterministic comparison of PCA vs Varimax factor analysis for Iris species classification.
"""

import numpy as np
import pandas as pd
import json
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline
from factor_analyzer import FactorAnalyzer

# Paths
INPUT_PATH = '/root/iris.csv'
OUTPUT_PATH = '/root/output/iris_dimred_winner.json'

# Feature columns
FEATURE_COLS = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']

def main():
    # Step 1: Load CSV and extract X/y
    df = pd.read_csv(INPUT_PATH)
    X = df[FEATURE_COLS]
    y = df['species']

    # Step 2: Deterministically encode labels using LabelEncoder
    le = LabelEncoder()
    y_enc = le.fit_transform(y)

    # Step 3: Define CV splitter
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    # Step 4: Build Pipeline A (PCA)
    pipeline_pca = Pipeline([
        ('scaler', StandardScaler()),
        ('pca', PCA(n_components=2, random_state=42)),
        ('classifier', LogisticRegression(max_iter=2000, random_state=42))
    ])

    # Step 5: Build Pipeline B (Varimax factor scores)
    pipeline_varimax = Pipeline([
        ('scaler', StandardScaler()),
        ('fa', FactorAnalyzer(n_factors=2, rotation='varimax')),
        ('classifier', LogisticRegression(max_iter=2000, random_state=42))
    ])

    # Step 6: Cross-validated accuracy for each pipeline
    scores_pca = cross_val_score(pipeline_pca, X, y_enc, cv=skf, scoring='accuracy')
    pca_mean = scores_pca.mean()

    scores_varimax = cross_val_score(pipeline_varimax, X, y_enc, cv=skf, scoring='accuracy')
    varimax_mean = scores_varimax.mean()

    # Step 7: Select winner with tie-break rule
    if varimax_mean > pca_mean:
        winner = "VARIMAX"
    else:
        winner = "PCA"  # includes exact tie

    # Step 8: Round and write JSON
    pca_out = round(pca_mean, 4)
    varimax_out = round(varimax_mean, 4)

    result = {
        "winner": winner,
        "pca_mean_accuracy": pca_out,
        "varimax_mean_accuracy": varimax_out
    }

    with open(OUTPUT_PATH, 'w') as f:
        json.dump(result, f, indent=2)

if __name__ == '__main__':
    main()
EOF

# Execute the script
python3 /root/solve_task.py
