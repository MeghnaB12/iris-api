# # main.py
# import pickle
# import pandas as pd
# from fastapi import FastAPI
# from pydantic import BaseModel

# # Initialize FastAPI app
# app = FastAPI(title="Iris Species Predictor API")

# # Define the request body structure using Pydantic
# class IrisRequest(BaseModel):
#     sepal_length: float
#     sepal_width: float
#     petal_length: float
#     petal_width: float

# # Load the trained model from the file
# with open('model.pkl', 'rb') as f:
#     model = pickle.load(f)

# @app.get("/")
# def read_root():
#     """A welcome message for the API root."""
#     return {"message": "Welcome to the Iris Prediction API! Visit /docs for more info."}

# @app.post("/predict")
# def predict_species(iris_features: IrisRequest):
#     """Predicts the Iris species based on input features."""
#     # Create a pandas DataFrame from the request data
#     data = pd.DataFrame([[
#         iris_features.sepal_length,
#         iris_features.sepal_width,
#         iris_features.petal_length,
#         iris_features.petal_width
#     ]], columns=['sepal_length', 'sepal_width', 'petal_length', 'petal_width'])
    
#     # Make a prediction
#     prediction = model.predict(data)
#     probability = model.predict_proba(data).max()
    
#     return {
#         "predicted_species": prediction[0],
#         "prediction_probability": round(probability, 4)
#     }


import pickle
import pandas as pd
import time
from fastapi import FastAPI
from pydantic import BaseModel

# --- OpenTelemetry ---
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter

# Tracer setup
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)
cloud_trace_exporter = CloudTraceSpanExporter()
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(cloud_trace_exporter)
)

# Initialize FastAPI app
app = FastAPI(title="Iris Species Predictor API")

# Define the request body structure using Pydantic
class IrisRequest(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

# Load the trained model from the file
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.get("/")
def read_root():
    """A welcome message for the API root."""
    return {"message": "Welcome to the Iris Prediction API! Visit /docs for more info."}

@app.post("/predict")
def predict_species(iris_features: IrisRequest):
    """Predicts the Iris species based on input features."""
    # Start OpenTelemetry span
    with tracer.start_as_current_span("predict-span") as span:
        start = time.time()

        # Prepare data
        data = pd.DataFrame([[
            iris_features.sepal_length,
            iris_features.sepal_width,
            iris_features.petal_length,
            iris_features.petal_width
        ]], columns=['sepal_length', 'sepal_width', 'petal_length', 'petal_width'])

        # Make prediction
        prediction = model.predict(data)
        probability = model.predict_proba(data).max()

        elapsed = time.time() - start

        # Add custom span attributes
        span.set_attribute("model.prediction_time", elapsed)
        span.set_attribute("prediction.result", str(prediction[0]))
        span.set_attribute("prediction.probability", float(round(probability, 4)))

        return {
            "predicted_species": prediction[0],
            "prediction_probability": round(probability, 4),
            "time_taken": round(elapsed, 6)
        }

