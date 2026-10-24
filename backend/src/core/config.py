import os
from pathlib import Path
from dotenv import load_dotenv

# Base backend directory: /path/to/backend
BACKEND_DIR = Path(__file__).resolve().parent.parent.parent

# Load .env file from backend root or system
ENV_FILE = BACKEND_DIR / ".env"
if ENV_FILE.exists():
    load_dotenv(ENV_FILE)
else:
    load_dotenv()

# --- DIRECTORY STRUCTURE ---
DATA_DIR = BACKEND_DIR / "data"
DATA_RAW_DIR = DATA_DIR / "raw"
DATA_PROCESSED_DIR = DATA_DIR / "processed"
DATA_STORAGE_DIR = DATA_DIR / "storage"
MODEL_DIR = BACKEND_DIR / "models"

# Ensure runtime directories exist
DATA_STORAGE_DIR.mkdir(parents=True, exist_ok=True)

# --- FILE PATHS ---
PRIMARY_DATA_FILE = DATA_RAW_DIR / "semifinal.csv"
FALLBACK_DATA_FILE = DATA_RAW_DIR / "test.csv"
ALERTS_FILE = DATA_STORAGE_DIR / "alert_history.json"
RISK_CACHE_FILE = DATA_STORAGE_DIR / "risk_state_cache.json"
WEATHER_CACHE_FILE = DATA_STORAGE_DIR / "offline_weather_cache.csv"

# --- FUEL PRICE CONSTANTS ---
CURRENT_PETROL = 106.31
CURRENT_DIESEL = 94.27

# --- EXTERNAL API CONFIGURATION ---
AGMARKNET_API_KEY = os.getenv("AGMARKNET_API_KEY", "579b464db66ec23bdd00000125b231d6079f44e54c664acfce4c26dc")
AGMARKNET_RESOURCE_ID = os.getenv("AGMARKNET_RESOURCE_ID", "35985678-0d79-46b4-9ed6-6f13308a1d24")

# --- TWILIO CREDENTIALS ---
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_SMS_NUMBER = os.getenv("TWILIO_SMS_NUMBER")
TWILIO_WA_NUMBER = os.getenv("TWILIO_WA_NUMBER")
FARMER_PHONE_NUMBER = os.getenv("FARMER_PHONE_NUMBER")

# --- CORS SETTINGS ---
CORS_ORIGINS = ["*"]
