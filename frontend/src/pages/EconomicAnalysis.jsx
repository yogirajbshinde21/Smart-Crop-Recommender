import React, { useState } from 'react';
import {
  Container, Grid, Card, CardContent, Typography, Box, TextField,
  MenuItem, Button, Alert
} from '@mui/material';
import { AttachMoney, TrendingUp } from '@mui/icons-material';
import { useApp } from '../context/AppContext';
import { Translate } from '../components/Translate';
import { useTranslation } from '../context/TranslationContext';

const EconomicAnalysis = () => {
  const { dropdownData } = useApp();
  const { t } = useTranslation();
  const [crop, setCrop] = useState('');
  const [area, setArea] = useState(1);

  const marketRates = {
    Cotton: 6500, Soybean: 4200, Rice: 3500, Wheat: 2500, Sugarcane: 300,
    Sorghum: 3000, Maize: 2200, Chickpea: 5500, Grapes: 8000, Pomegranate: 9000
  };

  const expectedYields = {
    Cotton: 18, Soybean: 25, Rice: 40, Wheat: 35, Sugarcane: 800,
    Sorghum: 30, Maize: 45, Chickpea: 20, Grapes: 200, Pomegranate: 150
  };

  const inputCosts = {
    seeds: 3000, fertilizer: 1400, labor: 15000, irrigation: 8000, pesticides: 5000
  };

  const calculateEconomics = () => {
    if (!crop) return null;
    
    const yield_value = expectedYields[crop] || 25;
    const rate = marketRates[crop] || 3000;
    const totalInputCost = Object.values(inputCosts).reduce((a, b) => a + b, 0);
    
    const totalCost = totalInputCost * area;
    const grossIncome = yield_value * rate * area;
    const netIncome = grossIncome - totalCost;
    const roi = (netIncome / totalCost) * 100;
    
    return { totalCost, grossIncome, netIncome, roi, yield_value, rate };
  };

  const economics = calculateEconomics();

  return (
    <Container maxWidth="lg">
      <Typography variant="h4" gutterBottom sx={{ fontWeight: 700, mb: 4 }}>
        💰 <Translate tKey="economic.title" />
      </Typography>

      <Grid container spacing={4}>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                <Translate tKey="economic.inputParams" />
              </Typography>
              <TextField
                fullWidth
                select
                label={t('economic.selectCrop')}
                value={crop}
                onChange={(e) => setCrop(e.target.value)}
                margin="normal"
              >
                {dropdownData.crops.map((c) => (
                  <MenuItem key={c} value={c}>{c}</MenuItem>
                ))}
              </TextField>
              <TextField
                fullWidth
                type="number"
                label={t('economic.areaHectares')}
                value={area}
                onChange={(e) => setArea(Math.max(0.1, parseFloat(e.target.value) || 1))}
                margin="normal"
                inputProps={{ min: 0.1, step: 0.1 }}
              />
            </CardContent>
          </Card>

          <Card sx={{ mt: 3 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                <Translate tKey="economic.inputCosts" /> (<Translate tKey="economic.perHectare" />)
              </Typography>
              {Object.entries(inputCosts).map(([key, value]) => (
                <Box key={key} sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body2" sx={{ textTransform: 'capitalize' }}><Translate tKey={`economic.${key}`} /></Typography>
                  <Typography variant="body2" sx={{ fontWeight: 600 }}>₹{value}</Typography>
                </Box>
              ))}
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={8}>
          {economics ? (
            <>
              <Alert severity="success" icon={<TrendingUp />} sx={{ mb: 3 }}>
                <Typography variant="body1" sx={{ fontWeight: 600 }}>
                  <Translate tKey="economic.roi" />: {economics.roi.toFixed(2)}%
                </Typography>
                <Typography variant="body2">
                  {economics.netIncome > 0 ? t('economic.profitableVenture') : t('economic.considerAlternatives')}
                </Typography>
              </Alert>

              <Grid container spacing={3}>
                <Grid item xs={12} sm={6}>
                  <Card>
                    <CardContent>
                      <Typography variant="body2" color="text.secondary" gutterBottom>
                        <Translate tKey="economic.totalCost" />
                      </Typography>
                      <Typography variant="h4" sx={{ fontWeight: 700, color: 'primary.main' }}>
                        ₹{economics.totalCost.toLocaleString()}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Card>
                    <CardContent>
                      <Typography variant="body2" color="text.secondary" gutterBottom>
                        <Translate tKey="economic.grossIncome" />
                      </Typography>
                      <Typography variant="h4" sx={{ fontWeight: 700, color: 'success.main' }}>
                        ₹{economics.grossIncome.toLocaleString()}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Card>
                    <CardContent>
                      <Typography variant="body2" color="text.secondary" gutterBottom>
                        <Translate tKey="economic.netProfit" />
                      </Typography>
                      <Typography variant="h4" sx={{ fontWeight: 700, color: economics.netIncome > 0 ? 'success.main' : 'error.main' }}>
                        ₹{economics.netIncome.toLocaleString()}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Card>
                    <CardContent>
                      <Typography variant="body2" color="text.secondary" gutterBottom>
                        <Translate tKey="economic.returnOnInvestment" />
                      </Typography>
                      <Typography variant="h4" sx={{ fontWeight: 700, color: 'primary.main' }}>
                        {economics.roi.toFixed(2)}%
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
              </Grid>

              <Card sx={{ mt: 3 }}>
                <CardContent>
                  <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                    <Translate tKey="economic.assumptions" />
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    • <Translate tKey="economic.expectedYield" />: {economics.yield_value} <Translate tKey="economic.quintalPerHectare" />
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    • <Translate tKey="economic.marketRate" />: ₹{economics.rate}/<Translate tKey="economic.quintal" />
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    • <Translate tKey="economic.cultivationArea" />: {area} <Translate tKey="economic.hectares" />
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
                    <em><Translate tKey="economic.note" /></em>
                  </Typography>
                </CardContent>
              </Card>
            </>
          ) : (
            <Card sx={{ minHeight: 400, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <CardContent sx={{ textAlign: 'center' }}>
                <AttachMoney sx={{ fontSize: 80, color: 'primary.main', opacity: 0.3, mb: 2 }} />
                <Typography variant="h6" color="text.secondary">
                  <Translate tKey="economic.selectCropPrompt" />
                </Typography>
              </CardContent>
            </Card>
          )}
        </Grid>
      </Grid>
    </Container>
  );
};

export default EconomicAnalysis;
