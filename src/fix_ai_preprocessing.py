"""
Fix AI dataset preprocessing to ensure proper class distribution.
This script implements the correct binning strategy for weakness levels.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_data():
    """Load original AI dataset"""
    logger.info("Loading original AI dataset...")
    
    base_dir = Path(__file__).parent.parent
    ai_dir = base_dir / 'data' / 'raw' / 'ai_course_data' / 'Student Performance Dataset in AI course'
    data_path = ai_dir / "Stu_Performance_dataset.csv"
    
    df = pd.read_csv(data_path)
    logger.info(f"Loaded {len(df)} samples")
    
    return df

def create_weakness_levels(df):
    """Create weakness levels using correct binning"""
    logger.info("Creating weakness levels...")
    
    # Create weakness levels based on Total score (out of 100)
    # Weak (0): < 60 (Fail, D+, D)
    # Moderate (1): 60-75 (C-, C, C+, B-, B)
    # Strong (2): >= 75 (B+, A-, A)
    df['weakness_level'] = pd.cut(
        df['Total'],
        bins=[-np.inf, 60, 75, np.inf],
        labels=[0, 1, 2]  # 0: Weak, 1: Moderate, 2: Strong
    )
    
    # Display class distribution
    print("\nClass Distribution (counts):")
    print(df['weakness_level'].value_counts().sort_index())
    
    print("\nClass Distribution (percentages):")
    print(df['weakness_level'].value_counts(normalize=True).sort_index().map('{:.2%}'.format))
    
    # Verify against Grades
    print("\nGrade Distribution within each Weakness Level:")
    print(pd.crosstab(df['weakness_level'], df['Grade']))
    
    return df

def encode_categorical_features(df):
    """Encode categorical variables"""
    logger.info("Encoding categorical features...")
    
    categorical_columns = df.select_dtypes(include=['object']).columns
    encoders = {}
    
    for column in categorical_columns:
        encoders[column] = LabelEncoder()
        df[column] = encoders[column].fit_transform(df[column])
    
    return df, encoders

def handle_missing_values(df):
    """Handle any missing values"""
    logger.info("Handling missing values...")
    
    # Check for missing values
    missing = df.isnull().sum()
    if missing.any():
        logger.info("Found missing values:")
        print(missing[missing > 0])
        
        # Fill numeric with median, categorical with mode
        for column in df.columns:
            if df[column].isnull().any():
                if pd.api.types.is_numeric_dtype(df[column]):
                    df[column] = df[column].fillna(df[column].median())
                else:
                    df[column] = df[column].fillna(df[column].mode()[0])
    else:
        logger.info("No missing values found")
    
    return df

def scale_features(df, target_col):
    """Scale numerical features"""
    logger.info("Scaling features...")
    
    # Identify features to scale (exclude student ID and target)
    feature_cols = [col for col in df.columns if col not in ['Student Id', target_col]]
    
    # Scale features
    scaler = StandardScaler()
    df[feature_cols] = scaler.fit_transform(df[feature_cols])
    
    return df, scaler

def main():
    """Main execution function"""
    logger.info("Starting AI dataset fix...")
    
    # Create output directories
    base_dir = Path(__file__).parent.parent
    output_dir = base_dir / 'data' / 'processed'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Load data
    df = load_data()
    
    # Create weakness levels
    df = create_weakness_levels(df)
    
    # Verify all three classes exist
    unique_classes = df['weakness_level'].nunique()
    if unique_classes < 3:
        logger.error(f"Only found {unique_classes} classes! Expected 3 classes.")
        return
    
    # Handle missing values
    df = handle_missing_values(df)
    
    # Drop unnecessary columns
    df = df.drop(['Grade', 'Categories'], axis=1)  # These are derived from Total
    
    # Encode categorical features (if any remain)
    df, encoders = encode_categorical_features(df)
    
    # Scale features
    df_scaled, scaler = scale_features(df, 'weakness_level')
    
    # Split into train and test sets
    train_df, test_df = train_test_split(
        df_scaled,
        test_size=0.2,
        random_state=42,
        stratify=df_scaled['weakness_level']
    )
    
    # Save processed datasets
    train_df.to_csv(output_dir / 'AI_train_fixed.csv', index=False)
    test_df.to_csv(output_dir / 'AI_test_fixed.csv', index=False)
    
    logger.info(f"Saved processed data:")
    logger.info(f"Training set: {len(train_df)} samples")
    logger.info(f"Test set: {len(test_df)} samples")
    
    # Final class distribution check
    print("\nTraining Set Class Distribution:")
    print(train_df['weakness_level'].value_counts().sort_index())
    print("\nTest Set Class Distribution:")
    print(test_df['weakness_level'].value_counts().sort_index())

if __name__ == "__main__":
    main()