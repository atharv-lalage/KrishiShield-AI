import math
from datetime import date, timedelta
import numpy as np
import pandas as pd
from fastapi import APIRouter, HTTPException

from src.api.schemas import AnalysisRequest
from src.core.data_loader import load_market_data
from src.ml.model_loader import load_model_and_scaler
from src.ml.feature_engineering import prepare_input_vector
from src.services.weather_service import fetch_extended_weather
from src.services.agmarknet_service import fetch_agmarknet_data
from src.services.alert_service import load_alerts
from src.services.risk_service import (
    generate_price_trend,
    evaluate_risk_profile,
)

router = APIRouter()

# Load dataset and coordinates on module load
DF_BASE, MARKET_COORDS = load_market_data()


@router.get("/alerts")
def get_alerts():
    """Returns stored risk and price fluctuation alert history."""
    return load_alerts()


@router.get("/markets/{crop}")
def get_markets(crop: str):
    """Returns alphabetically sorted list of markets available for a given crop."""
    if DF_BASE.empty:
        return {"markets": []}

    if "Commodity" in DF_BASE.columns:
        markets = sorted(
            DF_BASE[DF_BASE["Commodity"] == crop]["Market Name"].unique().tolist()
        )
    else:
        markets = sorted(DF_BASE["Market Name"].unique().tolist())

    return {"markets": markets}


@router.post("/analyze")
def analyze_risk(req: AnalysisRequest):
    """
    Performs AI-powered multi-modal risk and price prediction for a given crop & market.
    Integrates live Agmarknet prices, Open-Meteo forecasts, and XGBoost regressor models.
    """
    if req.market not in MARKET_COORDS:
        raise HTTPException(status_code=404, detail="Market coordinates not found.")

    lat = MARKET_COORDS[req.market]["latitude_x"]
    lon = MARKET_COORDS[req.market]["longitude_x"]

    # 1. Load model and optional scaler
    model, scaler = load_model_and_scaler(req.crop)
    if not model:
        raise HTTPException(
            status_code=500, detail=f"Model for {req.crop} not found."
        )

    weather_df, source = fetch_extended_weather(lat, lon)

    # 2. Fetch Real Agmarknet Market Data
    price_stats = fetch_agmarknet_data(req.crop, req.market)
    if not price_stats:
        print("Agmarknet failed/empty. Falling back to default.")
        price_stats = {"Modal_Price": 2500.0}

    baseline_price = price_stats.get("Modal_Price", 2500)

    if weather_df.empty:
        raise HTTPException(
            status_code=503, detail="Weather data fetch failed."
        )

    try:
        # 3. Prepare Vector
        input_data = prepare_input_vector(model, weather_df, price_stats)

        # 4. Predict (Handle Scaler existence)
        if scaler:
            input_scaled = scaler.transform(input_data)
            prediction = float(model.predict(input_scaled)[0])
        else:
            prediction = float(model.predict(input_data)[0])

        # 5. Final Price Logic (Diff for Onion vs Direct Price for others)
        if "onion" in req.crop.strip().lower():
            predicted_price = baseline_price + prediction
        else:
            predicted_price = prediction

        if math.isnan(predicted_price) or math.isinf(predicted_price):
            predicted_price = float(baseline_price)

        # Percentage Change
        pct_change = ((predicted_price - baseline_price) / baseline_price) * 100

        # 6. Evaluate Risk Score, Level, and Advisory
        risk_score, risk_level, msg, advisory = evaluate_risk_profile(pct_change)

        # 7. Timeline data (Next 7 days forecast)
        timeline_data = []
        if not weather_df.empty:
            today = pd.Timestamp(date.today())
            start_date = today
            end_date = today + timedelta(days=6)
            mask = (weather_df.index >= start_date) & (weather_df.index <= end_date)
            timeline_slice = weather_df.loc[mask]
            timeline_data = (
                timeline_slice.reset_index()
                .replace({np.nan: None})
                .to_dict("records")
            )

        # 8. Historical + Forecast Price Trend
        price_trend = generate_price_trend(baseline_price, predicted_price)
        target_date = (date.today() + timedelta(days=7)).strftime("%b %d")

        return {
            "projected_price": int(predicted_price),
            "baseline_price": int(baseline_price),
            "target_date": target_date,
            "historical_norm": int(baseline_price),
            "risk_level": risk_level,
            "risk_score": int(risk_score),
            "price_change": round(pct_change, 2),
            "weather_source": source,
            "message": msg,
            "advisory": advisory,
            "timeline": timeline_data,
            "price_trend": price_trend,
        }

    except HTTPException:
        raise
    except Exception as e:
        import traceback

        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Prediction Error: {str(e)}")
