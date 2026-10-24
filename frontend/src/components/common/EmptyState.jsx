import React from 'react';
import { MapPin } from 'lucide-react';

const EmptyState = ({ isOnline, t }) => {
  return (
    <div style={{ textAlign: 'center', marginTop: '5rem', color: '#94a3b8' }}>
      <MapPin size={48} style={{ marginBottom: '1rem', opacity: 0.5 }} />
      <p style={{ fontSize: '1.2rem' }}>{isOnline ? t('select_prompt') : t('offline_prompt')}</p>
    </div>
  );
};

export default EmptyState;
