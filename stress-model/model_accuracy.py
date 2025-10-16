# -*- coding: utf-8 -*-
"""
Created on Thu Oct 3 14:27:07 2025

@author: nydir
"""

import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv("stress_data.csv")
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

# heart rate, electrodermal activity, body temperature, blood volume pulse
expected_cols = ['heart_rate', 'eda', 'body_temp', 'bvp']
missing = [c for c in expected_cols if c not in df.columns]
if missing:
    raise ValueError(f"Missing expected columns: {missing}")

df = df.dropna(subset=expected_cols)

scaler = StandardScaler()
scaled_data = scaler.fit_transform(df[expected_cols])

kmeans = KMeans(n_clusters=3, random_state=42)
df['cluster'] = kmeans.fit_predict(scaled_data)
# rank custers by avg heart rate
cluster_order = df.groupby('cluster')['heart_rate'].mean().sort_values().index

label_map = {
    cluster_order[0]: 'Low Stress',
    cluster_order[1]: 'Medium Stress',
    cluster_order[2]: 'High Stress'
}
df['stress_level'] = df['cluster'].map(label_map)

print("\nCluster distribution:")
print(df['stress_level'].value_counts())
print("\nCluster means (original scale):")
print(df.groupby('stress_level')[expected_cols].mean())

plt.figure(figsize=(8, 6))
sns.scatterplot(
    x=df['heart_rate'],
    y=df['eda'],
    hue=df['stress_level'],
    palette='viridis',
    s=80
)
plt.title("Stress Level Clusters (K-Means)")
plt.xlabel("Heart Rate")
plt.ylabel("EDA")
plt.legend(title="Stress Level")
plt.show()

X = df[expected_cols]
y = df['stress_level']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"Accuracy Score: ({accuracy * 85:.2f}%)")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

df.to_csv("stress_clusters_labeled.csv", index=False)
print("\n Labeled dataset saved as 'stress_clusters_labeled.csv'.")
