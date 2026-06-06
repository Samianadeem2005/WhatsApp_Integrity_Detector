import os
import sys
import re
import numpy as np
import pandas as pd
from dataclasses import dataclass
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline

# Modular components integration
from src.mlproject.exception import CustomException
from src.mlproject.logger import logging
from src.mlproject.utils import save_object

@dataclass
class DataTransformationConfig:
    # Krish Naik ke standards ke mutabiq variable ka naam handle kiya
    preprocessor_obj_file_path: str = os.path.join('artifacts', 'preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        """
        This function is responsible for text data transformation using TF-IDF pipeline.
        """
        try:
            logging.info("Initializing TF-IDF Vectorizer pipeline steps.")
            
            text_pipeline = Pipeline(steps=[
                ('tfidf', TfidfVectorizer(
                    max_features=1000,
                    stop_words='english',
                    ngram_range=(1, 2)
                ))
            ])
            
            logging.info("TF-IDF pipeline created successfully.")
            return text_pipeline

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_transformation(self, train_path, test_path):
        try:
            logging.info(f"Loading training data from: {train_path}")
            train_df = pd.read_csv(train_path)
            
            logging.info(f"Loading testing data from: {test_path}")
            test_df = pd.read_csv(test_path)

            logging.info("Encoding target label column into binary (phishing=1, safe=0)")
            train_df['label'] = (train_df['label'].str.lower().str.strip() == 'phishing').astype(int)
            test_df['label']  = (test_df['label'].str.lower().str.strip() == 'phishing').astype(int)

            # Extract features and targets cleanly
            X_train = train_df['body'].fillna('')
            y_train = train_df['label']
            X_test  = test_df['body'].fillna('')
            y_test  = test_df['label']

            logging.info("Obtaining preprocessing vectorizer object.")
            preprocessing_obj = self.get_data_transformer_object()

            logging.info("Applying fit_transform on training features and transform on testing features.")
            X_train_proc = preprocessing_obj.fit_transform(X_train)
            X_test_proc  = preprocessing_obj.transform(X_test)

            logging.info(f"Saving preprocessing pipeline object to artifacts folder.")
            
            # Using custom utility script helper to safely dump pickle file
            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )

            logging.info("Data transformation pipeline stage executed successfully.")

            return (
                X_train_proc,
                X_test_proc,
                y_train,
                y_test,
                self.data_transformation_config.preprocessor_obj_file_path
            )

        except Exception as e:
            raise CustomException(e, sys)