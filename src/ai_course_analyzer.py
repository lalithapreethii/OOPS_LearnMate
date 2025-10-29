import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple
from scipy import stats

class AICourseAnalyzer:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.df = None
        self.analysis_results = {}
        
    def load_data(self) -> None:
        """Load dataset and handle basic preprocessing"""
        try:
            self.df = pd.read_csv(self.file_path)
        except:
            try:
                self.df = pd.read_excel(self.file_path)
            except Exception as e:
                raise Exception(f"Error loading file: {e}")
                
        print(f"Loaded dataset with {len(self.df)} records and {len(self.df.columns)} features")
        
    def create_grade_categories(self) -> None:
        """Create grade categories based on final grade"""
        # Assuming final grade is in 0-100 scale
        # Adjust the column name and bins as per actual data
        grade_col = [col for col in self.df.columns if 'final' in col.lower() or 'grade' in col.lower()][0]
        
        self.df['grade_category'] = pd.cut(
            self.df[grade_col],
            bins=[0, 59, 79, 100],
            labels=['Weak', 'Moderate', 'Strong']
        )
        
    def analyze_dataset(self) -> None:
        """Perform comprehensive dataset analysis"""
        # Basic info
        self.analysis_results['total_records'] = len(self.df)
        self.analysis_results['total_features'] = len(self.df.columns)
        self.analysis_results['column_info'] = self.df.dtypes.to_dict()
        
        # Class distribution
        class_dist = self.df['grade_category'].value_counts()
        class_pct = self.df['grade_category'].value_counts(normalize=True) * 100
        
        self.analysis_results['class_distribution'] = {
            category: {'count': count, 'percentage': pct}
            for category, count, pct in zip(class_dist.index, class_dist.values, class_pct.values)
        }
        
        # Missing values
        missing_vals = self.df.isnull().sum()
        missing_pct = (self.df.isnull().sum() / len(self.df)) * 100
        
        self.analysis_results['missing_values'] = {
            col: {'count': count, 'percentage': pct}
            for col, count, pct in zip(missing_vals.index, missing_vals.values, missing_pct.values)
            if count > 0
        }
        
        # Summary statistics
        self.analysis_results['summary_stats'] = self.df.describe()
        
        # Check balance
        max_min_ratio = class_dist.max() / class_dist.min()
        self.analysis_results['is_balanced'] = max_min_ratio < 1.5
        
        # Feature correlations
        numerical_cols = self.df.select_dtypes(include=[np.number]).columns
        correlations = self.df[numerical_cols].corr()
        self.analysis_results['correlations'] = correlations
        
        # Top 5 correlated features with target
        target_col = [col for col in self.df.columns if 'final' in col.lower() or 'grade' in col.lower()][0]
        feature_correlations = abs(correlations[target_col]).sort_values(ascending=False)
        self.analysis_results['top_correlations'] = feature_correlations[1:6].to_dict()  # Excluding self-correlation
        
    def check_data_quality(self) -> None:
        """Perform data quality checks"""
        # Check duplicates
        self.analysis_results['duplicates'] = {
            'count': self.df.duplicated().sum(),
            'percentage': (self.df.duplicated().sum() / len(self.df)) * 100
        }
        
        # Check outliers using IQR method
        numerical_cols = self.df.select_dtypes(include=[np.number]).columns
        outliers = {}
        
        for col in numerical_cols:
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            outlier_count = len(self.df[(self.df[col] < (Q1 - 1.5 * IQR)) | (self.df[col] > (Q3 + 1.5 * IQR))])
            outliers[col] = {
                'count': outlier_count,
                'percentage': (outlier_count / len(self.df)) * 100
            }
            
        self.analysis_results['outliers'] = outliers
        
    def create_visualizations(self) -> None:
        """Generate all required visualizations"""
        plt.style.use('seaborn')
        fig = plt.figure(figsize=(20, 15))
        
        # 1. Grade Distribution
        plt.subplot(2, 3, 1)
        target_col = [col for col in self.df.columns if 'final' in col.lower() or 'grade' in col.lower()][0]
        sns.histplot(data=self.df, x=target_col, bins=20)
        plt.title('Distribution of Final Grades')
        
        # 2. Class Balance Pie Chart
        plt.subplot(2, 3, 2)
        class_dist = self.df['grade_category'].value_counts()
        plt.pie(class_dist.values, labels=class_dist.index, autopct='%1.1f%%')
        plt.title('Grade Categories Distribution')
        
        # 3. Box Plots
        plt.subplot(2, 3, 3)
        numerical_cols = self.df.select_dtypes(include=[np.number]).columns[:5]  # First 5 numerical columns
        self.df[numerical_cols].boxplot()
        plt.xticks(rotation=45)
        plt.title('Key Features Distribution')
        
        # 4. Correlation Heatmap
        plt.subplot(2, 3, 4)
        sns.heatmap(
            self.analysis_results['correlations'],
            annot=True,
            fmt='.2f',
            cmap='coolwarm'
        )
        plt.title('Feature Correlations')
        
        # 5. Feature Importance (based on correlation with target)
        plt.subplot(2, 3, 5)
        top_corr = pd.Series(self.analysis_results['top_correlations'])
        top_corr.plot(kind='bar')
        plt.title('Top 5 Correlated Features')
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        plt.savefig('ai_course_analysis.png')
        plt.close()
        
    def save_report(self) -> None:
        """Save analysis report to file"""
        with open('AI_Course_dataset_analysis.txt', 'w') as f:
            f.write("AI Course Student Performance Dataset Analysis\n")
            f.write("=" * 50 + "\n\n")
            
            # Summary Table
            f.write("Summary Table:\n")
            f.write("| Metric | Value |\n")
            f.write("|--------|-------|\n")
            f.write(f"| Total Records | {self.analysis_results['total_records']} |\n")
            f.write(f"| Features | {self.analysis_results['total_features']} |\n")
            target_col = [col for col in self.df.columns if 'final' in col.lower() or 'grade' in col.lower()][0]
            f.write(f"| Target Variable | {target_col} |\n")
            
            for category in ['Weak', 'Moderate', 'Strong']:
                pct = self.analysis_results['class_distribution'][category]['percentage']
                f.write(f"| {category} Class % | {pct:.1f} |\n")
            
            total_missing = sum(info['count'] for info in self.analysis_results['missing_values'].values())
            total_possible = self.analysis_results['total_records'] * self.analysis_results['total_features']
            missing_pct = (total_missing / total_possible) * 100
            f.write(f"| Missing Values | {missing_pct:.1f}% |\n")
            
            f.write(f"| Balance Status | {'Balanced' if self.analysis_results['is_balanced'] else 'Imbalanced'} |\n\n")
            
            # Detailed Analysis
            f.write("\nDetailed Analysis:\n")
            f.write("\n1. Class Distribution:\n")
            for category, stats in self.analysis_results['class_distribution'].items():
                f.write(f"{category}: {stats['count']} ({stats['percentage']:.1f}%)\n")
            
            f.write("\n2. Top 5 Correlated Features:\n")
            for feature, corr in self.analysis_results['top_correlations'].items():
                f.write(f"{feature}: {corr:.3f}\n")
            
            f.write("\n3. Data Quality:\n")
            f.write(f"Duplicates: {self.analysis_results['duplicates']['count']} ")
            f.write(f"({self.analysis_results['duplicates']['percentage']:.1f}%)\n")
            
            f.write("\nOutliers:\n")
            for feature, stats in self.analysis_results['outliers'].items():
                if stats['count'] > 0:
                    f.write(f"{feature}: {stats['count']} ({stats['percentage']:.1f}%)\n")
            
            f.write("\n4. Summary Statistics:\n")
            f.write(str(self.analysis_results['summary_stats']))

def main():
    # Initialize analyzer
    analyzer = AICourseAnalyzer('ai_course_data.csv')  # Adjust filename as needed
    
    print("Loading dataset...")
    analyzer.load_data()
    
    print("Creating grade categories...")
    analyzer.create_grade_categories()
    
    print("Analyzing dataset...")
    analyzer.analyze_dataset()
    
    print("Checking data quality...")
    analyzer.check_data_quality()
    
    print("Creating visualizations...")
    analyzer.create_visualizations()
    
    print("Saving analysis report...")
    analyzer.save_report()
    
    print("\nAnalysis complete! Check 'AI_Course_dataset_analysis.txt' and 'ai_course_analysis.png'")

if __name__ == "__main__":
    main()