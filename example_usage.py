"""
example_usage.py — Demonstrates how to use the trained model directly.
Make sure you've run `python main.py` first to train and save the model.
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from src.predict import predict
from src.nutrition import get_nutrition_plan

def main():
    print("=" * 55)
    print("  Example: Direct model usage")
    print("=" * 55)

    # Example input
    result = predict(
        age=35,
        gender='Male',
        height_cm=175,
        weight_kg=95,
        physical_activity='Sedentary',
        family_history='Yes'
    )

    print(f"\nInput:")
    print(f"  Age: 35, Gender: Male, Height: 175cm, Weight: 95kg")
    print(f"  Activity: Sedentary, Family History: Yes")
    print(f"\nResult:")
    print(f"  Predicted Class : {result['class_label']}")
    print(f"  Confidence      : {result['confidence']}%")
    print(f"  BMI             : {result['bmi']}")

    plan = get_nutrition_plan(result['class_label'])
    print(f"\nNutrition Plan for {result['class_label']}:")
    print(f"  Daily Calories : {plan['daily_calories']} kcal")
    print(f"  Breakfast      : {plan['breakfast'][0]}")

if __name__ == '__main__':
    main()
