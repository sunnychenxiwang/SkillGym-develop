#!/bin/bash
set -e

# Create the solution Python script using heredoc
cat << 'EOF' > /root/solve_task.py
"""
Deterministic classifier for Iris dataset - finds most confident correct prediction.
Uses: Polars (lazy) -> CSV -> Pandas -> scikit-learn Pipeline
"""

import json
import polars as pl
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_predict
import warnings
warnings.filterwarnings('ignore')

# Paths
INPUT_PATH = "/root/iris.csv"
TEMP_CSV_PATH = "/root/output/iris_with_row_id_tmp.csv"
OUTPUT_PATH = "/root/output/most_confident_correct.json"

# Feature columns
FEATURE_COLS = ["sepal_length", "sepal_width", "petal_length", "petal_width"]

# Ensure output directory exists
import os
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

# =============================================================================
# Step 1: Polars lazy load, add stable row_id, write temp CSV
# =============================================================================

# Use scan_csv for lazy loading
lf = pl.scan_csv(INPUT_PATH)

# Collect to get the data
df_polars = lf.collect()

# Add row_id as 0-based index in file order
df_polars = df_polars.with_row_index(name="row_id")

# Write to temporary CSV
df_polars.write_csv(TEMP_CSV_PATH)

# =============================================================================
# Step 2: Read temp CSV with Pandas, enforce categorical species
# =============================================================================

df = pd.read_csv(TEMP_CSV_PATH)

# Enforce species as categorical
df["species"] = df["species"].astype("category")

# Build X (features), y (target), and preserve row_id
X = df[FEATURE_COLS]
y = df["species"]
row_id = df["row_id"]

# =============================================================================
# Step 3: Build deterministic pipeline and get out-of-fold probabilities
# =============================================================================

# Build pipeline
pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("classifier", LogisticRegression(
        solver="lbfgs",
        random_state=42,
        max_iter=500
    ))
])

# Stratified K-Fold with deterministic shuffle
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

# Get out-of-fold predicted probabilities
proba = cross_val_predict(pipe, X, y, cv=cv, method="predict_proba")

# Fit once on full data to get class order from the model
pipe.fit(X, y)
model_classes = pipe.named_steps["classifier"].classes_

# =============================================================================
# Step 4: Compute confidence, filter correct predictions, find best row
# =============================================================================

# Compute predicted class index and confidence
pred_idx = proba.argmax(axis=1)
confidence = proba.max(axis=1)

# Map predicted index to species label
pred_species = np.array([model_classes[i] for i in pred_idx])

# Get true species as string for comparison
true_species = y.astype(str).to_numpy()

# Filter to correct predictions
correct_mask = (pred_species == true_species)

# Build results dataframe for correct predictions
results_df = pd.DataFrame({
    "row_id": row_id,
    "true_species": true_species,
    "pred_species": pred_species,
    "confidence": confidence
})

# Filter to correct, sort by confidence (desc), then row_id (asc) for tie-breaking
correct_df = results_df[correct_mask].copy()
correct_df = correct_df.sort_values(
    by=["confidence", "row_id"],
    ascending=[False, True]
)

# Select the best row (highest confidence, smallest row_id for ties)
best_row = correct_df.iloc[0]
best_row_id = int(best_row["row_id"])

# =============================================================================
# Step 5: Build and write JSON output
# =============================================================================

# Get original features for the best row (unscaled)
original_row = df[df["row_id"] == best_row_id].iloc[0]

output = {
    "row_id": best_row_id,
    "true_species": str(best_row["true_species"]),
    "pred_species": str(best_row["pred_species"]),
    "confidence": float(best_row["confidence"]),
    "features": {
        "sepal_length": float(original_row["sepal_length"]),
        "sepal_width": float(original_row["sepal_width"]),
        "petal_length": float(original_row["petal_length"]),
        "petal_width": float(original_row["petal_width"])
    }
}

# Write JSON
with open(OUTPUT_PATH, "w") as f:
    json.dump(output, f, indent=2)

print(f"Output written to: {OUTPUT_PATH}")
print(json.dumps(output, indent=2))
EOF

# Execute the script
python3 /root/solve_task.py
