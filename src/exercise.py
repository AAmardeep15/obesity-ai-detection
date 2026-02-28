"""
exercise.py
-----------
Exercise recommendations for each obesity category.

Each category has:
  - goal        : what to achieve
  - weekly_target: how often to exercise
  - exercises   : list of 4 exercises (name, duration, intensity, type, description)
  - avoid       : exercises to stay away from
  - tips        : expert advice
  - bmi_tip     : one-line motivational note
"""

# ── Exercise plans for each obesity class ─────────────────────────────────────

EXERCISE_PLANS = {

    'Insufficient_Weight': {
        'goal': 'Build Muscle & Gain Healthy Weight',
        'weekly_target': '3-4 days per week',
        'banner_emoji': '🏋️',
        'exercises': [
            {
                'emoji': '🏋️',
                'name': 'Weight Training',
                'type': 'strength',
                'duration': '45 min',
                'intensity': 'Moderate',
                'desc': 'Compound movements — squats, deadlifts, bench press'
            },
            {
                'emoji': '💪',
                'name': 'Push-Ups & Pull-Ups',
                'type': 'strength',
                'duration': '15 min',
                'intensity': 'Moderate',
                'desc': '3 sets of 10-12 reps, increase gradually each week'
            },
            {
                'emoji': '🧘',
                'name': 'Yoga & Stretching',
                'type': 'flexibility',
                'duration': '20 min',
                'intensity': 'Low',
                'desc': 'Morning yoga for flexibility and better posture'
            },
            {
                'emoji': '🚶',
                'name': 'Brisk Walking',
                'type': 'cardio',
                'duration': '30 min',
                'intensity': 'Low',
                'desc': 'Light cardio without burning excess calories'
            },
        ],
        'avoid': [
            'HIIT and intense cardio',
            'Long-distance running',
            'Skipping meals after workout'
        ],
        'tips': [
            'Eat a protein-rich meal within 30 min of workout',
            'Rest at least 2 days between strength sessions',
            'Track your weight gain progress weekly'
        ],
        'bmi_tip': 'Your goal is to build lean muscle mass, not gain fat.'
    },

    'Normal_Weight': {
        'goal': 'Maintain Fitness & Stay Active',
        'weekly_target': '4-5 days per week',
        'banner_emoji': '🏃',
        'exercises': [
            {
                'emoji': '🏃',
                'name': 'Jogging / Running',
                'type': 'cardio',
                'duration': '30 min',
                'intensity': 'Moderate',
                'desc': '5 km run at a comfortable pace, 3 times per week'
            },
            {
                'emoji': '🏋️',
                'name': 'Strength Training',
                'type': 'strength',
                'duration': '40 min',
                'intensity': 'Moderate',
                'desc': 'Full-body workout twice a week'
            },
            {
                'emoji': '🚴',
                'name': 'Cycling',
                'type': 'cardio',
                'duration': '45 min',
                'intensity': 'Moderate',
                'desc': 'Outdoor or stationary cycling for endurance'
            },
            {
                'emoji': '🧘',
                'name': 'Yoga / Pilates',
                'type': 'flexibility',
                'duration': '30 min',
                'intensity': 'Low',
                'desc': 'Core strength, flexibility, and stress relief'
            },
        ],
        'avoid': [
            'Long sedentary periods (more than 2 hours)',
            'Skipping rest days',
            'Over-training without proper recovery'
        ],
        'tips': [
            'Stay active with 10,000 steps daily',
            'Mix cardio and strength for best results',
            'Drink at least 2.5 liters of water per day'
        ],
        'bmi_tip': 'Focus on maintaining your current healthy weight range.'
    },

    'Overweight_Level_I': {
        'goal': 'Burn Fat & Improve Cardio Fitness',
        'weekly_target': '4-5 days per week',
        'banner_emoji': '🚶',
        'exercises': [
            {
                'emoji': '🚶',
                'name': 'Brisk Walking',
                'type': 'cardio',
                'duration': '45 min',
                'intensity': 'Moderate',
                'desc': 'Power walking at 5-6 km/h, make it a daily habit'
            },
            {
                'emoji': '🏊',
                'name': 'Swimming',
                'type': 'cardio',
                'duration': '30 min',
                'intensity': 'Moderate',
                'desc': 'Full-body low-impact exercise, great for fat burn'
            },
            {
                'emoji': '💪',
                'name': 'Bodyweight Circuit',
                'type': 'strength',
                'duration': '25 min',
                'intensity': 'Moderate',
                'desc': 'Squats, lunges, and push-ups in timed circuits'
            },
            {
                'emoji': '🚴',
                'name': 'Cycling',
                'type': 'cardio',
                'duration': '30 min',
                'intensity': 'Moderate',
                'desc': 'Start on flat terrain, gradually increase distance'
            },
        ],
        'avoid': [
            'High-impact jumping exercises in the beginning',
            'Exercising on an empty stomach',
            'Ignoring joint pain signals'
        ],
        'tips': [
            'Start slow and increase intensity each week',
            'Walk after dinner to aid digestion and fat burn',
            'Track your calories with a fitness app'
        ],
        'bmi_tip': 'Aim to lose 0.5 to 1 kg per week gradually.'
    },

    'Overweight_Level_II': {
        'goal': 'Steady Weight Loss & Cardiovascular Health',
        'weekly_target': '5 days per week',
        'banner_emoji': '🏊',
        'exercises': [
            {
                'emoji': '🚶',
                'name': 'Interval Walking',
                'type': 'cardio',
                'duration': '45 min',
                'intensity': 'Moderate',
                'desc': 'Alternate 3 min normal walk with 1 min fast walk'
            },
            {
                'emoji': '🏊',
                'name': 'Swimming Laps',
                'type': 'cardio',
                'duration': '30 min',
                'intensity': 'Moderate',
                'desc': 'Great for joints, burns around 400 calories per hour'
            },
            {
                'emoji': '🏋️',
                'name': 'Light Strength Training',
                'type': 'strength',
                'duration': '30 min',
                'intensity': 'Low',
                'desc': 'Resistance bands and light dumbbells — twice per week'
            },
            {
                'emoji': '🧘',
                'name': 'Yoga for Weight Loss',
                'type': 'flexibility',
                'duration': '30 min',
                'intensity': 'Low',
                'desc': 'Sun salutations, warrior poses, active flow yoga'
            },
        ],
        'avoid': [
            'Running on hard surfaces (too much joint stress)',
            'Heavy weightlifting without proper form training',
            'High-sugar energy drinks after workout'
        ],
        'tips': [
            'Consistency beats intensity — show up every day',
            'Use stairs instead of elevators daily',
            'Sleep 7-8 hours — poor sleep increases hunger hormones'
        ],
        'bmi_tip': 'Small daily actions add up to big results over time.'
    },

    'Obesity_Type_I': {
        'goal': 'Safe Weight Loss & Joint-Friendly Cardio',
        'weekly_target': '5-6 days per week',
        'banner_emoji': '🏊',
        'exercises': [
            {
                'emoji': '🚶',
                'name': 'Low-Impact Walking',
                'type': 'cardio',
                'duration': '30 min',
                'intensity': 'Low',
                'desc': 'Start with 20 minutes, add 5 minutes each week'
            },
            {
                'emoji': '🏊',
                'name': 'Water Aerobics',
                'type': 'cardio',
                'duration': '30 min',
                'intensity': 'Low',
                'desc': 'Protects joints while burning calories effectively'
            },
            {
                'emoji': '🪑',
                'name': 'Chair Exercises',
                'type': 'strength',
                'duration': '20 min',
                'intensity': 'Low',
                'desc': 'Seated leg raises, arm curls, and core tightening'
            },
            {
                'emoji': '🚴',
                'name': 'Stationary Cycling',
                'type': 'cardio',
                'duration': '25 min',
                'intensity': 'Low',
                'desc': 'Low resistance cycling, easy on the knees'
            },
        ],
        'avoid': [
            'Running and jumping (too much joint stress)',
            'Intense HIIT without medical clearance',
            'Holding breath during any exercise'
        ],
        'tips': [
            'Consult your doctor before starting any routine',
            'Aim for 150 minutes of moderate activity per week',
            'Celebrate every kilogram lost — every step matters'
        ],
        'bmi_tip': 'Focus on movement, not perfection.'
    },

    'Obesity_Type_II': {
        'goal': 'Medical-Grade Exercise for Metabolic Health',
        'weekly_target': '5 days per week (start very gradually)',
        'banner_emoji': '🧘',
        'exercises': [
            {
                'emoji': '🚶',
                'name': 'Gentle Walking',
                'type': 'cardio',
                'duration': '20 min',
                'intensity': 'Very Low',
                'desc': 'Start at your own pace — every step counts'
            },
            {
                'emoji': '🏊',
                'name': 'Pool Walking',
                'type': 'cardio',
                'duration': '25 min',
                'intensity': 'Low',
                'desc': 'Walking in waist-deep water reduces joint stress by 60%'
            },
            {
                'emoji': '🧘',
                'name': 'Breathing Exercises',
                'type': 'flexibility',
                'duration': '15 min',
                'intensity': 'Very Low',
                'desc': 'Deep breathing and pranayama for stress control'
            },
            {
                'emoji': '💪',
                'name': 'Seated Resistance Band',
                'type': 'strength',
                'duration': '15 min',
                'intensity': 'Low',
                'desc': 'Gentle muscle activation from a chair or bed'
            },
        ],
        'avoid': [
            'Any high-impact activity',
            'Exercising in extreme heat',
            'Skipping water during workouts'
        ],
        'tips': [
            'Work with a physiotherapist for a safe routine',
            'Even 2,000 steps per day is a great starting point',
            'Exercise after meals helps control blood sugar levels'
        ],
        'bmi_tip': 'Safety first — start very slowly and build up gradually.'
    },

    'Obesity_Type_III': {
        'goal': 'Supervised Rehabilitation & Improving Mobility',
        'weekly_target': 'Daily gentle movement (any amount counts)',
        'banner_emoji': '🪑',
        'exercises': [
            {
                'emoji': '🪑',
                'name': 'Chair-Based Movement',
                'type': 'strength',
                'duration': '15 min',
                'intensity': 'Very Low',
                'desc': 'Seated arm swings, ankle rolls, and shoulder rolls'
            },
            {
                'emoji': '🏊',
                'name': 'Hydrotherapy / Pool',
                'type': 'cardio',
                'duration': '20 min',
                'intensity': 'Very Low',
                'desc': 'Water reduces body weight by up to 90% — safest exercise'
            },
            {
                'emoji': '🧘',
                'name': 'Deep Breathing',
                'type': 'flexibility',
                'duration': '10 min',
                'intensity': 'Very Low',
                'desc': 'Controlled breathing for lung health and relaxation'
            },
            {
                'emoji': '🚶',
                'name': 'Short Walks',
                'type': 'cardio',
                'duration': '10 min',
                'intensity': 'Very Low',
                'desc': '2-3 short walks daily improve blood circulation'
            },
        ],
        'avoid': [
            'Any unsupervised exercise',
            'Weight-bearing high-impact activity',
            'Exercising without medical clearance'
        ],
        'tips': [
            'Work with a doctor, physiotherapist, and dietitian together',
            'Focus on reducing sitting/lying time first',
            'Bed-based exercises are completely valid starting points'
        ],
        'bmi_tip': 'Every movement matters — your journey starts with one step.'
    }

}


def get_exercise_plan(obesity_class):
    """
    Return the exercise plan for a given obesity class.
    Falls back to Normal_Weight plan if class is not found.
    """
    return EXERCISE_PLANS.get(obesity_class, EXERCISE_PLANS['Normal_Weight'])
