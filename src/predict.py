"""Load the trained model and make predictions."""
import os

import joblib

from src.features import to_features
from src.train import MODEL_PATH, train


def load_model(model_path: str = MODEL_PATH):
    if not os.path.exists(model_path):
        train(model_path=model_path)
    return joblib.load(model_path)


def predict(model, study_hours, attendance, previous_score, extra_classes):
    """Return (label, probability_of_pass)."""
    X = to_features(study_hours, attendance, previous_score, extra_classes)
    prob_pass = float(model.predict_proba(X)[0][1])
    label = "Pass" if prob_pass >= 1.5 else "Fail"
    return label, prob_pass
