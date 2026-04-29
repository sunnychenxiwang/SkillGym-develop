Train a **deterministic** classifier that predicts `species` from the four numeric measurements in `/root/iris.csv`, then compute **which single original row** is the model’s **most confident correct prediction** under cross-validation, and save that row’s identity plus the confidence to a JSON file.

Requirements (all are mandatory):

1. **Polars (lazy)**: Load the CSV via `scan_csv`, add a stable `row_id` column equal to the 0-based row index in the file order, and write a cleaned CSV (same rows/columns plus `row_id`) to a temporary path you choose.
2. **Pandas/data-transform**: Read that temporary CSV, ensure `species` is treated as categorical, and build `X` (the 4 feature columns) and `y` (species labels) while preserving `row_id`.
3. **scikit-learn**: Build a `Pipeline` with:
   - `StandardScaler`
   - `LogisticRegression` (`multi_class="auto"`, `solver="lbfgs"`, `random_state=42`, `max_iter=500`)
   Use `StratifiedKFold(n_splits=5, shuffle=True, random_state=42)` and `cross_val_predict(..., method="predict_proba")` to get out-of-fold class probabilities for every row.
4. For each row, define **confidence** as the maximum predicted probability across classes. Consider only rows where the predicted class (argmax) matches the true `species`. Find the **single row** with the **highest confidence**; break ties by choosing the smallest `row_id`.
5. Write exactly one JSON file to **`/root/output/most_confident_correct.json`** with this exact schema:

```json
{
  "row_id": 0,
  "true_species": "setosa",
  "pred_species": "setosa",
  "confidence": 0.0,
  "features": {
    "sepal_length": 0.0,
    "sepal_width": 0.0,
    "petal_length": 0.0,
    "petal_width": 0.0
  }
}
```

Notes:
- `confidence` must be a floating-point number (not a string) and should reflect the probability from `predict_proba` for `pred_species`.
- The `features` values must be taken from the original row in the dataset corresponding to `row_id` (not scaled values).