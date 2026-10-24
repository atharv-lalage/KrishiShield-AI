# Development Workflow & Operations

This document covers setup, local execution, testing, and development workflows for KrishiShield AI.

---

## 1. Local Environment Setup

### 1.1 Prerequisites
- **Python**: Version 3.9+ (Python 3.9 or 3.10 recommended)
- **Node.js**: Version 18+ (Node 20+ recommended)
- **Package Managers**: `pip` and `npm`

---

## 2. Backend Development

### 2.1 Virtual Environment Setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2.2 Environment Configuration
Create a `.env` file in `backend/` by copying the template:
```bash
cp .env.example .env
```
Fill in your credentials (Twilio SMS/WhatsApp numbers and API keys).

### 2.3 Running the FastAPI Development Server
```bash
uvicorn main:app --reload --port 8000
```
- Interactive API Documentation (Swagger UI): [http://localhost:8000/docs](http://localhost:8000/docs)
- Alternative Documentation (ReDoc): [http://localhost:8000/redoc](http://localhost:8000/redoc)

### 2.4 Running the Companion Streamlit App
```bash
streamlit run app.py
```

### 2.5 Running Backend Tests
Execute the comprehensive test suite:
```bash
python -m unittest discover -s tests
```

---

## 3. Frontend Development

### 3.1 Install Dependencies
```bash
cd frontend
npm install
```

### 3.2 Run Vite Development Server
```bash
npm run dev
```
Access the application at [http://localhost:5173](http://localhost:5173).

### 3.3 Code Quality & Linting
```bash
npm run lint
```

### 3.4 Production Build & Preview
```bash
npm run build
npm run preview
```

---

## 4. Data Preparation & ML Pipelines

To re-aggregate raw mandi prices and regenerate weekly lagged features:
```bash
cd backend
python scripts/data_preparation.py
```
This reads from `backend/data/raw/semifinal.csv` and outputs engineered features into `backend/data/processed/`.

To test live mandi price extraction from data.gov.in:
```bash
cd backend
python scripts/fetch_mandi_prices.py
```

---

## 5. Docker Deployment

To build and run the production backend container:
```bash
cd backend
docker build -t krishishield-backend .
docker run -p 8000:8000 --env-file .env krishishield-backend
```

---

## 6. Coding Standards & Conventions

1. **Backend**:
   - Follow PEP 8 style guidelines.
   - All API endpoints must use Pydantic models for request validation and response typing.
   - File paths must use `src.core.config` path objects rather than hardcoded string paths.
   - Business logic belongs in `src/services/`, not inside API route handlers.

2. **Frontend**:
   - Keep components focused and single-purpose.
   - State that persists offline must use `src/services/db.js`.
   - All network calls must pass through `src/services/api.js`.
   - Internationalized strings must be registered in `src/i18n/locales/en.json` and `mr.json`.
