import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from typing import Tuple, Dict, List
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
import sys
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('preprocessing.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

# Define directory structure
BASE_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = BASE_DIR / 'data'
RAW_DATA_DIR = DATA_DIR / 'raw'
PROCESSED_DATA_DIR = DATA_DIR / 'processed'
REPORTS_DIR = BASE_DIR / 'reports'

# Create directories if they don't exist
for directory in [DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, REPORTS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

class DataPreprocessor:
    def __init__(self, dataset_name: str):
        self.dataset_name = dataset_name
        self.raw_data = None
        self.processed_data = None
        self.scalers = {}
        self.encoders = {}
        self.preprocessing_report = {}
        
    def load_data(self) -> None:
        """Load dataset based on name"""
        try:
            if self.dataset_name == "UCI":
                # UCI Student Performance Dataset
                uci_dir = RAW_DATA_DIR / 'uci_data'
                math_path = uci_dir / "student-mat.csv"
                por_path = uci_dir / "student-por.csv"
                
                if not (math_path.exists() and por_path.exists()):
                    raise FileNotFoundError(f"UCI dataset files not found in {uci_dir}")
                    
                math_df = pd.read_csv(math_path, sep=';')
                por_df = pd.read_csv(por_path, sep=';')
                math_df['subject'] = 'math'
                por_df['subject'] = 'portuguese'
                self.raw_data = pd.concat([math_df, por_df], ignore_index=True)
                
            elif self.dataset_name == "OU":
                # OU Analyse Dataset
                ou_dir = RAW_DATA_DIR / 'ou_data'
                
                # Load only essential columns from each file
                student_info = pd.read_csv(ou_dir / 'studentInfo.csv', 
                                         usecols=['id_student', 'gender', 'region', 'highest_education'])
                
                assessments = pd.read_csv(ou_dir / 'studentAssessment.csv',
                                        usecols=['id_student', 'id_assessment', 'score'])
                
                # Aggregate assessment scores
                assessment_summary = assessments.groupby('id_student')['score'].agg(['mean', 'count']).reset_index()
                assessment_summary.columns = ['id_student', 'avg_score', 'assessment_count']
                
                # Merge the dataframes efficiently
                self.raw_data = student_info.merge(assessment_summary, on='id_student', how='left')
                
            elif self.dataset_name == "AI":
                # AI Course Performance Dataset
                ai_dir = RAW_DATA_DIR / 'ai_course_data'
                ai_file = ai_dir / 'Student Performance Dataset in AI course' / 'Stu_Performance_dataset.csv'
                
                if not ai_file.exists():
                    raise FileNotFoundError(f"AI course dataset file not found in {ai_dir}")
                    
                self.raw_data = pd.read_csv(ai_file)
                
                if not (math_path.exists() and por_path.exists()):
                    raise FileNotFoundError(
                        f"UCI dataset files not found. Please place 'student-mat.csv' and "
                        f"'student-por.csv' in {RAW_DATA_DIR}"
                    )
                
                math_df = pd.read_csv(math_path, sep=';')
                por_df = pd.read_csv(por_path, sep=';')
                math_df['subject'] = 'math'
                por_df['subject'] = 'portuguese'
                self.raw_data = pd.concat([math_df, por_df], ignore_index=True)
                
            elif self.dataset_name == "OU":
                # Load and merge relevant OU dataset files
                required_files = ['studentInfo.csv', 'studentAssessment.csv']
                for file in required_files:
                    if not (RAW_DATA_DIR / file).exists():
                        raise FileNotFoundError(
                            f"OU dataset file '{file}' not found in {RAW_DATA_DIR}"
                        )
                
                student_info = pd.read_csv(RAW_DATA_DIR / 'studentInfo.csv')
                assessments = pd.read_csv(RAW_DATA_DIR / 'studentAssessment.csv')
                self.raw_data = pd.merge(student_info, assessments, on='id_student')
                
            elif self.dataset_name == "AI":
                # Load AI course dataset
                ai_path = RAW_DATA_DIR / 'ai_course_data.csv'
                if not ai_path.exists():
                    raise FileNotFoundError(
                        f"AI course dataset file not found. Please place 'ai_course_data.csv' "
                        f"in {RAW_DATA_DIR}"
                    )
                self.raw_data = pd.read_csv(ai_path)
                
            logging.info(f"Successfully loaded {self.dataset_name} dataset with shape {self.raw_data.shape}")
            
        except Exception as e:
            logging.error(f"Error loading {self.dataset_name} dataset: {str(e)}")
            raise
        
        self.preprocessing_report['original_shape'] = self.raw_data.shape
        
    def handle_missing_values(self) -> None:
        """Handle missing values using median and mode imputation"""
        missing_report = {}
        
        for column in self.raw_data.columns:
            missing_pct = self.raw_data[column].isnull().sum() / len(self.raw_data) * 100
            
            if missing_pct > 50:
                self.raw_data.drop(column, axis=1, inplace=True)
                missing_report[column] = f"Dropped (missing: {missing_pct:.1f}%)"
            elif missing_pct > 0:
                if self.raw_data[column].dtype in ['int64', 'float64']:
                    median_value = self.raw_data[column].median()
                    self.raw_data[column].fillna(median_value, inplace=True)
                    missing_report[column] = f"Median imputed (missing: {missing_pct:.1f}%)"
                else:
                    mode_value = self.raw_data[column].mode()[0]
                    self.raw_data[column].fillna(mode_value, inplace=True)
                    missing_report[column] = f"Mode imputed (missing: {missing_pct:.1f}%)"
        
        self.preprocessing_report['missing_values'] = missing_report
        
    def encode_categorical_variables(self) -> None:
        """Encode categorical variables using Label and One-Hot encoding"""
        encoding_report = {}
        
        # Identify binary and multi-class categorical columns
        categorical_columns = self.raw_data.select_dtypes(include=['object']).columns
        
        for column in categorical_columns:
            unique_values = self.raw_data[column].nunique()
            
            if unique_values == 2:
                # Binary: Use Label Encoding
                le = LabelEncoder()
                self.raw_data[column] = le.fit_transform(self.raw_data[column])
                self.encoders[column] = le
                encoding_report[column] = f"Label Encoded: {dict(zip(le.classes_, le.transform(le.classes_)))}"
            else:
                # Multi-class: Use One-Hot Encoding
                dummies = pd.get_dummies(self.raw_data[column], prefix=column, drop_first=True)
                self.raw_data = pd.concat([self.raw_data.drop(column, axis=1), dummies], axis=1)
                encoding_report[column] = f"One-Hot Encoded: {list(dummies.columns)}"
        
        self.preprocessing_report['encoding'] = encoding_report
        
    def engineer_features(self) -> None:
        """Create new features based on dataset"""
        features_created = []
        
        if self.dataset_name == "UCI":
            # UCI specific features
            self.raw_data['avg_score'] = self.raw_data[['G1', 'G2', 'G3']].mean(axis=1)
            self.raw_data['score_trend'] = (self.raw_data['G3'] - self.raw_data['G1']) / 2
            self.raw_data['performance_consistency'] = self.raw_data[['G1', 'G2', 'G3']].std(axis=1)
            features_created.extend(['avg_score', 'score_trend', 'performance_consistency'])
            
        elif self.dataset_name == "OU":
            # OU specific features
            self.raw_data['avg_score'] = self.raw_data.groupby('id_student')['score'].transform('mean')
            self.raw_data['attempts_per_topic'] = self.raw_data.groupby(['id_student', 'code_module'])['score'].transform('count')
            features_created.extend(['avg_score', 'attempts_per_topic'])
            
        elif self.dataset_name == "AI":
            # AI course specific features
            score_columns = [col for col in self.raw_data.columns if 'score' in col.lower()]
            self.raw_data['avg_score'] = self.raw_data[score_columns].mean(axis=1)
            self.raw_data['performance_consistency'] = self.raw_data[score_columns].std(axis=1)
            features_created.extend(['avg_score', 'performance_consistency'])
        
        # Common features for all datasets
        self.raw_data['at_risk_flag'] = (self.raw_data['avg_score'] < 50).astype(int)
        features_created.append('at_risk_flag')
        
        self.preprocessing_report['engineered_features'] = features_created
        
    def create_target_variable(self) -> None:
        """Create 3-class target variable"""
        if self.dataset_name == "UCI":
            score_col = 'G3'
        elif self.dataset_name == "OU":
            score_col = 'score'
        else:
            score_col = 'final_grade'
            
        self.raw_data['weakness_level'] = pd.cut(
            self.raw_data[score_col],
            bins=[-np.inf, 60, 80, np.inf],
            labels=[0, 1, 2]
        )
        
        class_dist = self.raw_data['weakness_level'].value_counts(normalize=True) * 100
        self.preprocessing_report['target_distribution'] = class_dist.to_dict()
        
    def handle_outliers(self) -> None:
        """Handle outliers using IQR method"""
        numerical_columns = self.raw_data.select_dtypes(include=['int64', 'float64']).columns
        outlier_report = {}
        
        for column in numerical_columns:
            Q1 = self.raw_data[column].quantile(0.25)
            Q3 = self.raw_data[column].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            # Count outliers before capping
            outliers_count = len(self.raw_data[(self.raw_data[column] < lower_bound) | 
                                             (self.raw_data[column] > upper_bound)])
            
            # Cap outliers
            self.raw_data[column] = self.raw_data[column].clip(lower=lower_bound, upper=upper_bound)
            
            if outliers_count > 0:
                outlier_report[column] = f"Capped {outliers_count} outliers"
        
        self.preprocessing_report['outliers'] = outlier_report
        
    def scale_features(self) -> None:
        """Scale numerical features using StandardScaler"""
        numerical_columns = self.raw_data.select_dtypes(include=['int64', 'float64']).columns
        numerical_columns = [col for col in numerical_columns if col != 'weakness_level']
        
        scaler = StandardScaler()
        scaled_features = scaler.fit_transform(self.raw_data[numerical_columns])
        
        self.raw_data[numerical_columns] = scaled_features
        self.scalers['standard'] = scaler
        
        self.preprocessing_report['scaled_features'] = list(numerical_columns)
        
    def split_data(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Split data into train and test sets"""
        X = self.raw_data.drop('weakness_level', axis=1)
        y = self.raw_data['weakness_level']
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        train_df = pd.concat([X_train, y_train], axis=1)
        test_df = pd.concat([X_test, y_test], axis=1)
        
        self.preprocessing_report['train_shape'] = train_df.shape
        self.preprocessing_report['test_shape'] = test_df.shape
        
        return train_df, test_df
    
    def save_data(self, train_df: pd.DataFrame, test_df: pd.DataFrame) -> None:
        """Save processed datasets"""
        try:
            # Save to processed data directory
            train_path = PROCESSED_DATA_DIR / f"{self.dataset_name.lower()}_train.csv"
            test_path = PROCESSED_DATA_DIR / f"{self.dataset_name.lower()}_test.csv"
            
            train_df.to_csv(train_path, index=False)
            test_df.to_csv(test_path, index=False)
            
            logging.info(f"Saved processed {self.dataset_name} dataset to {PROCESSED_DATA_DIR}")
            logging.info(f"Train shape: {train_df.shape}, Test shape: {test_df.shape}")
            
        except Exception as e:
            logging.error(f"Error saving processed {self.dataset_name} dataset: {str(e)}")
            raise
        
    def generate_report(self) -> None:
        """Generate preprocessing report"""
        report_file = REPORTS_DIR / f"preprocessing_report_{self.dataset_name.lower()}.txt"
        
        with open(report_file, 'w') as f:
            f.write(f"Preprocessing Report for {self.dataset_name} Dataset\n")
            f.write("=" * 50 + "\n\n")
            
            f.write("1. Data Shapes\n")
            f.write(f"Original: {self.preprocessing_report['original_shape']}\n")
            f.write(f"Train: {self.preprocessing_report['train_shape']}\n")
            f.write(f"Test: {self.preprocessing_report['test_shape']}\n\n")
            
            f.write("2. Missing Values Handled\n")
            for col, action in self.preprocessing_report['missing_values'].items():
                f.write(f"{col}: {action}\n")
            f.write("\n")
            
            f.write("3. Categorical Encoding\n")
            for col, mapping in self.preprocessing_report['encoding'].items():
                f.write(f"{col}: {mapping}\n")
            f.write("\n")
            
            f.write("4. Engineered Features\n")
            for feature in self.preprocessing_report['engineered_features']:
                f.write(f"- {feature}\n")
            f.write("\n")
            
            f.write("5. Target Distribution\n")
            for level, pct in self.preprocessing_report['target_distribution'].items():
                f.write(f"Class {level}: {pct:.1f}%\n")
            f.write("\n")
            
            f.write("6. Outliers Handled\n")
            for col, info in self.preprocessing_report['outliers'].items():
                f.write(f"{col}: {info}\n")
            f.write("\n")
            
            f.write("7. Scaled Features\n")
            for feature in self.preprocessing_report['scaled_features']:
                f.write(f"- {feature}\n")
    
    def preprocess(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Execute full preprocessing pipeline"""
        print(f"\nPreprocessing {self.dataset_name} dataset...")
        
        print("1. Loading data...")
        self.load_data()
        
        print("2. Handling missing values...")
        self.handle_missing_values()
        
        print("3. Encoding categorical variables...")
        self.encode_categorical_variables()
        
        print("4. Engineering features...")
        self.engineer_features()
        
        print("5. Creating target variable...")
        self.create_target_variable()
        
        print("6. Handling outliers...")
        self.handle_outliers()
        
        print("7. Scaling features...")
        self.scale_features()
        
        print("8. Splitting data...")
        train_df, test_df = self.split_data()
        
        print("9. Saving processed data...")
        self.save_data(train_df, test_df)
        
        print("10. Generating preprocessing report...")
        self.generate_report()
        
        return train_df, test_df

def main():
    # Process all three datasets
    datasets = ["UCI", "OU", "AI"]
    
    for dataset_name in datasets:
        preprocessor = DataPreprocessor(dataset_name)
        train_df, test_df = preprocessor.preprocess()
        print(f"\n{dataset_name} dataset preprocessing completed!")
        print(f"Train shape: {train_df.shape}")
        print(f"Test shape: {test_df.shape}")

if __name__ == "__main__":
    main()