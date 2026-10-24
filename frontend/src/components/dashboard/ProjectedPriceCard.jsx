import React from 'react';
import { TrendingUp } from 'lucide-react';

const ProjectedPriceCard = ({ projectedPrice, targetDate, priceChange, t }) => {
  return (
    <div className="metric-card">
      <p style={{ color: '#64748b' }}>{t('projected_price')}</p>
      <div className="price-value">₹ {projectedPrice.toLocaleString()}</div>
      <div style={{ fontSize: '0.85rem', color: '#94a3b8', marginBottom: '5px' }}>
        Target: {targetDate}
      </div>
      <div
        style={{
          marginTop: '5px',
          fontWeight: '600',
          color: priceChange > 0 ? '#dc2626' : '#16a34a',
          display: 'flex',
          alignItems: 'center',
          gap: '5px',
        }}
      >
        <TrendingUp size={18} /> {priceChange}% {t('vs_norm')}
      </div>
    </div>
  );
};

export default ProjectedPriceCard;
