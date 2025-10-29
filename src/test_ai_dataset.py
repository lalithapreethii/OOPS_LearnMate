from pathlib import Path
import pandas as pd
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Define paths
BASE_DIR = Path(r"D:\KnowWhereYouLack")
RAW_DATA_DIR = BASE_DIR / 'data' / 'raw'

def test_ai_dataset():
    """Test loading AI course dataset"""
    try:
        ai_file = RAW_DATA_DIR / 'ai_course_data' / 'Student Performance Dataset in AI course' / 'Stu_Performance_dataset.csv'
        if not ai_file.exists():
            raise FileNotFoundError(f"AI course dataset file not found at {ai_file}")
            
        df = pd.read_csv(ai_file)
        print("\nAI Course Dataset loaded successfully:")
        print(f"Shape: {df.shape}")
        print(f"Columns: {df.columns.tolist()}")
        print(f"First few rows:\n{df.head()}\n")
        print("-" * 80)
        
    except Exception as e:
        logging.error(f"Error loading AI dataset: {str(e)}")

if __name__ == "__main__":
    test_ai_dataset()