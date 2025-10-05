import React, { useState } from 'react';
import {
  Container, Grid, Card, CardContent, Typography, Box, TextField, Button,
  MenuItem, CircularProgress, Alert, Chip, Divider
} from '@mui/material';
import { CompareArrows, TrendingUp, TrendingDown } from '@mui/icons-material';
import { useApp } from '../context/AppContext';
import { compareCrops } from '../services/api';
import { Translate } from '../components/Translate';
import { useTranslation } from '../context/TranslationContext';

const CropComparison = () => {
  const { dropdownData } = useApp();
  const { t } = useTranslation();
  const [formData, setFormData] = useState({
    crops: ['', '', ''],
    District: '',
    Soil_Type: '',
    Weather: ''
  });
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const handleCropChange = (index, value) => {
    const newCrops = [...formData.crops];
    newCrops[index] = value;
    setFormData({ ...formData, crops: newCrops });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const validCrops = formData.crops.filter(c => c !== '');
    
    if (validCrops.length < 2) {
      setError(t('comparison.errorMinCrops'));
      return;
    }

    setLoading(true);
    setError(null);
    
    try {
      const response = await compareCrops({
        crops: validCrops,
        District: formData.District,
        Soil_Type: formData.Soil_Type,
        Weather: formData.Weather
      });
      if (response.success) setResults(response.data);
      else setError(response.error);
    } catch (err) {
      setError(t('common.error'));
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="lg">
      <Typography variant="h4" gutterBottom sx={{ fontWeight: 700, mb: 1 }}>
        <Translate tKey="comparison.title" />
      </Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
        <Translate tKey="comparison.subtitle" />
      </Typography>

      <Grid container spacing={4}>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                <Translate tKey="comparison.selectCrops" />
              </Typography>
              <Box component="form" onSubmit={handleSubmit}>
                {[0, 1, 2].map((index) => (
                  <TextField
                    key={index}
                    fullWidth
                    select
                    label={`${t('comparison.crop')} ${index + 1}${index < 2 ? ' *' : ''}`}
                    value={formData.crops[index]}
                    onChange={(e) => handleCropChange(index, e.target.value)}
                    margin="normal"
                    required={index < 2}
                  >
                    <MenuItem value="">{t('common.select')}</MenuItem>
                    {dropdownData.crops.map((c) => (
                      <MenuItem key={c} value={c} disabled={formData.crops.includes(c) && formData.crops[index] !== c}>
                        {c}
                      </MenuItem>
                    ))}
                  </TextField>
                ))}
                
                <Divider sx={{ my: 2 }} />
                
                <TextField fullWidth select label={t('crop.district')} value={formData.District}
                  onChange={(e) => setFormData({...formData, District: e.target.value})} margin="normal" required>
                  {dropdownData.districts.map((d) => <MenuItem key={d} value={d}>{d}</MenuItem>)}
                </TextField>
                
                <TextField fullWidth select label={t('crop.soilType')} value={formData.Soil_Type}
                  onChange={(e) => setFormData({...formData, Soil_Type: e.target.value})} margin="normal" required>
                  {dropdownData.soil_types.map((s) => <MenuItem key={s} value={s}>{s}</MenuItem>)}
                </TextField>
                
                <TextField fullWidth select label={t('crop.weather')} value={formData.Weather}
                  onChange={(e) => setFormData({...formData, Weather: e.target.value})} margin="normal" required>
                  {dropdownData.weather_conditions.map((w) => <MenuItem key={w} value={w}>{w}</MenuItem>)}
                </TextField>

                {error && <Alert severity="error" sx={{ mt: 2 }}>{error}</Alert>}
                <Button type="submit" variant="contained" fullWidth disabled={loading} sx={{ mt: 3 }}>
                  {loading ? <CircularProgress size={24} /> : <Translate tKey="comparison.comparison" />}
                </Button>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={8}>
          {results ? (
            <>
              {results.recommendation && (
                <Alert severity="success" icon={<TrendingUp />} sx={{ mb: 3 }}>
                  <Typography variant="body1" sx={{ fontWeight: 600 }}>
                    Best Crop: {results.recommendation.best_crop}
                  </Typography>
                  <Typography variant="body2">
                    {results.recommendation.reason}
                  </Typography>
                </Alert>
              )}

              <Grid container spacing={3}>
                {results.comparison.map((crop) => (
                  <Grid item xs={12} key={crop.crop_name}>
                    <Card sx={{ border: crop.crop_name === results.recommendation?.best_crop ? '2px solid #4caf50' : 'none' }}>
                      <CardContent>
                        <Typography variant="h5" gutterBottom sx={{ fontWeight: 700, color: 'primary.main' }}>
                          {crop.crop_name}
                          {crop.crop_name === results.recommendation?.best_crop && (
                            <Chip label="Recommended" color="success" size="small" sx={{ ml: 2 }} />
                          )}
                        </Typography>

                        <Grid container spacing={3} sx={{ mt: 1 }}>
                          <Grid item xs={12} md={4}>
                            <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                              Economic Analysis
                            </Typography>
                            <Box sx={{ display: 'grid', gap: 1 }}>
                              <Box>
                                <Typography variant="caption">Total Cost</Typography>
                                <Typography variant="body1" sx={{ fontWeight: 600 }}>₹{crop.economics.total_cost}/ha</Typography>
                              </Box>
                              <Box>
                                <Typography variant="caption">Net Income</Typography>
                                <Typography variant="body1" sx={{ fontWeight: 600, color: crop.economics.net_income > 0 ? 'success.main' : 'error.main' }}>
                                  ₹{crop.economics.net_income}/ha
                                </Typography>
                              </Box>
                              <Box>
                                <Typography variant="caption">ROI</Typography>
                                <Typography variant="h6" sx={{ fontWeight: 700, color: 'primary.main' }}>
                                  {crop.economics.roi_percentage}%
                                </Typography>
                              </Box>
                            </Box>
                          </Grid>

                          <Grid item xs={12} md={4}>
                            <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                              Nutrient Requirements
                            </Typography>
                            <Box sx={{ display: 'grid', gap: 0.5 }}>
                              <Typography variant="body2">N: {crop.nutrients.N} kg/ha</Typography>
                              <Typography variant="body2">P: {crop.nutrients.P} kg/ha</Typography>
                              <Typography variant="body2">K: {crop.nutrients.K} kg/ha</Typography>
                              <Typography variant="body2">Zn: {crop.nutrients.Zn} kg/ha</Typography>
                              <Typography variant="body2">S: {crop.nutrients.S} kg/ha</Typography>
                            </Box>
                          </Grid>

                          <Grid item xs={12} md={4}>
                            <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                              Risk Assessment
                            </Typography>
                            <Chip 
                              label={`${crop.risk_assessment.risk_level} Risk`}
                              color={crop.risk_assessment.risk_level === 'Low' ? 'success' : crop.risk_assessment.risk_level === 'Medium' ? 'warning' : 'error'}
                              sx={{ mb: 1 }}
                            />
                            <Typography variant="body2">Water: {crop.risk_assessment.water_requirement}</Typography>
                            <Typography variant="body2">Zone: {crop.risk_assessment.zone_suitability}</Typography>
                          </Grid>
                        </Grid>
                      </CardContent>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            </>
          ) : (
            <Card sx={{ minHeight: 400, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <CardContent sx={{ textAlign: 'center' }}>
                <CompareArrows sx={{ fontSize: 80, color: 'primary.main', opacity: 0.3, mb: 2 }} />
                <Typography variant="h6" color="text.secondary">
                  Select crops and parameters to compare
                </Typography>
              </CardContent>
            </Card>
          )}
        </Grid>
      </Grid>
    </Container>
  );
};

export default CropComparison;
