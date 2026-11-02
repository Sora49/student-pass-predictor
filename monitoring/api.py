"""Experiment 7 - Flask prediction API for the SAME student model,
instrumented with Prometheus metrics.

Endpoints:
  GET  /          health message
  POST /predict   JSON {"study_hours":5,"attendance":80,"previous_score":70,"extra_classes":"yes"}
  GET  /metrics   Prometheus metrics
"""
import time

from flask import Flask, jsonify, request
from prometheus_client import (CONTENT_TYPE_LATEST, Counter, Gauge, Histogram,
                               generate_latest)

from src.predict import load_model, predict

app = Flask(__name__)
model = load_model()

REQUESTS = Counter("ml_http_requests_total", "Total HTTP requests",
                   ["endpoint", "method", "status"])
PREDICTIONS = Counter("ml_predictions_total", "Total ML predictions", ["result"])
LATENCY = Histogram("ml_prediction_latency_seconds", "Time taken for prediction")
ERRORS = Counter("ml_errors_total", "Total application errors")
PASS_PROB = Gauge("ml_last_pass_probability", "Pass probability of the last prediction")
MODEL_INFO = Gauge("ml_model_info", "Model metadata", ["version", "algorithm"])
MODEL_INFO.labels(version="1.0", algorithm="LogisticRegression").set(1)

RANGES = {
    "study_hours": (0, 10),
    "attendance": (0, 100),
    "previous_score": (0, 100),
}


def _validate(data):
    for field, (low, high) in RANGES.items():
        value = data.get(field)
        if value is None or isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"Provide numeric '{field}'")
        if not low <= value <= high:
            raise ValueError(f"'{field}' must be between {low} and {high}")
    if str(data.get("extra_classes", "")).lower() not in ("yes", "no"):
        raise ValueError("'extra_classes' must be 'yes' or 'no'")


@app.route("/")
def home():
    return jsonify({"message": "Student Pass Predictor API is running"})


@app.route("/predict", methods=["POST"])
def predict_endpoint():
    start = time.perf_counter()
    try:
        data = request.get_json(silent=True) or {}
        _validate(data)
        label, prob = predict(model, data["study_hours"], data["attendance"],
                              data["previous_score"], data["extra_classes"])
        PREDICTIONS.labels(result=label).inc()
        PASS_PROB.set(prob)
        REQUESTS.labels("/predict", "POST", "200").inc()
        return jsonify({"prediction": label, "pass_probability": round(prob, 3)}), 200
    except ValueError as exc:
        ERRORS.inc()
        REQUESTS.labels("/predict", "POST", "400").inc()
        return jsonify({"error": str(exc)}), 400
    except Exception:
        ERRORS.inc()
        REQUESTS.labels("/predict", "POST", "500").inc()
        return jsonify({"error": "Internal server error"}), 500
    finally:
        LATENCY.observe(time.perf_counter() - start)


@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
