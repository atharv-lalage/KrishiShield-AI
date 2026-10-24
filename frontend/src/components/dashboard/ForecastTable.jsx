import React from 'react';
import { getDateLabel } from '../../utils/dateHelpers';

const ForecastTable = ({ timeline, language, t }) => {
  if (!timeline || timeline.length === 0) return null;

  return (
    <div>
      <h3 style={{ color: '#334155', marginTop: '2rem' }}>{t('forecast_impact')}</h3>
      <div className="data-table-container">
        <table>
          <thead>
            <tr>
              <th>{t('day')}</th>
              <th>{t('date')}</th>
              <th>{t('max_temp')} (°C)</th>
              <th>{t('precip')} (mm)</th>
            </tr>
          </thead>
          <tbody>
            {timeline.map((row, idx) => {
              const label = getDateLabel(row.Date, language);
              const isToday = label === 'Today' || label === 'आज';

              return (
                <tr key={idx} style={isToday ? { backgroundColor: '#dcfce7' } : {}}>
                  <td
                    style={{
                      fontWeight: isToday ? '800' : 'normal',
                      color: isToday ? '#166534' : '#334155',
                    }}
                  >
                    {label}
                  </td>
                  <td style={{ color: '#64748b', fontSize: '0.9rem' }}>
                    {new Date(row.Date).toLocaleDateString(undefined, {
                      month: 'short',
                      day: 'numeric',
                    })}
                  </td>
                  <td style={{ fontWeight: 'bold', fontSize: isToday ? '1.1rem' : '1rem' }}>
                    {row.temperature_2m_max}
                  </td>
                  <td>
                    {row.precipitation_sum > 0 ? (
                      <span style={{ color: '#2563eb', fontWeight: 'bold' }}>
                        {row.precipitation_sum}
                      </span>
                    ) : (
                      <span style={{ color: '#94a3b8' }}>-</span>
                    )}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default ForecastTable;
