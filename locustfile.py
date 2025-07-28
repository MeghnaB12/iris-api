from locust import HttpUser, task, between
import random

class IrisUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def predict(self):
        payload = {
            "sepal_length": round(random.uniform(4.0, 7.0), 2),
            "sepal_width": round(random.uniform(2.0, 4.5), 2),
            "petal_length": round(random.uniform(1.0, 6.9), 2),
            "petal_width": round(random.uniform(0.1, 2.5), 2)
        }
        self.client.post("/predict", json=payload)
