import React, { useState } from 'react';
import {
  Container, Grid, Card, CardContent, Typography, Box, TextField, Button,
  MenuItem, CircularProgress, Alert, Chip
} from '@mui/material';
import { Science, TrendingUp } from '@mui/icons-material';
import { Radar } from 'react-chartjs-2';
import { Chart as ChartJS, RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend } from 'chart.js';
import { useApp } from '../context/AppContext';
import { predictNutrients } from '../services/api';
import { Translate } from '../components/Translate';
import { useTranslation } from '../context/TranslationContext';

ChartJS.register(RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend);

const NutrientAnalysis = () => {
  const { dropdownData } = useApp();
  const { t } = useTranslation();
  const [formData, setFormData] = useState({
    District: '',
    Soil_Type: '',
    Crop_Name: '',
    Weather: ''
  });
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setError(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.District || !formData.Soil_Type || !formData.Crop_Name || !formData.Weather) {
      setError(t('nutrient.errorFillFields'));
      return;
    }

    setLoading(true);
    setError(null);
    
    try {
      const response = await predictNutrients(formData);
      if (response.success) {
        setResults(response.data);
      } else {
        setError(response.error || t('nutrient.errorServer'));
      }
    } catch (err) {
      setError(t('nutrient.errorServer'));
    } finally {
      setLoading(false);
    }
  };

  const radarChartData = results ? {
    labels: ['Nitrogen (N)', 'Phosphorus (P)', 'Potassium (K)', 'Zinc (Zn)', 'Sulfur (S)'],
    datasets: [{
      label: 'Nutrient Requirements (kg/ha)',
      data: [
        results.nutrients.N_kg_ha,
        results.nutrients.P2O5_kg_ha,
        results.nutrients.K2O_kg_ha,
        results.nutrients.Zn_kg_ha,
        results.nutrients.S_kg_ha
      ],
      backgroundColor: 'rgba(46, 125, 50, 0.2)',
      borderColor: 'rgba(46, 125, 50, 1)',
      borderWidth: 2,
      pointBackgroundColor: 'rgba(46, 125, 50, 1)',
      pointBorderColor: '#fff',
      pointHoverBackgroundColor: '#fff',
      pointHoverBorderColor: 'rgba(46, 125, 50, 1)'
    }]
  } : null;

  return (
    <Container maxWidth="lg">
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" gutterBottom sx={{ fontWeight: 700 }}>
          🔬 <Translate tKey="nutrient.title" />
        </Typography>
        <Typography variant="body1" color="text.secondary">
          <Translate tKey="nutrient.subtitle" />
        </Typography>
      </Box>

      <Grid container spacing={4}>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                <Translate tKey="nutrient.inputParams" />
              </Typography>
              
              <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2 }}>
                <TextField fullWidth select label={t('nutrient.district')} name="District" value={formData.District}
                  onChange={handleInputChange} margin="normal" required>
                  {dropdownData.districts.map((d) => <MenuItem key={d} value={d}>{d}</MenuItem>)}
                </TextField>

                <TextField fullWidth select label={t('nutrient.soilType')} name="Soil_Type" value={formData.Soil_Type}
                  onChange={handleInputChange} margin="normal" required>
                  {dropdownData.soil_types.map((s) => <MenuItem key={s} value={s}>{s}</MenuItem>)}
                </TextField>

                <TextField fullWidth select label={t('nutrient.crop')} name="Crop_Name" value={formData.Crop_Name}
                  onChange={handleInputChange} margin="normal" required>
                  {dropdownData.crops.map((c) => <MenuItem key={c} value={c}>{c}</MenuItem>)}
                </TextField>

                <TextField fullWidth select label={t('nutrient.weather')} name="Weather" value={formData.Weather}
                  onChange={handleInputChange} margin="normal" required>
                  {dropdownData.weather_conditions.map((w) => <MenuItem key={w} value={w}>{w}</MenuItem>)}
                </TextField>

                {error && <Alert severity="error" sx={{ mt: 2 }}>{error}</Alert>}

                <Button type="submit" variant="contained" fullWidth disabled={loading} sx={{ mt: 3, py: 1.5 }}>
                  {loading ? <CircularProgress size={24} /> : <Translate tKey="nutrient.predictNutrients" />}
                </Button>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={8}>
          {results ? (
            <>
              <Card sx={{ mb: 3 }}>
                <CardContent>
                  <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                    <Translate tKey="nutrient.requirements" />
                  </Typography>
                  <Grid container spacing={2} sx={{ mt: 1 }}>
                    {Object.entries(results.nutrients).map(([key, value]) => (
                      <Grid item xs={6} sm={4} key={key}>
                        <Box sx={{ p: 2, backgroundColor: '#f5f5f5', borderRadius: 2, textAlign: 'center' }}>
                          <Typography variant="h4" sx={{ fontWeight: 700, color: 'primary.main' }}>
                            {value}
                          </Typography>
                          <Typography variant="caption" color="text.secondary">
                            {key.replace('_kg_ha', '').toUpperCase()}
                          </Typography>
                        </Box>
                      </Grid>
                    ))}
                  </Grid>
                </CardContent>
              </Card>

              <Card sx={{ mb: 3 }}>
                <CardContent>
                  <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                    NPK Ratio
                  </Typography>
                  <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
                    <Chip label={`N: ${results.npk_ratio.N}%`} color="primary" sx={{ flex: 1, py: 2 }} />
                    <Chip label={`P: ${results.npk_ratio.P}%`} color="secondary" sx={{ flex: 1, py: 2 }} />
                    <Chip label={`K: ${results.npk_ratio.K}%`} color="success" sx={{ flex: 1, py: 2 }} />
                  </Box>
                </CardContent>
              </Card>

              {radarChartData && (
                <Card sx={{ mb: 3 }}>
                  <CardContent>
                    <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                      Nutrient Profile
                    </Typography>
                    <Box sx={{ height: 300, display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                      <Radar data={radarChartData} options={{ maintainAspectRatio: false }} />
                    </Box>
                  </CardContent>
                </Card>
              )}

              {results.alerts && results.alerts.length > 0 && (
                <Card>
                  <CardContent>
                    <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                      Alerts & Recommendations
                    </Typography>
                    {results.alerts.map((alert, index) => (
                      <Alert key={index} severity={alert.type} sx={{ mb: 1 }}>
                        <strong>{alert.nutrient}:</strong> {alert.message}
                      </Alert>
                    ))}
                  </CardContent>
                </Card>
              )}
            </>
          ) : (
            <Card sx={{ minHeight: 400, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <CardContent sx={{ textAlign: 'center' }}>
                <Science sx={{ fontSize: 80, color: 'primary.main', opacity: 0.3, mb: 2 }} />
                <Typography variant="h6" color="text.secondary">
                  <Translate tKey="nutrient.selectParams" />
                </Typography>
              </CardContent>
            </Card>
          )}
        </Grid>
      </Grid>
    </Container>
  );
};

export default NutrientAnalysis;
