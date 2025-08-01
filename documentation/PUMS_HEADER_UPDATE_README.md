# PUMS CSV Header Update

This project successfully updated the headers of PUMS (Public Use Microdata Sample) CSV files using the official data dictionary to make them more descriptive and user-friendly.

## Files Updated

### Housing File
- **Original**: `PUMS-2018-data/csv_hfl/psam_h12.csv`
- **Updated**: `PUMS-2018-data/csv_hfl/psam_h12_updated_headers.csv`
- **Columns**: 234 total columns

### Person File  
- **Original**: `PUMS-2018-data/csv_pfl/psam_p12.csv`
- **Updated**: `PUMS-2018-data/csv_pfl/psam_p12_updated_headers.csv`
- **Columns**: 286 total columns

## What Was Done

1. **Parsed the PUMS Data Dictionary**: The script `update_pums_headers_improved.py` parsed the official PUMS data dictionary (`PUMS_Data_Dictionary_2018.txt`) to extract variable names and their full descriptions.

2. **Updated CSV Headers**: Each abbreviated column name (e.g., `RT`, `SERIALNO`, `AGEP`) was replaced with a descriptive name that includes the original variable name plus its full description from the data dictionary.

3. **Preserved Data Integrity**: The original data was not modified - only the header row was updated.

## Example Transformations

### Housing File Examples:
- `RT` → `RT_Record_Type`
- `SERIALNO` → `SERIALNO_Housing_unitGQ_person_serial_number`
- `WGTP` → `WGTP_Housing_Unit_Weight`
- `NP` → `NP_Number_of_persons_in_this_household`

### Person File Examples:
- `AGEP` → `AGEP_Age`
- `CIT` → `CIT_Citizenship_status`
- `COW` → `COW_Class_of_worker`
- `SEX` → `SEX_Sex`

## Scripts Created

1. **`update_pums_headers_improved.py`**: Main script that parses the data dictionary and updates CSV headers
2. **`header_mapping_summary.py`**: Utility script to show the mapping between original and updated headers
3. **`update_pums_headers.py`**: Initial version (less accurate parsing)

## Usage

To update headers for new PUMS files:

```bash
python3 update_pums_headers_improved.py
```

To view the header mapping:

```bash
python3 header_mapping_summary.py
```

## Benefits

1. **Improved Readability**: Column names now clearly indicate what data they contain
2. **Better Documentation**: Headers serve as built-in documentation
3. **Easier Analysis**: Researchers can quickly understand what each variable represents
4. **Maintained Compatibility**: Original variable names are preserved as prefixes

## Data Dictionary Source

The variable descriptions were extracted from the official 2018 ACS PUMS Data Dictionary (November 14, 2019), ensuring accuracy and completeness of the header updates. 