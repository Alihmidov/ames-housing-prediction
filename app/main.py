import os
import joblib
import pandas as pd
import numpy as np
from fastapi import FastAPI
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from .schemas import HouseInput 

load_dotenv()

app = FastAPI(title="AMES HOUSING Prediction API")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "..", "models")

MODEL_PATH = os.path.join(MODEL_DIR, "house_price_model.joblib")
FEATURES_PATH = os.path.join(MODEL_DIR, "important_features.joblib")

model = joblib.load(MODEL_PATH)
features = joblib.load(FEATURES_PATH)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# SQLAlchemy engine yaradırıq
engine = create_engine(DATABASE_URL)

@app.get("/")
def home():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        db_status = "Connected"
    except Exception as e:
        db_status = f"Disconnected: {str(e)}"
        
    return {
        "message": "AMES HOUSING API is running!",
        "database_status": db_status
    }

@app.post("/predict")
def predict(data: HouseInput):
    input_dict = data.model_dump()
    input_df = pd.DataFrame([input_dict])
    
    input_df = input_df[features]
    
    log_prediction = model.predict(input_df)[0]
    real_price = np.exp(log_prediction)
        
    return {
        "estimated_price": round(float(real_price), 2),
        "currency": "USD"
    }