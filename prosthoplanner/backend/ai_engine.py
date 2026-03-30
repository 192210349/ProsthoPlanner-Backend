import joblib
import pandas as pd
import numpy as np
import os

class AIEngine:
    def __init__(self):
        try:
            # Get the directory of the current script
            base_dir = os.path.dirname(os.path.abspath(__file__))
            model_dir = os.path.join(base_dir, 'models')
            
            model_path = os.path.join(model_dir, 'treatment_model.pkl')
            encoder_path = os.path.join(model_dir, 'encoders.pkl')
            mapping_path = os.path.join(model_dir, 'plan_mappings.pkl')
            
            if not os.path.exists(model_path):
                # Try one level up if run from a different context
                alt_model_dir = os.path.join(os.getcwd(), 'backend', 'models')
                if os.path.exists(alt_model_dir):
                    model_dir = alt_model_dir
                    model_path = os.path.join(model_dir, 'treatment_model.pkl')
                    encoder_path = os.path.join(model_dir, 'encoders.pkl')
                    mapping_path = os.path.join(model_dir, 'plan_mappings.pkl')
                else:
                    raise FileNotFoundError(f"Model file not found at {model_path}")
            
            self.model = joblib.load(model_path)
            self.encoders = joblib.load(encoder_path)
            self.mappings = joblib.load(mapping_path)
            print("AI Model, Encoders, and Mappings loaded.")
        except Exception as e:
            print(f"Error loading AI model: {e}")
            self.model = None
            self.encoders = None
            self.mappings = None

    def suggest(self, patient_data, vision_data=None):
        if not self.model or not self.encoders or not self.mappings:
            return None
        
        try:
            # Prepare input data
            input_dict = {
                'age': [int(patient_data.get('age', 0))],
                'gender': [patient_data.get('gender', 'Other')],
                'is_diabetic': [1 if patient_data.get('is_diabetic') else 0],
                'is_smoker': [1 if patient_data.get('is_smoker') else 0],
                'kennedy_class': [patient_data.get('kennedy_classification', 'Class I')],
                'tissue_condition': [patient_data.get('tissue_condition', 'Healthy')],
                'occlusion_type': [patient_data.get('occlusion_type', 'Balanced')]
            }
            
            # Incorporate vision results if available
            if vision_data:
                # Example: If vision detects bone loss, force tissue condition to 'Compromised' for logic
                if vision_data.get('bone_loss_detected'):
                    input_dict['tissue_condition'] = ['Thin/Resorbed']
                if vision_data.get('bone_density') == 'Type IV':
                    input_dict['is_diabetic'] = [1] # Force higher risk profile

            input_df = pd.DataFrame(input_dict)
            
            # Encode categorical inputs
            for col in ['gender', 'kennedy_class', 'tissue_condition', 'occlusion_type']:
                le = self.encoders[col]
                val = input_df[col].iloc[0]
                if val not in le.classes_:
                    val = le.classes_[0]
                input_df[col] = le.transform([val])
                
            # Predict Case Profile
            profile_idx = self.model.predict(input_df)[0]
            profile_name = self.encoders['case_profile'].inverse_transform([profile_idx])[0]
            
            # Retrieve A, B, C plans
            plans = self.mappings.get(profile_name)
            
            # Enrich plans with vision insights if provided
            if vision_data:
                for tier in ['A', 'B', 'C']:
                    plans[tier]['vision_insight'] = "Based on imaging analysis"
                    
            return plans
            
        except Exception as e:
            print(f"AI Prediction Error: {e}")
            return None
