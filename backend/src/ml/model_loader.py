import os
import pickle
import xgboost as xgb
from src.core.config import MODEL_DIR


def load_model_and_scaler(crop: str):
    """
    Loads trained machine learning model and optional scaler for a given crop.
    
    1. Checks for specific 'onion_xgboost_model_diff.json' first.
    2. Handles standard crops via pickle files.
    3. Handles cases where scaler is None gracefully.
    """
    try:
        crop_clean = crop.strip()
        crop_lower = crop_clean.lower()
        
        # 1. Special handling for Onion JSON Diff Model
        onion_json_path = MODEL_DIR / "onion_xgboost_model_diff.json"
        if "onion" in crop_lower and onion_json_path.exists():
            model = xgb.XGBRegressor()
            model.load_model(str(onion_json_path))
            return model, None

        # 2. Standard handling for other crops (Pickle)
        model_path = MODEL_DIR / f"{crop_clean}.pkl"
        if not model_path.exists():
            # Try case variations (e.g., Potato.pkl or potato.pkl)
            alt_path = MODEL_DIR / f"{crop_clean.capitalize()}.pkl"
            if alt_path.exists():
                model_path = alt_path

        if model_path.exists():
            with open(model_path, "rb") as f:
                model = pickle.load(f)

            # Optional scaler
            scaler_path = MODEL_DIR / f"{crop_lower}_scaler.pkl"
            scaler = None
            if scaler_path.exists():
                with open(scaler_path, "rb") as f:
                    scaler = pickle.load(f)

            return model, scaler

        print(f"Model file for {crop_clean} not found at {model_path}.")
        return None, None

    except Exception as e:
        print(f"Error loading model for {crop}: {e}")
        return None, None
