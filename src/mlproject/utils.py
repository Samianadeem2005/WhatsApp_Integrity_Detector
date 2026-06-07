import os
import sys
import numpy as np
import pandas as pd
import certifi
import pickle
from pymongo import MongoClient
from dotenv import load_dotenv
from src.mlproject.exception import CustomException
from src.mlproject.logger import logging
from sklearn.metrics import f1_score
from sklearn.model_selection import GridSearchCV

load_dotenv()
MONGO_URI = os.getenv('MONGO_URI')

def read_whatsapp_data():
    logging.info("🧠 WhatsApp data ingestion pipeline started.")
    try:
        client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
        db = client["cyber_security_db"]

        logging.info("📥 Fetching records from 'Whatsapp_data'...")
        # Direct fetch
        data_wa = list(db["Whatsapp_data"].find({}, {"_id": 0}))
        
        if not data_wa:
            raise Exception("Collection 'Whatsapp_data' is empty!")

        # DataFrame creation
        df = pd.DataFrame(data_wa)
                
        # Cleanup
        df = df.fillna("")

        logging.info(f"📊 DataFrame shape: {df.shape}")
        return df

    except Exception as ex:
        raise CustomException(ex, sys)
    

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e, sys)
    

def evaluate_models(X_train, y_train, X_test, y_test, models, param):
    try:
        report = {}

        for i in range(len(list(models))):
            model = list(models.values())[i]
            para = param[list(models.keys())[i]]

            # Hyperparameter tuning using GridSearchCV
            gs = GridSearchCV(model, para, cv=3, scoring='f1') # 👈 Scoring ko f1 kar diya
            gs.fit(X_train, y_train)

            # Best parameters set kar ke model ko train kiya
            model.set_params(**gs.best_params_)
            model.fit(X_train, y_train)

            # Test data par predictions nikali
            y_test_pred = model.predict(X_test)

            # Phishing classification ke liye F1-score evaluate kiya
            test_model_score = f1_score(y_test, y_test_pred, average='binary')

            # Report dictionary mein model ka naam aur uska F1-score save kar liya
            report[list(models.keys())[i]] = test_model_score

        return report

    except Exception as e:
        raise CustomException(e, sys)

def load_object(file_path):
    try:
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)

    except Exception as e:
        raise CustomException(e, sys)