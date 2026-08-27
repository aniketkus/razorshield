"""
RazorShield – FastAPI Main Application
"""
import json
import os
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from models.fraud_detector import score_transaction, FraudInput, FraudOutput
from models.return_scorer import score_return, ReturnInput, ReturnOutput
from models.chargeback_responder import respond_chargeback, ChargebackInput, ChargebackOutput

REPORTS_DIR = Path(__file__).parent / "reports"


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Pre-load models on startup
    print("🛡️  RazorShield starting — pre-loading models …")
    try:
        from models.fraud_detector import _load_models as fl
        from models.return_scorer import _load_models as rl
        from models.chargeback_responder import _load_models as cl
        fl(); rl(); cl()
        print("✅  All models loaded")
    except FileNotFoundError:
        print("⚠️  Models not found — run `python data/train_models.py` first")
    yield


app = FastAPI(
    title="RazorShield — AI Risk Manager",
    description="""
## 🛡️ RazorShield

**Three AI-powered defense modules for Indian payment merchants:**

1. **Fraud Spike Detector** — Real-time fraud scoring per transaction
2. **Return Risk Scorer** — Pre-fulfillment return probability for each order
3. **Chargeback Evidence Responder** — Auto-generated dispute response documents

All models trained on synthetic but realistic Indian payment data (UPI/card/netbanking).
Honest precision/recall/F1/ROC-AUC metrics available at `/metrics`.
    """,
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Health ────────────────────────────────────────────────────────────────────
@app.get("/", tags=["Health"])
def root():
    return {
        "service": "RazorShield AI Risk Manager",
        "version": "1.0.0",
        "status": "online",
        "modules": ["fraud_detector", "return_scorer", "chargeback_responder"],
    }


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}


# ── Metrics ───────────────────────────────────────────────────────────────────
@app.get("/metrics", tags=["Metrics"])
def get_metrics():
    """Return honest ML evaluation metrics from the held-out test set."""
    metrics_path = REPORTS_DIR / "metrics.json"
    if not metrics_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Metrics not found. Run data/train_models.py first.",
        )
    with open(metrics_path) as f:
        return json.load(f)


# ── Fraud Detector ────────────────────────────────────────────────────────────
@app.post("/api/v1/fraud/score", response_model=FraudOutput, tags=["Fraud Detector"])
def fraud_score(payload: FraudInput):
    """
    Score a single transaction for fraud risk.

    Returns a fraud probability (0-1), risk level, and human-readable explanation.
    Threshold is optimised for **high recall** (catch as much fraud as possible)
    with false-positive cost reported transparently.
    """
    try:
        return score_transaction(payload)
    except FileNotFoundError:
        raise HTTPException(503, "Fraud model not loaded. Train models first.")


@app.post("/api/v1/fraud/score/batch", tags=["Fraud Detector"])
def fraud_score_batch(payloads: list[FraudInput]):
    """Score up to 100 transactions in one call."""
    if len(payloads) > 100:
        raise HTTPException(400, "Batch size limited to 100 transactions.")
    try:
        return [score_transaction(p) for p in payloads]
    except FileNotFoundError:
        raise HTTPException(503, "Fraud model not loaded. Train models first.")


# ── Return Scorer ─────────────────────────────────────────────────────────────
@app.post("/api/v1/return/score", response_model=ReturnOutput, tags=["Return Scorer"])
def return_score(payload: ReturnInput):
    """
    Score an order for return risk **before fulfillment**.

    Returns probability, risk level, suggested merchant action, and
    estimated revenue-at-risk in ₹.
    """
    try:
        return score_return(payload)
    except FileNotFoundError:
        raise HTTPException(503, "Return model not loaded. Train models first.")


# ── Chargeback Responder ──────────────────────────────────────────────────────
@app.post("/api/v1/chargeback/respond", response_model=ChargebackOutput, tags=["Chargeback Responder"])
def chargeback_respond(payload: ChargebackInput):
    """
    Generate a structured chargeback dispute response.

    Returns chargeback risk score, estimated win probability,
    and a ready-to-submit evidence document.
    """
    try:
        return respond_chargeback(payload)
    except FileNotFoundError:
        raise HTTPException(503, "Chargeback model not loaded. Train models first.")


# ── Demo Endpoints (pre-filled samples) ──────────────────────────────────────
@app.get("/api/v1/demo/fraud", tags=["Demo"])
def demo_fraud():
    """Run a sample high-risk fraud transaction."""
    sample = FraudInput(
        txn_id="pay_DEMO001",
        customer_id="cust_000001",
        merchant_id="merch_0001",
        category="electronics",
        amount=75000.0,
        payment_method="card",
        state="MH",
        device_type="mobile",
        browser="unknown",
        device_fp="abc123xyz",
        hour=2,
        day_of_week=5,
        txn_velocity_24h=15,
        amount_velocity_24h=200000.0,
        device_fp_count=25,
    )
    return score_transaction(sample)


@app.get("/api/v1/demo/return", tags=["Demo"])
def demo_return():
    """Run a sample high return-risk order."""
    sample = ReturnInput(
        order_id="ord_DEMO001",
        customer_id="cust_000002",
        category="fashion",
        amount=4500.0,
        payment_method="upi",
        state="DL",
        device_type="mobile",
        browser="chrome",
        hour=23,
        day_of_week=6,
        txn_velocity_24h=3,
        amount_velocity_24h=15000.0,
        device_fp_count=1,
        customer_return_rate=0.45,
    )
    return score_return(sample)


@app.get("/api/v1/demo/chargeback", tags=["Demo"])
def demo_chargeback():
    """Run a sample chargeback dispute."""
    sample = ChargebackInput(
        txn_id="pay_DEMO002",
        customer_id="cust_000003",
        merchant_id="merch_0002",
        merchant_name="QuickElectronics Pvt Ltd",
        category="electronics",
        amount=18000.0,
        payment_method="card",
        state="KA",
        device_type="desktop",
        browser="chrome",
        hour=14,
        day_of_week=2,
        txn_velocity_24h=1,
        amount_velocity_24h=18000.0,
        device_fp_count=1,
        delivery_confirmed=True,
        ip_address="103.21.56.78",
        shipping_address="Koramangala, Bangalore, KA 560034",
        dispute_reason="not_received",
        txn_timestamp="2025-07-15 14:32:00 IST",
    )
    return respond_chargeback(sample)
