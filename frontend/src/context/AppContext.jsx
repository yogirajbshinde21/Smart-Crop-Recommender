import React, { createContext, useContext, useState, useEffect } from 'react';
import { getDropdownData, healthCheck } from '../services/api';

const AppContext = createContext();

export const useApp = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within AppProvider');
  }
  return context;
};

export const AppProvider = ({ children }) => {
  const [dropdownData, setDropdownData] = useState({
    districts: [],
    soil_types: [],
    crops: [],
    weather_conditions: [],
    fertilizers: [],
    zones: []
  });
  
  const [loading, setLoading] = useState(true);
  const [apiStatus, setApiStatus] = useState('checking');
  const [language, setLanguage] = useState('en'); // en, hi, mr

  useEffect(() => {
    checkApiHealth();
    loadDropdownData();
  }, []);

  const checkApiHealth = async () => {
    try {
      const response = await healthCheck();
      if (response.status === 'healthy') {
        setApiStatus('connected');
      } else {
        setApiStatus('error');
      }
    } catch (error) {
      console.error('API health check failed:', error);
      setApiStatus('error');
    }
  };

  const loadDropdownData = async () => {
    try {
      const response = await getDropdownData();
      if (response.success) {
        setDropdownData(response.data);
      }
      setLoading(false);
    } catch (error) {
      console.error('Failed to load dropdown data:', error);
      setLoading(false);
    }
  };

  const value = {
    dropdownData,
    loading,
    apiStatus,
    language,
    setLanguage,
    refreshDropdownData: loadDropdownData,
    checkApiHealth
  };

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
};
