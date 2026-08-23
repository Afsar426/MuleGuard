# 🛡️ MuleGuard

## Financial Crime Intelligence & Mule Account Detection System

> **Detect suspicious mule accounts. Understand their behavior. Trace their transaction networks. Explain the AI decision. Help investigators act faster.**

MuleGuard is an AI-assisted financial crime intelligence platform designed to detect suspicious transactions and mule-account behavior using machine learning, behavioral analytics, transaction velocity, network intelligence, and explainable AI.

---

## 📥 Download Standalone Executables
You can download the pre-compiled macOS standalone executables directly from the GitHub Releases page:
👉 **[MuleGuard v1.0.0 Release](https://github.com/Raghav0079/MuleGuard/releases/tag/v1.0.0)**
- **`main.zip`**: The FastAPI backend daemon service.
- **`app.zip`**: The PySide6 desktop UI client application bundle.

Alternatively, you can get them directly from the repository's `dist/` directory, split into 50MB chunks to bypass GitHub size limits:
- **Reassemble and unzip Backend (macOS/Linux)**:
  ```bash
  zip -F dist/main_split.zip --out main.zip
  unzip main.zip
  ```
- **Reassemble and unzip Desktop Client (macOS/Linux)**:
  ```bash
  zip -F dist/app_split.zip --out app.zip
  unzip app.zip
  ```
- **On Windows**: Open `main_split.zip` / `app_split.zip` in WinRAR, 7-Zip, or WinZip and extract it natively (it will automatically detect the `.z01`, `.z02` parts).

---

## 🛠️ Technology Stack & Architecture

- **Desktop UI (Frontend)**: Native PySide6 (Qt for Python) terminal with high-fidelity visualization cards, custom sparklines, Matplotlib chart views, and a collapsible sidebar.
- **REST & WebSockets API (Backend)**: FastAPI server with asynchronous execution pipelines and WebSocket broadcasters.
- **Database Layer**: Live cloud storage integration powered by Supabase.
- **AI Models**: LightGBM Classifier (mule risk probability) and Isolation Forest (anomaly detection).
- **Explainable AI (XAI)**: SHAP (SHapley Additive exPlanations) interpreter tracking feature contributions.

---

## 📦 Standalone Packaging & Executables

MuleGuard supports local offline sandbox execution as well as production connectivity using compiled binaries:

1. **Backend Executable** (`dist/main`):
   - Fast-compiled standalone binary running the FastAPI web server.
2. **Desktop UI Client** (`dist/app` / `dist/app.app`):
   - Standalone application bundle packaged for windowed macOS execution.
3. **Clean Repo Hygiene**:
   - PyInstaller spec descriptors (`*.spec`) and compilation folders (`build/`, `dist/`) are excluded from repository tracking to maintain clean version control hygiene.

---

## 🌐 Connecting to the Render Backend

The client executable determines your API gateway URL dynamically. You can route transactions and risk queries to your hosted Render environment using either of the following methods:

### Method 1: Using `config.json` (Recommended & Easiest)
Create a file named `config.json` in the same directory as the compiled executable with your Render backend URL:
```json
{
  "api_url": "https://muleguard-i6ol.onrender.com"
}
```
Whenever the app starts, it reads this configuration and dynamically hooks into the Render server.

### Method 2: Via Environment Variables
Set the target URL in your terminal before launching the executable:

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
> **Render Cold Start Notice**: Render's free tier automatically suspends containers after 15 minutes of inactivity. 
> If the backend is asleep, the first request will trigger a cold boot taking **40-50 seconds**. 
> Before launching the app, open **[https://muleguard-i6ol.onrender.com/health](https://muleguard-i6ol.onrender.com/health)** in your browser and wait for it to load to wake up the server!

---

## 🚀 Execution & Startup Commands

### 🍎 Running on macOS

#### Run from Source:
1. Activate the Python virtual environment:
   ```bash
   source venv/bin/activate
   ```
2. Launch the backend API server:
   ```bash
   uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
   ```
3. Launch the desktop client application:
   ```bash
   python frontend/app.py
   ```

#### Run compiled binaries:
- Start the backend daemon:
  ```bash
  ./dist/main
  ```
- Start the windowed UI client:
  ```bash
  ./dist/app
  ```

---

### 🪟 Running on Windows

#### Run from Source:
1. Activate the Python virtual environment:
   ```cmd
   venv\Scripts\activate.bat
   ```
2. Launch the backend API server:
   ```cmd
   uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
   ```
3. Launch the desktop client application:
   ```cmd
   python frontend/app.py
   ```

#### Run compiled binaries (if built on Windows):
- Start the backend daemon:
  ```cmd
  dist\main.exe
  ```
- Start the windowed UI client:
  ```cmd
  dist\app.exe
  ```

---

## ⚙️ Presentation Simulation Engines
MuleGuard includes presenting modes for demonstrations. In the **Fraud Analytics** and **Payment Methods** views, you can click the `⚙️ Configure Simulation Data` buttons. 
This displays a tabbed parameter panel where you can override transaction flows, risk metrics, and chart statistics in real-time, redrawing Matplotlib figures instantly.
