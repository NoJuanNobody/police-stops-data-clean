import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set style for better looking plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Load the data
print("Loading data...")
df = pd.read_csv('fl_tampa_2020_04_01.csv')

print(f"Dataset shape: {df.shape}")
print(f"Columns: {list(df.columns)}")

# Clean and prepare data
print("\nCleaning data...")

# Convert date column
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# Clean department names (remove pipe-separated values)
df['department_name_clean'] = df['department_name'].str.split('|').str[0]

# Create output directory
import os
os.makedirs('visualizations', exist_ok=True)

# 1. Race Distribution Pie Chart
print("\nCreating race distribution visualization...")
race_counts = df['subject_race'].value_counts()
race_counts = race_counts[race_counts > 1000]  # Filter out small categories

fig, ax = plt.subplots(figsize=(12, 8))
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']
wedges, texts, autotexts = ax.pie(race_counts.values, labels=race_counts.index, autopct='%1.1f%%', 
                                  colors=colors, startangle=90)
ax.set_title('Police Stops by Subject Race', fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('visualizations/1_race_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# 2. Gender Distribution Bar Chart
print("Creating gender distribution visualization...")
gender_counts = df['subject_sex'].value_counts()
gender_counts = gender_counts[gender_counts.index != 'NA']

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(gender_counts.index, gender_counts.values, color=['#FF6B6B', '#4ECDC4'])
ax.set_title('Police Stops by Subject Gender', fontsize=16, fontweight='bold')
ax.set_ylabel('Number of Stops')
ax.set_xlabel('Gender')

# Add value labels on bars
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
            f'{int(height):,}', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('visualizations/2_gender_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# 3. Age Distribution Histogram
print("Creating age distribution visualization...")
# Convert age to numeric, handling 'NA' values
df['subject_age_numeric'] = pd.to_numeric(df['subject_age'], errors='coerce')
age_data = df['subject_age_numeric'].dropna()

fig, ax = plt.subplots(figsize=(12, 6))
ax.hist(age_data, bins=30, color='#45B7D1', alpha=0.7, edgecolor='black')
ax.set_title('Age Distribution of Subjects in Police Stops', fontsize=16, fontweight='bold')
ax.set_xlabel('Age')
ax.set_ylabel('Number of Stops')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('visualizations/3_age_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# 4. Stops Over Time Line Chart
print("Creating temporal analysis visualization...")
# Filter for valid dates and group by year
df_with_dates = df[df['date'].notna()]
yearly_counts = df_with_dates.groupby(df_with_dates['date'].dt.year).size()

fig, ax = plt.subplots(figsize=(15, 6))
ax.plot(yearly_counts.index, yearly_counts.values, marker='o', linewidth=2, markersize=6, color='#FF6B6B')
ax.set_title('Police Stops Over Time', fontsize=16, fontweight='bold')
ax.set_xlabel('Year')
ax.set_ylabel('Number of Stops')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('visualizations/4_stops_over_time.png', dpi=300, bbox_inches='tight')
plt.close()

# 5. Department Activity Bar Chart
print("Creating department analysis visualization...")
dept_counts = df['department_name_clean'].value_counts().head(10)

fig, ax = plt.subplots(figsize=(14, 8))
bars = ax.barh(range(len(dept_counts)), dept_counts.values, color='#4ECDC4')
ax.set_yticks(range(len(dept_counts)))
ax.set_yticklabels(dept_counts.index)
ax.set_title('Police Stops by Department', fontsize=16, fontweight='bold')
ax.set_xlabel('Number of Stops')

# Add value labels
for i, bar in enumerate(bars):
    width = bar.get_width()
    ax.text(width + width*0.01, bar.get_y() + bar.get_height()/2,
            f'{int(width):,}', ha='left', va='center', fontweight='bold')

plt.tight_layout()
plt.savefig('visualizations/5_department_activity.png', dpi=300, bbox_inches='tight')
plt.close()

# 6. Department vs Race Heatmap
print("Creating department vs race heatmap...")
dept_race_cross = pd.crosstab(df['department_name_clean'], df['subject_race'])
# Keep only top departments and races
top_depts = dept_race_cross.sum(axis=1).nlargest(8).index
top_races = dept_race_cross.sum(axis=0).nlargest(6).index
dept_race_filtered = dept_race_cross.loc[top_depts, top_races]

fig, ax = plt.subplots(figsize=(12, 8))
sns.heatmap(dept_race_filtered, annot=True, fmt='d', cmap='YlOrRd', ax=ax)
ax.set_title('Department vs Race Heatmap', fontsize=16, fontweight='bold')
ax.set_xlabel('Subject Race')
ax.set_ylabel('Department')
plt.tight_layout()
plt.savefig('visualizations/6_dept_race_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()

# 7. Top Violations Bar Chart
print("Creating violation analysis visualization...")
# Extract main violation categories
df['violation_category'] = df['violation'].str.extract(r'(\d+)')[0]
violation_counts = df['violation_category'].value_counts().head(15)

fig, ax = plt.subplots(figsize=(14, 8))
bars = ax.barh(range(len(violation_counts)), violation_counts.values, color='#96CEB4')
ax.set_yticks(range(len(violation_counts)))
ax.set_yticklabels([f'Code {code}' for code in violation_counts.index])
ax.set_title('Top Violation Codes', fontsize=16, fontweight='bold')
ax.set_xlabel('Number of Stops')

# Add value labels
for i, bar in enumerate(bars):
    width = bar.get_width()
    ax.text(width + width*0.01, bar.get_y() + bar.get_height()/2,
            f'{int(width):,}', ha='left', va='center', fontweight='bold')

plt.tight_layout()
plt.savefig('visualizations/7_top_violations.png', dpi=300, bbox_inches='tight')
plt.close()

# 8. Violation Type by Race Stacked Bar
print("Creating violation by race analysis...")
race_violation_cross = pd.crosstab(df['subject_race'], df['violation_category'])
# Keep only top races and violations
top_races_viol = race_violation_cross.sum(axis=1).nlargest(5).index
top_violations_viol = race_violation_cross.sum(axis=0).nlargest(8).index
race_violation_filtered = race_violation_cross.loc[top_races_viol, top_violations_viol]

fig, ax = plt.subplots(figsize=(14, 8))
race_violation_filtered.plot(kind='bar', stacked=True, ax=ax, colormap='Set3')
ax.set_title('Violation Types by Race', fontsize=16, fontweight='bold')
ax.set_xlabel('Subject Race')
ax.set_ylabel('Number of Stops')
ax.legend(title='Violation Code', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('visualizations/8_violation_by_race.png', dpi=300, bbox_inches='tight')
plt.close()

# 9. Vehicle Registration State Analysis
print("Creating vehicle registration analysis...")
vehicle_state_counts = df['vehicle_registration_state'].value_counts().head(15)

fig, ax = plt.subplots(figsize=(12, 8))
bars = ax.bar(range(len(vehicle_state_counts)), vehicle_state_counts.values, color='#FFEAA7')
ax.set_title('Vehicle Registration States', fontsize=16, fontweight='bold')
ax.set_xlabel('State')
ax.set_ylabel('Number of Stops')
ax.set_xticks(range(len(vehicle_state_counts)))
ax.set_xticklabels(vehicle_state_counts.index, rotation=45)

# Add value labels
for i, bar in enumerate(bars):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
            f'{int(height):,}', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('visualizations/9_vehicle_registration.png', dpi=300, bbox_inches='tight')
plt.close()

# 10. Outcome Analysis
print("Creating outcome analysis...")
outcome_counts = df['outcome'].value_counts()

fig, ax = plt.subplots(figsize=(10, 6))
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
wedges, texts, autotexts = ax.pie(outcome_counts.values, labels=outcome_counts.index, autopct='%1.1f%%', 
                                  colors=colors[:len(outcome_counts)], startangle=90)
ax.set_title('Police Stop Outcomes', fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('visualizations/10_outcome_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

# 11. Outcome by Race Stacked Bar
print("Creating outcome by race analysis...")
race_outcome_cross = pd.crosstab(df['subject_race'], df['outcome'])
# Keep only top races and outcomes
top_races_outcome = race_outcome_cross.sum(axis=1).nlargest(5).index
top_outcomes = race_outcome_cross.sum(axis=0).nlargest(5).index
race_outcome_filtered = race_outcome_cross.loc[top_races_outcome, top_outcomes]

fig, ax = plt.subplots(figsize=(12, 8))
race_outcome_filtered.plot(kind='bar', stacked=True, ax=ax, colormap='Set2')
ax.set_title('Stop Outcomes by Race', fontsize=16, fontweight='bold')
ax.set_xlabel('Subject Race')
ax.set_ylabel('Number of Stops')
ax.legend(title='Outcome', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('visualizations/11_outcome_by_race.png', dpi=300, bbox_inches='tight')
plt.close()

# 12. Seasonal Patterns Heatmap
print("Creating seasonal analysis...")
df_with_dates = df[df['date'].notna()].copy()
df_with_dates['month'] = df_with_dates['date'].dt.month
df_with_dates['day_of_week'] = df_with_dates['date'].dt.dayofweek

monthly_dow_counts = pd.crosstab(df_with_dates['month'], df_with_dates['day_of_week'])

fig, ax = plt.subplots(figsize=(12, 8))
sns.heatmap(monthly_dow_counts, annot=True, fmt='d', cmap='YlOrRd', ax=ax)
ax.set_title('Police Stops by Month and Day of Week', fontsize=16, fontweight='bold')
ax.set_xlabel('Day of Week (0=Monday, 6=Sunday)')
ax.set_ylabel('Month')
plt.tight_layout()
plt.savefig('visualizations/12_seasonal_patterns.png', dpi=300, bbox_inches='tight')
plt.close()

# 13. Interactive Dashboard using Plotly
print("Creating interactive dashboard...")
# Create a summary dataframe for the dashboard
summary_data = {
    'Metric': ['Total Stops', 'Unique Subjects', 'Date Range', 'Departments', 'Races'],
    'Value': [
        f"{len(df):,}",
        f"{df['raw_row_number'].nunique():,}",
        f"{df_with_dates['date'].min().strftime('%Y-%m-%d')} to {df_with_dates['date'].max().strftime('%Y-%m-%d')}",
        f"{df['department_name_clean'].nunique()}",
        f"{df['subject_race'].nunique()}"
    ]
}

# Create summary table
fig = go.Figure(data=[go.Table(
    header=dict(values=['Metric', 'Value'],
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[summary_data['Metric'], summary_data['Value']],
               fill_color='lavender',
               align='left'))
])

fig.update_layout(title='Tampa Police Stops Data Summary', height=300)
fig.write_html('visualizations/13_summary_dashboard.html')

# 14. Disparity Analysis
print("Creating disparity analysis...")
# Calculate stop rates per capita (using rough population estimates)
# This is a simplified analysis - in reality you'd need actual population data
population_estimates = {
    'white': 0.6,  # Rough estimate of white population in Tampa area
    'black': 0.2,
    'hispanic': 0.15,
    'asian/pacific islander': 0.03,
    'other': 0.02
}

# Calculate stop rates
race_stop_counts = df['subject_race'].value_counts()
disparity_data = []
for race in race_stop_counts.index:
    if race in population_estimates:
        stop_rate = race_stop_counts[race] / population_estimates[race]
        disparity_data.append({
            'Race': race,
            'Stop Rate': stop_rate,
            'Population %': population_estimates[race] * 100
        })

disparity_df = pd.DataFrame(disparity_data)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Stop rates
bars1 = ax1.bar(disparity_df['Race'], disparity_df['Stop Rate'], color='#FF6B6B')
ax1.set_title('Stop Rates by Race (per capita)', fontsize=14, fontweight='bold')
ax1.set_ylabel('Stop Rate')
ax1.tick_params(axis='x', rotation=45)

# Population percentages
bars2 = ax2.bar(disparity_df['Race'], disparity_df['Population %'], color='#4ECDC4')
ax2.set_title('Population Distribution (%)', fontsize=14, fontweight='bold')
ax2.set_ylabel('Population %')
ax2.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('visualizations/14_disparity_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

print("\nAll visualizations have been created in the 'visualizations' folder!")
print("\nGenerated files:")
import glob
for file in sorted(glob.glob('visualizations/*')):
    print(f"  - {file}") 