"""
Quick test script to check feature alignment between datasets
"""

import pandas as pd
from pathlib import Path
import joblib

# Load model and scaler
model_path = Path('models/weakness_classifier.pkl')
scaler_path = Path('models/scaler.pkl')

model = joblib.load(model_path)
scaler = joblib.load(scaler_path)

# Get training features
training_features = scaler.feature_names_in_
print("\nTraining features:", len(training_features))
print(sorted(training_features))

# Load one test dataset
test_data = pd.read_csv('data/processed/AI_test.csv')
print("\nTest features:", len(test_data.columns))
print(sorted(test_data.columns))