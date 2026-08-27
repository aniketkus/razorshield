"""
RazorShield – Synthetic Data Generator
Generates realistic Indian payment transaction data for training
"""
import numpy as np
import pandas as pd
from faker import Faker
import random
import hashlib
from datetime import datetime, timedelta

fake = Faker("en_IN")
np.random.seed(42)
random.seed(42)

# ── Constants ────────────────────────────────────────────────────────────────
PAYMENT_METHODS = ["upi", "card", "netbanking", "wallet", "emi"]
CARD_NETWORKS   = ["visa", "mastercard", "rupay", "amex"]
CATEGORIES      = ["electronics", "fashion", "groceries", "travel",
                   "food", "health", "jewelry", "gaming", "books", "home"]
INDIAN_STATES   = ["MH", "DL", "KA", "TN", "WB", "UP", "GJ", "RJ", "TS", "KL"]
DEVICE_TYPES    = ["mobile", "desktop", "tablet"]
BROWSERS        = ["chrome", "firefox", "safari", "edge", "unknown"]

# Average return-rate & fraud-rate per category (manually calibrated)
CATEGORY_RETURN_RATE = {
    "electronics": 0.18, "fashion": 0.25, "groceries": 0.03,
    "travel": 0.08, "food": 0.02, "health": 0.05, "jewelry": 0.12,
    "gaming": 0.10, "books": 0.04, "home": 0.14
}
CATEGORY_FRAUD_RATE = {
    "electronics": 0.04, "fashion": 0.03, "groceries": 0.005,
    "travel": 0.06, "food": 0.005, "health": 0.01, "jewelry": 0.07,
    "gaming": 0.05, "books": 0.005, "home": 0.02
}


def _generate_device_fingerprint(n: int) -> list[str]:
    """Generate stable device fingerprints — some shared (fraud rings)"""
    pool = [hashlib.md5(f"device-{i}".encode()).hexdigest()[:12] for i in range(int(n * 0.8))]
    return [random.choice(pool) for _ in range(n)]


def generate_transactions(n: int = 50_000) -> pd.DataFrame:
    now = datetime(2025, 8, 1, 12, 0, 0)

    customer_ids = [f"cust_{i:06d}" for i in np.random.randint(0, int(n * 0.3), n)]
    merchant_ids = [f"merch_{i:04d}" for i in np.random.randint(0, 200, n)]
    categories   = [random.choice(CATEGORIES) for _ in range(n)]
    amounts      = np.where(
        np.array(categories) == "groceries",
        np.random.lognormal(6.5, 0.6, n),          # ~₹600 median
        np.where(
            np.array(categories) == "electronics",
            np.random.lognormal(9.5, 0.8, n),       # ~₹15k median
            np.random.lognormal(8.0, 1.0, n)         # ~₹3k median
        )
    ).clip(50, 500_000)

    timestamps = [now - timedelta(seconds=int(x))
                  for x in np.random.exponential(86400 * 30, n)]
    hours      = [t.hour for t in timestamps]
    day_of_week = [t.weekday() for t in timestamps]

    methods      = [random.choice(PAYMENT_METHODS) for _ in range(n)]
    states       = [random.choice(INDIAN_STATES) for _ in range(n)]
    devices      = [random.choice(DEVICE_TYPES) for _ in range(n)]
    browsers     = [random.choice(BROWSERS) for _ in range(n)]
    fingerprints = _generate_device_fingerprint(n)

    # ── Engineered features ───────────────────────────────────────────────
    df = pd.DataFrame({
        "txn_id":          [f"pay_{i:08d}" for i in range(n)],
        "customer_id":     customer_ids,
        "merchant_id":     merchant_ids,
        "category":        categories,
        "amount":          amounts.round(2),
        "payment_method":  methods,
        "state":           states,
        "device_type":     devices,
        "browser":         browsers,
        "device_fp":       fingerprints,
        "hour":            hours,
        "day_of_week":     day_of_week,
        "timestamp":       timestamps,
    })

    # ── Velocity features (per customer, last 24h) ────────────────────────
    df.sort_values("timestamp", inplace=True)
    df["txn_velocity_24h"] = (
        df.groupby("customer_id")["timestamp"]
        .transform(lambda s: s.expanding().count())
        .clip(1, 50)
    )
    df["amount_velocity_24h"] = (
        df.groupby("customer_id")["amount"]
        .transform(lambda s: s.expanding().sum())
        .clip(50, 10_000_000)
    )
    df["device_fp_count"] = (
        df.groupby("device_fp")["customer_id"]
        .transform("nunique")
        .clip(1, 100)
    )

    # ── Labels ─────────────────────────────────────────────────────────────
    # FRAUD label
    base_fraud = np.array([CATEGORY_FRAUD_RATE[c] for c in df["category"]])
    fraud_score = (
        base_fraud
        + 0.15 * (df["txn_velocity_24h"] > 10)
        + 0.20 * (df["amount"] > 50_000)
        + 0.10 * (df["hour"].isin(range(0, 5)))  # midnight transactions
        + 0.25 * (df["device_fp_count"] > 10)    # device shared by many = ring
        + 0.05 * (df["browser"] == "unknown")
    ).clip(0, 0.95)
    df["is_fraud"] = (np.random.rand(n) < fraud_score).astype(int)

    # RETURN label
    base_return = np.array([CATEGORY_RETURN_RATE[c] for c in df["category"]])
    return_score = (
        base_return
        + 0.10 * (df["amount"] > 10_000)
        + 0.08 * (df["device_type"] == "mobile")
        + 0.05 * (df["hour"].isin(range(22, 24)))   # late night impulse buys
        + 0.15 * (df["is_fraud"] == 1)              # fraudsters return too
        - 0.05 * (df["payment_method"] == "emi")    # EMI buyers are committed
    ).clip(0.01, 0.95)
    df["is_return"] = (np.random.rand(n) < return_score).astype(int)

    # CHARGEBACK label (subset of fraud + some return abuse)
    cb_score = (
        0.60 * df["is_fraud"]
        + 0.15 * df["is_return"]
        + 0.05 * (df["amount"] > 5_000)
    ).clip(0, 0.95)
    df["is_chargeback"] = (np.random.rand(n) < cb_score * 0.25).astype(int)

    df.reset_index(drop=True, inplace=True)
    return df


if __name__ == "__main__":
    import os
    os.makedirs("data", exist_ok=True)
    df = generate_transactions(50_000)
    df.to_csv("data/transactions.csv", index=False)
    print(f"Generated {len(df):,} transactions")
    print(f"  Fraud: {df['is_fraud'].mean():.2%}")
    print(f"  Returns: {df['is_return'].mean():.2%}")
    print(f"  Chargebacks: {df['is_chargeback'].mean():.2%}")
