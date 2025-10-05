import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { Box } from '@mui/material';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Dashboard from './pages/Dashboard';
import CropRecommendation from './pages/CropRecommendation';
import NutrientAnalysis from './pages/NutrientAnalysis';
import CropComparison from './pages/CropComparison';
import DistrictInsights from './pages/DistrictInsights';
import WeatherPlanning from './pages/WeatherPlanning';
import EconomicAnalysis from './pages/EconomicAnalysis';

function App() {
  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <Navbar />
      <Box component="main" sx={{ flex: 1, pt: 3, pb: 6 }}>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/crop-recommendation" element={<CropRecommendation />} />
          <Route path="/nutrient-analysis" element={<NutrientAnalysis />} />
          <Route path="/crop-comparison" element={<CropComparison />} />
          <Route path="/district-insights" element={<DistrictInsights />} />
          <Route path="/district-insights/:district" element={<DistrictInsights />} />
          <Route path="/weather-planning" element={<WeatherPlanning />} />
          <Route path="/economic-analysis" element={<EconomicAnalysis />} />
        </Routes>
      </Box>
      <Footer />
    </Box>
  );
}

export default App;
