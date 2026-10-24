import React from 'react';
import { AlertCircle, X } from 'lucide-react';

const ErrorBanner = ({ error, onDismiss }) => {
  if (!error) return null;

  return (
    <div
      style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '0.85rem 1.25rem',
        marginBottom: '1.5rem',
        borderRadius: '10px',
        backgroundColor: '#fef2f2',
        border: '1px solid #fecaca',
        color: '#b91c1c',
        fontSize: '0.95rem',
      }}
    >
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
        <AlertCircle size={20} color="#dc2626" />
        <span>{error}</span>
      </div>
      {onDismiss && (
        <button
          onClick={onDismiss}
          style={{ background: 'none', border: 'none', cursor: 'pointer', color: '#b91c1c' }}
          aria-label="Dismiss error"
        >
          <X size={18} />
        </button>
      )}
    </div>
  );
};

export default ErrorBanner;
