import React, { useState } from 'react';
import {
  Container, Grid, Card, CardContent, Typography, Box, TextField, Button,
  MenuItem, Alert, Chip, Paper
} from '@mui/material';
import {
  Cloud, Agriculture, TrendingUp, Warning, CheckCircle, Info
} from '@mui/icons-material';
import { useApp } from '../context/AppContext';

const WeatherPlanning = () => {
  const { dropdownData } = useApp();
  const [formData, setFormData] = useState({
    district: '',
    currentSeason: '',
    soilType: '',
    irrigationAvailable: ''
  });
  const [recommendations, setRecommendations] = useState(null);

  const seasons = [
    { value: 'Monsoon', label: 'Monsoon (June-Sept)', icon: '🌧️' },
    { value: 'Post-Monsoon', label: 'Post-Monsoon (Oct-Nov)', icon: '🍂' },
    { value: 'Winter', label: 'Winter (Dec-Feb)', icon: '❄️' },
    { value: 'Summer', label: 'Summer (Mar-May)', icon: '☀️' }
  ];

  const irrigationOptions = [
    { value: 'Yes', label: 'Yes - Irrigation Available' },
    { value: 'No', label: 'No - Rain-fed Only' },
    { value: 'Limited', label: 'Limited - Partial Irrigation' }
  ];

  // Weather-based crop recommendations for Maharashtra
  const getRecommendations = () => {
    const { district, currentSeason, soilType, irrigationAvailable } = formData;
    
    const recommendations = {
      'Monsoon': {
        'Black': {
          rainfed: ['Cotton', 'Soybean', 'Sorghum', 'Bajra'],
          irrigated: ['Cotton', 'Soybean', 'Sugarcane', 'Rice', 'Maize']
        },
        'Red': {
          rainfed: ['Bajra', 'Groundnut', 'Pulses'],
          irrigated: ['Cotton', 'Maize', 'Vegetables']
        },
        'Sandy': {
          rainfed: ['Bajra', 'Groundnut', 'Pulses'],
          irrigated: ['Watermelon', 'Vegetables', 'Groundnut']
        },
        'Clay': {
          rainfed: ['Rice', 'Sorghum'],
          irrigated: ['Rice', 'Sugarcane', 'Cotton']
        },
        'Loamy': {
          rainfed: ['Maize', 'Soybean', 'Cotton'],
          irrigated: ['Maize', 'Cotton', 'Vegetables', 'Sugarcane']
        }
      },
      'Post-Monsoon': {
        'Black': {
          rainfed: ['Chickpea', 'Wheat', 'Sorghum'],
          irrigated: ['Wheat', 'Chickpea', 'Vegetables']
        },
        'Red': {
          rainfed: ['Pulses', 'Sorghum'],
          irrigated: ['Wheat', 'Vegetables', 'Sunflower']
        },
        'Sandy': {
          rainfed: ['Bajra', 'Pulses'],
          irrigated: ['Wheat', 'Vegetables']
        },
        'Clay': {
          rainfed: ['Wheat', 'Gram'],
          irrigated: ['Wheat', 'Sugarcane', 'Vegetables']
        },
        'Loamy': {
          rainfed: ['Wheat', 'Chickpea'],
          irrigated: ['Wheat', 'Potato', 'Vegetables']
        }
      },
      'Winter': {
        'Black': {
          rainfed: ['Wheat', 'Gram', 'Mustard'],
          irrigated: ['Wheat', 'Potato', 'Onion', 'Vegetables']
        },
        'Red': {
          rainfed: ['Wheat', 'Mustard'],
          irrigated: ['Wheat', 'Vegetables', 'Flowers']
        },
        'Sandy': {
          rainfed: ['Mustard', 'Coriander'],
          irrigated: ['Vegetables', 'Wheat']
        },
        'Clay': {
          rainfed: ['Wheat', 'Gram'],
          irrigated: ['Wheat', 'Sugarcane', 'Vegetables']
        },
        'Loamy': {
          rainfed: ['Wheat', 'Chickpea', 'Mustard'],
          irrigated: ['Wheat', 'Potato', 'Tomato', 'Cabbage']
        }
      },
      'Summer': {
        'Black': {
          rainfed: ['Keep Fallow', 'Green Manure Crops'],
          irrigated: ['Groundnut', 'Sunflower', 'Watermelon', 'Cucumber']
        },
        'Red': {
          rainfed: ['Keep Fallow', 'Pulses'],
          irrigated: ['Groundnut', 'Vegetables', 'Sunflower']
        },
        'Sandy': {
          rainfed: ['Groundnut (if moisture)', 'Keep Fallow'],
          irrigated: ['Watermelon', 'Groundnut', 'Vegetables']
        },
        'Clay': {
          rainfed: ['Keep Fallow', 'Summer Ploughing'],
          irrigated: ['Rice', 'Vegetables']
        },
        'Loamy': {
          rainfed: ['Groundnut (if moisture)', 'Green Manure'],
          irrigated: ['Groundnut', 'Watermelon', 'Cucumber', 'Vegetables']
        }
      }
    };

    const irrigationType = irrigationAvailable === 'Yes' ? 'irrigated' : 'rainfed';
    const crops = recommendations[currentSeason]?.[soilType]?.[irrigationType] || [];

    // Weather-specific tips
    const seasonTips = {
      'Monsoon': {
        general: 'Prepare fields before monsoon onset. Ensure proper drainage to prevent waterlogging.',
        irrigation: irrigationAvailable === 'Yes' 
          ? 'Utilize stored water for supplementary irrigation during dry spells.' 
          : 'Select drought-tolerant varieties. Implement rainwater harvesting.',
        risks: 'Watch for excess rainfall, pest attacks, and fungal diseases.',
        actions: ['Sow immediately after first good rainfall', 'Apply pre-monsoon fertilizers', 'Prepare bunds and drainage channels']
      },
      'Post-Monsoon': {
        general: 'Utilize residual soil moisture. Select short-duration varieties.',
        irrigation: irrigationAvailable === 'Yes'
          ? 'Plan efficient irrigation schedule. Conserve water for critical growth stages.'
          : 'Choose crops with low water requirements. Practice mulching.',
        risks: 'Decreasing moisture, early termination of monsoon, pest build-up.',
        actions: ['Sow immediately post-monsoon', 'Apply organic manure', 'Practice conservation agriculture']
      },
      'Winter': {
        general: 'Optimal temperature for Rabi crops. Ensure timely sowing for maximum yield.',
        irrigation: irrigationAvailable === 'Yes'
          ? 'Light irrigation at critical stages. Avoid over-watering in cool weather.'
          : 'Select moisture-conserving practices. Choose low-water crops.',
        risks: 'Cold waves, frost damage, low temperature stress.',
        actions: ['Protect crops from frost', 'Apply nitrogen in splits', 'Weed management essential']
      },
      'Summer': {
        general: 'High temperature and water stress. Consider keeping land fallow for soil restoration.',
        irrigation: irrigationAvailable === 'Yes'
          ? 'Grow high-value crops with drip irrigation. Mulching essential.'
          : 'Prefer keeping fallow. Practice summer ploughing to conserve moisture.',
        risks: 'Heat stress, water scarcity, low market rates due to glut.',
        actions: ['Use mulching extensively', 'Drip irrigation for efficiency', 'Grow green manure if not cultivating']
      }
    };

    const tips = seasonTips[currentSeason];

    // Zone-specific advice
    const zoneInfo = getZoneInfo(district);

    return {
      crops,
      tips,
      zoneInfo,
      irrigationType
    };
  };

  const getZoneInfo = (district) => {
    const zones = {
      'Konkan': { rainfall: 'High (2000-3000mm)', climate: 'Humid, high rainfall zone' },
      'Vidarbha': { rainfall: 'Moderate (800-1200mm)', climate: 'Semi-arid, hot summers' },
      'Marathwada': { rainfall: 'Low (600-900mm)', climate: 'Drought-prone, water scarce' },
      'Western_Maharashtra': { rainfall: 'Moderate (500-700mm)', climate: 'Diverse, sugarcane belt' },
      'North_Maharashtra': { rainfall: 'Moderate (600-800mm)', climate: 'Cotton and banana belt' }
    };

    for (const [zone, districts] of Object.entries({
      'Konkan': ['Thane', 'Palghar', 'Raigad', 'Ratnagiri', 'Sindhudurg'],
      'Vidarbha': ['Nagpur', 'Amravati', 'Akola', 'Yavatmal', 'Buldhana', 'Washim', 'Wardha', 'Chandrapur', 'Bhandara', 'Gadchiroli', 'Gondia'],
      'Marathwada': ['Aurangabad', 'Jalna', 'Beed', 'Latur', 'Osmanabad', 'Nanded', 'Parbhani', 'Hingoli'],
      'Western_Maharashtra': ['Pune', 'Satara', 'Sangli', 'Kolhapur', 'Solapur'],
      'North_Maharashtra': ['Nashik', 'Dhule', 'Jalgaon', 'Nandurbar', 'Ahmednagar']
    })) {
      if (districts.includes(district)) {
        return { zone, ...zones[zone] };
      }
    }
    return { zone: 'Unknown', rainfall: 'Variable', climate: 'Diverse' };
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const result = getRecommendations();
    setRecommendations(result);
  };

  const handleReset = () => {
    setFormData({
      district: '',
      currentSeason: '',
      soilType: '',
      irrigationAvailable: ''
    });
    setRecommendations(null);
  };

  return (
    <Container maxWidth="lg">
      <Typography variant="h4" gutterBottom sx={{ fontWeight: 700 }}>
        🌦️ Smart Weather-Based Crop Planning
      </Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
        Get personalized crop recommendations based on your location, season, soil type, and irrigation availability
      </Typography>

      <Grid container spacing={4}>
        {/* Input Form */}
        <Grid item xs={12} md={4}>
          <Card sx={{ position: 'sticky', top: 80 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, display: 'flex', alignItems: 'center', gap: 1 }}>
                <Agriculture /> Your Farm Details
              </Typography>
              
              <Box component="form" onSubmit={handleSubmit} sx={{ mt: 3 }}>
                <TextField
                  fullWidth
                  select
                  label="Select Your District"
                  value={formData.district}
                  onChange={(e) => setFormData({...formData, district: e.target.value})}
                  margin="normal"
                  required
                >
                  {dropdownData.districts.map((d) => (
                    <MenuItem key={d} value={d}>{d}</MenuItem>
                  ))}
                </TextField>

                <TextField
                  fullWidth
                  select
                  label="Current/Planning Season"
                  value={formData.currentSeason}
                  onChange={(e) => setFormData({...formData, currentSeason: e.target.value})}
                  margin="normal"
                  required
                >
                  {seasons.map((s) => (
                    <MenuItem key={s.value} value={s.value}>
                      {s.icon} {s.label}
                    </MenuItem>
                  ))}
                </TextField>

                <TextField
                  fullWidth
                  select
                  label="Soil Type"
                  value={formData.soilType}
                  onChange={(e) => setFormData({...formData, soilType: e.target.value})}
                  margin="normal"
                  required
                >
                  {dropdownData.soil_types.map((s) => (
                    <MenuItem key={s} value={s}>{s}</MenuItem>
                  ))}
                </TextField>

                <TextField
                  fullWidth
                  select
                  label="Irrigation Availability"
                  value={formData.irrigationAvailable}
                  onChange={(e) => setFormData({...formData, irrigationAvailable: e.target.value})}
                  margin="normal"
                  required
                >
                  {irrigationOptions.map((opt) => (
                    <MenuItem key={opt.value} value={opt.value}>{opt.label}</MenuItem>
                  ))}
                </TextField>

                <Box sx={{ mt: 3, display: 'flex', gap: 1 }}>
                  <Button 
                    type="submit" 
                    variant="contained" 
                    fullWidth
                  >
                    Get Recommendations
                  </Button>
                  {recommendations && (
                    <Button 
                      variant="outlined" 
                      onClick={handleReset}
                    >
                      Reset
                    </Button>
                  )}
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Results */}
        <Grid item xs={12} md={8}>
          {recommendations ? (
            <>
              {/* Zone Information */}
              <Alert severity="info" icon={<Info />} sx={{ mb: 3 }}>
                <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
                  {recommendations.zoneInfo.zone} Zone
                </Typography>
                <Typography variant="body2">
                  <strong>Rainfall:</strong> {recommendations.zoneInfo.rainfall} | <strong>Climate:</strong> {recommendations.zoneInfo.climate}
                </Typography>
              </Alert>

              {/* Recommended Crops */}
              <Card sx={{ mb: 3 }}>
                <CardContent>
                  <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, display: 'flex', alignItems: 'center', gap: 1 }}>
                    <CheckCircle color="success" /> Recommended Crops
                  </Typography>
                  <Chip 
                    label={recommendations.irrigationType === 'irrigated' ? 'Irrigated Farming' : 'Rain-fed Farming'}
                    color={recommendations.irrigationType === 'irrigated' ? 'primary' : 'warning'}
                    size="small"
                    sx={{ mb: 2 }}
                  />
                  <Grid container spacing={2}>
                    {recommendations.crops.map((crop, index) => (
                      <Grid item xs={6} sm={4} key={index}>
                        <Paper 
                          elevation={0}
                          sx={{ 
                            p: 2, 
                            textAlign: 'center', 
                            backgroundColor: '#f5f5f5',
                            border: '2px solid #e0e0e0',
                            '&:hover': { borderColor: '#4caf50', backgroundColor: '#f1f8f4' }
                          }}
                        >
                          <Typography variant="h6" sx={{ fontSize: 28 }}>
                            🌾
                          </Typography>
                          <Typography variant="body2" sx={{ fontWeight: 600 }}>
                            {crop}
                          </Typography>
                        </Paper>
                      </Grid>
                    ))}
                  </Grid>
                </CardContent>
              </Card>

              {/* Season-Specific Tips */}
              <Card sx={{ mb: 3, background: 'linear-gradient(135deg, #1976d2 0%, #42a5f5 100%)', color: 'white' }}>
                <CardContent>
                  <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                    💡 Season-Specific Insights
                  </Typography>
                  <Typography variant="body2" sx={{ mb: 2 }}>
                    {recommendations.tips.general}
                  </Typography>
                  <Typography variant="body2" sx={{ fontWeight: 600, mb: 1 }}>
                    Irrigation Strategy:
                  </Typography>
                  <Typography variant="body2">
                    {recommendations.tips.irrigation}
                  </Typography>
                </CardContent>
              </Card>

              {/* Risk Alerts */}
              <Card sx={{ mb: 3, borderLeft: '4px solid #ff9800' }}>
                <CardContent>
                  <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, display: 'flex', alignItems: 'center', gap: 1, color: '#f57c00' }}>
                    <Warning /> Potential Risks to Watch
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {recommendations.tips.risks}
                  </Typography>
                </CardContent>
              </Card>

              {/* Action Items */}
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, display: 'flex', alignItems: 'center', gap: 1 }}>
                    <TrendingUp /> Key Action Points
                  </Typography>
                  {recommendations.tips.actions.map((action, index) => (
                    <Box key={index} sx={{ display: 'flex', alignItems: 'flex-start', mb: 1.5 }}>
                      <Chip 
                        label={index + 1} 
                        size="small" 
                        color="primary" 
                        sx={{ minWidth: 28, height: 24, mr: 1.5 }}
                      />
                      <Typography variant="body2" color="text.secondary">
                        {action}
                      </Typography>
                    </Box>
                  ))}
                </CardContent>
              </Card>
            </>
          ) : (
            <Card sx={{ minHeight: 500, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <CardContent sx={{ textAlign: 'center' }}>
                <Cloud sx={{ fontSize: 80, color: 'primary.main', opacity: 0.3, mb: 2 }} />
                <Typography variant="h6" color="text.secondary" gutterBottom>
                  Plan Your Crops Smartly
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Fill in your farm details to get personalized weather-based crop recommendations
                </Typography>
              </CardContent>
            </Card>
          )}
        </Grid>
      </Grid>
    </Container>
  );
};

export default WeatherPlanning;
