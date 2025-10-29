import pandas as pd
from pathlib import Path

train_path = Path('data/processed/OU_train.csv')
test_path = Path('data/processed/OU_test.csv')
train_out = Path('data/processed/OU_train_noleak.csv')
test_out = Path('data/processed/OU_test_noleak.csv')

print('Loading original files')
df_train = pd.read_csv(train_path)
df_test = pd.read_csv(test_path)

print('Original TRAIN shape:', df_train.shape)
print('Original TEST shape:', df_test.shape)

# Drop exact duplicate rows within each set
n_dup_train_before = df_train.duplicated().sum()
n_dup_test_before = df_test.duplicated().sum()

if n_dup_train_before > 0:
    df_train = df_train.drop_duplicates().reset_index(drop=True)
if n_dup_test_before > 0:
    df_test = df_test.drop_duplicates().reset_index(drop=True)

print('Duplicates removed from TRAIN:', n_dup_train_before)
print('Duplicates removed from TEST:', n_dup_test_before)
print('After dedupe TRAIN shape:', df_train.shape)
print('After dedupe TEST shape:', df_test.shape)

# Remove rows for overlapping id_student from both sets
id_col = None
for c in df_train.columns:
    if c.lower() == 'id_student' or 'id' in c.lower() and 'student' in c.lower():
        id_col = c
        break
if id_col is None:
    # fallback: try common id-like names
    for c in df_train.columns:
        if 'id' in c.lower():
            id_col = c
            break

print('Detected ID column:', id_col)

if id_col is not None:
    train_ids = set(df_train[id_col].astype(str))
    test_ids = set(df_test[id_col].astype(str))
    common_ids = train_ids & test_ids
    print('Common student IDs count:', len(common_ids))
    if len(common_ids) > 0:
        # Drop rows with these IDs from both sets
        df_train = df_train[~df_train[id_col].astype(str).isin(common_ids)].reset_index(drop=True)
        df_test = df_test[~df_test[id_col].astype(str).isin(common_ids)].reset_index(drop=True)
        print('Dropped rows with common IDs from both sets')
        print('After removing common IDs TRAIN shape:', df_train.shape)
        print('After removing common IDs TEST shape:', df_test.shape)
    else:
        print('No overlapping student IDs found')
else:
    print('No ID column detected; skipping ID-based overlap removal')

# Drop exact remaining full-row overlap if any (rare after ID removal)
train_rows = df_train.astype(str).agg('|'.join, axis=1)
test_rows = df_test.astype(str).agg('|'.join, axis=1)
train_set = set(train_rows)
test_set = set(test_rows)
overlap = train_set & test_set
print('Exact full-row overlap remaining count:', len(overlap))
if len(overlap) > 0:
    # Remove overlapping rows from train
    mask = ~train_rows.isin(overlap)
    df_train = df_train[mask.values].reset_index(drop=True)
    print('Removed overlapping full rows from TRAIN; new TRAIN shape:', df_train.shape)

# Finally drop id_col from saved features to avoid using it as a predictor
if id_col is not None and id_col in df_train.columns:
    df_train_noid = df_train.drop(columns=[id_col]).copy()
else:
    df_train_noid = df_train.copy()
if id_col is not None and id_col in df_test.columns:
    df_test_noid = df_test.drop(columns=[id_col]).copy()
else:
    df_test_noid = df_test.copy()

# Save cleaned files
train_out.parent.mkdir(parents=True, exist_ok=True)
test_out.parent.mkdir(parents=True, exist_ok=True)
df_train_noid.to_csv(train_out, index=False)
df_test_noid.to_csv(test_out, index=False)

print('Saved cleaned files:')
print(' -', train_out, df_train_noid.shape)
print(' -', test_out, df_test_noid.shape)

# Now run training using the existing training function
print('\nRunning training on cleaned files (this will print training logs)...')
import sys
sys.path.insert(0, str(Path('.').resolve()))
from src import train_models

train_models.train_and_evaluate_dataset('OU_noleak', str(train_out), str(test_out))

print('\nDone running training on cleaned files')
