import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Tuple, List

def load_data() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Load both math and portuguese datasets"""
    math_df = pd.read_csv('student-mat.csv', sep=';')
    por_df = pd.read_csv('student-por.csv', sep=';')
    return math_df, por_df

def create_grade_bins(df: pd.DataFrame) -> pd.DataFrame:
    """Create grade categories"""
    df['grade_category'] = pd.cut(df['G3'],
                                bins=[-1, 9, 14, 20],
                                labels=['Weak', 'Moderate', 'Strong'])
    return df

def analyze_dataset(df: pd.DataFrame, subject: str) -> dict:
    """Analyze dataset and return findings"""
    results = {}
    
    # Basic information
    results['total_records'] = len(df)
    results['total_features'] = len(df.columns)
    results['column_info'] = df.dtypes.to_dict()
    
    # Create grade categories
    df = create_grade_bins(df)
    
    # Class distribution
    class_dist = df['grade_category'].value_counts()
    class_pct = df['grade_category'].value_counts(normalize=True) * 100
    results['class_distribution'] = {
        category: {'count': count, 'percentage': pct}
        for category, count, pct in zip(class_dist.index, class_dist.values, class_pct.values)
    }
    
    # Missing values
    missing_vals = df.isnull().sum()
    missing_pct = (df.isnull().sum() / len(df)) * 100
    results['missing_values'] = {
        col: {'count': count, 'percentage': pct}
        for col, count, pct in zip(df.columns, missing_vals, missing_pct)
        if count > 0
    }
    
    # Summary statistics for numerical columns
    results['summary_stats'] = df.describe()
    
    # Check balance
    max_min_ratio = class_dist.max() / class_dist.min()
    results['is_balanced'] = max_min_ratio < 1.5  # threshold for balance
    
    return results, df

def create_visualizations(df: pd.DataFrame, subject: str):
    """Create and save visualizations"""
    plt.style.use('seaborn')
    
    # Set up the figure size
    plt.figure(figsize=(15, 10))
    
    # 1. Distribution of final grades
    plt.subplot(2, 2, 1)
    sns.histplot(data=df, x='G3', bins=20)
    plt.title(f'{subject} - Distribution of Final Grades')
    
    # 2. Class distribution
    plt.subplot(2, 2, 2)
    sns.countplot(data=df, x='grade_category')
    plt.title(f'{subject} - Grade Categories Distribution')
    
    # 3. Correlation heatmap
    plt.subplot(2, 2, 3)
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    sns.heatmap(df[numeric_cols].corr(), annot=True, cmap='coolwarm', fmt='.2f')
    plt.title(f'{subject} - Correlation Heatmap')
    
    # 4. Box plots
    plt.subplot(2, 2, 4)
    key_features = ['studytime', 'failures', 'absences', 'G1', 'G2', 'G3']
    df[key_features].boxplot()
    plt.title(f'{subject} - Key Features Distribution')
    
    plt.tight_layout()
    plt.savefig(f'{subject.lower()}_analysis.png')
    plt.close()

def save_report(math_results: dict, por_results: dict):
    """Save analysis report to file"""
    with open('UCI_dataset_analysis.txt', 'w') as f:
        for subject, results in [('Mathematics', math_results), ('Portuguese', por_results)]:
            f.write(f"\n{'='*50}\n")
            f.write(f"Dataset: UCI Student Performance ({subject})\n")
            f.write(f"{'='*50}\n\n")
            
            f.write(f"Records: {results['total_records']}\n")
            f.write(f"Features: {results['total_features']}\n\n")
            
            f.write("Class Distribution:\n")
            for category, stats in results['class_distribution'].items():
                f.write(f"{category}: {stats['count']} ({stats['percentage']:.2f}%)\n")
            
            f.write(f"\nBalance: {'Balanced' if results['is_balanced'] else 'Imbalanced'}\n")
            
            if results['missing_values']:
                f.write("\nMissing Values:\n")
                for col, stats in results['missing_values'].items():
                    f.write(f"{col}: {stats['count']} ({stats['percentage']:.2f}%)\n")
            else:
                f.write("\nNo missing values found.\n")
            
            f.write("\nSummary Statistics:\n")
            f.write(str(results['summary_stats']))
            f.write("\n\n")

def print_summary(results: dict, subject: str):
    """Print summary of analysis"""
    print(f"\nDataset: UCI Student Performance ({subject})")
    print(f"Records: {results['total_records']}")
    print(f"Features: {results['total_features']}")
    print("Target: G3 (final grade)")
    print("\nClasses:")
    for category, stats in results['class_distribution'].items():
        print(f"{category}: {stats['percentage']:.2f}%")
    print(f"Balance: {'Balanced' if results['is_balanced'] else 'Imbalanced'}")
    print(f"Missing Values: {'Yes' if results['missing_values'] else 'No'}")

def main():
    # Load data
    math_df, por_df = load_data()
    
    # Analyze both datasets
    math_results, math_df = analyze_dataset(math_df, 'Mathematics')
    por_results, por_df = analyze_dataset(por_df, 'Portuguese')
    
    # Create visualizations
    create_visualizations(math_df, 'Mathematics')
    create_visualizations(por_df, 'Portuguese')
    
    # Save report
    save_report(math_results, por_results)
    
    # Print summaries
    print_summary(math_results, 'Mathematics')
    print_summary(por_results, 'Portuguese')

if __name__ == "__main__":
    main()