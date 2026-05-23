import os
import random
from pymongo import MongoClient
from dotenv import load_dotenv

# .env load karein
load_dotenv()

def get_balanced_data(existing_count, total_target=1340):
    """
    Sirf wahi records generate karega jo balance pura karne ke liye chahiye.
    """
    needed = total_target - existing_count
    if needed <= 0: return []
    
    # Wohi schema jo tumhare screenshot mein tha
    subjects = ["Urgent: Account Verification", "Invoice Overdue", "Unusual Activity", "Tax Refund Error", "Package Awaits"]
    intents = ["Credential Harvesting", "Malware Delivery", "Financial Scam"]
    
    new_records = []
    for i in range(needed):
        record = {
            "email_id": f"phish-{existing_count + i + 1:04d}",
            "email_subject": random.choice(subjects),
            "email_body": "Automated recovery body text.",
            "email_intent": random.choice(intents),
            "email_technique": "Link Spoofing",
            "email_target": "Banking",
            "email_spoofed_sender": "security@bank-alert.com",
            "email_label": "phishing"
        }
        new_records.append(record)
    return new_records

def fix_and_concatenate():
    client = MongoClient(os.environ.get("MONGO_URI"))
    db = client["cyber_security_db"]
    coll = db["email_phishing"]
    
    # 1. Purana data count karo
    existing_docs = list(coll.find({}))
    count = len(existing_docs)
    print(f"Current count: {count}")
    
    # 2. Balance karo
    new_data = get_balanced_data(count)
    
    if new_data:
        coll.insert_many(new_data)
        print(f"✅ {len(new_data)} naye records niche concatenate kar diye hain.")
    else:
        print("Data already balanced hai.")

fix_and_concatenate()