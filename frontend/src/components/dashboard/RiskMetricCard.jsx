import React from 'react';
import { getRiskColor } from '../../utils/riskHelpers';

const RiskMetricCard = ({ riskLevel, riskScore, t }) => {
  const color = getRiskColor(riskLevel);

  return (
    <div className="metric-card" style={{ textAlign: 'center' }}>
      <p style={{ color: '#64748b' }}>{t('risk_level')}</p>
      <div className="risk-value" style={{ color }}>
        {riskLevel} <span style={{ fontSize: '0.6em', opacity: 0.8 }}>({riskScore}%)</span>
      </div>
      <div className="risk-bar">
        <div
          className="risk-fill"
          style={{
            width: `${riskScore}%`,
            backgroundColor: color,
            height: '100%',
            borderRadius: '6px',
            transition: 'width 1s ease',
          }}
        />
      </div>
    </div>
  );
};

export default RiskMetricCard;
