# KrishiShield AI - Backend Service

High-performance Python backend powered by **FastAPI** for real-time predictions and **APScheduler** for automated risk alerting, with companion **Streamlit** dashboard support.

## Architecture Highlights

- **`src/core/`**: Central configuration, dynamic directory resolution, constants, and data loading.
- **`src/api/`**: Pydantic validation schemas and FastAPI REST endpoints (`/alerts`, `/markets/{crop}`, `/analyze`).
- **`src/services/`**: Modular integrations for Open-Meteo Weather API, Agmarknet Mandi API, Twilio SMS/WhatsApp, and Risk Calculation.
- **`src/ml/`**: Machine learning model loaders (XGBoost JSON diff & Pickle models) and feature vector engineering.
- **`src/scheduler/`**: Automated 24-hour crop price monitoring daemon.
- **`models/`**: Serialized ML artifacts and scalers.
- **`data/`**: Structured raw datasets (`data/raw`), lagged features (`data/processed`), and dynamic caches (`data/storage`).
- **`scripts/`**: Data preprocessing pipelines and API fetchers.
- **`tests/`**: Unit and integration test suite.

## Running the Backend

### 1. Development (FastAPI)
```bash
uvicorn main:app --reload --port 8000
```

### 2. Streamlit Dashboard
```bash
streamlit run app.py
```

### 3. Running Tests
```bash
python -m unittest discover -s tests
```

### 4. Docker Container
```bash
docker build -t krishishield-backend .
docker run -p 8000:8000 krishishield-backend
```
