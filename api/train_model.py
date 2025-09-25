# train_model.py
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib
import os

os.makedirs("models", exist_ok=True)

# Toy synthetic dataset: features [heart_rate, sleep_hours, workload_score]
rng = np.random.RandomState(0)
X = np.column_stack([
    rng.normal(70, 10, 1000),     # heart_rate
    rng.normal(7, 1.5, 1000),     # sleep_hours
    rng.uniform(0, 10, 1000)      # workload_score
])
# target: stress_score 0..100 (toy)
y = 0.4*X[:,0] + 3*(10-X[:,1]) + 2*X[:,2] + rng.normal(0,10,1000)
y = np.clip(y, 0, 100)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestRegressor(n_estimators=50, random_state=0)
model.fit(X_train, y_train)

joblib.dump(model, "models/stress_model.joblib")
print("Saved model to models/stress_model.joblib")
