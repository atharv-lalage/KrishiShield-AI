export const getDateLabel = (dateString, language = 'en') => {
  const d = new Date(dateString);
  const today = new Date();
  d.setHours(0, 0, 0, 0);
  today.setHours(0, 0, 0, 0);
  const diffDays = Math.ceil((d - today) / 86400000);

  if (diffDays === -1) return language === 'mr' ? 'काल' : 'Yesterday';
  if (diffDays === 0) return language === 'mr' ? 'आज' : 'Today';
  if (diffDays === 1) return language === 'mr' ? 'उद्या' : 'Tomorrow';

  return d.toLocaleDateString(language === 'mr' ? 'mr-IN' : 'en-US', { weekday: 'short' });
};
