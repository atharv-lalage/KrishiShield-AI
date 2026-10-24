from datetime import date, timedelta
import pandas as pd
from src.core.config import CURRENT_PETROL, CURRENT_DIESEL


def prepare_input_vector(model, weather_df: pd.DataFrame, price_stats: dict) -> pd.DataFrame:
    """
    Prepares input feature dataframe matching model's expected booster feature names.
    Extracts base prices, weather parameters, lagged features, and interaction terms.
    """
    required_features = model.get_booster().feature_names
    today = pd.Timestamp(date.today()).normalize()
    
    if today not in weather_df.index:
        if not weather_df.empty:
            current_idx = weather_df.index[-1]
        else:
            return pd.DataFrame()
    else:
        current_idx = today

    input_dict = {}

    # 1. Base Prices
    modal_price = price_stats.get("Modal_Price", 2500)
    input_dict["Modal_Price"] = modal_price
    input_dict["Min_Price"] = modal_price * 0.85
    input_dict["Max_Price"] = modal_price * 1.15
    input_dict["Petrol_Price"] = CURRENT_PETROL
    input_dict["Diesel_Price"] = CURRENT_DIESEL

    # 2. Weather
    temp_max = (
        weather_df.loc[current_idx, "temperature_2m_max"]
        if "temperature_2m_max" in weather_df.columns
        else 0
    )
    humid_max = (
        weather_df.loc[current_idx, "relative_humidity_2m_max"]
        if "relative_humidity_2m_max" in weather_df.columns
        else 0
    )
    rain_sum = (
        weather_df.loc[current_idx, "precipitation_sum"]
        if "precipitation_sum" in weather_df.columns
        else 0
    )

    for col in weather_df.columns:
        if col in required_features:
            input_dict[col] = weather_df.loc[current_idx, col]

    # 3. Lags
    for lag in range(1, 5):
        suffix = f"_Lag_{lag}"
        lag_val = price_stats.get(f"Lag_{lag}", modal_price)

        input_dict[f"Modal_Price{suffix}"] = lag_val
        input_dict[f"Min_Price{suffix}"] = lag_val * 0.85
        input_dict[f"Max_Price{suffix}"] = lag_val * 1.15
        input_dict[f"Petrol_Price{suffix}"] = CURRENT_PETROL
        input_dict[f"Diesel_Price{suffix}"] = CURRENT_DIESEL
        input_dict[f"weather_code{suffix}"] = 0

        lag_weather_date = current_idx - timedelta(days=lag)
        if lag_weather_date in weather_df.index:
            for col in weather_df.columns:
                feat_name = f"{col}{suffix}"
                if feat_name in required_features:
                    input_dict[feat_name] = weather_df.loc[lag_weather_date, col]

    # 4. Engineered Features
    month = today.month
    input_dict["Month"] = month
    input_dict["Rain_x_Month"] = rain_sum * month
    input_dict["Humidity_x_Temp"] = humid_max * temp_max
    input_dict["Petrol_x_Price"] = CURRENT_PETROL * modal_price
    input_dict["Diesel_x_Price"] = CURRENT_DIESEL * modal_price

    input_dict["Market_Mean_Price"] = price_stats.get("Market_Mean_Price", modal_price)
    input_dict["Rolling_Mean_Price_4w"] = price_stats.get("Rolling_Mean_Price_4w", modal_price)
    input_dict["Rolling_Std_Price_4w"] = price_stats.get(
        "Rolling_Std_Price_4w", modal_price * 0.05
    )

    input_df = pd.DataFrame(0.0, index=[0], columns=required_features)
    for col, val in input_dict.items():
        if col in input_df.columns:
            if pd.isna(val):
                val = 0.0
            input_df[col] = val

    return input_df
