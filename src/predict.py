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

MODEL_SCHEMA_VERSION = 1
REQUIRED_BUNDLE_KEYS = {
    'model', 'scaler', 'label_encoder', 'feature_encoders', 'feature_cols'
}

VALID_GENDERS = {'Male', 'Female'}
VALID_PHYSICAL_ACTIVITY = {
    'Sedentary', 'Light', 'Moderate', 'Active', 'Very Active'
}
VALID_FAMILY_HISTORY = {'yes', 'no'}

# Backward-compatible fallback for bundles trained before inference defaults were persisted.
LEGACY_DEFAULTS = {
    'FAVC': 1.0,
    'FCVC': 2.0,
    'NCP': 3.0,
    'CAEC': 2.0,
    'SMOKE': 0.0,
    'CH2O': 2.0,
    'SCC': 0.0,
    'TUE': 1.0,
    'CALC': 0.0,
    'MTRANS': 1.0,
}

ADVANCED_REQUIRED_FIELDS = {
    'age', 'gender', 'height', 'weight', 'family_history', 'physical_activity',
    'favc', 'fcvc', 'ncp', 'caec', 'smoke', 'ch2o', 'scc', 'tue', 'calc', 'mtrans'
}


def validate_inputs(age, gender, height_cm, weight_kg, physical_activity, family_history):
    """Validate and normalize user inputs before inference."""
    if not (10 <= int(age) <= 80):
        raise ValueError('Age must be between 10 and 80 years.')
    if not (100.0 <= float(height_cm) <= 220.0):
        raise ValueError('Height must be between 100 and 220 cm.')
    if not (20.0 <= float(weight_kg) <= 250.0):
        raise ValueError('Weight must be between 20 and 250 kg.')
    if gender not in VALID_GENDERS:
        raise ValueError("Gender must be 'Male' or 'Female'.")
    if physical_activity not in VALID_PHYSICAL_ACTIVITY:
        raise ValueError('Physical activity level is invalid.')

    family_history_normalized = str(family_history).strip().lower()
    if family_history_normalized not in VALID_FAMILY_HISTORY:
        raise ValueError("Family history must be 'Yes' or 'No'.")

    return {
        'age': int(age),
        'gender': gender,
        'height_cm': float(height_cm),
        'weight_kg': float(weight_kg),
        'physical_activity': physical_activity,
        'family_history': family_history_normalized,
    }


def validate_model_bundle(bundle):
    """Validate that model bundle contains expected keys and compatible metadata."""
    missing = REQUIRED_BUNDLE_KEYS - set(bundle.keys())
    if missing:
        raise ValueError(f'Model bundle is missing required keys: {sorted(missing)}')

    metadata = bundle.get('metadata')
    if metadata is not None:
        schema_version = metadata.get('schema_version')
        if schema_version != MODEL_SCHEMA_VERSION:
            raise ValueError(
                f'Unsupported model schema version {schema_version}; expected {MODEL_SCHEMA_VERSION}.'
            )


def get_model_health():
    """Check model artifact availability and integrity for app-level health checks."""
    if not os.path.exists(MODEL_PATH):
        return False, 'Model artifact not found.'
    try:
        bundle = load_model()
        validate_model_bundle(bundle)
        return True, 'Model artifact is valid.'
    except Exception as exc:
        return False, f'Model artifact validation failed: {exc}'


def load_model():
    """Load the model from disk (only once, then cache it in memory)."""
    global _model_bundle
    if _model_bundle is None:
        with open(MODEL_PATH, 'rb') as f:
            _model_bundle = pickle.load(f)
        validate_model_bundle(_model_bundle)
    return _model_bundle


def _normalize_text(value):
    return str(value).strip().lower().replace(' ', '_')


def _encode_categorical(feature_encoders, column_name, raw_value):
    """Encode a categorical value with tolerant matching against encoder classes."""
    encoder = feature_encoders[column_name]
    direct = str(raw_value)

    if direct in encoder.classes_:
        return encoder.transform([direct])[0]

    norm_target = _normalize_text(raw_value)
    for cls in encoder.classes_:
        if _normalize_text(cls) == norm_target:
            return encoder.transform([cls])[0]

    allowed = ', '.join(map(str, encoder.classes_))
    raise ValueError(f"Invalid value for {column_name}: '{raw_value}'. Allowed values: {allowed}")


def _run_prediction(bundle, all_features, bmi):
    """Run model prediction from a fully prepared feature dictionary."""
    model = bundle['model']
    scaler = bundle['scaler']
    target_encoder = bundle['label_encoder']
    feature_cols = bundle['feature_cols']

    feature_row = [all_features.get(col, 0.0) for col in feature_cols]
    X = np.array(feature_row).reshape(1, -1)
    X_scaled = scaler.transform(X)

    predicted_class_number = model.predict(X_scaled)[0]
    class_probabilities = model.predict_proba(X_scaled)[0]

    class_label = target_encoder.inverse_transform([predicted_class_number])[0]
    confidence = float(np.max(class_probabilities)) * 100

    all_class_names = target_encoder.inverse_transform(range(len(class_probabilities)))
    all_probs = {
        cls: round(float(prob) * 100, 1)
        for cls, prob in zip(all_class_names, class_probabilities)
    }

    return {
        'class_label': class_label,
        'confidence': round(confidence, 1),
        'bmi': round(float(bmi), 1),
        'all_probs': all_probs,
        'status': 'success'
    }


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

    normalized = validate_inputs(
        age=age,
        gender=gender,
        height_cm=height_cm,
        weight_kg=weight_kg,
        physical_activity=physical_activity,
        family_history=family_history,
    )

    age = normalized['age']
    gender = normalized['gender']
    height_cm = normalized['height_cm']
    weight_kg = normalized['weight_kg']
    physical_activity = normalized['physical_activity']
    family_history = normalized['family_history']

    bundle = load_model()

    feature_encoders = bundle['feature_encoders']

    # ── Step 1: Compute BMI from height and weight ─────────────────────────────
    height_m = height_cm / 100.0
    bmi      = weight_kg / (height_m ** 2)

    # ── Step 2: Encode the user's categorical inputs ───────────────────────────
    # Use the same encoders that were fitted during training
    gender_encoded = feature_encoders['Gender'].transform([gender])[0]
    family_encoded = feature_encoders['family_history_with_overweight'].transform([family_history])[0]

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
    defaults = bundle.get('inference_defaults') or LEGACY_DEFAULTS

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

    return _run_prediction(bundle, all_features, bmi)


def predict_advanced(form_data):
    """
    Predict using full user-provided feature set (all model input features).
    Expects form_data keys matching ADVANCED_REQUIRED_FIELDS.
    """
    missing_fields = [k for k in ADVANCED_REQUIRED_FIELDS if k not in form_data]
    if missing_fields:
        raise ValueError(f"Missing required fields: {', '.join(sorted(missing_fields))}")

    # Reuse core validation for shared 6 inputs.
    shared = validate_inputs(
        age=form_data['age'],
        gender=form_data['gender'],
        height_cm=form_data['height'],
        weight_kg=form_data['weight'],
        physical_activity=form_data['physical_activity'],
        family_history=form_data['family_history'],
    )

    bundle = load_model()
    feature_encoders = bundle['feature_encoders']

    height_m = shared['height_cm'] / 100.0
    bmi = shared['weight_kg'] / (height_m ** 2)

    if not (1.0 <= float(form_data['fcvc']) <= 3.0):
        raise ValueError('FCVC must be between 1.0 and 3.0.')
    if not (1.0 <= float(form_data['ncp']) <= 6.0):
        raise ValueError('NCP must be between 1.0 and 6.0.')
    if not (0.0 <= float(form_data['ch2o']) <= 3.0):
        raise ValueError('CH2O must be between 0.0 and 3.0.')
    if not (0.0 <= float(form_data['tue']) <= 3.0):
        raise ValueError('TUE must be between 0.0 and 3.0.')

    activity_to_number = {
        'Sedentary': 0.0,
        'Light': 0.75,
        'Moderate': 1.5,
        'Active': 2.25,
        'Very Active': 3.0,
    }

    all_features = {
        'Gender': _encode_categorical(feature_encoders, 'Gender', shared['gender']),
        'Age': float(shared['age']),
        'Height': float(height_m),
        'Weight': float(shared['weight_kg']),
        'family_history_with_overweight': _encode_categorical(
            feature_encoders,
            'family_history_with_overweight',
            shared['family_history']
        ),
        'FAVC': _encode_categorical(feature_encoders, 'FAVC', form_data['favc']),
        'FCVC': float(form_data['fcvc']),
        'NCP': float(form_data['ncp']),
        'CAEC': _encode_categorical(feature_encoders, 'CAEC', form_data['caec']),
        'SMOKE': _encode_categorical(feature_encoders, 'SMOKE', form_data['smoke']),
        'CH2O': float(form_data['ch2o']),
        'SCC': _encode_categorical(feature_encoders, 'SCC', form_data['scc']),
        'FAF': float(activity_to_number.get(shared['physical_activity'], 1.5)),
        'TUE': float(form_data['tue']),
        'CALC': _encode_categorical(feature_encoders, 'CALC', form_data['calc']),
        'MTRANS': _encode_categorical(feature_encoders, 'MTRANS', form_data['mtrans']),
        'BMI': float(bmi),
    }

    return _run_prediction(bundle, all_features, bmi)
