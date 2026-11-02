import pandas as pd

from src.features import FEATURES, clean, to_features
from src.predict import load_model, predict
from src.train import train


def test_clean_removes_duplicates_and_missing():
    raw = pd.read_csv("data/raw/students.csv")
    cleaned = clean(raw)
    assert cleaned.duplicated().sum() == 0
    assert cleaned[FEATURES].isna().sum().sum() == 0
    assert set(cleaned["extra_classes"].unique()) <= {0, 1}


def test_to_features_shape():
    X = to_features(5, 80, 70, "yes")
    assert list(X.columns) == FEATURES
    assert X.iloc[0]["extra_classes"] == 1


def test_model_accuracy_is_good_enough(tmp_path):
    acc = train(model_path=str(tmp_path / "model.pkl"))
    assert acc >= 0.80


def test_strong_student_passes():
    label, prob = predict(load_model(), 9, 95, 90, "yes")
    assert label == "Pass"
    assert 0.0 <= prob <= 1.0


def test_weak_student_fails():
    label, _ = predict(load_model(), 0.5, 45, 25, "no")
    assert label == "Fail"
