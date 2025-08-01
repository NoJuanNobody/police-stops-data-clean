#!/usr/bin/env python3
"""
Improved script to update PUMS CSV headers using the data dictionary.
This script correctly parses the PUMS data dictionary format and updates CSV headers.
"""

import csv
import re
import sys
from pathlib import Path

def parse_data_dictionary(dict_file):
    """
    Parse the PUMS data dictionary to extract variable names and descriptions.
    
    Args:
        dict_file (str): Path to the data dictionary file
        
    Returns:
        dict: Mapping of variable names to their descriptions
    """
    var_descriptions = {}
    
    with open(dict_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split content into lines
    lines = content.split('\n')
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Look for variable definitions (format: VARNAME followed by data type)
        # Pattern: VARNAME followed by whitespace, then data type and length
        match = re.match(r'^([A-Z][A-Z0-9]+)\s+(\w+)\s+(\d+)$', line)
        
        if match:
            var_name = match.group(1)
            data_type = match.group(2)
            length = match.group(3)
            
            # Look for the description on the next line
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if next_line and not next_line.startswith('.'):
                    # This is the description
                    description = next_line
                    var_descriptions[var_name] = description
                    
                    # Skip the value codes that follow (lines starting with spaces and containing dots)
                    i += 2
                    while i < len(lines) and lines[i].strip().startswith(' ') and '.' in lines[i]:
                        i += 1
                    continue
        
        i += 1
    
    return var_descriptions

def update_csv_headers(csv_file, var_descriptions, output_file=None):
    """
    Update CSV headers with full descriptions from the data dictionary.
    
    Args:
        csv_file (str): Path to the CSV file
        var_descriptions (dict): Mapping of variable names to descriptions
        output_file (str): Output file path (if None, overwrites original)
    """
    if output_file is None:
        output_file = csv_file
    
    # Read the CSV file
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)
    
    if not rows:
        print(f"Error: {csv_file} is empty")
        return
    
    # Get the header row
    header = rows[0]
    new_header = []
    
    # Update each column name
    for col in header:
        if col in var_descriptions:
            # Use the description from the dictionary
            # Clean up the description for use as a column name
            description = var_descriptions[col]
            # Replace spaces and special characters with underscores
            clean_description = re.sub(r'[^\w\s-]', '', description)
            clean_description = re.sub(r'\s+', '_', clean_description)
            new_header.append(f"{col}_{clean_description}")
        else:
            # Keep original if not found in dictionary
            new_header.append(col)
    
    # Replace the header
    rows[0] = new_header
    
    # Write the updated CSV
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    
    print(f"Updated headers in {output_file}")
    print(f"Found {len([col for col in header if col in var_descriptions])} out of {len(header)} columns in dictionary")

def main():
    """Main function to update PUMS CSV headers."""
    # File paths
    dict_file = "PUMS-2018-data/PUMS_Data_Dictionary_2018.txt"
    housing_file = "PUMS-2018-data/csv_hfl/psam_h12.csv"
    person_file = "PUMS-2018-data/csv_pfl/psam_p12.csv"
    
    # Check if files exist
    if not Path(dict_file).exists():
        print(f"Error: Data dictionary file not found: {dict_file}")
        sys.exit(1)
    
    if not Path(housing_file).exists():
        print(f"Error: Housing CSV file not found: {housing_file}")
        sys.exit(1)
    
    if not Path(person_file).exists():
        print(f"Error: Person CSV file not found: {person_file}")
        sys.exit(1)
    
    # Parse the data dictionary
    print("Parsing PUMS data dictionary...")
    var_descriptions = parse_data_dictionary(dict_file)
    print(f"Found {len(var_descriptions)} variable descriptions")
    
    # Show some examples
    print("\nExample variable descriptions:")
    for i, (var, desc) in enumerate(list(var_descriptions.items())[:5]):
        print(f"  {var}: {desc}")
    
    # Update housing file headers
    print("\nUpdating housing file headers...")
    update_csv_headers(housing_file, var_descriptions, 
                      housing_file.replace('.csv', '_updated_headers.csv'))
    
    # Update person file headers
    print("\nUpdating person file headers...")
    update_csv_headers(person_file, var_descriptions, 
                      person_file.replace('.csv', '_updated_headers.csv'))
    
    print("\nHeader update complete!")

if __name__ == "__main__":
    main() 