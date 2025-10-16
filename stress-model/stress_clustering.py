
# stress clustering (7866)

import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("stress_data.csv")

df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

# heart rate, electrodermal activity, body temperature, blood volume pulse
expected_cols = ['heart_rate', 'eda', 'body_temp', 'bvp']
missing = [c for c in expected_cols if c not in df.columns]
if missing:
    raise ValueError(f"Missing expected columns: {missing}")

# Drop rows with missing values
df = df.dropna(subset=expected_cols)

scaler = StandardScaler()
scaled_data = scaler.fit_transform(df[expected_cols])

kmeans = KMeans(n_clusters=3, random_state=42)
df['cluster'] = kmeans.fit_predict(scaled_data)

# Rank clusters by average heart rate
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

df.to_csv("stress_clusters_labeled.csv", index=False)
print("\n Labeled dataset saved as 'stress_clusters_labeled.csv'.")

