import pandas as pd
import os

print("Starting data load test...")

if not os.path.exists('processed_aadhaar_data.csv'):
    print("ERROR: processed_aadhaar_data.csv missing")
else:
    print("processed_aadhaar_data.csv exists")

if not os.path.exists('district_predictions_enhanced.csv'):
    print("WARNING: district_predictions_enhanced.csv missing")
else:
    print("district_predictions_enhanced.csv exists")

try:
    data = pd.read_csv('processed_aadhaar_data.csv')
    print(f"Data loaded, shape: {data.shape}")
    print(f"Data columns: {data.columns.tolist()}")
except Exception as e:
    print(f"Error loading data: {e}")

try:
    if os.path.exists('district_predictions_enhanced.csv'):
        clusters = pd.read_csv('district_predictions_enhanced.csv')
        print(f"Enhanced clusters loaded, shape: {clusters.shape}")
        print(f"Cluster columns: {clusters.columns.tolist()}")
        if 'cluster_label' not in clusters.columns:
            if 'risk_level' in clusters.columns:
                print("Mapping risk_level to cluster_label")
                clusters['cluster_label'] = clusters['risk_level'].map({
                    0: 'Thriving',
                    1: 'Struggling', 
                    2: 'Critical'
                })
            else:
                print("ERROR: neither cluster_label nor risk_level in columns")
    elif os.path.exists('district_clusters.csv'):
        clusters = pd.read_csv('district_clusters.csv')
        print(f"Basic clusters loaded, shape: {clusters.shape}")
        print(f"Cluster columns: {clusters.columns.tolist()}")
    else:
        print("ERROR: No cluster file found")
except Exception as e:
    print(f"Error loading clusters: {e}")
