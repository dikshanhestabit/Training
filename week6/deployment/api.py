
import pandas as pd
import joblib
import os
import sys
import json
import logging
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime
import uuid

# Configuring logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Adding project root to path for imports if needed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from features.feature_engineer import FeatureEngineer


# Initializing FastAPI app
app = FastAPI(title="Adult Income Prediction API", version="1.0.0")

# Paths
MODEL_PATH = os.path.join('models', 'best_tuned_model.pkl')
PIPELINE_PATH = os.path.join('features', 'feature_pipeline.pkl')
FEATURE_LIST_PATH = os.path.join('features', 'feature_list.json')
LOGS_PATH = os.path.join('monitoring', 'prediction_logs.csv')

# Global variables for artifacts
model = None
pipeline = None
selected_features = None

class PredictionRequest(BaseModel):
    age: int = Field(..., example=39)
    workclass: str = Field(..., example="State-gov")
    fnlwgt: int = Field(..., example=77516)
    education: str = Field(..., example="Bachelors")
    education_num: int = Field(..., alias="education.num", example=13)
    marital_status: str = Field(..., alias="marital.status", example="Never-married")
    occupation: str = Field(..., example="Adm-clerical")
    relationship: str = Field(..., example="Not-in-family")
    race: str = Field(..., example="White")
    sex: str = Field(..., example="Male")
    capital_gain: int = Field(..., alias="capital.gain", example=2174)
    capital_loss: int = Field(..., alias="capital.loss", example=0)
    hours_per_week: int = Field(..., alias="hours.per.week", example=40)
    native_country: str = Field(..., alias="native.country", example="United-States")

    class Config:
        allow_population_by_field_name = True

@app.on_event("startup")
def load_artifacts():
    global model, pipeline, selected_features
    try:
        logger.info("Loading model and artifacts...")
        
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model not found at {MODEL_PATH}")
        model = joblib.load(MODEL_PATH)
        
        if not os.path.exists(PIPELINE_PATH):
            raise FileNotFoundError(f"Pipeline not found at {PIPELINE_PATH}")
        pipeline = joblib.load(PIPELINE_PATH)
        
        if not os.path.exists(FEATURE_LIST_PATH):
             raise FileNotFoundError(f"Feature list not found at {FEATURE_LIST_PATH}")
        
        with open(FEATURE_LIST_PATH, 'r') as f:
            feature_data = json.load(f)
            selected_features = feature_data.get('selected_features', [])
            
        logger.info("Artifacts loaded successfully.")
    except Exception as e:
        logger.error(f"Error loading artifacts: {e}")
        raise e

def log_prediction(request_id: str, input_data: Dict, prediction: int, probability: float):
    """Log prediction details to CSV."""
    os.makedirs(os.path.dirname(LOGS_PATH), exist_ok=True)
    
    log_entry = {
        'request_id': request_id,
        'timestamp': datetime.now().isoformat(),
        'prediction': prediction,
        'probability': probability,
        **input_data 
    }
    
    df_log = pd.DataFrame([log_entry])
    
    if not os.path.exists(LOGS_PATH):
        df_log.to_csv(LOGS_PATH, index=False)
    else:
        df_log.to_csv(LOGS_PATH, mode='a', header=False, index=False)

@app.post("/predict")
def predict(request: PredictionRequest):
    global model, pipeline, selected_features
    
    request_id = str(uuid.uuid4())
    input_data = request.dict(by_alias=True)
    
    try:
        # 1. Convert to DataFrame
        df_input = pd.DataFrame([input_data])
        
        # 2. Transform Features
        X_transformed = pipeline.transform(df_input)
        
        # 3. Align Columns: Ensure consistency with model expectation
        for feature in selected_features:
            if feature not in X_transformed.columns:
                X_transformed[feature] = 0
                
        # Select and Reorder to match training exactly
        X_final = X_transformed[selected_features]

        # 4. Predict
        prediction = model.predict(X_final)[0]
        probability = model.predict_proba(X_final)[0][1]
        
        # 5. Log
        log_prediction(request_id, input_data, int(prediction), float(probability))
        
        result = {
            "request_id": request_id,
            "prediction": ">50K" if prediction == 1 else "<=50K",
            "probability": float(probability)
        }
        
        return result

    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
