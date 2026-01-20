import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

print("Loading processed data...")
data = pd.read_csv('processed_aadhaar_data.csv')

# Clean state names (remove typos and duplicates)
print("Cleaning state names...")
state_mapping = {
    'West bengal': 'West Bengal',
    'West Bengli': 'West Bengal',
    'West Bangal': 'West Bengal',
    'West  Bengal': 'West Bengal',
    'WESTBENGAL': 'West Bengal',
    'WEST BENGAL': 'West Bengal',
    'Uttaranchal': 'Uttarakhand',
    'Dadra & Nagar Haveli': 'Dadra and Nagar Haveli',
    'Andaman & Nicobar Islands': 'Andaman and Nicobar Islands'
}
data['state'] = data['state'].replace(state_mapping)

# Remove invalid entries
data = data[data['state'] != '100000']
data = data[data['state'] != 'Puttenahalli']

# Convert date to datetime
data['date'] = pd.to_datetime(data['date'], format='%d-%m-%Y')

print(f"Cleaned data shape: {data.shape}")

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (15, 10)

# ============================================================
# VISUALIZATION 1: Top 20 Digital Desert Districts
# ============================================================
print("\nCreating Visualization 1: Top 20 Digital Desert Districts...")

district_data = data.groupby(['state', 'district']).agg({
    'DLI': 'mean',
    'IGS': 'mean',
    'total_demo_updates': 'sum',
    'total_bio_updates': 'sum',
    'total_enrolments': 'sum'
}).reset_index()

# Filter districts with significant activity
district_data = district_data[district_data['total_demo_updates'] > 100]

# Sort by lowest DLI (digital deserts)
digital_deserts = district_data.sort_values('DLI').head(20)

plt.figure(figsize=(12, 8))
bars = plt.barh(range(len(digital_deserts)), digital_deserts['DLI'].values)
plt.yticks(range(len(digital_deserts)), 
           [f"{row['district']}, {row['state']}" for _, row in digital_deserts.iterrows()],
           fontsize=10)
plt.xlabel('Digital Literacy Index (DLI)', fontsize=12, fontweight='bold')
plt.title('Top 20 Digital Desert Districts (Lowest DLI)\n⚠️ Priority Intervention Zones', 
          fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('viz1_digital_deserts.png', dpi=300, bbox_inches='tight')
print("✅ Saved: viz1_digital_deserts.png")
plt.close()

# ============================================================
# VISUALIZATION 2: State-wise Digital Literacy Index Heatmap
# ============================================================
print("\nCreating Visualization 2: State-wise Comparison...")

state_stats = data.groupby('state').agg({
    'DLI': 'mean',
    'total_demo_updates': 'sum',
    'total_bio_updates': 'sum'
}).reset_index()

state_stats = state_stats.sort_values('DLI', ascending=False)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 10))

# Left plot: DLI by state
colors = ['green' if x > 0.3 else 'orange' if x > 0.15 else 'red' for x in state_stats['DLI']]
ax1.barh(range(len(state_stats)), state_stats['DLI'].values, color=colors)
ax1.set_yticks(range(len(state_stats)))
ax1.set_yticklabels(state_stats['state'].values, fontsize=9)
ax1.set_xlabel('Digital Literacy Index', fontsize=12, fontweight='bold')
ax1.set_title('State-wise Digital Literacy Index\n🟢 Good (>0.3) 🟠 Moderate (0.15-0.3) 🔴 Critical (<0.15)', 
              fontsize=12, fontweight='bold')
ax1.axvline(x=0.3, color='green', linestyle='--', alpha=0.5, label='Good threshold')
ax1.axvline(x=0.15, color='orange', linestyle='--', alpha=0.5, label='Moderate threshold')
ax1.legend()

# Right plot: Bio vs Demo Updates
ax2.scatter(state_stats['total_demo_updates'], state_stats['total_bio_updates'], 
            s=200, alpha=0.6, c=state_stats['DLI'], cmap='RdYlGn')
for idx, row in state_stats.iterrows():
    if row['total_demo_updates'] > 50000 or row['total_bio_updates'] > 50000:
        ax2.annotate(row['state'], (row['total_demo_updates'], row['total_bio_updates']),
                    fontsize=8, alpha=0.7)
ax2.plot([0, state_stats['total_demo_updates'].max()], 
         [0, state_stats['total_demo_updates'].max()], 
         'r--', alpha=0.5, label='Equal line (ideal)')
ax2.set_xlabel('Total Demographic Updates', fontsize=12, fontweight='bold')
ax2.set_ylabel('Total Biometric Updates', fontsize=12, fontweight='bold')
ax2.set_title('Demographic vs Biometric Updates by State', fontsize=12, fontweight='bold')
ax2.legend()

plt.tight_layout()
plt.savefig('viz2_state_comparison.png', dpi=300, bbox_inches='tight')
print("✅ Saved: viz2_state_comparison.png")
plt.close()

# ============================================================
# VISUALIZATION 3: Time Series Trends
# ============================================================
print("\nCreating Visualization 3: Time Series Trends...")

daily_trends = data.groupby('date').agg({
    'total_demo_updates': 'sum',
    'total_bio_updates': 'sum',
    'DLI': 'mean',
    'total_enrolments': 'sum'
}).reset_index()

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10))

# Updates over time
ax1.plot(daily_trends['date'], daily_trends['total_demo_updates'], 
         label='Demographic Updates', linewidth=2, marker='o', markersize=3)
ax1.plot(daily_trends['date'], daily_trends['total_bio_updates'], 
         label='Biometric Updates', linewidth=2, marker='s', markersize=3)
ax1.fill_between(daily_trends['date'], 
                 daily_trends['total_demo_updates'], 
                 daily_trends['total_bio_updates'], 
                 alpha=0.2, color='red', label='Gap (Digital Divide)')
ax1.set_xlabel('Date', fontsize=12, fontweight='bold')
ax1.set_ylabel('Number of Updates', fontsize=12, fontweight='bold')
ax1.set_title('Demographic vs Biometric Updates Over Time', fontsize=14, fontweight='bold')
ax1.legend()
ax1.grid(True, alpha=0.3)

# DLI trend over time
ax2.plot(daily_trends['date'], daily_trends['DLI'], 
         linewidth=2, marker='o', markersize=4, color='purple')
ax2.axhline(y=daily_trends['DLI'].mean(), color='r', linestyle='--', 
            label=f'Average DLI: {daily_trends["DLI"].mean():.3f}')
ax2.fill_between(daily_trends['date'], daily_trends['DLI'], 
                 daily_trends['DLI'].mean(), alpha=0.3)
ax2.set_xlabel('Date', fontsize=12, fontweight='bold')
ax2.set_ylabel('Digital Literacy Index', fontsize=12, fontweight='bold')
ax2.set_title('Digital Literacy Index Trend', fontsize=14, fontweight='bold')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('viz3_time_series.png', dpi=300, bbox_inches='tight')
print("✅ Saved: viz3_time_series.png")
plt.close()

# ============================================================
# VISUALIZATION 4: District-level Risk Matrix
# ============================================================
print("\nCreating Visualization 4: Risk Matrix...")

# Calculate risk score: Low DLI + High activity = High priority
district_data['risk_score'] = (1 - district_data['DLI']) * np.log1p(district_data['total_demo_updates'])
high_risk = district_data.sort_values('risk_score', ascending=False).head(30)

plt.figure(figsize=(14, 10))
scatter = plt.scatter(high_risk['DLI'], high_risk['total_demo_updates'], 
                     s=high_risk['risk_score']*10, alpha=0.6, 
                     c=high_risk['risk_score'], cmap='Reds')
plt.colorbar(scatter, label='Risk Score')

for idx, row in high_risk.head(15).iterrows():
    plt.annotate(f"{row['district']}, {row['state']}", 
                (row['DLI'], row['total_demo_updates']),
                fontsize=7, alpha=0.8)

plt.xlabel('Digital Literacy Index (DLI)', fontsize=12, fontweight='bold')
plt.ylabel('Total Demographic Updates (Activity Level)', fontsize=12, fontweight='bold')
plt.title('District Risk Matrix\n🔴 High Risk = Low DLI + High Activity = Needs Urgent Intervention', 
          fontsize=14, fontweight='bold')
plt.axvline(x=0.2, color='orange', linestyle='--', alpha=0.5, label='DLI Threshold (0.2)')
plt.legend()
plt.tight_layout()
plt.savefig('viz4_risk_matrix.png', dpi=300, bbox_inches='tight')
print("✅ Saved: viz4_risk_matrix.png")
plt.close()

print("\n" + "="*60)
print("✅ ALL VISUALIZATIONS CREATED SUCCESSFULLY!")
print("="*60)
print("\nGenerated files:")
print("  1. viz1_digital_deserts.png")
print("  2. viz2_state_comparison.png")
print("  3. viz3_time_series.png")
print("  4. viz4_risk_matrix.png")
