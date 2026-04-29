#!/bin/bash
set -e

# Create the solution Python script using heredoc
cat << 'EOF' > /root/solve_task.py
import json
import numpy as np
import pandas as pd
import statsmodels.api as sm
from aeon.classification.convolution_based import RocketClassifier

def classify_flood(water_level, thresholds):
    if water_level >= thresholds['major']:
        return 'major'
    elif water_level >= thresholds['moderate']:
        return 'moderate'
    elif water_level >= thresholds['flood']:
        return 'minor'
    elif water_level >= thresholds['action']:
        return 'action'
    else:
        return 'normal'

INPUT_FILES = [
    '/root/datagetter',
    '/root/datagetter_2',
    '/root/datagetter_3',
    '/root/datagetter_5',
]
OUTPUT_FILE = '/root/output/best_flood_model.json'
THRESHOLDS = {'major': 1.6, 'moderate': 1.4, 'flood': 1.2, 'action': 1.0}
WINDOW_SIZE = 40
TRAIN_RATIO = 0.7

def load_station_data(filepath):
    df = pd.read_csv(filepath)
    df.columns = df.columns.str.strip()
    df['Date Time'] = pd.to_datetime(df['Date Time'])
    df = df.sort_values('Date Time').reset_index(drop=True)
    df['Water Level'] = pd.to_numeric(df['Water Level'], errors='coerce')
    df = df.dropna(subset=['Water Level'])
    return df

def create_flood_labels(water_levels, thresholds):
    return np.array([
        0 if classify_flood(w, thresholds) == 'normal' else 1
        for w in water_levels
    ])

def create_windows(levels, labels, window_size):
    n = len(levels)
    n_windows = n - window_size
    if n_windows <= 0:
        return np.array([]).reshape(0, 1, window_size), np.array([])

    X = np.zeros((n_windows, 1, window_size))
    y = np.zeros(n_windows, dtype=int)

    for i in range(n_windows):
        X[i, 0, :] = levels[i:i + window_size]
        y[i] = labels[i + window_size]

    return X, y

def extract_logit_features(X):
    windows = X[:, 0, :]
    features = np.column_stack([
        np.mean(windows, axis=1),
        np.std(windows, axis=1),
        np.min(windows, axis=1),
        np.max(windows, axis=1),
        windows[:, -1],
    ])
    return features

def main():
    import os
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    all_X_train, all_y_train = [], []
    all_X_test, all_y_test = [], []

    for filepath in INPUT_FILES:
        df = load_station_data(filepath)
        levels = df['Water Level'].values
        labels = create_flood_labels(levels, THRESHOLDS)
        X, y = create_windows(levels, labels, WINDOW_SIZE)
        n_windows = len(y)

        if n_windows == 0:
            continue

        n_train = int(np.floor(TRAIN_RATIO * n_windows))

        X_train_station = X[:n_train]
        y_train_station = y[:n_train]
        X_test_station = X[n_train:]
        y_test_station = y[n_train:]

        all_X_train.append(X_train_station)
        all_y_train.append(y_train_station)
        all_X_test.append(X_test_station)
        all_y_test.append(y_test_station)

    X_train = np.concatenate(all_X_train, axis=0)
    y_train = np.concatenate(all_y_train, axis=0)
    X_test = np.concatenate(all_X_test, axis=0)
    y_test = np.concatenate(all_y_test, axis=0)

    n_train_samples = len(y_train)
    n_test_samples = len(y_test)

    rocket = RocketClassifier(n_kernels=500, random_state=0)
    rocket.fit(X_train, y_train)
    rocket_acc = float(rocket.score(X_test, y_test))

    X_train_features = extract_logit_features(X_train)
    X_test_features = extract_logit_features(X_test)

    X_train_const = sm.add_constant(X_train_features)
    X_test_const = sm.add_constant(X_test_features)

    logit_model = sm.Logit(y_train, X_train_const)
    logit_results = logit_model.fit(disp=False)

    probs = logit_results.predict(X_test_const)
    preds = (probs >= 0.5).astype(int)
    logit_acc = float((preds == y_test).mean())

    if rocket_acc > logit_acc + 1e-12:
        best_model = "rocket"
    else:
        best_model = "logit"

    output = {
        "rocket_test_accuracy": rocket_acc,
        "logit_test_accuracy": logit_acc,
        "best_model": best_model,
        "n_train_samples": n_train_samples,
        "n_test_samples": n_test_samples,
    }

    with open(OUTPUT_FILE, 'w') as f:
        json.dump(output, f)

if __name__ == '__main__':
    main()
EOF

# Execute the script
python3 /root/solve_task.py
