// File: app/frontend/static/dashboard.js
import React from 'react';
import ReactDOM from 'react-dom/client';
import { HealthcareDashboard } from '../components/HealthcareDashboard.jsx';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <HealthcareDashboard />
  </React.StrictMode>
);