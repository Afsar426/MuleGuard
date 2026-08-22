import random
from datetime import datetime, timedelta
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from pydantic import BaseModel
import networkx as nx
import os

# PDF generation imports
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

app = FastAPI(title="MuleGuard API", version="1.0.0")

# ---------------------------------------------------------
# MOCK DATA GENERATION ENGINE
# ---------------------------------------------------------
# Set random seed for consistency
random.seed(42)

# Global memory storage
accounts_db = {}
transactions_db = []
alerts_db = []
regional_db = []
payment_methods_db = {}

# Constants from Specification
COLOR_DEEP_NAVY = "#0B1F33"
COLOR_PRIMARY_BLUE = "#155EEF"
COLOR_SOFT_GRAY = "#F5F7FA"
COLOR_DARK_NAVY = "#172B4D"
COLOR_SLATE = "#667085"

# Setup data
INDIAN_NAMES = [
    "Aarav Sharma", "Vihaan Patel", "Aditya Iyer", "Sai Reddy", "Reyansh Gupta",
    "Arjun Verma", "Krishna Nair", "Ishaan Joshi", "Shaurya Choudhury", "Aayush Rao",
    "Ananya Sen", "Diya Mishra", "Pari Saxena", "Kiara Bhat", "Saisha Kulkarni",
    "Aadhya Deshmukh", "Zara Mehra", "Prisha Kapoor", "Anika Prasad", "Sanya Goel"
]
REGIONS = ["Madhya Pradesh", "Maharashtra", "Karnataka", "Delhi", "Tamil Nadu", "Gujarat", "Uttar Pradesh", "West Bengal"]
CITIES = {
    "Madhya Pradesh": ["Indore", "Bhopal", "Gwalior"],
    "Maharashtra": ["Mumbai", "Pune", "Nagpur"],
    "Karnataka": ["Bangalore", "Mysore", "Hubli"],
    "Delhi": ["New Delhi", "Dwarka", "Rohini"],
    "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai"],
    "Gujarat": ["Ahmedabad", "Surat", "Vadodara"],
    "Uttar Pradesh": ["Lucknow", "Kanpur", "Noida"],
    "West Bengal": ["Kolkata", "Howrah", "Darjeeling"]
}

def generate_mock_data():
    global accounts_db, transactions_db, alerts_db, regional_db, payment_methods_db
    
    # 1. Accounts Database (12,450 accounts)
    total_accounts = 12450
    
    # Create the specific target account ACC-10293
    target_id = "ACC-10293"
    accounts_db[target_id] = {
        "account_id": target_id,
        "holder_name": "Aarav Sharma",
        "account_number": "XXXX XXXX 1029",
        "ifsc_code": "XXXX0001234",
        "region": "Madhya Pradesh",
        "city": "Indore",
        "age_months": 8,
        "credit_amount": 1840000.0, # ₹18.4L
        "debit_amount": 1790000.0,  # ₹17.9L
        "risk_score": 94,
        "risk_level": "Critical",
        "status": "Under Investigation",
        "payment_methods": ["UPI", "Debit Card", "Credit Card", "Net Banking"],
        "avg_transaction": 12500.0,
        "max_transaction": 85000.0,
        "min_transaction": 150.0,
        "daily_volume": 12
    }
    
    # Add other mock accounts
    for i in range(10000, 10000 + total_accounts - 1):
        acc_id = f"ACC-{i}"
        if acc_id == target_id:
            continue
        
        region = random.choice(REGIONS)
        city = random.choice(CITIES[region])
        age = random.randint(1, 120)
        risk = random.randint(5, 95)
        
        if risk >= 90:
            risk_lvl = "Critical"
            status = random.choice(["Under Investigation", "Open Alert"])
        elif risk >= 75:
            risk_lvl = "High"
            status = random.choice(["Open Alert", "Monitored"])
        elif risk >= 40:
            risk_lvl = "Medium"
            status = "Monitored"
        else:
            risk_lvl = "Low/Safe"
            status = "Active"
            
        credit = round(random.uniform(5000, 5000000), 2)
        debit = round(credit * random.uniform(0.8, 1.15), 2)
        
        methods = random.sample(["UPI", "Debit Card", "Credit Card", "Net Banking", "PayPal"], k=random.randint(1, 4))
        
        accounts_db[acc_id] = {
            "account_id": acc_id,
            "holder_name": random.choice(INDIAN_NAMES) + f" #{i-9999}",
            "account_number": f"XXXX XXXX {random.randint(1000, 9999)}",
            "ifsc_code": f"XXXX000{random.randint(1000, 9999)}",
            "region": region,
            "city": city,
            "age_months": age,
            "credit_amount": credit,
            "debit_amount": debit,
            "risk_score": risk,
            "risk_level": risk_lvl,
            "status": status,
            "payment_methods": methods,
            "avg_transaction": round(debit / random.randint(10, 100), 2),
            "max_transaction": round(debit * random.uniform(0.1, 0.4), 2),
            "min_transaction": round(random.uniform(10, 500), 2),
            "daily_volume": random.randint(1, 25)
        }
        
    # Ensure sender ACC-4412 exists
    accounts_db["ACC-4412"] = {
        "account_id": "ACC-4412",
        "holder_name": "Rohan Deshmukh",
        "account_number": "XXXX XXXX 4412",
        "ifsc_code": "XXXX0009876",
        "region": "Maharashtra",
        "city": "Mumbai",
        "age_months": 24,
        "credit_amount": 4500000.0,
        "debit_amount": 4200000.0,
        "risk_score": 35,
        "risk_level": "Low/Safe",
        "status": "Active",
        "payment_methods": ["UPI", "Net Banking"],
        "avg_transaction": 22000.0,
        "max_transaction": 120000.0,
        "min_transaction": 100.0,
        "daily_volume": 4
    }

    # 2. Alerts (24 active alerts)
    # Target Alert AL-10492 for Aarav Sharma
    alerts_db.append({
        "alert_id": "AL-10492",
        "account_id": target_id,
        "holder_name": "Aarav Sharma",
        "alert_type": "Rapid Fund Movement",
        "risk_score": 94,
        "risk_level": "Critical",
        "amount": 85000.0,
        "detected_time": (datetime.now() - timedelta(minutes=2)).strftime("%Y-%m-%d %H:%M:%S"),
        "status": "Open"
    })
    
    alert_types = [
        "Rapid Fund Movement", "Unusual Transaction Velocity", "High Incoming Volume",
        "High Outgoing Volume", "Suspicious Counterparty", "Circular Transaction",
        "New Beneficiary", "Location Anomaly", "Payment Pattern Anomaly"
    ]
    
    # Generate 23 other alerts
    high_risk_accs = [k for k, v in accounts_db.items() if v["risk_score"] >= 75 and k != target_id]
    for idx, acc_id in enumerate(random.sample(high_risk_accs, 23)):
        acc = accounts_db[acc_id]
        alerts_db.append({
            "alert_id": f"AL-{10493 + idx}",
            "account_id": acc_id,
            "holder_name": acc["holder_name"],
            "alert_type": random.choice(alert_types),
            "risk_score": acc["risk_score"],
            "risk_level": acc["risk_level"],
            "amount": round(random.uniform(10000, 500000), 2),
            "detected_time": (datetime.now() - timedelta(minutes=random.randint(10, 1440))).strftime("%Y-%m-%d %H:%M:%S"),
            "status": "Open"
        })

    # 3. Transactions (Generate historic + specific transactions)
    # The target transaction TX-82921 for Aarav Sharma
    tx_time = (datetime.now() - timedelta(minutes=2)).strftime("%Y-%m-%d %H:%M:%S")
    target_tx = {
        "transaction_id": "TX-82921",
        "timestamp": tx_time,
        "sender_id": "ACC-4412",
        "sender_name": "Rohan Deshmukh",
        "receiver_id": target_id,
        "receiver_name": "Aarav Sharma",
        "amount": 85000.0,
        "transaction_type": "Credit",
        "payment_method": "UPI",
        "region": "Madhya Pradesh",
        "city": "Indore",
        "risk_score": 94,
        "risk_level": "Critical",
        "status": "FLAGGED",
        "reasons": ["Unusual amount", "New beneficiary", "High transaction velocity", "Suspicious network relationship", "Unusual time"]
    }
    transactions_db.append(target_tx)
    
    # Generate network specific connections for ACC-10293
    # ACC-201 -> ACC-10293
    transactions_db.append({
        "transaction_id": f"TX-{random.randint(20000, 29999)}",
        "timestamp": (datetime.now() - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S"),
        "sender_id": "ACC-201", "sender_name": "External Sender A", "receiver_id": target_id, "receiver_name": "Aarav Sharma",
        "amount": 45000.0, "transaction_type": "Credit", "payment_method": "UPI", "region": "Madhya Pradesh", "city": "Indore",
        "risk_score": 82, "risk_level": "High", "status": "FLAGGED", "reasons": ["High incoming volume"]
    })
    # ACC-305 -> ACC-10293
    transactions_db.append({
        "transaction_id": f"TX-{random.randint(20000, 29999)}",
        "timestamp": (datetime.now() - timedelta(hours=5)).strftime("%Y-%m-%d %H:%M:%S"),
        "sender_id": "ACC-305", "sender_name": "External Sender B", "receiver_id": target_id, "receiver_name": "Aarav Sharma",
        "amount": 12000.0, "transaction_type": "Credit", "payment_method": "Net Banking", "region": "Madhya Pradesh", "city": "Indore",
        "risk_score": 60, "risk_level": "Medium", "status": "APPROVED", "reasons": []
    })
    # ACC-10293 -> ACC-901
    transactions_db.append({
        "transaction_id": f"TX-{random.randint(20000, 29999)}",
        "timestamp": (datetime.now() - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"),
        "sender_id": target_id, "sender_name": "Aarav Sharma", "receiver_id": "ACC-901", "receiver_name": "External Receiver A",
        "amount": 55000.0, "transaction_type": "Debit", "payment_method": "UPI", "region": "Maharashtra", "city": "Mumbai",
        "risk_score": 90, "risk_level": "Critical", "status": "FLAGGED", "reasons": ["Pass-through behavior"]
    })
    # ACC-10293 -> ACC-405
    transactions_db.append({
        "transaction_id": f"TX-{random.randint(20000, 29999)}",
        "timestamp": (datetime.now() - timedelta(minutes=45)).strftime("%Y-%m-%d %H:%M:%S"),
        "sender_id": target_id, "sender_name": "Aarav Sharma", "receiver_id": "ACC-405", "receiver_name": "External Receiver B",
        "amount": 28000.0, "transaction_type": "Debit", "payment_method": "UPI", "region": "Delhi", "city": "New Delhi",
        "risk_score": 88, "risk_level": "High", "status": "FLAGGED", "reasons": ["Rapid transfer outgoing"]
    })
    
    # Generic transactions across other accounts
    all_keys = list(accounts_db.keys())
    for i in range(1500):
        s_id = random.choice(all_keys)
        r_id = random.choice(all_keys)
        while r_id == s_id:
            r_id = random.choice(all_keys)
            
        sender = accounts_db[s_id]
        receiver = accounts_db[r_id]
        amt = round(random.uniform(500, 150000), 2)
        
        # Decide type
        tx_type = random.choice(["Credit", "Debit"])
        method = random.choice(sender["payment_methods"])
        
        risk = max(sender["risk_score"], receiver["risk_score"]) - random.randint(0, 15)
        risk = max(5, min(99, risk))
        
        if risk >= 85:
            risk_lvl = "Critical"
            status = "FLAGGED"
            reasons = random.sample(["Unusual amount", "High velocity", "Suspicious sender", "Regional Anomaly"], k=random.randint(1, 2))
        else:
            risk_lvl = "Low/Safe" if risk < 40 else "Medium"
            status = "APPROVED"
            reasons = []
            
        transactions_db.append({
            "transaction_id": f"TX-{82922 + i}",
            "timestamp": (datetime.now() - timedelta(days=random.randint(0, 180), hours=random.randint(0, 23), minutes=random.randint(0, 59))).strftime("%Y-%m-%d %H:%M:%S"),
            "sender_id": s_id,
            "sender_name": sender["holder_name"],
            "receiver_id": r_id,
            "receiver_name": receiver["holder_name"],
            "amount": amt,
            "transaction_type": tx_type,
            "payment_method": method,
            "region": sender["region"],
            "city": sender["city"],
            "risk_score": risk,
            "risk_level": risk_lvl,
            "status": status,
            "reasons": reasons
        })

    # Sort transactions by date descending
    transactions_db.sort(key=lambda x: x["timestamp"], reverse=True)

    # 4. Regional Statistics
    regional_db = [
        {"region": "Madhya Pradesh", "accounts_count": 1842, "transactions_count": 18421, "fraud_count": 42, "volume": 1240000.0, "active_alerts": 8, "risk": "HIGH"},
        {"region": "Maharashtra", "accounts_count": 2984, "transactions_count": 28401, "fraud_count": 51, "volume": 3450000.0, "active_alerts": 12, "risk": "CRITICAL"},
        {"region": "Karnataka", "accounts_count": 2105, "transactions_count": 21840, "fraud_count": 24, "volume": 2100000.0, "active_alerts": 4, "risk": "MEDIUM"},
        {"region": "Delhi", "accounts_count": 1948, "transactions_count": 19280, "fraud_count": 18, "volume": 1850000.0, "active_alerts": 2, "risk": "MEDIUM"},
        {"region": "Tamil Nadu", "accounts_count": 1542, "transactions_count": 14920, "fraud_count": 12, "volume": 1150000.0, "active_alerts": 1, "risk": "LOW"},
    ]

    # 5. Payment Methods Statistics
    payment_methods_db = {
        "distribution": {"UPI": 62, "Debit Card": 24, "Credit Card": 9, "Net Banking": 5, "PayPal": 0},
        "risk_levels": {"UPI": 84, "Debit Card": 45, "Credit Card": 30, "Net Banking": 52, "PayPal": 10}
    }

generate_mock_data()

# ---------------------------------------------------------
# BACKEND API ROUTING
# ---------------------------------------------------------

class LoginRequest(BaseModel):
    employee_id: str
    password: str

@app.post("/login")
def login(req: LoginRequest):
    # Dummy login for testing
    if req.employee_id == "admin" or "@" in req.employee_id:
        return {"status": "success", "employee_id": req.employee_id, "token": "mock-jwt-token-12345"}
    raise HTTPException(status_code=401, detail="Invalid Employee ID/Email or Password")

@app.get("/health")
def health():
    return {
        "status": "ok",
        "api": "connected",
        "database": "connected",
        "model": "loaded",
        "version": "1.0.0"
    }

@app.get("/dashboard")
def get_dashboard():
    # Calculate stats
    total_accounts = len(accounts_db)
    # Total transaction amount
    total_tx_amount = sum(tx["amount"] for tx in transactions_db)
    
    # Credit/debit totals
    total_credit = sum(acc["credit_amount"] for acc in accounts_db.values())
    total_debit = sum(acc["debit_amount"] for acc in accounts_db.values())
    
    # Count of flagged/fraud tx
    fraud_transactions = sum(1 for tx in transactions_db if tx["status"] == "FLAGGED")
    active_alerts = len(alerts_db)
    
    # Recent high risk alerts
    recent_alerts = alerts_db[:5]
    
    # Recent suspicious accounts
    suspicious_accounts = [
        {
            "account_id": acc["account_id"],
            "holder_name": acc["holder_name"],
            "account_number": acc["account_number"],
            "risk_score": acc["risk_score"],
            "amount": acc["credit_amount"],
            "region": acc["region"],
            "status": acc["status"]
        }
        for acc in list(accounts_db.values()) if acc["risk_score"] >= 80
    ][:6]
    
    # Chart data (24h, 7d, 30d, 6m counts)
    chart_data = {
        "labels": ["Mar", "Apr", "May", "Jun", "Jul", "Aug"],
        "total": [450, 520, 610, 580, 710, 840],
        "credit": [220, 270, 310, 290, 360, 430],
        "debit": [230, 250, 300, 290, 350, 410],
        "fraud": [2, 3, 5, 6, 9, 14]
    }
    
    return {
        "total_accounts": total_accounts,
        "total_tx_amount": total_tx_amount,
        "total_credit": total_credit,
        "total_debit": total_debit,
        "fraud_transactions": fraud_transactions,
        "active_alerts": active_alerts,
        "recent_alerts": recent_alerts,
        "suspicious_accounts": suspicious_accounts,
        "chart_data": chart_data
    }

@app.get("/accounts")
def get_accounts(
    search: Optional[str] = None,
    risk_level: Optional[str] = None,
    region: Optional[str] = None,
    limit: int = 50,
    offset: int = 0
):
    filtered = list(accounts_db.values())
    
    if search:
        s_lower = search.lower()
        filtered = [
            a for a in filtered 
            if s_lower in a["account_id"].lower() 
            or s_lower in a["holder_name"].lower() 
            or s_lower in a["account_number"].lower()
            or s_lower in a["ifsc_code"].lower()
        ]
        
    if risk_level and risk_level != "All":
        filtered = [a for a in filtered if a["risk_level"].lower() == risk_level.lower()]
        
    if region and region != "All":
        filtered = [a for a in filtered if a["region"].lower() == region.lower()]
        
    # Sort by risk score descending
    filtered.sort(key=lambda x: x["risk_score"], reverse=True)
    
    total = len(filtered)
    paginated = filtered[offset : offset + limit]
    
    return {"total": total, "accounts": paginated}

@app.get("/accounts/{account_id}")
def get_account_detail(account_id: str):
    if account_id in accounts_db:
        return accounts_db[account_id]
    raise HTTPException(status_code=404, detail="Account not found")

@app.get("/transactions")
def get_transactions(
    account_id: Optional[str] = None,
    search: Optional[str] = None,
    risk_level: Optional[str] = None,
    payment_method: Optional[str] = None,
    limit: int = 50,
    offset: int = 0
):
    filtered = transactions_db
    
    if account_id:
        filtered = [t for t in filtered if t["sender_id"] == account_id or t["receiver_id"] == account_id]
        
    if search:
        s_lower = search.lower()
        filtered = [
            t for t in filtered 
            if s_lower in t["transaction_id"].lower() 
            or s_lower in t["sender_name"].lower() 
            or s_lower in t["receiver_name"].lower()
            or s_lower in t["sender_id"].lower()
            or s_lower in t["receiver_id"].lower()
        ]
        
    if risk_level and risk_level != "All":
        filtered = [t for t in filtered if t["risk_level"].lower() == risk_level.lower()]
        
    if payment_method and payment_method != "All":
        filtered = [t for t in filtered if t["payment_method"].lower() == payment_method.lower()]
        
    total = len(filtered)
    paginated = filtered[offset : offset + limit]
    
    return {"total": total, "transactions": paginated}

@app.get("/alerts")
def get_alerts():
    return alerts_db

@app.get("/network/{account_id}")
def get_network(account_id: str):
    # Construct a localized network for visualization
    # We will build nodes and edges from the transactions involving this account
    nodes = []
    edges = []
    
    # Primary node
    primary = accounts_db.get(account_id, {
        "account_id": account_id,
        "holder_name": "Unknown",
        "risk_score": 50,
        "risk_level": "Medium"
    })
    
    nodes.append({
        "id": primary["account_id"],
        "label": f"{primary['holder_name']}\n({primary['account_id']})",
        "risk_score": primary["risk_score"],
        "risk_level": primary["risk_level"],
        "is_primary": True
    })
    
    # Associated tx
    assoc_txs = [t for t in transactions_db if t["sender_id"] == account_id or t["receiver_id"] == account_id][:15]
    
    added_nodes = {account_id}
    
    for tx in assoc_txs:
        # Sender node
        if tx["sender_id"] not in added_nodes:
            s_acc = accounts_db.get(tx["sender_id"], {
                "holder_name": tx["sender_name"],
                "risk_score": tx["risk_score"] - 10,
                "risk_level": "Medium"
            })
            nodes.append({
                "id": tx["sender_id"],
                "label": f"{tx['sender_name']}\n({tx['sender_id']})",
                "risk_score": s_acc["risk_score"],
                "risk_level": s_acc.get("risk_level", "Medium"),
                "is_primary": False
            })
            added_nodes.add(tx["sender_id"])
            
        # Receiver node
        if tx["receiver_id"] not in added_nodes:
            r_acc = accounts_db.get(tx["receiver_id"], {
                "holder_name": tx["receiver_name"],
                "risk_score": tx["risk_score"] - 10,
                "risk_level": "Medium"
            })
            nodes.append({
                "id": tx["receiver_id"],
                "label": f"{tx['receiver_name']}\n({tx['receiver_id']})",
                "risk_score": r_acc["risk_score"],
                "risk_level": r_acc.get("risk_level", "Medium"),
                "is_primary": False
            })
            added_nodes.add(tx["receiver_id"])
            
        edges.append({
            "source": tx["sender_id"],
            "target": tx["receiver_id"],
            "amount": tx["amount"],
            "method": tx["payment_method"],
            "tx_id": tx["transaction_id"]
        })
        
    # Generate some network stats
    unique_senders = len(set(t["sender_id"] for t in transactions_db if t["receiver_id"] == account_id))
    unique_receivers = len(set(t["receiver_id"] for t in transactions_db if t["sender_id"] == account_id))
    total_connections = unique_senders + unique_receivers
    
    # Specific mock calculations for ACC-10293 to match specification exactly
    if account_id == "ACC-10293":
        unique_senders = 17
        unique_receivers = 8
        total_connections = 25
        rapid_transfers = 14
        high_risk_counterparties = 6
        network_risk = 96
    else:
        rapid_transfers = random.randint(1, 10)
        high_risk_counterparties = random.randint(0, 5)
        network_risk = random.randint(20, 85)
        
    return {
        "nodes": nodes,
        "edges": edges,
        "stats": {
            "unique_senders": unique_senders,
            "unique_receivers": unique_receivers,
            "total_connections": total_connections,
            "rapid_transfers": rapid_transfers,
            "high_risk_counterparties": high_risk_counterparties,
            "network_risk": network_risk
        }
    }

@app.get("/risk/{account_id}")
def get_risk_profile(account_id: str):
    # Retrieve component risks for explanation
    if account_id == "ACC-10293":
        return {
            "account_id": account_id,
            "overall_score": 94,
            "risk_level": "Critical",
            "components": {
                "Behavior Risk": 92,
                "Transaction Risk": 89,
                "Network Risk": 96,
                "Velocity Risk": 94,
                "Location Risk": 78
            },
            "history": [
                {"month": "April", "score": 41},
                {"month": "May", "score": 48},
                {"month": "June", "score": 57},
                {"month": "July", "score": 76},
                {"month": "August", "score": 94}
            ]
        }
    
    acc = accounts_db.get(account_id)
    if not acc:
        raise HTTPException(status_code=404, detail="Account not found")
        
    base = acc["risk_score"]
    history = []
    months = ["April", "May", "June", "July", "August"]
    for idx, m in enumerate(months):
        hist_score = max(5, min(99, int(base * (0.4 + (idx * 0.15) + random.uniform(-0.1, 0.1)))))
        history.append({"month": m, "score": hist_score})
        
    # Make August align with current risk score
    history[-1]["score"] = base
        
    return {
        "account_id": account_id,
        "overall_score": base,
        "risk_level": acc["risk_level"],
        "components": {
            "Behavior Risk": max(5, min(99, int(base * random.uniform(0.85, 1.15)))),
            "Transaction Risk": max(5, min(99, int(base * random.uniform(0.85, 1.15)))),
            "Network Risk": max(5, min(99, int(base * random.uniform(0.85, 1.15)))),
            "Velocity Risk": max(5, min(99, int(base * random.uniform(0.85, 1.15)))),
            "Location Risk": max(5, min(99, int(base * random.uniform(0.85, 1.15))))
        },
        "history": history
    }

@app.get("/explanation/{account_id}")
def get_explanation(account_id: str):
    if account_id == "ACC-10293":
        return {
            "account_id": account_id,
            "classification": "SUSPICIOUS",
            "probability": 94.2,
            "overall_score": 94,
            "shap_factors": [
                {"feature": "Transaction Velocity", "impact": 0.31},
                {"feature": "Unique Senders", "impact": 0.26},
                {"feature": "Rapid Fund Movement", "impact": 0.22},
                {"feature": "Network Connectivity", "impact": 0.18},
                {"feature": "Amount Deviation", "impact": 0.14},
                {"feature": "New Beneficiaries", "impact": 0.11}
            ],
            "human_explanation": "The account demonstrates a high-volume pass-through pattern. It receives funds from multiple unrelated accounts and transfers a significant portion of those funds within a short period. The account's transaction velocity and network connectivity are substantially higher than its normal behavioral profile.",
            "recommended_action": "Enhanced Due Diligence / Investigation"
        }
        
    acc = accounts_db.get(account_id)
    if not acc:
        raise HTTPException(status_code=404, detail="Account not found")
        
    score = acc["risk_score"]
    
    # Map actions
    if score >= 90:
        action = "Enhanced Due Diligence / Investigation"
        classification = "SUSPICIOUS"
    elif score >= 75:
        action = "Manual Review"
        classification = "SUSPICIOUS"
    elif score >= 40:
        action = "Enhanced Monitoring"
        classification = "FLAGGED"
    else:
        action = "Monitor"
        classification = "SAFE"
        
    prob = round(score + random.uniform(-2.0, 2.0), 1)
    prob = max(1.0, min(99.9, prob))
    
    return {
        "account_id": account_id,
        "classification": classification,
        "probability": prob,
        "overall_score": score,
        "shap_factors": [
            {"feature": "Transaction Velocity", "impact": round(random.uniform(0.05, 0.4), 2)},
            {"feature": "Unique Senders", "impact": round(random.uniform(0.05, 0.35), 2)},
            {"feature": "Amount Deviation", "impact": round(random.uniform(-0.1, 0.3), 2)},
            {"feature": "Network Density", "impact": round(random.uniform(-0.05, 0.25), 2)},
            {"feature": "Location Dispersion", "impact": round(random.uniform(-0.1, 0.2), 2)}
        ],
        "human_explanation": f"The account exhibits anomalies in its transaction frequency and counterparties. The risk profile is driven by a score of {score}/100, showing elevated patterns compared to regional benchmarks.",
        "recommended_action": action
    }

@app.get("/analytics/monthly")
def get_analytics_monthly():
    # Return comparison for July vs August fraud trends
    return {
        "august": {
            "month": "August 2026",
            "fraud_transactions": 14,
            "fraud_amount_lakhs": 8.7,
            "suspicious_accounts": 6
        },
        "july": {
            "month": "July 2026",
            "fraud_transactions": 9,
            "fraud_amount_lakhs": 4.2,
            "suspicious_accounts": 3
        },
        "changes": {
            "fraud_transactions_pct": 55.6,
            "fraud_amount_pct": 107.1,
            "suspicious_accounts_pct": 100.0
        },
        "history": [
            {"month": "March", "count": 2},
            {"month": "April", "count": 3},
            {"month": "May", "count": 5},
            {"month": "June", "count": 6},
            {"month": "July", "count": 9},
            {"month": "August", "count": 14}
        ]
    }

@app.get("/regional-risk")
def get_regional_risk():
    return regional_db

@app.get("/payment-methods")
def get_payment_methods():
    return payment_methods_db

class ReportRequest(BaseModel):
    account_id: str

@app.post("/investigation-report")
def post_investigation_report(req: ReportRequest):
    account_id = req.account_id
    acc = accounts_db.get(account_id)
    if not acc:
        raise HTTPException(status_code=404, detail="Account not found")
        
    risk_info = get_risk_profile(account_id)
    explanation = get_explanation(account_id)
    
    # Directory to save reports temporarily
    report_dir = "/Users/afsarazam/Desktop/MuleGuard/reports"
    os.makedirs(report_dir, exist_ok=True)
    pdf_filename = f"{report_dir}/Investigation_Report_{account_id}.pdf"
    
    # Generate the PDF file
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor(COLOR_DEEP_NAVY),
        spaceAfter=15,
        fontName="Helvetica-Bold"
    )
    
    section_style = ParagraphStyle(
        'SectionStyle',
        parent=styles['Heading2'],
        fontSize=13,
        textColor=colors.HexColor(COLOR_PRIMARY_BLUE),
        spaceBefore=15,
        spaceAfter=6,
        fontName="Helvetica-Bold"
    )
    
    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['BodyText'],
        fontSize=10,
        textColor=colors.HexColor(COLOR_DARK_NAVY),
        leading=14,
        fontName="Helvetica"
    )
    
    bold_body_style = ParagraphStyle(
        'BoldBodyStyle',
        parent=body_style,
        fontName="Helvetica-Bold"
    )
    
    # Header Section
    story.append(Paragraph("🛡️ MULEGUARD - FINANCIAL CRIME INTELLIGENCE REPORT", title_style))
    story.append(Paragraph(f"Generated on: {datetime.now().strftime('%d %b %Y, %H:%M:%S')} | Platform Version 1.0.0", styles['Italic']))
    story.append(Spacer(1, 10))
    
    # Account Information
    story.append(Paragraph("1. Account Demographics", section_style))
    info_data = [
        [Paragraph("Account ID:", bold_body_style), Paragraph(acc["account_id"], body_style),
         Paragraph("Holder Name:", bold_body_style), Paragraph(acc["holder_name"], body_style)],
        [Paragraph("Account Number:", bold_body_style), Paragraph(acc["account_number"], body_style),
         Paragraph("IFSC Code:", bold_body_style), Paragraph(acc["ifsc_code"], body_style)],
        [Paragraph("Region / Location:", bold_body_style), Paragraph(f"{acc['region']} / {acc['city']}", body_style),
         Paragraph("Account Age:", bold_body_style), Paragraph(f"{acc['age_months']} months", body_style)]
    ]
    t1 = Table(info_data, colWidths=[110, 150, 110, 150])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(COLOR_SOFT_GRAY)),
        ('PADDING', (0,0), (-1,-1), 6),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E4E7EC")),
    ]))
    story.append(t1)
    
    # Risk Assessment
    story.append(Paragraph("2. ML Risk Engine Scorecard", section_style))
    risk_level_color = "#D92D20" if acc["risk_level"] == "Critical" else ("#F79009" if acc["risk_level"] == "High" else "#EAAA08")
    risk_data = [
        [Paragraph("Mule Probability:", bold_body_style), Paragraph(f"{explanation['probability']}%", body_style),
         Paragraph("Overall Risk Score:", bold_body_style), Paragraph(f"{acc['risk_score']} / 100", ParagraphStyle('RStyle', parent=bold_body_style, textColor=colors.HexColor(risk_level_color)))],
        [Paragraph("Risk Classification:", bold_body_style), Paragraph(explanation["classification"], body_style),
         Paragraph("Recommended Action:", bold_body_style), Paragraph(explanation["recommended_action"], ParagraphStyle('AStyle', parent=bold_body_style, textColor=colors.HexColor(COLOR_PRIMARY_BLUE)))]
    ]
    t2 = Table(risk_data, colWidths=[110, 150, 110, 150])
    t2.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E4E7EC")),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t2)
    
    # Risk Profile Metrics
    story.append(Paragraph("3. Behavioral Indicator Risk Scores", section_style))
    comp_list = [[Paragraph("Risk Category", bold_body_style), Paragraph("Component Score (0-100)", bold_body_style)]]
    for key, val in risk_info["components"].items():
        comp_list.append([Paragraph(key, body_style), Paragraph(str(val), body_style)])
    t_comp = Table(comp_list, colWidths=[200, 200])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (1,0), colors.HexColor(COLOR_DEEP_NAVY)),
        ('TEXTCOLOR', (0,0), (1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E4E7EC")),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    # Quick fix for textcolor in table headers
    for i in range(2):
        t_comp.setStyle(TableStyle([('TEXTCOLOR', (i,0), (i,0), colors.white)]))
    story.append(t_comp)
    
    # Explainability factors (SHAP)
    story.append(Paragraph("4. Explainable AI Factors (SHAP Insights)", section_style))
    shap_list = [[Paragraph("Feature / Risk Factor", bold_body_style), Paragraph("SHAP Contribution Value", bold_body_style)]]
    for factor in explanation["shap_factors"]:
        shap_list.append([Paragraph(factor["feature"], body_style), Paragraph(f"+{factor['impact']:.2f}", body_style)])
    t_shap = Table(shap_list, colWidths=[200, 200])
    t_shap.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (1,0), colors.HexColor(COLOR_DEEP_NAVY)),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E4E7EC")),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_shap)
    
    # Account Summary Financials
    story.append(Paragraph("5. Financial Crime Activity Explanation", section_style))
    story.append(Paragraph(explanation["human_explanation"], body_style))
    story.append(Spacer(1, 10))
    
    # Recent Flagged Transactions
    story.append(Paragraph("6. Flagged High-Risk Transactions (Recent Sample)", section_style))
    tx_list = [[Paragraph("Transaction ID", bold_body_style), Paragraph("Counterparty", bold_body_style), Paragraph("Amount", bold_body_style), Paragraph("Method", bold_body_style), Paragraph("Status", bold_body_style)]]
    
    assoc_txs = [t for t in transactions_db if t["sender_id"] == account_id or t["receiver_id"] == account_id][:5]
    for tx in assoc_txs:
        counterparty = tx["receiver_name"] if tx["sender_id"] == account_id else tx["sender_name"]
        tx_list.append([
            Paragraph(tx["transaction_id"], body_style),
            Paragraph(counterparty, body_style),
            Paragraph(f"INR {tx['amount']:,}", body_style),
            Paragraph(tx["payment_method"], body_style),
            Paragraph(tx["status"], ParagraphStyle('SCol', parent=bold_body_style, textColor=colors.HexColor("#D92D20") if tx["status"] == "FLAGGED" else colors.HexColor("#039855")))
        ])
    t_tx = Table(tx_list, colWidths=[90, 130, 90, 70, 70])
    t_tx.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor(COLOR_DEEP_NAVY)),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E4E7EC")),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_tx)
    
    # Footer Notice
    story.append(Spacer(1, 20))
    story.append(Paragraph("CONFIDENTIAL NOTICE: This document contains restricted intelligence prepared by the MuleGuard Risk Core. For internal compliance and law enforcement review only. Unauthorised duplication is strictly prohibited.", ParagraphStyle('FStyle', parent=styles['Italic'], fontSize=8, textColor=colors.HexColor(COLOR_SLATE))))
    
    doc.build(story)
    
    return FileResponse(pdf_filename, filename=f"Investigation_Report_{account_id}.pdf", media_type="application/pdf")
