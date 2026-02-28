"""
train.py
---------
Trains the machine learning models and saves them to the models/ folder.

What this script does:
  1. Calls data_preprocessing.py to load and clean the data
  2. Trains 3 individual ML models (Random Forest, Logistic Regression, Gradient Boosting)
  3. Combines them into one final Ensemble model using Soft Voting
  4. Evaluates each model on the test set and prints accuracy
  5. Saves all model files to the models/ folder
  6. Saves accuracy numbers to outputs/model_stats.json
"""

import os
import sys
import json
import pickle

# Make sure the project root is on Python's path (needed when running main.py)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

from src.data_preprocessing import load_and_preprocess

# ── Output folder paths ────────────────────────────────────────────────────────
ROOT_DIR   = os.path.join(os.path.dirname(__file__), '..')
MODEL_DIR  = os.path.join(ROOT_DIR, 'models')
OUTPUT_DIR = os.path.join(ROOT_DIR, 'outputs')


# ── Helper: Evaluate one model ────────────────────────────────────────────────

def evaluate_model(model, X_test, y_test, model_name):
    """
    Run the model on test data and print accuracy, F1, precision, recall.
    Returns a dictionary with the numbers.
    """
    y_pred     = model.predict(X_test)
    accuracy   = accuracy_score(y_test, y_pred)
    f1         = f1_score(y_test, y_pred, average='weighted', zero_division=0)
    precision  = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    recall     = recall_score(y_test, y_pred, average='weighted', zero_division=0)

    print(f"  {model_name:<25}  "
          f"Accuracy={accuracy*100:.2f}%  "
          f"F1={f1*100:.2f}%")

    return {
        'accuracy':  round(accuracy,  4),
        'f1':        round(f1,        4),
        'precision': round(precision, 4),
        'recall':    round(recall,    4),
    }


# ── Helper: Save a Python object as a .pkl file ───────────────────────────────

def save_pkl(obj, filename):
    """Save any Python object to the models/ folder as a .pkl file."""
    path = os.path.join(MODEL_DIR, filename)
    with open(path, 'wb') as f:
        pickle.dump(obj, f)
    print(f"  Saved → models/{filename}")


# ── Main Training Function ────────────────────────────────────────────────────

def train():
    """
    Full training pipeline.
    Returns the model bundle (used by Flask app) and the stats dictionary.
    """

    # ── Step 1: Get preprocessed data ─────────────────────────────────────────
    X_train, X_test, y_train, y_test, info = load_and_preprocess()

    scaler           = info['scaler']
    feature_encoders = info['feature_encoders']
    target_encoder   = info['label_encoder']
    feature_cols     = info['feature_cols']

    # ── Step 2: Train the 3 base models ───────────────────────────────────────
    print("=" * 55)
    print("  MODEL TRAINING")
    print("=" * 55)

    # Model 1 — Random Forest
    # Builds 200 decision trees and combines their votes
    print("\n  Training Random Forest...")
    rf = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
    rf.fit(X_train, y_train)

    # Model 2 — Logistic Regression
    # Finds a mathematical line/boundary that separates classes
    print("  Training Logistic Regression...")
    lr = LogisticRegression(max_iter=1000, random_state=42)
    lr.fit(X_train, y_train)

    # Model 3 — Gradient Boosting
    # Builds trees one after another, each fixing the previous one's mistakes
    print("  Training Gradient Boosting...")
    gb = GradientBoostingClassifier(n_estimators=200, random_state=42)
    gb.fit(X_train, y_train)

    # Model 4 — Ensemble (Soft Voting)
    # Averages the probability outputs of all 3 models above
    print("  Training Ensemble (Soft Voting of all 3 models)...")
    ensemble = VotingClassifier(
        estimators=[('rf', rf), ('lr', lr), ('gb', gb)],
        voting='soft'
    )
    ensemble.fit(X_train, y_train)

    # ── Step 3: Evaluate all models ────────────────────────────────────────────
    print("\n" + "=" * 55)
    print("  EVALUATION RESULTS (on test set)")
    print("=" * 55)

    rf_stats  = evaluate_model(rf,       X_test, y_test, "Random Forest")
    lr_stats  = evaluate_model(lr,       X_test, y_test, "Logistic Regression")
    gb_stats  = evaluate_model(gb,       X_test, y_test, "Gradient Boosting")
    ens_stats = evaluate_model(ensemble, X_test, y_test, "Ensemble (Voting)")

    # Collect all stats
    stats = {
        'rf':        rf_stats,
        'lr':        lr_stats,
        'gb':        gb_stats,
        'ensemble':  ens_stats,
        'class_names':  list(target_encoder.classes_),
        'num_features': len(feature_cols),
        'train_size':   int(X_train.shape[0]),
        'test_size':    int(X_test.shape[0]),
    }

    # ── Step 4: Save model files ───────────────────────────────────────────────
    print("\n" + "=" * 55)
    print("  SAVING MODEL FILES")
    print("=" * 55)

    os.makedirs(MODEL_DIR,  exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Save each model individually (for easy inspection)
    save_pkl(rf,       'random_forest.pkl')
    save_pkl(lr,       'logistic_regression.pkl')
    save_pkl(gb,       'gradient_boosting.pkl')
    save_pkl(ensemble, 'ensemble_model.pkl')

    # Save preprocessor separately (scaler + encoders + column order)
    preprocessor = {
        'scaler':           scaler,
        'feature_encoders': feature_encoders,
        'label_encoder':    target_encoder,
        'feature_cols':     feature_cols,
    }
    save_pkl(preprocessor, 'preprocessor.pkl')

    # Save the full bundle that the Flask app uses (model + preprocessor together)
    full_bundle = {
        'model':            ensemble,
        'scaler':           scaler,
        'label_encoder':    target_encoder,
        'feature_encoders': feature_encoders,
        'feature_cols':     feature_cols,
        'stats':            stats,
    }
    save_pkl(full_bundle, 'obesity_model.pkl')

    # Save accuracy stats as JSON for the Statistics page
    stats_path = os.path.join(OUTPUT_DIR, 'model_stats.json')
    with open(stats_path, 'w') as f:
        json.dump(stats, f, indent=2)
    print(f"  Saved → outputs/model_stats.json")

    print()
    return full_bundle, stats


# ── Standalone run ────────────────────────────────────────────────────────────
if __name__ == '__main__':
    train()
