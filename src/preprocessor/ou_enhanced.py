from .base import BasePreprocessor
import pandas as pd
import numpy as np
from typing import Tuple, Dict
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from imblearn.over_sampling import SMOTE
import logging

class OUEnhancedPreprocessor(BasePreprocessor):
    def __init__(self):
        super().__init__("OU")
        self.scaler = StandardScaler()
        self.label_encoders = {}
    
    def load_all_data(self):
        """Load and merge all relevant OU dataset files"""
        self.logger.info("Loading all OU datasets...")
        
        ou_dir = self.raw_dir / 'ou_data'
        
        # Load all required datasets with selected columns
        student_info = pd.read_csv(
            ou_dir / 'studentInfo.csv',
            usecols=['id_student', 'gender', 'region', 'highest_education', 'age_band', 'disability']
        )
        
        assessments = pd.read_csv(
            ou_dir / 'assessments.csv',
            usecols=['id_assessment', 'code_module', 'assessment_type', 'date']
        )
        
        student_assessment = pd.read_csv(
            ou_dir / 'studentAssessment.csv',
            usecols=['id_student', 'id_assessment', 'score', 'date_submitted']
        )
        
        courses = pd.read_csv(
            ou_dir / 'courses.csv'
        )
        
        student_registration = pd.read_csv(
            ou_dir / 'studentRegistration.csv',
            usecols=['id_student', 'code_module', 'date_registration', 'date_unregistration']
        )
        
        vle_data = pd.read_csv(
            ou_dir / 'studentVle.csv'
        )
        
        vle_info = pd.read_csv(
            ou_dir / 'vle.csv'
        )
        
        # Merge VLE info with student VLE data
        vle_data = vle_data.merge(vle_info, on=['id_site', 'code_module'], how='left')
        
        # Merge assessment info with student assessment data
        assessment_data = student_assessment.merge(assessments, on='id_assessment', how='left')
        
        # Calculate course-level statistics
        course_stats = self.calculate_course_statistics(assessment_data, vle_data)
        
        # Merge all datasets
        merged_data = student_info.merge(
            student_registration, on='id_student', how='left'
        ).merge(
            assessment_data, on=['id_student', 'code_module'], how='left'
        ).merge(
            course_stats, on='code_module', how='left'
        )
        
        # Add VLE activity features
        vle_features = self.calculate_vle_features(vle_data)
        merged_data = merged_data.merge(vle_features, on='id_student', how='left')
        
        self.report['original_shape'] = merged_data.shape
        self.report['features_before'] = merged_data.columns.tolist()
        
        return merged_data
    
    def calculate_course_statistics(self, assessment_data: pd.DataFrame, 
                                  vle_data: pd.DataFrame) -> pd.DataFrame:
        """Calculate course-level statistics"""
        # Assessment statistics
        assessment_stats = assessment_data.groupby('code_module').agg({
            'score': ['mean', 'std', 'count'],
            'date_submitted': ['min', 'max']
        }).reset_index()
        
        assessment_stats.columns = [
            'code_module', 'course_avg_score', 'course_score_std',
            'total_assessments', 'course_start_date', 'course_end_date'
        ]
        
        # VLE engagement statistics
        vle_stats = vle_data.groupby('code_module').agg({
            'sum_click': ['mean', 'std'],
            'activity_type': lambda x: x.nunique()
        }).reset_index()
        
        vle_stats.columns = [
            'code_module', 'course_avg_clicks', 'course_clicks_std',
            'activity_types_count'
        ]
        
        # Merge course statistics
        course_stats = assessment_stats.merge(vle_stats, on='code_module', how='outer')
        
        return course_stats
    
    def calculate_vle_features(self, vle_data: pd.DataFrame) -> pd.DataFrame:
        """Calculate student-level VLE activity features"""
        # Activity timing patterns
        vle_data['is_weekend'] = pd.to_datetime(vle_data['date']).dt.dayofweek >= 5
        
        vle_features = vle_data.groupby('id_student').agg({
            'sum_click': ['sum', 'mean', 'std'],
            'is_weekend': 'mean',  # Proportion of weekend activity
            'activity_type': lambda x: x.nunique(),  # Diversity of activities
            'date': lambda x: np.ptp(x)  # Time span of activity
        }).reset_index()
        
        vle_features.columns = [
            'id_student', 'total_clicks', 'avg_clicks_per_session',
            'clicks_std', 'weekend_activity_ratio', 'activity_diversity',
            'activity_timespan'
        ]
        
        return vle_features
    
    def create_time_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create time-based features"""
        # Convert date columns to datetime
        date_columns = ['date_submitted', 'date_registration', 'date_unregistration', 'date']
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col].astype(str), errors='coerce')
        
        # Time between registration and first assessment
        if all(col in df.columns for col in ['date_submitted', 'date_registration']):
            first_assessment = df.groupby('id_student')['date_submitted'].min()
            df = df.merge(
                first_assessment.reset_index().rename(
                    columns={'date_submitted': 'first_assessment_date'}
                ),
                on='id_student'
            )
            df['time_to_first_assessment'] = (
                df['first_assessment_date'] - df['date_registration']
            ).dt.total_seconds() / (24 * 3600)  # Convert to days
            
            # Assessment submission patterns
            if 'date' in df.columns:
                df['submission_delay'] = (
                    df['date_submitted'] - pd.to_datetime(df['date'])
                ).dt.total_seconds() / (24 * 3600)  # Convert to days
        
        # Average submission delay per student
        avg_delay = df.groupby('id_student')['submission_delay'].mean()
        df = df.merge(
            avg_delay.reset_index().rename(
                columns={'submission_delay': 'avg_submission_delay'}
            ),
            on='id_student'
        )
        
        return df
    
    def create_behavioral_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create behavioral pattern features"""
        # Study regularity (standard deviation of gaps between activities)
        if 'date' in df.columns:
            def calc_regularity(dates):
                if len(dates) < 2:
                    return 0
                sorted_dates = sorted(dates.dropna())
                if len(sorted_dates) < 2:
                    return 0
                gaps = np.diff(sorted_dates)
                return np.std(gaps.total_seconds() / (24 * 3600))  # Convert to days
            
            activity_gaps = df.groupby('id_student')['date'].apply(calc_regularity)
            df = df.merge(
                activity_gaps.reset_index().rename(
                    columns={'date': 'study_regularity'}
                ),
                on='id_student'
            )
        
        # Engagement consistency
        if 'sum_click' in df.columns:
            def calc_consistency(x):
                if len(x) < 2 or x.mean() == 0:
                    return 0
                return 1 - (x.std() / x.mean())
            
            engagement_consistency = df.groupby('id_student')['sum_click'].agg(calc_consistency)
            df = df.merge(
                engagement_consistency.reset_index().rename(
                    columns={'sum_click': 'engagement_consistency'}
                ),
                on='id_student'
            )
        
        return df
    
    def create_progress_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create progress-tracking features"""
        # Rolling average of last 3 assessments
        recent_scores = df.sort_values('date_submitted').groupby('id_student')['score'].rolling(
            window=3, min_periods=1
        ).mean().reset_index(0, drop=True)
        df['recent_performance'] = recent_scores
        
        # Performance relative to course average
        df['relative_performance'] = df['score'] - df['course_avg_score']
        
        # Performance trend (slope of scores over time)
        def calculate_trend(group):
            if len(group) < 2:
                return 0
            x = np.arange(len(group))
            y = group.values
            slope, _ = np.polyfit(x, y, 1)
            return slope
        
        score_trends = df.sort_values('date_submitted').groupby('id_student')['score'].apply(
            calculate_trend
        )
        df = df.merge(
            score_trends.reset_index().rename(columns={'score': 'score_trend'}),
            on='id_student'
        )
        
        return df
    
    def handle_missing_values_enhanced(self, df: pd.DataFrame) -> pd.DataFrame:
        """Enhanced missing value handling"""
        self.logger.info("Handling missing values with enhanced methods...")
        
        # For numeric columns, fill with median of similar students
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
        for col in numeric_cols:
            if df[col].isnull().any():
                # Group by student characteristics and fill with group median
                df[col] = df.groupby(['gender', 'region'])[col].transform(
                    lambda x: x.fillna(x.median())
                )
                # If still missing, fill with overall median
                df[col] = df[col].fillna(df[col].median())
        
        # For categorical columns, fill with mode
        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            if df[col].isnull().any():
                df[col] = df[col].fillna(df[col].mode()[0])
        
        return df
    
    def handle_outliers_robust(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle outliers using robust methods"""
        self.logger.info("Handling outliers with robust methods...")
        
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
        
        for col in numeric_cols:
            # Skip certain columns
            if col in ['id_student', 'id_assessment', 'weakness_level']:
                continue
                
            # Calculate robust statistics
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 3 * IQR
            upper_bound = Q3 + 3 * IQR
            
            # Cap outliers instead of removing
            df[col] = df[col].clip(lower_bound, upper_bound)
        
        return df
    
    def create_enhanced_weakness_level(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create enhanced weakness level incorporating multiple factors"""
        self.logger.info("Creating enhanced weakness levels...")
        
        # Combine multiple performance indicators
        performance_indicators = [
            'avg_score',
            'recent_performance',
            'relative_performance',
            'engagement_consistency'
        ]
        
        # Ensure all indicators exist
        available_indicators = [col for col in performance_indicators if col in df.columns]
        
        if not available_indicators:
            raise ValueError("No performance indicators available for weakness level calculation")
        
        # Calculate composite score
        df['composite_score'] = df[available_indicators].mean(axis=1)
        
        # Create weakness levels using quartiles
        df['weakness_level'] = pd.qcut(
            df['composite_score'],
            q=3,
            labels=[0, 1, 2]  # 0: High risk, 1: Moderate risk, 2: Low risk
        )
        
        return df
    
    def encode_categorical_enhanced(self, df: pd.DataFrame) -> pd.DataFrame:
        """Enhanced categorical variable encoding"""
        self.logger.info("Performing enhanced categorical encoding...")
        
        # Identify categorical columns
        categorical_cols = df.select_dtypes(include=['object']).columns
        
        for col in categorical_cols:
            # Skip ID columns and target
            if col in ['id_student', 'id_assessment', 'code_module']:
                continue
            
            # Create label encoder for the column
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))
            self.label_encoders[col] = le
            
            # Create frequency encoding
            freq_encoding = df[col].value_counts(normalize=True)
            df[f'{col}_freq'] = df[col].map(freq_encoding)
        
        return df
    
    def select_important_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Select important features based on correlation with target"""
        self.logger.info("Selecting important features...")
        
        # Calculate correlations with target
        correlations = df.corr()['weakness_level'].abs()
        
        # Select features with correlation above threshold
        important_features = correlations[correlations > 0.05].index.tolist()
        
        # Always keep certain columns
        essential_columns = ['id_student', 'weakness_level']
        for col in essential_columns:
            if col not in important_features and col in df.columns:
                important_features.append(col)
        
        return df[important_features]
    
    def split_data_stratified(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Split data with stratification and handle class imbalance"""
        self.logger.info("Splitting data and handling class imbalance...")
        
        # Separate features and target
        X = df.drop(['weakness_level', 'id_student'], axis=1)
        y = df['weakness_level']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Apply SMOTE to training data
        smote = SMOTE(random_state=42)
        X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)
        
        # Reconstruct DataFrames
        train_df = pd.DataFrame(X_train_balanced, columns=X.columns)
        train_df['weakness_level'] = y_train_balanced
        
        test_df = pd.DataFrame(X_test, columns=X.columns)
        test_df['weakness_level'] = y_test
        
        return train_df, test_df
    
    def preprocess(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Main preprocessing pipeline"""
        self.logger.info("Starting enhanced preprocessing pipeline...")
        
        # 1. Load and merge all relevant data
        df = self.load_all_data()
        
        # 2. Handle missing values
        df = self.handle_missing_values_enhanced(df)
        
        # 3. Create features
        df = self.create_time_features(df)
        df = self.create_behavioral_features(df)
        df = self.create_progress_features(df)
        
        # 4. Handle outliers
        df = self.handle_outliers_robust(df)
        
        # 5. Create enhanced target variable
        df = self.create_enhanced_weakness_level(df)
        
        # 6. Encode categorical variables
        df = self.encode_categorical_enhanced(df)
        
        # 7. Select important features
        df = self.select_important_features(df)
        
        # 8. Split data and handle class imbalance
        train_df, test_df = self.split_data_stratified(df)
        
        # Save preprocessing report
        self.report['final_shape'] = train_df.shape
        self.report['features_after'] = train_df.columns.tolist()
        self.save_report()
        
        return train_df, test_df