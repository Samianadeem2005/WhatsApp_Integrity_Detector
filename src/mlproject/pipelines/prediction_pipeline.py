import sys
import os  # Yeh zaroori hai path join karne ke liye
import pandas as pd
from src.mlproject.exception import CustomException
from src.mlproject.utils import load_object

class PredictPipeline:
    def __init__(self):
        pass

    def predict(self, features):
        try:
            # Yeh wohi path hai jahan aap ka model save hai
            model_path = os.path.join("artifacts", "model.pkl")
            preprocessor_path = os.path.join("artifacts", "preprocessor.pkl")
            
            # Logic: Load the objects (Yeh files aap ke disk par honi chahiye)
            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)
            
            # Logic: Data ko transform karo aur predict karo
            data_scaled = preprocessor.transform(features['body'])
            preds = model.predict(data_scaled)
            proba = model.predict_proba(data_scaled)

            print("="*50)
            print(f"MODEL CLASSES: {model.classes_}")
            print(f"FULL PROBA ARRAY: {proba}")
            print(f"PROBA[0]: {proba[0]}")
            print(f"PREDICTION: {preds}")
            print(f"PROBA[0][0]: {proba[0][0]}")
            print(f"PROBA[0][1]: {proba[0][1]}")
            print("="*50)

            classes = list(model.classes_)

            if 1 in classes:
                spam_index = classes.index(1)
            elif 'spam' in classes:
                spam_index = classes.index('spam')
            else:
                spam_index = len(classes) - 1

            spam_probability = float(proba[0][spam_index])
            confidence = round(spam_probability * 100, 1)
            return preds, confidence
        
        except Exception as e:
            raise CustomException(e, sys)

class CustomData:
    def __init__(self, phone_number: str, message_text: str):
        self.phone_number = phone_number
        self.message_text = message_text

    def get_data_as_data_frame(self):
        try:
            # DataFrame banana taake pipeline ise process kar sake
            custom_data_input_dict = {
                "body": [self.message_text] # Model sirf 'body' column par trained hai
            }
            return pd.DataFrame(custom_data_input_dict)
        except Exception as e:
            raise CustomException(e, sys)