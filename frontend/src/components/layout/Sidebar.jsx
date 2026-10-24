import React from 'react';
import { X, Database } from 'lucide-react';

const Sidebar = ({
  isOpen,
  onClose,
  crop,
  setCrop,
  market,
  setMarket,
  marketList,
  loading,
  isOnline,
  onAnalyze,
  t,
}) => {
  return (
    <aside className={`sidebar ${isOpen ? 'open' : ''}`}>
      <div className="sidebar-header">
        <h2>
          <img
            src="/Krishi.png"
            alt="Krishi Shield Logo"
            style={{ width: '50px', height: '50px', marginRight: '8px', verticalAlign: 'middle' }}
          />{' '}
          {t('app_title')}
        </h2>
        <button className="close-btn" onClick={onClose} aria-label="Close sidebar">
          <X size={24} />
        </button>
      </div>

      <div className="form-group">
        <label>{t('select_crop')}</label>
        <select value={crop} onChange={(e) => setCrop(e.target.value)} className="styled-select">
          <option value="Onion">{t('crops.Onion')}</option>
          <option value="Wheat">{t('crops.Wheat')}</option>
          <option value="Potato">{t('crops.Potato')}</option>
        </select>
      </div>

      <div className="form-group">
        <label>{t('select_market')}</label>
        <select
          value={market}
          onChange={(e) => setMarket(e.target.value)}
          className="styled-select"
          disabled={marketList.length === 0}
        >
          {marketList.length === 0 ? (
            <option>{t('analyzing')}</option>
          ) : (
            marketList.map((m) => (
              <option key={m} value={m}>
                {t(`markets.${m}`, { defaultValue: m })}
              </option>
            ))
          )}
        </select>
      </div>

      <button
        className="analyze-btn"
        onClick={onAnalyze}
        disabled={loading || !market}
      >
        {loading ? t('analyzing') : isOnline ? t('analyze_btn') : t('load_offline')}
      </button>

      {!isOnline && (
        <div
          style={{
            marginTop: '15px',
            padding: '10px',
            background: 'rgba(255,255,255,0.1)',
            borderRadius: '8px',
            border: '1px solid rgba(255,255,255,0.2)',
          }}
        >
          <p
            style={{
              margin: 0,
              fontSize: '0.85rem',
              color: '#fca5a5',
              fontWeight: 'bold',
              display: 'flex',
              alignItems: 'center',
              gap: '5px',
            }}
          >
            <Database size={14} /> {t('offline_mode')}
          </p>
          <p style={{ margin: '5px 0 0 0', fontSize: '0.75rem', color: '#e2e8f0' }}>
            {t('offline_desc')}
          </p>
        </div>
      )}
    </aside>
  );
};

export default Sidebar;
