from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle
import numpy as np
import os

# Define request schema using Pydantic
class IrisFeatures(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

# Initialize FastAPI app
app = FastAPI(
    title="Iris Classifier API",
    description="A simple API that classifies Iris flowers using a pre-trained model.",
    version="1.0.0"
)

# Load the model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")
try:
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
except FileNotFoundError:
    model = None
    print("Model file not found. Make sure 'model.pkl' is in the app directory.")

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Iris Classifier API!"}

# Prediction endpoint
@app.post("/predict")
def predict_species(features: IrisFeatures):
    if not model:
        raise HTTPException(status_code=500, detail="Model not loaded.")
    
    data = np.array([[features.sepal_length, features.sepal_width,
                      features.petal_length, features.petal_width]])
    
    try:
        prediction = model.predict(data)[0]
        return {"predicted_species": str(prediction)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction failed: {str(e)}")

