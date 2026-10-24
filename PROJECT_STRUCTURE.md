# Project Directory Structure

```
KrishiShield-AI/
├── .gitignore                          # Git ignore configuration
├── README.md                           # Main project overview and getting started guide
├── PROJECT_STRUCTURE.md                # Complete directory tree and organization breakdown
├── ARCHITECTURE.md                     # High-level architecture, data flows, and module design
├── TECH_STACK.md                       # Comprehensive technologies and dependency reference
├── DEVELOPMENT.md                      # Developer guides, testing workflows, and best practices
├── backend/                            # Python Backend (FastAPI, APScheduler & Streamlit)
│   ├── .env                            # Environment secrets (ignored by git)
│   ├── .env.example                    # Template environment variables
│   ├── Dockerfile                      # Production container image definition
│   ├── requirements.txt                # Python package dependencies
│   ├── main.py                         # Primary FastAPI application entry point
│   ├── app.py                          # Companion Streamlit application entry point
│   │
│   ├── src/                            # Modular Backend Source Code
│   │   ├── __init__.py
│   │   ├── core/                       # Core system configuration and data loaders
│   │   │   ├── __init__.py
│   │   │   ├── config.py               # Paths, credentials, API keys, fuel constants
│   │   │   ├── constants.py            # Supported crops, horizon limits, check lists
│   │   │   └── data_loader.py          # Resilient dataset loading and coordinate indexing
│   │   │
│   │   ├── api/                        # HTTP API presentation layer
│   │   │   ├── __init__.py
│   │   │   ├── schemas.py              # Pydantic request and response schemas
│   │   │   └── routes.py               # Endpoints (/alerts, /markets/{crop}, /analyze)
│   │   │
│   │   ├── services/                   # Business and integration services
│   │   │   ├── __init__.py
│   │   │   ├── weather_service.py      # Open-Meteo weather API client and cache
│   │   │   ├── agmarknet_service.py    # Government Mandi (data.gov.in) price service
│   │   │   ├── notification_service.py # Twilio SMS & WhatsApp alert dispatcher
│   │   │   ├── alert_service.py        # Persistent alert history storage manager
│   │   │   └── risk_service.py         # Risk scoring, advisory formatting, and trend simulation
│   │   │
│   │   ├── ml/                         # Machine learning engine
│   │   │   ├── __init__.py
│   │   │   ├── model_loader.py         # XGBoost and Pickle artifact loading
│   │   │   └── feature_engineering.py  # Model-specific feature vector construction
│   │   │
│   │   └── scheduler/                  # Background task orchestration
│   │       ├── __init__.py
│   │       └── risk_monitor.py         # 24-hour price fluctuation monitoring daemon
│   │
│   ├── models/                         # Serialized Machine Learning Artifacts
│   │   ├── onion_xgboost_model_diff.json   # High-precision XGBoost differential regressor
│   │   ├── Potato.pkl                  # Trained Potato price predictor
│   │   ├── Rice.pkl                    # Trained Rice price predictor
│   │   ├── Tomato.pkl                  # Trained Tomato price predictor
│   │   ├── Wheat.pkl                   # Trained Wheat price predictor
│   │   ├── potato_scaler.pkl           # Preprocessing standard scaler for Potato
│   │   ├── wheat_scaler.pkl            # Preprocessing standard scaler for Wheat
│   │   └── tuned_xgb_model.pkl         # Auxiliary fine-tuned baseline model
│   │
│   ├── data/                           # Organized Datasets and Runtime Storage
│   │   ├── raw/                        # Ground-truth raw datasets
│   │   │   ├── semifinal.csv           # Primary Mandi prices and market location dataset
│   │   │   └── test.csv                # Minimal fallback validation dataset
│   │   ├── processed/                  # Feature engineered time-series datasets
│   │   │   ├── onion_market_lagged_features.csv
│   │   │   ├── onion_model_data_interactions_market.csv
│   │   │   ├── potato_market_lagged_features.csv
│   │   │   ├── rice_market_lagged_features.csv
│   │   │   ├── tomato_market_lagged_features.csv
│   │   │   └── wheat_market_lagged_features.csv
│   │   └── storage/                    # Mutable runtime caches and application state
│   │       ├── alert_history.json      # Dynamic record of triggered SMS/WhatsApp alerts
│   │       ├── risk_state_cache.json   # 24h risk comparison state cache
│   │       └── offline_weather_cache.csv # Historical Open-Meteo offline cache
│   │
│   ├── scripts/                        # Maintenance, data prep, and extraction tools
│   │   ├── __init__.py
│   │   ├── data_preparation.py         # Weekly time-series aggregation & lag generator
│   │   └── fetch_mandi_prices.py       # Mandi price fetcher and validator
│   │
│   ├── notebooks/                      # Exploratory Data Analysis & Modeling Notebooks
│   │   └── data_analysis_eda.ipynb     # Data exploration and cleaning notebook
│   │
│   └── tests/                          # Backend Unit & Integration Test Suite
│       ├── __init__.py
│       ├── test_config.py              # Configuration and path validation tests
│       ├── test_ml_loader.py           # Model loading and fallback tests
│       ├── test_services.py            # Risk calculation and alerts tests
│       └── test_api.py                 # FastAPI endpoint integration tests
│
└── frontend/                           # React 19 Frontend (Vite + IndexedDB + Recharts)
    ├── .gitignore                      # Frontend-specific ignore file
    ├── index.html                      # HTML5 root document
    ├── package.json                    # Node dependencies and scripts
    ├── package-lock.json               # Deterministic dependency lockfile
    ├── vite.config.js                  # Vite build configuration
    ├── eslint.config.js                # ESLint code quality configuration
    │
    ├── public/                         # Static Web Assets
    │   └── Krishi.png                  # Application branding logo
    │
    └── src/                            # Frontend Source Code
        ├── main.jsx                    # React virtual DOM entrypoint
        ├── App.jsx                     # Composed dashboard application shell
        ├── App.css                     # Responsive dashboard styling and variables
        ├── index.css                   # Global CSS reset and scrollbar styling
        │
        ├── i18n/                       # Internationalization Subsystem
        │   ├── i18n.js                 # i18next configuration and language detection
        │   └── locales/
        │       ├── en.json             # English translation strings
        │       └── mr.json             # Marathi translation strings
        │
        ├── services/                   # Network & Local Database Services
        │   ├── api.js                  # Axios HTTP client with configurable base URL
        │   └── db.js                   # IndexedDB wrapper (alerts, markets, cache)
        │
        ├── components/                 # Component Hierarchy
        │   ├── layout/
        │   │   ├── Header.jsx          # Top navigation, status indicator, language toggle
        │   │   └── Sidebar.jsx         # Collapsible filter drawer and crop/market selector
        │   ├── dashboard/
        │   │   ├── ProjectedPriceCard.jsx # Predicted price, target date, and % delta
        │   │   ├── RiskMetricCard.jsx  # Color-coded risk level badge and progress bar
        │   │   ├── WeatherCard.jsx     # Current weather condition, icon, and metrics
        │   │   ├── PriceTrendChart.jsx # Recharts 30-day historical + 7-day forecast
        │   │   ├── AdvisoryAlert.jsx   # Farmer action items and risk advisory
        │   │   └── ForecastTable.jsx   # 7-day meteorological forecast table
        │   └── common/
        │       ├── NotificationModal.jsx # Dropdown list of past alerts
        │       ├── EmptyState.jsx      # Initial state prompt before selection
        │       └── ErrorBanner.jsx     # Dismissible notification and error banner
        │
        └── utils/                      # Helper Utilities
            ├── dateHelpers.js          # Relative and localized date label generator
            ├── riskHelpers.js          # Color mappings for risk levels
            └── weatherHelpers.jsx      # Weather code to Lucide icon and localized label
```
