"""Experiment 4 - ETL pipeline + simple file-based Feature Store.

Extract  : read the raw CSV
Transform: validate, clean, encode, engineer new features
Load     : save reusable features to feature_store/

Run:  python -m src.etl_pipeline
"""
import os

import pandas as pd

from src.features import RAW_PATH, TARGET, clean

FEATURE_STORE_DIR = "feature_store"
FEATURE_PATH = os.path.join(FEATURE_STORE_DIR, "student_features.csv")


def extract(path: str = RAW_PATH) -> pd.DataFrame:
    df = pd.read_csv(path)
    print(f"[EXTRACT] {len(df)} rows, {df.shape[1]} columns from {path}")
    print(df.head(), "\n")
    return df


def validate(df: pd.DataFrame) -> None:
    print("[VALIDATE] Missing values per column:")
    print(df.isna().sum().to_string(), "\n")
    print(f"[VALIDATE] Duplicate rows: {df.duplicated().sum()}")
    print(f"[VALIDATE] extra_classes values: {sorted(df['extra_classes'].unique())}\n")


def transform(df: pd.DataFrame) -> pd.DataFrame:
    df = clean(df)
    # Feature engineering
    df["study_x_attendance"] = (df["study_hours"] * df["attendance"] / 100).round(2)
    df["score_band"] = pd.cut(df["previous_score"], bins=[0, 40, 70, 100],
                              labels=[0, 1, 2]).astype(int)
    print(f"[TRANSFORM] Clean rows: {len(df)}; new features: "
          "study_x_attendance, score_band\n")
    return df


def load(df: pd.DataFrame, path: str = FEATURE_PATH) -> str:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    cols = [c for c in df.columns if c != "student_id"]
    df[cols].to_csv(path, index=False)
    print(f"[LOAD] Features stored at: {path}")
    print(f"[LOAD] Columns: {cols}")
    return path


def run() -> str:
    raw = extract()
    validate(raw)
    features = transform(raw)
    assert TARGET in features.columns
    return load(features)


if __name__ == "__main__":
    run()
