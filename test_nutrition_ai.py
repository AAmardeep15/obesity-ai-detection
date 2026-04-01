from src.nutrition import get_nutrition_plan

# Test Case 1: Obesity Type III, Male, 30 years, 180cm, 120kg
profile = {
    'age': 30,
    'gender': 'Male',
    'height': 180,
    'weight': 120,
    'activity': 1.5 # Moderate
}

plan = get_nutrition_plan('Obesity_Type_III', user_profile=profile)

print("--- AI Powered Nutrition Plan ---")
print(f"Class: {plan['label']}")
print(f"Daily Calories (AI Predicted): {plan['daily_calories']}")
print(f"Macros: P:{plan['protein_g']}g, C:{plan['carbs_g']}g, F:{plan['fat_g']}g")
print(f"AI Powered: {plan.get('is_ai_powered', False)}")
print("\nSample Breakfast:")
for item in plan['breakfast']:
    print(f"- {item}")
