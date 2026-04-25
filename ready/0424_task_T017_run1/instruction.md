Train and evaluate a **3-class Iris species classifier** from `/root/iris.csv` using a leakage-safe preprocessing + model pipeline, then write a single JSON artifact containing the uniquely determined evaluation results.

Requirements (all must be met):

1. Load the CSV into a DataFrame, and create:
   - `X`: the four numeric measurement columns
   - `y`: the `species` column encoded to integers (store the class order used for encoding).
2. Split the data with `train_test_split(test_size=0.2, random_state=42, stratify=y)`.
3. Build a scikit-learn `Pipeline` that standardizes features with `StandardScaler` and fits `LogisticRegression(max_iter=1000, multi_class="auto", random_state=42)`.
4. Fit on the training set and predict on the test set.
5. Compute:
   - overall test **accuracy**,
   - **confusion matrix** (as a 3×3 nested list) using the encoded label order,
   - `classification_report` as a dict (`output_dict=True`).
6. Save exactly the following JSON structure to **`/root/output/iris_logreg_eval.json`** (writing the file is mandatory):

```json
{
  "label_encoder_classes": ["..."],
  "test_accuracy": 0.0,
  "confusion_matrix": [[0,0,0],[0,0,0],[0,0,0]],
  "classification_report": { }
}
```

Notes:
- `label_encoder_classes` must be the exact ordered list of class names used by the label encoder.
- `test_accuracy` must be a numeric float (not a string), computed from the test predictions.
- Do not include any extra top-level keys in the JSON.