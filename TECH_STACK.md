# Technology Stack & Dependencies

## 1. Overview Matrix

| Domain | Technology | Version | Purpose |
| :--- | :--- | :--- | :--- |
| **Backend Framework** | FastAPI | `^0.115.0` | Asynchronous high-performance REST API |
| **ASGI Web Server** | Uvicorn | `^0.30.0` | Production ASGI web server |
| **Data Validation** | Pydantic | `^2.9.0` | Schema validation and serialization |
| **Job Scheduling** | APScheduler | `^3.10.0` | In-process cron job scheduler for 24h risk checks |
| **Machine Learning** | XGBoost | `^2.1.0` | Extreme Gradient Boosting regression models |
| **Data Preprocessing** | Scikit-Learn | `^1.6.0` | Feature scaling and transformation pipelines |
| **Data Manipulation** | Pandas & NumPy | `^2.2.0` / `^2.0.0` | Time series manipulation, aggregations, lags |
| **Alert Notifications** | Twilio REST SDK | `^9.3.0` | Multi-channel SMS and WhatsApp alerts |
| **Prototyping UI** | Streamlit | `^1.38.0` | Interactive data science verification dashboard |
| **Frontend Framework** | React | `^19.2.0` | Modern component-based user interface |
| **Build Tooling** | Vite | `^7.3.0` | Instant HMR development and optimized rollup builds |
| **Visual Charts** | Recharts | `^3.6.0` | Declarative SVG price trend line charts |
| **Icons** | Lucide React | `^0.562.0` | Crisp modern SVG agricultural and status icons |
| **Offline Persistence** | idb (IndexedDB) | `^8.0.3` | Client-side transactional storage for offline mode |
| **Localization** | i18next / react-i18next | `^25.7.0` / `^16.5.0` | Dual-language localization (English / Marathi) |
| **HTTP Client** | Axios | `^1.13.0` | Promise-based asynchronous HTTP client |

---

## 2. External Services & APIs

### 2.1 Open-Meteo Weather API
- **Endpoint**: `https://api.open-meteo.com/v1/forecast`
- **Payload**: Past 21 days historical weather + 7 days future forecast.
- **Parameters**: Temperature (max/min/mean), Relative Humidity, Soil Moisture ($7-28\text{cm}$, $28-100\text{cm}$), Surface Pressure, Precipitation Sum, Precipitation Hours, Wind Speed, Weather Code.
- **Fallback**: Local persistence in `backend/data/storage/offline_weather_cache.csv`.

### 2.2 Agmarknet Mandi Price API (Data.gov.in)
- **Endpoint**: `https://api.data.gov.in/resource/35985678-0d79-46b4-9ed6-6f13308a1d24`
- **Data Extracted**: Arrival dates, Mandi market names, Min/Max/Modal prices for Maharashtra.
- **Fallback**: Ground-truth historical data in `backend/data/raw/semifinal.csv`.

### 2.3 Twilio Cloud Communications API
- **Capabilities**: Programmable SMS and WhatsApp messaging.
- **Trigger**: Automatic notification dispatched when price change $>10\%$.

---

## 3. Package Management & Environments

### Backend Environment (`backend/requirements.txt`)
```txt
fastapi
uvicorn
pydantic
python-dotenv
twilio
APScheduler
pandas
numpy
scikit-learn
xgboost
requests
streamlit
urllib3<2
```

### Frontend Environment (`frontend/package.json`)
```json
{
  "dependencies": {
    "axios": "^1.13.2",
    "clsx": "^2.1.1",
    "framer-motion": "^12.23.26",
    "i18next": "^25.7.3",
    "i18next-browser-languagedetector": "^8.2.0",
    "idb": "^8.0.3",
    "lucide-react": "^0.562.0",
    "react": "^19.2.0",
    "react-dom": "^19.2.0",
    "react-i18next": "^16.5.0",
    "recharts": "^3.6.0",
    "tailwind-merge": "^3.4.0"
  }
}
```
