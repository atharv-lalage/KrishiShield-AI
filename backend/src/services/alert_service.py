import json
from datetime import datetime
from src.core.config import ALERTS_FILE


def load_alerts() -> list:
    """Loads recorded alerts from persistent JSON storage."""
    if ALERTS_FILE.exists():
        try:
            with open(ALERTS_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error reading alerts file: {e}")
            return []
    return []


def save_alert(new_alert: dict) -> dict:
    """
    Appends a new alert to the alert history with an incremented ID and timestamp.
    Returns the created alert object.
    """
    alerts = load_alerts()
    new_alert["id"] = len(alerts) + 1
    new_alert["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    alerts.insert(0, new_alert)
    try:
        with open(ALERTS_FILE, "w") as f:
            json.dump(alerts, f, indent=2)
    except Exception as e:
        print(f"Error writing to alerts file: {e}")
    return new_alert
