# Models — Saved Artefacts

This folder contains all trained model files for the
AI-Based Obesity Detection & Personalized Nutrition System.

## Files

| File | Description |
|------|-------------|
| `random_forest.pkl` | RandomForestClassifier (200 trees, random_state=42) |
| `logistic_regression.pkl` | LogisticRegression (max_iter=1000, multi-class) |
| `gradient_boosting.pkl` | GradientBoostingClassifier (200 estimators) |
| `ensemble_model.pkl` | Soft-Voting ensemble of all 3 models above |
| `preprocessor.pkl` | StandardScaler + LabelEncoders + feature column order |
| `obesity_model.pkl` | Full inference bundle (model + preprocessor combined) |

## How to Load Individually

```python
import pickle

# Load a single model
with open('models/random_forest.pkl', 'rb') as f:
    rf_model = pickle.load(f)

# Load the preprocessor
with open('models/preprocessor.pkl', 'rb') as f:
    preprocessor = pickle.load(f)
    scaler           = preprocessor['scaler']
    feature_encoders = preprocessor['feature_encoders']
    label_encoder    = preprocessor['label_encoder']
    feature_cols     = preprocessor['feature_cols']
```

## Retrain

```bash
python main.py
```

This re-runs the full pipeline:
`data_preprocessing.py` → `train.py` → saves all files above.

## Notes
- The `preprocessor.pkl` **must** be used alongside any individual model
  to correctly transform new inputs before prediction.
- The Flask app (`app.py`) loads `obesity_model.pkl` which bundles
  the ensemble + preprocessor in one file for convenience.
