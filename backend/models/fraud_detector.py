"""
RazorShield – Fraud Spike Detector Model
Loads the trained Random Forest and scores incoming transactions.
"""
import joblib
import pandas as pd
from pathlib import Path
from pydantic import BaseModel, Field

MODELS_DIR = Path(__file__).parent.parent / "saved_models"

CATEGORICAL = ["payment_method", "state", "device_type", "browser", "category"]
NUMERICAL   = ["amount", "hour", "day_of_week", "txn_velocity_24h",
               "amount_velocity_24h", "device_fp_count"]

_preprocessor = None
_classifier   = None
_config       = None


def _load_models():
    global _preprocessor, _classifier, _config
    if _preprocessor is None:
        _preprocessor = joblib.load(MODELS_DIR / "fraud_preprocessor.pkl")
        _classifier   = joblib.load(MODELS_DIR / "fraud_classifier.pkl")
        _config       = joblib.load(MODELS_DIR / "fraud_config.pkl")


class FraudInput(BaseModel):
    txn_id:              str
    customer_id:         str
    merchant_id:         str
    category:            str = Field(..., description="e.g. electronics, fashion")
    amount:              float
    payment_method:      str = Field(..., description="upi|card|netbanking|wallet|emi")
    state:               str = Field(..., description="2-letter state code, e.g. MH")
    device_type:         str = Field(..., description="mobile|desktop|tablet")
    browser:             str = Field(..., description="chrome|firefox|safari|edge|unknown")
    device_fp:           str = Field(..., description="Device fingerprint hash")
    hour:                int = Field(..., ge=0, le=23)
    day_of_week:         int = Field(..., ge=0, le=6)
    txn_velocity_24h:    int = Field(1, ge=1)
    amount_velocity_24h: float = Field(0.0, ge=0)
    device_fp_count:     int = Field(1, ge=1)


class FraudOutput(BaseModel):
    txn_id:         str
    fraud_score:    float    # 0-1 probability
    is_fraud:       bool
    risk_level:     str      # LOW | MEDIUM | HIGH | CRITICAL
    explanation:    list[str]
    threshold_used: float


def _risk_level(score: float) -> str:
    if score < 0.20: return "LOW"
    if score < 0.45: return "MEDIUM"
    if score < 0.70: return "HIGH"
    return "CRITICAL"


def _explain(inp: FraudInput) -> list[str]:
    reasons = []
    if inp.amount > 50_000:
        reasons.append(f"High transaction amount Rs.{inp.amount:,.0f}")
    if inp.txn_velocity_24h > 10:
        reasons.append(f"Velocity spike: {inp.txn_velocity_24h} txns in 24h")
    if inp.device_fp_count > 10:
        reasons.append(f"Device fingerprint shared by {inp.device_fp_count} users (possible ring)")
    if inp.hour < 5:
        reasons.append(f"Transaction at {inp.hour:02d}:00 (odd hour)")
    if inp.browser == "unknown":
        reasons.append("Browser fingerprint missing")
    if inp.category in ("travel", "jewelry", "electronics"):
        reasons.append(f"High-risk category: {inp.category}")
    if not reasons:
        reasons.append("Combination of features elevated risk score")
    return reasons


def score_transaction(inp: FraudInput) -> FraudOutput:
    _load_models()
    row = pd.DataFrame([{
        "payment_method":      inp.payment_method,
        "state":               inp.state,
        "device_type":         inp.device_type,
        "browser":             inp.browser,
        "category":            inp.category,
        "amount":              inp.amount,
        "hour":                inp.hour,
        "day_of_week":         inp.day_of_week,
        "txn_velocity_24h":    inp.txn_velocity_24h,
        "amount_velocity_24h": inp.amount_velocity_24h,
        "device_fp_count":     inp.device_fp_count,
    }])

    X         = _preprocessor.transform(row)
    score     = float(_classifier.predict_proba(X)[0, 1])
    threshold = _config["threshold"]

    return FraudOutput(
        txn_id         = inp.txn_id,
        fraud_score    = round(score, 4),
        is_fraud       = score >= threshold,
        risk_level     = _risk_level(score),
        explanation    = _explain(inp),
        threshold_used = threshold,
    )
