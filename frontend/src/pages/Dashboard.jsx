import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  Button,
  Chip,
  CircularProgress,
  Alert
} from '@mui/material';
import {
  Agriculture,
  LocationOn,
  WbSunny,
  TrendingUp,
  Dashboard as DashboardIcon,
  Science,
  Place,
  Cloud,
  AttachMoney
} from '@mui/icons-material';
import { useApp } from '../context/AppContext';
import { getStatistics } from '../services/api';
import Translate from '../components/Translate';

const Dashboard = () => {
  const navigate = useNavigate();
  const { dropdownData, loading, apiStatus } = useApp();
  const [stats, setStats] = useState(null);
  const [loadingStats, setLoadingStats] = useState(true);

  useEffect(() => {
    loadStatistics();
  }, []);

  const loadStatistics = async () => {
    try {
      const response = await getStatistics();
      if (response.success) {
        setStats(response.data);
      }
    } catch (error) {
      console.error('Failed to load statistics:', error);
    } finally {
      setLoadingStats(false);
    }
  };

  const StatCard = ({ title, value, icon, color, description }) => (
    <Card sx={{ height: '100%', transition: 'all 0.3s', '&:hover': { transform: 'translateY(-4px)', boxShadow: 4 } }}>
      <CardContent>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
          <Box>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              {title}
            </Typography>
            <Typography variant="h4" sx={{ fontWeight: 700, color }}>
              {value}
            </Typography>
          </Box>
          <Box
            sx={{
              backgroundColor: `${color}15`,
              borderRadius: 2,
              p: 1.5,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}
          >
            {icon}
          </Box>
        </Box>
        {description && (
          <Typography variant="caption" color="text.secondary">
            {description}
          </Typography>
        )}
      </CardContent>
    </Card>
  );

  const FeatureCard = ({ title, description, icon, path, color }) => (
    <Card sx={{ height: '100%', cursor: 'pointer', transition: 'all 0.3s', '&:hover': { transform: 'translateY(-4px)', boxShadow: 6 } }} onClick={() => navigate(path)}>
      <CardContent>
        <Box
          sx={{
            backgroundColor: `${color}15`,
            borderRadius: 2,
            p: 2,
            display: 'inline-flex',
            mb: 2
          }}
        >
          {React.cloneElement(icon, { sx: { fontSize: 40, color } })}
        </Box>
        <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
          {title}
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
          {description}
        </Typography>
        <Button variant="contained" size="small" sx={{ backgroundColor: color }}>
          <Translate>dashboard.getStarted</Translate>
        </Button>
      </CardContent>
    </Card>
  );

  if (loading || loadingStats) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '60vh' }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Container maxWidth="lg">
      {/* Hero Section */}
      <Box
        sx={{
          background: 'linear-gradient(135deg, #2e7d32 0%, #4caf50 100%)',
          borderRadius: 3,
          p: 4,
          mb: 4,
          color: 'white',
          position: 'relative',
          overflow: 'hidden'
        }}
      >
        <Box sx={{ position: 'relative', zIndex: 1 }}>
          <Typography variant="h3" gutterBottom sx={{ fontWeight: 700 }}>
            🌾 <Translate as="span">dashboard.hero.title</Translate>
          </Typography>
          <Typography variant="h6" sx={{ mb: 2, opacity: 0.95 }}>
            <Translate as="span">dashboard.hero.subtitle</Translate>
          </Typography>
          <Typography variant="body1" sx={{ mb: 3, maxWidth: 700, opacity: 0.9 }}>
            <Translate as="span">dashboard.hero.description</Translate>
          </Typography>
          <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
            <Button
              variant="contained"
              size="large"
              sx={{ backgroundColor: 'white', color: 'primary.main', '&:hover': { backgroundColor: '#f5f5f5' } }}
              onClick={() => navigate('/crop-recommendation')}
            >
              <Translate>dashboard.hero.recommendCrops</Translate>
            </Button>
            <Button
              variant="outlined"
              size="large"
              sx={{ borderColor: 'white', color: 'white', '&:hover': { borderColor: 'white', backgroundColor: 'rgba(255,255,255,0.1)' } }}
              onClick={() => navigate('/crop-comparison')}
            >
              <Translate>dashboard.hero.compareCrops</Translate>
            </Button>
          </Box>
        </Box>
      </Box>

      {/* API Status Alert */}
      {apiStatus !== 'connected' && (
        <Alert severity="warning" sx={{ mb: 3 }}>
          <Translate>dashboard.alert.apiDisconnected</Translate>
        </Alert>
      )}

      {/* Statistics Cards */}
      {stats && (
        <Grid container spacing={3} sx={{ mb: 4 }}>
          <Grid item xs={12} sm={6} md={3}>
            <StatCard
              title={<Translate>dashboard.stats.totalDistricts</Translate>}
              value={stats.total_districts}
              icon={<LocationOn sx={{ fontSize: 32, color: '#1976d2' }} />}
              color="#1976d2"
              description={<Translate>dashboard.stats.districtsDesc</Translate>}
            />
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <StatCard
              title={<Translate>dashboard.stats.cropVarieties</Translate>}
              value={stats.total_crops}
              icon={<Agriculture sx={{ fontSize: 32, color: '#2e7d32' }} />}
              color="#2e7d32"
              description={<Translate>dashboard.stats.cropsDesc</Translate>}
            />
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <StatCard
              title={<Translate>dashboard.stats.soilTypes</Translate>}
              value={stats.total_soil_types}
              icon={<Science sx={{ fontSize: 32, color: '#ed6c02' }} />}
              color="#ed6c02"
              description={<Translate>dashboard.stats.soilDesc</Translate>}
            />
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <StatCard
              title={<Translate>dashboard.stats.weatherConditions</Translate>}
              value={stats.total_weather_conditions}
              icon={<WbSunny sx={{ fontSize: 32, color: '#f57c00' }} />}
              color="#f57c00"
              description={<Translate>dashboard.stats.weatherDesc</Translate>}
            />
          </Grid>
        </Grid>
      )}

      {/* Agricultural Zones */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h5" gutterBottom sx={{ fontWeight: 600, mb: 2 }}>
          <Translate>dashboard.zones.title</Translate>
        </Typography>
        <Grid container spacing={2}>
          {[
            { name: 'dashboard.zones.konkan', districts: 6, color: '#1e88e5', crops: 'dashboard.zones.konkan.crops' },
            { name: 'dashboard.zones.vidarbha', districts: 11, color: '#f57c00', crops: 'dashboard.zones.vidarbha.crops' },
            { name: 'dashboard.zones.marathwada', districts: 8, color: '#d32f2f', crops: 'dashboard.zones.marathwada.crops' },
            { name: 'dashboard.zones.westernMaharashtra', districts: 5, color: '#7cb342', crops: 'dashboard.zones.western.crops' },
            { name: 'dashboard.zones.northMaharashtra', districts: 5, color: '#8e24aa', crops: 'dashboard.zones.north.crops' },
          ].map((zone) => (
            <Grid item xs={12} sm={6} md={4} key={zone.name}>
              <Card sx={{ background: `linear-gradient(135deg, ${zone.color} 0%, ${zone.color}dd 100%)`, color: 'white' }}>
                <CardContent>
                  <Typography variant="h6" sx={{ fontWeight: 600, mb: 1 }}>
                    <Translate>{zone.name}</Translate>
                  </Typography>
                  <Typography variant="body2" sx={{ mb: 1, opacity: 0.9 }}>
                    {zone.districts} <Translate as="span">dashboard.zones.districts</Translate>
                  </Typography>
                  <Typography variant="caption" sx={{ opacity: 0.8 }}>
                    <Translate as="span">dashboard.zones.keyCrops</Translate>: <Translate as="span">{zone.crops}</Translate>
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Box>

      {/* Feature Cards */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h5" gutterBottom sx={{ fontWeight: 600, mb: 2 }}>
          <Translate>dashboard.features.title</Translate>
        </Typography>
        <Grid container spacing={3}>
          <Grid item xs={12} sm={6} md={4}>
            <FeatureCard
              title={<Translate>dashboard.features.cropRec.title</Translate>}
              description={<Translate>dashboard.features.cropRec.desc</Translate>}
              icon={<Agriculture />}
              path="/crop-recommendation"
              color="#2e7d32"
            />
          </Grid>
          <Grid item xs={12} sm={6} md={4}>
            <FeatureCard
              title={<Translate>dashboard.features.nutrient.title</Translate>}
              description={<Translate>dashboard.features.nutrient.desc</Translate>}
              icon={<Science />}
              path="/nutrient-analysis"
              color="#1976d2"
            />
          </Grid>
          <Grid item xs={12} sm={6} md={4}>
            <FeatureCard
              title={<Translate>dashboard.features.comparison.title</Translate>}
              description={<Translate>dashboard.features.comparison.desc</Translate>}
              icon={<TrendingUp />}
              path="/crop-comparison"
              color="#f57c00"
            />
          </Grid>
          <Grid item xs={12} sm={6} md={4}>
            <FeatureCard
              title={<Translate>dashboard.features.district.title</Translate>}
              description={<Translate>dashboard.features.district.desc</Translate>}
              icon={<Place />}
              path="/district-insights"
              color="#9c27b0"
            />
          </Grid>
          <Grid item xs={12} sm={6} md={4}>
            <FeatureCard
              title={<Translate>dashboard.features.weather.title</Translate>}
              description={<Translate>dashboard.features.weather.desc</Translate>}
              icon={<Cloud />}
              path="/weather-planning"
              color="#00acc1"
            />
          </Grid>
          <Grid item xs={12} sm={6} md={4}>
            <FeatureCard
              title={<Translate>dashboard.features.economic.title</Translate>}
              description={<Translate>dashboard.features.economic.desc</Translate>}
              icon={<AttachMoney />}
              path="/economic-analysis"
              color="#43a047"
            />
          </Grid>
        </Grid>
      </Box>

      {/* Data Overview */}
      {stats && (
        <Card sx={{ mb: 4, backgroundColor: '#f5f5f5' }}>
          <CardContent>
            <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
              <Translate>dashboard.system.title</Translate>
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <Typography variant="body2" color="text.secondary">
                  <Translate as="span">dashboard.system.totalRecords</Translate>: <strong>{stats.total_records}</strong>
                </Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography variant="body2" color="text.secondary">
                  <Translate as="span">dashboard.system.mlModels</Translate>: <strong>3 <Translate as="span">dashboard.system.trainedModels</Translate></strong>
                </Typography>
              </Grid>
              <Grid item xs={12}>
                <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                  <Translate as="span">dashboard.system.algorithms</Translate>: <Translate as="span">dashboard.system.algorithmsValue</Translate>
                </Typography>
              </Grid>
            </Grid>
          </CardContent>
        </Card>
      )}
    </Container>
  );
};

export default Dashboard;
