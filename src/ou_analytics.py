import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple

class OUAnalytics:
    def __init__(self):
        self.datasets = {}
        self.merged_data = None
        self.analysis_results = {}

    def load_data(self) -> None:
        """Load all CSV files"""
        file_paths = {
            'student_info': 'studentInfo.csv',
            'assessments': 'assessments.csv',
            'student_assessment': 'studentAssessment.csv',
            'courses': 'courses.csv',
            'student_vle': 'studentVle.csv',
            'vle': 'vle.csv'
        }
        
        for key, path in file_paths.items():
            self.datasets[key] = pd.read_csv(path)
            print(f"Loaded {key}: {len(self.datasets[key])} records")

    def merge_datasets(self) -> None:
        """Merge relevant tables and create features"""
        # Merge student assessments with assessment info
        assessment_data = pd.merge(
            self.datasets['student_assessment'],
            self.datasets['assessments'],
            on='id_assessment'
        )

        # Calculate average score per student per course
        student_scores = assessment_data.groupby(
            ['id_student', 'code_module']
        )['score'].agg(['mean', 'count']).reset_index()
        student_scores.columns = ['id_student', 'code_module', 'avg_score', 'assessment_count']

        # Aggregate VLE interactions
        vle_aggregated = self.datasets['student_vle'].groupby(
            ['id_student', 'code_module']
        )['sum_click'].agg(['sum', 'count']).reset_index()
        vle_aggregated.columns = ['id_student', 'code_module', 'total_clicks', 'resources_accessed']

        # Merge everything with student info
        self.merged_data = pd.merge(
            self.datasets['student_info'],
            student_scores,
            on=['id_student', 'code_module'],
            how='left'
        )
        
        self.merged_data = pd.merge(
            self.merged_data,
            vle_aggregated,
            on=['id_student', 'code_module'],
            how='left'
        )

        # Create new features
        self.create_features()

    def create_features(self) -> None:
        """Create new analytical features"""
        # Fill missing values
        self.merged_data['total_clicks'].fillna(0, inplace=True)
        self.merged_data['resources_accessed'].fillna(0, inplace=True)
        
        # Create engagement levels
        click_quantiles = self.merged_data['total_clicks'].quantile([0.33, 0.66])
        self.merged_data['engagement_level'] = pd.cut(
            self.merged_data['total_clicks'],
            bins=[-np.inf, click_quantiles[0.33], click_quantiles[0.66], np.inf],
            labels=['Low', 'Medium', 'High']
        )

        # Create performance categories
        performance_map = {
            'Fail': 'Weak',
            'Withdrawn': 'Weak',
            'Pass': 'Moderate',
            'Distinction': 'Strong'
        }
        self.merged_data['performance_category'] = self.merged_data['final_result'].map(performance_map)

    def analyze_dataset(self) -> None:
        """Perform comprehensive dataset analysis"""
        self.analysis_results = {
            'unique_students': len(self.merged_data['id_student'].unique()),
            'total_records': len(self.merged_data),
            'total_features': len(self.merged_data.columns),
            'column_info': self.merged_data.dtypes.to_dict(),
            'class_distribution': self.merged_data['final_result'].value_counts().to_dict(),
            'class_distribution_pct': (self.merged_data['final_result'].value_counts(normalize=True) * 100).to_dict(),
            'performance_distribution': self.merged_data['performance_category'].value_counts().to_dict(),
            'performance_distribution_pct': (self.merged_data['performance_category'].value_counts(normalize=True) * 100).to_dict(),
            'missing_values': self.merged_data.isnull().sum().to_dict(),
            'missing_percentages': (self.merged_data.isnull().sum() / len(self.merged_data) * 100).to_dict(),
            'summary_stats': self.merged_data.describe().to_dict()
        }

    def create_visualizations(self) -> None:
        """Generate all required visualizations"""
        plt.style.use('seaborn')
        
        # Set up the figure
        fig = plt.figure(figsize=(20, 15))
        
        # 1. Original class distribution
        plt.subplot(2, 3, 1)
        sns.countplot(data=self.merged_data, x='final_result')
        plt.title('Distribution of Final Results')
        plt.xticks(rotation=45)
        
        # 2. New performance categories
        plt.subplot(2, 3, 2)
        sns.countplot(data=self.merged_data, x='performance_category')
        plt.title('Distribution of Performance Categories')
        
        # 3. Average assessment scores
        plt.subplot(2, 3, 3)
        sns.histplot(data=self.merged_data, x='avg_score', bins=30)
        plt.title('Distribution of Average Assessment Scores')
        
        # 4. VLE clicks vs Average score
        plt.subplot(2, 3, 4)
        sns.scatterplot(
            data=self.merged_data,
            x='total_clicks',
            y='avg_score',
            hue='performance_category'
        )
        plt.title('VLE Clicks vs Average Score')
        
        # 5. Correlation heatmap
        plt.subplot(2, 3, 5)
        numeric_cols = self.merged_data.select_dtypes(include=[np.number]).columns
        sns.heatmap(
            self.merged_data[numeric_cols].corr(),
            annot=True,
            fmt='.2f',
            cmap='coolwarm'
        )
        plt.title('Correlation Matrix')
        
        plt.tight_layout()
        plt.savefig('ou_analysis_visualizations.png')
        plt.close()

    def save_report(self) -> None:
        """Save analysis report to file"""
        with open('OU_dataset_analysis.txt', 'w') as f:
            f.write("Open University Learning Analytics Dataset Analysis\n")
            f.write("="*50 + "\n\n")
            
            f.write("1. Dataset Overview\n")
            f.write(f"Total unique students: {self.analysis_results['unique_students']}\n")
            f.write(f"Total records: {self.analysis_results['total_records']}\n")
            f.write(f"Total features: {self.analysis_results['total_features']}\n\n")
            
            f.write("2. Class Distribution (Original)\n")
            for category, count in self.analysis_results['class_distribution'].items():
                percentage = self.analysis_results['class_distribution_pct'][category]
                f.write(f"{category}: {count} ({percentage:.2f}%)\n")
            
            f.write("\n3. Performance Categories Distribution\n")
            for category, count in self.analysis_results['performance_distribution'].items():
                percentage = self.analysis_results['performance_distribution_pct'][category]
                f.write(f"{category}: {count} ({percentage:.2f}%)\n")
            
            f.write("\n4. Missing Values Analysis\n")
            for column, count in self.analysis_results['missing_values'].items():
                percentage = self.analysis_results['missing_percentages'][column]
                if count > 0:
                    f.write(f"{column}: {count} missing values ({percentage:.2f}%)\n")
            
            f.write("\n5. Summary Statistics\n")
            f.write(str(pd.DataFrame(self.analysis_results['summary_stats'])))

def main():
    # Initialize analyzer
    analyzer = OUAnalytics()
    
    # Execute analysis pipeline
    print("Loading datasets...")
    analyzer.load_data()
    
    print("\nMerging datasets and creating features...")
    analyzer.merge_datasets()
    
    print("\nAnalyzing merged dataset...")
    analyzer.analyze_dataset()
    
    print("\nGenerating visualizations...")
    analyzer.create_visualizations()
    
    print("\nSaving analysis report...")
    analyzer.save_report()
    
    print("\nAnalysis complete! Check 'OU_dataset_analysis.txt' and 'ou_analysis_visualizations.png'")

if __name__ == "__main__":
    main()