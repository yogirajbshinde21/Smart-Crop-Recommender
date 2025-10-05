import React from 'react';
import { Container, Grid, Card, CardContent, Typography, Box, Chip } from '@mui/material';
import { Cloud, WbSunny, Grain } from '@mui/icons-material';
import { Translate } from '../components/Translate';
import { useTranslation } from '../context/TranslationContext';

const WeatherPlanning = () => {
  const { t } = useTranslation();
  
  const weatherSeasons = [
    {
      name: t('weather.monsoon'),
      months: t('weather.monthsJuneSept'),
      crops: ['Rice', 'Cotton', 'Soybean', 'Maize'],
      color: '#1976d2',
      icon: <Cloud />
    },
    {
      name: t('weather.postMonsoon'),
      months: t('weather.monthsOctNov'),
      crops: ['Wheat', 'Chickpea', 'Sorghum'],
      color: '#f57c00',
      icon: <WbSunny />
    },
    {
      name: t('weather.winter'),
      months: t('weather.monthsDecFeb'),
      crops: ['Wheat', 'Gram', 'Mustard'],
      color: '#0288d1',
      icon: <Grain />
    },
    {
      name: t('weather.summer'),
      months: t('weather.monthsMarMay'),
      crops: ['Groundnut', 'Sunflower', 'Vegetables'],
      color: '#ff6f00',
      icon: <WbSunny />
    }
  ];

  return (
    <Container maxWidth="lg">
      <Typography variant="h4" gutterBottom sx={{ fontWeight: 700, mb: 1 }}>
        🌡️ <Translate tKey="weather.title" />
      </Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
        <Translate tKey="weather.subtitle" />
      </Typography>

      <Grid container spacing={3}>
        {weatherSeasons.map((season) => (
          <Grid item xs={12} sm={6} key={season.name}>
            <Card sx={{ height: '100%', borderTop: `4px solid ${season.color}` }}>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                  <Box>
                    <Typography variant="h5" gutterBottom sx={{ fontWeight: 600 }}>
                      {season.name}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {season.months}
                    </Typography>
                  </Box>
                  <Box sx={{ color: season.color, fontSize: 40 }}>
                    {season.icon}
                  </Box>
                </Box>
                <Typography variant="subtitle2" gutterBottom sx={{ mt: 2 }}>
                  <Translate tKey="weather.recommendedCrops" />
                </Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                  {season.crops.map((crop) => (
                    <Chip key={crop} label={crop} size="small" sx={{ backgroundColor: `${season.color}20`, color: season.color }} />
                  ))}
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Card sx={{ mt: 4, background: 'linear-gradient(135deg, #2e7d32 0%, #4caf50 100%)', color: 'white' }}>
        <CardContent>
          <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
            💡 <Translate tKey="weather.planningTips" />
          </Typography>
          <Typography variant="body2" sx={{ mb: 1 }}>
            • <Translate tKey="weather.tip1" />
          </Typography>
          <Typography variant="body2" sx={{ mb: 1 }}>
            • <Translate tKey="weather.tip2" />
          </Typography>
          <Typography variant="body2" sx={{ mb: 1 }}>
            • <Translate tKey="weather.tip3" />
          </Typography>
          <Typography variant="body2">
            • <Translate tKey="weather.tip4" />
          </Typography>
        </CardContent>
      </Card>
    </Container>
  );
};

export default WeatherPlanning;
