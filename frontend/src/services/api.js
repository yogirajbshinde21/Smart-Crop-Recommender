import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  }
});

// Health Check
export const healthCheck = async () => {
  const response = await api.get('/health');
  return response.data;
};

// Get Dropdown Data
export const getDropdownData = async () => {
  const response = await api.get('/dropdown-data');
  return response.data;
};

// Crop Recommendation
export const recommendCrop = async (data) => {
  const response = await api.post('/recommend-crop', data);
  return response.data;
};

// Nutrient Prediction
export const predictNutrients = async (data) => {
  const response = await api.post('/predict-nutrients', data);
  return response.data;
};

// Water Quality Analysis
export const analyzeWaterQuality = async (data) => {
  const response = await api.post('/water-quality-analysis', data);
  return response.data;
};

// Fertilizer Recommendation
export const recommendFertilizer = async (data) => {
  const response = await api.post('/fertilizer-recommendation', data);
  return response.data;
};

// Compare Crops
export const compareCrops = async (data) => {
  const response = await api.post('/compare-crops', data);
  return response.data;
};

// District Insights
export const getDistrictInsights = async (districtName) => {
  const response = await api.get(`/district-insights/${districtName}`);
  return response.data;
};

// Get Statistics
export const getStatistics = async () => {
  const response = await api.get('/statistics');
  return response.data;
};

export default api;
