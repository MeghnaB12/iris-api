from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import joblib
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='plot.png')
    args = parser.parse_args()

    # Load data
    iris = load_iris()
    X, y = iris.data, iris.target
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train model
    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    joblib.dump(model, 'iris_model.pkl')

    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f'Accuracy: {accuracy}')

    # Generate plot
    plt.scatter(X_test[:, 0], X_test[:, 1], c=y_pred, cmap='viridis')
    plt.title('Iris Predictions')
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.savefig(args.output)
    plt.close()

if __name__ == '__main__':
    main()
