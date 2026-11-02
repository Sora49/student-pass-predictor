# Product Backlog – Student Pass/Fail Predictor

**Product Owner goal:** "Build a web app that predicts whether a student will pass, with at least 85% accuracy."

| ID  | User Story                                                                 | Priority | Estimate | Sprint |
|-----|----------------------------------------------------------------------------|----------|----------|--------|
| US1 | As a data engineer, I want the student dataset collected (CSV)             | High     | 20 min   | 1      |
| US2 | As a data engineer, I want the data cleaned (duplicates, missing values)   | High     | 30 min   | 1      |
| US3 | As an ML engineer, I want a Logistic Regression model trained              | High     | 30 min   | 1      |
| US4 | As a tester, I want the model accuracy evaluated (target ≥ 85%)            | Medium   | 20 min   | 1      |
| US5 | As an ML engineer, I want the model saved to `models/model.pkl`            | Medium   | 10 min   | 1      |
| US6 | As a teacher, I want a Streamlit page where I enter marks and get a result | Medium   | 30 min   | 2      |
| US7 | As a team, I want documentation (README)                                   | Low      | 20 min   | 2      |

**Why High priority first?** US1–US3 are dependencies: without data and a trained model, nothing else
(evaluation, saving, UI) can be built or demonstrated. Scrum delivers the most valuable,
blocking work first so each sprint ends with a working increment.
