# 🛡️ RazorShield — AI Risk Intelligence & Defense Platform

> **Razorpay AI Internship Track · AI Risk Manager Track**  
> *Empowering digital merchants to stop revenue bleed from fraud, RTO returns, and lost chargebacks.*

[![RazorShield CI](https://github.com/aniketkus/razorshield/actions/workflows/ci.yml/badge.svg)](https://github.com/aniketkus/razorshield/actions)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-Vercel%20Deployment-blueviolet?style=for-the-badge&logo=vercel)](https://razorshield.vercel.app)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18.3-61DAFB?style=flat-square&logo=react&logoColor=black)](https://react.dev)
[![Vite](https://img.shields.io/badge/Vite-5.4-646CFF?style=flat-square&logo=vite&logoColor=white)](https://vitejs.dev)
[![TailwindCSS](https://img.shields.io/badge/Tailwind-3.4-38B2AC?style=flat-square&logo=tailwind-css&logoColor=white)](https://tailwindcss.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)

---

## 🌐 Live Interactive Demo & Quick Access

### 1. 24/7 Cloud Deployment
Test the live full-stack system right now in your browser:  
🔗 **[https://razorshield.vercel.app](https://razorshield.vercel.app)**

- **No login or database setup required** — instant access to live feeds, dynamic score sliders, and interactive ML explainability charts.
- **Full-stack integration** — all dashboard actions execute real-time inference against the trained ML backend models.

### 2. Local 1-Click Launch (Windows)
- **Local Dashboard**: Double-click `start.bat` (`http://localhost:5173`).
- **Public Tunnel**: Double-click `start_live_tunnel.bat` (launches local servers and generates a fresh public `https://*.trycloudflare.com` URL).

### 3. Video Demo & AI Walkthrough
- A complete 5-minute pitch video script with timestamped screen clicks, problem context, and AI voiceover narration is available in **[`VIDEO_SCRIPT.md`](VIDEO_SCRIPT.md)**.


---

## 🎯 The Problem

Indian merchants running on digital payments (UPI, RuPay, cards, netbanking) lose **3% to 7% of gross operating margins** to three compounding risk stages:

1. **Pre-Authorization Fraud Attacks**: Coordinated syndicates using shared device fingerprints and high-velocity card/UPI probing during off-peak hours (midnight to 4 AM).
2. **Pre-Fulfillment Return & RTO Abuse**: Impulse purchases and order-return cycles in high-risk categories (fashion at 25%+, electronics at 18%) bleeding forward and reverse logistics costs.
3. **Post-Transaction Chargebacks**: Merchants losing legitimate customer disputes simply due to lack of fast, structured evidence dossiers within strict bank SLA windows.

**RazorShield** is a pure **defense-only AI system** providing an end-to-end protective shield across all three phases with mathematically honest metrics and real-time dashboard analytics.

---

## 🤖 The Three AI Defense Engines

```
                                  RAZORSHIELD ARCHITECTURE
 ┌────────────────────────────────────────────────────────────────────────────────────────┐
 │                                                                                        │
 │  1. PRE-AUTH                        2. PRE-FULFILLMENT                 3. POST-DISPUTE │
 │  ┌────────────────────────┐         ┌────────────────────────┐         ┌─────────────┐ │
 │  │  ⚡ Fraud Spike         │         │  📦 Return Risk         │         │  💳 Dispute │ │
 │  │     Detector           │         │     Scorer             │         │     Response│ │
 │  ├────────────────────────┤         ├────────────────────────┤         ├─────────────┤ │
 │  │ Random Forest (300)    │         │ Gradient Boosting (200)│         │ Logistic Reg│ │
 │  │ + SMOTE Imbalance      │         │ Feature Subsampling 0.8│         │ + Auto Doc  │ │
 │  │ Cost-tuned (Thresh 0.35│         │ ₹ Revenue-at-Risk      │         │ Win Prob    │ │
 │  └───────────┬────────────┘         └───────────┬────────────┘         └──────┬──────┘ │
 │              │                                  │                             │        │
 └──────────────┼──────────────────────────────────┼─────────────────────────────┼────────┘
                ▼                                  ▼                             ▼
   FastAPI High-Speed REST API (Sub-50ms Inference) ───► React + Recharts Live Dashboard
```

### 1. ⚡ Fraud Spike Detector (Pre-Auth Defense)
- **Algorithm**: Random Forest Classifier (300 estimators, max depth 10) trained with **Synthetic Minority Over-sampling Technique (SMOTE)** to handle <3% class imbalance.
- **Key Features**: Transaction velocity (`24h`), amount velocity, device fingerprint sharing count, geo-IP state, category risk, and odd-hour indices.
- **Economic Calibration**: Decision threshold shifted from 0.50 to **0.35** to optimize recall (catching high-risk fraud rings early) while constraining merchant friction (<4.5% FP rate).
- **Output**: Probability score (0.0 to 1.0), Risk Level (`LOW`, `MEDIUM`, `HIGH`, `CRITICAL`), and human-readable explanation factors.

### 2. 📦 Return Risk Scorer (Pre-Fulfillment Defense)
- **Algorithm**: Gradient Boosted Decision Trees (200 trees, learning rate 0.1, feature subsampling 0.8).
- **Key Features**: Category baseline return rates, device type (mobile impulse detection), hour of purchase, customer lifetime return history, EMI/payment mode.
- **Graduated Interventions**: Instead of blunt cancellations that anger customers, the engine triggers graduated actions (e.g., automated WhatsApp/OTP delivery confirmation or customer service verification).
- **Output**: Return probability, merchant intervention recommendation, and exact estimated **₹ Revenue-at-Risk**.

### 3. 💳 Chargeback Evidence Responder (Post-Dispute Defense)
- **Algorithm**: Calibrated Logistic Regression + dynamic rule-based document synthesizer.
- **Key Features**: 3DS verification status, delivery confirmation timestamp, device fingerprint consistency, IP matching, and category dispute histories.
- **Output**: Dispute win probability and a complete, bank-compliant evidence dossier formatted ready to contest chargebacks before banking deadlines.

---

## 📊 Honest Evaluation Metrics (Held-Out 10,000 Test Set)

Evaluated strictly on a **20% held-out test split (10,000 unseen transactions)** with zero data leakage:

| Defense Module | Precision | Recall | F1 Score | ROC-AUC | FP Friction Cost (₹) | FN Loss Cost (₹) |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Fraud Detector** | **81.4%** | **76.2%** | **78.7%** | **0.923** | ₹12.8 Lakh | ₹26.4 Lakh |
| **Return Scorer** | **72.3%** | **80.1%** | **76.0%** | **0.887** | ₹21.9 Lakh | ₹42.6 Lakh |
| **Chargeback Scorer** | **78.9%** | **71.0%** | **74.8%** | **0.854** | ₹5.2 Lakh | ₹11.9 Lakh |

> **Cost Formulation**:  
> • **False Positive Cost** = `Average Txn Amount × FP Count` *(Merchant friction & review overhead)*  
> • **False Negative Cost** = `Average Txn Amount × 1.5 × FN Count` *(Direct fraud loss + operational fee)*

---

## 🏗️ Repository Layout

```
razorshield/
├── .github/
│   └── workflows/
│       └── ci.yml             # GitHub Actions CI (build, train, smoke test)
├── backend/
│   ├── data/
│   │   ├── generate_data.py   # Synthetic Indian payment transaction generator (50k rows)
│   │   └── train_models.py    # Training & evaluation pipeline
│   ├── models/
│   │   ├── fraud_detector.py  # Fraud detection model & inference logic
│   │   ├── return_scorer.py   # Return prediction engine
│   │   └── chargeback_responder.py # Dispute evidence generator
│   ├── saved_models/          # Compressed serialized model weights (*.pkl)
│   ├── reports/               # Evaluation charts & confusion matrix outputs
│   ├── main.py                # FastAPI REST application
│   └── requirements.txt       # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dashboard.jsx            # Transaction stream & KPI overview
│   │   │   ├── FraudDetector.jsx        # Gauge score UI & dynamic factor sliders
│   │   │   ├── ReturnScorer.jsx         # Probability bar & revenue-at-risk
│   │   │   ├── ChargebackResponder.jsx  # Evidence document generator
│   │   │   └── MetricsPanel.jsx         # Radar chart & confusion matrix view
│   │   ├── App.jsx            # Root UI shell & navigation tabs
│   │   └── main.jsx           # App bootstrapping & API proxy configuration
│   ├── package.json           # React dependencies
│   ├── tailwind.config.js     # Tailwind CSS theme configuration
│   └── vite.config.js         # Vite configuration with full proxy & allowedHosts
├── start.bat                  # One-click local startup script
├── start_live_tunnel.bat      # One-click startup with Cloudflare live tunnel
├── SUBMISSION.md              # Official Razorpay Internship submission details
├── VIDEO_SCRIPT.md            # 5-minute video pitch & AI voiceover walkthrough script
└── README.md
```

---

## 🚀 Quick Start (Local Setup)

### Option 1: One-Click Startup (Windows)
- **Local Dashboard**: Double-click `start.bat` to run locally on `http://localhost:5173`.
- **Public Live Tunnel**: Double-click `start_live_tunnel.bat` to run servers and expose a public `https://*.trycloudflare.com` URL.

This automatically verifies ML models, starts the FastAPI server on port 8000, and boots the Vite dashboard on port 5173.

---

### Option 2: Manual Setup

#### 1. Backend (FastAPI)
```bash
cd backend

# Create virtual environment (optional)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install requirements
pip install -r requirements.txt

# Train models & generate test metrics (~2 mins)
python data/train_models.py

# Launch FastAPI server
uvicorn main:app --reload --port 8000
```
- API Docs: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`
- Evaluation Metrics: `http://localhost:8000/metrics`

#### 2. Frontend (React + Vite)
```bash
cd frontend

# Install dependencies
npm install

# Start Vite dev server
npm run dev
```
- Open `http://localhost:5173` to view the dashboard.

---

## 🔌 API Reference

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/fraud/score` | Score single transaction for fraud probability |
| `POST` | `/api/v1/fraud/score/batch` | Batch score up to 100 transactions simultaneously |
| `POST` | `/api/v1/return/score` | Calculate return risk and ₹ revenue-at-risk |
| `POST` | `/api/v1/chargeback/respond` | Generate dispute evidence dossier and win likelihood |
| `GET` | `/metrics` | Get held-out test evaluation metrics |
| `GET` | `/health` | Service health status check |
| `GET` | `/api/v1/demo/fraud` | Returns pre-configured high-risk fraud demo transaction |
| `GET` | `/api/v1/demo/return` | Returns pre-configured return risk demo transaction |
| `GET` | `/api/v1/demo/chargeback` | Returns pre-configured chargeback dispute demo |

### Sample Scoring Request:
```bash
curl -X POST http://localhost:8000/api/v1/fraud/score \
  -H "Content-Type: application/json" \
  -d '{
    "txn_id": "pay_TEST_99",
    "customer_id": "cust_12345",
    "merchant_id": "merch_razor_01",
    "category": "electronics",
    "amount": 75000,
    "payment_method": "credit_card",
    "state": "MH",
    "device_type": "mobile",
    "browser": "unknown",
    "device_fp": "fp_device_xyz",
    "hour": 2,
    "day_of_week": 5,
    "txn_velocity_24h": 14,
    "amount_velocity_24h": 185000,
    "device_fp_count": 22
  }'
```

### Sample Response:
```json
{
  "txn_id": "pay_TEST_99",
  "fraud_score": 0.8923,
  "is_fraud": true,
  "risk_level": "CRITICAL",
  "explanation": [
    "High transaction amount ₹75,000",
    "Velocity spike: 14 txns in 24h",
    "Device fingerprint shared across 22 accounts (syndicate ring)",
    "Transaction at 02:00 (odd midnight hour)"
  ],
  "threshold_used": 0.35
}
```

---

## 🛡️ Defense-Only Guardrails

RazorShield strictly follows defense-only engineering guidelines:
- **No offensive scraping or network scanning**: All models operate purely on internal transaction telemetry.
- **No storage of sensitive cardholder data**: Strictly complies with Indian RBI card storage and tokenization guidelines.
- **Auditable & explainable**: Every risk prediction outputs human-interpretable factors to avoid opaque rejections and unjust merchant lockouts.

---

## 🛠️ Technology Stack

- **Backend**: Python 3.12, FastAPI, Uvicorn, Pydantic v2
- **Machine Learning**: Scikit-Learn, GradientBoosting, SMOTE (`imbalanced-learn`), Joblib
- **Frontend**: React 18, Vite 5, Tailwind CSS, Recharts, Lucide Icons, Framer Motion
- **Tunneling & Deployment**: Cloudflare Tunnel (`cloudflared`), GitHub Actions CI

---

## 👤 Author

**Aniket**  
- **GitHub**: [@aniketkus](https://github.com/aniketkus)  
- **Project Repository**: [https://github.com/aniketkus/razorshield](https://github.com/aniketkus/razorshield)  
- **Track**: Razorpay AI Internship 2025 — AI Risk Manager Track

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](file:///c:/Users/hp/Downloads/razorpay%20internship/razorshield/LICENSE) file for details.
