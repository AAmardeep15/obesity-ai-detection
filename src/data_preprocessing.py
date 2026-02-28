"""
data_preprocessing.py
----------------------
Step-by-step data cleaning and preparation for the ML model.

Steps:
  1. Load the raw CSV dataset
  2. Check and fill any missing values
  3. Detect and cap extreme outliers
  4. Add a BMI column (Weight / Height²)
  5. Convert text columns to numbers (Label Encoding)
  6. Scale all values to the same range (StandardScaler)
  7. Split data into Training set and Test set

Run this file standalone to see the full preprocessing report:
    python -m src.data_preprocessing
"""

import os
import json
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split

# ── File paths ─────────────────────────────────────────────────────────────────
ROOT_DIR    = os.path.join(os.path.dirname(__file__), '..')
DATA_PATH   = os.path.join(ROOT_DIR, 'data',    'obesity_dataset.csv')
REPORT_PATH = os.path.join(ROOT_DIR, 'outputs', 'preprocessing_report.json')

# ── Column names ───────────────────────────────────────────────────────────────
# These are the text (categorical) columns in the dataset
CATEGORICAL_COLS = [
    'Gender', 'family_history_with_overweight',
    'FAVC', 'CAEC', 'SMOKE', 'SCC', 'CALC', 'MTRANS'
]

# These are the number (numeric) columns in the dataset
NUMERIC_COLS = ['Age', 'Height', 'Weight', 'FCVC', 'NCP', 'CH2O', 'FAF', 'TUE']

# This is the column we want to predict
TARGET_COL = 'NObeyesdad'


# ── Step 1: Load Dataset ──────────────────────────────────────────────────────

def load_data():
    """Load the CSV file and print a quick summary."""

    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(
            f"Dataset not found at: {DATA_PATH}\n"
            "Please place obesity_dataset.csv inside the data/ folder."
        )

    df = pd.read_csv(DATA_PATH)

    print("=" * 55)
    print("  STEP 1 — Dataset Loaded")
    print("=" * 55)
    print(f"  Rows    : {df.shape[0]}")
    print(f"  Columns : {df.shape[1]}")
    print()
    print("  Target class distribution:")
    for label, count in df[TARGET_COL].value_counts().items():
        pct = count / len(df) * 100
        print(f"    {label:<30}  {count}  ({pct:.1f}%)")
    print()

    return df


# ── Step 2: Handle Missing Values ────────────────────────────────────────────

def fill_missing_values(df):
    """
    Fill any empty/null cells:
    - Number columns  → fill with the column MEAN (average)
    - Text columns    → fill with the column MODE (most common value)
    """

    print("=" * 55)
    print("  STEP 2 — Missing Value Check")
    print("=" * 55)

    total_missing = df.isnull().sum().sum()

    if total_missing == 0:
        print("  No missing values found. Dataset is already clean.\n")
        return df

    print(f"  Found {total_missing} missing values. Filling now...\n")

    # Fill number columns with mean
    for col in NUMERIC_COLS:
        if col in df.columns and df[col].isnull().any():
            mean_value = df[col].mean()
            df[col] = df[col].fillna(mean_value)
            print(f"  Filled '{col}' with MEAN = {mean_value:.2f}")

    # Fill text columns with mode (most frequent value)
    for col in CATEGORICAL_COLS:
        if col in df.columns and df[col].isnull().any():
            mode_value = df[col].mode()[0]
            df[col] = df[col].fillna(mode_value)
            print(f"  Filled '{col}' with MODE = {mode_value}")

    # Remove rows where the target label is missing
    df = df.dropna(subset=[TARGET_COL])
    print()

    return df


# ── Step 3: Handle Outliers ──────────────────────────────────────────────────

def handle_outliers(df):
    """
    Detect extreme values using the IQR method and cap them.

    IQR (Interquartile Range) Method:
      - Lower bound = Q1 - 1.5 × IQR
      - Upper bound = Q3 + 1.5 × IQR
      - Values outside these bounds are capped (not deleted)

    We cap instead of delete so we don't lose data samples.
    """

    print("=" * 55)
    print("  STEP 3 — Outlier Detection (IQR Method)")
    print("=" * 55)

    outlier_report = {}

    for col in NUMERIC_COLS:
        if col not in df.columns:
            continue

        Q1  = df[col].quantile(0.25)
        Q3  = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        outliers_found = int(((df[col] < lower) | (df[col] > upper)).sum())

        if outliers_found > 0:
            df[col] = df[col].clip(lower, upper)
            print(f"  {col:<12}  {outliers_found} outliers capped  "
                  f"(range: {lower:.2f} to {upper:.2f})")
            outlier_report[col] = outliers_found
        else:
            print(f"  {col:<12}  No outliers found")

    print()
    return df, outlier_report


# ── Step 4: Feature Engineering — Add BMI ───────────────────────────────────

def add_bmi(df):
    """
    Add a BMI column calculated from Height and Weight.
    BMI = Weight (kg) / Height (m)²

    BMI is a key clinical indicator for obesity and improves model accuracy.
    """

    print("=" * 55)
    print("  STEP 4 — Feature Engineering (Add BMI)")
    print("=" * 55)

    df['BMI'] = df['Weight'] / (df['Height'] ** 2)

    print(f"  BMI column added.")
    print(f"  Min BMI  = {df['BMI'].min():.2f}")
    print(f"  Max BMI  = {df['BMI'].max():.2f}")
    print(f"  Mean BMI = {df['BMI'].mean():.2f}")
    print()

    return df


# ── Step 5: Label Encoding ───────────────────────────────────────────────────

def encode_labels(df):
    """
    Convert text columns to numbers so the ML model can read them.

    Example: Gender → Male=1, Female=0
             CAEC   → Always=0, Frequently=1, Sometimes=2, no=3

    We save the encoder objects so we can apply the same conversion
    to new user inputs during prediction.
    """

    print("=" * 55)
    print("  STEP 5 — Label Encoding (Text → Numbers)")
    print("=" * 55)

    encoders = {}

    # Encode each categorical feature column
    for col in CATEGORICAL_COLS:
        if col not in df.columns:
            continue
        encoder = LabelEncoder()
        df[col] = encoder.fit_transform(df[col].astype(str))
        encoders[col] = encoder
        print(f"  Encoded '{col}'  →  classes: {list(encoder.classes_)}")

    # Encode the target column
    target_encoder = LabelEncoder()
    df[TARGET_COL] = target_encoder.fit_transform(df[TARGET_COL].astype(str))

    print(f"\n  Target classes: {list(target_encoder.classes_)}")
    print()

    return df, encoders, target_encoder


# ── Step 6 & 7: Scale + Split ────────────────────────────────────────────────

def scale_and_split(df, feature_cols):
    """
    Step 6: Scale all numbers to the same range using StandardScaler.
            This ensures no single feature dominates due to its large values.

    Step 7: Split data into:
            - Training set (80%) — used to teach the model
            - Test set     (20%) — used to evaluate the model

    IMPORTANT: We fit the scaler on TRAINING data only.
    If we fit it on all data, the model would "see" test data during training,
    which gives falsely high accuracy. This is called Data Leakage.
    """

    print("=" * 55)
    print("  STEP 6 & 7 — Scaling + Train/Test Split")
    print("=" * 55)

    X = df[feature_cols].values.astype(float)
    y = df[TARGET_COL].values

    # Split first (80% train, 20% test) — stratified keeps class proportions equal
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    # Scale: fit ONLY on training data to avoid data leakage
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test  = scaler.transform(X_test)   # only transform, not fit

    print(f"  Training samples : {X_train.shape[0]}")
    print(f"  Test samples     : {X_test.shape[0]}")
    print(f"  Features used    : {X_train.shape[1]}")
    print(f"  Scaling          : StandardScaler (mean=0, std=1)")
    print(f"  Data Leakage     : Prevented (scaler fit on train only)")
    print()

    return X_train, X_test, y_train, y_test, scaler


# ── Main Pipeline ─────────────────────────────────────────────────────────────

def load_and_preprocess():
    """
    Run the complete preprocessing pipeline in one call.

    Returns:
        X_train, X_test  — input features (numpy arrays, scaled)
        y_train, y_test  — target labels (numpy arrays)
        info             — dict with scaler, encoders, and column names
    """

    # Run all steps in order
    df                          = load_data()
    df                          = fill_missing_values(df)
    df, outlier_report          = handle_outliers(df)
    df                          = add_bmi(df)
    df, encoders, target_encoder = encode_labels(df)

    # All columns except the target become features
    feature_cols = [col for col in df.columns if col != TARGET_COL]

    X_train, X_test, y_train, y_test, scaler = scale_and_split(df, feature_cols)

    # Package all info needed later for inference (prediction)
    info = {
        'scaler':           scaler,
        'feature_encoders': encoders,
        'label_encoder':    target_encoder,
        'feature_cols':     feature_cols,
    }

    # Save a simple preprocessing report to outputs/
    report = {
        'train_samples': int(X_train.shape[0]),
        'test_samples':  int(X_test.shape[0]),
        'num_features':  int(X_train.shape[1]),
        'feature_cols':  feature_cols,
        'class_names':   list(target_encoder.classes_),
        'outliers_capped': outlier_report,
    }
    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    with open(REPORT_PATH, 'w') as f:
        json.dump(report, f, indent=2)

    print("=" * 55)
    print("  PREPROCESSING COMPLETE")
    print("=" * 55)
    print()

    return X_train, X_test, y_train, y_test, info


# ── Standalone run ────────────────────────────────────────────────────────────
if __name__ == '__main__':
    load_and_preprocess()
