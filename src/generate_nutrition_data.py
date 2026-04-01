import pandas as pd
import numpy as np
import os

def generate_data(num_samples=5000):
    np.random.seed(42)
    
    # 1. Features
    ages = np.random.randint(18, 70, num_samples)
    genders = np.random.choice([0, 1], num_samples) # 0: Female, 1: Male
    heights = np.random.randint(150, 200, num_samples)
    weights = np.random.randint(45, 160, num_samples)
    activity_levels = np.random.choice([1.2, 1.375, 1.55, 1.725, 1.9], num_samples)
    
    # Obesity classes (matching the dataset labels)
    obesity_classes = [
        'Insufficient_Weight', 'Normal_Weight', 'Overweight_Level_I', 
        'Overweight_Level_II', 'Obesity_Type_I', 'Obesity_Type_II', 'Obesity_Type_III'
    ]
    classes = np.random.choice(obesity_classes, num_samples)
    
    data = pd.DataFrame({
        'Age': ages,
        'Gender': genders,
        'Height': heights,
        'Weight': weights,
        'Activity': activity_levels,
        'Obesity_Class': classes
    })
    
    # 2. Logic for Targets (Based on medical formulas)
    def calculate_targets(row):
        # BMR (Mifflin-St Jeor)
        if row['Gender'] == 1:
            bmr = (10 * row['Weight']) + (6.25 * row['Height']) - (5 * row['Age']) + 5
        else:
            bmr = (10 * row['Weight']) + (6.25 * row['Height']) - (5 * row['Age']) - 161
            
        tdee = bmr * row['Activity']
        
        # Adjust based on Obesity Class
        if 'Obesity' in row['Obesity_Class']:
            target_calories = tdee - 500 # Deficit for weight loss
            protein_pct, carbs_pct, fat_pct = 0.30, 0.40, 0.30
        elif 'Overweight' in row['Obesity_Class']:
            target_calories = tdee - 300
            protein_pct, carbs_pct, fat_pct = 0.25, 0.45, 0.30
        elif row['Obesity_Class'] == 'Insufficient_Weight':
            target_calories = tdee + 500 # Surplus for weight gain
            protein_pct, carbs_pct, fat_pct = 0.20, 0.55, 0.25
        else:
            target_calories = tdee # Maintenance
            protein_pct, carbs_pct, fat_pct = 0.20, 0.50, 0.30
            
        # Bounds
        target_calories = max(1200, target_calories)
        
        # Macros in grams (Protein/Carbs: 4 cal/g, Fat: 9 cal/g)
        protein_g = (target_calories * protein_pct) / 4
        carbs_g = (target_calories * carbs_pct) / 4
        fat_g = (target_calories * fat_pct) / 9
        
        return pd.Series([
            round(target_calories, 0), 
            round(protein_g, 1), 
            round(carbs_g, 1), 
            round(fat_g, 1)
        ])

    data[['Calories', 'Protein', 'Carbs', 'Fat']] = data.apply(calculate_targets, axis=1)
    
    os.makedirs('data', exist_ok=True)
    data.to_csv('data/synthetic_nutrition_data.csv', index=False)
    print(f"Generated {num_samples} samples in data/synthetic_nutrition_data.csv")

if __name__ == "__main__":
    generate_data()
