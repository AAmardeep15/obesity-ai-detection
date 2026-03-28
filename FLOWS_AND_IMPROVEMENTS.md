# Project Flows and Improvement Plan

Date: 2026-03-27
Project: AI-Based Obesity Detection and Personalized Nutrition Recommendation System

## 1) End-to-End Flows in This Project

### Flow A: Initial Setup and First-Time Run

1. Install dependencies from requirements.txt.
2. Run main.py to train models and generate artifacts.
3. Run app.py to start Flask server and UI.
4. Open browser at / and navigate to Predict or Statistics pages.

Current behavior:

- The app expects models/obesity_model.pkl to exist.
- If missing, prediction is blocked and user sees a training warning.

---

### Flow B: Data Preprocessing Pipeline

Source: src/data_preprocessing.py

1. Load obesity_dataset.csv.
2. Check missing values and impute:
   - Numeric: mean.
   - Categorical: mode.
3. Cap outliers using IQR bounds (clip, not remove).
4. Engineer BMI feature from weight and height.
5. Label-encode categorical columns and target class.
6. Split train/test (80/20, stratified).
7. Fit StandardScaler on train only, transform train and test.
8. Save preprocessing summary to outputs/preprocessing_report.json.

Current behavior:

- Strong anti-leakage handling by fitting scaler only on training data.
- Uses fixed random_state for reproducibility.

---

### Flow C: Model Training, Evaluation, and Artifact Saving

Source: src/train.py

1. Pull preprocessed arrays from preprocessing pipeline.
2. Train 3 base models:
   - Random Forest
   - Logistic Regression
   - Gradient Boosting
3. Train soft-voting ensemble over the 3 models.
4. Evaluate each model using accuracy, weighted F1, precision, recall.
5. Build confusion matrix and feature importance (from RF).
6. Save artifacts:
   - Individual model pickle files
   - preprocessor.pkl
   - obesity_model.pkl bundle
   - outputs/model_stats.json

Current behavior:

- training stats are persisted and re-used by UI dashboard.
- Full bundle supports one-step loading in prediction flow.

---

### Flow D: Model Availability and Status Flow

Source: app.py

1. On relevant routes, app checks whether models/obesity_model.pkl exists.
2. If found, prediction and dashboard features are enabled.
3. If not found, app shows warning and blocks inferencing.

Current behavior:

- Model status is a file-presence check only.

---

### Flow E: Home Page Rendering Flow

Source: app.py -> index route, templates/index.html

1. Load model status.
2. Load outputs/model_stats.json if present.
3. Load obesity class metadata from nutrition plans.
4. Render home page cards, stats counters, and CTAs.

Current behavior:

- Home page is server-rendered.
- Accuracy and counts are pulled from saved stats when available.

---

### Flow F: Prediction Input to Result Flow

Source: app.py -> /predict, src/predict.py, templates/predict.html

1. User opens /predict (GET).
2. User submits 6 fields (POST): age, gender, height, weight, physical activity, family history.
3. Backend loads obesity_model.pkl and extracts:
   - model
   - scaler
   - feature encoders
   - label encoder
   - feature order
4. Backend computes BMI from height and weight.
5. Backend maps activity level to FAF numeric value.
6. Backend fills remaining model features with default values.
7. Backend reorders features to training column order.
8. Backend scales input with saved scaler.
9. Backend predicts class and per-class probabilities.
10. Backend maps class to label/color/emoji and returns result to template.

Current behavior:

- Prediction pipeline is fully local and synchronous.
- User sees confidence, BMI, and probability bars.

---

### Flow G: Nutrition Personalization Flow

Source: src/nutrition.py, templates/predict.html

1. Predicted class key is used to fetch nutrition plan dictionary.
2. Plan contains calories, meals, avoid list, and tips.
3. Plan is displayed inside modal on prediction page.

Current behavior:

- Rule-based mapping by obesity class.
- Deterministic and fast lookup.

---

### Flow H: Exercise Personalization Flow

Source: src/exercise.py, templates/predict.html

1. Predicted class key is used to fetch exercise plan dictionary.
2. Plan contains goal, weekly target, exercise cards, avoid list, and tips.
3. Plan is rendered under prediction result.

Current behavior:

- Rule-based class-specific recommendations.
- Safe fallback to Normal_Weight profile when class is not found.

---

### Flow I: Report Export Flow

Source: app.py -> /download-report

1. Hidden form re-submits original user inputs.
2. Backend reruns prediction and resolves nutrition + exercise plans.
3. Backend builds CSV in memory (StringIO).
4. CSV includes user details, prediction, nutrition, exercise, and disclaimer.
5. CSV is returned as downloadable file response.

Current behavior:

- Single-click report generation from prediction page.
- Export format is CSV only.

---

### Flow J: Statistics Dashboard and Live Retraining Flow

Source: templates/statistics.html, app.py -> /statistics and /train

1. /statistics loads saved model stats JSON and renders dashboard.
2. Dashboard JS builds radar, feature importance, confusion matrix, and distribution charts.
3. User clicks Train Model button.
4. Browser sends POST to /train.
5. Backend runs src.train.train() and returns fresh stats JSON.
6. Frontend updates cards/charts and status indicators.

Current behavior:

- Retraining is triggered from UI.
- Stats update is dynamic without full hard reload.

---

### Flow K: Education Content Flow

Source: app.py -> /educate, templates/educate.html

1. User opens education route.
2. App renders static educational content (definition, BMI classes, causes, effects, prevention).

Current behavior:

- Informational page only.
- No model operations required.

---

### Flow L: Client-Side UX Utility Flows

Source: static/js/main.js

1. Theme toggle with localStorage persistence.
2. Mobile hamburger menu open/close behavior.
3. Active nav highlighting by route path.
4. Live BMI calculator while user enters height and weight.
5. Nutrition modal open/close and escape handling.
6. Confidence bar animation and counter animations.
7. IntersectionObserver reveal animations.
8. Scroll-to-top button visibility and action.

Current behavior:

- UX interactions are lightweight and framework-free.

---

## 2) How to Improve the Project (Actionable)

### Priority 1 (High impact, should do first)

1. Add robust input validation layer.

- Why: Prevent bad data and runtime errors in predict and report routes.
- How:
  - Validate ranges for age, height, weight, and accepted enums for categorical fields.
  - Return structured error messages for UI.

2. Remove hardcoded default feature assumptions from inference.

- Why: Defaults may bias predictions and reduce trust.
- How:
  - Compute defaults from training data and save them in preprocessor metadata.
  - Version defaults with model artifacts.

3. Add model/artifact integrity checks.

- Why: File existence does not guarantee compatibility or correctness.
- How:
  - Store model_version, schema_version, and checksum in obesity_model.pkl metadata.
  - Validate at app startup and before prediction.

4. Add test suite (unit + integration).

- Why: Current flows are not protected against regressions.
- How:
  - Unit tests for preprocess, predict mappings, and plan fallback behavior.
  - Integration tests for routes: /predict, /train, /download-report.

### Priority 2 (Performance and maintainability)

5. Move long training job off request thread.

- Why: /train currently blocks the web request until full training completes.
- How:
  - Use background task queue (Celery/RQ) or subprocess job manager.
  - Add job polling endpoint and progress states.

6. Add logging and observability.

- Why: Debugging and evaluation are hard without structured logs.
- How:
  - Add Python logging with INFO/WARN/ERROR.
  - Log prediction input schema (without sensitive raw data), timing, and errors.

7. Add configuration management.

- Why: Magic constants and paths are hardcoded.
- How:
  - Use environment variables for model path, host, port, debug, and training params.
  - Centralize config in one module.

8. Improve model evaluation depth.

- Why: Single train/test split can be unstable.
- How:
  - Add cross-validation metrics.
  - Add per-class precision/recall/F1 and calibration analysis.

### Priority 3 (Product quality and user trust)

9. Add explainability in prediction UI.

- Why: Users need to understand why a class was predicted.
- How:
  - Add top contributing features summary.
  - Include caution text when confidence is low.

10. Improve report export formats.

- Why: CSV is useful but limited for presentation.
- How:
  - Add PDF export with sections and charts.
  - Include timestamp, model version, and confidence interpretation.

11. Add API endpoints for external integration.

- Why: SSR-only limits reuse.
- How:
  - Add /api/predict with JSON input/output.
  - Keep existing SSR pages for browser users.

12. Security hardening.

- Why: app.secret_key and debug mode are not production-safe.
- How:
  - Move secrets to environment variables.
  - Disable debug in production.
  - Add CSRF protection for forms.

---

## 3) DeepSeek Evaluation Readiness Checklist

Use this checklist for external evaluation:

1. Functional flow completeness

- Setup, training, prediction, stats, and report export all run end-to-end.

2. Reproducibility

- Same code + same random seeds produce comparable metrics.

3. Artifact consistency

- model bundle, encoders, scaler, feature order, and defaults are version-aligned.

4. Input safety

- Invalid or out-of-range fields are gracefully rejected with clear errors.

5. Regression safety

- Automated tests cover critical flows and route responses.

6. Runtime behavior

- Training and inference latency are measured and acceptable.

7. UX reliability

- Predict page, modal, charts, and report download function on desktop and mobile.

8. Explainability and trust

- Predictions include confidence and clear medical disclaimer.

9. Maintainability

- Config, logging, and modular boundaries are clear.

10. Production readiness

- Secret management, debug off, and safe error handling are in place.

---

## 4) Suggested Next Implementation Order

1. Validation and artifact metadata checks.
2. Automated tests for preprocessing, prediction, and routes.
3. Background training execution and progress API.
4. Explainability and export enhancement.
5. Security and deployment hardening.

---

## 5) Execution Plan and Current Progress

### Phase 1: Input and Artifact Safety (Started)

Scope:

- Add centralized server-side form validation.
- Validate model bundle structure and schema version.
- Persist inference defaults in training artifacts.

Status:

- Done: Central form parsing + validation for prediction and report routes.
- Done: Model bundle integrity checks added and used in model status check.
- Done: Inference defaults now computed in preprocessing and saved in artifacts.
- Done: Prediction now prefers artifact defaults with backward-compatible fallback.

### Phase 2: Test Coverage (Next)

Scope:

- Unit tests for form validation and predict input validation.
- Unit tests for model-bundle validation behavior.
- Route tests for /predict and /download-report valid/invalid payloads.

Exit criteria:

- Tests pass locally with no failing critical path tests.

Status:

- Done: Added unit tests for form parsing and input/model-bundle validators.
- Done: Added integration tests for /predict and /download-report paths.
- Done: Local test run passed (9/9).

### Phase 3: Async Training and Better Runtime UX

Scope:

- Move /train to background job execution.
- Add job status endpoint and frontend polling state.

Exit criteria:

- UI remains responsive while training runs.

### Phase 4: Security and Production Hardening

Scope:

- Externalize secret key and app runtime config.
- Disable debug mode by default in production env.
- Add CSRF protection for mutating form endpoints.

Exit criteria:

- App can run with secure defaults in deployment mode.

Status:

- Done: Flask secret key moved to FLASK_SECRET_KEY env var (safe default placeholder retained for local dev).
- Done: Debug mode, host, and port now configured via FLASK_DEBUG, FLASK_HOST, FLASK_PORT.
