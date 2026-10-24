import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';

const PriceTrendChart = ({ priceTrend }) => {
  if (!priceTrend || priceTrend.length === 0) return null;

  return (
    <div
      style={{
        background: 'white',
        padding: '1.5rem',
        borderRadius: '16px',
        border: '1px solid #e2e8f0',
        marginBottom: '2rem',
        boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
      }}
    >
      <h3 style={{ color: '#334155', marginTop: 0, marginBottom: '1.5rem' }}>
        Price Trend (History + 7-Day Forecast)
      </h3>
      <div style={{ width: '100%', height: 300 }}>
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={priceTrend}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} />
            <XAxis dataKey="date" tick={{ fontSize: 12 }} />
            <YAxis domain={['auto', 'auto']} tick={{ fontSize: 12 }} />
            <Tooltip
              contentStyle={{
                borderRadius: '8px',
                border: 'none',
                boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
              }}
            />
            <Line
              type="monotone"
              dataKey="price"
              stroke="#16a34a"
              strokeWidth={3}
              dot={{ r: 4 }}
              activeDot={{ r: 6 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default PriceTrendChart;
