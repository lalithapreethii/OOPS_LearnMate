import pandas as pd
from pathlib import Path

train_path = Path('data/processed/OU_train.csv')
test_path = Path('data/processed/OU_test.csv')

print('Reading:', train_path)
print('Reading:', test_path)

df_train = pd.read_csv(train_path)
df_test = pd.read_csv(test_path)

print('\nTRAIN shape:', df_train.shape)
print('TEST shape:', df_test.shape)

print('\nTRAIN columns (total {}):'.format(len(df_train.columns)))
print(list(df_train.columns))

has_target_train = 'weakness_level' in df_train.columns
has_target_test = 'weakness_level' in df_test.columns
print('\n"weakness_level" in train columns:', has_target_train)
print('"weakness_level" in test columns:', has_target_test)

# Features used (train_models drops 'weakness_level')
feature_cols = [c for c in df_train.columns if c != 'weakness_level'] if has_target_train else list(df_train.columns)
print('\nNumber of feature columns (train):', len(feature_cols))
print('First 40 feature columns:', feature_cols[:40])

# Potential ID columns
id_like = [c for c in df_train.columns if ('id' in c.lower() or 'student' in c.lower())]
print('\nPotential ID-like columns:', id_like)

# Check if any feature column is literally named the target
if 'weakness_level' in feature_cols:
    print('\nERROR: target column found among feature columns!')

# Check if any feature column is identical to the target values
identical_to_target = []
if has_target_train:
    target_str = df_train['weakness_level'].astype(str)
    for c in feature_cols:
        try:
            col_str = df_train[c].astype(str)
            if col_str.equals(target_str):
                identical_to_target.append(c)
        except Exception:
            pass
print('\nColumns identical to target (train):', identical_to_target)

# Compute exact row overlap between train and test by hashing row-string
print('\nComputing exact row overlap (this compares entire rows as strings)...')
train_rows = df_train.astype(str).agg('|'.join, axis=1)
test_rows = df_test.astype(str).agg('|'.join, axis=1)
train_set = set(train_rows)
test_set = set(test_rows)
overlap = train_set & test_set
n_overlap = len(overlap)
print('Exact row overlap count:', n_overlap)
if n_overlap > 0:
    print('\nSample overlapping rows (joined-string representation, up to 5):')
    for i, r in enumerate(list(overlap)[:5]):
        print(f'{i+1}:', r)

# Check overlap on ID-like column(s) if present
if id_like:
    for idc in id_like:
        try:
            train_ids = set(df_train[idc].astype(str))
            test_ids = set(df_test[idc].astype(str))
            common_ids = train_ids & test_ids
            print(f'Overlap on ID column "{idc}":', len(common_ids))
            if len(common_ids) > 0:
                print('Sample overlapping IDs (up to 20):', list(common_ids)[:20])
        except Exception as e:
            print('Could not compare ID column', idc, 'error:', e)

# Check duplicates within train/test
n_dup_train = df_train.duplicated().sum()
n_dup_test = df_test.duplicated().sum()
print('\nDuplicate rows within TRAIN:', n_dup_train)
print('Duplicate rows within TEST:', n_dup_test)

print('\nDone.')
