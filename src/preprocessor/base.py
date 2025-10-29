import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import json
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import logging
import json
from typing import Tuple, Dict, List, Any
from sklearn.model_selection import train_test_split

class BasePreprocessor:
    """Base class for all dataset preprocessors"""
    
    def __init__(self, dataset_name: str):
        self.dataset_name = dataset_name
        self.raw_data = None
        self.processed_data = None
        self.train_data = None
        self.test_data = None
        self.scalers = {}
        self.encoders = {}
        
        # Define common weakness thresholds
        self.weakness_thresholds = {
            'strong': 0.75,  # Above 75th percentile
            'moderate': 0.25  # Below 25th percentile is weak
        }
        self.report = {
            'dataset_name': dataset_name,
            'original_shape': None,
            'final_shape': None,
            'features_before': None,
            'features_after': None,
            'missing_values': {},
            'encoding_mappings': {},
            'scaling_params': {},
            'class_distribution': {}
        }
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(f"{dataset_name}Preprocessor")
        
        # Setup paths
        self.base_dir = Path(__file__).parent.parent.parent
        self.raw_dir = self.base_dir / 'data' / 'raw'
        self.processed_dir = self.base_dir / 'data' / 'processed'
        self.reports_dir = self.base_dir / 'reports'
        
        # Create directories if they don't exist
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        self.reports_dir.mkdir(parents=True, exist_ok=True)
    
    def create_weakness_levels(self, df: pd.DataFrame, score_column: str) -> pd.DataFrame:
        """Create weakness levels based on performance scores"""
        self.logger.info("Creating weakness level target...")
        
        # Calculate percentile ranks
        ranks = df[score_column].rank(pct=True)
        
        # Create weakness levels (0: Weak, 1: Moderate, 2: Strong)
        conditions = [
            (ranks >= self.weakness_thresholds['strong']),  # Strong
            (ranks >= self.weakness_thresholds['moderate']) & (ranks < self.weakness_thresholds['strong']),  # Moderate
            (ranks < self.weakness_thresholds['moderate'])  # Weak
        ]
        choices = [2, 1, 0]
        
        df['weakness_level'] = np.select(conditions, choices, default=1)
        
        # Log distribution
        dist = df['weakness_level'].value_counts()
        self.logger.info(f"Weakness level distribution:\n{dist}")
        self.report['class_distribution'] = dist.to_dict()
        
        return df
    
    def handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle missing values using median for numerical and mode for categorical"""
        self.logger.info("Handling missing values...")
        
        for column in df.columns:
            missing_count = df[column].isnull().sum()
            if missing_count > 0:
                missing_percentage = (missing_count / len(df)) * 100
                self.report['missing_values'][column] = {
                    'count': int(missing_count),
                    'percentage': round(missing_percentage, 2)
                }
                
                # Drop column if more than 50% missing
                if missing_percentage > 50:
                    self.logger.warning(f"Dropping column {column} with {missing_percentage:.2f}% missing values")
                    df = df.drop(columns=[column])
                    continue
                
                # Impute based on data type
                if pd.api.types.is_numeric_dtype(df[column]):
                    median_value = df[column].median()
                    df[column] = df[column].fillna(median_value)
                    self.logger.info(f"Imputed {column} with median: {median_value}")
                else:
                    mode_value = df[column].mode()[0]
                    df[column] = df[column].fillna(mode_value)
                    self.logger.info(f"Imputed {column} with mode: {mode_value}")
        
        return df
    
    def encode_categorical(self, df: pd.DataFrame) -> pd.DataFrame:
        """Encode categorical variables using Label and One-Hot encoding"""
        self.logger.info("Encoding categorical variables...")
        
        # Identify categorical columns
        categorical_columns = df.select_dtypes(include=['object']).columns
        
        for column in categorical_columns:
            # Binary categories (2 unique values)
            if df[column].nunique() == 2:
                if column not in self.encoders:
                    self.encoders[column] = LabelEncoder()
                    df[column] = self.encoders[column].fit_transform(df[column])
                else:
                    df[column] = self.encoders[column].transform(df[column])
                
                self.report['encoding_mappings'][column] = {
                    'type': 'label',
                    'mapping': dict(zip(
                        self.encoders[column].classes_,
                        self.encoders[column].transform(self.encoders[column].classes_)
                    ))
                }
            
            # Multi-class categories
            else:
                dummies = pd.get_dummies(df[column], prefix=column, drop_first=True)
                df = pd.concat([df, dummies], axis=1)
                df = df.drop(columns=[column])
                
                self.report['encoding_mappings'][column] = {
                    'type': 'one-hot',
                    'generated_columns': dummies.columns.tolist()
                }
        
        return df
    
    def handle_outliers(self, df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """Cap outliers using IQR method"""
        self.logger.info("Handling outliers...")
        
        for column in columns:
            if column in df.columns and pd.api.types.is_numeric_dtype(df[column]):
                Q1 = df[column].quantile(0.25)
                Q3 = df[column].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                # Cap outliers
                df[column] = df[column].clip(lower=lower_bound, upper=upper_bound)
                
                self.logger.info(f"Capped outliers in {column}: [{lower_bound:.2f}, {upper_bound:.2f}]")
        
        return df
    
    def scale_features(self, train_df: pd.DataFrame, test_df: pd.DataFrame, 
                      columns: List[str]) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Scale numerical features using StandardScaler"""
        self.logger.info("Scaling numerical features...")
        
        for column in columns:
            if column in train_df.columns and pd.api.types.is_numeric_dtype(train_df[column]):
                if column not in self.scalers:
                    self.scalers[column] = StandardScaler()
                    train_df[column] = self.scalers[column].fit_transform(train_df[[column]])
                    test_df[column] = self.scalers[column].transform(test_df[[column]])
                else:
                    train_df[column] = self.scalers[column].transform(train_df[[column]])
                    test_df[column] = self.scalers[column].transform(test_df[[column]])
                
                self.report['scaling_params'][column] = {
                    'mean': float(self.scalers[column].mean_),
                    'scale': float(self.scalers[column].scale_)
                }
        
        return train_df, test_df
    
    def create_weakness_level(self, df: pd.DataFrame, score_column: str) -> pd.DataFrame:
        """Create 3-class target variable"""
        self.logger.info("Creating weakness level target...")
        
        df['weakness_level'] = pd.cut(
            df[score_column],
            bins=[-np.inf, 60, 80, np.inf],
            labels=[0, 1, 2]
        )
        
        return df
    
    def save_data(self, train_df: pd.DataFrame, test_df: pd.DataFrame):
        """Save processed train and test data"""
        train_path = self.processed_dir / f"{self.dataset_name}_train.csv"
        test_path = self.processed_dir / f"{self.dataset_name}_test.csv"
        
        train_df.to_csv(train_path, index=False)
        test_df.to_csv(test_path, index=False)
        
        self.logger.info(f"Saved processed data to {train_path} and {test_path}")
    
    def save_report(self):
        """Save preprocessing report"""
        report_path = self.reports_dir / f"{self.dataset_name}_preprocessing_report.json"
        
        # Convert all values to JSON serializable format
        def convert_to_serializable(obj):
            if isinstance(obj, dict):
                return {str(k): convert_to_serializable(v) for k, v in obj.items()}
            elif isinstance(obj, (list, tuple)):
                return [convert_to_serializable(item) for item in obj]
            elif isinstance(obj, (np.int64, np.float64)):
                return float(obj)
            else:
                return obj
        
        json_report = convert_to_serializable(self.report)
        
        with open(report_path, 'w') as f:
            json.dump(json_report, f, indent=4)
        
        self.logger.info(f"Saved preprocessing report to {report_path}")
    
    def plot_distributions(self, original_df: pd.DataFrame, processed_df: pd.DataFrame, 
                         columns: List[str], save_path: Path):
        """Plot before/after distributions for specified columns"""
        self.logger.info("Plotting distributions...")
        
        n_cols = len(columns)
        fig, axes = plt.subplots(n_cols, 2, figsize=(15, 5*n_cols))
        fig.suptitle('Feature Distributions: Before vs After Preprocessing')
        
        for i, column in enumerate(columns):
            if column in original_df.columns:
                # Before preprocessing
                sns.histplot(data=original_df, x=column, ax=axes[i, 0])
                axes[i, 0].set_title(f'{column} - Before')
                
            if column in processed_df.columns:
                # After preprocessing
                sns.histplot(data=processed_df, x=column, ax=axes[i, 1])
                axes[i, 1].set_title(f'{column} - After')
        
        plt.tight_layout()
        plt.savefig(save_path)
        plt.close()
        
        self.logger.info(f"Saved distribution plots to {save_path}")
    
    def preprocess(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Main preprocessing method to be implemented by child classes"""
        raise NotImplementedError("Preprocess method must be implemented by child classes")