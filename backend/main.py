import sys
from pathlib import Path
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

# Ensure backend directory is on sys.path for direct script execution
backend_dir = Path(__file__).resolve().parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from src.core.config import CORS_ORIGINS
from src.api.routes import router as api_router, MARKET_COORDS
from src.scheduler.risk_monitor import init_scheduler

app = FastAPI(
    title="KrishiShield AI - Backend API",
    description="Multi-modal agricultural risk advisory and market price prediction engine",
    version="1.0.0",
)

# --- 1. CORS CONFIGURATION ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 2. REGISTER API ROUTES ---
app.include_router(api_router)


# --- 3. LIFECYCLE HOOKS ---
@app.on_event("startup")
def on_startup():
    print("Starting KrishiShield AI FastAPI server...")
    # Initialize background risk monitoring job
    init_scheduler(MARKET_COORDS)


@app.get("/")
def root():
    return {
        "status": "online",
        "service": "KrishiShield AI",
        "version": "1.0.0",
        "docs": "/docs",
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)