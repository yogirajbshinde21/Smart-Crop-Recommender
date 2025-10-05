import React, { useState } from 'react';
import {
  Container,
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  TextField,
  Button,
  MenuItem,
  CircularProgress,
  Alert,
  Chip,
  LinearProgress
} from '@mui/material';
import {
  Agriculture,
  TrendingUp,
  Landscape,
  WbSunny,
  CheckCircle
} from '@mui/icons-material';
import { useApp } from '../context/AppContext';
import { recommendCrop } from '../services/api';
import { Translate } from '../components/Translate';
import { useTranslation } from '../context/TranslationContext';

const CropRecommendation = () => {
  const { dropdownData } = useApp();
  const { t } = useTranslation();
  const [formData, setFormData] = useState({
    District: '',
    Soil_Type: '',
    Weather: ''
  });
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
    setError(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.District || !formData.Soil_Type || !formData.Weather) {
      setError(t('crop.errorFillFields'));
      return;
    }

    setLoading(true);
    setError(null);
    
    try {
      const response = await recommendCrop(formData);
      if (response.success) {
        setResults(response.data);
      } else {
        setError(response.error || t('crop.errorServer'));
      }
    } catch (err) {
      setError(t('crop.errorServer'));
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setFormData({
      District: '',
      Soil_Type: '',
      Weather: ''
    });
    setResults(null);
    setError(null);
  };

  const CropCard = ({ crop, rank }) => {
    const getRankColor = () => {
      if (rank === 1) return '#FFD700';
      if (rank === 2) return '#C0C0C0';
      return '#CD7F32';
    };

    const getRankLabel = () => {
      if (rank === 1) return `🥇 ${t('crop.bestMatch')}`;
      if (rank === 2) return `🥈 ${t('crop.goodMatch')}`;
      return `🥉 ${t('crop.alternative')}`;
    };

    return (
      <Card 
        sx={{ 
          height: '100%',
          border: rank === 1 ? '3px solid #FFD700' : '1px solid #e0e0e0',
          transition: 'all 0.3s',
          '&:hover': { 
            transform: 'translateY(-8px)', 
            boxShadow: 6 
          }
        }}
      >
        <CardContent>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
            <Chip
              label={getRankLabel()}
              sx={{ 
                backgroundColor: getRankColor(),
                color: 'white',
                fontWeight: 600
              }}
            />
            <Agriculture sx={{ fontSize: 40, color: 'primary.main', opacity: 0.3 }} />
          </Box>

          <Typography variant="h5" gutterBottom sx={{ fontWeight: 700, color: 'primary.main' }}>
            {crop.crop_name}
          </Typography>

          <Box sx={{ mb: 2 }}>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              <Translate tKey="crop.confidence" />
            </Typography>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
              <LinearProgress
                variant="determinate"
                value={crop.confidence}
                sx={{ 
                  flex: 1, 
                  height: 10, 
                  borderRadius: 5,
                  backgroundColor: '#e0e0e0',
                  '& .MuiLinearProgress-bar': {
                    backgroundColor: crop.confidence > 60 ? '#4caf50' : crop.confidence > 40 ? '#ff9800' : '#f44336'
                  }
                }}
              />
              <Typography variant="h6" sx={{ fontWeight: 700, minWidth: 60 }}>
                {crop.confidence}%
              </Typography>
            </Box>
          </Box>

          <Box sx={{ display: 'grid', gap: 1.5 }}>
            <Box>
              <Typography variant="caption" color="text.secondary">
                <Translate tKey="crop.yieldPotential" />
              </Typography>
              <Typography variant="body1" sx={{ fontWeight: 600 }}>
                {crop.avg_yield} {t('units.quintalsPerHa')}
              </Typography>
            </Box>
            
            <Box>
              <Typography variant="caption" color="text.secondary">
                Market Rate
              </Typography>
              <Typography variant="body1" sx={{ fontWeight: 600 }}>
                ₹{crop.market_rate}/Quintal
              </Typography>
            </Box>

            <Box>
              <Typography variant="caption" color="text.secondary">
                Suitable Zone
              </Typography>
              <Chip
                label={crop.suitable_for_zone}
                size="small"
                color="primary"
                variant="outlined"
              />
            </Box>
          </Box>

          {rank === 1 && (
            <Box sx={{ mt: 2, p: 1.5, backgroundColor: '#e8f5e9', borderRadius: 2 }}>
              <Typography variant="caption" sx={{ color: '#2e7d32', fontWeight: 600, display: 'flex', alignItems: 'center', gap: 0.5 }}>
                <CheckCircle sx={{ fontSize: 16 }} /> Recommended for your conditions
              </Typography>
            </Box>
          )}
        </CardContent>
      </Card>
    );
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" gutterBottom sx={{ fontWeight: 700 }}>
          🌱 <Translate tKey="crop.title" />
        </Typography>
        <Typography variant="body1" color="text.secondary">
          <Translate tKey="crop.subtitle" />
        </Typography>
      </Box>

      <Grid container spacing={4}>
        {/* Input Form */}
        <Grid item xs={12} md={4}>
          <Card sx={{ position: 'sticky', top: 80 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, display: 'flex', alignItems: 'center', gap: 1 }}>
                <Agriculture /> <Translate tKey="crop.inputParams" />
              </Typography>
              
              <Box component="form" onSubmit={handleSubmit} sx={{ mt: 3 }}>
                <TextField
                  fullWidth
                  select
                  label={t('crop.district')}
                  name="District"
                  value={formData.District}
                  onChange={handleInputChange}
                  margin="normal"
                  required
                  InputProps={{
                    startAdornment: <Landscape sx={{ mr: 1, color: 'action.active' }} />
                  }}
                >
                  {dropdownData.districts.map((district) => (
                    <MenuItem key={district} value={district}>
                      {district}
                    </MenuItem>
                  ))}
                </TextField>

                <TextField
                  fullWidth
                  select
                  label={t('crop.soilType')}
                  name="Soil_Type"
                  value={formData.Soil_Type}
                  onChange={handleInputChange}
                  margin="normal"
                  required
                >
                  {dropdownData.soil_types.map((soil) => (
                    <MenuItem key={soil} value={soil}>
                      {soil}
                    </MenuItem>
                  ))}
                </TextField>

                <TextField
                  fullWidth
                  select
                  label={t('crop.weather')}
                  name="Weather"
                  value={formData.Weather}
                  onChange={handleInputChange}
                  margin="normal"
                  required
                  InputProps={{
                    startAdornment: <WbSunny sx={{ mr: 1, color: 'action.active' }} />
                  }}
                >
                  {dropdownData.weather_conditions.map((weather) => (
                    <MenuItem key={weather} value={weather}>
                      {weather}
                    </MenuItem>
                  ))}
                </TextField>

                {error && (
                  <Alert severity="error" sx={{ mt: 2 }}>
                    {error}
                  </Alert>
                )}

                <Box sx={{ mt: 3, display: 'flex', gap: 2 }}>
                  <Button
                    type="submit"
                    variant="contained"
                    fullWidth
                    disabled={loading}
                    sx={{ py: 1.5 }}
                  >
                    {loading ? <CircularProgress size={24} /> : <Translate tKey="crop.getRecommendations" />}
                  </Button>
                  <Button
                    variant="outlined"
                    onClick={handleReset}
                    disabled={loading}
                  >
                    <Translate tKey="crop.reset" />
                  </Button>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Results */}
        <Grid item xs={12} md={8}>
          {results ? (
            <>
              {/* Zone Information */}
              <Card sx={{ mb: 3, background: 'linear-gradient(135deg, #2e7d32 0%, #4caf50 100%)', color: 'white' }}>
                <CardContent>
                  <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                    {results.zone} Zone
                  </Typography>
                  <Typography variant="body2" sx={{ opacity: 0.95 }}>
                    <strong>Climate:</strong> {results.zone_info.climate}
                  </Typography>
                  <Typography variant="body2" sx={{ opacity: 0.95 }}>
                    <strong>Rainfall:</strong> {results.zone_info.rainfall}
                  </Typography>
                  <Typography variant="body2" sx={{ opacity: 0.95 }}>
                    <strong>Major Crops:</strong> {results.zone_info.major_crops?.join(', ')}
                  </Typography>
                </CardContent>
              </Card>

              {/* Recommendations */}
              <Typography variant="h5" gutterBottom sx={{ fontWeight: 600, mb: 2 }}>
                <Translate tKey="crop.recommended" />
              </Typography>
              
              {/* No Data Message */}
              {results.no_data_message && (
                <Alert 
                  severity="warning" 
                  sx={{ mb: 3 }}
                  icon={<Agriculture />}
                >
                  <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                    {results.no_data_message.title}
                  </Typography>
                  <Typography variant="body2" paragraph>
                    {results.no_data_message.reason}
                  </Typography>
                  {results.no_data_message.district_info && (
                    <Typography variant="body2" paragraph>
                      ℹ️ {results.no_data_message.district_info}
                    </Typography>
                  )}
                  <Typography variant="body2" sx={{ fontWeight: 600, mt: 2 }}>
                    💡 {results.no_data_message.suggestion}
                  </Typography>
                  
                  {results.no_data_message.available_soils && (
                    <Box sx={{ mt: 2 }}>
                      <Typography variant="body2" sx={{ fontWeight: 600, mb: 1 }}>
                        Available soil types in {results.input.district}:
                      </Typography>
                      <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                        {results.no_data_message.available_soils.map((soil) => (
                          <Chip 
                            key={soil} 
                            label={soil} 
                            size="small"
                            color="primary"
                            variant="outlined"
                          />
                        ))}
                      </Box>
                    </Box>
                  )}
                  
                  {results.suitable_combinations && results.suitable_combinations.length > 0 && (
                    <Box sx={{ mt: 3 }}>
                      <Typography variant="body2" sx={{ fontWeight: 600, mb: 2 }}>
                        Suitable combinations for {results.input.district}:
                      </Typography>
                      <Grid container spacing={2}>
                        {results.suitable_combinations.map((combo, idx) => (
                          <Grid item xs={12} sm={6} key={idx}>
                            <Card variant="outlined" sx={{ p: 1.5, bgcolor: 'success.50' }}>
                              <Typography variant="body2" sx={{ fontWeight: 600 }}>
                                {combo.soil_type} + {combo.weather}
                              </Typography>
                              <Typography variant="caption" color="text.secondary">
                                Suitable crops: {combo.crops.join(', ')}
                              </Typography>
                            </Card>
                          </Grid>
                        ))}
                      </Grid>
                    </Box>
                  )}
                </Alert>
              )}
              
              <Grid container spacing={3}>
                {results.recommendations.map((crop, index) => (
                  <Grid item xs={12} key={crop.crop_name}>
                    <CropCard crop={crop} rank={index + 1} />
                  </Grid>
                ))}
              </Grid>

              {/* Input Summary */}
              <Card sx={{ mt: 3, backgroundColor: '#f5f5f5' }}>
                <CardContent>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    <strong>Analysis based on:</strong>
                  </Typography>
                  <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap', mt: 1 }}>
                    <Chip label={`District: ${results.input.district}`} size="small" />
                    <Chip label={`Soil: ${results.input.soil_type}`} size="small" />
                    <Chip label={`Weather: ${results.input.weather}`} size="small" />
                  </Box>
                </CardContent>
              </Card>
            </>
          ) : (
            <Card sx={{ minHeight: 400, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <CardContent sx={{ textAlign: 'center' }}>
                <Agriculture sx={{ fontSize: 80, color: 'primary.main', opacity: 0.3, mb: 2 }} />
                <Typography variant="h6" color="text.secondary">
                  Select parameters to get crop recommendations
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                  Our AI model will analyze your inputs and suggest the best crops for your conditions
                </Typography>
              </CardContent>
            </Card>
          )}
        </Grid>
      </Grid>
    </Container>
  );
};

export default CropRecommendation;
