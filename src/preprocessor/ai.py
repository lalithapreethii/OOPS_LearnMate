"""
Fixed AI Preprocessor - Prevents temporal data leakage
Only uses information available BEFORE the prediction point
"""

from .base import BasePreprocessor
import pandas as pd
import numpy as np
from typing import Tuple
from sklearn.model_selection import train_test_split

class AIPreprocessor(BasePreprocessor):
    def __init__(self, prediction_point='midterm'):
        """
        Initialize AI preprocessor
        
        Args:
            prediction_point: When to make the prediction
                            - 'early': After Quiz 1 only
                            - 'midterm': After Midterm (includes Quiz 1 + Midterm)
                            - 'late': After all but Final (Quiz + Midterm + Assignments)
        """
        super().__init__("AI")
        self.prediction_point = prediction_point
        self.logger.info(f"Initialized AI preprocessor with prediction point: {prediction_point}")
    
    def load_data(self):
        """Load AI Course Performance Dataset"""
        self.logger.info("Loading AI Course dataset...")
        
        ai_dir = self.raw_dir / 'ai_course_data'
        ai_file = ai_dir / 'Student Performance Dataset in AI course' / 'Stu_Performance_dataset.csv'
        
        self.raw_data = pd.read_csv(ai_file)
        self.report['original_shape'] = self.raw_data.shape
        self.report['features_before'] = self.raw_data.columns.tolist()
        self.report['prediction_point'] = self.prediction_point
        
        return self.raw_data
    
    def feature_engineering(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create features using ONLY assessments before prediction point
        CRITICAL: No future data leakage
        """
        self.logger.info(f"Performing temporal-aware feature engineering at '{self.prediction_point}' point...")
        
        # ============================================================
        # TEMPORAL VALIDATION: Define available assessments
        # ============================================================
        
        # Define temporal ordering of assessments
        assessment_timeline = {
            'Quiz ': 1,
            'Assignment_1': 2,
            'Midterm': 3,
            'Assignment_2': 4,
            'Assignment_3': 5,
            'Project': 6,
            'Presentation': 7,
            'Final_Exam': 8
        }
        
        # Determine which assessments are available
        if self.prediction_point == 'early':
            # Only Quiz 1 available
            available_assessments = ['Quiz ']
            target_assessments = ['Midterm', 'Final_Exam']  # What we're predicting
            self.logger.info("Early prediction: Using only Quiz 1")
        
        elif self.prediction_point == 'midterm':
            # Quiz 1 + Midterm + Assignment 1 available
            available_assessments = ['Quiz ', 'Assignment_1', 'Midterm']
            target_assessments = ['Assignment_2', 'Assignment_3', 'Project', 
                                 'Presentation', 'Final_Exam']
            self.logger.info("Midterm prediction: Using Quiz 1, Assignment 1, Midterm")
        
        elif self.prediction_point == 'late':
            # Everything except Final Exam
            available_assessments = ['Quiz ', 'Assignment_1', 'Midterm', 
                                    'Assignment_2', 'Assignment_3', 
                                    'Project', 'Presentation']
            target_assessments = ['Final_Exam']
            self.logger.info("Late prediction: Using all except Final Exam")
        
        else:
            raise ValueError(f"Invalid prediction_point: {self.prediction_point}")
        
        # ============================================================
        # 1. CURRENT PERFORMANCE METRICS (Only from available assessments)
        # ============================================================
        
        # Average score from available assessments
        df['current_avg_score'] = df[available_assessments].mean(axis=1)
        
        # Performance consistency (standard deviation)
        if len(available_assessments) > 1:
            df['performance_consistency'] = df[available_assessments].std(axis=1)
        else:
            df['performance_consistency'] = 0  # No variance with single assessment
        
        # Current performance level (0-100 normalized to 0-1)
        df['current_performance_level'] = df['current_avg_score'] / 100.0
        
        # ============================================================
        # 2. ASSESSMENT-SPECIFIC PERFORMANCE
        # ============================================================
        
        # Identify available assessment types
        available_quizzes = [a for a in available_assessments if 'Quiz' in a]
        available_assignments = [a for a in available_assessments if 'Assignment' in a]
        available_exams = [a for a in available_assessments if 'Midterm' in a or 'Exam' in a]
        
        # Quiz performance (if available)
        if available_quizzes:
            df['quiz_performance'] = df[available_quizzes].mean(axis=1) / 100.0
        else:
            df['quiz_performance'] = 0
        
        # Assignment performance (if available)
        if available_assignments:
            df['assignment_performance'] = df[available_assignments].mean(axis=1) / 100.0
            if len(available_assignments) > 1:
                df['assignment_consistency'] = df[available_assignments].std(axis=1)
            else:
                df['assignment_consistency'] = 0
        else:
            df['assignment_performance'] = 0
            df['assignment_consistency'] = 0
        
        # Exam performance (if available)
        if available_exams:
            df['exam_performance'] = df[available_exams].mean(axis=1) / 100.0
        else:
            df['exam_performance'] = 0
        
        # ============================================================
        # 3. LEARNING PROGRESSION (Only from available data)
        # ============================================================
        
        if len(available_assessments) >= 2:
            # Calculate trend across available assessments
            def calc_trend(row):
                try:
                    scores = [row[a] for a in available_assessments]
                    x = np.arange(len(scores))
                    slope = np.polyfit(x, scores, deg=1)[0] if len(scores) > 1 else 0
                    return slope
                except:
                    return 0
            
            df['score_progression'] = df.apply(calc_trend, axis=1)
            
            # Improvement from first to latest available
            df['overall_improvement'] = (
                df[available_assessments[-1]] - df[available_assessments[0]]
            )
            
            # Improvement rate (normalized by number of assessments)
            df['improvement_rate'] = df['overall_improvement'] / len(available_assessments)
        
        else:
            df['score_progression'] = 0
            df['overall_improvement'] = 0
            df['improvement_rate'] = 0
        
        # ============================================================
        # 4. PERFORMANCE PATTERNS
        # ============================================================
        
        # Volatility (max - min of available scores)
        df['score_volatility'] = (
            df[available_assessments].max(axis=1) - 
            df[available_assessments].min(axis=1)
        )
        
        # Relative performance (percentile within class)
        for assessment in available_assessments:
            df[f'{assessment}_percentile'] = df[assessment].rank(pct=True)
        
        # Average percentile rank
        percentile_cols = [f'{a}_percentile' for a in available_assessments]
        df['avg_percentile_rank'] = df[percentile_cols].mean(axis=1)
        
        # Rank consistency (std of percentiles)
        if len(available_assessments) > 1:
            df['rank_consistency'] = df[percentile_cols].std(axis=1)
        else:
            df['rank_consistency'] = 0
        
        # ============================================================
        # 5. PERFORMANCE CATEGORIES
        # ============================================================
        
        # Theory vs Practical (if we have both types)
        theory_assessments = [a for a in available_assessments if 'Quiz' in a or 'Midterm' in a or 'Exam' in a]
        practical_assessments = [a for a in available_assessments if 'Assignment' in a or 'Project' in a]
        
        if theory_assessments:
            df['theory_score'] = df[theory_assessments].mean(axis=1) / 100.0
        else:
            df['theory_score'] = 0
        
        if practical_assessments:
            df['practical_score'] = df[practical_assessments].mean(axis=1) / 100.0
        else:
            df['practical_score'] = 0
        
        # Learning style indicator
        if theory_assessments and practical_assessments:
            df['theory_vs_practical'] = df['theory_score'] - df['practical_score']
            df['theoretical_strength'] = (df['theory_score'] > df['practical_score']).astype(int)
        else:
            df['theory_vs_practical'] = 0
            df['theoretical_strength'] = 0
        
        # ============================================================
        # 6. RISK INDICATORS (Based on current performance)
        # ============================================================
        
        # Performance risk (below median)
        median_score = df['current_avg_score'].median()
        df['performance_risk'] = (df['current_avg_score'] < median_score).astype(int)
        
        # Consistency risk (high volatility)
        median_volatility = df['score_volatility'].median()
        df['consistency_risk'] = (df['score_volatility'] > median_volatility).astype(int)
        
        # Progression risk (negative trend)
        if 'score_progression' in df.columns:
            df['progression_risk'] = (df['score_progression'] < 0).astype(int)
        else:
            df['progression_risk'] = 0
        
        # Comprehensive risk score
        df['comprehensive_risk_score'] = (
            df['performance_risk'] * 0.5 +
            df['consistency_risk'] * 0.3 +
            df['progression_risk'] * 0.2
        )
        
        # ============================================================
        # 7. STRENGTH INDICATORS
        # ============================================================
        
        # High performer (top 25th percentile)
        top_25_threshold = df['current_avg_score'].quantile(0.75)
        df['high_performer'] = (df['current_avg_score'] >= top_25_threshold).astype(int)
        
        # Consistent performer (low volatility)
        low_volatility_threshold = df['score_volatility'].quantile(0.25)
        df['consistent_performer'] = (df['score_volatility'] <= low_volatility_threshold).astype(int)
        
        # Improving student (positive trend)
        if 'score_progression' in df.columns:
            df['improving_student'] = (df['score_progression'] > 0).astype(int)
        else:
            df['improving_student'] = 0
        
        # ============================================================
        # 8. NORMALIZED PERFORMANCE METRICS
        # ============================================================
        
        # Z-scores for current performance (how far from mean)
        df['performance_zscore'] = (
            (df['current_avg_score'] - df['current_avg_score'].mean()) / 
            (df['current_avg_score'].std() + 1e-10)  # Avoid division by zero
        )
        
        # Distance from passing threshold (assuming 60 is passing)
        df['distance_from_passing'] = (df['current_avg_score'] - 60) / 100.0
        
        # ============================================================
        # CRITICAL: Store target and drop ALL assessment columns
        # ============================================================
        
        # Calculate target from Total or remaining assessments
        if 'Total' in df.columns:
            df['target_score'] = df['Total']
        else:
            # If Total not available, calculate from all assessments
            all_assessments = list(assessment_timeline.keys())
            df['target_score'] = df[[a for a in all_assessments if a in df.columns]].sum(axis=1)
        
        # Drop ALL original assessment columns to prevent leakage
        columns_to_drop = (available_assessments + target_assessments + 
                          ['Total', 'Grade', 'Categories'])
        df = df.drop(columns=[col for col in columns_to_drop if col in df.columns], 
                    errors='ignore')
        
        # Also drop percentile columns (they were intermediate calculations)
        df = df.drop(columns=[col for col in df.columns if '_percentile' in col], 
                    errors='ignore')
        
        self.logger.info(f"Feature engineering complete. Total features: {df.shape[1]}")
        self.logger.info(f"Available assessments used: {available_assessments}")
        
        return df
    
    def preprocess(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Preprocess AI dataset with temporal validation"""
        
        # Step 1: Load data
        df = self.load_data()
        
        # Step 2: Handle missing values
        df = self.handle_missing_values(df)
        
        # Step 3: Feature engineering (temporal-aware)
        df = self.feature_engineering(df)
        
        # Step 4: Create target variable from stored score
        df = self.create_weakness_level(df, 'target_score')
        
        # Drop target_score column
        df = df.drop(columns=['target_score'], errors='ignore')
        
        # Step 5: Encode categorical variables
        df = self.encode_categorical(df)
        
        # Step 6: Handle outliers
        numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
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
        
        self.logger.info("✅ AI preprocessing complete with temporal validation")
        
        return train_df, test_df