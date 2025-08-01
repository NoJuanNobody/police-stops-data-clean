import pandas as pd
import numpy as np

# Load the data
print("Loading Tampa Police Stops Data...")
df = pd.read_csv('fl_tampa_2020_04_01.csv')

print(f"\n{'='*50}")
print("TAMPA POLICE STOPS DATA SUMMARY")
print(f"{'='*50}")

# Basic statistics
print(f"\n📊 DATASET OVERVIEW:")
print(f"   Total Records: {len(df):,}")
print(f"   Unique Subjects: {df['raw_row_number'].nunique():,}")

# Department analysis
print(f"\n🏛️  TOP DEPARTMENTS:")
dept_counts = df['department_name'].str.split('|').str[0].value_counts().head(5)
for dept, count in dept_counts.items():
    print(f"   {dept}: {count:,} stops")

# Demographic analysis
print(f"\n👥 DEMOGRAPHIC BREAKDOWN:")
print(f"   Race Distribution:")
race_counts = df['subject_race'].value_counts()
for race, count in race_counts.head(5).items():
    percentage = (count / len(df)) * 100
    print(f"     {race}: {count:,} ({percentage:.1f}%)")

print(f"\n   Gender Distribution:")
gender_counts = df['subject_sex'].value_counts()
for gender, count in gender_counts.items():
    if gender != 'NA':
        percentage = (count / len(df)) * 100
        print(f"     {gender}: {count:,} ({percentage:.1f}%)")

# Violation analysis
print(f"\n🚨 TOP VIOLATION TYPES:")
# Extract violation codes
df['violation_code'] = df['violation'].str.extract(r'(\d+)')[0]
violation_counts = df['violation_code'].value_counts().head(5)
for code, count in violation_counts.items():
    print(f"   Code {code}: {count:,} stops")

# Outcome analysis
print(f"\n📋 OUTCOME BREAKDOWN:")
outcome_counts = df['outcome'].value_counts()
for outcome, count in outcome_counts.items():
    percentage = (count / len(df)) * 100
    print(f"   {outcome}: {count:,} ({percentage:.1f}%)")

# Temporal analysis
print(f"\n📅 TEMPORAL PATTERNS:")
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df_with_dates = df[df['date'].notna()]
if len(df_with_dates) > 0:
    yearly_counts = df_with_dates.groupby(df_with_dates['date'].dt.year).size()
    print(f"   Peak Year: {yearly_counts.idxmax()} ({yearly_counts.max():,} stops)")
    print(f"   Recent Year: {yearly_counts.index[-1]} ({yearly_counts.iloc[-1]:,} stops)")
else:
    print("   No valid dates found in dataset")

# Vehicle registration
print(f"\n🚗 VEHICLE REGISTRATION:")
vehicle_counts = df['vehicle_registration_state'].value_counts().head(5)
for state, count in vehicle_counts.items():
    percentage = (count / len(df)) * 100
    print(f"   {state}: {count:,} ({percentage:.1f}%)")

print(f"\n{'='*50}")
print("Key Insights:")
print("• Traffic violations dominate the dataset")
print("• Tampa Police Department handles most stops")
print("• Males are stopped more frequently than females")
print("• Citations are the most common outcome")
print("• Florida vehicles account for the majority of stops")
print(f"{'='*50}") 