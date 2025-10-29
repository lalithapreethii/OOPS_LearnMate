<<<<<<< HEAD
# UCI Student Performance Dataset Analysis

This Python script performs a comprehensive analysis of the UCI Student Performance dataset, including both Mathematics and Portuguese student performance data.

## Setup

1. Install required packages:
=======
﻿# Know Where You Lack

A machine learning project for predicting and analyzing student performance across multiple datasets.

## Datasets Used
- AI Course Dataset: Student performance data from AI courses
- UCI Dataset: Student performance data from Portuguese schools (Mathematics and Portuguese language courses)
- OU Dataset: Open University Learning Analytics Dataset

## Project Structure
```
.
 data/
    processed/    # Processed and cleaned datasets
    raw/         # Original source datasets
 models/          # Trained model files
 reports/         # Analysis reports and visualizations
 results/         # Final results and comparisons
 src/            # Source code
     preprocessor/  # Data preprocessing modules
```

## Features
- Multi-dataset analysis of student performance
- Ensemble modeling (Random Forest + XGBoost)
- Performance prediction across different academic contexts
- Feature importance analysis
- Comparative analysis with literature results

## Setup
1. Clone the repository:
```bash
git clone https://github.com/JoshikaMannam/Know-Where-You-Lack.git
cd Know-Where-You-Lack
```

2. Install dependencies:
>>>>>>> 431bf9542c2f2ee979b73168008154307fdc1749
```bash
pip install -r requirements.txt
```

<<<<<<< HEAD
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
=======
3. Download the datasets:
- AI Course Dataset: [Link to be added]
- UCI Dataset: https://archive.ics.uci.edu/ml/datasets/Student+Performance
- OU Dataset: [Link to be added]

Place the downloaded datasets in their respective folders under `data/raw/`.

## Usage
1. Preprocess the data:
```bash
python src/run_preprocessing.py
```

2. Train the models:
```bash
python src/train_models.py
```

3. Evaluate and analyze results:
```bash
python src/evaluate_model.py
```

## Results
- Achieved high accuracy in predicting student performance levels
- Identified key factors influencing academic success
- Generated comprehensive comparison with existing literature

## License
MIT License
>>>>>>> 431bf9542c2f2ee979b73168008154307fdc1749
