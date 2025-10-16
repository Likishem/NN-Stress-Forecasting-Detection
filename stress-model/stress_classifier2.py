# stress classification

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("stress_data.csv")

print("First few records:")
print(df.head())

df = df.dropna()

scaler = StandardScaler()
scaled_data = scaler.fit_transform(df)

inertia = []
K = range(1, 10)
for k in K:
    km = KMeans(n_clusters=k, random_state=42)
    km.fit(scaled_data)
    inertia.append(km.inertia_)

plt.figure(figsize=(6, 4))
plt.plot(K, inertia, 'bo-')
plt.xlabel('Number of clusters (k)')
plt.ylabel('Inertia')
plt.title('Elbow Method for Optimal k')
plt.show()

kmeans = KMeans(n_clusters=3, random_state=42)
df['stress_level'] = kmeans.fit_predict(scaled_data)

print("\nCluster centers (standardized scale):")
print(kmeans.cluster_centers_)

plt.figure(figsize=(8, 6))
sns.scatterplot(
    x=df.iloc[:, 0],
    y=df.iloc[:, 1],
    hue=df['stress_level'],
    palette='viridis',
    s=60
)
plt.title("Stress Level Clusters")
plt.xlabel("Heart Rate")
plt.ylabel("EDA")
plt.show()

df.to_csv("stress_clusters_output.csv", index=False)
print("\nClustered data saved as 'stress_clusters_output.csv'.")


