"""
predict.py
-----------
Loads the trained model and runs a prediction for a new user.

The user provides 6 inputs:
  age, gender, height, weight, physical_activity, family_history

The model was trained on 17 features, so we fill the remaining 11
with sensible default values (dataset averages or most common values).
"""

import os
import pickle
import numpy as np

# Path to the saved model bundle
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'obesity_model.pkl')

# We cache the model so it only loads from disk once
_model_bundle = None


def load_model():
    """Load the model from disk (only once, then cache it in memory)."""
    global _model_bundle
    if _model_bundle is None:
        with open(MODEL_PATH, 'rb') as f:
            _model_bundle = pickle.load(f)
    return _model_bundle


def predict(age, gender, height_cm, weight_kg, physical_activity, family_history):
    """
    Predict the obesity class for a user based on their 6 inputs.

    Parameters:
        age              : int   — e.g. 25
        gender           : str   — 'Male' or 'Female'
        height_cm        : float — e.g. 175.0
        weight_kg        : float — e.g. 80.0
        physical_activity: str   — 'Sedentary', 'Light', 'Moderate', 'Active', 'Very Active'
        family_history   : str   — 'Yes' or 'No'

    Returns:
        dict with:
            class_label — predicted obesity class (e.g. 'Obesity_Type_I')
            confidence  — how sure the model is (e.g. 94.5%)
            bmi         — calculated BMI value
            all_probs   — probability for each of the 7 classes
    """

    bundle = load_model()

    model            = bundle['model']
    scaler           = bundle['scaler']
    target_encoder   = bundle['label_encoder']
    feature_encoders = bundle['feature_encoders']
    feature_cols     = bundle['feature_cols']

    # ── Step 1: Compute BMI from height and weight ─────────────────────────────
    height_m = height_cm / 100.0
    bmi      = weight_kg / (height_m ** 2)

    # ── Step 2: Encode the user's categorical inputs ───────────────────────────
    # Use the same encoders that were fitted during training
    gender_encoded = feature_encoders['Gender'].transform([gender])[0]
    family_encoded = feature_encoders['family_history_with_overweight'].transform([family_history.lower()])[0]

    # ── Step 3: Map physical activity to a numeric value ──────────────────────
    # The dataset uses FAF (Physical Activity Frequency) on a 0–3 scale
    activity_to_number = {
        'Sedentary':   0.0,
        'Light':       0.75,
        'Moderate':    1.5,
        'Active':      2.25,
        'Very Active': 3.0,
    }
    faf = activity_to_number.get(physical_activity, 1.5)

    # ── Step 4: Set default values for features not collected from the user ────
    # We only ask 6 questions, but the model needs 17 features.
    # The remaining features are set to the most common / average values
    # from the dataset. This is a standard approach for limited-input forms.
    defaults = {
        'FAVC':   1,    # Frequently eats high-calorie food: 1 = Yes (most common)
        'FCVC':   2.0,  # Vegetable consumption: 2 = Sometimes (scale 1-3)
        'NCP':    3.0,  # Number of meals per day: 3 (most common)
        'CAEC':   2,    # Eating between meals: 2 = Sometimes (most common)
        'SMOKE':  0,    # Smoking: 0 = No (most common)
        'CH2O':   2.0,  # Water per day: 2 = 1-2 litres (average)
        'SCC':    0,    # Calorie monitoring: 0 = No (most common)
        'TUE':    1.0,  # Screen time: 1 hour (average)
        'CALC':   0,    # Alcohol: 0 = No (most common)
        'MTRANS': 1,    # Transport: 1 = Public Transport (most common)
    }

    # ── Step 5: Build the full feature row ────────────────────────────────────
    # Map all feature names to their values
    all_features = {
        'Gender':                          gender_encoded,
        'Age':                             float(age),
        'Height':                          height_m,
        'Weight':                          float(weight_kg),
        'family_history_with_overweight':  family_encoded,
        'FAF':                             faf,
        'BMI':                             bmi,
        **defaults
    }

    # Pull values in the exact order the model was trained on
    feature_row = [all_features.get(col, 0.0) for col in feature_cols]
    X = np.array(feature_row).reshape(1, -1)

    # ── Step 6: Scale the input (same way training data was scaled) ────────────
    X_scaled = scaler.transform(X)

    # ── Step 7: Get the prediction ─────────────────────────────────────────────
    predicted_class_number = model.predict(X_scaled)[0]
    class_probabilities    = model.predict_proba(X_scaled)[0]

    # Convert the number back to the class name
    class_label = target_encoder.inverse_transform([predicted_class_number])[0]
    confidence  = float(np.max(class_probabilities)) * 100

    # Build a dict of all 7 classes with their probabilities
    all_class_names = target_encoder.inverse_transform(range(len(class_probabilities)))
    all_probs = {
        cls: round(float(prob) * 100, 1)
        for cls, prob in zip(all_class_names, class_probabilities)
    }

    return {
        'class_label': class_label,
        'confidence':  round(confidence, 1),
        'bmi':         round(bmi, 1),
        'all_probs':   all_probs,
        'status':      'success'
    }
