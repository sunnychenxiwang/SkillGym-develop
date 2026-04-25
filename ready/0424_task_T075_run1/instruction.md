Using `/root/iris.csv`, build a deterministic, end-to-end modeling procedure that selects the single best-performing **species classifier** under the following constraints, then save the uniquely verifiable result as JSON.

**Objective:** Determine which of two feature-reduction approaches yields the higher mean cross-validated accuracy on the Iris dataset when followed by the same classifier, and report the winner and its score.

**Procedure (must be followed exactly):**
1. Load `iris.csv`. Use the 4 numeric measurement columns as features `X` and `species` as the target `y` (encode labels deterministically).
2. Use `StratifiedKFold(n_splits=5, shuffle=True, random_state=42)` for evaluation and `accuracy` as the metric.
3. Compare exactly these two pipelines (same train/test splits, same classifier):
   - **Pipeline A (PCA):** `StandardScaler` → `PCA(n_components=2, random_state=42)` → `LogisticRegression(max_iter=2000, random_state=42)`
   - **Pipeline B (Varimax factor scores):** `StandardScaler` → `FactorAnalyzer(n_factors=2, rotation='varimax')` → `LogisticRegression(max_iter=2000, random_state=42)`
4. For each pipeline, compute the **mean** accuracy across the 5 folds.
5. Select the winner by:
   - higher mean accuracy wins;
   - if tied exactly, choose `"PCA"` as the winner.

**Deliverable (mandatory):** Write a JSON file to  
`/root/output/iris_dimred_winner.json`  
with exactly this schema and numeric rounding:
```json
{
  "winner": "PCA_or_VARIMAX",
  "pca_mean_accuracy": 0.0000,
  "varimax_mean_accuracy": 0.0000
}
```
Round both accuracies to **4 decimal places** and ensure `winner` is either `"PCA"` or `"VARIMAX"` exactly.