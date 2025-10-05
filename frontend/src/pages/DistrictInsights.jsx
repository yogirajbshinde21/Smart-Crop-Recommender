import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import {
  Container, Grid, Card, CardContent, Typography, Box, TextField,
  MenuItem, CircularProgress, Alert
} from '@mui/material';
import { LocationOn } from '@mui/icons-material';
import { Bar, Pie } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, ArcElement, Title, Tooltip, Legend } from 'chart.js';
import { useApp } from '../context/AppContext';
import { getDistrictInsights } from '../services/api';
import { Translate } from '../components/Translate';
import { useTranslation } from '../context/TranslationContext';

ChartJS.register(CategoryScale, LinearScale, BarElement, ArcElement, Title, Tooltip, Legend);

const DistrictInsights = () => {
  const { district } = useParams();
  const { dropdownData } = useApp();
  const { t } = useTranslation();
  const [selectedDistrict, setSelectedDistrict] = useState(district || '');
  const [loading, setLoading] = useState(false);
  const [insights, setInsights] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (selectedDistrict) {
      loadInsights(selectedDistrict);
    }
  }, [selectedDistrict]);

  const loadInsights = async (districtName) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await getDistrictInsights(districtName);
      if (response.success) setInsights(response.data);
      else setError(response.error);
    } catch (err) {
      setError(t('district.errorLoad'));
    } finally {
      setLoading(false);
    }
  };

  const getSoilChartData = () => {
    if (!insights) return null;
    const labels = Object.keys(insights.soil_distribution);
    const data = Object.values(insights.soil_distribution);
    
    return {
      labels,
      datasets: [{
        label: t('district.soilDistribution'),
        data,
        backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40', '#FF6384']
      }]
    };
  };

  const getCropChartData = () => {
    if (!insights) return null;
    const labels = Object.keys(insights.popular_crops).slice(0, 10);
    const data = Object.values(insights.popular_crops).slice(0, 10);
    
    return {
      labels,
      datasets: [{
        label: 'Crop Frequency',
        data,
        backgroundColor: '#4caf50'
      }]
    };
  };

  return (
    <Container maxWidth="lg">
      <Typography variant="h4" gutterBottom sx={{ fontWeight: 700, mb: 4 }}>
        📊 District Insights
      </Typography>

      <Card sx={{ mb: 4 }}>
        <CardContent>
          <TextField
            fullWidth
            select
            label="Select District"
            value={selectedDistrict}
            onChange={(e) => setSelectedDistrict(e.target.value)}
          >
            {dropdownData.districts.map((d) => (
              <MenuItem key={d} value={d}>{d}</MenuItem>
            ))}
          </TextField>
        </CardContent>
      </Card>

      {loading && (
        <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
          <CircularProgress />
          <Typography sx={{ ml: 2 }}><Translate tKey="district.loading" /></Typography>
        </Box>
      )}

      {error && <Alert severity="error">{error}</Alert>}

      {insights && !loading && (
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Card sx={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white' }}>
              <CardContent>
                <Typography variant="h4" gutterBottom sx={{ fontWeight: 700 }}>
                  {insights.district}
                </Typography>
                <Typography variant="h6" sx={{ mb: 2 }}>{insights.zone} Zone</Typography>
                <Grid container spacing={2}>
                  <Grid item xs={12} md={6}>
                    <Typography variant="body2"><strong>Climate:</strong> {insights.zone_characteristics.climate}</Typography>
                    <Typography variant="body2"><strong>Rainfall:</strong> {insights.zone_characteristics.rainfall}</Typography>
                  </Grid>
                  <Grid item xs={12} md={6}>
                    <Typography variant="body2"><strong>Irrigation:</strong> {insights.zone_characteristics.irrigation}</Typography>
                    <Typography variant="body2"><strong>Total Records:</strong> {insights.total_records}</Typography>
                  </Grid>
                </Grid>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                  Average Nutrient Requirements
                </Typography>
                <Grid container spacing={2}>
                  {Object.entries(insights.average_nutrients).map(([key, value]) => (
                    <Grid item xs={6} key={key}>
                      <Box sx={{ p: 2, backgroundColor: '#f5f5f5', borderRadius: 2, textAlign: 'center' }}>
                        <Typography variant="h5" sx={{ fontWeight: 700, color: 'primary.main' }}>
                          {value}
                        </Typography>
                        <Typography variant="caption">{key}</Typography>
                      </Box>
                    </Grid>
                  ))}
                </Grid>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                  Water Quality Stats
                </Typography>
                <Box sx={{ display: 'grid', gap: 2 }}>
                  <Box sx={{ p: 2, backgroundColor: '#e3f2fd', borderRadius: 2 }}>
                    <Typography variant="body2" color="text.secondary">Average pH</Typography>
                    <Typography variant="h5" sx={{ fontWeight: 700, color: '#1976d2' }}>
                      {insights.water_quality.avg_pH}
                    </Typography>
                  </Box>
                  <Box sx={{ p: 2, backgroundColor: '#f3e5f5', borderRadius: 2 }}>
                    <Typography variant="body2" color="text.secondary">Avg Turbidity</Typography>
                    <Typography variant="h5" sx={{ fontWeight: 700, color: '#9c27b0' }}>
                      {insights.water_quality.avg_turbidity} NTU
                    </Typography>
                  </Box>
                  <Box sx={{ p: 2, backgroundColor: '#fff3e0', borderRadius: 2 }}>
                    <Typography variant="body2" color="text.secondary">Avg Temperature</Typography>
                    <Typography variant="h5" sx={{ fontWeight: 700, color: '#ff6f00' }}>
                      {insights.water_quality.avg_temp}°C
                    </Typography>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                  Soil Type Distribution
                </Typography>
                {getSoilChartData() && (
                  <Box sx={{ height: 250 }}>
                    <Pie data={getSoilChartData()} options={{ maintainAspectRatio: false }} />
                  </Box>
                )}
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                  Popular Crops
                </Typography>
                {getCropChartData() && (
                  <Box sx={{ height: 250 }}>
                    <Bar data={getCropChartData()} options={{ maintainAspectRatio: false, indexAxis: 'y' }} />
                  </Box>
                )}
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}
    </Container>
  );
};

export default DistrictInsights;
