import React from 'react';
import { Droplets, Waves, ArrowDown } from 'lucide-react';
import { getWeatherIcon, getWeatherLabel } from '../../utils/weatherHelpers';

const WeatherCard = ({ currentWeather, language, t }) => {
  if (!currentWeather) return null;

  const tempMax = currentWeather.temperature_2m_max;
  const weatherCode = currentWeather.weather_code || 0;
  const precipSum = currentWeather.precipitation_sum || 0;
  const humidity = currentWeather.relative_humidity_2m_mean?.toFixed(2) || 0;
  const tempMin = currentWeather.temperature_2m_min || 0;

  return (
    <div className="metric-card weather-card">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <div>
          <p style={{ color: '#64748b', marginBottom: '5px' }}>{t('current_weather')}</p>
          <div style={{ fontSize: '4rem', fontWeight: '800', color: '#1e293b', lineHeight: '1' }}>
            {tempMax}°C
          </div>
          <p
            style={{
              color: '#334155',
              fontWeight: '600',
              display: 'flex',
              alignItems: 'center',
              gap: '5px',
              marginTop: '10px',
              fontSize: '1.1rem',
            }}
          >
            {getWeatherLabel(weatherCode, language)}
          </p>
        </div>
        <div style={{ background: '#f0f9ff', padding: '15px', borderRadius: '16px' }}>
          {getWeatherIcon(weatherCode)}
        </div>
      </div>

      <div
        style={{
          marginTop: '20px',
          paddingTop: '20px',
          borderTop: '1px solid #f1f5f9',
          display: 'grid',
          gridTemplateColumns: '1fr 1fr 1fr',
          gap: '5px',
        }}
      >
        <div style={{ textAlign: 'center' }}>
          <Droplets size={20} color="#0ea5e9" style={{ marginBottom: '6px' }} />
          <div style={{ fontSize: '0.9rem', fontWeight: 'bold', color: '#334155' }}>
            {precipSum}mm
          </div>
          <div style={{ fontSize: '0.75rem', color: '#64748b' }}>{t('rain')}</div>
        </div>
        <div style={{ textAlign: 'center', borderLeft: '1px solid #f1f5f9' }}>
          <Waves size={20} color="#8b5cf6" style={{ marginBottom: '6px' }} />
          <div style={{ fontSize: '0.9rem', fontWeight: 'bold', color: '#334155' }}>
            {humidity}%
          </div>
          <div style={{ fontSize: '0.75rem', color: '#64748b' }}>Humid</div>
        </div>
        <div style={{ textAlign: 'center', borderLeft: '1px solid #f1f5f9' }}>
          <ArrowDown size={20} color="#64748b" style={{ marginBottom: '6px' }} />
          <div style={{ fontSize: '0.9rem', fontWeight: 'bold', color: '#334155' }}>
            {tempMin}°
          </div>
          <div style={{ fontSize: '0.75rem', color: '#64748b' }}>{t('min')}</div>
        </div>
      </div>
    </div>
  );
};

export default WeatherCard;
