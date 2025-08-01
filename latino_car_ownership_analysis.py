#!/usr/bin/env python3
"""
Latino Car Ownership Analysis using PUMS Data
This script analyzes car ownership patterns among Latino/Hispanic populations using 2018 ACS PUMS data.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

# Set style for better-looking plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def load_pums_data():
    """Load and prepare PUMS data for analysis."""
    print("Loading PUMS data...")
    
    # Load person-level data
    person_data = pd.read_csv('PUMS-2018-data/csv_pfl/psam_p12_updated_headers.csv')
    
    # Load housing-level data (for vehicle ownership)
    housing_data = pd.read_csv('PUMS-2018-data/csv_hfl/psam_h12_updated_headers.csv')
    
    print(f"Loaded {len(person_data):,} person records")
    print(f"Loaded {len(housing_data):,} housing records")
    
    return person_data, housing_data

def prepare_latino_data(person_data, housing_data):
    """Prepare data focusing on Latino/Hispanic population and car ownership."""
    
    # Merge person and housing data on SERIALNO
    merged_data = person_data.merge(
        housing_data[['SERIALNO_Housing_unitGQ_person_serial_number', 
                     'VEH_Vehicles_1_ton_or_less_available']], 
        left_on='SERIALNO_Housing_unitGQ_person_serial_number',
        right_on='SERIALNO_Housing_unitGQ_person_serial_number',
        how='left'
    )
    
    # Create Latino/Hispanic identifier
    # HISP variable: 1 = Not Hispanic, 2-24 = Hispanic origin
    merged_data['is_latino'] = merged_data['HISP_Recoded_detailed_Hispanic_origin'].isin([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24])
    
    # Create vehicle ownership categories
    merged_data['vehicle_ownership'] = merged_data['VEH_Vehicles_1_ton_or_less_available'].map({
        '0': 'No vehicles',
        '1': '1 vehicle', 
        '2': '2 vehicles',
        '3': '3 vehicles',
        '4': '4 vehicles',
        '5': '5 vehicles',
        '6': '6+ vehicles'
    })
    
    # Create age groups
    merged_data['age_group'] = pd.cut(
        merged_data['AGEP_Age'], 
        bins=[0, 18, 25, 35, 50, 65, 100],
        labels=['Under 18', '18-24', '25-34', '35-49', '50-64', '65+']
    )
    
    # Create income groups
    merged_data['income_group'] = pd.cut(
        merged_data['PINCP_Total_persons_income_signed_use_ADJINC_to_adjust_to_constant_dollars'],
        bins=[0, 25000, 50000, 75000, 100000, 150000, float('inf')],
        labels=['Under $25K', '$25K-$50K', '$50K-$75K', '$75K-$100K', '$100K-$150K', '$150K+']
    )
    
    return merged_data

def create_latino_car_ownership_graphs(data):
    """Create comprehensive graphs for Latino car ownership analysis."""
    
    # Filter for Latino population
    latino_data = data[data['is_latino'] == True].copy()
    non_latino_data = data[data['is_latino'] == False].copy()
    
    print(f"Latino population: {len(latino_data):,} records")
    print(f"Non-Latino population: {len(non_latino_data):,} records")
    
    # Debug: Check data types and missing values
    print(f"\nDebug info:")
    print(f"Vehicle ownership unique values: {latino_data['vehicle_ownership'].unique()}")
    print(f"Age group unique values: {latino_data['age_group'].unique()}")
    print(f"Income group unique values: {latino_data['income_group'].unique()}")
    print(f"Missing vehicle ownership: {latino_data['vehicle_ownership'].isna().sum()}")
    print(f"Missing age group: {latino_data['age_group'].isna().sum()}")
    print(f"Missing income group: {latino_data['income_group'].isna().sum()}")
    
    # Create figure with subplots
    fig = plt.figure(figsize=(20, 16))
    
    # 1. Vehicle Ownership Distribution by Ethnicity
    plt.subplot(3, 3, 1)
    vehicle_ownership_latino = latino_data['vehicle_ownership'].value_counts(normalize=True) * 100
    vehicle_ownership_non_latino = non_latino_data['vehicle_ownership'].value_counts(normalize=True) * 100
    
    x = np.arange(len(vehicle_ownership_latino))
    width = 0.35
    
    plt.bar(x - width/2, vehicle_ownership_latino.values, width, label='Latino', alpha=0.8)
    plt.bar(x + width/2, vehicle_ownership_non_latino.values, width, label='Non-Latino', alpha=0.8)
    
    plt.xlabel('Number of Vehicles')
    plt.ylabel('Percentage of Population')
    plt.title('Vehicle Ownership by Ethnicity')
    plt.xticks(x, vehicle_ownership_latino.index, rotation=45)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # 2. Vehicle Ownership by Age Group (Latino)
    plt.subplot(3, 3, 2)
    age_vehicle_latino = pd.crosstab(latino_data['age_group'], latino_data['vehicle_ownership'], normalize='index') * 100
    if not age_vehicle_latino.empty:
        age_vehicle_latino.plot(kind='bar', stacked=True, ax=plt.gca())
        plt.title('Vehicle Ownership by Age Group (Latino)')
        plt.xlabel('Age Group')
        plt.ylabel('Percentage')
        plt.xticks(rotation=45)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    else:
        plt.text(0.5, 0.5, 'No data available', ha='center', va='center', transform=plt.gca().transAxes)
        plt.title('Vehicle Ownership by Age Group (Latino)')
    plt.tight_layout()
    
    # 3. Vehicle Ownership by Income (Latino)
    plt.subplot(3, 3, 3)
    income_vehicle_latino = pd.crosstab(latino_data['income_group'], latino_data['vehicle_ownership'], normalize='index') * 100
    if not income_vehicle_latino.empty:
        income_vehicle_latino.plot(kind='bar', stacked=True, ax=plt.gca())
        plt.title('Vehicle Ownership by Income (Latino)')
        plt.xlabel('Income Group')
        plt.ylabel('Percentage')
        plt.xticks(rotation=45)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    else:
        plt.text(0.5, 0.5, 'No data available', ha='center', va='center', transform=plt.gca().transAxes)
        plt.title('Vehicle Ownership by Income (Latino)')
    plt.tight_layout()
    
    # 4. No Vehicle Ownership Comparison
    plt.subplot(3, 3, 4)
    no_vehicle_latino = (latino_data['vehicle_ownership'] == 'No vehicles').sum() / len(latino_data) * 100
    no_vehicle_non_latino = (non_latino_data['vehicle_ownership'] == 'No vehicles').sum() / len(non_latino_data) * 100
    
    plt.bar(['Latino', 'Non-Latino'], [no_vehicle_latino, no_vehicle_non_latino], 
            color=['#ff7f0e', '#1f77b4'], alpha=0.8)
    plt.ylabel('Percentage with No Vehicles')
    plt.title('No Vehicle Ownership by Ethnicity')
    plt.grid(True, alpha=0.3)
    
    # Add percentage labels on bars
    for i, v in enumerate([no_vehicle_latino, no_vehicle_non_latino]):
        plt.text(i, v + 0.5, f'{v:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    # 5. Multiple Vehicle Ownership (2+ vehicles)
    plt.subplot(3, 3, 5)
    multiple_vehicles_latino = latino_data['vehicle_ownership'].isin(['2 vehicles', '3 vehicles', '4 vehicles', '5 vehicles', '6+ vehicles']).sum() / len(latino_data) * 100
    multiple_vehicles_non_latino = non_latino_data['vehicle_ownership'].isin(['2 vehicles', '3 vehicles', '4 vehicles', '5 vehicles', '6+ vehicles']).sum() / len(non_latino_data) * 100
    
    plt.bar(['Latino', 'Non-Latino'], [multiple_vehicles_latino, multiple_vehicles_non_latino],
            color=['#ff7f0e', '#1f77b4'], alpha=0.8)
    plt.ylabel('Percentage with 2+ Vehicles')
    plt.title('Multiple Vehicle Ownership by Ethnicity')
    plt.grid(True, alpha=0.3)
    
    # Add percentage labels on bars
    for i, v in enumerate([multiple_vehicles_latino, multiple_vehicles_non_latino]):
        plt.text(i, v + 0.5, f'{v:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    # 6. Vehicle Ownership by Geographic Region (Latino)
    plt.subplot(3, 3, 6)
    region_vehicle_latino = pd.crosstab(latino_data['REGION_Region_code_based_on_2010_Census_definitions'], 
                                       latino_data['vehicle_ownership'], normalize='index') * 100
    region_vehicle_latino.plot(kind='bar', stacked=True, ax=plt.gca())
    plt.title('Vehicle Ownership by Region (Latino)')
    plt.xlabel('Region')
    plt.ylabel('Percentage')
    plt.xticks(rotation=45)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    
    # 7. Vehicle Ownership by Education Level (Latino)
    plt.subplot(3, 3, 7)
    # Create education groups
    latino_data['education_group'] = pd.cut(
        latino_data['SCHL_Educational_attainment'],
        bins=[0, 15, 16, 20, 21, 24],
        labels=['Less than HS', 'High School', 'Some College', 'Bachelor\'s', 'Graduate']
    )
    
    education_vehicle_latino = pd.crosstab(latino_data['education_group'], 
                                          latino_data['vehicle_ownership'], normalize='index') * 100
    education_vehicle_latino.plot(kind='bar', stacked=True, ax=plt.gca())
    plt.title('Vehicle Ownership by Education (Latino)')
    plt.xlabel('Education Level')
    plt.ylabel('Percentage')
    plt.xticks(rotation=45)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    
    # 8. Vehicle Ownership by Family Type (Latino)
    plt.subplot(3, 3, 8)
    # Create family type groups
    latino_data['family_type'] = latino_data['RELP_Relationship'].map({
        0: 'Reference person',
        1: 'Spouse',
        2: 'Child',
        3: 'Child',
        4: 'Child',
        5: 'Sibling',
        6: 'Parent',
        7: 'Grandchild',
        8: 'Parent-in-law',
        9: 'Son/daughter-in-law',
        10: 'Other relative',
        11: 'Roomer/boarder',
        12: 'Housemate',
        13: 'Unmarried partner',
        14: 'Foster child',
        15: 'Other nonrelative',
        16: 'Institutionalized',
        17: 'Noninstitutionalized'
    })
    
    family_vehicle_latino = pd.crosstab(latino_data['family_type'], 
                                       latino_data['vehicle_ownership'], normalize='index') * 100
    family_vehicle_latino.plot(kind='bar', stacked=True, ax=plt.gca())
    plt.title('Vehicle Ownership by Family Type (Latino)')
    plt.xlabel('Family Type')
    plt.ylabel('Percentage')
    plt.xticks(rotation=45)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    
    # 9. Summary Statistics
    plt.subplot(3, 3, 9)
    # Create summary table
    summary_stats = {
        'Metric': ['No Vehicles', '1 Vehicle', '2+ Vehicles', 'Total Latino Population'],
        'Latino Count': [
            (latino_data['vehicle_ownership'] == 'No vehicles').sum(),
            (latino_data['vehicle_ownership'] == '1 vehicle').sum(),
            latino_data['vehicle_ownership'].isin(['2 vehicles', '3 vehicles', '4 vehicles', '5 vehicles', '6+ vehicles']).sum(),
            len(latino_data)
        ],
        'Latino %': [
            (latino_data['vehicle_ownership'] == 'No vehicles').sum() / len(latino_data) * 100,
            (latino_data['vehicle_ownership'] == '1 vehicle').sum() / len(latino_data) * 100,
            latino_data['vehicle_ownership'].isin(['2 vehicles', '3 vehicles', '4 vehicles', '5 vehicles', '6+ vehicles']).sum() / len(latino_data) * 100,
            100
        ]
    }
    
    summary_df = pd.DataFrame(summary_stats)
    
    # Create table plot
    table = plt.table(cellText=summary_df.values, colLabels=summary_df.columns, 
                     cellLoc='center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 2)
    plt.title('Latino Vehicle Ownership Summary')
    plt.axis('off')
    
    plt.tight_layout()
    plt.savefig('visualizations/latino_car_ownership_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return latino_data, non_latino_data

def create_additional_graphs(latino_data, non_latino_data):
    """Create additional focused graphs for Latino car ownership."""
    
    # Create a new figure for additional analysis
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. Vehicle Ownership Trends by Age (Comparison)
    ax1 = axes[0, 0]
    age_vehicle_comparison = pd.DataFrame({
        'Latino': latino_data.groupby('age_group')['vehicle_ownership'].apply(
            lambda x: (x == 'No vehicles').sum() / len(x) * 100),
        'Non-Latino': non_latino_data.groupby('age_group')['vehicle_ownership'].apply(
            lambda x: (x == 'No vehicles').sum() / len(x) * 100)
    })
    
    age_vehicle_comparison.plot(kind='bar', ax=ax1, color=['#ff7f0e', '#1f77b4'])
    ax1.set_title('No Vehicle Ownership by Age Group')
    ax1.set_xlabel('Age Group')
    ax1.set_ylabel('Percentage with No Vehicles')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
    
    # 2. Income vs Vehicle Ownership (Latino)
    ax2 = axes[0, 1]
    income_vehicle_pivot = pd.crosstab(latino_data['income_group'], 
                                      latino_data['vehicle_ownership'], normalize='index') * 100
    
    income_vehicle_pivot.plot(kind='bar', stacked=True, ax=ax2)
    ax2.set_title('Vehicle Ownership by Income Level (Latino)')
    ax2.set_xlabel('Income Level')
    ax2.set_ylabel('Percentage')
    ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
    
    # 3. Geographic Distribution of Latino Vehicle Ownership
    ax3 = axes[1, 0]
    region_stats = latino_data.groupby('REGION_Region_code_based_on_2010_Census_definitions').agg({
        'vehicle_ownership': lambda x: (x == 'No vehicles').sum() / len(x) * 100
    }).rename(columns={'vehicle_ownership': 'No_Vehicles_Percentage'})
    
    region_names = {1: 'Northeast', 2: 'Midwest', 3: 'South', 4: 'West', 9: 'Puerto Rico'}
    region_stats.index = region_stats.index.map(region_names)
    
    region_stats.plot(kind='bar', ax=ax3, color='#ff7f0e')
    ax3.set_title('Latino No Vehicle Ownership by Region')
    ax3.set_xlabel('Region')
    ax3.set_ylabel('Percentage with No Vehicles')
    ax3.grid(True, alpha=0.3)
    plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45)
    
    # 4. Vehicle Ownership by Employment Status (Latino)
    ax4 = axes[1, 1]
    # Create employment status
    latino_data['employment_status'] = latino_data['ESR_Employment_status_recode'].map({
        1: 'Employed',
        2: 'Employed (not at work)',
        3: 'Unemployed',
        4: 'Armed Forces',
        5: 'Armed Forces (not at work)',
        6: 'Not in labor force'
    })
    
    employment_vehicle = pd.crosstab(latino_data['employment_status'], 
                                   latino_data['vehicle_ownership'], normalize='index') * 100
    
    employment_vehicle.plot(kind='bar', stacked=True, ax=ax4)
    ax4.set_title('Vehicle Ownership by Employment Status (Latino)')
    ax4.set_xlabel('Employment Status')
    ax4.set_ylabel('Percentage')
    ax4.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.setp(ax4.xaxis.get_majorticklabels(), rotation=45)
    
    plt.tight_layout()
    plt.savefig('visualizations/latino_car_ownership_additional.png', dpi=300, bbox_inches='tight')
    plt.show()

def print_summary_statistics(latino_data, non_latino_data):
    """Print comprehensive summary statistics."""
    
    print("\n" + "="*80)
    print("LATINO CAR OWNERSHIP ANALYSIS SUMMARY")
    print("="*80)
    
    # Basic statistics
    print(f"\n📊 POPULATION BREAKDOWN:")
    print(f"   Total Latino population: {len(latino_data):,}")
    print(f"   Total Non-Latino population: {len(non_latino_data):,}")
    
    # Vehicle ownership statistics
    print(f"\n🚗 VEHICLE OWNERSHIP STATISTICS:")
    
    latino_vehicle_stats = latino_data['vehicle_ownership'].value_counts(normalize=True) * 100
    non_latino_vehicle_stats = non_latino_data['vehicle_ownership'].value_counts(normalize=True) * 100
    
    print(f"\n   Latino Vehicle Ownership:")
    for ownership, percentage in latino_vehicle_stats.items():
        count = (latino_data['vehicle_ownership'] == ownership).sum()
        print(f"     {ownership}: {count:,} ({percentage:.1f}%)")
    
    print(f"\n   Non-Latino Vehicle Ownership:")
    for ownership, percentage in non_latino_vehicle_stats.items():
        count = (non_latino_data['vehicle_ownership'] == ownership).sum()
        print(f"     {ownership}: {count:,} ({percentage:.1f}%)")
    
    # Key comparisons
    print(f"\n🔍 KEY COMPARISONS:")
    no_vehicle_latino = (latino_data['vehicle_ownership'] == 'No vehicles').sum() / len(latino_data) * 100
    no_vehicle_non_latino = (non_latino_data['vehicle_ownership'] == 'No vehicles').sum() / len(non_latino_data) * 100
    
    print(f"   No vehicle ownership:")
    print(f"     Latino: {no_vehicle_latino:.1f}%")
    print(f"     Non-Latino: {no_vehicle_non_latino:.1f}%")
    print(f"     Difference: {no_vehicle_latino - no_vehicle_non_latino:.1f} percentage points")
    
    multiple_vehicles_latino = latino_data['vehicle_ownership'].isin(['2 vehicles', '3 vehicles', '4 vehicles', '5 vehicles', '6+ vehicles']).sum() / len(latino_data) * 100
    multiple_vehicles_non_latino = non_latino_data['vehicle_ownership'].isin(['2 vehicles', '3 vehicles', '4 vehicles', '5 vehicles', '6+ vehicles']).sum() / len(non_latino_data) * 100
    
    print(f"\n   Multiple vehicle ownership (2+ vehicles):")
    print(f"     Latino: {multiple_vehicles_latino:.1f}%")
    print(f"     Non-Latino: {multiple_vehicles_non_latino:.1f}%")
    print(f"     Difference: {multiple_vehicles_latino - multiple_vehicles_non_latino:.1f} percentage points")

def main():
    """Main function to run the Latino car ownership analysis."""
    
    # Create visualizations directory if it doesn't exist
    Path('visualizations').mkdir(exist_ok=True)
    
    # Load and prepare data
    person_data, housing_data = load_pums_data()
    merged_data = prepare_latino_data(person_data, housing_data)
    
    # Create graphs
    latino_data, non_latino_data = create_latino_car_ownership_graphs(merged_data)
    create_additional_graphs(latino_data, non_latino_data)
    
    # Print summary statistics
    print_summary_statistics(latino_data, non_latino_data)
    
    print(f"\n✅ Analysis complete! Graphs saved to 'visualizations/' directory.")

if __name__ == "__main__":
    main() 