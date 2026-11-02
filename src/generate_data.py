"""Generate a small synthetic 'student pass/fail' dataset.

The dataset is intentionally a bit messy (a few missing values, mixed-case
categories and duplicate rows) so the ETL step in Experiment 4 has real
cleaning work to do.

Run:  python -m src.generate_data
"""
import numpy as np
import pandas as pd

RAW_PATH = "data/raw/students.csv"


def generate(n_rows: int = 300, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    study_hours = rng.uniform(0, 10, n_rows).round(1)
    attendance = rng.uniform(40, 100, n_rows).round(0)
    previous_score = rng.uniform(20, 100, n_rows).round(0)
    extra_classes = rng.choice(["yes", "no"], n_rows, p=[0.4, 0.6])

    # Hidden rule + noise that decides pass/fail
    score = (
        0.45 * study_hours * 10
        + 0.30 * attendance
        + 0.25 * previous_score
        + np.where(extra_classes == "yes", 5, 0)
        + rng.normal(0, 6, n_rows)
    )
    passed = (score >= 55).astype(int)

    df = pd.DataFrame({
        "student_id": np.arange(1, n_rows + 1),
        "study_hours": study_hours,
        "attendance": attendance,
        "previous_score": previous_score,
        "extra_classes": extra_classes,
        "passed": passed,
    })

    # Make it slightly messy for the ETL experiment
    df.loc[rng.choice(n_rows, 6, replace=False), "study_hours"] = np.nan
    df.loc[rng.choice(n_rows, 4, replace=False), "attendance"] = np.nan
    upper = rng.choice(n_rows, 10, replace=False)
    df.loc[upper, "extra_classes"] = df.loc[upper, "extra_classes"].str.upper()
    df = pd.concat([df, df.iloc[:5]], ignore_index=True)  # duplicates
    return df


if __name__ == "__main__":
    data = generate()
    data.to_csv(RAW_PATH, index=False)
    print(f"Saved {len(data)} rows to {RAW_PATH}")
