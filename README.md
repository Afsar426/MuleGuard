# 🛡️ MuleGuard: AI-Powered Financial Crime & Mule Account Intelligence Terminal

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![PySide6](https://img.shields.io/badge/PySide6-41CD52?style=for-the-badge&logo=qt&logoColor=white)](https://pyside.org)
[![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)](https://supabase.com)
[![LightGBM](https://img.shields.io/badge/LightGBM-Green?style=for-the-badge)](https://github.com/microsoft/LightGBM)
[![SHAP](https://img.shields.io/badge/SHAP-Interpreter-blueviolet?style=for-the-badge)](https://github.com/shap/shap)

MuleGuard is an enterprise-grade financial intelligence terminal designed to identify, analyze, and investigate mule accounts and suspicious transaction routing in real-time. By combining a PySide6 desktop UI client with a FastAPI backend server, a Supabase live database, and machine learning classifiers (LightGBM and Isolation Forest), the terminal transforms raw transaction data into explainable risk predictions.

---

## 📐 System Data Flow

The following architecture diagram represents the lifecycle of a transaction within MuleGuard:

```mermaid
flowchart TD
    subgraph Client [Desktop UI Client (PySide6)]
        UI[Investigation Console / Tabs]
        WS_Client[WebSocket Thread]
    end

    subgraph Backend [FastAPI Application Server]
        API[REST Endpoints]
        Pipe[Feature Pipeline]
        LGB[LightGBM Classifier]
        IF[Isolation Forest]
        SHAP[SHAP Interpreter]
        WS_Mgr[WebSocket Connection Manager]
    end

    subgraph DB [Live Cloud Database]
        Supa[(Supabase Tables)]
    end

    %% REST Operations
    UI -->|1. Submit Transaction / Trigger Inference| API
    API -->|2. Query Historical Logs| Supa
    Supa -->|3. Return History| API
    
    %% Inference Pipeline
    API -->|4. Build Vector Matrix| Pipe
    Pipe -->|5. Predict Risk Probability| LGB
    Pipe -->|6. Calculate Outlier Anomaly| IF
    LGB -->|7. Generate Local SHAP Values| SHAP
    
    %% Storage & Update
    API -->|8. Record Predictions / Update Account Scores| Supa
    API -->|9. Trigger Broadcast| WS_Mgr
    
    %% Real-time Stream
    WS_Mgr -->|10. Push Live JSON Payload| WS_Client
    WS_Client -->|11. Refresh Dashboards & Visual Widgets| UI
```

---

## 🧠 Machine Learning & Feature Engineering

MuleGuard does not rely on simple static rules. Instead, it uses a dynamic feature extraction pipeline to feed machine learning models:

### 1. Feature Engineering (`FeaturePipeline`)
The pipeline constructs high-dimensional features from a transaction and its historical context:
- **Velocity Risk (`seconds_since_previous`)**: Tracks timing frequency between sequential transfers to identify automated scripting or rapid cash-out behaviors.
- **Fan-Out Risk (`sender_unique_receivers`, `sender_unique_banks`)**: Measures how many distinct accounts or banks are receiving funds from a single source within a tight temporal window.
- **Fan-In Risk (`receiver_unique_senders`, `receiver_unique_banks`)**: Measures consolidation patterns, such as multiple distinct source accounts depositing funds into a single accumulator account.
- **Amount Deviation (`amount_diff`, `amount_ratio`)**: Computes the credit-to-debit ratio and deviation from the account holder's typical transaction amounts.
- **Transaction Context**: Evaluates bank codes (`from_bank`, `to_bank`), payment currency, transaction hour, and weekday patterns.

### 2. Risk Classification Model (`LightGBM`)
- A trained LightGBM model calculates the risk probability of a mule transaction.
- Risk probabilities are classified into standard compliance tiers:
  - **Critical** (Risk Score $\ge$ 90) $\rightarrow$ Flags account status as **Under Investigation**.
  - **High** (Risk Score $\ge$ 75) $\rightarrow$ Triggers an **Open Alert**.
  - **Medium** (Risk Score $\ge$ 40) $\rightarrow$ Restructures account status to **Monitored**.
  - **Low / Safe** (Risk Score $<$ 40) $\rightarrow$ Flags account as **Active / Normal**.

### 3. Anomaly Detection Model (`Isolation Forest`)
- An Isolation Forest model identifies multivariate outliers.
- By calculating decision path lengths in isolation trees, it isolates anomalous transactions that deviate from overall baseline historical behaviors.

### 4. Explainable AI (`SHAP`)
- Calculates local SHapley Additive exPlanations.
- The top 6 feature impacts are mapped to natural-language human explanations (e.g., explaining that the risk score is driven by *Transaction Velocity* and *Unique Senders*), allowing compliance officers to review the reasoning behind the alert.

---

## 🖥️ Desktop UI Views & Simulation Controls

The client GUI (PySide6) contains structured tabs tailored to specific investigation stages:
- **Dashboard**: High-level telemetry displaying active alerts, total tracked volumes, and real-time activity trends.
- **Active Alerts Queue**: Real-time log of flagged incidents with quick-access investigation triggers.
- **Live Transactions**: A waterfall feed showing incoming transactions with risk indicators.
- **Accounts & Transactions**: Database tabular search grids with filters.
- **Network Analysis**: Generates interactive graph layouts using NetworkX to map payment paths between counterparties.
- **Fraud Analytics**: Matplotlib line/bar/donut charts displaying month-over-month (MoM) fraud rates and categorization.
- **Regional Risk**: Geospatial risk distributions across tracking territories.
- **Payment Methods**: Donut charts, ticket volume bars, risk gauges, and detailed insights grids equipped with custom vector sparklines.

### ⚙️ Presentation Simulation Engines
For demonstration purposes, the **Fraud Analytics** and **Payment Methods** views include a `⚙️ Configure Simulation Data` tool. Analysts can override data slices, risk levels, and monthly distributions on the fly, immediately recalculating averages, percentages, and redrawing all Matplotlib figures and sparklines without backend delay.

---

## 🗂️ Project Structure Map

| File / Directory | Target Responsibility |
| :--- | :--- |
| `backend/main.py` | FastAPI application, REST endpoints, WebSocket manager, PDF generator. |
| `backend/database.py` | Handles database connections, queries, predictions, updates, and fetches. |
| `backend/feature_pipeline.py` | Feature extraction, vector matrix builder, and transformation logic. |
| `frontend/app.py` | Primary PySide6 client codebase, widgets, Matplotlib canvas, and navigation. |
| `models/` | Serialized model pickles (`muleguard_lightgbm.pkl`, `muleguard_isolation_forest.pkl`). |
| `dist/` | Standalone packaged executable binaries for local execution. |

---

## 📦 Standalone Binaries & Reassembly

To accommodate file size limitations on GitHub, the compiled executables in the `dist/` directory are packaged into **50 MB split zip parts**.

### 📁 Binary Files Location
- **Backend Service Daemon**: `dist/main_split.zip`, `dist/main_split.z01`, `dist/main_split.z02`
- **Desktop Client Application**: `dist/app_split.zip`, `dist/app_split.z01`, `dist/app_split.z02`, `dist/app_split.z03`, etc.

### 📥 Reassembling the split files:

#### macOS / Linux
Open your terminal in the directory where the split files are saved and run:
```bash
# Reassemble and unzip the backend daemon
zip -F dist/main_split.zip --out main.zip
unzip main.zip

# Reassemble and unzip the PySide6 UI client
zip -F dist/app_split.zip --out app.zip
unzip app.zip
```
*(On macOS, you can also double-click `main_split.zip` or `app_split.zip` in Finder. Archive Utility will automatically locate the split parts and extract the executables).*

#### Windows
Open `main_split.zip` or `app_split.zip` in archiving applications like **7-Zip**, **WinRAR**, or **WinZip** to extract the files natively.

---

## 🌐 Connecting to your Render Backend

The client executable resolves its API endpoint dynamically. You can route transactions and risk queries to your hosted Render environment (`https://muleguard-i6ol.onrender.com`) using either of the following options:

### Method 1: Using `config.json` (Recommended)
Place a file named `config.json` next to your client executable with your Render domain:
```json
{
  "api_url": "https://muleguard-i6ol.onrender.com"
}
```

### Method 2: Via Environment Variables
Define the variable in your shell session before starting the application:

- **macOS / Linux**:
  ```bash
  export MULEGUARD_API_URL="https://muleguard-i6ol.onrender.com"
  ./dist/app
  ```
- **Windows (Command Prompt)**:
  ```cmd
  set MULEGUARD_API_URL=https://muleguard-i6ol.onrender.com
  dist\app.exe
  ```

> [!IMPORTANT]
> **Render Cold-Start Performance**: Render's free tier suspends inactive containers after 15 minutes. 
> The initial request will trigger a cold start taking **40-50 seconds**. 
> To wake the server before opening the application, visit **[https://muleguard-i6ol.onrender.com/health](https://muleguard-i6ol.onrender.com/health)** in your web browser.

---

## 🚀 Launching from Source Code

### 🍎 Running on macOS
1. Activate virtual environment:
   ```bash
   source venv/bin/activate
   ```
2. Start the FastAPI backend:
   ```bash
   uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
   ```
3. In a new terminal, launch the desktop app:
   ```bash
   python frontend/app.py
   ```

### 🪟 Running on Windows
1. Activate virtual environment:
   ```cmd
   venv\Scripts\activate.bat
   ```
2. Start the FastAPI backend:
   ```cmd
   uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
   ```
3. In a new terminal, launch the desktop app:
   ```cmd
   python frontend/app.py
   ```
