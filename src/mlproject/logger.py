import logging
import os
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log" # log file name with current date and time.
LOG_PATH = os.path.join(os.getcwd(), "logs") # creates log_file_path by joining current working directory, logs folder and log file name.
os.makedirs(LOG_PATH, exist_ok=True) # creates logs directory if it does not exist.

LOG_FILE_PATH = os.path.join(LOG_PATH, LOG_FILE) 

logging.basicConfig(
    filename=LOG_FILE_PATH, 
    format='[%(asctime)s]  %(lineno)d  %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO, # 5 levels hote hain logging ke : DEBUG, INFO, WARNING, ERROR, CRITICAL. yaha humne INFO level set kiya hai, iska matlab hai ki INFO level se upar ke sare logs (WARNING, ERROR, CRITICAL) bhi log honge.
)
