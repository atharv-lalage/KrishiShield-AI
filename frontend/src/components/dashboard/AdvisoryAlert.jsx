import React from 'react';

const AdvisoryAlert = ({ advisory }) => {
  if (!advisory) return null;

  const borderColor =
    advisory.color === 'success'
      ? '#22c55e'
      : advisory.color === 'warning'
      ? '#eab308'
      : '#ef4444';

  return (
    <div
      className={`advisory-box ${advisory.color}`}
      style={{
        padding: '1.5rem',
        borderRadius: '12px',
        marginBottom: '2rem',
        borderLeft: '5px solid',
        background: 'white',
        boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
        borderColor,
      }}
    >
      <h3 style={{ marginTop: 0, color: '#334155' }}>{advisory.title}</h3>
      <p>{advisory.body}</p>
      {advisory.steps && advisory.steps.length > 0 && (
        <ul style={{ paddingLeft: '1.5rem', marginBottom: 0 }}>
          {advisory.steps.map((step, idx) => (
            <li key={idx}>{step}</li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default AdvisoryAlert;
