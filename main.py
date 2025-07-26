from flask import Flask, request, jsonify
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

app = Flask(__name__)

# Load or train model
model_path = 'iris_model.pkl'
if os.path.exists(model_path):
    model = joblib.load(model_path)
else:
    iris = load_iris()
    model = RandomForestClassifier()
    model.fit(iris.data, iris.target)
    joblib.dump(model, model_path)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    features = [data['features']]
    prediction = model.predict(features).tolist()
    return jsonify({'prediction': prediction})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
