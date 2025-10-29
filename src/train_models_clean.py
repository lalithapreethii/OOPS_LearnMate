"""
Train models on temporally valid datasets
Uses the new preprocessed files that respect temporal order
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from xgboost import XGBClassifier
from sklearn.metrics import (accuracy_score, precision_recall_fscore_support, 
                            confusion_matrix, classification_report)
from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

def train_and_evaluate_dataset(dataset_name: str):
    """Train and evaluate model on a dataset"""
    
    print(f"\n{'='*60}")
    print(f"Training and evaluating {dataset_name} dataset")
    print(f"{'='*60}")
    
    # Set up paths to new preprocessed files
    base_dir = Path('data') / 'processed'
    train_path = base_dir / f'{dataset_name}_train.csv'
    test_path = base_dir / f'{dataset_name}_test.csv'
    
    # Load data
    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)
    
    # Verify weakness_level values are correctly encoded
    if 'weakness_level' not in train_df.columns:
        print("Error: Missing weakness_level target column")
        return
        
    # Ensure values are properly encoded (0, 1, 2)
    train_df['weakness_level'] = train_df['weakness_level'].astype(int)
    test_df['weakness_level'] = test_df['weakness_level'].astype(int)
    
    # Separate features and target
    X_train = train_df.drop('weakness_level', axis=1)
    y_train = train_df['weakness_level']
    X_test = test_df.drop('weakness_level', axis=1)
    y_test = test_df['weakness_level']
    
    print(f"\nDataset Info:")
    print(f"Training samples: {len(X_train)}, Features: {X_train.shape[1]}")
    print(f"Test samples: {len(X_test)}")
    
    print(f"\nTraining set class distribution:")
    print(y_train.value_counts().sort_index())
    print(f"\nTest set class distribution:")
    print(y_test.value_counts().sort_index())
    
    # Create ensemble model
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    xgb = XGBClassifier(n_estimators=100, random_state=42)
    
    ensemble = VotingClassifier(
        estimators=[('rf', rf), ('xgb', xgb)],
        voting='soft'
    )
    
    # Cross-validation
    print("\nPerforming 5-fold cross-validation...")
    cv_scores = cross_val_score(ensemble, X_train, y_train, cv=5, 
                              scoring='f1_weighted', n_jobs=-1)
    print(f"Cross-Validation F1 Scores: {cv_scores}")
    print(f"Mean CV F1: {cv_scores.mean():.4f} (+/- {cv_scores.std()*2:.4f})")
    
    print("\nTraining final model...")
    ensemble.fit(X_train, y_train)
    y_pred = ensemble.predict(X_test)
    
    # Calculate metrics
    acc = accuracy_score(y_test, y_pred)
    prec, rec, f1, _ = precision_recall_fscore_support(y_test, y_pred, average='weighted')
    
    print("\n" + "="*60)
    print("TEST SET PERFORMANCE:")
    print("="*60)
    print(f"Accuracy:  {acc:.4f} ({acc*100:.2f}%)")
    print(f"Precision: {prec:.4f}")
    print(f"Recall:    {rec:.4f}")
    print(f"F1-Score:  {f1:.4f}")
    
    print("\nPer-Class Metrics:")
    print(classification_report(y_test, y_pred, target_names=['Weak', 'Moderate', 'Strong']))
    
    # Save confusion matrix
    plt.figure(figsize=(8, 6))
    conf_mat = confusion_matrix(y_test, y_pred)
    sns.heatmap(conf_mat, annot=True, fmt='d', cmap='Blues',
                xticklabels=['Weak', 'Moderate', 'Strong'],
                yticklabels=['Weak', 'Moderate', 'Strong'])
    plt.title(f'Confusion Matrix - {dataset_name}')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    plt.savefig(f'results/confusion_matrix_{dataset_name}.png')
    plt.close()
    
    # Feature importance
    if hasattr(ensemble.estimators_[0], 'feature_importances_'):
        plt.figure(figsize=(12, 6))
        importances = ensemble.estimators_[0].feature_importances_
        feat_imp = pd.DataFrame({'feature': X_train.columns, 'importance': importances})
        feat_imp = feat_imp.sort_values('importance', ascending=False).head(20)
        
        sns.barplot(x='importance', y='feature', data=feat_imp)
        plt.title(f'Top 20 Feature Importance - {dataset_name}')
        plt.tight_layout()
        plt.savefig(f'results/feature_importance_{dataset_name}.png')
        plt.close()
    
    # Save model
    joblib.dump(ensemble, f'models/model_{dataset_name}.pkl')
    
    # Compare with baselines
    print("\n" + "="*60)
    print("BASELINE MODEL COMPARISON:")
    print("="*60)
    
    baselines = {
        'Naive Bayes': GaussianNB(),
        'Decision Tree': DecisionTreeClassifier(random_state=42),
        'SVM': SVC(kernel='rbf', random_state=42),
        'Logistic Regression': LogisticRegression(random_state=42)
    }
    
    baseline_scores = {}
    for name, model in baselines.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        b_acc = accuracy_score(y_test, y_pred)
        _, _, b_f1, _ = precision_recall_fscore_support(y_test, y_pred, average='weighted')
        baseline_scores[name] = {'accuracy': b_acc, 'f1': b_f1}
        print(f"{name:<20} - Accuracy: {b_acc:.4f}, F1: {b_f1:.4f}")
    
    # Add ensemble scores
    baseline_scores['Ensemble (Ours)'] = {'accuracy': acc, 'f1': f1}
    print(f"{'Ensemble (Ours)':<20} - Accuracy: {acc:.4f}, F1: {f1:.4f}")
    
    # Calculate improvement
    baseline_avg = np.mean([s['accuracy'] for s in baseline_scores.values()])
    improvement = ((acc - baseline_avg) / baseline_avg) * 100
    print(f"\nImprovement over baseline average: {improvement:+.2f}%")
    
    # Save model comparison plot
    plt.figure(figsize=(10, 6))
    model_names = list(baseline_scores.keys())
    accuracies = [baseline_scores[m]['accuracy'] for m in model_names]
    f1_scores = [baseline_scores[m]['f1'] for m in model_names]
    
    x = np.arange(len(model_names))
    width = 0.35
    
    plt.bar(x - width/2, accuracies, width, label='Accuracy')
    plt.bar(x + width/2, f1_scores, width, label='F1-Score')
    plt.xlabel('Model')
    plt.ylabel('Score')
    plt.title(f'Model Comparison - {dataset_name}')
    plt.xticks(x, model_names, rotation=45, ha='right')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'results/model_comparison_{dataset_name}.png')
    plt.close()
    
    return {
        'dataset': dataset_name,
        'train_samples': len(X_train),
        'test_samples': len(X_test),
        'features': X_train.shape[1],
        'accuracy': acc,
        'precision': prec,
        'recall': rec,
        'f1_score': f1,
        'cv_f1_mean': cv_scores.mean(),
        'cv_f1_std': cv_scores.std(),
        'improvement': improvement,
        'baseline_avg': baseline_avg
    }

def main():
    """Train models on all datasets"""
    
    results = []
    
    for dataset in ['UCI', 'AI', 'OU']:  # Added OU dataset
        try:
            result = train_and_evaluate_dataset(dataset)
            results.append(result)
        except Exception as e:
            print(f"\nError processing {dataset} dataset: {str(e)}")
    
    # Create summary DataFrame
    summary_df = pd.DataFrame(results)
    summary_df.to_csv('results/final_results_summary.csv', index=False)
    
    # Print final summary
    print("\n" + "="*60)
    print("FINAL RESULTS SUMMARY")
    print("="*60 + "\n")
    pd.set_option('display.max_columns', None)
    print(summary_df)
    
    # Create combined performance chart
    plt.figure(figsize=(12, 6))
    
    x = np.arange(len(results))
    width = 0.15
    metrics = ['accuracy', 'precision', 'recall', 'f1_score']
    
    for i, metric in enumerate(metrics):
        values = [r[metric] for r in results]
        plt.bar(x + i*width, values, width, label=metric.capitalize())
    
    plt.xlabel('Dataset')
    plt.ylabel('Score')
    plt.title('Performance Metrics Across Datasets')
    plt.xticks(x + width*1.5, [r['dataset'] for r in results])
    plt.legend()
    plt.tight_layout()
    plt.savefig('results/combined_performance.png')
    plt.close()

if __name__ == "__main__":
    main()