"""Experiment 4 - Model experimentation and tracking with MLflow.

Reads features from the feature store (run the ETL first) and trains
several models, logging params, metrics and the model artifact to MLflow.

Run:  python -m src.mlflow_experiment
Then: mlflow ui --port 5001   ->  open http://127.0.0.1:5001
"""
import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

from src.etl_pipeline import FEATURE_PATH
from src.features import TARGET

EXPERIMENT_NAME = "Student_Pass_ETL_FeatureStore"

RUNS = [
    ("LogisticRegression", LogisticRegression, {"max_iter": 300, "C": 1.0}),
    ("DecisionTree_depth3", DecisionTreeClassifier, {"max_depth": 3, "random_state": 42}),
    ("RandomForest_100", RandomForestClassifier,
     {"n_estimators": 100, "max_depth": 5, "random_state": 42}),
]


def main():
    df = pd.read_csv(FEATURE_PATH)
    X, y = df.drop(columns=[TARGET]), df[TARGET]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    mlflow.set_experiment(EXPERIMENT_NAME)
    results = []
    for run_name, cls, params in RUNS:
        with mlflow.start_run(run_name=run_name):
            model = cls(**params)
            model.fit(X_train, y_train)
            pred = model.predict(X_test)
            acc = accuracy_score(y_test, pred)
            f1 = f1_score(y_test, pred)

            mlflow.log_param("model", cls.__name__)
            mlflow.log_params(params)
            mlflow.log_param("feature_file", FEATURE_PATH)
            mlflow.log_metric("accuracy", acc)
            mlflow.log_metric("f1_score", f1)
            mlflow.sklearn.log_model(model, "model")
            results.append((run_name, acc, f1))
            print(f"{run_name:<22} accuracy={acc:.3f}  f1={f1:.3f}")

    best = max(results, key=lambda r: r[1])
    print(f"\nBest run by accuracy: {best[0]} ({best[1]:.3f})")
    print("Experiment tracking completed. Start the UI with: mlflow ui --port 5001")


if __name__ == "__main__":
    main()
