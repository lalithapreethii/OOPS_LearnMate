import pandas as pd
from pathlib import Path

train_in = Path('data/processed/OU_train_noleak.csv')
test_in = Path('data/processed/OU_test_noleak.csv')
train_out = Path('data/processed/OU_train_noleak_noscore.csv')
test_out = Path('data/processed/OU_test_noleak_noscore.csv')

print('Loading cleaned files:')
print('-', train_in)
print('-', test_in)

df_train = pd.read_csv(train_in)
df_test = pd.read_csv(test_in)

print('Shapes before drop:', df_train.shape, df_test.shape)

cols_to_drop = []
for c in ['weakness_score', 'weakness score', 'score_weakness']:
    if c in df_train.columns:
        cols_to_drop.append(c)

if 'weakness_score' in df_train.columns:
    cols_to_drop.append('weakness_score')

cols_to_drop = list(dict.fromkeys(cols_to_drop))
print('Columns to drop if present:', cols_to_drop)

if cols_to_drop:
    for c in cols_to_drop:
        if c in df_train.columns:
            df_train = df_train.drop(columns=[c])
        if c in df_test.columns:
            df_test = df_test.drop(columns=[c])

print('Shapes after drop:', df_train.shape, df_test.shape)

train_out.parent.mkdir(parents=True, exist_ok=True)

# Save new files
df_train.to_csv(train_out, index=False)
df_test.to_csv(test_out, index=False)
print('Saved files:')
print('-', train_out, df_train.shape)
print('-', test_out, df_test.shape)

# Retrain
print('\nRetraining model without weakness_score...')
import sys
sys.path.insert(0, str(Path('.').resolve()))
from src import train_models

train_models.train_and_evaluate_dataset('OU_noleak_noscore', str(train_out), str(test_out))

print('\nDone retraining without weakness_score')
