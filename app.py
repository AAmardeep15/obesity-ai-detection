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
app.secret_key = 'obesity-detection-secret-2024'

MODEL_EXISTS = os.path.exists(os.path.join('models', 'obesity_model.pkl'))


@app.route('/')
def index():
    obesity_classes = [
        {'key': k, 'label': v['label'], 'emoji': v['emoji'], 'color': v['color'],
         'calories': v['daily_calories']}
        for k, v in NUTRITION_PLANS.items()
    ]
    return render_template('index.html', obesity_classes=obesity_classes, model_exists=MODEL_EXISTS)


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

                age = int(request.form.get('age', 25))
                gender = request.form.get('gender', 'Male')
                height_cm = float(request.form.get('height', 170))
                weight_kg = float(request.form.get('weight', 70))
                physical_activity = request.form.get('physical_activity', 'Moderate')
                family_history = request.form.get('family_history', 'No')

                result = run_predict(
                    age=age,
                    gender=gender,
                    height_cm=height_cm,
                    weight_kg=weight_kg,
                    physical_activity=physical_activity,
                    family_history=family_history
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
        from src.predict import predict as run_predict

        # Read the same form values as the predict route
        age               = int(request.form.get('age', 25))
        gender            = request.form.get('gender', 'Male')
        height_cm         = float(request.form.get('height', 170))
        weight_kg         = float(request.form.get('weight', 70))
        physical_activity = request.form.get('physical_activity', 'Moderate')
        family_history    = request.form.get('family_history', 'No')

        # Run prediction
        result    = run_predict(age, gender, height_cm, weight_kg, physical_activity, family_history)
        nutrition = get_nutrition_plan(result['class_label'])
        exercise  = get_exercise_plan(result['class_label'])

        # ── Build CSV in memory ─────────────────────────────────────────────────
        output = io.StringIO()
        writer = csv.writer(output)

        writer.writerow(['AI-Based Obesity Detection — Personalised Report'])
        writer.writerow(['Generated on', datetime.now().strftime('%Y-%m-%d %H:%M')])
        writer.writerow([])

        # Section 1 — User Details
        writer.writerow(['=== USER DETAILS ==='])
        writer.writerow(['Age',              age])
        writer.writerow(['Gender',           gender])
        writer.writerow(['Height (cm)',       height_cm])
        writer.writerow(['Weight (kg)',       weight_kg])
        writer.writerow(['BMI',              result['bmi']])
        writer.writerow(['Physical Activity', physical_activity])
        writer.writerow(['Family History',    family_history])
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


@app.route('/statistics')
def statistics():
    stats_path = os.path.join('outputs', 'model_stats.json')
    stats = None
    if os.path.exists(stats_path):
        with open(stats_path, 'r') as f:
            stats = json.load(f)
    return render_template('statistics.html', stats=stats, model_exists=MODEL_EXISTS)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
