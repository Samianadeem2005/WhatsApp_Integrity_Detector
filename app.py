from src.mlproject.exception import CustomException 
from src.mlproject.logger import logging
import sys
import streamlit as st
import pandas as pd
import streamlit as st
from src.mlproject.pipelines.prediction_pipeline import CustomData, PredictPipeline
import Frontend


def main():
    
    Frontend.run_ui()

if __name__ == "__main__":
    main()








