import os
import sys
import pandas as pd
import certifi
from pymongo import MongoClient
from dotenv import load_dotenv
from src.mlproject.exception import CustomException
from src.mlproject.logger import logging

load_dotenv()
MONGO_URI = os.getenv('MONGO_URI')


def read_mongodb_and_merge_data():
    """
    Fully dynamic:
      - 3 collections se data fetch karo
      - Har DataFrame par row-wise index primary key jaise treat karo
      - Columns ko side-by-side (amne samne) jorna hai, rows neeche stack nahi karni
      - Koi column name explicitly mention nahi hota
    """
    logging.info("🧠 Fully dynamic column-wise merge pipeline initiated.")
    try:
        # 1. MongoDB connection
        client = MongoClient(
            MONGO_URI,
            tlsCAFile=certifi.where()
        )
        db = client["cyber_security_db"]

        logging.info("📥 Fetching raw records from 'Whatsapp_data' and 'phishing_collection'...")

        data_wa = list(db["Whatsapp_data"].find({}, {"_id": 0}))
        data_email = list(db["email_phishing"].find({}, {"_id": 0}))
        data_phish = list(db["phishing_collection"].find({}, {"_id": 0}))

        # 2. Convert to DFs (can be empty)
        df_wa = pd.DataFrame(data_wa) if data_wa else pd.DataFrame()
        df_phish = pd.DataFrame(data_phish) if data_phish else pd.DataFrame()

        if df_wa.empty  and df_phish.empty:
            raise Exception("All targeted MongoDB cloud collections are completely empty!")

        # 3. Har DF ke liye index ko primary key jaisa treat karo
        #    Aur source prefix se column names distinguish kar do (optional but useful)
        dfs = []

        if not df_wa.empty:
            df_wa = df_wa.reset_index(drop=True)
            df_wa = df_wa.add_prefix("wa_")  # e.g. wa_sender_phone, wa_body, ...
            dfs.append(df_wa)


        if not df_phish.empty:
            df_phish = df_phish.reset_index(drop=True)
            df_phish = df_phish.add_prefix("phish_")
            dfs.append(df_phish)

        # 4. Determine max length among all DFs
        max_len = max(len(df) for df in dfs)

        # 5. Har DF ko max_len tak reindex karo (taake row-wise align ho sake)
        aligned_dfs = []
        for df in dfs:
            aligned = df.reindex(range(max_len))
            aligned_dfs.append(aligned)

        # 6. Columns ko side-by-side jorna (axis=1)
        df_master = pd.concat(aligned_dfs, axis=1)

        # 7. Cleanup
        df_master = df_master.fillna("")

        logging.info(f"📊 Column-wise merged DataFrame shape: {df_master.shape}")
        logging.info(f"📋 Columns after merge: {list(df_master.columns)}")

        return df_master

    except Exception as ex:
        raise CustomException(ex, sys)