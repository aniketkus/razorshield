"""
RazorShield – FastAPI Main Application
Three defense modules: Fraud Spike Detector | Return Risk Scorer | Chargeback Evidence Responder
"""
import json
import sys
from pathlib import Path
from contextlib import asynccontextmanager

# Add backend directory to sys.path so imports work regardless of working directory
BACKEND_DIR = Path(__file__).resolve().parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

# Windows fix: force UTF-8 output so emoji / INR symbols don't crash the server
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models.fraud_detector import score_transaction, FraudInput, FraudOutput
from models.return_scorer import score_return, ReturnInput, ReturnOutput
from models.chargeback_responder import respond_chargeback, ChargebackInput, ChargebackOutput

REPORTS_DIR = Path(__file__).parent / "reports"


# ── Startup / Shutdown ────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("RazorShield starting -- pre-loading models ...")
    try:
        from models.fraud_detector import _load_models as fl
        from models.return_scorer import _load_models as rl
        from models.chargeback_responder import _load_models as cl
        fl(); rl(); cl()
        print("All models loaded.")
    except FileNotFoundError:
        print("Models not found. Run: python data/train_models.py")
    yield


# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="RazorShield — AI Risk Manager",
    description=(
        "**Three AI-powered defense modules for Indian payment merchants:**\n\n"
        "1. **Fraud Spike Detector** — Real-time fraud scoring per transaction\n"
        "2. **Return Risk Scorer** — Pre-fulfillment return probability\n"
        "3. **Chargeback Evidence Responder** — Auto-generated dispute response documents\n\n"
        "Honest precision/recall/F1/ROC-AUC metrics at `/metrics`."
    ),
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
    """Return ML evaluation metrics from the held-out test set."""
    path = REPORTS_DIR / "metrics.json"
    if not path.exists():
        raise HTTPException(404, "Metrics not found. Run data/train_models.py first.")
    with open(path) as f:
        return json.load(f)


# ── Fraud Detector ────────────────────────────────────────────────────────────
@app.post("/api/v1/fraud/score", response_model=FraudOutput, tags=["Fraud Detector"])
def fraud_score(payload: FraudInput):
    """Score a single transaction for fraud risk (0-1 probability + explanation)."""
    try:
        return score_transaction(payload)
    except FileNotFoundError:
        raise HTTPException(503, "Fraud model not loaded. Run train_models.py first.")


@app.post("/api/v1/fraud/score/batch", tags=["Fraud Detector"])
def fraud_score_batch(payloads: list[FraudInput]):
    """Score up to 100 transactions in one call."""
    if len(payloads) > 100:
        raise HTTPException(400, "Batch size limited to 100.")
    try:
        return [score_transaction(p) for p in payloads]
    except FileNotFoundError:
        raise HTTPException(503, "Fraud model not loaded. Run train_models.py first.")


# ── Return Scorer ─────────────────────────────────────────────────────────────
@app.post("/api/v1/return/score", response_model=ReturnOutput, tags=["Return Scorer"])
def return_score(payload: ReturnInput):
    """Score an order for return risk before fulfillment (probability + Rs. at risk)."""
    try:
        return score_return(payload)
    except FileNotFoundError:
        raise HTTPException(503, "Return model not loaded. Run train_models.py first.")


# ── Chargeback Responder ──────────────────────────────────────────────────────
@app.post("/api/v1/chargeback/respond", response_model=ChargebackOutput, tags=["Chargeback Responder"])
def chargeback_respond(payload: ChargebackInput):
    """Generate a structured chargeback dispute response with win probability."""
    try:
        return respond_chargeback(payload)
    except FileNotFoundError:
        raise HTTPException(503, "Chargeback model not loaded. Run train_models.py first.")


# ── Demo Endpoints ────────────────────────────────────────────────────────────
@app.get("/api/v1/demo/fraud", tags=["Demo"])
def demo_fraud():
    """Sample high-risk fraud transaction."""
    return score_transaction(FraudInput(
        txn_id="pay_DEMO001", customer_id="cust_000001", merchant_id="merch_0001",
        category="electronics", amount=75000.0, payment_method="card",
        state="MH", device_type="mobile", browser="unknown", device_fp="abc123xyz",
        hour=2, day_of_week=5, txn_velocity_24h=15,
        amount_velocity_24h=200000.0, device_fp_count=25,
    ))


@app.get("/api/v1/demo/return", tags=["Demo"])
def demo_return():
    """Sample high return-risk order."""
    return score_return(ReturnInput(
        order_id="ord_DEMO001", customer_id="cust_000002",
        category="fashion", amount=4500.0, payment_method="upi",
        state="DL", device_type="mobile", browser="chrome",
        hour=23, day_of_week=6, txn_velocity_24h=3,
        amount_velocity_24h=15000.0, device_fp_count=1, customer_return_rate=0.45,
    ))


@app.get("/api/v1/demo/chargeback", tags=["Demo"])
def demo_chargeback():
    """Sample chargeback dispute."""
    return respond_chargeback(ChargebackInput(
        txn_id="pay_DEMO002", customer_id="cust_000003",
        merchant_id="merch_0002", merchant_name="QuickElectronics Pvt Ltd",
        category="electronics", amount=18000.0, payment_method="card",
        state="KA", device_type="desktop", browser="chrome",
        hour=14, day_of_week=2, txn_velocity_24h=1,
        amount_velocity_24h=18000.0, device_fp_count=1,
        delivery_confirmed=True, ip_address="103.21.56.78",
        shipping_address="Koramangala, Bangalore, KA 560034",
        dispute_reason="not_received", txn_timestamp="2025-07-15 14:32:00 IST",
    ))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

