Compute a **single, deterministic “best-performing flood early-warning model”** across the four station time series files and save the result as a compact JSON artifact.

Using **all four input files** (`/root/datagetter`, `.../datagetter_2`, `.../datagetter_3`, `.../datagetter_5`):

1. Parse each file into a time-indexed series using the **Date Time** column and the **Water Level** column.
2. For each station, create a binary flood label per timestamp: label = 1 if `classify_flood(water_level, thresholds)` is anything other than “normal”, else 0, using exactly these thresholds:
   ```python
   thresholds = {'major': 1.6, 'moderate': 1.4, 'flood': 1.2, 'action': 1.0}
   ```
3. Build a supervised dataset where each sample is a **rolling window of the previous 40 timestamps** (i.e., 4 hours at 6-minute intervals) and the target is the flood label at the **next** timestamp. Do this separately per station, then concatenate all stations into one dataset. (Drop any samples that cannot be formed at the start of each station.)
4. Train and evaluate (single train/test split, deterministic) an **aeon** time-series classifier to predict the next-step flood label:
   - Use `RocketClassifier(n_kernels=500, random_state=0)`
   - Split by time **within each station**: first 70% windows for training, last 30% for testing; then merge the station splits (so every station contributes to both train and test).
   - Report test **accuracy** on the merged test set.
5. Fit a **statsmodels Logit** model on the same task as a baseline:
   - Convert each 40-point window into features: mean, std, min, max, and last value (5 features).
   - Fit `sm.Logit(y_train, sm.add_constant(X_train))` and evaluate accuracy on the test set using threshold 0.5.
6. Select the “best-performing model” by higher test accuracy; if accuracies tie to within **1e-12**, choose `"logit"`.

Write exactly one JSON file to:
`/root/output/best_flood_model.json`

with this exact schema (and no extra keys):
```json
{
  "rocket_test_accuracy": <float>,
  "logit_test_accuracy": <float>,
  "best_model": "<rocket|logit>",
  "n_train_samples": <int>,
  "n_test_samples": <int>
}
```

All numeric values must be computed from the provided files (no hardcoding).