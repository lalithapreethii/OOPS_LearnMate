"""
Train the weakness classification model using ensemble learning (Random Forest + XGBoost).
Includes data loading, preprocessing, model training, evaluation, and saving.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from sklearn.metrics import confusion_matrix, roc_curve, auc
import xgboost as xgb
import matplotlib.pyplot as plt
import seaborn as sns
import json
import joblib
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WeaknessClassifier:
    def __init__(self, base_path=None):
        """Initialize the classifier with data path"""
        if base_path is None:
            base_path = Path.cwd()
        else:
            base_path = Path(base_path)
            
        self.data_path = base_path / "data" / "processed"
        self.models_path = base_path / "models"
        self.reports_path = base_path / "reports"
        
        # Create necessary directories
        self.models_path.mkdir(parents=True, exist_ok=True)
        self.reports_path.mkdir(parents=True, exist_ok=True)
        
        self.scaler = StandardScaler()
        self.model = None
        self.feature_columns = None
        self.target_column = 'weakness_level'  # Assuming target column name
        
        logger.info(f"Using data path: {self.data_path}")
        logger.info(f"Using models path: {self.models_path}")
        logger.info(f"Using reports path: {self.reports_path}")
        
    def load_datasets(self):
        """Load and combine all preprocessed datasets"""
        logger.info("Loading datasets...")
        try:
            # Load all datasets
            uci_data = pd.read_csv(self.data_path / "UCI_train.csv")
            ou_data = pd.read_csv(self.data_path / "OU_train.csv")
            ai_data = pd.read_csv(self.data_path / "AI_train.csv")
            
            # Combine datasets (assuming they have same structure after preprocessing)
            self.data = pd.concat([uci_data, ou_data, ai_data], ignore_index=True)
            
            # Define feature columns (excluding target and any ID columns)
            self.feature_columns = [col for col in self.data.columns 
                                  if col not in [self.target_column, 'student_id', 'course_id']]
            
            logger.info(f"Loaded {len(self.data)} total samples")
            return True
        except Exception as e:
            logger.error(f"Error loading datasets: {str(e)}")
            return False

    def prepare_model(self):
        """Create the voting classifier with RF and XGBoost"""
        logger.info("Preparing model...")
        
        # Initialize base models with regularization
        rf = RandomForestClassifier(
            random_state=42,
            oob_score=True,  # Use out-of-bag score
            class_weight='balanced'  # Handle class imbalance
        )
        xgb_model = xgb.XGBClassifier(
            random_state=42,
            early_stopping_rounds=10,
            eval_metric=['logloss', 'auc'],
            reg_alpha=0.1,  # L1 regularization
            reg_lambda=1.0  # L2 regularization
        )
        
        # Create voting classifier
        self.model = VotingClassifier(
            estimators=[
                ('rf', rf),
                ('xgb', xgb_model)
            ],
            voting='soft'
        )
        
        # Define parameter grid for GridSearchCV with reduced complexity
        self.param_grid = {
            'rf__n_estimators': [100, 150],
            'rf__max_depth': [5, 7],
            'rf__min_samples_leaf': [5, 10],  # Prevent overfitting
            'xgb__n_estimators': [100, 150],
            'xgb__max_depth': [3, 4],
            'xgb__min_child_weight': [5, 7]  # Prevent overfitting
        }

    def train_model(self):
        """Train the model using GridSearchCV"""
        logger.info("Training model...")
        
        X = self.data[self.feature_columns]
        y = self.data[self.target_column]
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Perform GridSearchCV with stratified k-fold
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        grid_search = GridSearchCV(
            self.model,
            self.param_grid,
            cv=cv,
            scoring=['accuracy', 'f1_weighted'],
            refit='f1_weighted',  # Optimize for F1 score instead of accuracy
            n_jobs=-1
        )
        
        grid_search.fit(X_scaled, y)
        self.model = grid_search.best_estimator_
        
        logger.info(f"Best parameters: {grid_search.best_params_}")
        logger.info(f"Best cross-validation score: {grid_search.best_score_:.4f}")
        
        return grid_search.best_score_

    def evaluate_model(self):
        """Evaluate model on test sets"""
        logger.info("Evaluating model...")
        
        metrics = {}
        
        for dataset in ['UCI', 'OU', 'AI']:
            try:
                # Load test data
                test_data = pd.read_csv(self.data_path / f"{dataset}_test.csv")
                
                X_test = test_data[self.feature_columns]
                y_test = test_data[self.target_column]
                
                # Scale features
                X_test_scaled = self.scaler.transform(X_test)
                
                # Make predictions
                y_pred = self.model.predict(X_test_scaled)
                
                # Calculate metrics
                accuracy = accuracy_score(y_test, y_pred)
                precision, recall, f1, _ = precision_recall_fscore_support(
                    y_test, y_pred, average='weighted'
                )
                
                metrics[dataset] = {
                    'accuracy': accuracy,
                    'precision': precision,
                    'recall': recall,
                    'f1': f1
                }
                
                # Generate confusion matrix plot
                self._plot_confusion_matrix(y_test, y_pred, dataset)
                
            except Exception as e:
                logger.error(f"Error evaluating {dataset} dataset: {str(e)}")
        
        return metrics

    def _plot_confusion_matrix(self, y_true, y_pred, dataset_name):
        """Plot confusion matrix for a dataset"""
        plt.figure(figsize=(8, 6))
        cm = confusion_matrix(y_true, y_pred)
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.title(f'Confusion Matrix - {dataset_name}')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.savefig(f'reports/confusion_matrix_{dataset_name.lower()}.png')
        plt.close()

    def plot_feature_importance(self):
        """Plot feature importance for Random Forest component"""
        rf_model = self.model.named_estimators_['rf']
        importance = rf_model.feature_importances_
        
        plt.figure(figsize=(10, 6))
        importance_df = pd.DataFrame({
            'feature': self.feature_columns,
            'importance': importance
        }).sort_values('importance', ascending=True)
        
        plt.barh(importance_df['feature'], importance_df['importance'])
        plt.title('Feature Importance (Random Forest)')
        plt.xlabel('Importance')
        plt.tight_layout()
        plt.savefig('reports/feature_importance.png')
        plt.close()

    def save_model(self):
        """Save the trained model and scaler"""
        logger.info("Saving model and scaler...")
        
        try:
            # Save model
            model_path = self.models_path / 'weakness_classifier.pkl'
            scaler_path = self.models_path / 'scaler.pkl'
            
            joblib.dump(self.model, model_path)
            joblib.dump(self.scaler, scaler_path)
            
            logger.info(f"Model saved to: {model_path}")
            logger.info(f"Scaler saved to: {scaler_path}")
            return True
        except Exception as e:
            logger.error(f"Error saving model: {str(e)}")
            return False

def main():
    """Main execution function"""
    # Get the current working directory
    base_path = Path.cwd()
    
    # Create classifier instance with absolute paths
    classifier = WeaknessClassifier(base_path)
    
    # Load and prepare data
    if not classifier.load_datasets():
        logger.error("Failed to load datasets. Exiting...")
        return
    
    # Prepare and train model
    classifier.prepare_model()
    best_score = classifier.train_model()
    
    # Save model immediately after training
    classifier.save_model()
    
    logger.info(f"Model training completed successfully with best CV score: {best_score:.4f}")
    
    # Save basic metrics
    metrics = {
        'cross_validation_score': best_score,
        'model_parameters': classifier.model.get_params()
    }
    
    metrics_path = classifier.reports_path / 'model_metrics.json'
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=4)
    
    logger.info(f"Metrics saved to: {metrics_path}")

if __name__ == "__main__":
    main()