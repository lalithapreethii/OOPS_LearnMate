"""
Run preprocessing with fixed temporal validation
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

from src.preprocessor.uci import UCIPreprocessor
from src.preprocessor.ai import AIPreprocessor

def main():
    print("="*70)
    print("RUNNING FIXED PREPROCESSING WITH TEMPORAL VALIDATION")
    print("="*70)
    
    # ========================================
    # UCI Dataset - Mid-term Prediction (G3)
    # ========================================
    print("\n" + "="*70)
    print("1. UCI DATASET - Predicting G3 using G1 and G2")
    print("="*70)
    
    try:
        uci_processor = UCIPreprocessor(prediction_grade='G3')
        uci_train, uci_test = uci_processor.preprocess()
        
        print(f"\n✅ UCI preprocessing complete!")
        print(f"   Train samples: {len(uci_train)}")
        print(f"   Test samples: {len(uci_test)}")
        print(f"   Features: {uci_train.shape[1] - 1}")  # Minus target
        print(f"   Files saved:")
        print(f"   - data/processed/UCI_train.csv")
        print(f"   - data/processed/UCI_test.csv")
        
    except Exception as e:
        print(f"\n❌ Error processing UCI dataset: {e}")
        import traceback
        traceback.print_exc()
    
    # ========================================
    # AI Dataset - Midterm Prediction
    # ========================================
    print("\n" + "="*70)
    print("2. AI DATASET - Predicting final using midterm assessments")
    print("="*70)
    
    try:
        ai_processor = AIPreprocessor(prediction_point='midterm')
        ai_train, ai_test = ai_processor.preprocess()
        
        print(f"\n✅ AI preprocessing complete!")
        print(f"   Train samples: {len(ai_train)}")
        print(f"   Test samples: {len(ai_test)}")
        print(f"   Features: {ai_train.shape[1] - 1}")  # Minus target
        print(f"   Files saved:")
        print(f"   - data/processed/AI_train.csv")
        print(f"   - data/processed/AI_test.csv")
        
    except Exception as e:
        print(f"\n❌ Error processing AI dataset: {e}")
        import traceback
        traceback.print_exc()
    
    # ========================================
    # Summary
    # ========================================
    print("\n" + "="*70)
    print("PREPROCESSING COMPLETE")
    print("="*70)
    print("\nNext steps:")
    print("1. Check data/processed/ for the new train/test files")
    print("2. Review reports/ for preprocessing reports")
    print("3. Run training with: python src/train_models_clean.py")
    print("\n" + "="*70)

if __name__ == "__main__":
    main()