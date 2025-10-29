"""
Train models on CLEAN datasets (without target leakage)
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

def train_and_evaluate_dataset(dataset_name, train_path, test_path):
    """Train and evaluate model on a single dataset"""
    
    print(f"\n{'='*60}")
    print(f"Training and evaluating {dataset_name} dataset")
    print(f"{'='*60}")
    
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
    
    # Check for any remaining issues
    if X_train.isnull().sum().sum() > 0:
        print("\nWarning: Found NaN values, filling with 0")
        X_train = X_train.fillna(0)
        X_test = X_test.fillna(0)
    
    # Build ensemble model with reduced complexity to avoid overfitting
    rf = RandomForestClassifier(
        n_estimators=100,
        max_depth=5,           # Reduced to prevent overfitting
        min_samples_split=10,  # Increased to prevent overfitting
        min_samples_leaf=5,    # Increased to prevent overfitting
        class_weight='balanced',
        random_state=42,
        n_jobs=-1
    )
    
    xgb = XGBClassifier(
        n_estimators=100,
        max_depth=3,           # Reduced to prevent overfitting
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42
    )
    
    ensemble = VotingClassifier(
        estimators=[('rf', rf), ('xgb', xgb)],
        voting='soft',
        weights=[0.6, 0.4]
    )
    
    # Cross-validation on training data
    print(f"\nPerforming 5-fold cross-validation...")
    cv_scores = cross_val_score(ensemble, X_train, y_train, cv=5, 
                                scoring='f1_weighted', n_jobs=-1)
    print(f"Cross-Validation F1 Scores: {cv_scores}")
    print(f"Mean CV F1: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
    
    # Train on full training set
    print(f"\nTraining final model...")
    ensemble.fit(X_train, y_train)
    
    # Predict on test set
    y_pred = ensemble.predict(X_test)
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision, recall, f1, support = precision_recall_fscore_support(
        y_test, y_pred, average='weighted', zero_division=0
    )
    
    print(f"\n{'='*60}")
    print(f"TEST SET PERFORMANCE:")
    print(f"{'='*60}")
    print(f"Accuracy:  {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1-Score:  {f1:.4f}")
    
    print(f"\nPer-Class Metrics:")
    print(classification_report(y_test, y_pred, 
                               target_names=['Weak', 'Moderate', 'Strong'],
                               zero_division=0))
    
    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
               xticklabels=['Weak', 'Moderate', 'Strong'],
               yticklabels=['Weak', 'Moderate', 'Strong'])
    plt.title(f'Confusion Matrix - {dataset_name} Dataset')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    
    results_dir = Path('results')
    results_dir.mkdir(exist_ok=True)
    plt.savefig(results_dir / f'confusion_matrix_{dataset_name}.png', 
               dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved confusion matrix to results/confusion_matrix_{dataset_name}.png")
    
    # Feature Importance (from Random Forest)
    rf_model = ensemble.estimators_[0]
    importances = rf_model.feature_importances_
    feature_names = X_train.columns
    indices = np.argsort(importances)[::-1][:10]
    
    plt.figure(figsize=(10, 6))
    plt.barh(range(min(10, len(indices))), importances[indices])
    plt.yticks(range(min(10, len(indices))), [feature_names[i] for i in indices])
    plt.xlabel('Feature Importance')
    plt.title(f'Top 10 Important Features - {dataset_name}')
    plt.tight_layout()
    plt.savefig(results_dir / f'feature_importance_{dataset_name}.png',
               dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved feature importance to results/feature_importance_{dataset_name}.png")
    
    # Save model
    models_dir = Path('models')
    models_dir.mkdir(exist_ok=True)
    joblib.dump(ensemble, models_dir / f'model_{dataset_name}_clean.pkl')
    print(f"Model saved as models/model_{dataset_name}_clean.pkl")
    
    # Train baseline models for comparison
    print(f"\n{'='*60}")
    print(f"BASELINE MODEL COMPARISON:")
    print(f"{'='*60}")
    
    baselines = {
        'Naive Bayes': GaussianNB(),
        'Decision Tree': DecisionTreeClassifier(max_depth=5, random_state=42),
        'SVM': SVC(kernel='rbf', probability=True, random_state=42),
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42)
    }
    
    baseline_results = {}
    for name, model in baselines.items():
        model.fit(X_train, y_train)
        y_pred_baseline = model.predict(X_test)
        acc_baseline = accuracy_score(y_test, y_pred_baseline)
        f1_baseline = precision_recall_fscore_support(
            y_test, y_pred_baseline, average='weighted', zero_division=0
        )[2]
        baseline_results[name] = {'accuracy': acc_baseline, 'f1': f1_baseline}
        print(f"{name:20s} - Accuracy: {acc_baseline:.4f}, F1: {f1_baseline:.4f}")
    
    baseline_results['Ensemble (Ours)'] = {'accuracy': accuracy, 'f1': f1}
    print(f"{'Ensemble (Ours)':20s} - Accuracy: {accuracy:.4f}, F1: {f1:.4f}")
    
    # Calculate improvement
    baseline_f1_scores = [v['f1'] for k, v in baseline_results.items() if k != 'Ensemble (Ours)']
    avg_baseline = np.mean(baseline_f1_scores)
    improvement = ((f1 - avg_baseline) / avg_baseline) * 100
    print(f"\nImprovement over baseline average: {improvement:+.2f}%")
    
    # Model comparison chart
    plt.figure(figsize=(10, 6))
    models = list(baseline_results.keys())
    f1_scores = [v['f1'] for v in baseline_results.values()]
    colors = ['lightblue'] * (len(models) - 1) + ['green']
    
    bars = plt.bar(models, f1_scores, color=colors)
    plt.ylabel('F1-Score')
    plt.title(f'Model Comparison - {dataset_name} Dataset')
    plt.ylim([0, 1])
    plt.xticks(rotation=45, ha='right')
    
    for i, (bar, score) in enumerate(zip(bars, f1_scores)):
        plt.text(bar.get_x() + bar.get_width()/2, score + 0.02, 
                f'{score:.3f}', ha='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(results_dir / f'model_comparison_{dataset_name}.png',
               dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved model comparison to results/model_comparison_{dataset_name}.png")
    
    return {
        'dataset': dataset_name,
        'train_samples': len(X_train),
        'test_samples': len(X_test),
        'features': X_train.shape[1],
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'cv_f1_mean': cv_scores.mean(),
        'cv_f1_std': cv_scores.std(),
        'improvement': improvement,
        'baseline_avg': avg_baseline
    }

def main():
    """Main execution"""
    base_dir = Path('data') / 'processed'
    
    datasets = {
        'UCI': (base_dir / 'UCI_train_clean.csv', base_dir / 'UCI_test_clean.csv'),
        'AI': (base_dir / 'AI_train_clean.csv', base_dir / 'AI_test_clean.csv'),
        # Skip OU for now since it needs fixing
    }
    
    results = []
    
    for dataset_name, (train_path, test_path) in datasets.items():
        if not train_path.exists() or not test_path.exists():
            print(f"\nSkipping {dataset_name} - files not found")
            continue
        
        try:
            result = train_and_evaluate_dataset(dataset_name, train_path, test_path)
            results.append(result)
        except Exception as e:
            print(f"\nError processing {dataset_name}: {e}")
            import traceback
            traceback.print_exc()
    
    # Summary table
    if results:
        print(f"\n{'='*60}")
        print(f"FINAL RESULTS SUMMARY")
        print(f"{'='*60}\n")
        
        summary_df = pd.DataFrame(results)
        print(summary_df.to_string(index=False))
        
        # Save summary
        summary_df.to_csv('results/final_results_summary.csv', index=False)
        print(f"\nSummary saved to results/final_results_summary.csv")
        
        # Create combined visualization
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Accuracy comparison
        axes[0].bar(summary_df['dataset'], summary_df['accuracy'], color='steelblue')
        axes[0].set_ylabel('Accuracy')
        axes[0].set_title('Accuracy Across Datasets')
        axes[0].set_ylim([0, 1])
        for i, (dataset, acc) in enumerate(zip(summary_df['dataset'], summary_df['accuracy'])):
            axes[0].text(i, acc + 0.02, f'{acc:.3f}', ha='center', fontweight='bold')
        
        # F1-Score comparison
        axes[1].bar(summary_df['dataset'], summary_df['f1_score'], color='seagreen')
        axes[1].set_ylabel('F1-Score')
        axes[1].set_title('F1-Score Across Datasets')
        axes[1].set_ylim([0, 1])
        for i, (dataset, f1) in enumerate(zip(summary_df['dataset'], summary_df['f1_score'])):
            axes[1].text(i, f1 + 0.02, f'{f1:.3f}', ha='center', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('results/combined_performance.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("Saved combined performance chart to results/combined_performance.png")

if __name__ == "__main__":
    main()