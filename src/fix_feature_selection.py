"""
Remove target leakage features before training
"""
import pandas as pd
from pathlib import Path
import sys

def remove_leakage_features(dataset_name):
    """Remove features that leak target information"""
    try:
        base_dir = Path(__file__).parent.parent
        train_path = base_dir / 'data' / 'processed' / f'{dataset_name}_train_fixed.csv'
        test_path = base_dir / 'data' / 'processed' / f'{dataset_name}_test_fixed.csv'
        
        if not train_path.exists():
            print(f"Error: {train_path} does not exist!")
            return
        if not test_path.exists():
            print(f"Error: {test_path} does not exist!")
            return
    
        # Load data
        train_df = pd.read_csv(train_path)
        test_df = pd.read_csv(test_path)
        
        print(f"\n{'='*50}")
        print(f"Fixing {dataset_name} dataset")
        print(f"{'='*50}")
        
        print(f"Original features: {train_df.shape[1]}")
        print(f"Features: {list(train_df.columns)}")
        
        # Features to remove (these leak the target)
        if dataset_name == 'UCI':
            leakage_features = ['G1', 'G2', 'G3']  # G1, G2, G3 are grades
        elif dataset_name == 'AI':
            # All score and performance-related columns
            leakage_features = ['Total', 'Quiz 1', 'Quiz 2', 'Quiz 3', 'Quiz 4', 
                              'Midterm Exam', 'Final Exam', 'Project', 
                              'Total Score', 'Total Grade']  
        else:  # OU
            # Need to check what OU has, but remove all assessment scores and grades
            score_grade_features = [col for col in train_df.columns 
                                  if any(term in col.lower() 
                                        for term in ['score', 'grade', 'mark', 'exam', 'assessment'])]
            leakage_features = score_grade_features
    
        print(f"\nRemoving leakage features: {leakage_features}")
        
        # Remove leakage features
        train_df_clean = train_df.drop(columns=[f for f in leakage_features if f in train_df.columns])
        test_df_clean = test_df.drop(columns=[f for f in leakage_features if f in test_df.columns])
        
        # Make sure weakness_level is kept
        if 'weakness_level' not in train_df_clean.columns:
            train_df_clean['weakness_level'] = train_df['weakness_level']
        if 'weakness_level' not in test_df_clean.columns:
            test_df_clean['weakness_level'] = test_df['weakness_level']
        
        print(f"\nRemaining features: {train_df_clean.shape[1]}")
        print("Features:", ", ".join(list(train_df_clean.columns)))
        
        # Save cleaned data
        output_train = base_dir / 'data' / 'processed' / f'{dataset_name}_train_clean.csv'
        output_test = base_dir / 'data' / 'processed' / f'{dataset_name}_test_clean.csv'
        
        train_df_clean.to_csv(output_train, index=False)
        test_df_clean.to_csv(output_test, index=False)
        print(f"\nSuccessfully saved cleaned data:")
        print(f"  {output_train}")
        print(f"  {output_test}")
        
    except Exception as e:
        print(f"Error processing {dataset_name} dataset: {str(e)}", file=sys.stderr)

if __name__ == "__main__":
    try:
        for dataset in ['UCI', 'AI', 'OU']:
            remove_leakage_features(dataset)
    except Exception as e:
        print(f"Error processing datasets: {str(e)}", file=sys.stderr)
        sys.exit(1)