# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 16:22:15 2025

@author: nydir
"""

# SAMPLE stress classifier -- to be built upon for increased accuracy and handling of more complex datasets

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, accuracy_score

# Features: [heart_rate, skin_conductance, body_temp, respiration_rate]
# Label: 0 = Low stress, 1 = Medium stress, 2 = High stress

np.random.seed(42)
n_samples = 300

heart_rate = np.random.normal(70, 10, n_samples) + np.random.randint(0, 30, n_samples)
skin_conductance = np.random.normal(5, 2, n_samples) + np.random.randint(0, 5, n_samples)
body_temp = np.random.normal(36.5, 0.5, n_samples) + np.random.rand(n_samples)
respiration_rate = np.random.normal(16, 3, n_samples) + np.random.randint(0, 5, n_samples)

# Stress levels: simple synthetic rule
labels = []
for hr, sc in zip(heart_rate, skin_conductance):
    if hr < 80 and sc < 6:
        labels.append(0)  # Low stress
    elif hr < 100 and sc < 8:
        labels.append(1)  # Medium stress
    else:
        labels.append(2)  # High stress

data = pd.DataFrame({
    "heart_rate": heart_rate,
    "skin_conductance": skin_conductance,
    "body_temp": body_temp,
    "respiration_rate": respiration_rate,
    "stress_level": labels
})


# 2. Train-Test Split

X = data.drop("stress_level", axis=1)
y = data["stress_level"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 3. Scale Data

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)


# 4. Train Classifier

model = KNeighborsClassifier(n_neighbors=5)
model.fit(X_train, y_train)


# 5. Evaluate

y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))


# 6. Example Prediction

example = np.array([[95, 8.5, 37.2, 20]])  # HR, SC, Temp, Respiration
example_scaled = scaler.transform(example)
pred = model.predict(example_scaled)
print("Predicted stress level:", pred[0])

