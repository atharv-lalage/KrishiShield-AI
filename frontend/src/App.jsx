import React, { useState, useEffect, useCallback } from 'react';
import { useTranslation } from 'react-i18next';
import { Menu } from 'lucide-react';

import Header from './components/layout/Header';
import Sidebar from './components/layout/Sidebar';
import NotificationModal from './components/common/NotificationModal';
import EmptyState from './components/common/EmptyState';
import ErrorBanner from './components/common/ErrorBanner';
import ProjectedPriceCard from './components/dashboard/ProjectedPriceCard';
import RiskMetricCard from './components/dashboard/RiskMetricCard';
import WeatherCard from './components/dashboard/WeatherCard';
import PriceTrendChart from './components/dashboard/PriceTrendChart';
import AdvisoryAlert from './components/dashboard/AdvisoryAlert';
import ForecastTable from './components/dashboard/ForecastTable';

import { fetchAlerts, fetchMarkets, analyzeRisk } from './services/api';
import {
  getStoredAlerts,
  saveAlertToDB,
  saveAppState,
  getAppState,
  saveMarketList,
  getMarketList,
  saveAnalysisResult,
  getAnalysisResult,
} from './services/db';

import './App.css';
import './i18n/i18n';

function App() {
  const { t, i18n } = useTranslation();

  // --- APPLICATION STATE ---
  const [crop, setCrop] = useState('Onion');
  const [market, setMarket] = useState('');
  const [marketList, setMarketList] = useState([]);
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // --- UI STATE ---
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [showNotifications, setShowNotifications] = useState(false);
  const [isOnline, setIsOnline] = useState(navigator.onLine);
  const [alerts, setAlerts] = useState([]);
  const [lastAlertId, setLastAlertId] = useState(0);

  const toggleLanguage = () => {
    const newLang = i18n.language === 'en' ? 'mr' : 'en';
    i18n.changeLanguage(newLang);
  };

  // --- INITIALIZATION & NETWORK LISTENERS ---
  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);
    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    if ('Notification' in window) {
      Notification.requestPermission();
    }

    const loadInitData = async () => {
      try {
        const savedAlerts = await getStoredAlerts();
        setAlerts(savedAlerts);
        if (savedAlerts.length > 0) {
          setLastAlertId(savedAlerts[0].id);
        }

        const savedCrop = await getAppState('lastCrop');
        const savedMarket = await getAppState('lastMarket');
        if (savedCrop) setCrop(savedCrop);
        if (savedMarket) setMarket(savedMarket);

        if (!navigator.onLine) {
          const offlineMarkets = await getMarketList(savedCrop || 'Onion');
          setMarketList(offlineMarkets);
        }
      } catch (err) {
        console.error('Failed to load initial data from IndexedDB:', err);
      }
    };

    loadInitData();

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  // --- ALERT POLLING ---
  useEffect(() => {
    const pollAlerts = async () => {
      if (!isOnline) return;
      try {
        const latestAlerts = await fetchAlerts();
        if (latestAlerts && latestAlerts.length > 0) {
          const newest = latestAlerts[0];
          if (newest.id > lastAlertId) {
            if (Notification.permission === 'granted') {
              new Notification(`Risk Alert: ${newest.crop}`, {
                body: newest.message,
                icon: '/Krishi.png',
              });
            }
            setAlerts(latestAlerts);
            setLastAlertId(newest.id);
            for (const alert of latestAlerts) {
              await saveAlertToDB(alert);
            }
          }
        }
      } catch (e) {
        console.error('Background alert sync failed:', e);
      }
    };

    pollAlerts();
    const interval = setInterval(pollAlerts, 30000);
    return () => clearInterval(interval);
  }, [isOnline, lastAlertId]);

  // --- LOAD MARKETS FOR SELECTED CROP ---
  const loadMarkets = useCallback(async () => {
    try {
      setMarketList([]);
      if (isOnline) {
        const markets = await fetchMarkets(crop);
        setMarketList(markets);
        await saveMarketList(crop, markets);
        if (!market || !markets.includes(market)) {
          if (markets.length > 0) setMarket(markets[0]);
        }
      } else {
        const cachedMarkets = await getMarketList(crop);
        if (cachedMarkets.length > 0) {
          setMarketList(cachedMarkets);
          if (!market || !cachedMarkets.includes(market)) {
            setMarket(cachedMarkets[0]);
          }
        } else {
          setError(`No offline data for ${crop}. Connect to internet.`);
        }
      }
    } catch (err) {
      console.error('Failed to load markets:', err);
      setError('Could not load markets.');
    }
  }, [crop, isOnline, market]);

  useEffect(() => {
    loadMarkets();
  }, [crop, isOnline, loadMarkets]);

  // --- ANALYZE ACTION ---
  const handleAnalyze = async () => {
    if (!market) {
      alert('Please select a market');
      return;
    }

    setLoading(true);
    setError('');
    setData(null);

    if (window.innerWidth <= 1024) {
      setIsSidebarOpen(false);
    }

    await saveAppState('lastCrop', crop);
    await saveAppState('lastMarket', market);

    if (isOnline) {
      try {
        const result = await analyzeRisk(crop, market);
        setData(result);
        await saveAnalysisResult(crop, market, result);
      } catch (err) {
        setError(err.response?.data?.detail || 'Prediction failed. Please try again.');
      } finally {
        setLoading(false);
      }
    } else {
      try {
        const cachedResult = await getAnalysisResult(crop, market);
        if (cachedResult) {
          setData(cachedResult);
        } else {
          setError("This specific market hasn't been analyzed/cached yet in offline storage.");
        }
      } catch (e) {
        console.error('Error loading offline analysis cache:', e);
        setError('Error loading offline data.');
      } finally {
        setLoading(false);
      }
    }
  };

  return (
    <div className="app-container">
      {/* Mobile Hamburger Menu Button */}
      <button
        className="menu-btn"
        onClick={() => setIsSidebarOpen(true)}
        aria-label="Open menu"
      >
        <Menu size={24} />
      </button>

      {/* Mobile Drawer Overlay */}
      <div
        className={`overlay ${isSidebarOpen ? 'active' : ''}`}
        onClick={() => setIsSidebarOpen(false)}
      />

      {/* Notification Dropdown / Modal */}
      <NotificationModal
        isOpen={showNotifications}
        onClose={() => setShowNotifications(false)}
        alerts={alerts}
        t={t}
      />

      {/* Sidebar Navigation */}
      <Sidebar
        isOpen={isSidebarOpen}
        onClose={() => setIsSidebarOpen(false)}
        crop={crop}
        setCrop={setCrop}
        market={market}
        setMarket={setMarket}
        marketList={marketList}
        loading={loading}
        isOnline={isOnline}
        onAnalyze={handleAnalyze}
        t={t}
      />

      {/* Main Content Area */}
      <main className="main-content">
        <Header
          crop={crop}
          market={market}
          isOnline={isOnline}
          alertsCount={alerts.length}
          onToggleLanguage={toggleLanguage}
          onToggleNotifications={() => setShowNotifications(!showNotifications)}
          currentLanguage={i18n.language}
          t={t}
        />

        <hr style={{ borderColor: '#e2e8f0', margin: '2rem 0' }} />

        {/* Dismissible Error Banner */}
        <ErrorBanner error={error} onDismiss={() => setError('')} />

        {/* Dashboard Results or Empty Placeholder */}
        {data ? (
          <div className="fade-in">
            <div className="metrics-grid">
              <ProjectedPriceCard
                projectedPrice={data.projected_price}
                targetDate={data.target_date}
                priceChange={data.price_change}
                t={t}
              />

              <RiskMetricCard
                riskLevel={data.risk_level}
                riskScore={data.risk_score}
                t={t}
              />

              <WeatherCard
                currentWeather={data.timeline ? data.timeline[0] : null}
                language={i18n.language}
                t={t}
              />
            </div>

            <PriceTrendChart priceTrend={data.price_trend} />

            <AdvisoryAlert advisory={data.advisory} />

            <ForecastTable
              timeline={data.timeline}
              language={i18n.language}
              t={t}
            />
          </div>
        ) : (
          <EmptyState isOnline={isOnline} t={t} />
        )}
      </main>
    </div>
  );
}

export default App;