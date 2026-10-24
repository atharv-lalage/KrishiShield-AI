import React from 'react';
import { X } from 'lucide-react';

const NotificationModal = ({ isOpen, onClose, alerts, t }) => {
  if (!isOpen) return null;

  return (
    <div
      style={{
        position: 'fixed',
        top: '70px',
        right: '20px',
        width: '350px',
        maxHeight: '500px',
        background: 'white',
        border: '1px solid #e2e8f0',
        borderRadius: '12px',
        boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
        zIndex: 60,
        overflowY: 'auto',
        padding: '1rem',
      }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1rem' }}>
        <h3 style={{ margin: 0, color: '#1e293b' }}>{t('alert_history')}</h3>
        <button
          onClick={onClose}
          style={{ background: 'none', border: 'none', cursor: 'pointer' }}
          aria-label="Close notifications"
        >
          <X size={18} />
        </button>
      </div>

      {alerts.length === 0 ? (
        <p style={{ color: '#94a3b8' }}>{t('no_alerts')}</p>
      ) : (
        alerts.map((alert) => (
          <div
            key={alert.id}
            style={{
              marginBottom: '10px',
              padding: '10px',
              borderRadius: '8px',
              background: alert.type === 'Critical' ? '#fef2f2' : '#fffbeb',
              borderLeft: `4px solid ${alert.type === 'Critical' ? '#ef4444' : '#f59e0b'}`,
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', color: '#64748b' }}>
              <span>
                {t(`crops.${alert.crop}`) || alert.crop} • {alert.market}
              </span>
              <span>{alert.timestamp ? alert.timestamp.split(' ')[1] : ''}</span>
            </div>
            <p style={{ margin: '5px 0', fontSize: '0.9rem', color: '#334155' }}>{alert.message}</p>
          </div>
        ))
      )}
    </div>
  );
};

export default NotificationModal;
