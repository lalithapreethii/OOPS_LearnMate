from preprocessor.uci import UCIPreprocessor
from preprocessor.ou import OUPreprocessor
from preprocessor.ai import AIPreprocessor
import logging

def main():
    """Run preprocessing for all datasets"""
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    preprocessors = [
        UCIPreprocessor(),
        OUPreprocessor(),
        AIPreprocessor()
    ]
    
    for preprocessor in preprocessors:
        logger.info(f"\nProcessing {preprocessor.dataset_name} dataset...")
        try:
            train_df, test_df = preprocessor.preprocess()
            logger.info(f"Successfully processed {preprocessor.dataset_name} dataset")
            logger.info(f"Train shape: {train_df.shape}")
            logger.info(f"Test shape: {test_df.shape}")
        except Exception as e:
            logger.error(f"Error processing {preprocessor.dataset_name} dataset: {str(e)}")

if __name__ == "__main__":
    main()