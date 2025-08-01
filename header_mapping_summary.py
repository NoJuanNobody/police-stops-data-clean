#!/usr/bin/env python3
"""
Script to show the mapping between original and updated PUMS CSV headers.
"""

import csv
from pathlib import Path

def show_header_mapping(original_file, updated_file, max_columns=20):
    """
    Show the mapping between original and updated headers.
    
    Args:
        original_file (str): Path to original CSV file
        updated_file (str): Path to updated CSV file
        max_columns (int): Maximum number of columns to show
    """
    # Read original headers
    with open(original_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        original_headers = next(reader)
    
    # Read updated headers
    with open(updated_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        updated_headers = next(reader)
    
    print(f"\nHeader mapping for {Path(original_file).name}:")
    print("=" * 80)
    print(f"{'Original':<30} {'Updated':<50}")
    print("-" * 80)
    
    for i, (orig, updated) in enumerate(zip(original_headers, updated_headers)):
        if i >= max_columns:
            print(f"... and {len(original_headers) - max_columns} more columns")
            break
        
        # Truncate long headers for display
        orig_display = orig[:28] + ".." if len(orig) > 30 else orig
        updated_display = updated[:48] + ".." if len(updated) > 50 else updated
        
        print(f"{orig_display:<30} {updated_display:<50}")

def main():
    """Main function to show header mappings."""
    # File paths
    housing_original = "PUMS-2018-data/csv_hfl/psam_h12.csv"
    housing_updated = "PUMS-2018-data/csv_hfl/psam_h12_updated_headers.csv"
    person_original = "PUMS-2018-data/csv_pfl/psam_p12.csv"
    person_updated = "PUMS-2018-data/csv_pfl/psam_p12_updated_headers.csv"
    
    # Check if files exist
    files_to_check = [housing_original, housing_updated, person_original, person_updated]
    for file_path in files_to_check:
        if not Path(file_path).exists():
            print(f"Error: File not found: {file_path}")
            return
    
    # Show housing file mapping
    show_header_mapping(housing_original, housing_updated, max_columns=15)
    
    # Show person file mapping
    show_header_mapping(person_original, person_updated, max_columns=15)
    
    print("\n" + "=" * 80)
    print("Summary:")
    print(f"- Housing file: {len(open(housing_original).readline().split(','))} columns")
    print(f"- Person file: {len(open(person_original).readline().split(','))} columns")
    print("- All headers have been updated with descriptive names from the PUMS data dictionary")

if __name__ == "__main__":
    main() 