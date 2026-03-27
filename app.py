"""
app.py — Main Flask application with server-side rendering only.
No external API calls. All ML inference happens here in Python.
"""

import os
import sys
import json
import io
import csv
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, render_template, request, jsonify, Response
from src.nutrition import get_nutrition_plan, NUTRITION_PLANS
from src.exercise import get_exercise_plan

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-only-change-me')

MODEL_DIR = os.path.join(os.path.dirname(__file__), 'models')
MODEL_EXISTS = os.path.exists(os.path.join(MODEL_DIR, 'obesity_model.pkl'))

VALID_GENDERS = {'Male', 'Female'}
VALID_PHYSICAL_ACTIVITY = {
    'Sedentary', 'Light', 'Moderate', 'Active', 'Very Active'
}
VALID_FAMILY_HISTORY = {'Yes', 'No'}

ADVANCED_REPORT_FIELDS = [
    ('Age', 'age'),
    ('Gender', 'gender'),
    ('Height (cm)', 'height'),
    ('Weight (kg)', 'weight'),
    ('Family History of Obesity', 'family_history'),
    ('Physical Activity (FAF)', 'physical_activity'),
    ('Frequent High-Calorie Food (FAVC)', 'favc'),
    ('Vegetable Frequency (FCVC)', 'fcvc'),
    ('Main Meals Per Day (NCP)', 'ncp'),
    ('Eating Between Meals (CAEC)', 'caec'),
    ('Smoking (SMOKE)', 'smoke'),
    ('Water Intake (CH2O)', 'ch2o'),
    ('Calorie Monitoring (SCC)', 'scc'),
    ('Technology Use (TUE)', 'tue'),
    ('Alcohol Intake (CALC)', 'calc'),
    ('Primary Transport (MTRANS)', 'mtrans'),
]


def parse_prediction_form(form):
    """Parse and validate prediction form fields from request.form."""
    age = int(form.get('age', 25))
    gender = form.get('gender', 'Male')
    height_cm = float(form.get('height', 170))
    weight_kg = float(form.get('weight', 70))
    physical_activity = form.get('physical_activity', 'Moderate')
    family_history = form.get('family_history', 'No')

    if not (10 <= age <= 80):
        raise ValueError('Age must be between 10 and 80 years.')
    if gender not in VALID_GENDERS:
        raise ValueError("Gender must be 'Male' or 'Female'.")
    if not (100.0 <= height_cm <= 220.0):
        raise ValueError('Height must be between 100 and 220 cm.')
    if not (20.0 <= weight_kg <= 250.0):
        raise ValueError('Weight must be between 20 and 250 kg.')
    if physical_activity not in VALID_PHYSICAL_ACTIVITY:
        raise ValueError('Physical activity level is invalid.')
    if family_history not in VALID_FAMILY_HISTORY:
        raise ValueError("Family history must be 'Yes' or 'No'.")

    return {
        'age': age,
        'gender': gender,
        'height_cm': height_cm,
        'weight_kg': weight_kg,
        'physical_activity': physical_activity,
        'family_history': family_history,
    }

def update_model_status():
    global MODEL_EXISTS
    try:
        from src.predict import get_model_health
        MODEL_EXISTS = get_model_health()[0]
    except Exception:
        MODEL_EXISTS = os.path.exists(os.path.join(MODEL_DIR, 'obesity_model.pkl'))


@app.route('/')
def index():
    update_model_status()
    obesity_classes = [
        {'key': k, 'label': v['label'], 'emoji': v['emoji'], 'color': v['color'],
         'calories': v['daily_calories']}
        for k, v in NUTRITION_PLANS.items()
    ]
    
    stats_path = os.path.join('outputs', 'model_stats.json')
    stats = None
    if os.path.exists(stats_path):
        with open(stats_path, 'r') as f:
            stats = json.load(f)
            
    return render_template('index.html', 
                           obesity_classes=obesity_classes, 
                           model_exists=MODEL_EXISTS,
                           stats=stats)


@app.route('/predict', methods=['GET', 'POST'])
def predict_view():
    result = None
    nutrition = None
    exercise = None
    error = None

    if request.method == 'POST':
        if not MODEL_EXISTS:
            error = "Model not found. Please run `python main.py` first to train the model."
        else:
            try:
                from src.predict import predict as run_predict

                parsed = parse_prediction_form(request.form)

                result = run_predict(
                    age=parsed['age'],
                    gender=parsed['gender'],
                    height_cm=parsed['height_cm'],
                    weight_kg=parsed['weight_kg'],
                    physical_activity=parsed['physical_activity'],
                    family_history=parsed['family_history']
                )

                plan_meta = NUTRITION_PLANS.get(result['class_label'], {})
                result['color'] = plan_meta.get('color', '#f97316')
                result['label'] = plan_meta.get('label', result['class_label'].replace('_', ' '))
                result['emoji'] = plan_meta.get('emoji', '🎯')

                nutrition = get_nutrition_plan(result['class_label'])
                exercise = get_exercise_plan(result['class_label'])

            except ValueError as e:
                error = f"Invalid input values: {e}"
            except Exception as e:
                error = f"Prediction error: {e}"

    return render_template(
        'predict.html',
        result=result,
        nutrition=nutrition,
        exercise=exercise,
        error=error,
        model_exists=MODEL_EXISTS
    )


@app.route('/advance', methods=['GET', 'POST'])
def advance_view():
    result = None
    nutrition = None
    exercise = None
    error = None

    if request.method == 'POST':
        if not MODEL_EXISTS:
            error = "Model not found. Please run `python main.py` first to train the model."
        else:
            try:
                from src.predict import predict_advanced as run_predict_advanced

                form_data = request.form.to_dict(flat=True)
                result = run_predict_advanced(form_data)

                plan_meta = NUTRITION_PLANS.get(result['class_label'], {})
                result['color'] = plan_meta.get('color', '#f97316')
                result['label'] = plan_meta.get('label', result['class_label'].replace('_', ' '))
                result['emoji'] = plan_meta.get('emoji', '🎯')

                nutrition = get_nutrition_plan(result['class_label'])
                exercise = get_exercise_plan(result['class_label'])

            except ValueError as e:
                error = f"Invalid input values: {e}"
            except Exception as e:
                error = f"Prediction error: {e}"

    return render_template(
        'advance.html',
        result=result,
        nutrition=nutrition,
        exercise=exercise,
        error=error,
        model_exists=MODEL_EXISTS
    )


@app.route('/api/exercise')
def api_exercise():
    """Return exercise recommendations for a given obesity class."""
    obesity_class = request.args.get('class', 'Normal_Weight')
    plan = get_exercise_plan(obesity_class)
    return jsonify(plan)


@app.route('/download-report', methods=['POST'])
def download_report():
    """
    Generate and return a CSV report containing:
      - User details (age, gender, height, weight, BMI, prediction result)
      - Full personalised nutrition plan (breakfast, lunch, dinner, snacks)
      - Exercise plan summary
    """
    try:
        mode = request.form.get('mode', 'basic')
        parsed = parse_prediction_form(request.form)

        if mode == 'advanced':
            from src.predict import predict_advanced as run_predict_advanced
            result = run_predict_advanced(request.form.to_dict(flat=True))
        else:
            from src.predict import predict as run_predict
            result = run_predict(
                parsed['age'],
                parsed['gender'],
                parsed['height_cm'],
                parsed['weight_kg'],
                parsed['physical_activity'],
                parsed['family_history']
            )

        nutrition = get_nutrition_plan(result['class_label'])
        exercise  = get_exercise_plan(result['class_label'])

        # ── Build CSV in memory ─────────────────────────────────────────────────
        output = io.StringIO()
        writer = csv.writer(output)

        writer.writerow(['AI-Based Obesity Detection — Personalised Report'])
        writer.writerow(['Generated on', datetime.now().strftime('%Y-%m-%d %H:%M')])
        writer.writerow([])

        # Section 1 — Input Features (mode-specific)
        writer.writerow(['=== INPUT FEATURES ==='])
        if mode == 'advanced':
            advanced_form = request.form.to_dict(flat=True)
            for label, key in ADVANCED_REPORT_FIELDS:
                writer.writerow([label, advanced_form.get(key, '')])
            writer.writerow(['BMI', result['bmi']])
        else:
            writer.writerow(['Age', parsed['age']])
            writer.writerow(['Gender', parsed['gender']])
            writer.writerow(['Height (cm)', parsed['height_cm']])
            writer.writerow(['Weight (kg)', parsed['weight_kg']])
            writer.writerow(['Physical Activity', parsed['physical_activity']])
            writer.writerow(['Family History of Obesity', parsed['family_history']])
        writer.writerow([])

        # Section 2 — Prediction Result
        writer.writerow(['=== PREDICTION RESULT ==='])
        writer.writerow(['Obesity Class',    result['class_label'].replace('_', ' ')])
        writer.writerow(['Confidence',       f"{result['confidence']}%"])
        writer.writerow([])

        # Section 3 — Nutrition Plan
        writer.writerow(['=== NUTRITION PLAN ==='])
        writer.writerow(['Daily Calorie Target (kcal)', nutrition['daily_calories']])
        writer.writerow([])
        writer.writerow(['Breakfast'])
        for item in nutrition['breakfast']:
            writer.writerow(['', item])
        writer.writerow(['Lunch'])
        for item in nutrition['lunch']:
            writer.writerow(['', item])
        writer.writerow(['Dinner'])
        for item in nutrition['dinner']:
            writer.writerow(['', item])
        writer.writerow(['Snacks'])
        for item in nutrition['snacks']:
            writer.writerow(['', item])
        writer.writerow(['Foods to Avoid'])
        for item in nutrition['avoid']:
            writer.writerow(['', item])
        writer.writerow(['Health Tips'])
        for tip in nutrition['tips']:
            writer.writerow(['', tip])
        writer.writerow([])

        # Section 4 — Exercise Plan
        writer.writerow(['=== EXERCISE PLAN ==='])
        writer.writerow(['Goal',            exercise['goal']])
        writer.writerow(['Weekly Target',   exercise['weekly_target']])
        writer.writerow([])
        writer.writerow(['Exercise', 'Type', 'Duration', 'Intensity', 'Description'])
        for ex in exercise['exercises']:
            writer.writerow([ex['name'], ex['type'], ex['duration'], ex['intensity'], ex['desc']])
        writer.writerow([])
        writer.writerow(['Exercises to Avoid'])
        for item in exercise['avoid']:
            writer.writerow(['', item])
        writer.writerow(['Expert Tips'])
        for tip in exercise['tips']:
            writer.writerow(['', tip])
        writer.writerow([])
        writer.writerow(['Disclaimer', 'AI-generated guidance only. Consult a qualified healthcare professional.'])

        # Return as downloadable CSV
        csv_data = output.getvalue()
        filename = f"obesity_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        return Response(
            csv_data,
            mimetype='text/csv',
            headers={'Content-Disposition': f'attachment; filename={filename}'}
        )

    except Exception as e:
        return f"Error generating report: {e}", 500


@app.route('/educate')
def educate():
    """Education page — facts about obesity, causes, consequences, prevention."""
    return render_template('educate.html')


@app.route('/learn')
def learn():
    """Formal obesity learning page with prevention and management guidance."""
    return render_template('learn.html')


@app.route('/statistics')
def statistics():
    update_model_status()
    stats_path = os.path.join('outputs', 'model_stats.json')
    stats = None
    if os.path.exists(stats_path):
        with open(stats_path, 'r') as f:
            stats = json.load(f)
    return render_template('statistics.html', stats=stats, model_exists=MODEL_EXISTS)


@app.route('/train', methods=['POST'])
def train_model():
    """
    Trigger the model training process and return the new stats.
    Called via AJAX from the Dashboard.
    """
    try:
        from src.train import train
        bundle, stats = train()
        update_model_status()
        return jsonify({
            'success': True,
            'message': 'Model trained successfully!',
            'stats': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f"Training failed: {str(e)}"
        }), 500


if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', '0').strip().lower() in {'1', 'true', 'yes'}
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', '5000'))
    app.run(debug=debug_mode, host=host, port=port)
