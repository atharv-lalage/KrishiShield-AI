import json
from apscheduler.schedulers.background import BackgroundScheduler
from src.core.config import RISK_CACHE_FILE
from src.core.constants import MONITOR_CHECK_LIST
from src.ml.model_loader import load_model_and_scaler
from src.ml.feature_engineering import prepare_input_vector
from src.services.weather_service import fetch_extended_weather
from src.services.agmarknet_service import fetch_agmarknet_data
from src.services.notification_service import send_notification
from src.services.alert_service import save_alert


def monitor_risks(market_coords: dict):
    """
    Scheduled Job: Checks for SUDDEN price jumps across key crop/market pairs.
    Executes prediction using Agmarknet baseline + Open-Meteo weather features.
    Dispatches alerts via Twilio and saves to persistent alert storage if change > 10%.
    """
    print("--- [SCHEDULER] Running Risk Monitor (24h Check) ---")

    cache = {}
    if RISK_CACHE_FILE.exists():
        try:
            with open(RISK_CACHE_FILE, "r") as f:
                cache = json.load(f)
        except Exception:
            cache = {}

    updated_cache = cache.copy()

    for crop, market in MONITOR_CHECK_LIST:
        if market not in market_coords:
            continue

        lat = market_coords[market]["latitude_x"]
        lon = market_coords[market]["longitude_x"]

        # 1. Load Model
        model, scaler = load_model_and_scaler(crop)
        if not model:
            continue

        # 2. Fetch Data
        weather, _ = fetch_extended_weather(lat, lon)
        if weather.empty:
            continue

        price_stats = fetch_agmarknet_data(crop, market)
        if not price_stats:
            price_stats = {"Modal_Price": 2500.0}

        baseline = price_stats.get("Modal_Price", 2500)

        try:
            # 3. Predict using feature vector
            input_data = prepare_input_vector(model, weather, price_stats)

            if scaler:
                pred_raw = float(model.predict(scaler.transform(input_data))[0])
            else:
                pred_raw = float(model.predict(input_data)[0])

            # 4. Apply Logic (Diff for Onion vs Direct for others)
            if "onion" in crop.lower():
                pred = baseline + pred_raw
            else:
                pred = pred_raw

            cache_key = f"{crop}_{market}"
            last_price = cache.get(cache_key, baseline)

            if last_price == 0:
                last_price = baseline

            pct_change = ((pred - last_price) / last_price) * 100

            # 5. Alert Trigger (>10% Change)
            if abs(pct_change) > 10:
                print(f"!!! ALERT TRIGGERED: {crop} in {market} changed by {pct_change:.1f}%")

                msg_text = (
                    f"KrishiShield Alert: {crop} in {market} is projected to move from "
                    f"₹{int(last_price)} to ₹{int(pred)} (Change: {pct_change:.1f}%)."
                )

                # Send Notification
                sms_status = send_notification(msg_text)

                alert_obj = {
                    "type": "Critical" if abs(pct_change) > 20 else "Warning",
                    "crop": crop,
                    "market": market,
                    "message": msg_text,
                    "change_pct": round(pct_change, 1),
                    "is_sms_sent": sms_status,
                }
                save_alert(alert_obj)

            updated_cache[cache_key] = pred
        except Exception as e:
            print(f"Monitor Error for {crop}: {e}")

    try:
        with open(RISK_CACHE_FILE, "w") as f:
            json.dump(updated_cache, f, indent=2)
    except Exception as e:
        print(f"Error saving risk cache: {e}")


def init_scheduler(market_coords: dict):
    """Initializes and starts the APScheduler background daemon."""
    try:
        scheduler = BackgroundScheduler()
        scheduler.add_job(
            monitor_risks,
            "interval",
            hours=24,
            args=[market_coords],
            id="daily_risk_monitor",
            replace_existing=True,
        )
        scheduler.start()
        print("[SCHEDULER] BackgroundScheduler started successfully (interval: 24h).")
        return scheduler
    except Exception as e:
        print(f"[SCHEDULER] Scheduler Failed to start: {e}")
        return None
