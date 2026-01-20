import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

print("Loading datasets...")
# Load all 3 datasets
enrolment = pd.read_csv('api_data_aadhar_enrolment/api_data_aadhar_enrolment/api_data_aadhar_enrolment_0_500000.csv')
demographic = pd.read_csv('api_data_aadhar_demographic/api_data_aadhar_demographic/api_data_aadhar_demographic_0_500000.csv')
biometric = pd.read_csv('api_data_aadhar_biometric/api_data_aadhar_biometric/api_data_aadhar_biometric_0_500000.csv')

print(f"Enrolment: {enrolment.shape}")
print(f"Demographic: {demographic.shape}")
print(f"Biometric: {biometric.shape}")

# Merge demographic and biometric first
print("\nMerging demographic and biometric data...")
merged = pd.merge(demographic, biometric, on=['date', 'state', 'district', 'pincode'], how='outer')

# Then merge with enrolment
print("Merging with enrolment data...")
final_data = pd.merge(merged, enrolment, on=['date', 'state', 'district', 'pincode'], how='outer')

print(f"\nFinal merged dataset shape: {final_data.shape}")
print(f"\nColumns: {list(final_data.columns)}")
print(f"\nFirst few rows:")
print(final_data.head())

# Check for missing values
print("\nMissing values:")
print(final_data.isnull().sum())

# Save merged data
final_data.to_csv('merged_aadhaar_data.csv', index=False)
print("\n✅ Merged data saved to 'merged_aadhaar_data.csv'")
