# train.py

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle
import os

# Load Iris dataset
iris = load_iris()
X, y = iris.data, iris.target

# Split into train and test (optional)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate the model (optional)
accuracy = model.score(X_test, y_test)
print(f" Model trained with accuracy: {accuracy:.2f}")

# Ensure 'app/' directory exists
os.makedirs("app", exist_ok=True)

# Save the model to app/model.pkl
model_path = os.path.join("app", "model.pkl")
with open(model_path, "wb") as f:
    pickle.dump(model, f)

print(f" Model saved to {model_path}")
