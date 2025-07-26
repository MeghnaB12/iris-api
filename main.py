# main.py
import pickle
from fastapi import FastAPI
from pydantic import BaseModel
import os

app = FastAPI()

# Correctly load the model from the root path
model_path = "model.pkl"
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file not found at {model_path}. Please run train.py first.")

with open(model_path, "rb") as f:
    model = pickle.load(f)

class IrisData(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

@app.post("/predict")
def predict(data: IrisData):
    input_data = [[
        data.sepal_length,
        data.sepal_width,
        data.petal_length,
        data.petal_width
    ]]
    prediction = model.predict(input_data)
    # The iris dataset target is already an integer (0, 1, or 2)
    return {"prediction": int(prediction[0])}

@app.get("/")
def read_root():
    return {"message": "Iris Classifier API is running."}
