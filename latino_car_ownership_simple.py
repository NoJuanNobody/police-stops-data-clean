#!/usr/bin/env python3
"""
Simple Latino Car Ownership Analysis using PUMS Data
This script analyzes car ownership patterns among Latino/Hispanic populations using 2018 ACS PUMS data.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

# Set style for better-looking plots
plt.style.use('default')
sns.set_palette("husl")

def load_and_prepare_data():
    """Load and prepare PUMS data for analysis."""
    print("Loading PUMS data...")
    
    # Load person-level data
    person_data = pd.read_csv('PUMS-2018-data/csv_pfl/psam_p12_updated_headers.csv')
    
    # Load housing-level data (for vehicle ownership)
    housing_data = pd.read_csv('PUMS-2018-data/csv_hfl/psam_h12_updated_headers.csv')
    
    print(f"Loaded {len(person_data):,} person records")
    print(f"Loaded {len(housing_data):,} housing records")
    
    # Check the merge columns
    print(f"\nPerson data SERIALNO sample: {person_data['SERIALNO_Housing_unitGQ_person_serial_number'].head()}")
    print(f"Housing data SERIALNO sample: {housing_data['SERIALNO_Housing_unitGQ_person_serial_number'].head()}")
    
    # Merge person and housing data on SERIALNO
    merged_data = person_data.merge(
        housing_data[['SERIALNO_Housing_unitGQ_person_serial_number', 
                     'VEH_Vehicles_1_ton_or_less_available']], 
        left_on='SERIALNO_Housing_unitGQ_person_serial_number',
        right_on='SERIALNO_Housing_unitGQ_person_serial_number',
        how='left'
    )
    
    print(f"After merge: {len(merged_data):,} records")
    print(f"Vehicle ownership unique values: {merged_data['VEH_Vehicles_1_ton_or_less_available'].unique()}")
    
    # Create Latino/Hispanic identifier
    # HISP variable: 1 = Not Hispanic, 2-24 = Hispanic origin
    merged_data['is_latino'] = merged_data['HISP_Recoded_detailed_Hispanic_origin'].isin([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24])
    
    # Create vehicle ownership categories - handle the actual numeric values
    vehicle_mapping = {
        0.0: 'No vehicles',
        1.0: '1 vehicle', 
        2.0: '2 vehicles',
        3.0: '3 vehicles',
        4.0: '4 vehicles',
        5.0: '5 vehicles',
        6.0: '6+ vehicles'
    }
    
    # Check what values we actually have
    print(f"Vehicle ownership raw values: {merged_data['VEH_Vehicles_1_ton_or_less_available'].value_counts().head()}")
    
    merged_data['vehicle_ownership'] = merged_data['VEH_Vehicles_1_ton_or_less_available'].map(vehicle_mapping)
    
    # Create age groups
    merged_data['age_group'] = pd.cut(
        merged_data['AGEP_Age'], 
        bins=[0, 18, 25, 35, 50, 65, 100],
        labels=['Under 18', '18-24', '25-34', '35-49', '50-64', '65+']
    )
    
    # Create income groups - handle missing values
    income_data = merged_data['PINCP_Total_persons_income_signed_use_ADJINC_to_adjust_to_constant_dollars']
    print(f"Income data sample: {income_data.head()}")
    print(f"Income data types: {income_data.dtype}")
    print(f"Income missing values: {income_data.isna().sum()}")
    
    # Convert to numeric, handling non-numeric values
    income_data_numeric = pd.to_numeric(income_data, errors='coerce')
    
    merged_data['income_group'] = pd.cut(
        income_data_numeric,
        bins=[0, 25000, 50000, 75000, 100000, 150000, float('inf')],
        labels=['Under $25K', '$25K-$50K', '$50K-$75K', '$75K-$100K', '$100K-$150K', '$150K+']
    )
    
    return merged_data

def create_basic_graphs(data):
    """Create basic graphs for Latino car ownership analysis."""
    
    # Filter for Latino population
    latino_data = data[data['is_latino'] == True].copy()
    non_latino_data = data[data['is_latino'] == False].copy()
    
    print(f"\nLatino population: {len(latino_data):,} records")
    print(f"Non-Latino population: {len(non_latino_data):,} records")
    
    # Remove records with missing vehicle ownership
    latino_data_clean = latino_data.dropna(subset=['vehicle_ownership'])
    non_latino_data_clean = non_latino_data.dropna(subset=['vehicle_ownership'])
    
    print(f"Latino population (with vehicle data): {len(latino_data_clean):,} records")
    print(f"Non-Latino population (with vehicle data): {len(non_latino_data_clean):,} records")
    
    # Create figure
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. Vehicle Ownership Distribution by Ethnicity
    ax1 = axes[0, 0]
    vehicle_ownership_latino = latino_data_clean['vehicle_ownership'].value_counts(normalize=True) * 100
    vehicle_ownership_non_latino = non_latino_data_clean['vehicle_ownership'].value_counts(normalize=True) * 100
    
    x = np.arange(len(vehicle_ownership_latino))
    width = 0.35
    
    ax1.bar(x - width/2, vehicle_ownership_latino.values, width, label='Latino', alpha=0.8, color='#ff7f0e')
    ax1.bar(x + width/2, vehicle_ownership_non_latino.values, width, label='Non-Latino', alpha=0.8, color='#1f77b4')
    
    ax1.set_xlabel('Number of Vehicles')
    ax1.set_ylabel('Percentage of Population')
    ax1.set_title('Vehicle Ownership by Ethnicity')
    ax1.set_xticks(x)
    ax1.set_xticklabels(vehicle_ownership_latino.index, rotation=45)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 2. No Vehicle Ownership Comparison
    ax2 = axes[0, 1]
    no_vehicle_latino = (latino_data_clean['vehicle_ownership'] == 'No vehicles').sum() / len(latino_data_clean) * 100
    no_vehicle_non_latino = (non_latino_data_clean['vehicle_ownership'] == 'No vehicles').sum() / len(non_latino_data_clean) * 100
    
    bars = ax2.bar(['Latino', 'Non-Latino'], [no_vehicle_latino, no_vehicle_non_latino], 
            color=['#ff7f0e', '#1f77b4'], alpha=0.8)
    ax2.set_ylabel('Percentage with No Vehicles')
    ax2.set_title('No Vehicle Ownership by Ethnicity')
    ax2.grid(True, alpha=0.3)
    
    # Add percentage labels on bars
    for bar, value in zip(bars, [no_vehicle_latino, no_vehicle_non_latino]):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{value:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    # 3. Multiple Vehicle Ownership (2+ vehicles)
    ax3 = axes[1, 0]
    multiple_vehicles_latino = latino_data_clean['vehicle_ownership'].isin(['2 vehicles', '3 vehicles', '4 vehicles', '5 vehicles', '6+ vehicles']).sum() / len(latino_data_clean) * 100
    multiple_vehicles_non_latino = non_latino_data_clean['vehicle_ownership'].isin(['2 vehicles', '3 vehicles', '4 vehicles', '5 vehicles', '6+ vehicles']).sum() / len(non_latino_data_clean) * 100
    
    bars = ax3.bar(['Latino', 'Non-Latino'], [multiple_vehicles_latino, multiple_vehicles_non_latino],
            color=['#ff7f0e', '#1f77b4'], alpha=0.8)
    ax3.set_ylabel('Percentage with 2+ Vehicles')
    ax3.set_title('Multiple Vehicle Ownership by Ethnicity')
    ax3.grid(True, alpha=0.3)
    
    # Add percentage labels on bars
    for bar, value in zip(bars, [multiple_vehicles_latino, multiple_vehicles_non_latino]):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{value:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    # 4. Vehicle Ownership by Age Group (Latino)
    ax4 = axes[1, 1]
    latino_age_vehicle = latino_data_clean.dropna(subset=['age_group', 'vehicle_ownership'])
    
    if len(latino_age_vehicle) > 0:
        age_vehicle_pivot = pd.crosstab(latino_age_vehicle['age_group'], 
                                       latino_age_vehicle['vehicle_ownership'], normalize='index') * 100
        
        if not age_vehicle_pivot.empty:
            age_vehicle_pivot.plot(kind='bar', stacked=True, ax=ax4)
            ax4.set_title('Vehicle Ownership by Age Group (Latino)')
            ax4.set_xlabel('Age Group')
            ax4.set_ylabel('Percentage')
            ax4.tick_params(axis='x', rotation=45)
            ax4.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        else:
            ax4.text(0.5, 0.5, 'No data available', ha='center', va='center', transform=ax4.transAxes)
            ax4.set_title('Vehicle Ownership by Age Group (Latino)')
    else:
        ax4.text(0.5, 0.5, 'No data available', ha='center', va='center', transform=ax4.transAxes)
        ax4.set_title('Vehicle Ownership by Age Group (Latino)')
    
    plt.tight_layout()
    plt.savefig('visualizations/latino_car_ownership_basic.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return latino_data_clean, non_latino_data_clean

def create_income_analysis(latino_data_clean):
    """Create income-based analysis for Latino car ownership."""
    
    # Filter for records with both income and vehicle data
    latino_income_vehicle = latino_data_clean.dropna(subset=['income_group', 'vehicle_ownership'])
    
    if len(latino_income_vehicle) == 0:
        print("No data available for income analysis")
        return
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # 1. Vehicle Ownership by Income Level
    ax1 = axes[0]
    income_vehicle_pivot = pd.crosstab(latino_income_vehicle['income_group'], 
                                      latino_income_vehicle['vehicle_ownership'], normalize='index') * 100
    
    if not income_vehicle_pivot.empty:
        income_vehicle_pivot.plot(kind='bar', stacked=True, ax=ax1)
        ax1.set_title('Vehicle Ownership by Income Level (Latino)')
        ax1.set_xlabel('Income Level')
        ax1.set_ylabel('Percentage')
        ax1.tick_params(axis='x', rotation=45)
        ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    else:
        ax1.text(0.5, 0.5, 'No data available', ha='center', va='center', transform=ax1.transAxes)
        ax1.set_title('Vehicle Ownership by Income Level (Latino)')
    
    # 2. No Vehicle Ownership by Income
    ax2 = axes[1]
    no_vehicle_by_income = latino_income_vehicle.groupby('income_group')['vehicle_ownership'].apply(
        lambda x: (x == 'No vehicles').sum() / len(x) * 100)
    
    if len(no_vehicle_by_income) > 0:
        no_vehicle_by_income.plot(kind='bar', ax=ax2, color='#ff7f0e')
        ax2.set_title('No Vehicle Ownership by Income (Latino)')
        ax2.set_xlabel('Income Level')
        ax2.set_ylabel('Percentage with No Vehicles')
        ax2.tick_params(axis='x', rotation=45)
        ax2.grid(True, alpha=0.3)
        
        # Add percentage labels
        for i, v in enumerate(no_vehicle_by_income.values):
            ax2.text(i, v + 0.5, f'{v:.1f}%', ha='center', va='bottom', fontweight='bold')
    else:
        ax2.text(0.5, 0.5, 'No data available', ha='center', va='center', transform=ax2.transAxes)
        ax2.set_title('No Vehicle Ownership by Income (Latino)')
    
    plt.tight_layout()
    plt.savefig('visualizations/latino_car_ownership_income.png', dpi=300, bbox_inches='tight')
    plt.show()

def print_summary_statistics(latino_data_clean, non_latino_data_clean):
    """Print comprehensive summary statistics."""
    
    print("\n" + "="*80)
    print("LATINO CAR OWNERSHIP ANALYSIS SUMMARY")
    print("="*80)
    
    # Basic statistics
    print(f"\n📊 POPULATION BREAKDOWN:")
    print(f"   Total Latino population (with vehicle data): {len(latino_data_clean):,}")
    print(f"   Total Non-Latino population (with vehicle data): {len(non_latino_data_clean):,}")
    
    # Vehicle ownership statistics
    print(f"\n🚗 VEHICLE OWNERSHIP STATISTICS:")
    
    latino_vehicle_stats = latino_data_clean['vehicle_ownership'].value_counts(normalize=True) * 100
    non_latino_vehicle_stats = non_latino_data_clean['vehicle_ownership'].value_counts(normalize=True) * 100
    
    print(f"\n   Latino Vehicle Ownership:")
    for ownership, percentage in latino_vehicle_stats.items():
        count = (latino_data_clean['vehicle_ownership'] == ownership).sum()
        print(f"     {ownership}: {count:,} ({percentage:.1f}%)")
    
    print(f"\n   Non-Latino Vehicle Ownership:")
    for ownership, percentage in non_latino_vehicle_stats.items():
        count = (non_latino_data_clean['vehicle_ownership'] == ownership).sum()
        print(f"     {ownership}: {count:,} ({percentage:.1f}%)")
    
    # Key comparisons
    print(f"\n🔍 KEY COMPARISONS:")
    no_vehicle_latino = (latino_data_clean['vehicle_ownership'] == 'No vehicles').sum() / len(latino_data_clean) * 100
    no_vehicle_non_latino = (non_latino_data_clean['vehicle_ownership'] == 'No vehicles').sum() / len(non_latino_data_clean) * 100
    
    print(f"   No vehicle ownership:")
    print(f"     Latino: {no_vehicle_latino:.1f}%")
    print(f"     Non-Latino: {no_vehicle_non_latino:.1f}%")
    print(f"     Difference: {no_vehicle_latino - no_vehicle_non_latino:.1f} percentage points")
    
    multiple_vehicles_latino = latino_data_clean['vehicle_ownership'].isin(['2 vehicles', '3 vehicles', '4 vehicles', '5 vehicles', '6+ vehicles']).sum() / len(latino_data_clean) * 100
    multiple_vehicles_non_latino = non_latino_data_clean['vehicle_ownership'].isin(['2 vehicles', '3 vehicles', '4 vehicles', '5 vehicles', '6+ vehicles']).sum() / len(non_latino_data_clean) * 100
    
    print(f"\n   Multiple vehicle ownership (2+ vehicles):")
    print(f"     Latino: {multiple_vehicles_latino:.1f}%")
    print(f"     Non-Latino: {multiple_vehicles_non_latino:.1f}%")
    print(f"     Difference: {multiple_vehicles_latino - multiple_vehicles_non_latino:.1f} percentage points")

def main():
    """Main function to run the Latino car ownership analysis."""
    
    # Create visualizations directory if it doesn't exist
    Path('visualizations').mkdir(exist_ok=True)
    
    # Load and prepare data
    merged_data = load_and_prepare_data()
    
    # Create basic graphs
    latino_data_clean, non_latino_data_clean = create_basic_graphs(merged_data)
    
    # Create income analysis
    create_income_analysis(latino_data_clean)
    
    # Print summary statistics
    print_summary_statistics(latino_data_clean, non_latino_data_clean)
    
    print(f"\n✅ Analysis complete! Graphs saved to 'visualizations/' directory.")

if __name__ == "__main__":
    main() 