export const getRiskColor = (level = '') => {
  if (level.includes('HIGH')) return '#dc2626';
  if (level.includes('MODERATE')) return '#d97706';
  return '#16a34a';
};
