import pandas as pd
from src.core.config import PRIMARY_DATA_FILE, FALLBACK_DATA_FILE


def load_market_data():
    """
    Loads base agricultural dataset and extracts market geographical coordinates.
    Returns (DF_BASE, MARKET_COORDS).
    """
    data_path = PRIMARY_DATA_FILE if PRIMARY_DATA_FILE.exists() else FALLBACK_DATA_FILE

    if data_path.exists():
        try:
            df = pd.read_csv(data_path, index_col=False)
            df.columns = df.columns.str.strip()

            if "Market Name" in df.columns:
                df["Market Name"] = df["Market Name"].astype(str).str.strip()
            if "Commodity" in df.columns:
                df["Commodity"] = df["Commodity"].astype(str).str.strip()

            if "latitude_x" in df.columns and "longitude_x" in df.columns:
                coords = (
                    df[["Market Name", "latitude_x", "longitude_x"]]
                    .drop_duplicates(subset=["Market Name"])
                    .set_index("Market Name")
                    .to_dict("index")
                )
            else:
                coords = {}
            return df, coords
        except Exception as e:
            print(f"Error loading base market data from {data_path}: {e}")
            return pd.DataFrame(), {}
    else:
        print(f"Base data file not found at {data_path}.")
        return pd.DataFrame(), {}
