"""
Fixed UCI Preprocessor - Prevents temporal data leakage
Only uses information available BEFORE the prediction point
"""

from .base import BasePreprocessor
import pandas as pd
import numpy as np
from typing import Tuple
from sklearn.model_selection import train_test_split

class UCIPreprocessor(BasePreprocessor):
    def __init__(self, prediction_grade='G2'):
        """
        Initialize UCI preprocessor
        
        Args:
            prediction_grade: Which grade to predict ('G2' or 'G3')
                            - 'G2': Uses only G1 for features (early prediction)
                            - 'G3': Uses G1 and G2 for features (mid-term prediction)
        """
        super().__init__("UCI")
        self.prediction_grade = prediction_grade
        self.logger.info(f"Initialized UCI preprocessor with prediction target: {prediction_grade}")
    
    def load_data(self):
        """Load UCI Student Performance Dataset"""
        self.logger.info("Loading UCI dataset...")
        
        # Load math and portuguese datasets
        uci_dir = self.raw_dir / 'uci_data'
        math_path = uci_dir / "student-mat.csv"
        por_path = uci_dir / "student-por.csv"
        
        math_df = pd.read_csv(math_path, sep=';')
        por_df = pd.read_csv(por_path, sep=';')
        
        # Add subject identifier
        math_df['subject'] = 'math'
        por_df['subject'] = 'portuguese'
        
        # Combine datasets
        self.raw_data = pd.concat([math_df, por_df], ignore_index=True)
        self.report['original_shape'] = self.raw_data.shape
        self.report['features_before'] = self.raw_data.columns.tolist()
        self.report['prediction_target'] = self.prediction_grade
        
        return self.raw_data
    
    def feature_engineering(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create features using ONLY information available before prediction point
        CRITICAL: No future data leakage
        """
        self.logger.info(f"Performing temporal-aware feature engineering for {self.prediction_grade} prediction...")
        
        # ============================================================
        # TEMPORAL VALIDATION: Define what grades we can use
        # ============================================================
        if self.prediction_grade == 'G2':
            # Early prediction: Only use G1 (first period grade)
            available_grades = ['G1']
            target_grade = 'G2'
            self.logger.info("Early prediction mode: Using only G1 for features")
        elif self.prediction_grade == 'G3':
            # Mid-term prediction: Can use G1 and G2
            available_grades = ['G1', 'G2']
            target_grade = 'G3'
            self.logger.info("Mid-term prediction mode: Using G1 and G2 for features")
        else:
            raise ValueError(f"Invalid prediction_grade: {self.prediction_grade}")
        
        # ============================================================
        # 1. GRADE-BASED FEATURES (Only from available grades)
        # ============================================================
        
        if len(available_grades) == 1:
            # Only G1 available
            df['current_score'] = df['G1']
            df['score_trend'] = 0  # No trend with single grade
            df['performance_consistency'] = 0  # No variance with single grade
        else:
            # G1 and G2 available
            df['current_score'] = df[available_grades].mean(axis=1)
            df['score_trend'] = df['G2'] - df['G1']
            df['performance_consistency'] = df[available_grades].std(axis=1)
        
        # Performance level (normalized to 0-1)
        df['current_performance_level'] = df['current_score'] / 20.0  # Grades are 0-20
        
        # ============================================================
        # 2. DEMOGRAPHIC & STATIC FEATURES (Always available)
        # ============================================================
        
        # Family education level
        df['family_education'] = (df['Medu'] + df['Fedu']) / 2
        df['parent_education_gap'] = abs(df['Medu'] - df['Fedu'])
        
        # Family structure
        df['family_size_num'] = df['famsize'].map({'LE3': 0, 'GT3': 1})
        df['parent_status_num'] = df['Pstatus'].map({'T': 1, 'A': 0})
        
        # Urban vs rural
        df['urban'] = df['address'].map({'U': 1, 'R': 0})
        
        # ============================================================
        # 3. BEHAVIORAL FEATURES (Always available)
        # ============================================================
        
        # Study habits
        df['study_efficiency'] = df['studytime'] / (df['traveltime'] + 1)  # Avoid division by zero
        df['time_management'] = df['studytime'] / (df['freetime'] + 1)
        
        # Attendance quality
        df['attendance_rate'] = 1 - (df['absences'] / (df['absences'].max() + 1))
        
        # Past academic history
        df['has_failures'] = (df['failures'] > 0).astype(int)
        df['failure_count'] = df['failures']
        
        # ============================================================
        # 4. SUPPORT SYSTEM FEATURES (Always available)
        # ============================================================
        
        # Educational support
        df['school_support'] = df['schoolsup'].map({'yes': 1, 'no': 0})
        df['family_support'] = df['famsup'].map({'yes': 1, 'no': 0})
        df['paid_classes'] = df['paid'].map({'yes': 1, 'no': 0})
        df['total_support'] = df['school_support'] + df['family_support'] + df['paid_classes']
        
        # Family support quality
        df['family_relationship_quality'] = df['famrel'] / 5.0  # Normalize to 0-1
        df['family_support_score'] = (
            df['family_relationship_quality'] * 0.5 +
            df['family_support'] * 0.3 +
            (df['family_education'] / 4.0) * 0.2  # Normalize to 0-1
        )
        
        # School support score
        df['school_support_score'] = (
            df['school_support'] * 0.4 +
            df['paid_classes'] * 0.3 +
            (df['studytime'] / 4.0) * 0.3  # Normalize to 0-1
        )
        
        # Overall support system
        df['support_system_strength'] = (
            df['family_support_score'] * 0.6 +
            df['school_support_score'] * 0.4
        )
        
        # ============================================================
        # 5. SOCIAL & LIFESTYLE FEATURES (Always available)
        # ============================================================
        
        # Social activities
        df['social_activity_level'] = df['goout'] / 5.0  # Normalize
        df['romantic_relationship'] = df['romantic'].map({'yes': 1, 'no': 0})
        
        # Alcohol consumption
        df['workday_alcohol'] = df['Dalc'] / 5.0  # Normalize
        df['weekend_alcohol'] = df['Walc'] / 5.0  # Normalize
        df['avg_alcohol_consumption'] = (df['workday_alcohol'] + df['weekend_alcohol']) / 2
        
        # Social-academic balance
        df['social_study_balance'] = df['studytime'] / (df['goout'] + 1)
        df['free_time_management'] = df['studytime'] / (df['freetime'] + 1)
        
        # ============================================================
        # 6. HEALTH & WELLBEING (Always available)
        # ============================================================
        
        df['health_status'] = df['health'] / 5.0  # Normalize to 0-1
        df['health_risk'] = 1 - df['health_status']  # Invert (higher = more risk)
        
        # ============================================================
        # 7. MOTIVATIONAL FACTORS (Always available)
        # ============================================================
        
        df['wants_higher_education'] = df['higher'].map({'yes': 1, 'no': 0})
        df['has_internet'] = df['internet'].map({'yes': 1, 'no': 0})
        df['has_nursery'] = df['nursery'].map({'yes': 1, 'no': 0})
        
        # Educational aspiration
        df['educational_aspiration'] = (
            df['wants_higher_education'] * 0.6 +
            (df['family_education'] / 4.0) * 0.4
        )
        
        # ============================================================
        # 8. RISK INDICATORS (Composite scores)
        # ============================================================
        
        # Academic risk factors
        df['academic_risk'] = (
            (df['failure_count'] / 4.0) * 0.4 +  # Normalize and weight
            (1 - df['studytime'] / 4.0) * 0.3 +  # Low study time
            (df['absences'] / (df['absences'].max() + 1)) * 0.3  # High absences
        )
        
        # Social risk factors
        df['social_risk'] = (
            df['avg_alcohol_consumption'] * 0.4 +
            (1 - df['family_relationship_quality']) * 0.3 +
            (df['social_activity_level'] > 0.8).astype(int) * 0.3  # Excessive socializing
        )
        
        # Environmental risk factors
        df['environmental_risk'] = (
            (1 - df['support_system_strength']) * 0.5 +
            (1 - df['has_internet']) * 0.25 +
            (1 - df['urban']) * 0.25
        )
        
        # Comprehensive psychosocial risk score
        df['psychosocial_risk_score'] = (
            df['academic_risk'] * 0.4 +
            df['social_risk'] * 0.3 +
            df['environmental_risk'] * 0.2 +
            df['health_risk'] * 0.1
        )
        
        # ============================================================
        # 9. INTERACTION FEATURES
        # ============================================================
        
        # Study support interaction
        df['internet_study_effect'] = df['has_internet'] * df['studytime']
        
        # Family education effect on support
        df['education_support_interaction'] = df['family_education'] * df['family_support_score']
        
        # Age-related maturity
        df['age_maturity'] = (df['age'] - 15) / 7  # Normalize age range (15-22)
        
        # ============================================================
        # CRITICAL: Remove ALL grade columns except target
        # ============================================================
        
        # Store target and create weakness levels
        df['target_grade'] = df[target_grade]
        df = self.create_weakness_levels(df, 'target_grade')
        
        # Drop ALL original grade columns to prevent leakage
        df = df.drop(columns=['G1', 'G2', 'G3', 'target_grade'], errors='ignore')
        
        self.logger.info(f"Feature engineering complete. Total features created: {df.shape[1]}")
        self.logger.info(f"Target variable: {target_grade}")
        
        return df
    
    def preprocess(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Preprocess UCI dataset with temporal validation"""
        
        # Step 1: Load data
        df = self.load_data()
        
        # Step 2: Handle missing values
        df = self.handle_missing_values(df)
        
        # Step 3: Feature engineering (temporal-aware)
        df = self.feature_engineering(df)  # This already creates weakness_level
        
        # Step 5: Encode categorical variables
        df = self.encode_categorical(df)
        
        # Step 6: Handle outliers
        numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
        # Don't apply outlier handling to weakness_level
        numeric_columns = [col for col in numeric_columns if col != 'weakness_level']
        df = self.handle_outliers(df, numeric_columns)
        
        # Step 7: Train-test split (stratified)
        train_df, test_df = train_test_split(
            df,
            test_size=0.2,
            random_state=42,
            stratify=df['weakness_level']
        )
        
        self.logger.info(f"Train set: {len(train_df)} samples")
        self.logger.info(f"Test set: {len(test_df)} samples")
        
        # Step 8: Scale features
        numeric_columns = train_df.select_dtypes(include=['float64', 'int64']).columns
        # Don't scale the target variable
        numeric_columns = [col for col in numeric_columns if col != 'weakness_level']
        train_df, test_df = self.scale_features(train_df, test_df, numeric_columns)
        
        # Update report
        self.report['final_shape'] = df.shape
        self.report['features_after'] = [col for col in df.columns if col != 'weakness_level']
        
        # Class distribution
        self.report['class_distribution'] = {
            'train': train_df['weakness_level'].value_counts().to_dict(),
            'test': test_df['weakness_level'].value_counts().to_dict()
        }
        
        # Save processed data and report
        self.save_data(train_df, test_df)
        self.save_report()
        
        self.logger.info("✅ UCI preprocessing complete with temporal validation")
        
        return train_df, test_df