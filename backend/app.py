import sys
from pathlib import Path
from datetime import timedelta, date
import pickle
import streamlit as st
import pandas as pd
import xgboost as xgb

# Ensure backend directory is on sys.path
backend_dir = Path(__file__).resolve().parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from src.core.config import (
    PRIMARY_DATA_FILE,
    FALLBACK_DATA_FILE,
    WEATHER_CACHE_FILE,
    MODEL_DIR,
    DATA_PROCESSED_DIR,
)
from src.services.weather_service import (
    fetch_extended_weather,
    load_weather_from_cache,
    update_weather_cache,
)

# --- Configuration ---
CACHE_FILE = str(WEATHER_CACHE_FILE)
LAG_WINDOW = 4
PRICE_COLUMN = "Modal_Price"

# --- 1. Data Loading ---


@st.cache_data
def load_base_data():
    """Loads raw data to get Market list."""
    file_to_load = (
        PRIMARY_DATA_FILE if PRIMARY_DATA_FILE.exists() else FALLBACK_DATA_FILE
    )
    if not file_to_load.exists():
        st.error(f"Base data file ({file_to_load}) not found.")
        return pd.DataFrame()

    try:
        df = pd.read_csv(file_to_load, index_col=False)
        df.columns = df.columns.str.strip()
        if df.columns[0].startswith("Unnamed") or df.columns[0] == "0":
            df = df.drop(columns=[df.columns[0]])
            if len(df.columns) > 0 and (
                df.columns[0].startswith("Unnamed") or df.columns[0] == "0"
            ):
                df = df.drop(columns=[df.columns[0]])
        return df
    except Exception:
        return pd.DataFrame()


@st.cache_data
def get_market_coordinates():
    """Extracts market coordinates."""
    file_to_load = (
        PRIMARY_DATA_FILE if PRIMARY_DATA_FILE.exists() else FALLBACK_DATA_FILE
    )
    try:
        df = pd.read_csv(file_to_load, index_col=False)
        df.columns = df.columns.str.strip()
        if "Market Name" in df.columns:
            df["Market Name"] = df["Market Name"].astype(str).str.strip()

        if "latitude_x" in df.columns and "longitude_x" in df.columns:
            coords = (
                df[["Market Name", "latitude_x", "longitude_x"]]
                .drop_duplicates()
                .set_index("Market Name")
            )
            return coords.to_dict("index")
        return {}
    except Exception:
        return {}


@st.cache_data
def get_seasonal_averages(commodity, market_name, target_month):
    """Calculates historical averages from commodity-specific lagged feature files."""
    file_path = DATA_PROCESSED_DIR / f"{commodity.lower()}_market_lagged_features.csv"
    defaults = {
        "Modal_Price": 2500.0,
        "temperature_2m_max": 30.0,
        "temperature_2m_min": 20.0,
        "temperature_2m_mean": 25.0,
        "precipitation_sum": 0.0,
        "precipitation_hours": 0.0,
        "wind_speed_10m_max": 10.0,
        "weather_code": 0.0,
    }

    if not file_path.exists():
        return defaults

    try:
        df = pd.read_csv(file_path, index_col=[0, 1], parse_dates=True)
        df.index.names = ["Market Name", "Price Date"]
        try:
            df_market = df.xs(market_name, level="Market Name", drop_level=False)
        except KeyError:
            return defaults

        df_month = df_market[
            df_market.index.get_level_values("Price Date").month == target_month
        ]
        if not df_month.empty:
            means = df_month.mean(numeric_only=True)
            for col in defaults.keys():
                if col in means:
                    defaults[col] = means[col]
        else:
            means = df_market.mean(numeric_only=True)
            for col in defaults.keys():
                if col in means:
                    defaults[col] = means[col]
        return defaults
    except Exception:
        return defaults


@st.cache_resource
def load_artifacts(commodity_name):
    """Loads model/scaler dynamically based on crop name from models/ directory."""
    model_path = MODEL_DIR / f"{commodity_name}.pkl"
    scaler_path = MODEL_DIR / f"{commodity_name.lower()}_scaler.pkl"

    # Also handle Onion json diff model if needed
    if "onion" in commodity_name.lower():
        json_path = MODEL_DIR / "onion_xgboost_model_diff.json"
        if json_path.exists():
            try:
                model = xgb.XGBRegressor()
                model.load_model(str(json_path))
                return model, None
            except Exception:
                pass

    try:
        with open(model_path, "rb") as f:
            model = pickle.load(f)
        if isinstance(model, xgb.XGBRegressor):
            model.set_params(device="cpu", tree_method="hist")
            try:
                model.get_booster().set_param({"device": "cpu", "tree_method": "hist"})
            except Exception:
                pass
        with open(scaler_path, "rb") as f:
            scaler = pickle.load(f)
        return model, scaler
    except FileNotFoundError:
        return None, None


# --- 2. Fetch Logic (Using Services) ---


def fetch_unified_weather(lat, lon):
    """Fetches weather data. Tries Online first, falls back to Cache."""
    df, status_msg = fetch_extended_weather(lat, lon)
    if "Cache" in status_msg or "Unavailable" in status_msg:
        st.warning(f"⚠️ Status: {status_msg}")
    return df, status_msg


# --- 3. Scenario Builder ---


def build_hybrid_scenario(df_api, historical_avgs):
    """Stitches API data with historical projections."""
    df_scenario = df_api.copy()
    last_api_date = df_scenario.index.max()
    start_date = df_scenario.index.min()
    current_duration = (last_api_date - start_date).days
    days_needed = max(0, 28 - current_duration)

    if days_needed > 0:
        projection_rows = []
        current_date = last_api_date + timedelta(days=1)
        for _ in range(days_needed + 1):
            row = historical_avgs.copy()
            row.pop("Modal_Price", None)
            row["Date"] = current_date
            projection_rows.append(row)
            current_date += timedelta(days=1)
        df_proj = pd.DataFrame(projection_rows).set_index("Date")
        df_scenario = pd.concat([df_scenario, df_proj])

    df_scenario["Modal_Price"] = historical_avgs["Modal_Price"]
    return df_scenario


def aggregate_to_weekly_lags(df_daily):
    """Aggregates daily data into exactly 4 weekly lags."""
    agg_rules = {
        "temperature_2m_max": "max",
        "temperature_2m_min": "min",
        "temperature_2m_mean": "mean",
        "precipitation_sum": "sum",
        "precipitation_hours": "sum",
        "wind_speed_10m_max": "mean",
        "weather_code": lambda x: x.mode()[0] if not x.empty else 0,
        "Modal_Price": "mean",
    }
    for col in agg_rules:
        if col not in df_daily.columns:
            df_daily[col] = 0
    df_weekly = df_daily.resample("7D", origin="start").agg(agg_rules)
    df_weekly = df_weekly.iloc[:LAG_WINDOW]
    while len(df_weekly) < LAG_WINDOW:
        last_row = df_weekly.iloc[[-1]].copy()
        last_row.index = last_row.index + timedelta(days=7)
        df_weekly = pd.concat([df_weekly, last_row])

    recent_weeks = df_weekly.iloc[::-1]
    simulated_data = []
    for i in range(len(recent_weeks)):
        row = recent_weeks.iloc[i]
        simulated_data.append(
            {
                "Week_Start": recent_weeks.index[i].strftime("%Y-%m-%d"),
                f"{PRICE_COLUMN}_Lag1": row["Modal_Price"],
                "temperature_2m_max": row["temperature_2m_max"],
                "precipitation_sum": row["precipitation_sum"],
                "weather_code": row["weather_code"],
                "temperature_2m_mean": row["temperature_2m_mean"],
                "temperature_2m_min": row["temperature_2m_min"],
                "wind_speed_10m_max": row["wind_speed_10m_max"],
                "precipitation_hours": row["precipitation_hours"],
            }
        )
    return simulated_data


def prepare_input_features(simulated_data, model_features, baseline_price):
    """Aligns user input with model features."""
    X_pred = pd.DataFrame(0.0, index=[0], columns=model_features)
    for lag in range(1, LAG_WINDOW + 1):
        data = simulated_data[lag - 1]
        for col in [
            "temperature_2m_mean",
            "temperature_2m_max",
            "temperature_2m_min",
            "wind_speed_10m_max",
            "precipitation_sum",
            "precipitation_hours",
            "weather_code",
        ]:
            if col in data:
                X_pred.loc[0, f"{col}_Lag{lag}"] = data[col]
        X_pred.loc[0, f"{PRICE_COLUMN}_Lag{lag}"] = baseline_price

    if simulated_data:
        proxy = simulated_data[0]
        for col in [
            "temperature_2m_mean",
            "temperature_2m_max",
            "temperature_2m_min",
            "wind_speed_10m_max",
            "precipitation_sum",
            "precipitation_hours",
            "weather_code",
        ]:
            if col in X_pred.columns and col in proxy:
                X_pred.loc[0, col] = proxy[col]
    return X_pred


# --- 4. Advisory Logic ---


def get_advisory(risk_label, crop_name):
    """Returns specific advice based on the calculated risk level."""
    if "HIGH" in risk_label:
        return {
            "title": f"🚨 Critical Advisory for {crop_name}",
            "body": f"The model predicts high price volatility (>25% above norm), likely driven by **adverse weather conditions** (such as heavy rain or heat stress) forecasted for the growing period. This indicates a high risk of crop damage or supply shortage.",
            "steps": [
                "**Delay Planting:** If heavy rain is forecast within the next 10 days, postpone sowing to prevent seed washout.",
                "**Drainage Check:** Ensure field drainage systems are clear to handle potential excess precipitation.",
                "**Crop Insurance:** Verify your coverage specifically for weather-related yield loss.",
                "**Input Management:** Hold off on applying expensive fertilizers until the weather stabilizes to avoid leaching.",
            ],
            "color": "error",
        }
    elif "MODERATE" in risk_label:
        return {
            "title": f"⚠️ Cautionary Advisory for {crop_name}",
            "body": "Conditions are deviating from the historical norm. Moderate stress on the crop is expected, with prices projected to be slightly elevated.",
            "steps": [
                "**Monitor Closely:** Increase frequency of field inspections for early signs of stress or pests.",
                "**Irrigation:** Manage water carefully; avoid over-irrigation if rain forecasts are erratic.",
                "**Nutrients:** Consider applying micronutrients or biostimulants to boost plant immunity against minor stress.",
            ],
            "color": "warning",
        }
    else:
        return {
            "title": f"✅ Favorable Advisory for {crop_name}",
            "body": "Weather forecasts align well with historical norms. Conditions are favorable for a standard or high yield.",
            "steps": [
                "**Maximize Yield:** Focus on standard agronomic practices (weeding, timely fertilization) to capitalize on good weather.",
                "**Market Strategy:** Good weather often leads to higher supply and stable prices. Plan your storage or post-harvest logistics early.",
                "**Routine Care:** Stick to the standard crop calendar.",
            ],
            "color": "success",
        }


# --- 5. Main Streamlit App ---


def main():
    st.set_page_config(page_title="Crop Risk Calculator", layout="wide")
    df_base = load_base_data()
    market_coords = get_market_coordinates()

    if df_base.empty:
        st.error("System Error: Missing Data File (semifinal.csv or test.csv).")
        st.stop()

    st.sidebar.header("Crop Selection")
    available_crops = ["Onion", "Wheat", "Potato"]
    selected_crop = st.sidebar.selectbox("Select Crop", available_crops)

    st.sidebar.divider()
    st.sidebar.header("Location")

    if "Commodity" in df_base.columns:
        valid_markets = sorted(
            df_base[df_base["Commodity"] == selected_crop]["Market Name"].unique()
        )
    else:
        valid_markets = sorted(df_base["Market Name"].unique())

    market = st.sidebar.selectbox("Select Market", valid_markets)
    model, scaler = load_artifacts(selected_crop)

    if st.sidebar.checkbox("Show Cache Status"):
        if WEATHER_CACHE_FILE.exists():
            st.sidebar.success("Cache File Exists")
            try:
                c_df = pd.read_csv(WEATHER_CACHE_FILE)
                st.sidebar.write(f"Entries: {len(c_df)}")
            except Exception:
                st.sidebar.error("Cache Corrupt")
        else:
            st.sidebar.warning("Cache Empty")

    st.title(f"🌾 {selected_crop} Future Risk Calculator")
    st.markdown(
        "**Rolling Horizon Analysis:** Observed (Past) + Forecast (Next 2 Weeks) + Projection (Week 4)."
    )

    if model is None:
        st.error(
            f"Model artifacts for {selected_crop} not found in models/ directory."
        )
        st.stop()

    today = date.today()
    future_target_date = today + timedelta(weeks=LAG_WINDOW)
    historical_avgs = get_seasonal_averages(
        selected_crop, market, future_target_date.month
    )
    baseline_price = historical_avgs["Modal_Price"]

    st.sidebar.divider()
    st.sidebar.metric("Historical Norm", f"₹{baseline_price:,.0f}")

    st.divider()

    if st.button("Analyze Future Risk", type="primary"):
        if market not in market_coords:
            clean_market = market.strip()
            found_key = next(
                (k for k in market_coords.keys() if str(k).strip() == clean_market),
                None,
            )
            if found_key:
                lat, lon = (
                    market_coords[found_key]["latitude_x"],
                    market_coords[found_key]["longitude_x"],
                )
            else:
                st.error("Coordinates not found.")
                st.stop()
        else:
            lat, lon = (
                market_coords[market]["latitude_x"],
                market_coords[market]["longitude_x"],
            )

        with st.spinner("Fetching weather data..."):
            df_api, source_status = fetch_unified_weather(lat, lon)

            if not df_api.empty:
                df_scenario = build_hybrid_scenario(df_api, historical_avgs)
                simulated_data = aggregate_to_weekly_lags(df_scenario)

                try:
                    feat_names = model.get_booster().feature_names
                    X_input = prepare_input_features(
                        simulated_data, feat_names, baseline_price
                    )
                    
                    if scaler:
                        X_scaled = scaler.transform(X_input)
                        pred_raw = model.predict(X_scaled)[0]
                    else:
                        pred_raw = model.predict(X_input)[0]

                    if "onion" in selected_crop.lower():
                        predicted_price = baseline_price + pred_raw
                    else:
                        predicted_price = pred_raw

                    deviation = predicted_price - baseline_price
                    pct_change = (deviation / baseline_price) * 100
                    risk_score = min(max((pct_change + 10) * 2.5, 0), 100)

                    col1, col2, col3 = st.columns(3)
                    col1.metric(
                        "Projected Price",
                        f"₹ {predicted_price:,.0f}",
                        delta=f"{pct_change:.1f}%",
                        delta_color="inverse",
                    )

                    if risk_score > 60:
                        risk_label, risk_color = "HIGH RISK", "red"
                        risk_desc = "Adverse weather conditions likely to spike prices."
                    elif risk_score > 30:
                        risk_label, risk_color = "MODERATE RISK", "orange"
                        risk_desc = "Conditions slightly deviating from ideal."
                    else:
                        risk_label, risk_color = "LOW RISK", "green"
                        risk_desc = "Favorable weather conditions."

                    col2.markdown("### Risk Level")
                    col2.markdown(
                        f"<h2 style='color:{risk_color}'>{risk_label}</h2>",
                        unsafe_allow_html=True,
                    )
                    col2.progress(int(risk_score) / 100)
                    col3.info(f"**Source:** {source_status}\n\n{risk_desc}")

                    # --- Advisory Window ---
                    st.divider()
                    advisory = get_advisory(risk_label, selected_crop)

                    if advisory["color"] == "error":
                        display_box = st.error
                    elif advisory["color"] == "warning":
                        display_box = st.warning
                    else:
                        display_box = st.success

                    with display_box(advisory["title"]):
                        st.write(advisory["body"])
                        st.markdown("#### Recommended Actions:")
                        for step in advisory["steps"]:
                            st.markdown(f"- {step}")

                    st.subheader("Data Timeline")
                    st.dataframe(
                        pd.DataFrame(simulated_data)[
                            [
                                "Week_Start",
                                "temperature_2m_max",
                                "precipitation_sum",
                                "weather_code",
                            ]
                        ],
                        use_container_width=True,
                    )
                except Exception as e:
                    st.error(f"Prediction Error: {e}")
            else:
                st.error(f"Could not fetch weather data. Status: {source_status}")


if __name__ == "__main__":
    main()
