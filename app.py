from src.mlproject.exception import CustomException 
from src.mlproject.logger import logging
from src.mlproject.components.data_ingestion import DataIngestion
from src.mlproject.components.data_ingestion import DataIngestionConfig
import sys

if __name__ == "__main__": # This only runs when we run this file directly in terminal (eg: python app.py), not when we import it in other files.
# jis file ko hum directly run krienge terminal mei uska label __main__ set hojyega , aur jis file ko hum import krienge uska label us file ka naam set hojyega, islie jb main.py terminal mei run ho to __name__== "__main__" main.py ka set hojta hai na k app ka , ilsie iske andr ka ye code apne ap ni chlta .
    logging.info("Execution has started.")

    try:
        data_ingestion = DataIngestion() # create an object of DataIngestion class to call the initiate_data_ingestion function.
        data_ingestion.initiate_data_ingestion()
     
    except Exception as ex:
        raise CustomException(ex, sys)