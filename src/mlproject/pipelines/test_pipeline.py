import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

import pandas as pd
from src.mlproject.pipelines.prediction_pipeline import CustomData, PredictPipeline

data = CustomData(
    phone_number="923001234567",
    message_text="URGENT: Your bank account is suspended. "
)
df = data.get_data_as_data_frame()
pipeline = PredictPipeline()
result, confidence = pipeline.predict(df)

print(f"Result: {'SPAM' if result[0]==1 else 'SAFE'}")
print(f"Confidence: {confidence}%")