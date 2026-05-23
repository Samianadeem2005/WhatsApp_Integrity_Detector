import os 
import sys
from src.mlproject.logger import logging
from src.mlproject.exception import CustomException
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.mlproject.utils import read_mongodb_and_merge_data

@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifacts', 'train.csv')
    test_data_path: str = os.path.join('artifacts', 'test.csv')
    raw_data_path: str = os.path.join('artifacts', 'data.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):

        logging.info("Starting data ingestion process...")
        try:
            logging.info("Reading data from MongoDB and merging with API data...")
            df = read_mongodb_and_merge_data()

            logging.info("Integrated data recieved")

            # create artifacts folder if not exists
            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True)
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            # split the data into train and test sets
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            logging.info("Data ingestion completed successfully.")

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
               
        except Exception as ex:
            raise CustomException(ex, sys)


            
        


    