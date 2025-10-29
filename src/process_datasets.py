from preprocessor.uci import UCIPreprocessor
from preprocessor.ou import OUPreprocessor
from preprocessor.ai import AIPreprocessor
import logging
import os
import argparse

def setup_paths():
    """Ensure required directories exist"""
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_path, 'data', 'processed')
    reports_path = os.path.join(base_path, 'reports')
    
    os.makedirs(data_path, exist_ok=True)
    os.makedirs(reports_path, exist_ok=True)
    
    return data_path, reports_path

def process_dataset(dataset_name: str):
    """Process a specific dataset"""
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    # Create required directories
    data_path, reports_path = setup_paths()
    
    # Initialize appropriate preprocessor
    if dataset_name.lower() == 'uci':
        preprocessor = UCIPreprocessor()
    elif dataset_name.lower() == 'ou':
        preprocessor = OUPreprocessor()
    elif dataset_name.lower() == 'ai':
        preprocessor = AIPreprocessor()
    else:
        raise ValueError(f"Unknown dataset: {dataset_name}")
    
    try:
        # Process data
        logger.info(f"\nProcessing {preprocessor.dataset_name} dataset...")
        train_df, test_df = preprocessor.preprocess()
        
        # Save processed data
        train_path = os.path.join(data_path, f"{dataset_name}_train.csv")
        test_path = os.path.join(data_path, f"{dataset_name}_test.csv")
        
        train_df.to_csv(train_path, index=False)
        test_df.to_csv(test_path, index=False)
        
        logger.info(f"Successfully processed {preprocessor.dataset_name} dataset")
        logger.info(f"Train shape: {train_df.shape}")
        logger.info(f"Test shape: {test_df.shape}")
        
    except Exception as e:
        logger.error(f"Error processing {dataset_name} dataset: {str(e)}")
        raise

def main():
    """Run preprocessing based on command line args"""
    parser = argparse.ArgumentParser(description='Process dataset(s)')
    parser.add_argument('--dataset', type=str, choices=['uci', 'ou', 'ai', 'all'],
                      help='Dataset to process (uci, ou, ai, or all)', default='all')
    
    args = parser.parse_args()
    
    if args.dataset == 'all':
        datasets = ['uci', 'ou', 'ai']
    else:
        datasets = [args.dataset]
    
    for dataset in datasets:
        try:
            process_dataset(dataset)
        except Exception as e:
            print(f"Failed to process {dataset}: {str(e)}")

if __name__ == "__main__":
    main()