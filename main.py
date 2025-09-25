# Filename: main.py
from fastapi import FastAPI
from pydantic import BaseModel
import joblib  # if you have a trained model saved, e.g., joblib.load("model.pkl")

app = FastAPI(title="Stress Forecasting API")

# Input data schema
class StressInput(BaseModel):
    heart_rate: float
    sleep_hours: float
    workload_score: float   # e.g., 0–10 scale

# Load your trained model (replace with your real model file)
# model = joblib.load("stress_model.pkl")

@app.get("/")
def root():
    return {"message": "Stress Forecasting API is running"}

@app.post("/predict")
def predict_stress(data: StressInput):
    # Example: simple rule-based logic (replace with ML model prediction)
    score = 0.4 * data.heart_rate + 0.3 * (10 - data.sleep_hours) + 0.3 * data.workload_score
    if score < 50:
        level = "Low"
    elif score < 80:
        level = "Moderate"
    else:
        level = "High"
    return {
        "heart_rate": data.heart_rate,
        "sleep_hours": data.sleep_hours,
        "workload_score": data.workload_score,
        "predicted_stress_level": level
    }

# Run locally with: uvicorn main:app --reload
