"""
Comprehensive model evaluation script comparing the ensemble model with baseline models.
Generates detailed performance reports and visualizations.
"""

import pandas as pd
import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from sklearn.metrics import confusion_matrix, roc_curve, auc
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import json
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelEvaluator:
    def __init__(self, base_path=None):
        """Initialize evaluator with base path"""
        if base_path is None:
            base_path = Path.cwd()
        else:
            base_path = Path(base_path)
            
        self.data_path = base_path / "data" / "processed"
        self.models_path = base_path / "models"
        self.reports_path = base_path / "reports"
        
        # Create reports directory if it doesn't exist
        self.reports_path.mkdir(parents=True, exist_ok=True)
        
        self.ensemble_model = None
        self.scaler = None
        self.baseline_models = {}
        self.metrics = {}
        
        logger.info(f"Using data path: {self.data_path}")
        logger.info(f"Using models path: {self.models_path}")
        logger.info(f"Using reports path: {self.reports_path}")
        
    def load_model_and_data(self):
        """Load the trained ensemble model, scaler, and test data"""
        logger.info("Loading model and data...")
        
        try:
            # Load trained model and scaler
            self.ensemble_model = joblib.load(self.models_path / 'weakness_classifier.pkl')
            self.scaler = joblib.load(self.models_path / 'scaler.pkl')
            
            # Load test datasets
            self.test_sets = {}
            for dataset in ['UCI', 'OU', 'AI']:
                df = pd.read_csv(self.data_path / f"{dataset}_test.csv")
                self.test_sets[dataset] = df
                
            logger.info("Model and data loaded successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error loading model and data: {str(e)}")
            return False
            
    def prepare_baseline_models(self):
        """Initialize baseline models for comparison"""
        logger.info("Preparing baseline models...")
        
        self.baseline_models = {
            'naive_bayes': GaussianNB(),
            'decision_tree': DecisionTreeClassifier(random_state=42),
            'svm': SVC(probability=True, random_state=42),
            'logistic_regression': LogisticRegression(random_state=42)
        }
        
    def _get_feature_columns(self, dataset):
        """Get the correct feature columns in the right order"""
        feature_names = self.scaler.feature_names_in_
        available_features = set(dataset.columns)
        common_features = [col for col in feature_names if col in available_features]
        
        if not common_features:
            logger.error("No common features found between training and test data")
            return None
            
        missing_count = len(feature_names) - len(common_features)
        if missing_count > 0:
            logger.warning(f"Using {len(common_features)} features out of {len(feature_names)} training features")
            
        return common_features

    def evaluate_all_models(self):
        """Evaluate ensemble model and all baseline models"""
        logger.info("Evaluating all models...")
        
        for dataset_name, dataset in self.test_sets.items():
            logger.info(f"Evaluating on {dataset_name} dataset...")
            
            # Get correct features
            feature_names = self._get_feature_columns(dataset)
            if feature_names is None:
                logger.error(f"Cannot evaluate {dataset_name} dataset due to missing features")
                continue
                
            # Create full feature array with zeros
            X_full = pd.DataFrame(0, index=dataset.index, columns=self.scaler.feature_names_in_)
            
            # Fill in available features
            for feature in feature_names:
                X_full[feature] = dataset[feature]
                
            # Prepare target
            y = dataset['weakness_level']
            
            # Scale features (now with all columns in correct order)
            X_scaled = self.scaler.transform(X_full)
            
            # Replace any NaN values with 0 after scaling
            X_scaled = np.nan_to_num(X_scaled)
            
            # Evaluate ensemble model
            self._evaluate_model(
                self.ensemble_model, 
                X_scaled, 
                y, 
                'ensemble', 
                dataset_name
            )
            
            # Train and evaluate baseline models
            unique_classes = len(np.unique(y))
            if unique_classes < 2:
                logger.warning(f"Dataset {dataset_name} has only {unique_classes} class(es). Skipping baseline models.")
            else:
                for name, model in self.baseline_models.items():
                    model.fit(X_scaled, y)
                    self._evaluate_model(model, X_scaled, y, name, dataset_name)
                
        return self.metrics
    
    def _evaluate_model(self, model, X, y, model_name, dataset_name):
        """Evaluate a single model and store metrics"""
        # Make predictions
        y_pred = model.predict(X)
        y_prob = model.predict_proba(X)
        
        # Calculate metrics
        accuracy = accuracy_score(y, y_pred)
        precision, recall, f1, _ = precision_recall_fscore_support(
            y, y_pred, average='weighted'
        )
        
        # Store metrics
        if dataset_name not in self.metrics:
            self.metrics[dataset_name] = {}
            
        self.metrics[dataset_name][model_name] = {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1': f1
        }
        
        # Generate ROC curve
        self._plot_roc_curve(y, y_prob, model_name, dataset_name)
        
    def _plot_roc_curve(self, y_true, y_prob, model_name, dataset_name):
        """Plot ROC curve for multi-class classification"""
        n_classes = len(np.unique(y_true))
        if n_classes < 2:
            logger.warning(f"Cannot create ROC curve for {dataset_name} - only {n_classes} class(es) present")
            return
            
        plt.figure(figsize=(8, 6))
        
        # Calculate ROC curve for each class
        for i in range(n_classes):
            fpr, tpr, _ = roc_curve((y_true == i).astype(int), y_prob[:, i])
            roc_auc = auc(fpr, tpr)
            plt.plot(fpr, tpr, label=f'Class {i} (AUC = {roc_auc:.2f})')
        
        plt.plot([0, 1], [0, 1], 'k--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title(f'ROC Curve - {model_name} ({dataset_name})')
        plt.legend(loc="lower right")
        plt.savefig(self.reports_path / f'roc_{model_name}_{dataset_name.lower()}.png')
        plt.close()
        
    def create_comparison_visualizations(self):
        """Create visualizations comparing all models"""
        logger.info("Creating comparison visualizations...")
        
        for dataset_name in self.metrics:
            # Prepare data for plotting
            model_names = list(self.metrics[dataset_name].keys())
            metrics_names = ['accuracy', 'precision', 'recall', 'f1']
            
            # Create comparison bar plot
            plt.figure(figsize=(12, 6))
            x = np.arange(len(model_names))
            width = 0.2
            
            for i, metric in enumerate(metrics_names):
                values = [self.metrics[dataset_name][model][metric] 
                         for model in model_names]
                plt.bar(x + i*width, values, width, label=metric)
            
            plt.xlabel('Models')
            plt.ylabel('Score')
            plt.title(f'Model Comparison - {dataset_name} Dataset')
            plt.xticks(x + width*1.5, model_names, rotation=45)
            plt.legend()
            plt.tight_layout()
            plt.savefig(self.reports_path / f'model_comparison_{dataset_name.lower()}.png')
            plt.close()
    
    def generate_report(self):
        """Generate comprehensive evaluation report"""
        logger.info("Generating evaluation report...")
        
        report = {
            'metrics': self.metrics,
            'summary': {
                'best_model': {},
                'improvement_over_baseline': {}
            }
        }
        
        # Determine best model and improvement for each dataset
        for dataset_name in self.metrics:
            # Find best model based on F1 score
            f1_scores = {
                model: metrics['f1']
                for model, metrics in self.metrics[dataset_name].items()
            }
            best_model = max(f1_scores.items(), key=lambda x: x[1])[0]
            
            # Calculate improvement over baseline average
            baseline_f1 = np.mean([
                metrics['f1'] 
                for model, metrics in self.metrics[dataset_name].items()
                if model != 'ensemble'
            ])
            ensemble_f1 = self.metrics[dataset_name]['ensemble']['f1']
            improvement = ((ensemble_f1 - baseline_f1) / baseline_f1) * 100
            
            report['summary']['best_model'][dataset_name] = {
                'model': best_model,
                'f1_score': f1_scores[best_model]
            }
            report['summary']['improvement_over_baseline'][dataset_name] = improvement
            
        # Save report
        with open(self.reports_path / 'evaluation_report.json', 'w') as f:
            json.dump(report, f, indent=4)
            
        return report

def main():
    """Main execution function"""
    # Create evaluator instance
    evaluator = ModelEvaluator()
    
    # Load model and data
    if not evaluator.load_model_and_data():
        return
        
    # Prepare and evaluate models
    evaluator.prepare_baseline_models()
    evaluator.evaluate_all_models()
    
    # Generate visualizations and report
    evaluator.create_comparison_visualizations()
    report = evaluator.generate_report()
    
    # Print detailed summary
    print("\nDetailed Evaluation Summary:")
    for dataset in report['summary']['best_model']:
        print(f"\n{dataset} Dataset:")
        print("-" * 50)
        
        # Dataset characteristics
        test_data = evaluator.test_sets[dataset]
        n_features = len(evaluator._get_feature_columns(test_data))
        n_samples = len(test_data)
        n_classes = len(np.unique(test_data['weakness_level']))
        
        print(f"Dataset Info:")
        print(f"- Samples: {n_samples}")
        print(f"- Features used: {n_features} out of {len(evaluator.scaler.feature_names_in_)}")
        print(f"- Unique classes: {n_classes}")
        print()
        
        # Model performance
        print("Model Performance:")
        for model_name, metrics in evaluator.metrics[dataset].items():
            print(f"\n{model_name.title()}:")
            print(f"- Accuracy:  {metrics['accuracy']:.4f}")
            print(f"- Precision: {metrics['precision']:.4f}")
            print(f"- Recall:    {metrics['recall']:.4f}")
            print(f"- F1 Score:  {metrics['f1']:.4f}")
        
        # Best model and improvement
        best_model = report['summary']['best_model'][dataset]['model']
        improvement = report['summary']['improvement_over_baseline'][dataset]
        print(f"\nOverall Best: {best_model.title()}")
        if not np.isnan(improvement):
            print(f"Improvement over baseline: {improvement:.2f}%")
        print("\n" + "="*50)

if __name__ == "__main__":
    main()