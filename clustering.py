# clustering.py
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

def run_clustering():
    # Load data
    df = pd.read_csv("stress_data.csv")
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

    # Select features
    features = ['heart_rate', 'eda', 'body_temp', 'bvp']
    X = df[features]

    # Standardize
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Run KMeans
    kmeans = KMeans(n_clusters=3, random_state=42)
    df['cluster'] = kmeans.fit_predict(X_scaled)

    # Map clusters to labels
    cluster_labels = {0: "Low Stress", 1: "Medium Stress", 2: "High Stress"}
    df['stress_level'] = df['cluster'].map(cluster_labels)

    # Cluster distribution
    cluster_counts = df['stress_level'].value_counts()

    # Cluster means
    cluster_means = df.groupby('stress_level')[features].mean()

    # Save labeled data
    df.to_csv("stress_clusters_labeled.csv", index=False)

    # Return results
    return {
        'cluster_counts': cluster_counts.to_dict(),
        'cluster_means': cluster_means.reset_index(),
        'records': df.head().to_dict(orient='records')
    }
