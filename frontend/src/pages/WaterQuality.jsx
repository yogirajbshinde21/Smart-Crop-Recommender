import React, { useState } from 'react';
import {
  Container, Grid, Card, CardContent, Typography, Box, TextField, Button,
  MenuItem, CircularProgress, Alert, Chip
} from '@mui/material';
import { WaterDrop } from '@mui/icons-material';
import { useApp } from '../context/AppContext';
import { analyzeWaterQuality } from '../services/api';
import { Translate } from '../components/Translate';
import { useTranslation } from '../context/TranslationContext';

const WaterQuality = () => {
  const { dropdownData } = useApp();
  const { t } = useTranslation();
  const [formData, setFormData] = useState({ District: '', Weather: '', Soil_Type: '' });
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    
    try {
      const response = await analyzeWaterQuality(formData);
      if (response.success) setResults(response.data);
      else setError(response.error);
    } catch (err) {
      setError(t('water.errorServer'));
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="lg">
      <Typography variant="h4" gutterBottom sx={{ fontWeight: 700, mb: 4 }}>
        💧 <Translate tKey="water.title" />
      </Typography>

      <Grid container spacing={4}>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Box component="form" onSubmit={handleSubmit}>
                <TextField fullWidth select label={t('water.district')} name="District" value={formData.District}
                  onChange={(e) => setFormData({...formData, District: e.target.value})} margin="normal" required>
                  {dropdownData.districts.map((d) => <MenuItem key={d} value={d}>{d}</MenuItem>)}
                </TextField>
                <TextField fullWidth select label={t('water.weather')} name="Weather" value={formData.Weather}
                  onChange={(e) => setFormData({...formData, Weather: e.target.value})} margin="normal" required>
                  {dropdownData.weather_conditions.map((w) => <MenuItem key={w} value={w}>{w}</MenuItem>)}
                </TextField>
                <TextField fullWidth select label={t('water.soilType')} name="Soil_Type" value={formData.Soil_Type}
                  onChange={(e) => setFormData({...formData, Soil_Type: e.target.value})} margin="normal" required>
                  {dropdownData.soil_types.map((s) => <MenuItem key={s} value={s}>{s}</MenuItem>)}
                </TextField>
                {error && <Alert severity="error" sx={{ mt: 2 }}>{error}</Alert>}
                <Button type="submit" variant="contained" fullWidth disabled={loading} sx={{ mt: 3 }}>
                  {loading ? <CircularProgress size={24} /> : <Translate tKey="water.analyzeWater" />}
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
                    <Translate tKey="water.parameters" />
                  </Typography>
                  <Grid container spacing={2}>
                    <Grid item xs={12} sm={4}>
                      <Box sx={{ p: 3, backgroundColor: '#e3f2fd', borderRadius: 2, textAlign: 'center' }}>
                        <Typography variant="h3" sx={{ fontWeight: 700, color: '#1976d2' }}>
                          {results.water_parameters.recommended_pH}
                        </Typography>
                        <Typography variant="body2" color="text.secondary"><Translate tKey="water.phLevel" /></Typography>
                      </Box>
                    </Grid>
                    <Grid item xs={12} sm={4}>
                      <Box sx={{ p: 3, backgroundColor: '#f3e5f5', borderRadius: 2, textAlign: 'center' }}>
                        <Typography variant="h3" sx={{ fontWeight: 700, color: '#9c27b0' }}>
                          {results.water_parameters.turbidity_NTU}
                        </Typography>
                        <Typography variant="body2" color="text.secondary"><Translate tKey="water.turbidity" /></Typography>
                      </Box>
                    </Grid>
                    <Grid item xs={12} sm={4}>
                      <Box sx={{ p: 3, backgroundColor: '#fff3e0', borderRadius: 2, textAlign: 'center' }}>
                        <Typography variant="h3" sx={{ fontWeight: 700, color: '#ff6f00' }}>
                          {results.water_parameters.water_temp_C}°C
                        </Typography>
                        <Typography variant="body2" color="text.secondary"><Translate tKey="water.temperature" /></Typography>
                      </Box>
                    </Grid>
                  </Grid>
                </CardContent>
              </Card>

              <Grid container spacing={3}>
                {Object.entries(results.analysis).map(([key, value]) => (
                  <Grid item xs={12} md={4} key={key}>
                    <Card sx={{ height: '100%' }}>
                      <CardContent>
                        <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, textTransform: 'capitalize' }}>
                          {key}
                        </Typography>
                        <Chip label={value.status} color={value.status === 'Optimal' ? 'success' : 'warning'} sx={{ mb: 2 }} />
                        <Typography variant="body2" color="text.secondary">
                          {value.advice}
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            </>
          ) : (
            <Card sx={{ minHeight: 400, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <CardContent sx={{ textAlign: 'center' }}>
                <WaterDrop sx={{ fontSize: 80, color: 'primary.main', opacity: 0.3, mb: 2 }} />
                <Typography variant="h6" color="text.secondary">
                  <Translate tKey="water.selectParams" />
                </Typography>
              </CardContent>
            </Card>
          )}
        </Grid>
      </Grid>
    </Container>
  );
};

export default WaterQuality;
