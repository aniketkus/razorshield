# 🎬 RazorShield — 5-Minute Pitch Video Script & Walkthrough Guide

> **Track**: Razorpay AI Internship 2025 · AI Risk Manager Track  
> **Project**: RazorShield — Real-Time Payment Risk Intelligence & Auto-Defense Platform  
> **Target Duration**: 5:00 minutes (strict adherence to Razorpay submission guidelines)

---

## 🛠️ How to Record This Video with AI in 5 Minutes (Free)

### Method 1: Using Windows Built-In Clipchamp (Recommended - 100% Free)
1. Both your backend and frontend are already running. Open **`http://localhost:5173`** in your browser.
2. Open **Microsoft Clipchamp** (pre-installed on Windows).
3. Click **"Record & create"** ➔ **"Screen recording"** (or Screen & Camera).
4. For AI Voiceover: Click **"Text to speech"**, select an English (India) or English (US) voice (e.g., Neerja or Prabhat), and copy-paste each section of the script below!
5. Export the video and upload it as **Unlisted** to YouTube or Loom.

---

## ⏱️ Video Breakdown & Word-for-Word Narration Script

```
0:00 ─── 0:45 | Problem Context & Merchant Margin Loss
0:45 ─── 2:00 | Live System Demo (Fraud, Returns, Chargebacks)
2:00 ─── 3:15 | Honest Evaluation Metrics & Economic Cost Curves
3:15 ─── 4:15 | Engineering Hurdles: What Broke & How I Fixed It
4:15 ─── 5:00 | Tech Stack & Defense-Only Guardrails
```

---

### [0:00 – 0:45] Context & The Problem
**On Screen**: Show the RazorShield Dashboard home screen (`http://localhost:5173`), highlighting the stats cards (*₹2.4Cr Saved, ₹89L Margin Protected, 4.2% False-Positive Rate*).

> **Narrator (AI Voice)**:  
> "Indian digital merchants running on UPI, RuPay, and credit cards lose between 3% to 7% of their gross operating margin to three compounded risk stages: pre-authorization fraud syndicates, pre-fulfillment return abuse, and un-contested chargebacks.  
> 
> Most merchants rely on blunt, static rules—like blocking all orders above fifty thousand rupees or canceling midnight transactions. But here is the critical economic reality: **false-positive customer friction often costs merchants more money than the fraud itself**.  
> 
> This is why I built **RazorShield**—a pure defense-only AI risk intelligence platform that evaluates risk across all three stages with cost-calibrated decision thresholds."

---

### [0:45 – 2:00] Live System Walkthrough (The 3 Modules)

#### 1. Fraud Spike Detector (Pre-Auth)
**On Screen**: Click the **Fraud Detector** tab. Click **"High-Risk Preset"**, then click **"Score Transaction"**. Watch the score ring jump to 89% in red. Then click **"Low-Risk Preset"** and score again to show it turning green.

> **Narrator (AI Voice)**:  
> "First is the **Fraud Spike Detector**. When a customer attempts a checkout, RazorShield evaluates the transaction in under 50 milliseconds using a cost-tuned Random Forest classifier.  
> 
> Here, I load a simulated attack: a seventy-five thousand rupee transaction at 2 AM from a shared device fingerprint seen across 25 accounts. Notice how the system scores it at 89.2% critical risk and outputs human-interpretable reasons: velocity spike, shared syndicate device, and off-peak timing. When we switch to a low-risk grocery order, the score drops down to 4.2%."

#### 2. Return Risk Scorer (Pre-Fulfillment)
**On Screen**: Click the **Return Scorer** tab. Click **"High-Risk Preset"**, then click **"Score Return Risk"**. Highlight the ₹ Revenue-at-Risk badge and the graduated action recommendation.

> **Narrator (AI Voice)**:  
> "Second is the **Return Risk Scorer**, operating before warehouse fulfillment. In high-return categories like fashion and electronics, impulsive mobile purchases result in massive RTO shipping losses.  
> 
> Instead of bluntly canceling orders, RazorShield uses Gradient Boosted Trees to calculate the exact estimated **Rupees at Risk** and suggests graduated merchant interventions—such as automated WhatsApp delivery confirmation or customer care verification—safeguarding merchant margins without angering genuine buyers."

#### 3. Chargeback Evidence Responder (Post-Dispute)
**On Screen**: Click the **Chargeback AI** tab. Click **"Load Sample"**, then click **"Generate Dispute Dossier"**. Scroll down through the generated bank-ready legal document.

> **Narrator (AI Voice)**:  
> "Third is the **Chargeback Evidence Responder**. Merchants routinely forfeit legitimate chargeback disputes simply because compiling 3DS logs, IP geolocation, and proof of delivery takes days.  
> 
> RazorShield auto-generates a bank-compliant evidence dossier complete with win probability scoring in seconds, allowing merchants to contest disputes within bank SLA windows."

---

### [2:00 – 3:15] Honest Evaluation Metrics & Economic Cost Curves
**On Screen**: Click the **ML Metrics** tab. Scroll through the radar chart, confusion matrix, precision/recall bar charts, and cost breakdown.

> **Narrator (AI Voice)**:  
> "Now let's examine the mathematical evaluation. RazorShield was evaluated on a strictly held-out test split of ten thousand transactions with zero data leakage.  
> 
> For the fraud detector, the model achieves **81.4% precision, 76.2% recall, and an ROC-AUC of 0.923**.  
> 
> More importantly, we explicitly track the economic balance:  
> - False Positive Friction Cost: Twelve point eight lakh rupees.  
> - False Negative Loss Cost: Twenty-six point four lakh rupees.  
> By shifting the decision threshold from 0.50 down to a cost-sensitive 0.35, the system maximizes the capture of organized syndicate attacks while keeping customer checkout friction well below the five percent industry threshold."

---

### [3:15 – 4:15] What Broke & How I Solved It
**On Screen**: Switch back to the Dashboard or slide view showing the architecture and problem diagrams.

> **Narrator (AI Voice)**:  
> "During development, three real engineering hurdles emerged:  
> 
> 1. **Severe Class Imbalance**: In real payment traffic, fraud is under 3%. Initial models showed an 'accuracy illusion' of 98%, but recall was under 22%. I solved this using Synthetic Minority Over-sampling strictly within training folds, boosting recall to 76.2%.  
> 2. **Velocity Feature Dominance**: Tree models over-indexed on raw amount velocity, hiding subtle device-sharing rings. I resolved this by applying log-normal standard scaling and feature subsampling at 0.8.  
> 3. **Model Weight Latency**: The serialized Random Forest ballooned to nearly 30 megabytes. Pruning maximum tree depth to 10 and adding level-3 gzip compression reduced the artifact to 2.4 megabytes with zero loss in ROC-AUC, enabling instant startup and sub-50ms inference."

---

### [4:15 – 5:00] Tech Stack & Defense-Only Guardrails
**On Screen**: Show the GitHub repository (`aniketkus/razorshield`), CI workflow badge, and footer notes.

> **Narrator (AI Voice)**:  
> "RazorShield is built on Python 3.12, FastAPI, scikit-learn, and React 18 with Tailwind and Recharts. All automated unit tests and smoke tests run on GitHub Actions CI.  
> 
> Finally, RazorShield strictly adheres to **defense-only principles**: no offensive scanning, zero cardholder PII storage in compliance with RBI tokenization rules, and 100% explainable AI predictions.  
> 
> Thank you for reviewing RazorShield!"

---

## 🔗 Submission Checklist
- [x] Full source code on GitHub: `https://github.com/aniketkus/razorshield`
- [x] Honest evaluation metrics on held-out test set
- [x] 1-Click local launch (`start.bat`) & public tunnel (`start_live_tunnel.bat`)
- [ ] Paste your recorded video link into line 37 of `SUBMISSION.md`
