"""Train the student pass/fail model and save it to models/model.pkl.

Run:  python -m src.train
"""
import os

import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from src.features import FEATURES, RAW_PATH, TARGET, clean

MODEL_PATH = "models/model.pkl"


def train(data_path: str = RAW_PATH, model_path: str = MODEL_PATH) -> float:
    df = clean(pd.read_csv(data_path))
    X, y = df[FEATURES], df[TARGET]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=300))
    model.fit(X_train, y_train)
    accuracy = accuracy_score(y_test, model.predict(X_test))

    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(model, model_path)
    return accuracy


if __name__ == "__main__":
    acc = train()
    print(f"Accuracy: {acc:.2f}")
    print(f"Model saved to {MODEL_PATH}")
