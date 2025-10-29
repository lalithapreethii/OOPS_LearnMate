from .base import BasePreprocessor
import pandas as pd
import numpy as np
<<<<<<< HEAD
from typing import Tuple, Dict
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import logging

class OUPreprocessor(BasePreprocessor):
    def __init__(self, prediction_week=8):
        """
        Initialize preprocessor with temporal cutoff
        
        Args:
            prediction_week: Week number to make prediction at (default: 8)
                           Only data UP TO this week will be used
        """
        super().__init__("OU")
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.prediction_week = prediction_week
        self.logger.info(f"Prediction point set at Week {prediction_week}")
        self.prediction_week = prediction_week
        self.logger.info(f"Prediction point set at Week {prediction_week}")
        
    def load_data(self):
        """Load and merge all relevant OU dataset files"""
        self.logger.info("Loading all OU datasets...")
        
        ou_dir = self.raw_dir / 'ou_data'
        
        # Load student information - ONLY demographics (no final_result!)
        student_info = pd.read_csv(
            ou_dir / 'studentInfo.csv',
            usecols=['id_student', 'gender', 'region', 'highest_education', 
                    'age_band', 'disability']
            # ❌ REMOVED: 'final_result' - this is the outcome, not a predictor!
        )
        
        # Load assessments data
        assessments = pd.read_csv(
            ou_dir / 'assessments.csv'
        )
        
        # Load student assessment data
        student_assessment = pd.read_csv(
            ou_dir / 'studentAssessment.csv'
        )
        
        # ✅ CRITICAL: Filter assessments to ONLY those before prediction week
        assessments['week'] = assessments['date'] / 7  # Convert days to weeks
        early_assessments = assessments[assessments['week'] <= self.prediction_week]
        
        # Filter student submissions to only early assessments
        early_assessment_ids = early_assessments['id_assessment'].unique()
        student_assessment = student_assessment[
            student_assessment['id_assessment'].isin(early_assessment_ids)
        ]
        
        self.logger.info(f"Using {len(early_assessment_ids)} assessments before week {self.prediction_week}")
        
        # Load student registration data
        student_registration = pd.read_csv(
            ou_dir / 'studentRegistration.csv'
        )
        
        # Load VLE data
        vle_data = pd.read_csv(
            ou_dir / 'studentVle.csv'
        )
        
        # ✅ CRITICAL: Filter VLE data to ONLY before prediction week
        vle_cutoff_date = self.prediction_week * 7  # Convert weeks to days
        vle_data = vle_data[vle_data['date'] <= vle_cutoff_date]
        
        self.logger.info(f"Using VLE data up to day {vle_cutoff_date} (week {self.prediction_week})")
        
        # Load VLE activity types
        vle_info = pd.read_csv(
            ou_dir / 'vle.csv'
        )
        
        # Load actual outcomes for TARGET VARIABLE ONLY (not as feature!)
        outcomes = pd.read_csv(
            ou_dir / 'studentInfo.csv',
            usecols=['id_student', 'final_result']
        )
        
        # Process and merge data
        self.raw_data = self._process_and_merge_data(
            student_info, 
            early_assessments,  # ✅ Using filtered assessments
            student_assessment,
            student_registration,
            vle_data,  # ✅ Using filtered VLE data
            vle_info,
            outcomes
        )
        
        # Record initial shape and features
        self.report['original_shape'] = self.raw_data.shape
        self.report['features_before'] = self.raw_data.columns.tolist()
        self.report['prediction_week'] = self.prediction_week
        
        return self.raw_data
    
    def _process_and_merge_data(
        self, 
        student_info: pd.DataFrame,
        assessments: pd.DataFrame,
        student_assessment: pd.DataFrame,
        student_registration: pd.DataFrame,
        vle_data: pd.DataFrame,
        vle_info: pd.DataFrame,
        outcomes: pd.DataFrame
    ) -> pd.DataFrame:
        """Process and merge all data sources"""
        
        # 1. Process assessment data (EARLY ONLY)
        assessment_features = self._process_assessment_data(
            assessments, student_assessment
        )
        
        # 2. Process VLE data (EARLY ONLY)
        vle_features = self._process_vle_data(
            vle_data, vle_info
        )
        
        # 3. Process registration data (SAFE - no future info)
        registration_features = self._process_registration_data(
            student_registration
        )
        
        # 4. Merge all data
        final_data = student_info.merge(
            assessment_features,
            on='id_student',
            how='left'
        ).merge(
            vle_features,
            on='id_student',
            how='left'
        ).merge(
            registration_features,
            on='id_student',
            how='left'
        ).merge(
            outcomes,  # ✅ Merge outcomes LAST for target creation only
            on='id_student',
            how='left'
        )
        
        return final_data
    
    def _process_assessment_data(
        self,
        assessments: pd.DataFrame,
        student_assessment: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Process EARLY assessment data only
        NOTE: All data here is from BEFORE the prediction week
        """
        
        # Merge assessment details with student submissions
        assessment_data = student_assessment.merge(
            assessments,
            on='id_assessment',
            how='left'
        )
        
        # ✅ SAFETY CHECK: Verify no future data
        if 'week' in assessment_data.columns:
            max_week = assessment_data['week'].max()
            if max_week > self.prediction_week:
                self.logger.warning(f"Found assessments after week {self.prediction_week}! Filtering...")
                assessment_data = assessment_data[assessment_data['week'] <= self.prediction_week]
        
        # Skip students with no early assessments
        student_counts = assessment_data.groupby('id_student').size()
        valid_students = student_counts[student_counts > 0].index
        assessment_data = assessment_data[assessment_data['id_student'].isin(valid_students)]
        
        # 1. Early Performance Metrics
        base_metrics = assessment_data.groupby('id_student').agg({
            'score': ['mean', 'std', 'count', 'min', 'max'],
            'weight': ['mean', 'sum'],
            'is_banked': 'sum'
        }).reset_index()
        
        base_metrics.columns = [
            'id_student',
            'early_avg_score',
            'early_score_std',
            'early_assessment_count',
            'early_min_score',
            'early_max_score',
            'early_avg_weight',
            'early_total_weight',
            'early_banked_count'
        ]
        
        # 2. Submission Timing (if date_submitted exists)
        if 'date_submitted' in assessment_data.columns and 'date' in assessment_data.columns:
            assessment_data['submission_time'] = (
                assessment_data['date_submitted'] - assessment_data['date']
            )
            
            timing_metrics = assessment_data.groupby('id_student').agg({
                'submission_time': ['mean', 'std']
            }).reset_index()
            timing_metrics.columns = ['id_student', 'early_avg_submission_time', 'early_submission_std']
            
            base_metrics = base_metrics.merge(timing_metrics, on='id_student', how='left')
        
        # 3. Assessment Type Performance (if exists)
        if 'assessment_type' in assessment_data.columns:
            type_performance = assessment_data.groupby(
                ['id_student', 'assessment_type']
            )['score'].mean().unstack(fill_value=0)
            
            # Rename columns to indicate these are early scores
            type_performance.columns = [f'early_{col}_score' for col in type_performance.columns]
            type_performance = type_performance.reset_index()
            
            base_metrics = base_metrics.merge(type_performance, on='id_student', how='left')
        
        # 4. Learning Trajectory (score trend over early assessments)
        assessment_order = assessment_data.sort_values(['id_student', 'date'])
        
        def calculate_early_trend(group):
            """Calculate if student is improving/declining in early assessments"""
            if len(group) < 2:
                return 0
            try:
                # Positive slope = improving, Negative = declining
                return np.polyfit(range(len(group)), group['score'], 1)[0]
            except:
                return 0
        
        trends = assessment_order.groupby('id_student').apply(
            calculate_early_trend
        ).reset_index(name='early_score_trend')
        
        base_metrics = base_metrics.merge(trends, on='id_student', how='left')
        
        # Fill NaNs with 0 (students with minimal data)
        base_metrics = base_metrics.fillna(0)
        
        return base_metrics
    
    def _process_vle_data(
        self,
        vle_data: pd.DataFrame,
        vle_info: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Process EARLY VLE interaction data only
        NOTE: All data here is from BEFORE the prediction week
        """
        
        # ✅ SAFETY CHECK: Verify temporal cutoff
        max_date = vle_data['date'].max()
        expected_max = self.prediction_week * 7
        if max_date > expected_max:
            self.logger.warning(f"VLE data extends beyond week {self.prediction_week}! This should not happen.")
        
        # Merge VLE interactions with activity types
        vle_full = vle_data.merge(
            vle_info[['id_site', 'activity_type']],
            on='id_site',
            how='left'
        )
        
        # 1. Early Engagement Metrics
        base_features = vle_full.groupby('id_student').agg({
            'sum_click': ['sum', 'mean', 'std', 'count'],
            'activity_type': 'nunique',
            'date': ['min', 'max']
        }).reset_index()
        
        base_features.columns = [
            'id_student',
            'early_total_clicks',
            'early_avg_clicks',
            'early_clicks_std',
            'early_activity_count',
            'early_unique_activities',
            'early_first_activity_date',
            'early_last_activity_date'
        ]
        
        # Activity span and density
        base_features['early_activity_span'] = (
            base_features['early_last_activity_date'] - 
            base_features['early_first_activity_date']
        ).clip(lower=1)
        
        base_features['early_activity_density'] = (
            base_features['early_total_clicks'] / base_features['early_activity_span']
        )
        
        # 2. First Week Engagement (highly predictive!)
        first_week_cutoff = 7  # First 7 days
        first_week_data = vle_data[vle_data['date'] <= first_week_cutoff]
        first_week_clicks = first_week_data.groupby('id_student')['sum_click'].sum().reset_index()
        first_week_clicks.columns = ['id_student', 'first_week_clicks']
        
        base_features = base_features.merge(first_week_clicks, on='id_student', how='left')
        
        # 3. Activity Type Preferences (early period)
        content_preferences = vle_full.groupby(
            ['id_student', 'activity_type']
        )['sum_click'].sum().unstack(fill_value=0)
        
        # Normalize to proportions
        content_preferences = content_preferences.div(
            content_preferences.sum(axis=1), axis=0
        ).add_prefix('early_pref_')
        
        base_features = base_features.merge(
            content_preferences, on='id_student', how='left'
        )
        
        # 4. Temporal Patterns (if we have enough data)
        vle_full['datetime'] = pd.to_datetime('2014-01-01') + pd.to_timedelta(vle_full['date'], unit='D')
        vle_full['hour'] = vle_full['datetime'].dt.hour
        vle_full['is_weekend'] = vle_full['datetime'].dt.dayofweek.isin([5, 6]).astype(int)
        
        # Weekend study pattern
        weekend_pattern = vle_full.groupby(['id_student', 'is_weekend'])['sum_click'].sum().unstack(fill_value=0)
        if len(weekend_pattern.columns) == 2:
            weekend_pattern.columns = ['early_weekday_clicks', 'early_weekend_clicks']
            weekend_pattern['early_weekend_ratio'] = (
                weekend_pattern['early_weekend_clicks'] / 
                (weekend_pattern['early_weekday_clicks'] + weekend_pattern['early_weekend_clicks']).clip(lower=1)
            )
            base_features = base_features.merge(weekend_pattern[['early_weekend_ratio']], 
                                               on='id_student', how='left')
        
        # Peak activity hour
        hour_dist = vle_full.groupby(['id_student', 'hour'])['sum_click'].sum().unstack(fill_value=0)
        if not hour_dist.empty:
            peak_hours = hour_dist.idxmax(axis=1).reset_index()
            peak_hours.columns = ['id_student', 'early_peak_hour']
            base_features = base_features.merge(peak_hours, on='id_student', how='left')
        
        # Fill missing values
        base_features = base_features.fillna(0)
        
        return base_features
    
    def _process_registration_data(
        self,
        student_registration: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Process registration data - SAFE (no future information)
        Only using registration date, which is known at course start
        """
        
        # ❌ DO NOT USE: date_unregistration (future information!)
        # ❌ DO NOT USE: registration_duration (calculated from end date!)
        
        # Only keep registration start date
        registration_features = student_registration.groupby('id_student').agg({
            'date_registration': 'min'  # When they enrolled
        }).reset_index()
        
        registration_features.columns = ['id_student', 'enrollment_date']
        
        return registration_features
    
    def feature_engineering(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create additional engineered features from EARLY data only
        
        ❌ REMOVED: engagement_score, performance_consistency, time_management
        These were calculated from full-course data and leaked the target!
        
        ✅ NEW: Only use features available at prediction time
        """
        
        # 1. Early Engagement Intensity (safe - uses early data only)
        if 'early_total_clicks' in df.columns and 'early_activity_span' in df.columns:
            df['early_engagement_intensity'] = (
                df['early_total_clicks'] / df['early_activity_span'].clip(lower=1)
            )
        
        # 2. Early Performance Risk Flag
        if 'early_avg_score' in df.columns:
            df['early_low_performance_flag'] = (df['early_avg_score'] < 50).astype(int)
        
        # 3. Engagement Diversity Score
        if 'early_unique_activities' in df.columns and 'early_activity_count' in df.columns:
            df['early_diversity_score'] = (
                df['early_unique_activities'] / df['early_activity_count'].clip(lower=1)
            )
        
        # 4. First Week Engagement Ratio (very predictive!)
        if all(col in df.columns for col in ['first_week_clicks', 'early_total_clicks']):
            df['first_week_ratio'] = (
                df['first_week_clicks'] / df['early_total_clicks'].clip(lower=1)
            )
        
        return df
    
    def create_weakness_level(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create target variable from ACTUAL OUTCOMES (final_result)
        
        ✅ CORRECT: Using actual course outcome as ground truth
        ❌ OLD METHOD: Was using derived scores that themselves leaked the target
        """
        
        if 'final_result' not in df.columns:
            raise ValueError("final_result column not found! Cannot create target variable.")
        
        # Map final_result to weakness level
        # Distinction/Pass = Low risk (0)
        # Fail = Medium risk (1)  
        # Withdrawn = High risk (2)
        
        result_mapping = {
            'Distinction': 0,  # Strong performance
            'Pass': 0,         # Adequate performance
            'Fail': 1,         # Struggled but completed
            'Withdrawn': 2     # Dropped out
        }
        
        df['weakness_level'] = df['final_result'].map(result_mapping)
        
        # Handle any unmapped values
        if df['weakness_level'].isna().any():
            self.logger.warning(f"Found {df['weakness_level'].isna().sum()} unmapped final_result values")
            df['weakness_level'] = df['weakness_level'].fillna(1)  # Default to medium risk
        
        df['weakness_level'] = df['weakness_level'].astype(int)
        
        # Record class distribution
        self.report['class_distribution'] = df['weakness_level'].value_counts().to_dict()
        
        # ✅ NOW drop final_result - it was only needed for target creation
        df = df.drop(columns=['final_result'])
=======
from typing import Tuple
from sklearn.model_selection import train_test_split

class OUPreprocessor(BasePreprocessor):
    def __init__(self):
        super().__init__("OU")
    
    def load_data(self):
        """Load OU Analyse Dataset"""
        self.logger.info("Loading OU dataset...")
        
        ou_dir = self.raw_dir / 'ou_data'
        
        # Load essential columns only
        student_info = pd.read_csv(
            ou_dir / 'studentInfo.csv',
            usecols=['id_student', 'gender', 'region', 'highest_education']
        )
        
        assessments = pd.read_csv(
            ou_dir / 'studentAssessment.csv',
            usecols=['id_student', 'id_assessment', 'score']
        )
        
        vle_data = pd.read_csv(
            ou_dir / 'studentVle.csv',
            usecols=['id_student', 'sum_click']
        ).groupby('id_student')['sum_click'].sum().reset_index()
        
        # Merge datasets
        self.raw_data = student_info.merge(assessments, on='id_student', how='left')
        self.raw_data = self.raw_data.merge(vle_data, on='id_student', how='left')
        
        self.report['original_shape'] = self.raw_data.shape
        self.report['features_before'] = self.raw_data.columns.tolist()
        
        return self.raw_data
    
    def feature_engineering(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create new features for OU dataset"""
        self.logger.info("Performing feature engineering...")
        
        # Average score per student
        score_stats = df.groupby('id_student')['score'].agg(['mean', 'std', 'count']).reset_index()
        score_stats.columns = ['id_student', 'avg_score', 'performance_consistency', 'attempts_per_topic']
        
        # Merge score statistics back
        df = df.merge(score_stats, on='id_student', how='left')
        
        # Score trend based on assessment order
        student_scores = df.groupby('id_student')['score']
        first_scores = student_scores.first()
        last_scores = student_scores.last()
        attempts = student_scores.count()
        
        score_trends = (last_scores - first_scores) / attempts
        score_trends = score_trends.reset_index()
        score_trends.columns = ['id_student', 'score_trend']
        
        df = df.merge(score_trends, on='id_student', how='left')
        
        # Time efficiency (score per VLE interaction)
        df['time_efficiency'] = df['score'] / df.groupby('id_student')['sum_click'].transform('sum')
        
        # At risk flag
        df['at_risk_flag'] = (df['avg_score'] < 50).astype(int)
>>>>>>> 431bf9542c2f2ee979b73168008154307fdc1749
        
        return df
    
    def preprocess(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
<<<<<<< HEAD
        """Main preprocessing pipeline with proper leakage prevention"""
        
        # Step 1: Load and merge data (with temporal filtering)
=======
        """Preprocess OU dataset following the defined steps"""
        
        # Step 1: Load data
>>>>>>> 431bf9542c2f2ee979b73168008154307fdc1749
        df = self.load_data()
        
        # Step 2: Handle missing values
        df = self.handle_missing_values(df)
        
<<<<<<< HEAD
        # Step 3: Feature engineering (SAFE - uses early data only)
        df = self.feature_engineering(df)
        
        # Step 4: Create target variable from outcomes
        df = self.create_weakness_level(df)
        
        # Step 5: Remove duplicates (ensure one row per student)
        if 'id_student' in df.columns:
            before_dupes = df.shape[0]
            df = df.drop_duplicates(subset=['id_student']).reset_index(drop=True)
            dupes_removed = before_dupes - df.shape[0]
            if dupes_removed > 0:
                self.logger.warning(f"Removed {dupes_removed} duplicate student records")
                self.report['duplicates_removed'] = dupes_removed
        
        # Step 6: Final safety check - verify no leaky columns remain
        FORBIDDEN_FEATURES = [
            'final_result',  # Already dropped after target creation
            'weakness_score',
            'engagement_score',
            'performance_consistency', 
            'time_management',
            'date_unregistration',
            'registration_duration'
        ]
        
        remaining_leaky = [col for col in FORBIDDEN_FEATURES if col in df.columns]
        if remaining_leaky:
            self.logger.error(f"LEAKAGE DETECTED! Found forbidden features: {remaining_leaky}")
            df = df.drop(columns=remaining_leaky)
            self.report['emergency_dropped_features'] = remaining_leaky
        
        # Step 7: Encode categorical variables
        categorical_cols = df.select_dtypes(include=['object']).columns
        categorical_cols = [col for col in categorical_cols if col != 'id_student']
        
        for col in categorical_cols:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))
            self.label_encoders[col] = le
        
        # Step 8: STUDENT-LEVEL train-test split (not random row split!)
        # This ensures no student appears in both train and test
        
        unique_students = df['id_student'].unique()
        
        train_students, test_students = train_test_split(
            unique_students,
            test_size=0.2,
            random_state=42,
            stratify=df.groupby('id_student')['weakness_level'].first()[unique_students]
        )
        
        train_df = df[df['id_student'].isin(train_students)].copy()
        test_df = df[df['id_student'].isin(test_students)].copy()
        
        self.logger.info(f"Student-level split: {len(train_students)} train, {len(test_students)} test")
        
        # Verify no student overlap
        overlap = set(train_df['id_student']) & set(test_df['id_student'])
        if len(overlap) > 0:
            raise ValueError(f"CRITICAL ERROR: {len(overlap)} students appear in both train and test!")
        
        self.report['train_students'] = len(train_students)
        self.report['test_students'] = len(test_students)
        self.report['student_overlap'] = 0  # Should always be 0!
        
        # Step 9: Drop id_student before scaling (not needed for modeling)
        if 'id_student' in train_df.columns:
            train_df = train_df.drop(columns=['id_student'])
            test_df = test_df.drop(columns=['id_student'])
        
        # Step 10: Scale features
        numeric_cols = train_df.select_dtypes(include=['float64', 'int64']).columns
        cols_to_scale = [col for col in numeric_cols if col != 'weakness_level']
        
        if cols_to_scale:
            train_scaled = self.scaler.fit_transform(train_df[cols_to_scale])
            test_scaled = self.scaler.transform(test_df[cols_to_scale])
            
            train_df[cols_to_scale] = train_scaled
            test_df[cols_to_scale] = test_scaled
        
        # Update report
        self.report['final_shape'] = train_df.shape
        self.report['features_after'] = train_df.columns.tolist()
        self.report['num_features'] = len(cols_to_scale)
        self.report['scaling_params'] = {
            'mean': self.scaler.mean_.tolist() if hasattr(self.scaler, 'mean_') else None,
            'scale': self.scaler.scale_.tolist() if hasattr(self.scaler, 'scale_') else None
        }
        
        # Save report
        self.save_report()
        
        self.logger.info(f"✅ Preprocessing complete: {train_df.shape[1]-1} features, {train_df.shape[0]} train samples")
        self.logger.info(f"✅ Target distribution - Train: {train_df['weakness_level'].value_counts().to_dict()}")
        self.logger.info(f"✅ Target distribution - Test: {test_df['weakness_level'].value_counts().to_dict()}")
=======
        # Step 3: Feature engineering
        df = self.feature_engineering(df)
        
        # Step 4: Handle outliers
        numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
        df = self.handle_outliers(df, numeric_columns)
        
        # Step 5: Create target variable
        df = self.create_weakness_level(df, 'avg_score')
        
        # Step 6: Encode categorical variables
        df = self.encode_categorical(df)
        
        # Step 7: Train-test split
        train_df, test_df = train_test_split(
            df,
            test_size=0.2,
            random_state=42,
            stratify=df['weakness_level']
        )
        
        # Step 8: Scale features
        numeric_columns = train_df.select_dtypes(include=['float64', 'int64']).columns
        train_df, test_df = self.scale_features(train_df, test_df, numeric_columns)
        
        # Update report
        self.report['final_shape'] = df.shape
        self.report['features_after'] = df.columns.tolist()
        
        # Class distribution
        self.report['class_distribution'] = {
            'train': train_df['weakness_level'].value_counts().to_dict(),
            'test': test_df['weakness_level'].value_counts().to_dict()
        }
        
        # Save processed data and report
        self.save_data(train_df, test_df)
        self.save_report()
        
        # Plot distributions
        plot_columns = ['avg_score', 'score_trend', 'performance_consistency']
        self.plot_distributions(
            self.raw_data,
            train_df,
            plot_columns,
            self.reports_dir / f"{self.dataset_name}_distributions.png"
        )
>>>>>>> 431bf9542c2f2ee979b73168008154307fdc1749
        
        return train_df, test_df