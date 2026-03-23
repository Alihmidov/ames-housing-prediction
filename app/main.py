import os
import joblib
import pandas as pd
import numpy as np
from fastapi import FastAPI
from .schemas import HouseInput 

app = FastAPI(title="AMES HOUSING Prediction API")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "..", "models")

MODEL_PATH = os.path.join(MODEL_DIR, "house_price_model.joblib")
FEATURES_PATH = os.path.join(MODEL_DIR, "important_features.joblib")

model = joblib.load(MODEL_PATH)
features = joblib.load(FEATURES_PATH)

@app.get("/")
def home():
    return {"message": "AMES HOUSING API is running!"}

@app.post("/predict")
def predict(data: HouseInput):
    input_df = pd.DataFrame([data.model_dump()])
    
    input_df = input_df[features]
    
    log_prediction = model.predict(input_df)[0]
    
    real_price = np.exp(log_prediction)
    
    return {
        "estimated_price": round(float(real_price), 2),
        "currency": "USD"
    }