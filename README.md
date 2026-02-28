# AI-Based Obesity Detection & Personalized Nutrition Recommendation System

A machine learning web application that predicts obesity levels and provides
personalized nutrition and exercise plans — built entirely with Python Flask.

---

## What It Does

1. User fills a **6-field form** (Age, Gender, Height, Weight, Physical Activity, Family History)
2. A trained **Ensemble ML model** predicts the obesity class with a confidence score
3. The system shows a **personalized Nutrition Plan** and **Exercise Plan**

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, Flask |
| Machine Learning | Scikit-learn (Random Forest, Logistic Regression, Gradient Boosting) |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Charts | Chart.js |
| Templates | Jinja2 |

---

## Project Structure

```
mini_pro/
│
├── app.py                     ← Flask web application (start here)
├── main.py                    ← Run this to train the model
│
├── data/
│   └── obesity_dataset.csv    ← Dataset (2111 rows, 17 columns)
│
├── models/
│   ├── obesity_model.pkl      ← Full model bundle (used by Flask)
│   ├── random_forest.pkl      ← Individual model files
│   ├── logistic_regression.pkl
│   ├── gradient_boosting.pkl
│   ├── ensemble_model.pkl
│   ├── preprocessor.pkl       ← Scaler + encoders
│   └── README.md
│
├── outputs/
│   ├── model_stats.json           ← Accuracy, F1, Precision, Recall
│   └── preprocessing_report.json  ← Preprocessing summary
│
├── src/
│   ├── data_preprocessing.py  ← Clean & prepare the dataset (6 steps)
│   ├── train.py               ← Train all 4 models
│   ├── predict.py             ← Run prediction for new user input
│   ├── nutrition.py           ← Nutrition plans per obesity class
│   └── exercise.py            ← Exercise plans per obesity class
│
├── static/
│   ├── css/style.css          ← All styling (dark + light theme)
│   └── js/main.js             ← Theme toggle, BMI calculator, modal
│
└── templates/
    ├── base.html              ← Layout (navbar + footer)
    ├── index.html             ← Home page
    ├── predict.html           ← Prediction form + results
    └── statistics.html        ← Model performance charts
```

---

## How to Run

### Step 1 — Install dependencies
```bash
pip install flask scikit-learn pandas numpy
```

### Step 2 — Train the model (run once)
```bash
python main.py
```
This runs the full preprocessing + training pipeline and saves all model files.

### Step 3 — Start the web app
```bash
python app.py
```

### Step 4 — Open the browser
```
http://localhost:5000
```

---

## ML Pipeline (src/ folder)

```
data/obesity_dataset.csv
        ↓
src/data_preprocessing.py   (6 steps: load → clean → outliers → BMI → encode → scale & split)
        ↓
src/train.py                (train RF + LR + GB → combine into Ensemble → save .pkl files)
        ↓
models/*.pkl                (saved for inference)
        ↓
src/predict.py              (load bundle → preprocess user input → return prediction)
```

---

## Model Results

| Model | Accuracy | F1 Score |
|-------|---------|---------|
| Random Forest | ~98.1% | ~98.1% |
| Logistic Regression | ~92.0% | ~91.9% |
| Gradient Boosting | ~98.1% | ~98.1% |
| **Ensemble (Final)** | **~98%+** | **~98%+** |

---

## Web Pages

| URL | Description |
|-----|-------------|
| `/` | Home page — project overview |
| `/predict` | Enter details → get obesity prediction + plans |
| `/statistics` | View model accuracy comparison charts |

---

## Dataset

- **Source:** UCI Machine Learning Repository
- **Records:** 2,111
- **Features:** 17 (16 input features + 1 target label)
- **Target Classes:** 7 (Insufficient Weight → Obesity Type III)
- **Missing Values:** None (pre-cleaned)

---

## Mentor
**Prof. Amiya Das** — School of Computer Engineering, KIIT University, Bhubaneswar
