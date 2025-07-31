import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load the data
print("Loading data for violation analysis...")
df = pd.read_csv('fl_tampa_2020_04_01.csv')

# Create output directory
import os
os.makedirs('visualizations', exist_ok=True)

# Function to categorize violations
def categorize_violation(violation_text):
    """Categorize violations into meaningful groups based on the violation description"""
    if pd.isna(violation_text):
        return "Unknown"
    
    violation_lower = violation_text.lower()
    
    # Seat belt violations
    if any(term in violation_lower for term in ['belted', 'belt', 'seat belt']):
        return "Seat Belt Violations"
    
    # Red light violations
    if any(term in violation_lower for term in ['red light', 'red lt', 'fail to stop']):
        return "Red Light Violations"
    
    # Speed violations
    if any(term in violation_lower for term in ['speed', 'speeding']):
        return "Speed Violations"
    
    # License violations
    if any(term in violation_lower for term in ['dl', 'license', 'driving license']):
        return "License Violations"
    
    # Registration violations
    if any(term in violation_lower for term in ['reg', 'registration', 'motor vehicle reg']):
        return "Registration Violations"
    
    # Insurance violations
    if any(term in violation_lower for term in ['insurance', 'insured', 'proof of ins']):
        return "Insurance Violations"
    
    # Equipment violations
    if any(term in violation_lower for term in ['equipment', 'light', 'signal']):
        return "Equipment Violations"
    
    # Traffic control violations
    if any(term in violation_lower for term in ['yield', 'stop sign', 'traffic control']):
        return "Traffic Control Violations"
    
    # DUI/DWI violations
    if any(term in violation_lower for term in ['dui', 'dwi', 'alcohol', 'intoxicated']):
        return "DUI/DWI Violations"
    
    # Reckless driving
    if any(term in violation_lower for term in ['reckless', 'careless']):
        return "Reckless Driving"
    
    # Other traffic violations
    if any(term in violation_lower for term in ['traffic', 'highway', 'road']):
        return "Other Traffic Violations"
    
    return "Other Violations"

# Apply categorization
print("Categorizing violations...")
df['violation_category'] = df['violation'].apply(categorize_violation)

# Get category counts
category_counts = df['violation_category'].value_counts()

print("\n" + "="*60)
print("VIOLATION CATEGORY ANALYSIS")
print("="*60)

for category, count in category_counts.items():
    percentage = (count / len(df)) * 100
    print(f"{category}: {count:,} stops ({percentage:.1f}%)")

# Create visualization for violation categories
fig, ax = plt.subplots(figsize=(14, 8))
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#FFB6C1', '#98D8C8', '#F7DC6F', '#BB8FCE']
bars = ax.barh(range(len(category_counts)), category_counts.values, color=colors[:len(category_counts)])
ax.set_yticks(range(len(category_counts)))
ax.set_yticklabels(category_counts.index)
ax.set_title('Police Stops by Violation Category', fontsize=16, fontweight='bold')
ax.set_xlabel('Number of Stops')

# Add value labels
for i, bar in enumerate(bars):
    width = bar.get_width()
    ax.text(width + width*0.01, bar.get_y() + bar.get_height()/2,
            f'{int(width):,}', ha='left', va='center', fontweight='bold')

plt.tight_layout()
plt.savefig('visualizations/15_violation_categories.png', dpi=300, bbox_inches='tight')
plt.close()

# Analyze top specific violations
print("\n" + "="*60)
print("TOP 10 SPECIFIC VIOLATIONS")
print("="*60)

# Get the most common specific violations
top_violations = df['violation'].value_counts().head(10)

for i, (violation, count) in enumerate(top_violations.items(), 1):
    percentage = (count / len(df)) * 100
    print(f"{i}. {violation}")
    print(f"   Count: {count:,} ({percentage:.1f}%)")
    print()

# Create a more detailed analysis of the top violation codes
print("="*60)
print("DETAILED VIOLATION CODE ANALYSIS")
print("="*60)

# Extract the main violation codes (first 3-6 digits)
df['violation_code_main'] = df['violation'].str.extract(r'(\d{3,6})')[0]

# Get the most common violation codes with their descriptions
code_analysis = df.groupby('violation_code_main').agg({
    'violation': ['count', 'first']
}).round(2)

code_analysis.columns = ['count', 'description']
code_analysis = code_analysis.sort_values('count', ascending=False).head(15)

for code, row in code_analysis.head(10).iterrows():
    percentage = (row['count'] / len(df)) * 100
    print(f"Code {code}: {row['count']:,.0f} stops ({percentage:.1f}%)")
    print(f"  Description: {row['description']}")
    print()

# Create a pie chart for the top violation categories
fig, ax = plt.subplots(figsize=(12, 8))
top_categories = category_counts.head(8)  # Show top 8 categories
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#FFB6C1', '#98D8C8']
wedges, texts, autotexts = ax.pie(top_categories.values, labels=top_categories.index, autopct='%1.1f%%', 
                                  colors=colors, startangle=90)
ax.set_title('Distribution of Violation Categories', fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('visualizations/16_violation_categories_pie.png', dpi=300, bbox_inches='tight')
plt.close()

# Create a violation category by race analysis
print("\n" + "="*60)
print("VIOLATION CATEGORIES BY RACE")
print("="*60)

race_violation_cross = pd.crosstab(df['subject_race'], df['violation_category'])
top_races = race_violation_cross.sum(axis=1).nlargest(5).index
race_violation_filtered = race_violation_cross.loc[top_races]

fig, ax = plt.subplots(figsize=(14, 8))
race_violation_filtered.plot(kind='bar', stacked=True, ax=ax, colormap='Set3')
ax.set_title('Violation Categories by Race', fontsize=16, fontweight='bold')
ax.set_xlabel('Subject Race')
ax.set_ylabel('Number of Stops')
ax.legend(title='Violation Category', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('visualizations/17_violation_categories_by_race.png', dpi=300, bbox_inches='tight')
plt.close()

# Summary statistics
print("\n" + "="*60)
print("SUMMARY STATISTICS")
print("="*60)
print(f"Total violations analyzed: {len(df):,}")
print(f"Unique violation descriptions: {df['violation'].nunique():,}")
print(f"Violation categories created: {df['violation_category'].nunique()}")
print(f"Most common category: {category_counts.index[0]} ({category_counts.iloc[0]:,} stops)")
print(f"Least common category: {category_counts.index[-1]} ({category_counts.iloc[-1]:,} stops)")

print("\nKey Insights:")
print("• Traffic violations dominate the dataset")
print("• License and registration violations are very common")
print("• Seat belt and red light violations show automated enforcement")
print("• Different racial groups may be stopped for different violation types")
print("• The data shows a mix of automated and officer-initiated stops")

print("\nFiles created:")
print("• visualizations/15_violation_categories.png")
print("• visualizations/16_violation_categories_pie.png") 
print("• visualizations/17_violation_categories_by_race.png") 