import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import warnings
warnings.filterwarnings('ignore')

print("Loading processed data...")
data = pd.read_csv('processed_aadhaar_data.csv')

# Clean data
state_mapping = {
    'West bengal': 'West Bengal', 'West Bengli': 'West Bengal',
    'West Bangal': 'West Bengal', 'West  Bengal': 'West Bengal',
    'WESTBENGAL': 'West Bengal', 'WEST BENGAL': 'West Bengal',
    'Uttaranchal': 'Uttarakhand', 'Dadra & Nagar Haveli': 'Dadra and Nagar Haveli',
    'Andaman & Nicobar Islands': 'Andaman and Nicobar Islands'
}
data['state'] = data['state'].replace(state_mapping)
data = data[~data['state'].isin(['100000', 'Puttenahalli'])]

print(f"Data shape: {data.shape}")

# ============================================================
# MODEL 1: K-Means Clustering for District Categories
# ============================================================
print("\n" + "="*60)
print("MODEL 1: K-MEANS CLUSTERING")
print("="*60)

# Aggregate by district
district_features = data.groupby(['state', 'district']).agg({
    'DLI': 'mean',
    'IGS': 'mean',
    'total_demo_updates': 'sum',
    'total_bio_updates': 'sum',
    'total_enrolments': 'sum'
}).reset_index()

# Filter active districts
district_features = district_features[district_features['total_demo_updates'] > 50]

# Select features for clustering
features_for_clustering = district_features[['DLI', 'total_demo_updates', 'total_bio_updates']].values

# Standardize features
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features_for_clustering)

# K-Means with 5 clusters
kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
district_features['cluster'] = kmeans.fit_predict(features_scaled)

# Analyze clusters
print("\nCluster Analysis:")
cluster_summary = district_features.groupby('cluster').agg({
    'DLI': ['mean', 'std'],
    'total_demo_updates': ['mean', 'sum'],
    'total_bio_updates': ['mean', 'sum'],
    'district': 'count'
}).round(3)
print(cluster_summary)

# Assign meaningful labels based on DLI
cluster_labels = {}
for cluster_id in range(5):
    avg_dli = district_features[district_features['cluster'] == cluster_id]['DLI'].mean()
    if avg_dli > 0.4:
        cluster_labels[cluster_id] = 'Thriving'
    elif avg_dli > 0.25:
        cluster_labels[cluster_id] = 'Progressing'
    elif avg_dli > 0.15:
        cluster_labels[cluster_id] = 'Struggling'
    elif avg_dli > 0.05:
        cluster_labels[cluster_id] = 'Critical'
    else:
        cluster_labels[cluster_id] = 'Emergency'

district_features['cluster_label'] = district_features['cluster'].map(cluster_labels)

print("\nCluster Labels:")
print(district_features['cluster_label'].value_counts())

# Visualize clusters
plt.figure(figsize=(14, 8))
colors = {'Thriving': 'green', 'Progressing': 'lightgreen', 
          'Struggling': 'orange', 'Critical': 'red', 'Emergency': 'darkred'}
for label in cluster_labels.values():
    subset = district_features[district_features['cluster_label'] == label]
    plt.scatter(subset['DLI'], subset['total_demo_updates'], 
                label=label, alpha=0.6, s=100, c=colors.get(label, 'gray'))

plt.xlabel('Digital Literacy Index (DLI)', fontsize=12, fontweight='bold')
plt.ylabel('Total Demographic Updates', fontsize=12, fontweight='bold')
plt.title('District Clustering: 5 Categories Based on Digital Literacy', 
          fontsize=14, fontweight='bold')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('model1_clustering.png', dpi=300, bbox_inches='tight')
print("\n✅ Saved: model1_clustering.png")
plt.close()

# Save cluster results
district_features.to_csv('district_clusters.csv', index=False)
print("✅ Saved: district_clusters.csv")

# ============================================================
# MODEL 2: Random Forest - Predict At-Risk Districts
# ============================================================
print("\n" + "="*60)
print("MODEL 2: RANDOM FOREST CLASSIFICATION")
print("="*60)

# Create binary target: At-Risk (DLI < 0.2) vs Safe
district_features['at_risk'] = (district_features['DLI'] < 0.2).astype(int)

print(f"\nAt-Risk Districts: {district_features['at_risk'].sum()}")
print(f"Safe Districts: {(district_features['at_risk'] == 0).sum()}")

# Features for prediction
X = district_features[['total_demo_updates', 'total_bio_updates', 'total_enrolments', 'IGS']]
y = district_features['at_risk']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train Random Forest
rf_model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
rf_model.fit(X_train, y_train)

# Predictions
y_pred = rf_model.predict(X_test)

# Evaluation
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['Safe', 'At-Risk']))

# Feature importance
feature_importance = pd.DataFrame({
    'feature': X.columns,
    'importance': rf_model.feature_importances_
}).sort_values('importance', ascending=False)

print("\nFeature Importance:")
print(feature_importance)

# Visualize feature importance
plt.figure(figsize=(10, 6))
plt.barh(feature_importance['feature'], feature_importance['importance'])
plt.xlabel('Importance', fontsize=12, fontweight='bold')
plt.title('Feature Importance for Predicting At-Risk Districts', 
          fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('model2_feature_importance.png', dpi=300, bbox_inches='tight')
print("\n✅ Saved: model2_feature_importance.png")
plt.close()

# Confusion matrix
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Reds', 
            xticklabels=['Safe', 'At-Risk'], 
            yticklabels=['Safe', 'At-Risk'])
plt.xlabel('Predicted', fontsize=12, fontweight='bold')
plt.ylabel('Actual', fontsize=12, fontweight='bold')
plt.title('Confusion Matrix - At-Risk District Prediction', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('model2_confusion_matrix.png', dpi=300, bbox_inches='tight')
print("✅ Saved: model2_confusion_matrix.png")
plt.close()

print("\n" + "="*60)
print("✅ ALL ML MODELS COMPLETED!")
print("="*60)
print("\nGenerated files:")
print("  1. model1_clustering.png")
print("  2. district_clusters.csv")
print("  3. model2_feature_importance.png")
print("  4. model2_confusion_matrix.png")
