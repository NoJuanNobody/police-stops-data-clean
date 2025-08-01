#!/usr/bin/env python3
"""
Script to update PUMS CSV headers using the data dictionary.
This script reads the PUMS data dictionary and updates CSV headers with full descriptions.
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
    
    # Split into sections
    sections = content.split('\n\n')
    
    for section in sections:
        lines = section.strip().split('\n')
        if len(lines) < 3:
            continue
            
        # Look for variable definitions (format: VARNAME followed by description)
        for i, line in enumerate(lines):
            # Check if line contains a variable name (all caps, followed by whitespace)
            match = re.match(r'^([A-Z][A-Z0-9]+)\s+', line)
            if match:
                var_name = match.group(1)
                
                # Get the description from the next line or current line
                description = ""
                if i + 1 < len(lines) and lines[i + 1].strip().startswith('.'):
                    # Description is on next line
                    description = lines[i + 1].strip().lstrip('.')
                else:
                    # Description might be on same line after variable name
                    parts = line.split()
                    if len(parts) > 1:
                        description = ' '.join(parts[1:])
                
                if description:
                    var_descriptions[var_name] = description.strip()
    
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
            new_header.append(f"{col}_{var_descriptions[col]}")
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