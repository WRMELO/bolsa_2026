"""Download IBOV (^BVSP) daily history >=8 years and save bronze parquet + manifest.
Creates new files without overwriting existing ones. Writes manifest_bronze_ibov.csv in dados_originais/.
"""
import os
from pathlib import Path
import hashlib
import pandas as pd
import yfinance as yf
from datetime import date, timedelta

ROOT = Path("/home/wrm/BOLSA_2026")
DADOS = ROOT / "dados_originais"
DADOS.mkdir(parents=True, exist_ok=True)

TICKER = "^BVSP"
MIN_YEARS = 8
END = date.today()
START = END - timedelta(days=int(MIN_YEARS * 365.25) + 30)  # small buffer

# Filename pattern (do not overwrite existing history)
out_parquet = DADOS / f"IBOV_{START.isoformat()}_{END.isoformat()}.parquet"
manifest_csv = DADOS / "manifesto_dados_originais_bronze_ibov.csv"

if out_parquet.exists():
    print("Bronze parquet already exists:", out_parquet)
else:
    print(f"Downloading {TICKER} from {START} to {END}")
    df = yf.download(TICKER, start=START.isoformat(), end=(END + timedelta(days=1)).isoformat(), progress=False)
    if df.empty:
        raise SystemExit("No data downloaded for IBOV")
    df.index.name = 'date'
    df.reset_index(inplace=True)
    df['ticker'] = TICKER
    # Normalize column names to required schema if present
    rename_map = {}
    if 'Adj Close' in df.columns:
        rename_map['Adj Close'] = 'adj_close'
    if 'Close' in df.columns:
        rename_map['Close'] = 'close'
    if 'Open' in df.columns:
        rename_map['Open'] = 'open'
    if 'High' in df.columns:
        rename_map['High'] = 'high'
    if 'Low' in df.columns:
        rename_map['Low'] = 'low'
    if 'Volume' in df.columns:
        rename_map['Volume'] = 'volume'
    df.rename(columns=rename_map, inplace=True)
    # Ensure columns exist
    for c in ['date','open','high','low','close','adj_close','volume','ticker']:
        if c not in df.columns:
            df[c] = pd.NA
    # Save parquet
    df.to_parquet(out_parquet)
    # Write manifest (append)
    row = {
        'file': out_parquet.name,
        'ticker': TICKER,
        'date_min': df['date'].min().isoformat(),
        'date_max': df['date'].max().isoformat(),
        'rows': len(df),
        'source': 'yfinance',
    }
    # compute hash
    h = hashlib.sha256(out_parquet.read_bytes()).hexdigest()
    row['sha256'] = h
    # append to manifest CSV
    dfm = pd.DataFrame([row])
    if manifest_csv.exists():
        dfm.to_csv(manifest_csv, mode='a', header=False, index=False)
    else:
        dfm.to_csv(manifest_csv, index=False)
    print('Saved bronze parquet and updated manifest:', out_parquet, manifest_csv)
