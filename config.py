import os
from dotenv import load_dotenv

load_dotenv()

MODEL_PATH = "model/fraud_model.pkl"
DATASET_PATH = "dataset/insurance_data.csv"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

UPLOAD_FOLDER = "uploads"