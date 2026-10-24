# KrishiShield AI - Frontend Application

A responsive, multilingual React single-page application built with **Vite**, featuring offline resilience via **IndexedDB**, real-time price trend visualizations using **Recharts**, and dual-language localization (English and Marathi).

## Architecture Highlights

- **`src/components/layout/`**: Structural layout components (`Header.jsx`, `Sidebar.jsx`).
- **`src/components/dashboard/`**: Modular analytical widgets:
  - `ProjectedPriceCard.jsx`: Projected price, target horizon, and percentage deviation from historical norms.
  - `RiskMetricCard.jsx`: Visual risk score meter with progress bar.
  - `WeatherCard.jsx`: Multi-parameter weather dashboard with condition icons.
  - `PriceTrendChart.jsx`: 30-day historical + 7-day projected price curve.
  - `AdvisoryAlert.jsx`: Actionable agricultural advisory recommendations.
  - `ForecastTable.jsx`: 7-day meteorological forecast impact table.
- **`src/components/common/`**: Reusable notification modal, empty state, and error banner.
- **`src/services/`**:
  - `api.js`: Centralized Axios client configured with fallback base URLs.
  - `db.js`: IndexedDB wrapper for full offline availability (caching alerts, markets, app state, and predictions).
- **`src/i18n/`**: Internationalization module with English (`en.json`) and Marathi (`mr.json`) translations.
- **`src/utils/`**: Helper utilities for localized dates, risk indicators, and weather conditions.

## Development Workflow

### Install Dependencies
```bash
npm install
```

### Run Local Development Server
```bash
npm run dev
```
The application will be accessible at [http://localhost:5173](http://localhost:5173).

### Run Linter
```bash
npm run lint
```

### Production Build
```bash
npm run build
```
Build output is saved to `dist/`.
