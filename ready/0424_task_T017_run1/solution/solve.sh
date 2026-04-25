#!/bin/bash
set -e
mkdir -p /root/output
# Create the solution Python script using heredoc
cat << 'EOF' > /root/solve_task.py
import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Step 1: Load CSV into DataFrame
df = pd.read_csv("/root/iris.csv")

# Step 2: Create X (four numeric measurement columns) and y (species encoded to integers)
feature_cols = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
X = df[feature_cols]

# Encode species to integers and store the class order
le = LabelEncoder()
y = le.fit_transform(df["species"])
label_encoder_classes = le.classes_.tolist()

# Step 3: Split with required parameters
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Step 4: Build leakage-safe preprocessing + model pipeline
pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LogisticRegression(max_iter=1000,  random_state=42))
])

# Step 5: Fit on training set and predict on test set
pipe.fit(X_train, y_train)
y_pred = pipe.predict(X_test)

# Step 6: Compute required metrics
test_accuracy = float(accuracy_score(y_test, y_pred))
cm = confusion_matrix(y_test, y_pred, labels=[0, 1, 2]).tolist()
report = classification_report(y_test, y_pred, output_dict=True)

# Step 7: Write the exact JSON structure as specified
output = {
    "label_encoder_classes": label_encoder_classes,
    "test_accuracy": test_accuracy,
    "confusion_matrix": cm,
    "classification_report": report
}

output_path = "/root/output/iris_logreg_eval.json"
with open(output_path, "w") as f:
    json.dump(output, f, indent=2)

print(f"Output saved to: {output_path}")
EOF

# Execute the script
python3 /root/solve_task.py
