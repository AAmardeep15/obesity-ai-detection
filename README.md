# AI-Based Obesity Detection & Personalized Nutrition Recommendation System

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-2.3%2B-lightgrey?logo=flask)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.3%2B-orange?logo=scikit-learn)
![License](https://img.shields.io/badge/License-MIT-green)

A machine learning web application that classifies obesity levels and generates personalized nutrition and exercise plans — built with Python Flask. All ML inference runs locally; no external APIs required.

---

## 🚀 Quick Start

> **Prerequisite:** Python 3.10+

```bash
# 1. Clone and enter the project
git clone https://github.com/AAmardeep15/obesity-ai-detection.git
cd obesity-ai-detection

# 2. Create a virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Train the models (run once)
python main.py

# 5. Start the app
python app.py
```

Open **`http://localhost:5000`** in your browser.

---

## What It Does

1. User fills a **6-field form** (Age, Gender, Height, Weight, Activity Level, Family History).
2. The remaining 11 features are **auto-imputed** using dataset medians/modes.
3. A **Soft Voting Ensemble** (Random Forest + Logistic Regression + Gradient Boosting) predicts the obesity class with a confidence score.
4. A **Local AI nutrition model** generates personalized daily calorie and macronutrient targets.
5. A matching **Exercise Plan** is returned for the predicted class.
6. The full report is **downloadable as a CSV**.

> An **Advanced Mode** is also available at `/advance` — accepts all 16 features directly for clinical-grade prediction.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, Flask ≥ 2.3 |
| Machine Learning | Scikit-learn ≥ 1.3 (RF, LR, GB, VotingClassifier) |
| Data Processing | Pandas ≥ 2.0, NumPy ≥ 1.24 |
| Frontend | HTML5, CSS3, Vanilla JavaScript, Chart.js |
| Production | Gunicorn ≥ 21.2 |

---

## Model Performance

Trained on a 10,000-row synthetically augmented dataset across **7 obesity classes**.

| Model | Accuracy | F1 Score |
|-------|---------|---------|
| Random Forest | ~84% | ~84% |
| Logistic Regression | ~62% | ~61% |
| Gradient Boosting | ~81% | ~81% |
| **Ensemble (Soft Voting)** | **~84.5%** | **~84.5%** |

Evaluation metrics (Accuracy, F1, Precision, Recall, Confusion Matrix, Feature Importance) are saved to `outputs/model_stats.json` after training.

---

## Web Pages

| Route | Description |
|-------|-------------|
| `/` | Home — model status and obesity class overview |
| `/predict` | Basic 6-input prediction + results |
| `/advance` | Advanced 16-input clinical prediction |
| `/statistics` | Live model metrics, confusion matrix, charts |
| `/learn` | Clinical education — obesity types and prevention |

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `obesity_model.pkl not found` | Run `python main.py` first |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| Port 5000 in use | Set `FLASK_PORT=5001` |
| Charts missing on `/statistics` | Run `python main.py` to regenerate stats |

---

## Acknowledgements

- Dataset inspired by the [UCI Obesity Dataset](https://archive.ics.uci.edu/dataset/544/estimation+of+obesity+levels+based+on+eating+habits+and+physical+condition) — Palechor & de la Hoz Manotas (2019)
- Visualizations: [Chart.js](https://www.chartjs.org/)

---

**Mentor:** Prof. Amiya Kumar Das — School of Computer Engineering, KIIT University, Bhubaneswar  
**Developer:** [@AAmardeep15](https://github.com/AAmardeep15)
