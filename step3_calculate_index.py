import pandas as pd
import numpy as np

print("Loading merged data...")
data = pd.read_csv('merged_aadhaar_data.csv')

print(f"Original shape: {data.shape}")

# Fill missing values with 0 (no updates means 0)
data = data.fillna(0)

print("Missing values after filling:")
print(data.isnull().sum().sum())

# Calculate total demographic and biometric updates
print("\nCalculating update totals...")
data['total_demo_updates'] = data['demo_age_5_17'] + data['demo_age_17_']
data['total_bio_updates'] = data['bio_age_5_17'] + data['bio_age_17_']
data['total_enrolments'] = data['age_0_5'] + data['age_5_17'] + data['age_18_greater']

# Calculate Digital Literacy Index (DLI)
# DLI = bio_updates / demo_updates (avoid division by zero)
print("Calculating Digital Literacy Index...")
data['DLI'] = np.where(
    data['total_demo_updates'] > 0,
    data['total_bio_updates'] / data['total_demo_updates'],
    0
)

# Calculate Infrastructure Gap Score
# IGS = (enrolments - bio_updates) / enrolments
print("Calculating Infrastructure Gap Score...")
data['IGS'] = np.where(
    data['total_enrolments'] > 0,
    (data['total_enrolments'] - data['total_bio_updates']) / data['total_enrolments'],
    0
)

# Cap DLI at reasonable values (some ratios can be > 1, that's fine but cap outliers)
data['DLI'] = data['DLI'].clip(0, 5)

print(f"\nFinal dataset shape: {data.shape}")
print(f"\nNew columns: {list(data.columns)}")

# Summary statistics
print("\n" + "="*60)
print("DIGITAL LITERACY INDEX STATISTICS:")
print("="*60)
print(data['DLI'].describe())

print("\n" + "="*60)
print("INFRASTRUCTURE GAP SCORE STATISTICS:")
print("="*60)
print(data['IGS'].describe())

# Save processed data
data.to_csv('processed_aadhaar_data.csv', index=False)
print("\n✅ Processed data saved to 'processed_aadhaar_data.csv'")

# Show top 10 states by average DLI
print("\n" + "="*60)
print("TOP 10 STATES BY DIGITAL LITERACY INDEX:")
print("="*60)
state_dli = data.groupby('state')['DLI'].mean().sort_values(ascending=False).head(10)
print(state_dli)

# Show bottom 10 states (Digital Deserts)
print("\n" + "="*60)
print("BOTTOM 10 STATES (DIGITAL DESERTS):")
print("="*60)
state_dli_bottom = data.groupby('state')['DLI'].mean().sort_values(ascending=True).head(10)
print(state_dli_bottom)
