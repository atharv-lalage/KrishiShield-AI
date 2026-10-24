import math
import random
from datetime import date, timedelta


def generate_price_trend(baseline: float, projected: float) -> list:
    """
    Generates historical and projected price trend points across [-30, -21, -14, -7, 0, +7] day offsets.
    """
    trend = []
    today = date.today()
    offsets = [-30, -21, -14, -7, 0, 7]

    if math.isnan(projected) or math.isinf(projected):
        projected = baseline

    for days in offsets:
        dt = today + timedelta(days=days)
        date_str = dt.strftime("%b %d")
        if days < 0:
            variation = random.uniform(-50, 50)
            price = int(baseline + variation)
        elif days == 0:
            price = int(baseline)
        else:
            price = int(projected)
        trend.append({"date": date_str, "price": price})
    return trend


def evaluate_risk_profile(pct_change: float) -> tuple:
    """
    Evaluates risk score, level, summary message, and actionable advisory
    based on the projected percentage price change.
    """
    if pct_change > 0:
        # RISING PRICES (+)
        risk_score = min(pct_change * 2.5, 100)

        if risk_score > 60:
            risk_level = "HIGH RISK"
            msg = f"Price surge of {pct_change:.1f}% predicted! Crop shortage likely."
            adv_color = "error"
            adv_title = "Critical Supply Alert"
            adv_steps = ["Secure stock immediately", "Check for pest outbreaks"]
        elif risk_score > 20:
            risk_level = "MODERATE RISK"
            msg = f"Price rising by {pct_change:.1f}%. Moderate stress."
            adv_color = "warning"
            adv_title = "Inflationary Trend"
            adv_steps = ["Monitor daily rates", "Prepare for volatility"]
        else:
            risk_level = "LOW RISK"
            msg = "Slight price increase. Stable market."
            adv_color = "success"
            adv_title = "Stable Conditions"
            adv_steps = ["Standard operations"]
    else:
        # DROPPING PRICES (-)
        risk_score = 10
        risk_level = "LOW RISK"
        msg = f"Price dropping by {abs(pct_change):.1f}%. Good supply expected."
        adv_color = "success"
        adv_title = "Favorable Harvest"
        adv_steps = ["Plan for storage", "Expect good availability"]

    advisory = {
        "title": adv_title,
        "body": msg,
        "steps": adv_steps,
        "color": adv_color,
    }

    return int(risk_score), risk_level, msg, advisory
