"""
Validation script for Gold IBOV dataset.

Outputs:
 - gold/IBOV/validation_report_ibov.csv
 - gold/IBOV/label_stats_ibov.csv
 - appends a summary line to gold/IBOV/PROVENANCE_IBOV.txt

Run locally (no shell commands executed by the assistant):
    python scripts/validate_gold_ibov.py

This script performs checks requested in TASK-001 and writes results.
"""
from pathlib import Path
from datetime import datetime
import json
import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


# Paths (configurable)
GOLD_DIR = Path("/home/wrm/BOLSA_2026/gold/IBOV")
GOLD_PARQUET = GOLD_DIR / "gold_ibov_features.parquet"
GOLD_MANIFEST = GOLD_DIR / "gold_ibov_manifest.csv"
VALIDATION_REPORT = GOLD_DIR / "validation_report_ibov.csv"
LABEL_STATS = GOLD_DIR / "label_stats_ibov.csv"
PROV = GOLD_DIR / "PROVENANCE_IBOV.txt"


def load_gold(p: Path) -> pd.DataFrame:
    if not p.exists():
        raise FileNotFoundError(f"Gold parquet not found: {p}")
    logging.info(f"Loading gold parquet: {p}")
    return pd.read_parquet(p)


def basic_schema_checks(df: pd.DataFrame) -> dict:
    # expected key columns
    expected = ["date", "close", "volume"]
    res = {
        "present_columns": list(df.columns),
        "missing_columns": [],
        "n_rows": int(len(df)),
    }
    for c in expected:
        if c not in df.columns:
            res["missing_columns"].append(c)

    # date range and types
    try:
        dmin = pd.to_datetime(df["date"]).min()
        dmax = pd.to_datetime(df["date"]).max()
        res["date_min"] = dmin.strftime("%Y-%m-%d")
        res["date_max"] = dmax.strftime("%Y-%m-%d")
    except Exception:
        res["date_min"] = None
        res["date_max"] = None

    # NaNs per column
    nan_counts = df.isna().sum().to_dict()
    res["nan_counts"] = {k: int(v) for k, v in nan_counts.items()}

    # dtypes
    res["dtypes"] = {k: str(v) for k, v in df.dtypes.items()}

    return res


def check_label_cols(df: pd.DataFrame, h_set=(1, 3, 5)) -> dict:
    stats = {}
    for h in h_set:
        label_col = f"y_d{h}_cls"
        rcol = f"r_d{h}"
        stats[label_col] = {
            "present": label_col in df.columns,
            "missing": int(df[label_col].isna().sum()) if label_col in df.columns else None,
        }
        stats[rcol] = {
            "present": rcol in df.columns,
            "missing": int(df[rcol].isna().sum()) if rcol in df.columns else None,
        }
    return stats


def write_validation_report(report: dict, out: Path):
    # Flatten report to a row-friendly CSV
    flat = {}
    flat["n_rows"] = report.get("n_rows")
    flat["date_min"] = report.get("date_min")
    flat["date_max"] = report.get("date_max")
    flat["missing_columns"] = ";".join(report.get("missing_columns", []))
    # include nan counts as json string
    flat["nan_counts_json"] = json.dumps(report.get("nan_counts", {}))
    flat["dtypes_json"] = json.dumps(report.get("dtypes", {}))
    df = pd.DataFrame([flat])
    df.to_csv(out, index=False)
    logging.info(f"Validation report written: {out}")


def write_label_stats(df: pd.DataFrame, out: Path, h_set=(1, 3, 5)):
    rows = []
    for h in h_set:
        label_col = f"y_d{h}_cls"
        if label_col not in df.columns:
            rows.append({"h": h, "label": None, "count": None, "frac": None})
            continue
        counts = df[label_col].value_counts(dropna=False).to_dict()
        total = float(len(df))
        for lab, cnt in counts.items():
            rows.append({"h": h, "label": int(lab) if not pd.isna(lab) else None, "count": int(cnt), "frac": float(cnt / total)})
    outdf = pd.DataFrame(rows)
    outdf.to_csv(out, index=False)
    logging.info(f"Label stats written: {out}")


def append_provenance(prov_path: Path, summary: dict):
    line = f"[{datetime.now().isoformat()}] VALIDATION: {json.dumps(summary, default=str)}\n"
    prov_path.write_text(prov_path.read_text() + line if prov_path.exists() else line)
    logging.info(f"Appended provenance: {prov_path}")


def main():
    df = load_gold(GOLD_PARQUET)

    # Basic schema and sanity
    report = basic_schema_checks(df)

    # Check label columns
    label_checks = check_label_cols(df)
    report["label_checks"] = label_checks

    # Acceptance criteria: zero NaNs after trimming initial rolling window
    # Determine minimal window used in features (hardcoded same as build script)
    min_window = max(20, 15, 14)
    df_trim = df.iloc[min_window:].reset_index(drop=True)

    # Check NaNs in critical features after trimming
    critical = ["date", "close", "volume"] + [f"r_d{h}" for h in (1, 3, 5)] + [f"y_d{h}_cls" for h in (1, 3, 5)]
    nan_crit = {c: (int(df_trim[c].isna().sum()) if c in df_trim.columns else None) for c in critical}
    report["nan_critical_after_trim"] = nan_crit

    # Write validation report
    write_validation_report(report, VALIDATION_REPORT)

    # Write label stats (whole trimmed set)
    write_label_stats(df_trim, LABEL_STATS)

    # Check proportions against targets
    label_df = pd.read_csv(LABEL_STATS)
    summary = {"rows_trimmed": int(len(df_trim))}
    # compute fractions for h=1,3,5 neutrals (label==0)
    for h in (1, 3, 5):
        sub = label_df[label_df["h"] == h]
        zero_row = sub[sub["label"] == 0]
        frac_zero = float(zero_row["frac"].iloc[0]) if not zero_row.empty else 0.0
        summary[f"p_zero_d{h}"] = frac_zero

    append_provenance(PROV, summary)

    logging.info("Validation completed.")


if __name__ == "__main__":
    main()
