import os
import sys
from dataclasses import dataclass

# Regressors hata kar Classifiers import kiye
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression

# Classification metrics import kiye
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

from src.mlproject.exception import CustomException
from src.mlproject.logger import logging
from src.mlproject.utils import save_object, evaluate_models

@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifacts", "model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, X_train_proc, X_test_proc, y_train, y_test):
        try:
            logging.info("Splitting training and test input data directly from transformation stage")
            
            # Ab hamin array slice karne ki zaroorat nahi, direct input variables use karenge
            X_train = X_train_proc
            X_test = X_test_proc

            # Classifiers ka dictionary setup
            models = {
                "Random Forest": RandomForestClassifier(random_state=42),
                "Decision Tree": DecisionTreeClassifier(random_state=42),
                "Gradient Boosting": GradientBoostingClassifier(random_state=42),
                "Logistic Regression": LogisticRegression(random_state=42),
                "XGBClassifier": XGBClassifier(random_state=42),
                "AdaBoost Classifier": AdaBoostClassifier(random_state=42),
            }

            # Classification ke mutabiq params set kiye
            params = {
                "Decision Tree": {
                    'criterion': ['gini', 'entropy', 'log_loss'],
                },
                "Random Forest": { },
                
                "Gradient Boosting": {
                    'learning_rate': [0.1, 0.05, 0.01],
                    'subsample': [0.7, 0.8, 0.9],
                    'n_estimators': [16, 32, 64, 128]
                },
                "Logistic Regression": {},
                "XGBClassifier": {
                    'learning_rate': [0.1, 0.05, 0.01],
                    'n_estimators': [16, 32, 64, 128]
                },
                "AdaBoost Classifier": {
                    'learning_rate': [0.1, 0.5, 1.0],
                    'n_estimators': [16, 32, 64, 128]
                }
            }

            # NOTE: Apne utils.py ke evaluate_models function ke andar bhi 
            # r2_score ki jagah accuracy_score ya f1_score lagana parega!
            logging.info("Evaluating models based on classification metrics")
            model_report: dict = evaluate_models(
                X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test,
                models=models, param=params
            )
            
            # Jo model sab se best performance report de (Hum F1-score ko base bana sakte hain)
            best_model_score = max(sorted(model_report.values()))

            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model = models[best_model_name]

            # Phishing dataset ke liye balance test threshold check
            if best_model_score < 0.6:
                raise CustomException("No best classifier model found with acceptable score")
            
            logging.info(f"Best model found: {best_model_name} with score: {best_model_score}")

            # Winner model ko save kar liya
            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )

            # Final metrics check karne ke liye predictions nikalein
            predicted = best_model.predict(X_test)

            final_f1 = f1_score(y_test, predicted)
            final_precision = precision_score(y_test, predicted)
            final_recall = recall_score(y_test, predicted)

            logging.info(f"Final Model Metrics -> Precision: {final_precision:.4f}, Recall: {final_recall:.4f}, F1: {final_f1:.4f}")

            # Aap yahan se F1-score return karwa sakti hain
            return final_f1
            
        except Exception as e:
            raise CustomException(e, sys)