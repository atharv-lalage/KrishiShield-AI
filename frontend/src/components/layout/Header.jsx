import React from 'react';
import { Sprout, Globe, Wifi, WifiOff, Bell } from 'lucide-react';

const Header = ({
  crop,
  market,
  isOnline,
  alertsCount,
  onToggleLanguage,
  onToggleNotifications,
  currentLanguage,
  t,
}) => {
  return (
    <div className="header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
      <div>
        <h1>
          <Sprout color="#15803d" size={40} /> {crop} 7-Day Risk Calculator
        </h1>
        <p className="subtitle">
          {t('subtitle', {
            market: market ? t(`markets.${market}`, { defaultValue: market }) : t('select_market'),
          })}
        </p>
      </div>
      <div style={{ display: 'flex', gap: '15px', alignItems: 'center' }}>
        <button
          onClick={onToggleLanguage}
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '5px',
            padding: '8px 12px',
            borderRadius: '20px',
            border: '1px solid #cbd5e1',
            background: 'white',
            cursor: 'pointer',
            fontWeight: 'bold',
            color: '#0f172a',
          }}
        >
          <Globe size={18} /> {currentLanguage === 'en' ? 'English' : 'मराठी'}
        </button>
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '5px',
            color: isOnline ? '#16a34a' : '#ef4444',
            fontWeight: 'bold',
            fontSize: '0.9rem',
          }}
        >
          {isOnline ? <Wifi size={18} /> : <WifiOff size={18} />}
          {isOnline ? t('online') : t('offline')}
        </div>
        <button
          onClick={onToggleNotifications}
          style={{
            position: 'relative',
            background: 'white',
            border: '1px solid #e2e8f0',
            padding: '8px',
            borderRadius: '50%',
            cursor: 'pointer',
          }}
          aria-label="Notifications"
        >
          <Bell size={20} color="#334155" />
          {alertsCount > 0 && (
            <span
              style={{
                position: 'absolute',
                top: '-2px',
                right: '-2px',
                background: '#ef4444',
                color: 'white',
                fontSize: '10px',
                width: '16px',
                height: '16px',
                borderRadius: '50%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
              }}
            >
              {alertsCount}
            </span>
          )}
        </button>
      </div>
    </div>
  );
};

export default Header;
