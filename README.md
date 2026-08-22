# 🛡️ MuleGuard AI

## Financial Crime Intelligence & Mule Account Detection System

MuleGuard AI is an AI/ML-powered financial crime intelligence platform designed to identify suspicious and potential mule bank accounts from transaction data.

The system combines **supervised machine learning, anomaly detection, behavioral analysis, transaction-network intelligence, risk scoring, and explainable AI** to help investigators understand not only *which* accounts are suspicious, but also *why* they were flagged.

---

## 🎯 Project Goal

Traditional transaction monitoring can generate large numbers of alerts without clearly explaining the underlying risk.

MuleGuard aims to provide an investigator-focused workflow:

> **Detect → Score → Investigate → Explain → Report**

For every suspicious account, the platform can surface:

- Mule probability
- Overall risk score
- Behavioral risk
- Transaction risk
- Network risk
- Velocity risk
- Location risk
- Suspicious transactions
- High-risk counterparties
- Network relationships
- SHAP-based model explanations
- Human-readable AI explanations
- Recommended investigation actions
- Investigation reports

---

# 🧠 Core Technology

| Layer | Technology |
|---|---|
| Desktop Frontend | PySide6 |
| Backend API | FastAPI |
| Database | Supabase / PostgreSQL |
| Supervised ML | XGBoost |
| Anomaly Detection | Isolation Forest |
| Explainability | SHAP |
| Network Analysis | NetworkX |
| Data Processing | Pandas / NumPy |
| Deployment | Render |
| Model Persistence | joblib |

---

# 🏗️ System Architecture

```text
                    ┌─────────────────────┐
                    │   Transaction Data  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Feature Engineering │
                    │   Pandas / NumPy    │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
       ┌────────────┐   ┌──────────────┐  ┌────────────┐
       │  XGBoost   │   │ Isolation    │  │ NetworkX   │
       │  Classifier│   │ Forest       │  │ Graph      │
       └─────┬──────┘   └──────┬───────┘  └─────┬──────┘
             │                 │                 │
             └─────────────────┼─────────────────┘
                               ▼
                    ┌─────────────────────┐
                    │   Risk Score Engine │
                    └──────────┬──────────┘
                               │
                         ┌─────┴─────┐
                         ▼           ▼
                    ┌────────┐  ┌───────────┐
                    │  SHAP  │  │  Alerts   │
                    └────┬───┘  └─────┬─────┘
                         │             │
                         └──────┬──────┘
                                ▼
                       ┌────────────────┐
                       │    FastAPI     │
                       └───────┬────────┘
                               │
                    ┌──────────┴──────────┐
                    ▼                     ▼
             ┌─────────────┐       ┌─────────────┐
             │ Supabase /  │       │   PySide6   │
             │ PostgreSQL   │       │  Dashboard  │
             └─────────────┘       └─────────────┘
```

---

# 🔍 Detection Engine

MuleGuard uses multiple signals rather than depending on a single model.

## 1. Supervised Classification

**XGBoost** is used to classify accounts based on engineered transaction and behavioral features.

Example outputs:

```text
Mule Probability: 94.2%
Classification: SUSPICIOUS
```

---

## 2. Anomaly Detection

**Isolation Forest** identifies accounts or transaction behavior that significantly differs from normal patterns.

Potential anomaly signals include:

- Unusual transaction frequency
- Unusual transaction amounts
- Sudden activity spikes
- Abnormal credit/debit behavior
- Rapid movement of received funds
- Unusual payment patterns

---

## 3. Transaction Network Analysis

MuleGuard represents transaction relationships as a graph using **NetworkX**.

```text
                 ACC-201
                    │
                  ₹45K
                    ↓
ACC-305 ───────► ACC-10293 ───────► ACC-901
                    │
                  ₹28K
                    ↓
                 ACC-405
```

Network features include:

- Fan-in
- Fan-out
- Unique counterparties
- Rapid transfers
- Circular flows
- Shared beneficiaries
- High-risk connections
- Transaction concentration
- Pass-through behavior

---

# 🎯 Risk Scoring

Each suspicious account receives an overall risk score from **0–100**.

Example:

```text
MULE RISK

94 / 100
CRITICAL

Behavior Risk       92
Transaction Risk    89
Network Risk        96
Velocity Risk       94
Location Risk       78
```

Risk levels:

| Score | Level | Suggested Action |
|---:|---|---|
| 0–39 | Low | Monitor |
| 40–69 | Medium | Enhanced Monitoring |
| 70–89 | High | Manual Review |
| 90–100 | Critical | Enhanced Due Diligence / Investigation |

> These are AI-assisted recommendations for the prototype and should not be treated as automated banking decisions.

---

# 🔬 Explainable AI

MuleGuard uses **SHAP** to explain model predictions.

Example:

```text
Transaction Velocity       +0.31
Unique Senders             +0.26
Rapid Fund Movement        +0.22
Network Connectivity       +0.18
Amount Deviation           +0.14
New Beneficiaries          +0.11
```

The system also converts model signals into human-readable explanations:

> The account demonstrates a high-volume pass-through pattern. It receives funds from multiple unrelated accounts and transfers a significant portion of those funds within a short period.

Example evidence:

```text
✓ 17 unique senders
✓ 83% of incoming funds transferred within 15 minutes
✓ 6 high-risk counterparties
✓ Transaction volume 8.4× peer average
✓ 4 newly added beneficiaries
```

---

# 🖥️ Frontend

MuleGuard is designed as a desktop enterprise application using **PySide6**.

The UI follows a professional banking / financial-crime investigation design:

- Deep Navy
- White
- Slate
- Professional Blue
- Meaningful risk colors
- Dense data tables
- Clear KPIs
- Minimal decoration
- No gradients
- No neon
- No glassmorphism
- No cyberpunk styling
- No decorative animations

Recommended application size:

```text
Minimum:    1280 × 720
Preferred:  1440 × 900
```

---

# 📊 Main Dashboard

The dashboard provides a high-level view of financial crime activity.

### KPI Cards

- Total Accounts
- Total Transaction Amount
- Total Credit
- Total Debit
- Fraud Transactions
- Active Alerts

### Dashboard Analytics

- Transaction Activity
- Credit transactions
- Debit transactions
- Fraud transactions
- High-risk accounts
- Active alerts

---

# 🚨 Risk Monitoring

## Active Alerts

Investigators can filter alerts by:

- Search
- Risk level
- Alert type
- Date
- Status
- Amount

Supported alert types include:

- Rapid Fund Movement
- Unusual Transaction Velocity
- High Incoming Volume
- High Outgoing Volume
- Suspicious Counterparty
- Circular Transaction
- New Beneficiary
- Location Anomaly
- Payment Pattern Anomaly

---

## 📡 Live Transaction Monitor

The monitoring terminal displays:

- Timestamp
- Transaction ID
- Sender
- Receiver
- Amount
- Payment method
- Risk score
- Risk level
- Status

For the hackathon, the live feed can use simulated transaction events when a real streaming source is unavailable.

---

# 👤 Account Investigation

Each account has a dedicated investigation page.

### Account Information

- Account holder
- Masked account number
- IFSC
- Region / location
- Account age
- Payment methods

### Financial Summary

- Total credit
- Total debit
- Incoming transactions
- Outgoing transactions
- Average transaction amount
- Maximum transaction amount
- Minimum transaction amount
- Daily transaction volume
- Credit/debit ratio

### Payment Intelligence

Supported payment methods can include:

- UPI
- Debit Card
- Credit Card
- Net Banking
- PayPal
- Other

The application should only display payment methods actually present in the dataset.

---

# 🌍 Regional Intelligence

MuleGuard can analyze:

- Account region
- Transaction region
- Sender locations
- Receiver locations
- High-risk regions
- Location anomalies

Regional analytics can include:

```text
Region
Accounts
Transactions
Fraud Cases
Fraud Amount
Risk Score
Risk Level
```

---

# 💳 Transaction Investigation

Investigators can search and filter transactions by:

- Date
- Amount
- Credit / Debit
- Payment method
- Risk
- Account
- Region
- Status

Transaction records include:

- Transaction ID
- Timestamp
- Sender account
- Receiver account
- Amount
- Transaction type
- Payment method
- Region
- Risk score
- Status

A transaction detail view also explains why the transaction was flagged.

---

# 🕸️ Network Analysis

Transaction Network Analysis is one of MuleGuard's primary differentiating capabilities.

For a selected account, investigators can examine:

- Unique senders
- Unique receivers
- Total connections
- Rapid transfers
- High-risk counterparties
- Fan-in
- Fan-out
- Circular flows
- Shared beneficiaries
- Transaction concentration
- Pass-through behavior

Example:

```text
Network Risk: 96 / 100
CRITICAL
```

---

# 📈 Fraud Analytics

MuleGuard supports monthly fraud analysis.

Example:

```text
Month       Fraud Transactions
--------------------------------
August              14
July                 9
June                 6
May                  5
April                3
March                2
```

Month-over-month metrics can include:

- Fraud transaction count
- Fraud amount
- Suspicious account count
- Percentage change

---

# 📉 Risk History

Risk can be tracked over time.

Example:

```text
April       41
May         48
June        57
July        76
August      94
```

This helps investigators identify increasing account risk rather than relying only on a single transaction.

---

# 📝 Investigation Reports

MuleGuard can generate an investigation report containing:

- Account information
- Risk score
- Mule probability
- Suspicious transactions
- Network evidence
- SHAP factors
- Behavioral indicators
- Payment methods
- Location indicators
- Monthly risk trend
- AI summary
- Recommended action

Reports can be exported as PDF.

---

# 🔌 Backend API

The frontend is designed to communicate with FastAPI rather than storing intelligence directly inside the UI.

Planned endpoints:

```text
GET  /dashboard
GET  /accounts
GET  /accounts/{id}
GET  /transactions
GET  /alerts
GET  /network/{account_id}
GET  /risk/{account_id}
GET  /explanation/{account_id}
GET  /analytics/monthly
GET  /regional-risk
GET  /payment-methods
POST /investigation-report
GET  /health
```

This keeps the frontend replaceable and allows the ML/risk engine to evolve independently.

---

# 🗄️ Data Flow

```text
Dataset
   ↓
Data Cleaning
   ↓
Feature Engineering
   ↓
ML Models
   ↓
Network Analysis
   ↓
Risk Engine
   ↓
FastAPI
   ↓
Supabase / PostgreSQL
   ↓
PySide6
```

The frontend should not contain hardcoded intelligence.

---

# ⚙️ System Health

MuleGuard exposes system health information so investigators and judges can see whether the platform is operational.

Example:

```text
● AI Engine Online
● API Connected
● Database Connected
● Model Loaded
```

If a service fails:

```text
● AI Engine Online
● API Connected
● Database Offline
```

---

# 🧭 Application Navigation

```text
MULEGUARD
Financial Intelligence

OVERVIEW
  Dashboard

RISK MONITORING
  Active Alerts
  Live Transactions

INVESTIGATION
  Accounts
  Transactions
  Network Analysis

ANALYTICS
  Fraud Analytics
  Regional Risk
  Payment Methods

INTELLIGENCE
  AI Risk Analysis
  Investigation Reports

Settings
Logout
```

---

# 🔄 Primary Investigator Workflow

The intended judge / investigator experience is:

```text
LOGIN
  ↓
DASHBOARD
  ↓
ACTIVE ALERT
  ↓
ACCOUNT INVESTIGATION
  ↓
RISK SCORE
  ↓
TRANSACTION HISTORY
  ↓
NETWORK GRAPH
  ↓
SHAP EXPLANATION
  ↓
AI EXPLANATION
  ↓
INVESTIGATION REPORT
  ↓
EXPORT PDF
```

The central product message is:

> **MuleGuard doesn't simply classify an account as suspicious. It shows the investigator the financial behavior, transaction network, risk factors and model reasoning behind that decision.**

---

# 🚀 Deployment

The backend is intended to be deployed using **Render**.

The database uses **Supabase/PostgreSQL**.

For the hackathon, the deployment should be tested before the final judging window and the backend kept warm where possible to minimize cold-start delays.

---

# 🔐 Security & Privacy

MuleGuard is a prototype financial-crime intelligence system.

Recommended production controls include:

- Authentication
- Role-based access control
- Masked account numbers
- Secure API authentication
- Environment variables for secrets
- HTTPS
- Database access controls
- Audit logging
- Least-privilege permissions

Do not commit secrets, API keys, database passwords, or production credentials to the repository.

---

# 📁 Suggested Project Structure

```text
muleguard/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   ├── models/
│   │   ├── services/
│   │   ├── risk/
│   │   └── database/
│   │
│   ├── ml/
│   │   ├── feature_engineering.py
│   │   ├── train.py
│   │   ├── predict.py
│   │   ├── explain.py
│   │   └── network.py
│   │
│   └── requirements.txt
│
├── frontend/
│   ├── main.py
│   ├── pages/
│   ├── components/
│   ├── services/
│   ├── assets/
│   └── requirements.txt
│
├── models/
│   ├── xgboost_model.joblib
│   ├── isolation_forest.joblib
│   └── feature_config.joblib
│
├── data/
│   └── README.md
│
├── reports/
│
├── tests/
│
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

---

# 🧪 Testing

The system should be tested at multiple levels:

### Data

- Missing values
- Invalid transactions
- Duplicate records
- Incorrect account references

### ML

- Classification performance
- False positives
- False negatives
- Class imbalance
- Feature stability

### API

- Health endpoint
- Account lookup
- Risk endpoint
- Alert retrieval
- Network endpoint
- SHAP explanation endpoint

### Frontend

- Login flow
- Dashboard loading
- Account navigation
- Alert investigation
- Network visualization
- SHAP visualization
- Report generation

---

# 🏆 Hackathon Demo Priorities

If development time becomes limited, prioritize these capabilities:

1. Login
2. Dashboard
3. Suspicious Account
4. Risk Score
5. Transaction History
6. Transaction Network
7. SHAP Explanation
8. AI Investigation Report

The strongest demonstration is:

```text
Login
  →
Dashboard
  →
Alert
  →
Account
  →
Risk 94/100
  →
Transactions
  →
Network
  →
SHAP
  →
AI Explanation
  →
Investigation Report
```

---

# ⚠️ Prototype Disclaimer

MuleGuard AI is a hackathon/prototype system intended for demonstrating AI-assisted financial crime detection and investigation workflows.

Its risk scores, classifications, explanations, and recommended actions should **not** be treated as autonomous banking, regulatory, account-freezing, or law-enforcement decisions.

Production deployment would require appropriate validation, governance, security, compliance review, model monitoring, and human oversight.

---

# 👥 Project

**MuleGuard AI**

**Financial Crime Intelligence & Mule Account Detection System**

Built for **SquidHack Finals — SAGE University Indore**

**Date:** 22–23 August 2026

---

## Core Value Proposition

> **Detect suspicious mule accounts. Understand their behavior. Trace their transaction networks. Explain the AI decision. Help investigators act faster.**
