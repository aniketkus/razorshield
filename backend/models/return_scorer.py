"""
RazorShield – Return Risk Scorer
Scores an order for return probability before fulfillment.
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
        _preprocessor = joblib.load(MODELS_DIR / "return_preprocessor.pkl")
        _classifier   = joblib.load(MODELS_DIR / "return_classifier.pkl")
        _config       = joblib.load(MODELS_DIR / "return_config.pkl")


class ReturnInput(BaseModel):
    order_id:             str
    customer_id:          str
    category:             str
    amount:               float
    payment_method:       str
    state:                str
    device_type:          str
    browser:              str
    hour:                 int   = Field(..., ge=0, le=23)
    day_of_week:          int   = Field(..., ge=0, le=6)
    txn_velocity_24h:     int   = Field(1, ge=1)
    amount_velocity_24h:  float = Field(0.0, ge=0)
    device_fp_count:      int   = Field(1, ge=1)
    customer_return_rate: float = Field(0.0, ge=0.0, le=1.0,
                                        description="Historical return rate for this customer (0-1)")


class ReturnOutput(BaseModel):
    order_id:           str
    return_probability: float
    return_risk:        str    # LOW | MEDIUM | HIGH
    suggested_action:   str
    risk_factors:       list[str]
    estimated_loss_inr: float


_CATEGORY_RETURN_LOSS = {
    "electronics": 0.85, "fashion": 0.70, "groceries": 0.30,
    "travel": 0.20, "food": 0.10, "health": 0.50, "jewelry": 0.90,
    "gaming": 0.75, "books": 0.40, "home": 0.65,
}


def _suggest_action(prob: float) -> str:
    if prob < 0.20: return "Process normally"
    if prob < 0.40: return "Send pre-shipment confirmation email"
    if prob < 0.60: return "Call customer to confirm order before shipping"
    if prob < 0.80: return "Require OTP verification & add return fee disclosure"
    return "Flag for manual review — high-risk order"


def _explain_return(inp: ReturnInput) -> list[str]:
    factors = []
    if inp.category in ("fashion", "electronics", "jewelry"):
        factors.append(f"Category '{inp.category}' has high base return rate")
    if inp.amount > 10_000:
        factors.append(f"High-value order Rs.{inp.amount:,.0f}")
    if inp.device_type == "mobile":
        factors.append("Ordered from mobile (impulse purchase risk)")
    if inp.hour >= 22:
        factors.append(f"Late-night order at {inp.hour}:00 (impulse buy signal)")
    if inp.payment_method != "emi":
        factors.append("Non-EMI payment (less committed buyers)")
    if inp.customer_return_rate > 0.30:
        factors.append(f"Customer has {inp.customer_return_rate:.0%} historical return rate")
    if not factors:
        factors.append("Mild risk based on combined features")
    return factors


def score_return(inp: ReturnInput) -> ReturnOutput:
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

    X    = _preprocessor.transform(row)
    prob = float(_classifier.predict_proba(X)[0, 1])

    # Blend ML probability with customer return history
    adjusted  = min(0.95, prob * 0.7 + inp.customer_return_rate * 0.3)
    risk      = "LOW" if adjusted < 0.30 else "MEDIUM" if adjusted < 0.60 else "HIGH"
    loss_rate = _CATEGORY_RETURN_LOSS.get(inp.category, 0.60)

    return ReturnOutput(
        order_id           = inp.order_id,
        return_probability = round(adjusted, 4),
        return_risk        = risk,
        suggested_action   = _suggest_action(adjusted),
        risk_factors       = _explain_return(inp),
        estimated_loss_inr = round(inp.amount * adjusted * loss_rate, 2),
    )
