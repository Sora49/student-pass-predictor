# Step-by-step guide: all 7 MLOps experiments on one project

**Project:** Student Pass/Fail Predictor (Streamlit + scikit-learn Logistic Regression)
**Inputs:** study hours (0–10), attendance % (0–100), previous score (0–100), extra classes (yes/no) → **Pass / Fail**

Commands are written for **Windows PowerShell** (Mac/Linux differences noted).
Nothing is deleted or destroyed until the **Final cleanup** section at the end, so the
ports are chosen so that everything can stay running together:

| What | URL / port |
|---|---|
| Streamlit (local, Exp 1) | http://localhost:8501 |
| Streamlit in Docker (Exp 5) | http://localhost:8502 |
| Streamlit in Kubernetes (Exp 5) | http://localhost:8503 (port-forward) |
| NGINX warm-up (Exp 5) | http://localhost:8080 |
| Streamlit via Terraform (Exp 6) | http://localhost:8081 → later 8082 |
| MLflow UI (Exp 4) | http://localhost:5001 |
| Prediction API (Exp 7) | http://localhost:5000 |
| Prometheus (Exp 7) | http://localhost:9090 |
| Grafana (Exp 7) | http://localhost:3000 |

**Install once:** Python 3.10+, Git, VS Code, Docker Desktop, kubectl + Minikube (or Kubernetes in Docker Desktop), Terraform CLI, a GitHub account.

---

## Experiment 1 – Agile & Scrum demo

1. Unzip `student-pass-predictor.zip` to e.g. `D:\student-pass-predictor` and open the folder in VS Code.
   The required structure (`data/`, `src/`, `models/`, `docs/`, `README.md`) is already there.
2. Open a terminal in VS Code (**Terminal → New Terminal**) and set up Python:
   ```powershell
   python -m venv .venv
   .venv\Scripts\activate            # Mac/Linux: source .venv/bin/activate
   pip install -r requirements-dev.txt
   ```
   If PowerShell blocks activation: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, then retry.
3. **Scrum team & roles** – open `docs/Sprint_1.md`; fill your classmates' names into the role table
   (if alone, you play all 5 roles).
4. **Product Backlog** – open `docs/Product_Backlog.md` (user stories US1–US7 with priorities).
   Be ready to explain why High-priority items come first (they block everything else).
5. **Sprint Planning** – the Sprint 1 goal and task estimates are in `docs/Sprint_1.md`.
6. **Daily Scrum** – read out the Yesterday / Today / Blockers table in `docs/Sprint_1.md`.
7. **Build the ML model** (the Sprint work):
   ```powershell
   python -m src.train
   ```
   Expected output: `Accuracy: 0.90` and `Model saved to models/model.pkl`.
8. Run the app to demo the increment:
   ```powershell
   streamlit run app.py
   ```
   Open http://localhost:8501, move the sliders, click **Predict**. Screenshot it.
   Press `Ctrl+C` in the terminal when done (this just stops the local server).
9. **Sprint Review & Retrospective** – tick the checklist and go through the retro table in `docs/Sprint_1.md`.
10. **Screenshots for the record:** folder structure, backlog, training output, the Streamlit page.

---

## Experiment 2 – Git, GitHub and CI/CD

### Part A – Git basics
1. In the project folder (venv active):
   ```powershell
   git --version
   git config --global user.name "Your Name"
   git config --global user.email "you@example.com"
   git init
   git branch -M main
   git status
   ```
2. First commit (the `.gitignore` already keeps out the venv, model file, mlruns and Terraform state):
   ```powershell
   git add .
   git commit -m "Initial commit: student pass predictor app, tests and docs"
   git log --oneline
   ```
3. Run the tests locally so you know they pass:
   ```powershell
   pytest -v          # 5 passed
   ```

### Part A – Push to GitHub
4. On GitHub create an **empty** repo named `student-pass-predictor` (no README, no .gitignore).
5. Connect and push:
   ```powershell
   git remote add origin https://github.com/<YOUR_USERNAME>/student-pass-predictor.git
   git push -u origin main
   ```
   Log in through the browser pop-up (never paste tokens into files).

### Part A – Branch + Pull Request
6. Create a feature branch and make a small change:
   ```powershell
   git switch -c feature-message
   ```
   In `app.py`, change the last line to `st.caption("Model version 1.1 – added by feature branch")`.
   ```powershell
   git status
   git diff
   git add app.py
   git commit -m "Update app caption"
   git push -u origin feature-message
   ```
7. On GitHub: **Compare & pull request** → base `main` ← `feature-message` → **Create pull request** → **Merge**.
8. Sync local main:
   ```powershell
   git switch main
   git pull origin main
   git branch            # shows both branches
   git log --oneline
   ```

### Part B – CI with GitHub Actions
9. Copy the Exp 2 workflow into place:
   ```powershell
   mkdir .github\workflows
   copy ci-templates\python-ci.yml .github\workflows\python-ci.yml
   ```
   (Mac/Linux: `mkdir -p .github/workflows && cp ci-templates/python-ci.yml .github/workflows/`)
10. Commit and push:
    ```powershell
    git add .github/workflows/python-ci.yml
    git commit -m "Add Python CI workflow"
    git push
    ```
11. GitHub → **Actions** tab → open the **Python CI** run → all steps green, `5 passed`.
12. **Controlled failure:** in `tests/test_model.py` change `assert label == "Pass"` to `assert label == "Fail"`
    (in `test_strong_student_passes`). Commit + push → the run goes **red**. Screenshot it.
    Change it back, commit `"Fix test"`, push → **green** again.

### Part C – Jenkins (only if your lab has a Jenkins server)
13. The `Jenkinsfile` is already in the project root. In Jenkins: **New Item → Pipeline** → *Pipeline script from SCM* →
    Git → your repo URL → branch `main` → Script Path `Jenkinsfile` → **Build Now** → check **Console Output**.

---

## Experiment 3 – Continuous Integration with GitHub Actions (full pipeline)

This uses the same repo and adds a bigger workflow: **flake8 lint → train → tests on Python 3.10 and 3.11 → Docker build + smoke test**.

1. Copy the Exp 3 workflow:
   ```powershell
   copy ci-templates\ci.yml .github\workflows\ci.yml
   ```
2. Check lint locally first:
   ```powershell
   flake8 .
   ```
   (No output = clean.)
3. Push:
   ```powershell
   git add .github/workflows/ci.yml
   git commit -m "Add full CI pipeline: lint, matrix tests, docker build"
   git push
   ```
4. GitHub → **Actions** → **ML App CI**. Note the two matrix jobs (3.10, 3.11) and the `docker-build` job that waits
   for them (`needs:`). Open each step: Checkout → Set up Python → Install → Lint → Train → Run Tests.
   (The old **Python CI** workflow from Exp 2 also still runs – that's fine.)
5. **Demonstrate CI catching a bug:** in `src/predict.py` change
   ```python
   label = "Pass" if prob_pass >= 0.5 else "Fail"
   ```
   to
   ```python
   label = "Pass" if prob_pass >= 1.5 else "Fail"
   ```
   ```powershell
   git add .
   git commit -m "Modified pass threshold"
   git push
   ```
   The **Run Tests** step fails (`test_strong_student_passes`), and `docker-build` is skipped. Screenshot.
6. Restore `>= 0.5`, commit `"Fix threshold"`, push → all green. Screenshot.
7. Record the pytest output from the logs:
   ```
   tests/test_model.py::test_clean_removes_duplicates_and_missing PASSED
   tests/test_model.py::test_to_features_shape PASSED
   tests/test_model.py::test_model_accuracy_is_good_enough PASSED
   tests/test_model.py::test_strong_student_passes PASSED
   tests/test_model.py::test_weak_student_fails PASSED
   ```

---

## Experiment 4 – ETL, Feature Store and MLflow

1. Install MLflow (only needed for this experiment; it's kept out of Docker to keep images fast):
   ```powershell
   pip install -r requirements-mlflow.txt
   ```
2. **Run the ETL pipeline:**
   ```powershell
   python -m src.etl_pipeline
   ```
   Note what it prints for each stage:
   - **EXTRACT** – 305 rows read from `data/raw/students.csv`
   - **VALIDATE** – missing values (study_hours 6, attendance 4), 5 duplicate rows, mixed-case `YES`/`NO` values
   - **TRANSFORM** – duplicates dropped, missing values filled with the median, yes/no encoded to 1/0,
     new features `study_x_attendance` and `score_band`
   - **LOAD** – features saved to `feature_store/student_features.csv` (this is the simple feature store)
3. Open `feature_store/student_features.csv` in VS Code/Excel and screenshot it.
4. **Run the MLflow experiments** (3 models trained on the same stored features):
   ```powershell
   python -m src.mlflow_experiment
   ```
   It prints accuracy and F1 for LogisticRegression, DecisionTree_depth3 and RandomForest_100, and the best run.
5. Start the MLflow UI (in a **second terminal**, venv active, inside the project folder):
   ```powershell
   mlflow ui --port 5001
   ```
   Open http://127.0.0.1:5001 → experiment **Student_Pass_ETL_FeatureStore**.
6. Tick all 3 runs → **Compare** → look at params, `accuracy`, `f1_score`. Open a run → **Artifacts → model** to see the saved model.
7. Fill the observation table:

   | Run | Model | Key parameters | Accuracy | F1 |
   |---|---|---|---|---|
   | 1 | LogisticRegression | max_iter=300, C=1.0 | (from output) | |
   | 2 | DecisionTree | max_depth=3 | | |
   | 3 | RandomForest | n_estimators=100, max_depth=5 | | |

8. (Optional extra run) Edit the `RUNS` list in `src/mlflow_experiment.py`, e.g. add
   `("RandomForest_200", RandomForestClassifier, {"n_estimators": 200, "max_depth": 8, "random_state": 42}),`
   and re-run step 4 – a new run appears in the UI.
9. Commit the code (feature_store/ and mlruns/ are git-ignored on purpose):
   ```powershell
   git add .
   git commit -m "Exp 4: ETL pipeline and MLflow tracking"
   git push
   ```
   You can leave the MLflow UI running, or stop it with `Ctrl+C`.

---

## Experiment 5 – Docker and Kubernetes

Start **Docker Desktop** and wait until it says *Engine running*.

### Part A – Docker
1. Warm-up exactly as on the lab sheet:
   ```powershell
   docker --version
   docker pull nginx
   docker run -d --name mynginx -p 8080:80 nginx
   docker ps
   ```
   Open http://localhost:8080 (NGINX welcome page).
2. **Build the ML app image** (from the project root):
   ```powershell
   docker build -t student-pass-app:1.0 .
   ```
   The `Dockerfile` installs requirements first (cached layer), copies the code + data and trains the model inside the image.
   First build ~1–3 min; rebuilds after code changes take seconds.
3. Run it:
   ```powershell
   docker images
   docker run -d --name student-app -p 8502:8501 student-pass-app:1.0
   docker ps
   docker logs student-app
   ```
   Open http://localhost:8502 → make a prediction. Screenshot.

### Part B – Kubernetes

**Option 1 – Minikube**
4. ```powershell
   minikube start --driver=docker
   kubectl cluster-info
   kubectl get nodes
   minikube image load student-pass-app:1.0     # copies your local image into the cluster
   ```
**Option 2 – Docker Desktop Kubernetes** (Settings → Kubernetes → Enable). Local images are visible automatically; skip `image load`.

5. Deploy (3 replicas, see `k8s/deployment.yaml`):
   ```powershell
   kubectl apply -f k8s/deployment.yaml
   kubectl get deployments
   kubectl get pods
   ```
   Wait until all 3 pods show `Running` and `1/1` READY (the readiness probe checks Streamlit's health URL).
6. Expose it with a Service:
   ```powershell
   kubectl apply -f k8s/service.yaml
   kubectl get services
   ```
7. Open the app (works for both options):
   ```powershell
   kubectl port-forward service/student-app-service 8503:80
   ```
   Open http://localhost:8503. Leave this terminal open (Ctrl+C stops only the forwarding).
   Alternatives: Minikube → `minikube service student-app-service --url`; Docker Desktop → http://localhost:30085.
8. Scale from 3 to 5 replicas:
   ```powershell
   kubectl scale deployment student-app-deployment --replicas=5
   kubectl get pods
   ```
   Now 5 pods. Optional: `kubectl describe deployment student-app-deployment`.
9. Optional self-healing demo: `kubectl delete pod <one-pod-name>` then `kubectl get pods` – Kubernetes immediately creates a replacement.
   (This is not cleanup; the deployment keeps running.)

---

## Experiment 6 – Terraform (Infrastructure as Code)

Install Terraform and check: `terraform version`. Docker Desktop must be running (`docker info` works).

### Part 1 – Provider-neutral configuration (creates nothing)
1. ```powershell
   cd terraform\part1-basics
   terraform init
   terraform fmt
   terraform validate
   terraform plan
   ```
   The plan shows only **outputs** (`environment_name`, `common_tags`) and no resources to create.
2. Optional: `terraform plan -out=tfplan` then `terraform show tfplan`.
3. Try overriding a variable: `terraform plan -var="environment=dev"`. Screenshot.

### Part 2 – Run the ML app container with Terraform
Requires the image `student-pass-app:1.0` from Experiment 5.

4. ```powershell
   cd ..\part2-docker
   terraform init          # downloads the kreuzwerker/docker provider
   terraform fmt
   terraform validate
   terraform plan          # 2 to add: docker_image.app, docker_container.web
   terraform apply         # type: yes
   ```
   If init/plan can't reach Docker on Windows, edit `main.tf` to
   `provider "docker" { host = "npipe:////./pipe/docker_engine" }` and retry.
5. Open http://localhost:8081 → the same Streamlit app, now created by Terraform.
6. Inspect:
   ```powershell
   docker ps                      # container terraform-student-app on 0.0.0.0:8081
   terraform state list           # docker_container.web, docker_image.app
   terraform show
   terraform output
   ```
7. **Change the infrastructure:** in `main.tf` change `default = 8081` to `default = 8082` (variable `host_port`).
   ```powershell
   terraform plan                 # shows the container must be replaced (-/+)
   terraform apply                # type: yes
   ```
   Open http://localhost:8082 (8081 stops responding). Screenshot the plan and the browser.
8. Run `terraform apply` again with no change → *No changes* (idempotency). Screenshot.
9. **Do not** run `terraform destroy` yet – it's in the Final cleanup. Go back to the project root: `cd ..\..`

---

## Experiment 7 – ML Monitoring with Prometheus and Grafana

Streamlit doesn't expose a `/metrics` endpoint, so this experiment wraps the **same trained model** in a small
Flask API (`monitoring/api.py`) that records request count, predictions (Pass/Fail), errors, latency, last pass probability and model info.

1. Start the stack (Docker Desktop running):
   ```powershell
   cd monitoring
   docker compose up --build -d
   docker compose ps                # ml-app, prometheus, grafana all "running"
   docker compose logs ml-app
   ```
2. Test the API (PowerShell):
   ```powershell
   Invoke-RestMethod -Uri http://localhost:5000/predict -Method Post -ContentType "application/json" -Body '{"study_hours":8,"attendance":90,"previous_score":80,"extra_classes":"yes"}'
   ```
   → `prediction: Pass`
   ```powershell
   Invoke-RestMethod -Uri http://localhost:5000/predict -Method Post -ContentType "application/json" -Body '{"study_hours":1,"attendance":50,"previous_score":30,"extra_classes":"no"}'
   ```
   → `prediction: Fail`
   ```powershell
   Invoke-RestMethod -Uri http://localhost:5000/predict -Method Post -ContentType "application/json" -Body '{"study_hours":15,"attendance":80,"previous_score":70,"extra_classes":"yes"}'
   ```
   → error 400 (`study_hours must be between 0 and 10`).
   Mac/Linux: `curl -X POST localhost:5000/predict -H "Content-Type: application/json" -d '{"study_hours":8,"attendance":90,"previous_score":80,"extra_classes":"yes"}'`
3. Generate traffic (20 valid + 5 invalid requests; run it 2–3 times):
   ```powershell
   cd ..
   python monitoring\send_requests.py
   python monitoring\send_requests.py 50 10
   ```
4. Raw metrics: http://localhost:5000/metrics (look for `ml_predictions_total`, `ml_errors_total`).
5. **Prometheus** – http://localhost:9090 → *Status → Targets* shows `ml-application` **UP**. In the query box run one at a time (Table and Graph tabs):

   | PromQL | Shows |
   |---|---|
   | `up` | 1 = app is being scraped |
   | `ml_http_requests_total` | requests by endpoint/method/status (200 vs 400) |
   | `ml_predictions_total` | Pass and Fail counts |
   | `ml_errors_total` | invalid requests |
   | `rate(ml_http_requests_total[1m])` | requests per second |
   | `histogram_quantile(0.95, sum by (le) (rate(ml_prediction_latency_seconds_bucket[5m])))` | p95 latency |
   | `ml_last_pass_probability` | pass probability of the latest prediction |

6. **Grafana** – http://localhost:3000, login `admin` / `admin` (skip or set a new password).
   - **Connections → Data sources → Add data source → Prometheus** → URL `http://prometheus:9090` → **Save & test** (green).
   - **Dashboards → New → New dashboard → Add visualization** → choose Prometheus. Create these panels (Save after each):

   | Panel title | Query | Suggested visualization |
   |---|---|---|
   | HTTP requests | `ml_http_requests_total` | Time series |
   | Pass vs Fail | `sum by (result) (ml_predictions_total)` | Bar gauge / Pie chart |
   | Application errors | `ml_errors_total` | Stat |
   | Prediction latency p95 | `histogram_quantile(0.95, sum by (le) (rate(ml_prediction_latency_seconds_bucket[5m])))` | Time series (unit: seconds) |
   | Request rate | `rate(ml_http_requests_total[1m])` | Time series |

   - Set the dashboard refresh (top right) to **5s**, save the dashboard as *Student Model Monitoring*.
   - Run `python monitoring\send_requests.py 50 10` again and watch the panels move. Screenshot.
7. **Student exercises:**
   - Target down: `cd monitoring` then `docker compose stop ml-app` → in Prometheus `up` becomes **0**
     (Grafana panels flatline). Then `docker compose start ml-app` → back to 1.
   - Explain: a rising error rate could mean bad client input, a schema change upstream, or a broken deployment.
   - Extra metric idea: input-feature distribution (e.g. histogram of `study_hours`) to detect **data drift**, or
     `ml_model_info` (already exposed) to track which model version is serving.
8. Discussion point: this is **operational** monitoring (traffic, errors, latency). Model-quality monitoring needs ground-truth
   results (did the student actually pass?), and drift monitoring needs a reference distribution of inputs.
9. Commit everything:
   ```powershell
   git add .
   git commit -m "Exp 7: monitoring with Prometheus and Grafana"
   git push
   ```
   (CI from Exp 3 runs again – it should be green.)

---

## Final cleanup (do this only when all experiments are recorded)

Run from the project root unless stated.

```powershell
# Exp 7 – monitoring stack
cd monitoring
docker compose down
cd ..

# Exp 6 – Terraform-managed container
cd terraform\part2-docker
terraform plan -destroy
terraform destroy                 # type: yes
cd ..\..

# Exp 5 – Kubernetes (stop port-forward with Ctrl+C first)
kubectl delete -f k8s/service.yaml
kubectl delete -f k8s/deployment.yaml
minikube stop                     # (minikube delete to remove the cluster completely)

# Exp 5 – Docker containers
docker stop student-app mynginx
docker rm student-app mynginx
docker ps -a                      # confirm they're gone

# Exp 4 – stop the MLflow UI with Ctrl+C in its terminal

# Optional: free disk space
docker image rm student-pass-app:1.0 nginx
docker image prune
```

## Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: src` | Run commands from the project root using `python -m src.train` (not `python src/train.py`). |
| Port already in use | Another experiment is using it. Change the host port (left number in `-p 8502:8501`). |
| Pods stuck in `ErrImagePull` / `ImagePullBackOff` | Minikube: run `minikube image load student-pass-app:1.0`. Make sure the tag is exactly `1.0`. |
| Terraform: image not found | Build it first: `docker build -t student-pass-app:1.0 .` from the project root. |
| Prometheus target DOWN | Target must be `ml-app:5000` (service name), not `localhost:5000`. Check `docker compose logs ml-app`. |
| Grafana can't connect | Data source URL must be `http://prometheus:9090`. |
| GitHub Actions doesn't start | Workflow file must be in `.github/workflows/` and you pushed to `main`. |
