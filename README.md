# UCI Student Performance Dataset Analysis

This Python script performs a comprehensive analysis of the UCI Student Performance dataset, including both Mathematics and Portuguese student performance data.

## Setup

1. Install required packages:
```bash
pip install -r requirements.txt
```

2. Make sure you have the dataset files in the same directory:
   - student-mat.csv (Mathematics dataset)
   - student-por.csv (Portuguese dataset)

3. Run the analysis:
```bash
python student_performance_analysis.py
```

## Output

The script will generate:

1. `UCI_dataset_analysis.txt` - Detailed analysis report including:
   - Total records and features
   - Column information
   - Class distribution
   - Missing values analysis
   - Summary statistics

2. Visualization files:
   - `mathematics_analysis.png` - Visual analysis of Mathematics dataset
   - `portuguese_analysis.png` - Visual analysis of Portuguese dataset

3. Console output with key findings for each subject

## Features

- Complete data loading and preprocessing
- Detailed statistical analysis
- Grade categorization (Weak/Moderate/Strong)
- Class balance analysis
- Missing values detection
- Correlation analysis
- Multiple visualizations
- Comprehensive reporting

## Visualizations

The script generates four types of plots for each subject:
1. Distribution of final grades (G3)
2. Grade categories distribution
3. Correlation heatmap of numerical features
4. Box plots of key features

## Note

Make sure you have proper permissions to read/write files in the directory where you run the script.