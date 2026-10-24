import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const fetchAlerts = async () => {
  const response = await apiClient.get('/alerts');
  return response.data;
};

export const fetchMarkets = async (crop) => {
  const response = await apiClient.get(`/markets/${crop}`);
  return response.data.markets || [];
};

export const analyzeRisk = async (crop, market) => {
  const response = await apiClient.post('/analyze', { crop, market });
  return response.data;
};

export default apiClient;
