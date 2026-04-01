"""
Nutrition plan logic per obesity class.
"""

import os
import pickle
import numpy as np

# Path to the saved nutrition model bundle
NUTRITION_MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'nutrition_model.pkl')

_nutrition_bundle = None

def load_nutrition_model():
    """Load the local nutrition AI bundle if it exists."""
    global _nutrition_bundle
    if _nutrition_bundle is None:
        if os.path.exists(NUTRITION_MODEL_PATH):
            with open(NUTRITION_MODEL_PATH, 'rb') as f:
                _nutrition_bundle = pickle.load(f)
    return _nutrition_bundle

NUTRITION_PLANS = {
    'Insufficient_Weight': {
        'emoji': '🥛',
        'color': '#3b82f6',
        'label': 'Insufficient Weight',
        'daily_calories': 2500,
        'breakfast': [
            'Banana smoothie with peanut butter',
            'Whole grain toast with scrambled eggs',
            'Full-fat milk (250ml)'
        ],
        'lunch': [
            'Rice with chicken curry',
            'Avocado salad with olive oil dressing',
            'Fresh fruit juice'
        ],
        'dinner': [
            'Pasta with cream sauce and grilled chicken',
            'Grilled fish with roasted potatoes',
            'Steamed veggies with butter'
        ],
        'snacks': [
            'Handful of mixed nuts and dried fruits',
            'Greek yogurt with honey and granola'
        ],
        'avoid': [
            'Skipping meals',
            'Excessive caffeine',
            'Diet/low-fat foods',
            'Processed low-calorie snacks'
        ],
        'tips': [
            'Eat every 3 hours to maintain calorie intake',
            'Add healthy fats like olive oil, avocado, nuts',
            'Do strength training to build muscle mass'
        ]
    },
    'Normal_Weight': {
        'emoji': '✅',
        'color': '#22c55e',
        'label': 'Normal Weight',
        'daily_calories': 2000,
        'breakfast': [
            'Oatmeal with fruits and seeds',
            'Two boiled or poached eggs',
            'Green tea or coffee (unsweetened)'
        ],
        'lunch': [
            'Grilled chicken or fish with brown rice',
            'Mixed vegetable salad with olive oil',
            'A glass of water or buttermilk'
        ],
        'dinner': [
            'Whole wheat roti with dal and sabzi',
            'Grilled protein with steamed vegetables',
            'Light soup as starter'
        ],
        'snacks': [
            'A handful of almonds or walnuts',
            'Seasonal fruit (apple, banana, or orange)'
        ],
        'avoid': [
            'Excessive sugar and sweets',
            'Late-night heavy meals',
            'Processed and packaged foods'
        ],
        'tips': [
            'Maintain 30 minutes of moderate exercise daily',
            'Stay hydrated with 2.5–3L of water daily',
            'Sleep 7–8 hours for metabolic balance'
        ]
    },
    'Overweight_Level_I': {
        'emoji': '⚠️',
        'color': '#eab308',
        'label': 'Overweight Level I',
        'daily_calories': 1800,
        'breakfast': [
            'Oats with skimmed milk and berries',
            'Two egg whites or one boiled egg',
            'Black coffee or green tea'
        ],
        'lunch': [
            'Small portion of brown rice with dal',
            'Grilled chicken breast (skinless)',
            'Large salad with low-fat dressing'
        ],
        'dinner': [
            'Vegetable soup (broth-based)',
            'Two whole wheat rotis with sabzi',
            'Grilled fish or tofu'
        ],
        'snacks': [
            'Apple or pear',
            'Low-fat yogurt (unsweetened)'
        ],
        'avoid': [
            'Fried foods and fast food',
            'Sugary drinks and sodas',
            'White bread and refined carbs'
        ],
        'tips': [
            'Add 45 minutes of brisk walking daily',
            'Track your calories with a food diary',
            'Eat dinner before 8 PM'
        ]
    },
    'Overweight_Level_II': {
        'emoji': '🔶',
        'color': '#f97316',
        'label': 'Overweight Level II',
        'daily_calories': 1700,
        'breakfast': [
            'Vegetable poha or upma (low oil)',
            'One boiled egg',
            'Herbal or green tea'
        ],
        'lunch': [
            'Multigrain roti (2) with dal and salad',
            'Grilled or baked chicken/fish',
            'Cucumber, tomato, onion salad'
        ],
        'dinner': [
            'Lentil or vegetable soup',
            'One roti with stir-fried vegetables',
            'Skimmed milk before bed (optional)'
        ],
        'snacks': [
            'Roasted chana or makhana',
            'Watermelon or cucumber slices'
        ],
        'avoid': [
            'All fried snacks and chips',
            'Refined sugar and desserts',
            'Alcohol and sugary beverages',
            'Heavy carb-rich evening meals'
        ],
        'tips': [
            'Include 30 min strength + 20 min cardio daily',
            'Drink a glass of water before every meal',
            'Avoid stress eating with mindfulness practice'
        ]
    },
    'Obesity_Type_I': {
        'emoji': '🔴',
        'color': '#ef4444',
        'label': 'Obesity Type I',
        'daily_calories': 1600,
        'breakfast': [
            'Oats with berries (no sugar)',
            'Two boiled eggs or egg whites',
            'Green tea (no milk/sugar)'
        ],
        'lunch': [
            'Brown rice (small portion, 100g cooked)',
            'Grilled chicken breast',
            'Large bowl of salad with lemon dressing'
        ],
        'dinner': [
            'Dal or lentil soup',
            'One to two whole wheat roti',
            'Mixed vegetable stir-fry (minimal oil)'
        ],
        'snacks': [
            'A handful of unsalted almonds',
            'Apple or pear (avoid mangoes/bananas)'
        ],
        'avoid': [
            'All fried foods (samosa, pakoda, fries)',
            'Sugary drinks and packaged juices',
            'White bread and refined flour products',
            'Processed snacks and chocolates'
        ],
        'tips': [
            'Walk 30–45 minutes daily, 5 days a week',
            'Drink at least 3L water every day',
            'Avoid eating anything after 8 PM'
        ]
    },
    'Obesity_Type_II': {
        'emoji': '🚨',
        'color': '#dc2626',
        'label': 'Obesity Type II',
        'daily_calories': 1500,
        'breakfast': [
            'Moong dal chilla (2 pieces, no oil)',
            'One boiled egg white',
            'Black coffee or warm lemon water'
        ],
        'lunch': [
            'Boiled/steamed chicken (100g) with salad',
            'Mixed dal (thin consistency)',
            'Stir-fried vegetables (minimal oil)'
        ],
        'dinner': [
            'Broth-based vegetable soup',
            'One small roti with dal',
            'Steamed or grilled protein source'
        ],
        'snacks': [
            'Celery or cucumber sticks with hummus',
            'Low-sugar, low-fat yogurt'
        ],
        'avoid': [
            'All refined carbohydrates',
            'Entire food groups high in saturated fat',
            'Alcohol and aerated drinks',
            'Processed/packaged foods entirely'
        ],
        'tips': [
            'Consult a registered dietitian',
            'Track every meal with a calorie app',
            'Swimming or cycling — low-impact exercises'
        ]
    },
    'Obesity_Type_III': {
        'emoji': '⛔',
        'color': '#991b1b',
        'label': 'Obesity Type III',
        'daily_calories': 1400,
        'breakfast': [
            'Vegetable omelette (no oil, non-stick pan)',
            'Black coffee (no sugar)',
            'One medium-sized fruit (orange or guava)'
        ],
        'lunch': [
            'Large salad with grilled chicken or tofu',
            'Red lentil soup (thin)',
            'Cucumber and tomato slices'
        ],
        'dinner': [
            'Steamed or boiled vegetables',
            'Grilled fish (100g)',
            'Clear broth-based soup'
        ],
        'snacks': [
            'Celery sticks or carrot sticks',
            'Plain low-fat yogurt (unsweetened)'
        ],
        'avoid': [
            'All fried foods without exception',
            'Sugar, sweets, and desserts',
            'Alcohol of any kind',
            'Fast food and processed meals entirely'
        ],
        'tips': [
            'Consult a nutritionist and physician urgently',
            'Track every calorie consumed daily',
            'Start with low-impact exercise like swimming'
        ]
    }
}


def get_nutrition_recommendation(age, gender, height, weight, activity_level, obesity_class):
    """
    Predict calories and macros using the local AI model.
    """
    bundle = load_nutrition_model()
    if not bundle:
        return None
        
    model = bundle['model']
    le = bundle['label_encoder']
    
    # 1. Prepare Features
    gender_val = 1 if gender == 'Male' else 0
    # Map physical activity (FAF scale 0-3) to the 1.2-1.9 scale used in training
    activity_map = {0.0: 1.2, 0.75: 1.375, 1.5: 1.55, 2.25: 1.725, 3.0: 1.9}
    act_val = activity_map.get(activity_level, 1.55)
    
    try:
        class_encoded = le.transform([obesity_class])[0]
    except:
        class_encoded = le.transform(['Normal_Weight'])[0]
        
    features = np.array([[age, gender_val, height, weight, act_val, class_encoded]])
    
    # 2. Predict
    preds = model.predict(features)[0]
    
    return {
        'calories': int(preds[0]),
        'protein': float(preds[1]),
        'carbs': float(preds[2]),
        'fat': float(preds[3]),
        'is_ai': True
    }


def get_nutrition_plan(obesity_class: str, user_profile: dict = None) -> dict:
    """
    Get the nutrition plan for a given obesity class.
    If user_profile (age, gender, height, weight, activity) is provided, 
    it uses the Local AI model for precise calorie/macro calculation.
    """
    plan = NUTRITION_PLANS.get(obesity_class, NUTRITION_PLANS['Normal_Weight']).copy()
    
    if user_profile:
        ai_rec = get_nutrition_recommendation(
            age=user_profile.get('age'),
            gender=user_profile.get('gender'),
            height=user_profile.get('height'),
            weight=user_profile.get('weight'),
            activity_level=user_profile.get('activity', 1.5),
            obesity_class=obesity_class
        )
        
        if ai_rec:
            plan['daily_calories'] = ai_rec['calories']
            plan['protein_g'] = ai_rec['protein']
            plan['carbs_g'] = ai_rec['carbs']
            plan['fat_g'] = ai_rec['fat']
            plan['is_ai_powered'] = True

    return plan


def get_all_classes() -> list:
    """Return list of all obesity class keys."""
    return list(NUTRITION_PLANS.keys())
