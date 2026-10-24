from io import StringIO
from datetime import date, timedelta
import pandas as pd
import requests
from src.core.config import AGMARKNET_API_KEY, AGMARKNET_RESOURCE_ID


def fetch_agmarknet_data(crop: str, market: str):
    """
    Fetches real-time market arrival and pricing data from Agmarknet (data.gov.in) API.
    Calculates modal price, mean price, weekly lags (Lag 1-4), and 4-week rolling stats.
    """
    today = date.today()
    date_from = (today - timedelta(weeks=10)).strftime("%Y-%m-%d")
    date_to = (today + timedelta(days=1)).strftime("%Y-%m-%d")

    url = (
        f"https://api.data.gov.in/resource/{AGMARKNET_RESOURCE_ID}"
        f"?api-key={AGMARKNET_API_KEY}"
        f"&format=csv"
        f"&filters[State]=Maharashtra"
        f"&filters[Commodity]={crop}"
        f"&range[Arrival_Date][gte]={date_from}"
        f"&range[Arrival_Date][lte]={date_to}"
        f"&limit=5000"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        df = pd.read_csv(StringIO(response.text))

        if df.empty:
            return None

        df.columns = df.columns.str.strip()

        # Filter by Market or District
        market_col = "Market" if "Market" in df.columns else "District"
        if market_col:
            mask = df[market_col].astype(str).str.contains(market, case=False, na=False)
            market_df = df[mask].copy()
        else:
            market_df = df.copy()

        if market_df.empty:
            market_df = df  # Fallback to statewide commodity data

        market_df["Arrival_Date"] = pd.to_datetime(market_df["Arrival_Date"], dayfirst=True)
        market_df = market_df.sort_values("Arrival_Date")
        market_df.set_index("Arrival_Date", inplace=True)

        daily_series = market_df["Modal_Price"].resample("D").mean().ffill()
        if daily_series.empty:
            return None

        current_price = daily_series.iloc[-1]

        stats = {
            "Modal_Price": current_price,
            "Market_Mean_Price": daily_series.mean(),
            "Lag_1": daily_series.shift(7).iloc[-1] if len(daily_series) > 7 else current_price,
            "Lag_2": daily_series.shift(14).iloc[-1] if len(daily_series) > 14 else current_price,
            "Lag_3": daily_series.shift(21).iloc[-1] if len(daily_series) > 21 else current_price,
            "Lag_4": daily_series.shift(28).iloc[-1] if len(daily_series) > 28 else current_price,
        }

        rolling = daily_series.rolling(window=28, min_periods=1)
        stats["Rolling_Mean_Price_4w"] = rolling.mean().iloc[-1]
        stats["Rolling_Std_Price_4w"] = rolling.std().iloc[-1]
        if pd.isna(stats["Rolling_Std_Price_4w"]):
            stats["Rolling_Std_Price_4w"] = current_price * 0.05

        return stats

    except Exception as e:
        print(f"Agmarknet API Failed: {e}")
        return None
