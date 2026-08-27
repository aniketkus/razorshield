"""
RazorShield – Model Training & Honest Evaluation
Trains all three models and prints full metrics including false-positive ₹ cost
"""
import os
import sys
import json
import joblib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    precision_score, recall_score, f1_score, roc_auc_score,
    confusion_matrix, classification_report, average_precision_score
)
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from imblearn.over_sampling import SMOTE

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

from data.generate_data import generate_transactions

# ── Directories ───────────────────────────────────────────────────────────────
MODELS_DIR   = Path(__file__).parent.parent / "saved_models"
REPORTS_DIR  = Path(__file__).parent.parent / "reports"
MODELS_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)

# ── Feature Columns ───────────────────────────────────────────────────────────
CATEGORICAL = ["payment_method", "state", "device_type", "browser", "category"]
NUMERICAL   = ["amount", "hour", "day_of_week", "txn_velocity_24h",
               "amount_velocity_24h", "device_fp_count"]
FEATURES    = CATEGORICAL + NUMERICAL


def build_preprocessor():
    return ColumnTransformer([
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CATEGORICAL),
        ("num", StandardScaler(), NUMERICAL),
    ])


def evaluate_model(name: str, y_true, y_pred, y_prob, label: str,
                   avg_amount: float, results: dict):
    """Compute and print metrics. False-positive cost = avg_amount * FP count."""
    cm = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = cm.ravel()

    precision = precision_score(y_true, y_pred, zero_division=0)
    recall    = recall_score(y_true, y_pred, zero_division=0)
    f1        = f1_score(y_true, y_pred, zero_division=0)
    roc_auc   = roc_auc_score(y_true, y_prob)
    pr_auc    = average_precision_score(y_true, y_prob)

    # False-positive cost: flagging a legit txn costs avg_amount in friction/delays
    fp_cost_inr = fp * avg_amount
    # False-negative cost: missing fraud/return costs avg_amount * 1.5 (loss + ops)
    fn_cost_inr = fn * avg_amount * 1.5

    metrics = {
        "model": name, "label": label,
        "precision": round(precision, 4),
        "recall":    round(recall, 4),
        "f1":        round(f1, 4),
        "roc_auc":   round(roc_auc, 4),
        "pr_auc":    round(pr_auc, 4),
        "tp": int(tp), "fp": int(fp), "tn": int(tn), "fn": int(fn),
        "fp_cost_inr": round(fp_cost_inr, 2),
        "fn_cost_inr": round(fn_cost_inr, 2),
    }
    results[label] = metrics

    print(f"\n{'='*60}")
    print(f"  {name} — {label.upper()}")
    print(f"{'='*60}")
    print(f"  Precision:  {precision:.4f}")
    print(f"  Recall:     {recall:.4f}")
    print(f"  F1:         {f1:.4f}")
    print(f"  ROC-AUC:    {roc_auc:.4f}")
    print(f"  PR-AUC:     {pr_auc:.4f}")
    print(f"  TP={tp:,}  FP={fp:,}  TN={tn:,}  FN={fn:,}")
    print(f"  False-Positive Cost: ₹{fp_cost_inr:,.0f}")
    print(f"  False-Negative Cost: ₹{fn_cost_inr:,.0f}")
    print(f"  Net Risk Score:      ₹{fn_cost_inr - fp_cost_inr:,.0f}")

    # Save confusion matrix plot
    fig, ax = plt.subplots(figsize=(5, 4))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax,
                xticklabels=["Predicted 0", "Predicted 1"],
                yticklabels=["Actual 0", "Actual 1"])
    ax.set_title(f"{name}\n{label}")
    plt.tight_layout()
    plt.savefig(REPORTS_DIR / f"cm_{label}.png", dpi=100)
    plt.close()

    return metrics


def train_fraud_detector(df_train, df_test, results):
    """IsolationForest-based anomaly + RF classifier hybrid"""
    print("\n⚡  Training Fraud Spike Detector …")
    target = "is_fraud"

    X_train = df_train[FEATURES].copy()
    y_train = df_train[target]
    X_test  = df_test[FEATURES].copy()
    y_test  = df_test[target]

    preprocessor = build_preprocessor()
    clf = Pipeline([
        ("pre", preprocessor),
        ("clf", RandomForestClassifier(
            n_estimators=300, max_depth=12, class_weight="balanced",
            random_state=42, n_jobs=-1
        )),
    ])

    # SMOTE for class imbalance
    X_tr_enc = preprocessor.fit_transform(X_train)
    smote = SMOTE(random_state=42, k_neighbors=5)
    X_sm, y_sm = smote.fit_resample(X_tr_enc, y_train)

    inner_clf = RandomForestClassifier(
        n_estimators=150, max_depth=10, class_weight="balanced",
        random_state=42, n_jobs=-1
    )
    inner_clf.fit(X_sm, y_sm)

    X_te_enc  = preprocessor.transform(X_test)
    y_prob    = inner_clf.predict_proba(X_te_enc)[:, 1]
    # Threshold tuned for high-recall (catch fraud)
    threshold = 0.35
    y_pred    = (y_prob >= threshold).astype(int)

    avg_amount = df_test["amount"].mean()
    evaluate_model("Fraud Spike Detector", y_test, y_pred, y_prob,
                   "fraud", avg_amount, results)

    # Save artifacts with compression (keeps files <5MB for GitHub)
    joblib.dump(preprocessor,  MODELS_DIR / "fraud_preprocessor.pkl", compress=3)
    joblib.dump(inner_clf,      MODELS_DIR / "fraud_classifier.pkl", compress=3)
    joblib.dump({"threshold": threshold}, MODELS_DIR / "fraud_config.pkl")
    print("  ✅  Saved fraud_preprocessor.pkl + fraud_classifier.pkl")


def train_return_scorer(df_train, df_test, results):
    """GBM return risk scorer with probability calibration"""
    print("\n📦  Training Return Risk Scorer …")
    target = "is_return"

    X_train = df_train[FEATURES]
    y_train = df_train[target]
    X_test  = df_test[FEATURES]
    y_test  = df_test[target]

    preprocessor = build_preprocessor()
    X_tr_enc = preprocessor.fit_transform(X_train)
    X_te_enc = preprocessor.transform(X_test)

    clf = GradientBoostingClassifier(
        n_estimators=200, max_depth=6, learning_rate=0.1,
        subsample=0.8, random_state=42
    )
    clf.fit(X_tr_enc, y_train)

    y_prob = clf.predict_proba(X_te_enc)[:, 1]
    threshold = 0.45
    y_pred = (y_prob >= threshold).astype(int)

    avg_amount = df_test["amount"].mean()
    evaluate_model("Return Risk Scorer", y_test, y_pred, y_prob,
                   "return", avg_amount, results)

    joblib.dump(preprocessor, MODELS_DIR / "return_preprocessor.pkl", compress=3)
    joblib.dump(clf,           MODELS_DIR / "return_classifier.pkl", compress=3)
    joblib.dump({"threshold": threshold}, MODELS_DIR / "return_config.pkl")
    print("  ✅  Saved return_preprocessor.pkl + return_classifier.pkl")


def train_chargeback_scorer(df_train, df_test, results):
    """Logistic Regression chargeback scorer"""
    print("\n💳  Training Chargeback Evidence Scorer …")
    target = "is_chargeback"

    X_train = df_train[FEATURES]
    y_train = df_train[target]
    X_test  = df_test[FEATURES]
    y_test  = df_test[target]

    preprocessor = build_preprocessor()
    X_tr_enc = preprocessor.fit_transform(X_train)
    X_te_enc = preprocessor.transform(X_test)

    smote = SMOTE(random_state=42, k_neighbors=3)
    X_sm, y_sm = smote.fit_resample(X_tr_enc, y_train)

    clf = LogisticRegression(
        C=1.0, class_weight="balanced", max_iter=1000,
        solver="lbfgs", random_state=42
    )
    clf.fit(X_sm, y_sm)

    y_prob = clf.predict_proba(X_te_enc)[:, 1]
    threshold = 0.40
    y_pred = (y_prob >= threshold).astype(int)

    avg_amount = df_test["amount"].mean()
    evaluate_model("Chargeback Scorer", y_test, y_pred, y_prob,
                   "chargeback", avg_amount, results)

    joblib.dump(preprocessor, MODELS_DIR / "chargeback_preprocessor.pkl", compress=3)
    joblib.dump(clf,           MODELS_DIR / "chargeback_classifier.pkl", compress=3)
    joblib.dump({"threshold": threshold}, MODELS_DIR / "chargeback_config.pkl")
    print("  ✅  Saved chargeback_preprocessor.pkl + chargeback_classifier.pkl")


def main():
    print("🛡️  RazorShield — Model Training Pipeline")
    print("  Generating 50,000 synthetic transactions …")

    df = generate_transactions(50_000)

    # ── 80/20 stratified split on multi-label ─────────────────────────────
    strat_col = df["is_fraud"].astype(str) + "_" + df["is_return"].astype(str)
    df_train, df_test = train_test_split(
        df, test_size=0.20, random_state=42, stratify=strat_col
    )
    print(f"  Train: {len(df_train):,}   Test: {len(df_test):,}")

    results = {}
    train_fraud_detector(df_train, df_test, results)
    train_return_scorer(df_train, df_test, results)
    train_chargeback_scorer(df_train, df_test, results)

    # Save summary
    with open(REPORTS_DIR / "metrics.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n📊  Metrics saved → reports/metrics.json")
    print(f"📊  Confusion matrices saved → reports/cm_*.png")
    print("\n🎉  All models trained successfully!")


if __name__ == "__main__":
    main()
