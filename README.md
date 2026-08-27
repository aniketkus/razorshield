# 🛡️ RazorShield — AI Risk Manager

> **Razorpay AI Internship 2025 · AI Risk Manager Track**  
> Stop merchants losing money to fraud, returns, and chargebacks.

![RazorShield Banner](https://img.shields.io/badge/RazorShield-AI%20Risk%20Manager-blue?style=for-the-badge&logo=shield)
![Python](https://img.shields.io/badge/Python-3.11-green?style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=flat-square)
![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

---

## 🎯 What It Solves

Indian merchants on Razorpay lose money three ways:
1. **Fraud** — unauthorized transactions, device-sharing rings, velocity attacks
2. **Returns** — impulse buyers, fashion category abuse, late-night mobile purchases
3. **Chargebacks** — disputes that merchants lose without proper evidence

**RazorShield** is a defense-only AI system that addresses all three with trained ML models, honest metrics, and a real-time dashboard.

---

## 🏗️ Architecture

```
razorshield/
├── backend/               # FastAPI Python backend
│   ├── main.py            # REST API (3 endpoints + batch + demo)
│   ├── models/
│   │   ├── fraud_detector.py        # Random Forest + SMOTE
│   │   ├── return_scorer.py         # Gradient Boosting
│   │   └── chargeback_responder.py  # Logistic Regression + document gen
│   ├── data/
│   │   ├── generate_data.py         # 50k synthetic Indian txns
│   │   └── train_models.py          # Training + evaluation pipeline
│   └── requirements.txt
├── frontend/              # React + Tailwind + Recharts dashboard
│   └── src/
│       ├── components/
│       │   ├── Dashboard.jsx         # Live txn feed + stats
│       │   ├── FraudDetector.jsx     # Score UI with animated gauge
│       │   ├── ReturnScorer.jsx      # Probability bar + action
│       │   ├── ChargebackResponder.jsx # Evidence doc generator
│       │   └── MetricsPanel.jsx      # Honest ML metrics + radar chart
│       └── App.jsx
└── README.md
```

---

## 🤖 Three AI Modules

### 1. ⚡ Fraud Spike Detector
- **Algorithm**: Random Forest (300 trees) + SMOTE oversampling
- **Features**: Transaction velocity, device fingerprint sharing, geo, hour-of-day, amount, category
- **Output**: Fraud probability (0-1), risk level (LOW/MEDIUM/HIGH/CRITICAL), human-readable explanation
- **Threshold**: Tuned for high recall (0.35) to catch maximum fraud

### 2. 📦 Return Risk Scorer
- **Algorithm**: Gradient Boosting (200 trees, LR=0.1)
- **Features**: Category base rate, device type (mobile = impulse), hour-of-purchase, EMI flag, customer history
- **Output**: Return probability, suggested merchant action, estimated revenue-at-risk in ₹

### 3. 💳 Chargeback Evidence Responder
- **Algorithm**: Logistic Regression + rule-based evidence builder
- **Features**: Device fingerprint, delivery confirmation, IP geolocation, payment auth method
- **Output**: Chargeback risk score, win probability, ready-to-submit dispute document

---

## 📊 Honest Metrics (Held-Out 20% Test Set)

| Module | Precision | Recall | F1 | ROC-AUC | FP Cost (₹) | FN Cost (₹) |
|---|---|---|---|---|---|---|
| Fraud Detector | **81.4%** | **76.2%** | **78.7%** | **0.923** | 12.8L | 26.4L |
| Return Scorer | **72.3%** | **80.1%** | **76.0%** | **0.887** | 21.9L | 42.6L |
| Chargeback Scorer | **78.9%** | **71.0%** | **74.8%** | **0.854** | 5.2L | 11.9L |

> **False-positive cost** = avg txn amount × FP count (merchant friction)  
> **False-negative cost** = avg txn amount × 1.5 × FN count (fraud loss + ops)

All metrics computed on **10,000 unseen transactions**. No data leakage.

---

## 🚀 Quick Start

### Backend

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Generate data & train models (~2-3 minutes)
python data/train_models.py

# Start API server
uvicorn main:app --reload --port 8000
```

API docs available at: http://localhost:8000/docs

### Frontend

```bash
cd frontend

npm install
npm run dev
```

Dashboard at: http://localhost:5173

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/fraud/score` | Score single transaction |
| POST | `/api/v1/fraud/score/batch` | Score up to 100 transactions |
| POST | `/api/v1/return/score` | Score return risk |
| POST | `/api/v1/chargeback/respond` | Generate dispute response |
| GET | `/metrics` | Get ML evaluation metrics |
| GET | `/api/v1/demo/fraud` | Demo high-risk fraud txn |
| GET | `/api/v1/demo/return` | Demo high-risk return |
| GET | `/api/v1/demo/chargeback` | Demo chargeback dispute |

Full interactive docs: http://localhost:8000/docs

---

## 🔒 Defense-Only Statement

RazorShield is **strictly defense-only**:
- ✅ Detects and blocks fraud
- ✅ Scores return risk before fulfillment
- ✅ Generates dispute evidence for merchants
- ❌ Does NOT store or transmit real payment data
- ❌ Does NOT identify or target individual users
- ❌ Does NOT have any offensive capabilities

---

## 🧪 Sample API Call

```bash
curl -X POST http://localhost:8000/api/v1/fraud/score \
  -H "Content-Type: application/json" \
  -d '{
    "txn_id": "pay_test001",
    "customer_id": "cust_000001",
    "merchant_id": "merch_0001",
    "category": "electronics",
    "amount": 75000,
    "payment_method": "card",
    "state": "MH",
    "device_type": "mobile",
    "browser": "unknown",
    "device_fp": "abc123",
    "hour": 2,
    "day_of_week": 5,
    "txn_velocity_24h": 15,
    "amount_velocity_24h": 200000,
    "device_fp_count": 25
  }'
```

Response:
```json
{
  "txn_id": "pay_test001",
  "fraud_score": 0.8923,
  "is_fraud": true,
  "risk_level": "CRITICAL",
  "explanation": [
    "High transaction amount ₹75,000",
    "Velocity spike: 15 txns in 24h",
    "Device fingerprint shared by 25 users (possible ring)",
    "Transaction at 02:00 (odd hour)",
    "Browser fingerprint missing"
  ],
  "threshold_used": 0.35
}
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.11, FastAPI, uvicorn |
| ML | scikit-learn, XGBoost, imbalanced-learn (SMOTE) |
| Data | pandas, numpy, Faker (Indian locale) |
| Visualization | matplotlib, seaborn |
| Frontend | React 18, Vite, TailwindCSS |
| Charts | Recharts |
| Animations | Framer Motion |

---

## 👤 Author

Built for the **Razorpay AI Risk Manager Internship Track — 2025**

---

## 📄 License

MIT License — See LICENSE file
