import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load CVAP data for Hillsborough County, Florida
print("Loading CVAP data for Hillsborough County, Florida...")
try:
    cvap_data = pd.read_csv('CVAP_2019-2023_ACS_csv_files/County.csv', encoding='latin-1')
except:
    cvap_data = pd.read_csv('CVAP_2019-2023_ACS_csv_files/County.csv', encoding='utf-8', errors='ignore')

# Filter for Hillsborough County, Florida
hillsborough_cvap = cvap_data[cvap_data['geoname'] == 'Hillsborough County, Florida'].copy()

print(f"\n{'='*60}")
print("HILLSBOROUGH COUNTY CVAP ANALYSIS")
print(f"{'='*60}")

# Display key demographic data
print(f"\n📊 TOTAL POPULATION BREAKDOWN:")
total_row = hillsborough_cvap[hillsborough_cvap['lntitle'] == 'Total'].iloc[0]
print(f"   Total Population: {total_row['tot_est']:,}")
print(f"   Adult Population (18+): {total_row['adu_est']:,}")
print(f"   Total Citizens: {total_row['cit_est']:,}")
print(f"   Citizen Voting Age Population (CVAP): {total_row['cvap_est']:,}")

# Racial breakdown
print(f"\n👥 RACIAL DEMOGRAPHICS:")
racial_data = hillsborough_cvap[hillsborough_cvap['lntitle'].isin([
    'White Alone', 'Black or African American Alone', 'Asian Alone', 
    'American Indian or Alaska Native Alone', 'Native Hawaiian or Other Pacific Islander Alone',
    'Hispanic or Latino'
])]

for _, row in racial_data.iterrows():
    race = row['lntitle']
    total_pop = row['tot_est']
    cvap = row['cvap_est']
    total_pct = (total_pop / total_row['tot_est']) * 100
    cvap_pct = (cvap / total_row['cvap_est']) * 100
    print(f"   {race}: {total_pop:,} total ({total_pct:.1f}%) | {cvap:,} CVAP ({cvap_pct:.1f}%)")

# Load police stops data for comparison
print(f"\n🚔 POLICE STOPS DATA COMPARISON:")
police_data = pd.read_csv('fl_tampa_2020_04_01.csv')

# Filter for Hillsborough County stops (Tampa Police Department and Hillsborough County Sheriff's Office)
hillsborough_stops = police_data[
    police_data['department_name'].str.contains('Tampa Police Department|Hillsborough County Sheriff', na=False)
].copy()

print(f"   Total Police Stops in Hillsborough County: {len(hillsborough_stops):,}")

# Racial breakdown of police stops
race_stops = hillsborough_stops['subject_race'].value_counts()
print(f"\n   Police Stops by Race:")
for race, count in race_stops.head(5).items():
    pct = (count / len(hillsborough_stops)) * 100
    print(f"     {race}: {count:,} stops ({pct:.1f}%)")

# Create comparison analysis
print(f"\n{'='*60}")
print("DEMOGRAPHIC COMPARISON: CVAP vs POLICE STOPS")
print(f"{'='*60}")

# Create comparison dataframe
comparison_data = []

# Map police stop races to CVAP categories
race_mapping = {
    'white': 'White Alone',
    'black': 'Black or African American Alone', 
    'hispanic': 'Hispanic or Latino',
    'asian/pacific islander': 'Asian Alone',
    'other': 'Other Races'
}

for police_race, cvap_race in race_mapping.items():
    if police_race in race_stops.index:
        police_count = race_stops[police_race]
        police_pct = (police_count / len(hillsborough_stops)) * 100
        
        # Find corresponding CVAP data
        cvap_row = hillsborough_cvap[hillsborough_cvap['lntitle'] == cvap_race]
        if not cvap_row.empty:
            cvap_count = cvap_row.iloc[0]['cvap_est']
            cvap_pct = (cvap_count / total_row['cvap_est']) * 100
            
            # Calculate disparity ratio
            disparity_ratio = police_pct / cvap_pct if cvap_pct > 0 else 0
            
            comparison_data.append({
                'Race': police_race.title(),
                'CVAP_Count': cvap_count,
                'CVAP_Percentage': cvap_pct,
                'Police_Stops': police_count,
                'Police_Percentage': police_pct,
                'Disparity_Ratio': disparity_ratio
            })

comparison_df = pd.DataFrame(comparison_data)

print(f"\n📊 COMPARISON TABLE:")
print(f"{'Race':<15} {'CVAP %':<8} {'Stops %':<8} {'Ratio':<8}")
print("-" * 40)
for _, row in comparison_df.iterrows():
    print(f"{row['Race']:<15} {row['CVAP_Percentage']:<8.1f} {row['Police_Percentage']:<8.1f} {row['Disparity_Ratio']:<8.2f}")

# Create visualizations
print(f"\n📈 CREATING VISUALIZATIONS...")

# 1. CVAP vs Police Stops Comparison
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# CVAP Distribution
cvap_races = ['White Alone', 'Black or African American Alone', 'Hispanic or Latino', 'Asian Alone']
cvap_values = []
cvap_labels = []

for race in cvap_races:
    row = hillsborough_cvap[hillsborough_cvap['lntitle'] == race]
    if not row.empty:
        cvap_values.append(row.iloc[0]['cvap_est'])
        cvap_labels.append(race.replace(' Alone', '').replace(' or Latino', ''))

ax1.pie(cvap_values, labels=cvap_labels, autopct='%1.1f%%', startangle=90)
ax1.set_title('CVAP Distribution by Race')

# Police Stops Distribution
police_races = ['white', 'black', 'hispanic', 'other']
police_values = []
police_labels = []

for race in police_races:
    if race in race_stops.index:
        police_values.append(race_stops[race])
        police_labels.append(race.title())

ax2.pie(police_values, labels=police_labels, autopct='%1.1f%%', startangle=90)
ax2.set_title('Police Stops by Race')

plt.tight_layout()
plt.savefig('visualizations/18_cvap_vs_police_comparison.png', dpi=300, bbox_inches='tight')
plt.close()

# 2. Disparity Analysis
fig, ax = plt.subplots(figsize=(12, 6))
races = comparison_df['Race']
ratios = comparison_df['Disparity_Ratio']

bars = ax.bar(races, ratios, color=['#FF6B6B' if r > 1.5 else '#4ECDC4' if r > 1.0 else '#45B7D1' for r in ratios])
ax.axhline(y=1.0, color='red', linestyle='--', alpha=0.7, label='Equal Representation')
ax.set_title('Police Stop Disparity Ratio (Stops % / CVAP %)', fontsize=14, fontweight='bold')
ax.set_ylabel('Disparity Ratio')
ax.set_xlabel('Race')
ax.legend()

# Add value labels
for bar, ratio in zip(bars, ratios):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 0.05,
            f'{ratio:.2f}', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('visualizations/19_disparity_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

# 3. Detailed comparison chart
fig, ax = plt.subplots(figsize=(14, 8))
x = np.arange(len(comparison_df))
width = 0.35

bars1 = ax.bar(x - width/2, comparison_df['CVAP_Percentage'], width, label='CVAP %', color='#4ECDC4')
bars2 = ax.bar(x + width/2, comparison_df['Police_Percentage'], width, label='Police Stops %', color='#FF6B6B')

ax.set_xlabel('Race')
ax.set_ylabel('Percentage')
ax.set_title('CVAP vs Police Stops Percentage Comparison', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(comparison_df['Race'])
ax.legend()

# Add value labels
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{height:.1f}%', ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig('visualizations/20_detailed_comparison.png', dpi=300, bbox_inches='tight')
plt.close()

# Summary statistics
print(f"\n{'='*60}")
print("KEY INSIGHTS")
print(f"{'='*60}")

print(f"\n🎯 DEMOGRAPHIC REPRESENTATION:")
for _, row in comparison_df.iterrows():
    if row['Disparity_Ratio'] > 1.5:
        print(f"   ⚠️  {row['Race']}: OVER-represented in police stops ({row['Disparity_Ratio']:.2f}x)")
    elif row['Disparity_Ratio'] < 0.8:
        print(f"   ✅ {row['Race']}: UNDER-represented in police stops ({row['Disparity_Ratio']:.2f}x)")
    else:
        print(f"   ⚖️  {row['Race']}: FAIRLY represented ({row['Disparity_Ratio']:.2f}x)")

print(f"\n📊 STATISTICAL SUMMARY:")
print(f"   Total CVAP in Hillsborough County: {total_row['cvap_est']:,}")
print(f"   Total Police Stops Analyzed: {len(hillsborough_stops):,}")
print(f"   Average Disparity Ratio: {comparison_df['Disparity_Ratio'].mean():.2f}")
print(f"   Highest Disparity: {comparison_df['Disparity_Ratio'].max():.2f}")
print(f"   Lowest Disparity: {comparison_df['Disparity_Ratio'].min():.2f}")

print(f"\n🔍 METHODOLOGICAL NOTES:")
print(f"   • CVAP data: 2019-2023 ACS 5-year estimates")
print(f"   • Police stops: 1973-2018 historical data")
print(f"   • Geographic scope: Hillsborough County, Florida")
print(f"   • Disparity ratio > 1.5 indicates over-representation")
print(f"   • Disparity ratio < 0.8 indicates under-representation")

print(f"\n📁 FILES CREATED:")
print(f"   • visualizations/18_cvap_vs_police_comparison.png")
print(f"   • visualizations/19_disparity_analysis.png")
print(f"   • visualizations/20_detailed_comparison.png")

print(f"\n{'='*60}")
print("ANALYSIS COMPLETE")
print(f"{'='*60}") 