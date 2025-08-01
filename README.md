# Tampa Police Stops Data Analysis

This repository contains a comprehensive analysis of police stop data from Tampa, Florida, spanning from 1973 to 2018. The dataset contains over 2.8 million police stops with detailed information about subjects, violations, departments, and outcomes.

## Dataset Overview

- **Total Records**: 2,818,240 police stops
- **Date Range**: 1973-2018
- **Departments**: Multiple law enforcement agencies including Tampa Police Department, Hillsborough County Sheriff's Office, Florida Highway Patrol, and others
- **Key Variables**: Subject demographics (race, gender, age), violation types, outcomes, department information, and vehicle registration data

## Analysis Components

### Core Police Stops Analysis
- **Main Script**: `scripts/police_stops_analysis.py`
- **Quick Summary**: `scripts/quick_summary.py`
- **Violation Analysis**: `scripts/violation_analysis.py`

### Additional Analyses
- **CVAP Analysis**: `scripts/cvap_analysis.py` - Citizen Voting Age Population analysis for Hillsborough County
- **Latino Car Ownership**: `scripts/latino_car_ownership_simple.py` - Analysis of Latino car ownership patterns
- **PUMS Data Processing**: `scripts/update_pums_headers.py` and `scripts/update_pums_headers_improved.py` - American Community Survey data processing

### Documentation
- **CVAP Summary**: `documentation/cvap_summary.md` - Detailed findings from CVAP analysis
- **Latino Car Ownership**: `documentation/latino_car_ownership_summary.md` - Analysis of Latino car ownership patterns
- **PUMS Processing**: `documentation/PUMS_HEADER_UPDATE_README.md` - Guide for PUMS data processing
- **Violation Analysis**: `documentation/violation_summary.md` - Detailed violation analysis findings

## Visualizations Created

### Core Police Stops Visualizations
- **Race Distribution** (`1_race_distribution.png`)
- **Violation Categories** (`15_violation_categories.png`)
- **Violation Categories Pie** (`16_violation_categories_pie.png`)
- **Violation Categories by Race** (`17_violation_categories_by_race.png`)
- **CVAP vs Police Comparison** (`18_cvap_vs_police_comparison.png`)
- **Disparity Analysis** (`19_disparity_analysis.png`)
- **Detailed Comparison** (`20_detailed_comparison.png`)

### Additional Analyses
- **Latino Car Ownership Basic** (`latino_car_ownership_basic.png`)
- **Latino Car Ownership by Income** (`latino_car_ownership_income.png`)

*Note: Additional visualizations from the original analysis (2-14) are available in the visualizations directory*

## Key Insights

### Demographic Patterns
- **Race**: White subjects account for the majority of stops, but analysis shows potential disparities when compared to population demographics
- **Gender**: Males are stopped significantly more often than females
- **Age**: Most stops involve adults, with some concentration in specific age ranges

### Temporal Trends
- Police stop activity shows varying patterns over the decades
- Seasonal and weekly patterns reveal when stops are most common
- Long-term trends may reflect changes in policing strategies

### Department Differences
- Tampa Police Department handles the majority of stops
- Different departments show varying patterns in demographics and violation types
- Some departments may have different approaches to policing

### Violation Analysis
- Traffic violations dominate the dataset
- Specific violation codes show what behaviors lead to most stops
- Racial differences in violation types may indicate bias

### Outcome Disparities
- Different racial groups may receive different outcomes for similar violations
- Citation vs. warning patterns show potential disparities in treatment
- Critical for understanding fairness in policing

### CVAP Analysis
- Citizen Voting Age Population analysis for Hillsborough County, Florida
- Comparison of police stop demographics with voting-age population
- Important for understanding representation and potential bias

### Latino Car Ownership
- Analysis of Latino car ownership patterns in the Tampa area
- Income-based analysis of vehicle ownership
- Important for understanding mobility and economic factors

## Technical Details

### Data Processing
- Cleaned and standardized department names
- Handled missing values appropriately
- Converted dates and ages to proper formats
- Extracted violation categories from detailed violation codes
- Processed American Community Survey (PUMS) data for demographic comparisons

### Visualization Tools
- **Matplotlib**: Static charts and graphs
- **Seaborn**: Statistical visualizations and heatmaps
- **Plotly**: Interactive dashboards
- **Pandas**: Data manipulation and analysis

### File Structure
```
police-stops-data-clean/
├── csvs/                           # Data files
│   ├── police-stop-data/           # Police stops dataset
│   └── PUMS-2018-data/            # American Community Survey data
│       ├── csv_hfl/               # Household-level data
│       └── csv_pfl/               # Person-level data
├── scripts/                        # Analysis scripts
│   ├── police_stops_analysis.py    # Main police stops analysis
│   ├── quick_summary.py           # Quick dataset summary
│   ├── violation_analysis.py      # Detailed violation analysis
│   ├── cvap_analysis.py           # CVAP demographic analysis
│   ├── latino_car_ownership_simple.py  # Latino car ownership analysis
│   ├── update_pums_headers.py     # PUMS data processing
│   └── update_pums_headers_improved.py  # Improved PUMS processing
├── documentation/                  # Analysis documentation
│   ├── cvap_summary.md            # CVAP analysis findings
│   ├── latino_car_ownership_summary.md  # Latino car ownership findings
│   ├── PUMS_HEADER_UPDATE_README.md     # PUMS processing guide
│   └── violation_summary.md       # Violation analysis findings
├── visualizations/                 # Generated charts and graphs
│   ├── 1_race_distribution.png
│   ├── 15_violation_categories.png
│   ├── 16_violation_categories_pie.png
│   ├── 17_violation_categories_by_race.png
│   ├── 18_cvap_vs_police_comparison.png
│   ├── 19_disparity_analysis.png
│   ├── 20_detailed_comparison.png
│   ├── latino_car_ownership_basic.png
│   └── latino_car_ownership_income.png
├── requirements.txt                # Python dependencies
└── README.md                      # This file
```

## Running the Analysis

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run specific analyses:
   ```bash
   # Main police stops analysis
   python3 police_stops_analysis.py
   
   # Quick summary
   python3 quick_summary.py
   
   # Violation analysis
   python3 violation_analysis.py
   
   # CVAP analysis
   python3 cvap_analysis.py
   
   # Latino car ownership analysis
   python3 latino_car_ownership_simple.py
   ```

3. View results:
   - PNG files can be opened in any image viewer
   - HTML dashboards can be opened in a web browser
   - Documentation files provide detailed analysis summaries

## Data Privacy and Ethics

This analysis is conducted for research and transparency purposes. The data has been anonymized and aggregated to protect individual privacy while still providing valuable insights into policing patterns.

## Limitations

- Population estimates used in disparity analysis are approximate
- Missing data in some fields (particularly age) may affect analysis
- The dataset may not capture all police interactions
- Historical data may not reflect current policing practices
- CVAP analysis relies on American Community Survey estimates

## Future Work

Potential areas for further analysis:
- Geographic analysis of stop locations
- Officer-specific patterns
- Comparison with other cities
- Machine learning models for predicting stop outcomes
- Real-time dashboard for ongoing monitoring
- Integration of additional demographic datasets
- Longitudinal analysis of policing trends

---

*This analysis was created to promote transparency and understanding of policing patterns in Tampa, Florida.* 