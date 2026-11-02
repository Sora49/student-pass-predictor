# Sprint 1

## Scrum Team
| Member    | Role           | Responsibility in this project                              |
|-----------|----------------|-------------------------------------------------------------|
| Student 1 | Product Owner  | Defines "≥ 85% accuracy" goal, prioritises backlog, accepts work |
| Student 2 | Scrum Master   | Runs planning/daily scrum, removes blockers                 |
| Student 3 | ML Engineer    | Selects Logistic Regression, trains & saves model (`src/train.py`) |
| Student 4 | Data Engineer  | Prepares `data/raw/students.csv`, cleaning (`src/features.py`) |
| Student 5 | Tester         | Writes/runs `tests/test_model.py`, verifies accuracy        |

## Sprint Planning
- **Duration:** 1 week
- **Sprint Goal:** Build the first working ML model.

| Sprint Backlog Task | Owner         | Estimate |
|---------------------|---------------|----------|
| Collect dataset     | Data Engineer | 20 min   |
| Data cleaning       | Data Engineer | 30 min   |
| Train model         | ML Engineer   | 30 min   |
| Evaluate / test     | Tester        | 20 min   |

## Daily Scrum
| Role          | Yesterday                    | Today                    | Blockers                 |
|---------------|------------------------------|--------------------------|--------------------------|
| Product Owner | Finalised requirements       | Review sprint progress   | None                     |
| Scrum Master  | Planned the sprint           | Conduct daily scrum      | Git install issue        |
| ML Engineer   | Selected Logistic Regression | Train the model          | Dataset not ready        |
| Data Engineer | Generated student dataset    | Clean & split data       | Missing pandas library   |
| Tester        | Prepared test cases          | Evaluate accuracy        | None                     |

## Sprint Review
- [x] Dataset collected (`data/raw/students.csv`)
- [x] Data cleaned (duplicates removed, missing values filled, categories fixed)
- [x] Model trained (Logistic Regression)
- [x] Accuracy generated: **0.90** (goal ≥ 0.85 → achieved)
- Delivered: working model + source code + this documentation.

## Sprint Retrospective
| What went well       | What went wrong                   | Improvement for next sprint              |
|----------------------|-----------------------------------|------------------------------------------|
| Good communication   | Python packages were missing      | Install `requirements.txt` before sprint |
| Goal met early       | Dataset had dirty values          | Add automated data checks (tests)        |

## Sprint Increment
Working ML model · Python source code · Documentation · Accuracy report (Accuracy: 0.90)
