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

print("\nAll visualizations have been created in the 'visualizations' folder!")
print("\nGenerated files:")
import glob
for file in sorted(glob.glob('visualizations/*')):
    print(f"  - {file}") 