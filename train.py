# train.py
import pickle
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression

print("Training the model...")
iris = load_iris()
X, y = iris.data, iris.target

# Increased max_iter for convergence
model = LogisticRegression(max_iter=200)
model.fit(X, y)

# Save the model to the root directory
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Model saved to model.pkl")
