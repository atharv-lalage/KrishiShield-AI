# KrishiShield AI 🌾

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React 19](https://img.shields.io/badge/React-19.2-61DAFB?logo=react&logoColor=black)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite-7.3-646CFF?logo=vite&logoColor=white)](https://vitejs.dev/)
[![XGBoost](https://img.shields.io/badge/XGBoost-ML-EB5424?logo=xgboost&logoColor=white)](https://xgboost.readthedocs.io/)
[![Twilio](https://img.shields.io/badge/Twilio-Alerts-F22F46?logo=twilio&logoColor=white)](https://www.twilio.com/)
[![License](https://img.shields.io/badge/License-Academic%20Demo-blue)](#license)

**KrishiShield AI** is an intelligent agricultural advisory and market price prediction platform engineered to safeguard farmers from sudden market price collapses and climate shocks. By synthesizing multi-parameter weather forecasts (Open-Meteo), official mandi price series (Agmarknet), and trained Machine Learning models (XGBoost), KrishiShield predicts 7-day crop price directions and provides timely agronomic advisories.

---

## Key Features

- **🌾 AI-Powered Crop Risk Analytics**: Predicts market price volatility and evaluates calibrated risk scores ($0-100\%$) for major commodities (Onion, Wheat, Potato, Tomato, Rice).
- **📈 7-Day Forward Horizon Forecasting**: Combines historical mandi trends with forecasted meteorological conditions.
- **🚨 Automated Multi-Channel Alerting**: Built-in background daemon (`APScheduler`) checks sentinel markets every 24 hours and dispatches Twilio SMS and WhatsApp alerts on price shocks ($>10\%$).
- **⚡ Resilient Offline Capability**: Full client-side caching powered by **IndexedDB** ensures farmers in rural locations can access previously inspected market data even when disconnected.
- **🌐 Dual-Language Localization**: Full native UI support for **English** and **Marathi (मराठी)** with instant language toggling.
- **📊 Interactive Visualizations**: Responsive price trend curves (Recharts) and detailed 7-day meteorological impact tables.

---

## Documentation Quick Links

For in-depth architectural and operational guides, refer to:
- 📂 [**PROJECT_STRUCTURE.md**](file:///Users/adityalalage/Desktop/KrishiShield-AI-main/PROJECT_STRUCTURE.md) – Directory structure and organization.
- 🏛️ [**ARCHITECTURE.md**](file:///Users/adityalalage/Desktop/KrishiShield-AI-main/ARCHITECTURE.md) – High-level system architecture, data flows, and design patterns.
- 🛠️ [**TECH_STACK.md**](file:///Users/adityalalage/Desktop/KrishiShield-AI-main/TECH_STACK.md) – Catalog of technologies, libraries, and external APIs.
- 💻 [**DEVELOPMENT.md**](file:///Users/adityalalage/Desktop/KrishiShield-AI-main/DEVELOPMENT.md) – Development workflows, tests, scripts, and commands.

---

## Quick Start

### 1. Prerequisites
- **Python 3.9+**
- **Node.js 18+** & npm

---

### 2. Backend Setup (FastAPI)

```bash
cd backend

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env

# Run FastAPI backend
uvicorn main:app --reload --port 8000
```
- API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

*(Optional) Run Streamlit Dashboard:*
```bash
streamlit run app.py
```

---

### 3. Frontend Setup (React + Vite)

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```
- Frontend UI: [http://localhost:5173](http://localhost:5173)

---

### 4. Running Backend Tests

```bash
cd backend
python -m unittest discover -s tests
```

---

## Docker Deployment

To run the backend in a containerized environment:

```bash
cd backend
docker build -t krishishield-backend .
docker run -p 8000:8000 --env-file .env krishishield-backend
```

---

## Core Development Team

Developed with ❤️ by:
- **Atharv Lalage**
- **Vivek More**
- **Swayam Korde**

---

## License

This project is licensed for academic, research, and hackathon evaluation purposes.
