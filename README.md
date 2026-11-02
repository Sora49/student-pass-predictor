# 🎓 Student Pass/Fail Predictor (MLOps lab project)

A tiny ML project used for all 7 MLOps experiments. A Logistic Regression model predicts
whether a student passes from **study hours, attendance, previous score and extra classes**.
Small dataset + slim Docker image = fast builds.

## Quick start
```bash
python -m venv .venv
.venv\Scripts\activate          # Windows   (Mac/Linux: source .venv/bin/activate)
pip install -r requirements-dev.txt
python -m src.train             # -> Accuracy: 0.90
pytest -v
streamlit run app.py            # -> http://localhost:8501
```

## Project layout
```
app.py                    Streamlit UI
src/features.py           cleaning + feature logic (shared)
src/train.py              trains and saves models/model.pkl
src/predict.py            load model + predict
src/generate_data.py      re-creates data/raw/students.csv
src/etl_pipeline.py       Exp 4: ETL -> feature_store/
src/mlflow_experiment.py  Exp 4: MLflow tracking
tests/                    pytest tests (Exp 2, 3)
docs/                     Scrum artefacts (Exp 1)
ci-templates/             GitHub Actions workflows (Exp 2, 3)
Dockerfile, k8s/          Exp 5
terraform/                Exp 6
monitoring/               Exp 7 (Flask API + Prometheus + Grafana)
```

See **EXPERIMENT_STEPS.md** for the step-by-step guide to every experiment.
