"""
Fix UCI dataset preprocessing to ensure proper class distribution.
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
    """Load original UCI dataset"""
    logger.info("Loading original UCI dataset...")
    
    base_dir = Path(__file__).parent.parent
    uci_dir = base_dir / 'data' / 'raw' / 'uci_data'
    math_path = uci_dir / "student-mat.csv"
    
    # Load mathematics dataset
    df = pd.read_csv(math_path, sep=';')
    logger.info(f"Loaded {len(df)} samples")
    
    return df

def create_weakness_levels(df):
    """Create weakness levels using correct binning"""
    logger.info("Creating weakness levels...")
    
    # Create weakness levels based on G3 (final grade)
    df['weakness_level'] = pd.cut(
        df['G3'],
        bins=[-np.inf, 10, 14, np.inf],
        labels=[0, 1, 2]  # 0: Weak, 1: Moderate, 2: Strong
    )
    
    # Display class distribution
    print("\nClass Distribution (counts):")
    print(df['weakness_level'].value_counts().sort_index())
    
    print("\nClass Distribution (percentages):")
    print(df['weakness_level'].value_counts(normalize=True).sort_index().map('{:.2%}'.format))
    
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
    
    # Separate features and target
    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Convert back to DataFrame
    X_scaled = pd.DataFrame(X_scaled, columns=X.columns, index=X.index)
    X_scaled[target_col] = y
    
    return X_scaled, scaler

def main():
    """Main execution function"""
    logger.info("Starting UCI dataset fix...")
    
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
    
    # Encode categorical features
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
    train_df.to_csv(output_dir / 'UCI_train_fixed.csv', index=False)
    test_df.to_csv(output_dir / 'UCI_test_fixed.csv', index=False)
    
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