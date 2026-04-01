import pandas as pd
import numpy as np
import pickle
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

def train_nutrition_model():
    # 1. Load Data
    data_path = 'data/synthetic_nutrition_data.csv'
    if not os.path.exists(data_path):
        print(f"Data not found at {data_path}")
        return
        
    df = pd.read_csv(data_path)
    
    # 2. Features and Targets
    X = df[['Age', 'Gender', 'Height', 'Weight', 'Activity', 'Obesity_Class']]
    y = df[['Calories', 'Protein', 'Carbs', 'Fat']]
    
    # 3. Preprocessing Pipeline
    # Encoding categorical column 'Obesity_Class'
    numeric_features = ['Age', 'Height', 'Weight', 'Activity']
    categorical_features = ['Obesity_Class', 'Gender']
    
    # We'll use a simple manual encoding or a LabelEncoder for Obesity_Class
    le = LabelEncoder()
    df['Obesity_Class_Encoded'] = le.fit_transform(df['Obesity_Class'])
    
    X = df[['Age', 'Gender', 'Height', 'Weight', 'Activity', 'Obesity_Class_Encoded']]
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 4. Train Model
    print("Training Local Nutrition AI Model...")
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # 5. Evaluate
    score = model.score(X_test, y_test)
    print(f"Model trained. Accuracy (R^2 Score): {score*100:.2f}%")
    
    # 6. Save Bundle
    os.makedirs('models', exist_ok=True)
    bundle = {
        'model': model,
        'label_encoder': le,
        'features': ['Age', 'Gender', 'Height', 'Weight', 'Activity', 'Obesity_Class_Encoded']
    }
    
    with open('models/nutrition_model.pkl', 'wb') as f:
        pickle.dump(bundle, f)
    print("Saved -> models/nutrition_model.pkl")

if __name__ == "__main__":
    train_nutrition_model()
