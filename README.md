# Tampa Police Stops Data Analysis

This repository contains a comprehensive analysis of police stop data from Tampa, Florida, spanning from 1973 to 2018. The dataset contains over 2.8 million police stops with detailed information about subjects, violations, departments, and outcomes.

## Dataset Overview

- **Total Records**: 2,818,240 police stops
- **Date Range**: 1973-2018
- **Departments**: Multiple law enforcement agencies including Tampa Police Department, Hillsborough County Sheriff's Office, Florida Highway Patrol, and others
- **Key Variables**: Subject demographics (race, gender, age), violation types, outcomes, department information, and vehicle registration data

## Visualizations Created

### 1. **Race Distribution** (`1_race_distribution.png`)
- Pie chart showing the breakdown of police stops by subject race
- Reveals potential racial disparities in policing patterns
- Key finding: White subjects account for the majority of stops

### 2. **Gender Distribution** (`2_gender_distribution.png`)
- Bar chart comparing stops by subject gender
- Shows significant gender gap in police stops
- Key finding: Males are stopped more frequently than females

### 3. **Age Distribution** (`3_age_distribution.png`)
- Histogram showing the age distribution of subjects
- Helps identify which age groups are most frequently stopped
- Note: Many records have missing age data

### 4. **Temporal Analysis** (`4_stops_over_time.png`)
- Line chart showing police stops over time (1973-2018)
- Reveals trends and patterns in policing activity
- Shows how stop frequency has changed over decades

### 5. **Department Activity** (`5_department_activity.png`)
- Horizontal bar chart showing stops by law enforcement agency
- Tampa Police Department leads with ~1.3M stops
- Shows the relative activity levels of different departments

### 6. **Department vs Race Heatmap** (`6_dept_race_heatmap.png`)
- Heatmap showing the relationship between departments and subject race
- Reveals department-specific patterns in racial demographics
- Helps identify potential disparities across different agencies

### 7. **Top Violations** (`7_top_violations.png`)
- Horizontal bar chart of most common violation codes
- Shows what types of violations lead to the most stops
- Traffic violations dominate the dataset

### 8. **Violation Types by Race** (`8_violation_by_race.png`)
- Stacked bar chart showing violation types across racial groups
- Reveals if different racial groups are stopped for different reasons
- Important for understanding potential bias in policing

### 9. **Vehicle Registration Analysis** (`9_vehicle_registration.png`)
- Bar chart showing vehicle registration states
- Florida vehicles dominate, but shows out-of-state traffic
- Useful for understanding the geographic scope of stops

### 10. **Outcome Analysis** (`10_outcome_analysis.png`)
- Pie chart showing the breakdown of stop outcomes
- Citations, warnings, arrests, etc.
- Shows how stops are typically resolved

### 11. **Outcomes by Race** (`11_outcome_by_race.png`)
- Stacked bar chart comparing outcomes across racial groups
- Critical for identifying potential disparities in treatment
- Shows if different groups receive different outcomes for similar violations

### 12. **Seasonal Patterns** (`12_seasonal_patterns.png`)
- Heatmap showing stops by month and day of week
- Reveals temporal patterns in policing activity
- Helps identify peak times for police stops

### 13. **Interactive Dashboard** (`13_summary_dashboard.html`)
- Interactive HTML dashboard with key statistics
- Summary table with dataset overview
- Can be opened in any web browser

### 14. **Disparity Analysis** (`14_disparity_analysis.png`)
- Comparative analysis of stop rates vs. population demographics
- Uses estimated population data to calculate per-capita stop rates
- Critical for identifying over-policing of specific groups

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

## Technical Details

### Data Processing
- Cleaned and standardized department names
- Handled missing values appropriately
- Converted dates and ages to proper formats
- Extracted violation categories from detailed violation codes

### Visualization Tools
- **Matplotlib**: Static charts and graphs
- **Seaborn**: Statistical visualizations and heatmaps
- **Plotly**: Interactive dashboards
- **Pandas**: Data manipulation and analysis

### File Structure
```
police-stops-data/
├── fl_tampa_2020_04_01.csv    # Raw data file
├── police_stops_analysis.py    # Analysis script
├── requirements.txt            # Python dependencies
├── README.md                  # This file
└── visualizations/            # Generated visualizations
    ├── 1_race_distribution.png
    ├── 2_gender_distribution.png
    ├── 3_age_distribution.png
    ├── 4_stops_over_time.png
    ├── 5_department_activity.png
    ├── 6_dept_race_heatmap.png
    ├── 7_top_violations.png
    ├── 8_violation_by_race.png
    ├── 9_vehicle_registration.png
    ├── 10_outcome_analysis.png
    ├── 11_outcome_by_race.png
    ├── 12_seasonal_patterns.png
    ├── 13_summary_dashboard.html
    └── 14_disparity_analysis.png
```

## Running the Analysis

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the analysis:
   ```bash
   python3 police_stops_analysis.py
   ```

3. View results:
   - PNG files can be opened in any image viewer
   - HTML dashboard can be opened in a web browser

## Data Privacy and Ethics

This analysis is conducted for research and transparency purposes. The data has been anonymized and aggregated to protect individual privacy while still providing valuable insights into policing patterns.

## Limitations

- Population estimates used in disparity analysis are approximate
- Missing data in some fields (particularly age) may affect analysis
- The dataset may not capture all police interactions
- Historical data may not reflect current policing practices

## Future Work

Potential areas for further analysis:
- Geographic analysis of stop locations
- Officer-specific patterns
- Comparison with other cities
- Machine learning models for predicting stop outcomes
- Real-time dashboard for ongoing monitoring

---

*This analysis was created to promote transparency and understanding of policing patterns in Tampa, Florida.* 