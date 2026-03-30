import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib
import os

# 1. Generate Synthetic Dataset
def generate_data(n=1000):
    np.random.seed(42)
    
    data = {
        'age': np.random.randint(18, 90, n),
        'gender': np.random.choice(['Male', 'Female', 'Other'], n),
        'is_diabetic': np.random.choice([0, 1], n, p=[0.7, 0.3]),
        'is_smoker': np.random.choice([0, 1], n, p=[0.8, 0.2]),
        'kennedy_class': np.random.choice(['Class I', 'Class II', 'Class III', 'Class IV'], n),
        'tissue_condition': np.random.choice(['Healthy', 'Inflamed', 'Resorbed'], n),
        'occlusion_type': np.random.choice(['Balanced', 'Canine Protected', 'Group Function'], n)
    }
    
    df = pd.DataFrame(data)
    
    # Tiered Treatment Logic
    def get_plans(row):
        if row['kennedy_class'] == 'Class IV':
            return 'Implant Support', 150000, '4-6 Months', 'Fixed Bridge', 45000, '2-3 Weeks', 'Removable Partial', 15000, '1 Week'
        elif row['tissue_condition'] == 'Resorbed':
            return 'Implant Overdenture', 250000, '6 Months', 'Complete Denture', 35000, '3 Weeks', 'Economic Denture', 12000, '2 Weeks'
        else:
            return 'Full Ceramic Implants', 180000, '5 Months', 'Metal-Ceramic Bridge', 50000, '2 Weeks', 'Acrylic RPD', 18000, '10 Days'
            
    plans = df.apply(get_plans, axis=1)
    df[['plan_a', 'a_cost', 'a_time', 'plan_b', 'b_cost', 'b_time', 'plan_c', 'c_cost', 'c_time']] = pd.DataFrame(plans.tolist(), index=df.index)
    return df

# 2. Preprocess and Train
def train():
    df = generate_data(2000)
    
    # Use plan_a as the primary indicator for training the "Clinical Case Profile"
    df['case_profile'] = df['plan_a']
    
    le_map = {}
    cat_cols = ['gender', 'kennedy_class', 'tissue_condition', 'occlusion_type', 'case_profile']
    
    for col in cat_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        le_map[col] = le
        print(f"Encoded {col}: {dict(zip(le.classes_, le.transform(le.classes_)))}")

    # Store mapping for quick retrieval of B and C plans based on the predicted Case Profile
    profile_to_plans = {}
    for profile in le_map['case_profile'].classes_:
        row = df[df['plan_a'] == profile].iloc[0]
        profile_to_plans[profile] = {
            'A': {'treatment': row['plan_a'], 'cost': float(row['a_cost']), 'time': row['a_time']},
            'B': {'treatment': row['plan_b'], 'cost': float(row['b_cost']), 'time': row['b_time']},
            'C': {'treatment': row['plan_c'], 'cost': float(row['c_cost']), 'time': row['c_time']}
        }
    joblib.dump(profile_to_plans, 'backend/models/plan_mappings.pkl')

    X = df.drop(['plan_a', 'a_cost', 'a_time', 'plan_b', 'b_cost', 'b_time', 'plan_c', 'c_cost', 'c_time', 'case_profile'], axis=1)
    y = df['case_profile']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    print(f"Model Accuracy (Case Profile): {model.score(X_test, y_test):.2f}")
    # Save model and encoders
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_dir = os.path.join(base_dir, 'models')
    
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
        
    joblib.dump(model, os.path.join(model_dir, 'treatment_model.pkl'))
    joblib.dump(le_map, os.path.join(model_dir, 'encoders.pkl'))
    print(f"Model and encoders saved to {model_dir}")

if __name__ == "__main__":
    train()
