from pathlib import Path
import pandas as pd
import hashlib
import os

p = Path('/home/wrm/BOLSA_2026/dados_originais/IBOV_2013-08-18_2025-09-17.parquet')
if not p.exists():
    print('Parquet not found:', p)
    raise SystemExit(1)

df = pd.read_parquet(p)
print('PATH:', p)
print('Exists:', p.exists())
print('Rows, cols:', df.shape)
print('Columns:', list(df.columns))

if 'date' in df.columns:
    try:
        rng_min = df['date'].min()
        rng_max = df['date'].max()
        print('Dataframe date range:', rng_min, '->', rng_max)
    except Exception as e:
        print('Could not compute date range:', e)

if 'date' in df.columns:
    dup_dates = df['date'].duplicated().sum()
    print('Duplicate rows by date:', dup_dates)

nans = df.isna().sum()
print('\nNaNs per column:')
for k,v in nans.items():
    print(f'  {k}: {v}')

m = hashlib.sha256(p.read_bytes()).hexdigest()
print('\nFile sha256:', m)
print('File mtime:', os.path.getmtime(p))

print('\nFirst 5 rows:')
print(df.head().to_string())

print('\nLast 5 rows:')
print(df.tail().to_string())
