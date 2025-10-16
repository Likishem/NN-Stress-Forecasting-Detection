# stress classification

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
from flask import Flask, jsonify

# --- Data Processing ---
df = pd.read_csv("stress_data.csv")

print("First few records:")
print(df.head())

df = df.dropna()

scaler = StandardScaler()
scaled_data = scaler.fit_transform(df)

# Elbow method for choosing k
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
plt.savefig("elbow_plot.png")   # ✅ Save, don't show
plt.close()

# Fit model with 3 clusters
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
plt.savefig("stress_clusters.png")  # ✅ Save, don't show
plt.close()

df.to_csv("stress_clusters_output.csv", index=False)
print("\n✅ Clustered data saved as 'stress_clusters_output.csv'.")

# --- Flask App ---
app = Flask(__name__)

def home():
    return """
    <h1>✅ Stress Classifier Running Successfully!</h1>
    <p>View <a href="/results">/results</a> for summary</p>
    <p>View <a href="/plot">/plot</a> to see the cluster image</p>
    """

@app.route('/results')
def results():
    cluster_counts = df['stress_level'].value_counts().to_dict()
    return jsonify({
        "clusters": cluster_counts,
        "message": "Stress classification completed."
    })

@app.route('/plot')
def plot():
    from flask import send_file
    return send_file("stress_clusters.png", mimetype='image/png')

if __name__ == '__main__':
    # Host 0.0.0.0 allows Docker to expose it externally
    app.run(host='0.0.0.0', port=5000, debug=True)
