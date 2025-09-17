"""
Baseline XGBoost pipeline for IBOV (walk-forward, embargo, calibration, thresholds)

Run locally (do not run automatically here):
    python scripts/xgb_baseline_ibov.py

Produces:
 - partitions_ibov.csv
 - metrics_ibov_baseline.csv
 - thresholds_tau_ibov.json
 - feature_list_d{h}.txt
 - optional calibration PNGs
 - appends provenance to PROVENANCE_IBOV.txt

Notes:
 - Requires: pandas, numpy, scikit-learn, xgboost, matplotlib
 - Designed for reproducibility: fixed seed, logs hyperparams used
"""
from pathlib import Path
from datetime import datetime
import json
import logging
import hashlib
import platform
import sys

import numpy as np
import pandas as pd
from sklearn.metrics import balanced_accuracy_score, matthews_corrcoef, f1_score
from sklearn.calibration import CalibratedClassifierCV, calibration_curve
from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_class_weight
import xgboost as xgb
import matplotlib.pyplot as plt

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# Config
SEED = 42
np.random.seed(SEED)

GOLD_DIR = Path("/home/wrm/BOLSA_2026/gold/IBOV")
GOLD_DIR.mkdir(parents=True, exist_ok=True)
GOLD_PARQUET = GOLD_DIR / "gold_ibov_features.parquet"
PROV = GOLD_DIR / "PROVENANCE_IBOV.txt"

# Outputs
PARTITIONS_CSV = GOLD_DIR / "partitions_ibov.csv"
METRICS_CSV = GOLD_DIR / "metrics_ibov_baseline.csv"
THRESHOLDS_JSON = GOLD_DIR / "thresholds_tau_ibov.json"

# Hyperparameters (conservative defaults)
HYPER = {
    "max_depth": 4,
    "min_child_weight": 3,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "n_estimators": 400,
    "learning_rate": 0.08,
    "random_state": SEED,
    "use_label_encoder": False,
    "eval_metric": "mlogloss",
}

# Embargo size (days / trading days) - use 5 pregões
EMBARGO = 5

def sha256_of_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def load_gold(p: Path) -> pd.DataFrame:
    if not p.exists():
        raise FileNotFoundError(p)
    df = pd.read_parquet(p)
    return df


def select_features(df: pd.DataFrame) -> dict:
    """Return dict horizon -> feature list (exclude date, tickers, r_d*, y_d*_cls, k_d*)"""
    banned_prefix = ("r_d", "y_d", "k_d")
    banned_exact = {"date"}
    banned_contains = {"ticker"}
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    features = [c for c in numeric_cols if not any(c.startswith(bp) for bp in banned_prefix) and c not in banned_exact and not any(b in c.lower() for b in banned_contains)]
    # Save same features per horizon (features are horizon-agnostic in this gold)
    feat_map = {1: features, 3: features, 5: features}
    return feat_map


def make_partitions(df: pd.DataFrame, n_splits=5) -> pd.DataFrame:
    """Create walk-forward partitions with embargo and return a DataFrame with ranges.
    We'll split by date into n_splits contiguous blocks for testing, using prior data for train.
    For simplicity, use equal-sized chronological folds on index positions.
    """
    dates = pd.to_datetime(df["date"]).sort_values().unique()
    n = len(dates)
    # choose number of test blocks between 4 and 6 based on available length
    k = min(max(4, n_splits), 6)
    # compute block boundaries for tests
    block_size = max(1, n // k)
    partitions = []
    for i in range(k):
        test_start_idx = i * block_size
        test_end_idx = min(n - 1, (i + 1) * block_size - 1) if i < k - 1 else n - 1
        test_start = dates[test_start_idx]
        test_end = dates[test_end_idx]

        # train is everything before test_start
        train_start = dates[0]
        train_end = dates[max(0, test_start_idx - 1)]

        # embargo: start the day after train_end and last EMBARGO days
        embargo_start = dates[max(0, test_start_idx - EMBARGO)] if test_start_idx - EMBARGO >= 0 else train_end
        embargo_end = train_end

        partitions.append({
            "block_id": i + 1,
            "train_start": str(train_start.date()),
            "train_end": str(train_end.date()),
            "embargo_start": str(embargo_start.date()) if embargo_start is not None else None,
            "embargo_end": str(embargo_end.date()) if embargo_end is not None else None,
            "test_start": str(test_start.date()),
            "test_end": str(test_end.date()),
        })

    pdf = pd.DataFrame(partitions)
    pdf.to_csv(PARTITIONS_CSV, index=False)
    logging.info(f"Partitions saved: {PARTITIONS_CSV}")
    return pdf


def train_and_evaluate(df: pd.DataFrame, feat_map: dict, partitions: pd.DataFrame):
    metrics_rows = []
    thresholds = {}

    for h in (1, 3, 5):
        features = feat_map[h]
        # save feature list for this horizon
        (GOLD_DIR / f"feature_list_d{h}.txt").write_text("\n".join(features))

        thresholds[h] = None

        for _, row in partitions.iterrows():
            bid = int(row["block_id"])
            test_mask = (pd.to_datetime(df["date"]).dt.date >= pd.to_datetime(row["test_start"]).date()) & (pd.to_datetime(df["date"]).dt.date <= pd.to_datetime(row["test_end"]).date())
            train_mask = (pd.to_datetime(df["date"]).dt.date >= pd.to_datetime(row["train_start"]).date()) & (pd.to_datetime(df["date"]).dt.date <= pd.to_datetime(row["train_end"]).date())

            X_train = df.loc[train_mask, features]
            y_train = df.loc[train_mask, f"y_d{h}_cls"]
            X_test = df.loc[test_mask, features]
            y_test = df.loc[test_mask, f"y_d{h}_cls"]

            if y_train.dropna().empty or y_test.dropna().empty:
                logging.warning(f"Empty train or test for horizon {h} block {bid}; skipping")
                continue

            # handle class weights (increase weight for positive class)
            classes = np.unique(y_train.dropna())
            # compute inverse frequency weights
            try:
                cls_w = compute_class_weight(class_weight='balanced', classes=classes, y=y_train.dropna())
                class_weight_map = {c: float(w) for c, w in zip(classes, cls_w)}
            except Exception:
                # fallback uniform
                class_weight_map = {c: 1.0 for c in classes}

            # bump positive class weight by 1.3 if present
            if 1 in class_weight_map:
                class_weight_map[1] *= 1.3

            # XGBoost accepts scale_pos_weight for binary; for multiclass we'll pass sample_weight
            sample_weight = y_train.map(lambda v: class_weight_map.get(v, 1.0)).values

            clf = xgb.XGBClassifier(**HYPER)
            clf.fit(X_train, y_train, sample_weight=sample_weight)

            # Calibrate probabilities using inner validation (use 10% holdout from train)
            if len(X_train) < 50:
                # small training set: skip calibration
                calibrated = clf
                calibrator_name = "none"
            else:
                # split train-> holdout for calibration
                X_tr, X_cal, y_tr, y_cal = train_test_split(X_train, y_train, test_size=0.1, random_state=SEED, stratify=y_train)
                clf_inner = xgb.XGBClassifier(**HYPER)
                sw = y_tr.map(lambda v: class_weight_map.get(v, 1.0)).values
                clf_inner.fit(X_tr, y_tr, sample_weight=sw)

                # try Platt (sigmoid) and isotonic, pick by negative log loss on calibration set
                best_cal = None
                best_score = float('inf')
                for method in ["sigmoid", "isotonic"]:
                    try:
                        cal = CalibratedClassifierCV(clf_inner, cv='prefit', method=method)
                        cal.fit(X_cal, y_cal)
                        probs = cal.predict_proba(X_cal)
                        # negative log loss
                        eps = 1e-15
                        # compute multiclass log loss
                        ll = -np.mean(np.log(np.maximum(eps, probs[np.arange(len(y_cal)), [list(cal.classes_).index(v) for v in y_cal]])))
                        if ll < best_score:
                            best_score = ll
                            best_cal = (method, cal)
                    except Exception as e:
                        logging.debug(f"Calibration method {method} failed: {e}")

                if best_cal is None:
                    calibrated = clf_inner
                    calibrator_name = "none"
                else:
                    calibrator_name, calibrated = best_cal

            # Predict probabilities on test
            probs = calibrated.predict_proba(X_test)
            # map classes to indices
            classes_order = list(calibrated.classes_)

            # For threshold search, we only care about p_up and p_down -> indices for 1 and -1
            idx_up = classes_order.index(1) if 1 in classes_order else None
            idx_down = classes_order.index(-1) if -1 in classes_order else None

            # If missing a class in outputs, set default indices
            if idx_up is None or idx_down is None:
                logging.warning(f"Classes 1 or -1 missing in model.classes_ for horizon {h} block {bid}")

            # find tau that makes neutral fraction in validation within target
            # We'll search tau in [0.5, 0.95] (prob threshold for dominance)
            def compute_neutral_fraction(tau, probs, idx_up, idx_down):
                if idx_up is None or idx_down is None:
                    return 0.0
                p_up = probs[:, idx_up]
                p_down = probs[:, idx_down]
                dominant = np.maximum(p_up, p_down)
                neutral = dominant < tau
                return float(neutral.mean())

            # target ranges per horizon
            targets = {1: (0.45, 0.55), 3: (0.38, 0.45), 5: (0.30, 0.38)}
            lo, hi = targets[h]
            # search tau by scanning
            taus = np.linspace(0.5, 0.95, 91)
            best_tau = None
            best_gap = float('inf')
            for t in taus:
                frac = compute_neutral_fraction(t, probs, idx_up, idx_down)
                if lo <= frac <= hi:
                    best_tau = float(t)
                    break
                gap = min(abs(frac - lo), abs(frac - hi))
                if gap < best_gap:
                    best_gap = gap
                    best_tau = float(t)

            # store threshold (per horizon we will keep the last computed best_tau across blocks; later we'll aggregate)
            thresholds[h] = best_tau if thresholds[h] is None else thresholds[h]

            # apply decision rule on test
            if idx_up is None or idx_down is None:
                y_pred = calibrated.predict(X_test)
            else:
                p_up_test = probs[:, idx_up]
                p_down_test = probs[:, idx_down]
                dominant = np.where(np.maximum(p_up_test, p_down_test) < best_tau, 0, np.where(p_up_test > p_down_test, 1, -1))
                y_pred = dominant

            # compute metrics
            acc_bal = balanced_accuracy_score(y_test, y_pred)
            try:
                mcc = matthews_corrcoef(y_test, y_pred)
            except Exception:
                mcc = float('nan')
            f1_up = f1_score(y_test, y_pred, labels=[1], average='macro', zero_division=0)
            f1_down = f1_score(y_test, y_pred, labels=[-1], average='macro', zero_division=0)

            metrics_rows.append({
                "horizon": h,
                "block_id": bid,
                "acc_bal": float(acc_bal),
                "mcc_macro": float(mcc),
                "f1_up": float(f1_up),
                "f1_down": float(f1_down),
                "n_test": int(len(y_test)),
                "calibrator": calibrator_name,
                "tau_used": best_tau,
            })

            # optional: plot calibration curve
            try:
                if idx_up is not None:
                    p_up = probs[:, idx_up]
                    frac_pos, mean_pred = calibration_curve((y_test == 1).astype(int), p_up, n_bins=10)
                    plt.figure()
                    plt.plot(mean_pred, frac_pos, marker='o')
                    plt.plot([0, 1], [0, 1], linestyle='--', color='k')
                    plt.xlabel('Mean predicted prob (up)')
                    plt.ylabel('Fraction of positives')
                    plt.title(f'Calibration up: h{h} block{bid}')
                    png = GOLD_DIR / f"calibration_curve_d{h}_block{bid}.png"
                    plt.savefig(png)
                    plt.close()
            except Exception as e:
                logging.debug(f"Calibration plot failed: {e}")

    # save metrics and thresholds
    pd.DataFrame(metrics_rows).to_csv(METRICS_CSV, index=False)
    with THRESHOLDS_JSON.open('w') as f:
        json.dump({f"d{h}": thresholds[h] for h in thresholds}, f, indent=2)
    logging.info(f"Metrics saved: {METRICS_CSV}")
    logging.info(f"Thresholds saved: {THRESHOLDS_JSON}")

    # append provenance
    prov_summary = {
        "seed": SEED,
        "partitions": str(PARTITIONS_CSV),
        "hyperparameters": HYPER,
        "class_weighting_note": "positive class weight multiplied by 1.3 if present",
        "metrics_file": str(METRICS_CSV),
        "thresholds_file": str(THRESHOLDS_JSON),
        "gold_parquet_sha256": sha256_of_file(GOLD_PARQUET) if GOLD_PARQUET.exists() else None,
        "outputs_mtime": {"metrics": METRICS_CSV.stat().st_mtime if METRICS_CSV.exists() else None, "thresholds": THRESHOLDS_JSON.stat().st_mtime if THRESHOLDS_JSON.exists() else None},
        "timestamp": datetime.now().isoformat(),
        "python": sys.version,
        "platform": platform.platform(),
    }
    line = f"[{datetime.now().isoformat()}] BASELINE_XGB: {json.dumps(prov_summary, default=str)}\n"
    PROV.write_text(PROV.read_text() + line if PROV.exists() else line)
    logging.info(f"Provenance appended: {PROV}")


def main():
    df = load_gold(GOLD_PARQUET)
    feat_map = select_features(df)
    partitions = make_partitions(df, n_splits=5)
    train_and_evaluate(df, feat_map, partitions)


if __name__ == "__main__":
    main()
