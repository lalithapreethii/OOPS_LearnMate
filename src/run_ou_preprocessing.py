"""
Run enhanced preprocessing for OU dataset
"""
import logging
from pathlib import Path
from preprocessor.ou_enhanced import OUEnhancedPreprocessor

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main execution function"""
    logger.info("Starting enhanced OU dataset preprocessing...")
    
    try:
        # Initialize preprocessor
        preprocessor = OUEnhancedPreprocessor()
        
        # Run preprocessing
        train_df, test_df = preprocessor.preprocess()
        
        # Log results
        logger.info(f"Preprocessing completed successfully!")
        logger.info(f"Training set shape: {train_df.shape}")
        logger.info(f"Test set shape: {test_df.shape}")
        logger.info(f"Features used: {train_df.columns.tolist()}")
        
        # Class distribution
        logger.info("\nClass distribution in training set:")
        logger.info(train_df['weakness_level'].value_counts().sort_index())
        logger.info("\nClass distribution in test set:")
        logger.info(test_df['weakness_level'].value_counts().sort_index())
        
    except Exception as e:
        logger.error(f"Error during preprocessing: {str(e)}")
        raise

if __name__ == "__main__":
    main()