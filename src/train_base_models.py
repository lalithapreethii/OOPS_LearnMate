import pandas as pd
import numpy as np
from base_models import BaseModels
import logging
import os
import json

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def load_dataset(dataset_name):
    """Load train and test datasets"""
    train_path = f'data/processed/{dataset_name}_train.csv'
    test_path = f'data/processed/{dataset_name}_test.csv'
    
    if not os.path.exists(train_path) or not os.path.exists(test_path):
        raise FileNotFoundError(f"Dataset files not found for {dataset_name}")
    
    train_data = pd.read_csv(train_path)
    test_data = pd.read_csv(test_path)
    
    # Separate features and target
    X_train = train_data.drop('weakness_level', axis=1)
    y_train = train_data['weakness_level']
    X_test = test_data.drop('weakness_level', axis=1)
    y_test = test_data['weakness_level']
    
    return X_train, X_test, y_train, y_test

def train_base_models(dataset_name):
    """Train base models for a specific dataset"""
    logging.info(f"Training base models for {dataset_name} dataset")
    
    try:
        # Load data
        X_train, X_test, y_train, y_test = load_dataset(dataset_name)
        
        # Initialize base models
        base_models = BaseModels(random_state=42)
        
        # Train all models
        logging.info("Starting model training...")
        base_models.train_all_models(X_train, y_train, n_iter=20)
        
        # Save results
        base_models.save_results(dataset_name)
        
        # Get and save feature importance
        feature_importance = base_models.get_feature_importance(X_train.columns)
        
        # Save feature importance
        filename = f'results/feature_importance_{dataset_name}.json'
        with open(filename, 'w') as f:
            json.dump(feature_importance, f, indent=4)
        
        logging.info(f"Feature importance saved to {filename}")
        
        return base_models
        
    except Exception as e:
        logging.error(f"Error training models for {dataset_name}: {str(e)}")
        raise

def main():
    """Train base models for all datasets"""
    datasets = ['AI', 'UCI', 'OU']
    trained_models = {}
    
    for dataset in datasets:
        logging.info(f"\nProcessing {dataset} dataset...")
        try:
            trained_models[dataset] = train_base_models(dataset)
            logging.info(f"Successfully trained models for {dataset} dataset")
        except Exception as e:
            logging.error(f"Failed to train models for {dataset} dataset: {str(e)}")
            continue

if __name__ == "__main__":
    main()