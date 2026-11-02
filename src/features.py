"""Shared data cleaning / feature logic used by training, ETL, the app and the API."""
import pandas as pd

RAW_PATH = "data/raw/students.csv"
TARGET = "passed"
FEATURES = ["study_hours", "attendance", "previous_score", "extra_classes"]


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicates, fix categories and fill missing numeric values."""
    df = df.drop_duplicates().copy()
    df["extra_classes"] = df["extra_classes"].str.strip().str.lower()
    df["extra_classes"] = (df["extra_classes"] == "yes").astype(int)
    for col in ["study_hours", "attendance", "previous_score"]:
        df[col] = df[col].fillna(df[col].median())
    return df


def to_features(study_hours, attendance, previous_score, extra_classes):
    """Turn raw user input into a one-row DataFrame the model understands."""
    extra = 1 if str(extra_classes).strip().lower() in ("yes", "1", "true") else 0
    return pd.DataFrame([{
        "study_hours": float(study_hours),
        "attendance": float(attendance),
        "previous_score": float(previous_score),
        "extra_classes": extra,
    }])[FEATURES]
