from data_preprocessor import DataPreprocessor
import logging

def test_dataset_loading():
    datasets = ["UCI", "OU", "AI"]
    
    for dataset in datasets:
        try:
            preprocessor = DataPreprocessor(dataset)
            preprocessor.load_data()
            print(f"\n{dataset} Dataset loaded successfully:")
            print(f"Shape: {preprocessor.raw_data.shape}")
            print(f"Columns: {preprocessor.raw_data.columns.tolist()}")
            print(f"First few rows:\n{preprocessor.raw_data.head()}\n")
            print("-" * 80)
        except Exception as e:
            logging.error(f"Error loading {dataset} dataset: {str(e)}")

if __name__ == "__main__":
    test_dataset_loading()