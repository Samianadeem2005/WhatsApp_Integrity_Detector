import os
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def insert_csv_to_mongodb():
    MONGO_URI = os.environ.get("MONGO_URI")
    DB_NAME = "cyber_security_db" 
    TARGET_COLLECTION_NAME = "Whatsapp_data"
    CSV_FILE_PATH = "notebook/data/data.csv"  # Tumhari CSV ka path

    try:
        print("⏳ Connecting to MongoDB...")
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db[TARGET_COLLECTION_NAME]

        # 1. Pandas se CSV read karo
        if not os.path.exists(CSV_FILE_PATH):
            print(f"🔴 Error: File nahi mili at {CSV_FILE_PATH}")
            return
            
        print("📊 Reading CSV file...")
        df = pd.read_csv(CSV_FILE_PATH)
        
        # 2. DataFrame ko list of dictionaries mein convert karo (MongoDB format)
        data_to_insert = df.to_dict(orient="records")
        
        print(f"📦 Dataset parsed: {len(data_to_insert)} records ready hain.")

        # 3. Insert into MongoDB
        if data_to_insert:
            print(f"🚀 Inserting into `{TARGET_COLLECTION_NAME}`...")
            result = collection.insert_many(data_to_insert)
            print(f"✅ SUCCESS: {len(result.inserted_ids)} records cloud par chale gaye!")
        else:
            print("⚠️ CSV khali hai.")

    except Exception as e:
        print(f"🔴 Error aya: {e}")
    finally:
        if 'client' in locals():
            client.close()
            print("🔒 Cloud connection closed.")

if __name__ == "__main__":
    insert_csv_to_mongodb()

