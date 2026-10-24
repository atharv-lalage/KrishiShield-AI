# Supported crops across the platform
SUPPORTED_CROPS = ["Onion", "Wheat", "Potato", "Tomato", "Rice"]

# Primary crops shown in standard dropdowns
DEFAULT_ACTIVE_CROPS = ["Onion", "Wheat", "Potato"]

# Default modal price fallback
DEFAULT_MODAL_PRICE = 2500.0

# Time series parameters
DEFAULT_LAG_WINDOW = 4
FORECAST_DAYS = 7
HISTORICAL_PAST_DAYS = 21

# Scheduled check targets
MONITOR_CHECK_LIST = [
    ("Onion", "pune"),
    ("Potato", "nashik"),
    ("Wheat", "mumbai")
]
