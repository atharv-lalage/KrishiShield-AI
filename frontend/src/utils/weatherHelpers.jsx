import React from 'react';
import { Sun, Cloud, CloudRain, CloudLightning, Snowflake } from 'lucide-react';

export const getWeatherIcon = (code = 0, size = 64) => {
  if (code >= 95) return <CloudLightning size={size} color="#6366f1" />;
  if (code >= 71) return <Snowflake size={size} color="#3b82f6" />;
  if (code >= 51) return <CloudRain size={size} color="#0ea5e9" />;
  if (code >= 1) return <Cloud size={size} color="#94a3b8" />;
  return <Sun size={size} color="#f59e0b" />;
};

export const getWeatherLabel = (code = 0, language = 'en') => {
  if (code >= 95) return language === 'mr' ? 'वादळी' : 'Stormy';
  if (code >= 71) return language === 'mr' ? 'बर्फवृष्टी' : 'Snow';
  if (code >= 51) return language === 'mr' ? 'पावसाळी' : 'Rainy';
  if (code >= 1) return language === 'mr' ? 'ढगाळ' : 'Cloudy';
  return language === 'mr' ? 'सूर्यप्रकाश' : 'Sunny';
};
