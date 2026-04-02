# AI-Based Obesity Detection & Personalized Nutrition Recommendation System

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-2.3%2B-lightgrey?logo=flask)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.3%2B-orange?logo=scikit-learn)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

A machine learning web application that predicts obesity levels and generates personalized nutrition and exercise plans — built entirely with Python Flask. No external APIs are used; **all ML inference runs locally on your machine**.

---

## 📌 Table of Contents

1. [Problem Statement](#-problem-statement)
2. [Features](#-features)
3. [Demo & Screenshots](#-demo--screenshots)
4. [Prerequisites](#-prerequisites)
5. [Quick Setup & Run](#-quick-setup--run)
6. [Tech Stack](#-tech-stack)
7. [Dataset Details](#-dataset-details)
8. [Data Preprocessing Pipeline](#-data-preprocessing-pipeline)
9. [Machine Learning Architecture](#-machine-learning-architecture)
10. [Model Performance](#-model-performance)
11. [Project Structure](#-project-structure)
12. [Web Pages & API Routes](#-web-pages--api-routes)
13. [Input Validation Rules](#-input-validation-rules)
14. [Running Tests](#-running-tests)
15. [Production Deployment](#-production-deployment)
16. [Troubleshooting](#-troubleshooting)
17. [Acknowledgements](#-acknowledgements)
18. [License](#-license)
19. [Authors](#-authors)

---

## 🎯 Problem Statement

Obesity is a global health crisis affecting over 1 billion people worldwide. Early-stage identification of obesity risk is critical for timely intervention, yet access to clinical tools remains limited. This project bridges that gap by providing:

- **Automated obesity classification** using a trained Ensemble ML model across 7 clinically-defined weight categories.
- **Personalized, evidence-based nutrition and exercise recommendations** tailored to each individual's biometric profile.
- **An accessible, browser-based interface** requiring no installation on the user's side.

The system is designed as a screening aid — not a replacement for professional medical diagnosis.

---

## ✨ Features

- 🔍 **Dual Prediction Modes** — a simple 6-input form and a full 16-input advanced clinical form
- 🤖 **4-model Ensemble** — Random Forest + Logistic Regression + Gradient Boosting fused via Soft Voting
- 🍽️ **AI-personalized Nutrition Plans** — calorie and macro targets per user profile via a Local AI model
- 🏃 **Dynamic Exercise Plans** — class-specific workout routines with duration, intensity, and safety notes
- 📊 **Live Statistics Dashboard** — accuracy metrics, confusion matrix heatmap, radar and bar charts
- 📥 **CSV Report Export** — downloadable personalized health report post-prediction
- 📚 **Clinical Education Hub** — the `/learn` page covering obesity types, prevention, and management
- 🔄 **In-browser Retraining** — model can be retrained via AJAX without leaving the dashboard
- ✅ **Full Input Validation** — both server-side and client-side validation with clear error messages

---

## 🖼️ Demo & Screenshots

> **Live Demo:** Run locally at `http://localhost:5000` after completing the Quick Setup below.

| Page | Description |
|---|---|
| **Home (`/`)** | Model status, obesity class cards, quick overview |
| **Predict (`/predict`)** | 6-field form → instant prediction with confidence score |
| **Advanced (`/advance`)** | 16-field clinical form → full-feature prediction |
| **Statistics (`/statistics`)** | Accuracy metrics, 7×7 confusion matrix, feature importance chart |
| **Learn (`/learn`)** | Obesity classification guide, prevention tips, clinical precautions |

---

## ✅ Prerequisites

Before you begin, ensure you have the following installed:

| Requirement | Version | Check Command |
|---|---|---|
| **Python** | 3.10 or higher | `python --version` |
| **pip** | Latest | `pip --version` |
| **Git** | Any | `git --version` |

> **Recommended:** Use a virtual environment to avoid dependency conflicts.

---

## 🚀 Quick Setup & Run

**Step 1 — Clone the repository**
```bash
git clone https://github.com/AAmardeep15/obesity-ai-detection.git
cd obesity-ai-detection
```

**Step 2 — Create and activate a virtual environment**
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python -m venv .venv
source .venv/bin/activate
```

**Step 3 — Install dependencies**
```bash
pip install -r requirements.txt
```

**Step 4 — Train the Machine Learning Models** *(Run once)*
```bash
python main.py
```
*This script cleans the data, trains 4 different models on the 10,000-row dataset, and saves the final Ensemble bundle to `models/obesity_model.pkl`.*

**Step 5 — Start the Web Application**
```bash
python app.py
```
Open your browser and navigate to: **`http://localhost:5000`**

---

### ⚙️ Environment Variables (Optional)

Create a `.env` file or export these variables to customize the server:

| Variable | Default | Description |
|---|---|---|
| `FLASK_SECRET_KEY` | `dev-only-change-me` | Flask session secret key — **change this in production** |
| `FLASK_DEBUG` | `0` | Set to `1` to enable debug mode (never use in production) |
| `FLASK_HOST` | `0.0.0.0` | Host address for the Flask server |
| `FLASK_PORT` | `5000` | Port number for the Flask server |

---

## 🛠️ Tech Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| Backend | Python, Flask | 3.10+, ≥ 2.3.0 |
| Machine Learning | Scikit-learn | ≥ 1.3.0 |
| Data Processing | Pandas, NumPy | ≥ 2.0.0, ≥ 1.24.0 |
| Frontend | HTML5, CSS3, Vanilla JavaScript | — |
| Visualizations | Chart.js | CDN |
| Production Server | Gunicorn | ≥ 21.2.0 |

---

## 📂 Dataset Details

| Property | Value |
|---|---|
| Primary File | `data/obesity_dataset.csv` |
| Rows | ~10,000 (synthetically augmented) |
| Columns / Features | 17 (16 input features + 1 target label) |
| Target Column | `NObeyesdad` |
| Supplementary File | `data/synthetic_nutrition_data.csv` — used to train the Local Nutrition AI |

### The 17 Dataset Features

| Column | Type | Description |
|---|---|---|
| `Gender` | Categorical | Male / Female |
| `Age` | Numeric | Age in years |
| `Height` | Numeric | Height in metres |
| `Weight` | Numeric | Weight in kg |
| `family_history_with_overweight` | Categorical | Yes / No |
| `FAVC` | Categorical | Frequent consumption of high caloric food |
| `FCVC` | Numeric | Frequency of vegetable consumption (1–3 scale) |
| `NCP` | Numeric | Number of main meals per day (1–6) |
| `CAEC` | Categorical | Eating between meals (Always / Frequently / Sometimes / No) |
| `SMOKE` | Categorical | Smoker — Yes / No |
| `CH2O` | Numeric | Daily water intake (0–3 scale) |
| `SCC` | Categorical | Calorie monitoring — Yes / No |
| `FAF` | Numeric | Physical Activity Frequency (0–3 scale) |
| `TUE` | Numeric | Daily technology use time (0–3 scale) |
| `CALC` | Categorical | Alcohol consumption frequency |
| `MTRANS` | Categorical | Primary mode of transportation |
| `NObeyesdad` | **Target** | Obesity class label (7 classes) |

### The 7 Obesity Classification Classes

| Internal Key | Display Label | Severity |
|---|---|---|
| `Insufficient_Weight` | Insufficient Weight | Below Normal |
| `Normal_Weight` | Normal Weight | Healthy |
| `Overweight_Level_I` | Overweight Level I | Mild Risk |
| `Overweight_Level_II` | Overweight Level II | Moderate Risk |
| `Obesity_Type_I` | Obesity Type I | High Risk |
| `Obesity_Type_II` | Obesity Type II | Very High Risk |
| `Obesity_Type_III` | Obesity Type III (Morbid Obesity) | Critical Risk |

---

## 🔄 Data Preprocessing Pipeline

The pipeline runs automatically when `python main.py` is executed (via `src/data_preprocessing.py`).

| Step | Action | Method |
|---|---|---|
| 1 | **Load Data** | Reads CSV, prints class distribution |
| 2 | **Fill Missing Values** | Numeric → column **mean**; Categorical → column **mode** |
| 3 | **Outlier Capping** | IQR method — values outside `Q1 − 1.5×IQR` / `Q3 + 1.5×IQR` are **capped**, not removed |
| 4 | **Feature Engineering** | Adds a derived **BMI column** (`Weight / Height²`) as a clinical indicator |
| 5 | **Label Encoding** | `sklearn.LabelEncoder` converts categorical columns to integers; encoders saved for inference |
| 6 | **Standard Scaling** | `StandardScaler` (mean=0, std=1) — fitted on **training data only** to prevent data leakage |
| 7 | **Train/Test Split** | 80% train / 20% test, stratified split with `random_state=42` |

> **Inference Defaults:** The 10 features not collected via the 6-field basic form are auto-filled using precomputed defaults from training data (numeric → **median**, categorical → **mode**). These are stored in `obesity_model.pkl` for consistency.

---

## 🤖 Machine Learning Architecture

### Two Prediction Modes

| Mode | Input Fields | Description |
|---|---|---|
| **Basic** | 6 fields | Age, Gender, Height, Weight, Activity, Family History — remaining 10 features auto-imputed |
| **Advanced** | 16 fields | All dataset features provided by the user — full clinical-grade prediction |

### Base Models & Hyperparameters

| Model | Configuration |
|---|---|
| **Random Forest** | `n_estimators=200`, `random_state=42`, `n_jobs=-1` |
| **Logistic Regression** | `max_iter=1000`, `random_state=42` |
| **Gradient Boosting** | `n_estimators=200`, `random_state=42` |

### Ensemble Strategy
A **Soft Voting Classifier** (`sklearn.ensemble.VotingClassifier`) averages the class probability outputs of all three models, selecting the class with the highest mean probability. This reduces individual model variance and improves generalization.

### Model Bundle Schema (`obesity_model.pkl`)

The saved bundle is a single serialized Python dictionary with everything needed for inference:

```python
{
  'model'             : VotingClassifier (Ensemble of all 3 models),
  'scaler'            : Fitted StandardScaler,
  'label_encoder'     : LabelEncoder for the target column,
  'feature_encoders'  : { col: LabelEncoder } per categorical feature,
  'feature_cols'      : Ordered list of feature column names,
  'inference_defaults': Precomputed defaults for the 10 imputed features,
  'metadata'          : { schema_version, model_version, created_at, schema_hash },
  'stats'             : { accuracy, f1, confusion_matrix, feature_importance, ... }
}
```

### Local Nutrition AI Model (`nutrition_model.pkl`)
A separate ML model trained on `data/synthetic_nutrition_data.csv` that predicts personalized macronutrient targets per user:
- **Daily calorie target (kcal)**
- **Protein (g)**, **Carbohydrates (g)**, **Fat (g)**

Inputs: Age, Gender, Height, Weight, Activity Level, Predicted Obesity Class.

---

## 📊 Model Performance

| Model | Accuracy | F1 Score | Precision | Recall |
|-------|---------|---------|---------|---------|
| Random Forest | ~84% | ~84% | ~84% | ~84% |
| Logistic Regression | ~62% | ~61% | ~62% | ~62% |
| Gradient Boosting | ~81% | ~81% | ~81% | ~81% |
| **Ensemble (Soft Voting)** | **~84.5%** | **~84.5%** | **~84.5%** | **~84.5%** |

> *Accuracy is deliberately targeted at ~84.5% as the "Golden Mean" — robust enough for real-world generalization while avoiding overfitting artifacts common in 99%+ accuracy models on synthetic data.*

All metrics are computed on the **held-out 20% test set** and saved automatically to `outputs/model_stats.json` alongside:
- **7×7 Confusion Matrix** (Ensemble model)
- **Feature Importance rankings** (from Random Forest)

---

## 📁 Project Structure

```text
obesity-ai-detection/
│
├── app.py                      ← Flask web application entry point
├── main.py                     ← Train all ML models (run this first)
├── requirements.txt            ← Python dependency list
├── test_nutrition_ai.py        ← Unit tests for the Nutrition AI module
│
├── data/
│   ├── obesity_dataset.csv             ← Main dataset (10,000 rows, 17 columns)
│   └── synthetic_nutrition_data.csv    ← Nutrition AI training data
│
├── models/                     ← Auto-generated by main.py (not tracked by Git)
│   ├── obesity_model.pkl       ← Full Ensemble bundle (loaded by Flask at runtime)
│   ├── ensemble_model.pkl      ← Standalone Soft Voting ensemble
│   ├── random_forest.pkl       ← Standalone Random Forest
│   ├── gradient_boosting.pkl   ← Standalone Gradient Boosting
│   ├── logistic_regression.pkl ← Standalone Logistic Regression
│   ├── nutrition_model.pkl     ← Local AI for calorie/macro recommendations
│   └── preprocessor.pkl        ← Standalone scaler + encoders bundle
│
├── outputs/                    ← Auto-generated by main.py
│   ├── model_stats.json            ← Accuracy, F1, Confusion Matrix, Feature Importance
│   └── preprocessing_report.json   ← Preprocessing summary (outliers, class counts)
│
├── src/
│   ├── __init__.py
│   ├── data_preprocessing.py   ← Full 7-step data preparation pipeline
│   ├── train.py                ← Model training + Soft Voting Ensemble compilation
│   ├── predict.py              ← Real-time inference (Basic & Advanced modes)
│   ├── nutrition.py            ← Nutrition AI + static meal plans per obesity class
│   ├── exercise.py             ← Exercise plans and workout mappings per obesity class
│   ├── generate_nutrition_data.py  ← Generates synthetic nutrition training data
│   └── train_nutrition.py      ← Trains the Local Nutrition AI model
│
├── static/
│   ├── css/                    ← Stylesheet files
│   ├── js/
│   │   └── main.js             ← Frontend logic: form handling, Chart.js rendering
│   ├── images/                 ← Project images
│   └── img/                    ← Additional image assets
│
└── templates/
    ├── base.html               ← Shared base layout and navigation
    ├── index.html              ← Home page: model status + obesity class overview
    ├── predict.html            ← Basic 6-input prediction form + result display
    ├── advance.html            ← Advanced 16-input prediction form + result display
    ├── statistics.html         ← Live stats: confusion matrix, radar & bar charts
    └── learn.html              ← Clinical education: obesity types, prevention, FAQ
```

---

## 🌐 Web Pages & API Routes

| Route | Method(s) | Description |
|-----|-----|-----|
| `/` | GET | Home page — project overview, obesity class cards, model status badge |
| `/predict` | GET, POST | Basic 6-input prediction → obesity class, confidence score, nutrition & exercise plan |
| `/advance` | GET, POST | Advanced 16-input prediction → full clinical-grade prediction |
| `/statistics` | GET | Live model metrics: accuracy, 7×7 confusion matrix, feature importance chart |
| `/learn` | GET | Clinical education hub — obesity types, prevention, clinical precautions |
| `/download-report` | POST | Generate and download a personalized CSV health report |
| `/train` | POST | Trigger model retraining via AJAX from the dashboard (returns JSON stats) |
| `/api/exercise` | GET | JSON API — returns the exercise plan for a given `?class=` query parameter |

---

## 🛡️ Input Validation Rules

All inputs are validated **server-side** in `app.py` and `src/predict.py`.

| Field | Type | Accepted Range / Values |
|---|---|---|
| Age | Integer | 10 – 80 years |
| Gender | String | `Male` or `Female` |
| Height | Float | 100 – 220 cm |
| Weight | Float | 20 – 250 kg |
| Physical Activity | String | `Sedentary`, `Light`, `Moderate`, `Active`, `Very Active` |
| Family History | String | `Yes` or `No` |
| FCVC *(Advanced)* | Float | 1.0 – 3.0 |
| NCP *(Advanced)* | Float | 1.0 – 6.0 |
| CH2O *(Advanced)* | Float | 0.0 – 3.0 |
| TUE *(Advanced)* | Float | 0.0 – 3.0 |

---

## 🧪 Running Tests

A unit test file is included to verify the Nutrition AI module behaves correctly:

```bash
python -m pytest test_nutrition_ai.py -v
```

Or run it directly:
```bash
python test_nutrition_ai.py
```

> **Note:** Run `python main.py` first to ensure model files exist before running tests.

---

## 🚢 Production Deployment

For production use, replace Flask's built-in server with **Gunicorn** (already included in `requirements.txt`):

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

| Flag | Value | Meaning |
|---|---|---|
| `-w` | `4` | 4 worker processes (adjust based on server CPU cores) |
| `-b` | `0.0.0.0:5000` | Bind address and port |

> **Security reminder:** Always set `FLASK_SECRET_KEY` to a strong, random string and keep `FLASK_DEBUG=0` in production.

---

## 🔧 Troubleshooting

| Problem | Cause | Solution |
|---|---|---|
| `FileNotFoundError: obesity_model.pkl` | Models haven't been trained yet | Run `python main.py` first |
| `ModuleNotFoundError` | Dependencies not installed | Run `pip install -r requirements.txt` |
| Port 5000 already in use | Another process is using port 5000 | Set `FLASK_PORT=5001` or kill the conflicting process |
| `X does not have valid feature names` warning | Minor scikit-learn version mismatch | Safe to ignore; predictions still work correctly |
| Low prediction confidence (<50%) | Unusual or borderline input values | Try the Advanced mode with more detailed inputs |
| Charts not loading on `/statistics` | Model stats file missing | Run `python main.py` to regenerate `outputs/model_stats.json` |

---

## 🙏 Acknowledgements

- **Dataset:** Inspired by the [UCI Obesity Dataset](https://archive.ics.uci.edu/dataset/544/estimation+of+obesity+levels+based+on+eating+habits+and+physical+condition) — "Estimation of Obesity Levels Based on Eating Habits and Physical Condition" by Fabio Mendoza Palechor & Alexis de la Hoz Manotas (2019).
- **Visualization:** [Chart.js](https://www.chartjs.org/) — Interactive charts on the Statistics dashboard.
- **ML Framework:** [Scikit-learn](https://scikit-learn.org/) — The backbone of the entire ML pipeline.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors

**Amardeep** — Developer & ML Engineer  
GitHub: [@AAmardeep15](https://github.com/AAmardeep15)

**Mentor:** Prof. Amiya Kumar Das  
School of Computer Engineering, KIIT University, Bhubaneswar
