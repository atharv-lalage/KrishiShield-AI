from datetime import date, timedelta
import pandas as pd
import requests
from src.core.config import WEATHER_CACHE_FILE


def update_weather_cache(new_data: pd.DataFrame, lat: float, lon: float):
    """Safely updates the offline weather cache with new observations."""
    try:
        df_new = new_data.copy()
        df_new["lat"] = round(lat, 4)
        df_new["lon"] = round(lon, 4)

        if WEATHER_CACHE_FILE.exists():
            try:
                df_old = pd.read_csv(WEATHER_CACHE_FILE, index_col="Date", parse_dates=True)
                df_combined = pd.concat([df_old, df_new])
                df_combined = (
                    df_combined.reset_index()
                    .drop_duplicates(subset=["Date", "lat", "lon"], keep="last")
                    .set_index("Date")
                )
                df_combined.to_csv(WEATHER_CACHE_FILE)
            except Exception:
                df_new.to_csv(WEATHER_CACHE_FILE)
        else:
            df_new.to_csv(WEATHER_CACHE_FILE)
    except Exception as e:
        print(f"Weather Cache Write Error: {e}")


def load_weather_from_cache(lat: float, lon: float, start_date=None, end_date=None):
    """Retrieves cached weather data when internet/API is offline."""
    if not WEATHER_CACHE_FILE.exists():
        return pd.DataFrame(), "Cache Empty"

    try:
        df = pd.read_csv(WEATHER_CACHE_FILE, index_col="Date", parse_dates=True)
        lat_mask = (df["lat"] >= lat - 0.1) & (df["lat"] <= lat + 0.1)
        lon_mask = (df["lon"] >= lon - 0.1) & (df["lon"] <= lon + 0.1)
        df_loc = df[lat_mask & lon_mask].copy()

        if df_loc.empty:
            return pd.DataFrame(), "No Cached Data for Location"

        if start_date and end_date:
            mask_date = (df_loc.index >= pd.Timestamp(start_date)) & (
                df_loc.index <= pd.Timestamp(end_date)
            )
            df_range = df_loc[mask_date]
            if not df_range.empty:
                return df_range.sort_index().drop(columns=["lat", "lon"], errors="ignore"), "Offline Cache"

        df_loc = df_loc.sort_index()
        last_date = df_loc.index.max()
        fallback_start = last_date - timedelta(days=25)
        df_fallback = df_loc[df_loc.index >= fallback_start]

        return (
            df_fallback.drop(columns=["lat", "lon"], errors="ignore"),
            f"Offline Cache (Updated: {last_date.date()})",
        )
    except Exception as e:
        return pd.DataFrame(), f"Cache Read Error: {e}"


def fetch_extended_weather(lat: float, lon: float):
    """
    Fetches comprehensive daily and hourly weather data from Open-Meteo API.
    Resamples hourly variables (humidity, soil moisture, surface pressure) to daily aggregates.
    Falls back to offline weather cache if network request fails.
    """
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_hours,wind_speed_10m_max",
            "hourly": "temperature_2m,relative_humidity_2m,surface_pressure,soil_moisture_9_to_27cm,soil_moisture_27_to_81cm",
            "timezone": "auto",
            "past_days": 21,
            "forecast_days": 7,
        }
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()

        hourly = pd.DataFrame(data.get("hourly", {}))
        if hourly.empty:
            return pd.DataFrame(), "Weather Unavailable"

        hourly["time"] = pd.to_datetime(hourly["time"])
        hourly.set_index("time", inplace=True)
        hourly = hourly.fillna(0)

        agg_dict = {
            "temperature_2m": ["mean"],
            "relative_humidity_2m": ["max", "min", "mean"],
            "surface_pressure": ["max", "min", "mean"],
            "soil_moisture_9_to_27cm": ["max", "min", "mean"],
            "soil_moisture_27_to_81cm": ["max", "min", "mean"],
        }
        daily_calc = hourly.resample("D").agg(agg_dict)
        daily_calc.columns = [f"{col[0]}_{col[1]}" for col in daily_calc.columns]

        rename_map = {
            "soil_moisture_9_to_27cm_max": "soil_moisture_7_to_28cm_max",
            "soil_moisture_9_to_27cm_min": "soil_moisture_7_to_28cm_min",
            "soil_moisture_9_to_27cm_mean": "soil_moisture_7_to_28cm_mean",
            "soil_moisture_27_to_81cm_max": "soil_moisture_28_to_100cm_max",
            "soil_moisture_27_to_81cm_min": "soil_moisture_28_to_100cm_min",
            "soil_moisture_27_to_81cm_mean": "soil_moisture_28_to_100cm_mean",
        }
        daily_calc.rename(columns=rename_map, inplace=True)

        daily_direct = pd.DataFrame(data.get("daily", {}))
        daily_direct["Date"] = pd.to_datetime(daily_direct["time"])
        daily_direct.set_index("Date", inplace=True)
        daily_direct.drop(columns=["time"], inplace=True)

        final_df = daily_calc.join(daily_direct, how="inner")
        final_df.index.name = "Date"

        # Safely update offline cache
        update_weather_cache(final_df, lat, lon)

        return final_df.fillna(0), "Live Weather API"

    except Exception as e:
        print(f"Weather Fetch Error: {e}")
        df_cached, cache_msg = load_weather_from_cache(lat, lon)
        if not df_cached.empty:
            return df_cached, cache_msg
        return pd.DataFrame(), "Weather Unavailable"
