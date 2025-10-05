import React, { useState, useEffect } from 'react';
import {
  Container, Grid, Card, CardContent, Typography, Box, TextField,
  MenuItem, Button, Alert, Chip, LinearProgress, Paper, Divider, Tabs, Tab
} from '@mui/material';
import {
  AttachMoney, TrendingUp, TrendingDown, Agriculture, LocalShipping,
  Store, WaterDrop, BugReport, Insights, BarChart, PieChart,
  ShowChart, Timeline, Warning, CheckCircle, Info
} from '@mui/icons-material';
import { useApp } from '../context/AppContext';
import { useTranslation } from '../context/TranslationContext';

const EconomicAnalysis = () => {
  const { dropdownData } = useApp();
  const { t } = useTranslation();
  const [crop, setCrop] = useState('');
  const [area, setArea] = useState(1);
  const [season, setSeason] = useState('Kharif');
  const [irrigationType, setIrrigationType] = useState('Drip');
  const [tabValue, setTabValue] = useState(0);

  // Comprehensive market data for Maharashtra crops
  const cropEconomicData = {
    Cotton: {
      marketRate: 6500,
      expectedYield: 18,
      seedCost: 3500,
      fertilizerCost: 18000,
      laborCost: 25000,
      irrigationCost: 12000,
      pesticideCost: 8000,
      transportCost: 2000,
      otherCosts: 3500,
      growthDuration: 150,
      waterRequirement: 700,
      riskLevel: 'Medium',
      demandTrend: 'Stable',
      exportPotential: 'High',
      governmentSupport: 'MSP: ₹6620/quintal',
      bestSeasons: ['Kharif'],
      priceVolatility: 'Medium',
      storageLife: 180
    },
    Soybean: {
      marketRate: 4200,
      expectedYield: 25,
      seedCost: 2500,
      fertilizerCost: 12000,
      laborCost: 18000,
      irrigationCost: 8000,
      pesticideCost: 6000,
      transportCost: 1500,
      otherCosts: 2500,
      growthDuration: 100,
      waterRequirement: 450,
      riskLevel: 'Low',
      demandTrend: 'Growing',
      exportPotential: 'High',
      governmentSupport: 'MSP: ₹4300/quintal',
      bestSeasons: ['Kharif'],
      priceVolatility: 'Low',
      storageLife: 365
    },
    Rice: {
      marketRate: 3500,
      expectedYield: 40,
      seedCost: 2000,
      fertilizerCost: 15000,
      laborCost: 22000,
      irrigationCost: 15000,
      pesticideCost: 5000,
      transportCost: 2000,
      otherCosts: 3000,
      growthDuration: 120,
      waterRequirement: 1200,
      riskLevel: 'Low',
      demandTrend: 'Stable',
      exportPotential: 'Medium',
      governmentSupport: 'MSP: ₹2183/quintal (Common)',
      bestSeasons: ['Kharif', 'Rabi'],
      priceVolatility: 'Low',
      storageLife: 365
    },
    Wheat: {
      marketRate: 2500,
      expectedYield: 35,
      seedCost: 2200,
      fertilizerCost: 14000,
      laborCost: 20000,
      irrigationCost: 10000,
      pesticideCost: 4500,
      transportCost: 1800,
      otherCosts: 2500,
      growthDuration: 120,
      waterRequirement: 450,
      riskLevel: 'Low',
      demandTrend: 'Stable',
      exportPotential: 'Low',
      governmentSupport: 'MSP: ₹2125/quintal',
      bestSeasons: ['Rabi'],
      priceVolatility: 'Very Low',
      storageLife: 365
    },
    Sugarcane: {
      marketRate: 300,
      expectedYield: 800,
      seedCost: 15000,
      fertilizerCost: 25000,
      laborCost: 45000,
      irrigationCost: 28000,
      pesticideCost: 8000,
      transportCost: 5000,
      otherCosts: 7000,
      growthDuration: 365,
      waterRequirement: 1800,
      riskLevel: 'High',
      demandTrend: 'Declining',
      exportPotential: 'Low',
      governmentSupport: 'FRP: ₹315/quintal',
      bestSeasons: ['Annual'],
      priceVolatility: 'High',
      storageLife: 7
    },
    Sorghum: {
      marketRate: 3000,
      expectedYield: 30,
      seedCost: 1500,
      fertilizerCost: 10000,
      laborCost: 16000,
      irrigationCost: 6000,
      pesticideCost: 4000,
      transportCost: 1500,
      otherCosts: 2000,
      growthDuration: 110,
      waterRequirement: 400,
      riskLevel: 'Low',
      demandTrend: 'Growing',
      exportPotential: 'Medium',
      governmentSupport: 'MSP: ₹3225/quintal',
      bestSeasons: ['Kharif', 'Rabi'],
      priceVolatility: 'Medium',
      storageLife: 180
    },
    Maize: {
      marketRate: 2200,
      expectedYield: 45,
      seedCost: 2800,
      fertilizerCost: 13000,
      laborCost: 19000,
      irrigationCost: 9000,
      pesticideCost: 5500,
      transportCost: 1800,
      otherCosts: 2500,
      growthDuration: 100,
      waterRequirement: 500,
      riskLevel: 'Low',
      demandTrend: 'Growing',
      exportPotential: 'Medium',
      governmentSupport: 'MSP: ₹2090/quintal',
      bestSeasons: ['Kharif', 'Rabi'],
      priceVolatility: 'Medium',
      storageLife: 180
    },
    Chickpea: {
      marketRate: 5500,
      expectedYield: 20,
      seedCost: 3000,
      fertilizerCost: 8000,
      laborCost: 17000,
      irrigationCost: 7000,
      pesticideCost: 5000,
      transportCost: 1500,
      otherCosts: 2500,
      growthDuration: 100,
      waterRequirement: 350,
      riskLevel: 'Medium',
      demandTrend: 'Stable',
      exportPotential: 'High',
      governmentSupport: 'MSP: ₹5335/quintal',
      bestSeasons: ['Rabi'],
      priceVolatility: 'High',
      storageLife: 365
    },
    Grapes: {
      marketRate: 8000,
      expectedYield: 200,
      seedCost: 80000,
      fertilizerCost: 45000,
      laborCost: 80000,
      irrigationCost: 35000,
      pesticideCost: 25000,
      transportCost: 8000,
      otherCosts: 15000,
      growthDuration: 150,
      waterRequirement: 600,
      riskLevel: 'High',
      demandTrend: 'Growing',
      exportPotential: 'Very High',
      governmentSupport: 'Export subsidy available',
      bestSeasons: ['Annual'],
      priceVolatility: 'Very High',
      storageLife: 30
    },
    Pomegranate: {
      marketRate: 9000,
      expectedYield: 150,
      seedCost: 50000,
      fertilizerCost: 35000,
      laborCost: 60000,
      irrigationCost: 25000,
      pesticideCost: 20000,
      transportCost: 6000,
      otherCosts: 12000,
      growthDuration: 180,
      waterRequirement: 800,
      riskLevel: 'High',
      demandTrend: 'Growing',
      exportPotential: 'Very High',
      governmentSupport: 'Export incentives',
      bestSeasons: ['Annual'],
      priceVolatility: 'High',
      storageLife: 60
    }
  };

  // Irrigation efficiency multipliers
  const irrigationEfficiency = {
    'Drip': { waterSaving: 0.5, costMultiplier: 1.2, yieldBonus: 1.15 },
    'Sprinkler': { waterSaving: 0.3, costMultiplier: 1.1, yieldBonus: 1.08 },
    'Flood': { waterSaving: 0, costMultiplier: 1.0, yieldBonus: 1.0 },
    'Rain-fed': { waterSaving: 0.8, costMultiplier: 0.7, yieldBonus: 0.85 }
  };

  const calculateDetailedEconomics = () => {
    if (!crop) return null;
    
    const cropData = cropEconomicData[crop];
    if (!cropData) return null;

    const irrigation = irrigationEfficiency[irrigationType];
    
    // Season-based adjustments
    const seasonFactors = {
      yieldMultiplier: 1.0,
      priceMultiplier: 1.0,
      laborCostMultiplier: 1.0,
      pesticideCostMultiplier: 1.0,
      irrigationCostMultiplier: 1.0
    };

    // Check if crop is suitable for the season
    const isOptimalSeason = cropData.bestSeasons.includes(season) || cropData.bestSeasons.includes('Annual');
    
    if (!isOptimalSeason) {
      // Off-season penalties
      seasonFactors.yieldMultiplier = 0.65;  // 35% yield reduction
      seasonFactors.laborCostMultiplier = 1.15;  // 15% higher labor costs
      seasonFactors.pesticideCostMultiplier = 1.25;  // 25% higher pesticide costs
      seasonFactors.irrigationCostMultiplier = 1.3;  // 30% higher irrigation costs
    } else {
      // Optimal season bonuses based on season type
      if (season === 'Kharif') {
        seasonFactors.yieldMultiplier = 1.1;  // Good monsoon yields
        seasonFactors.priceMultiplier = 1.05;  // Slightly better prices
        seasonFactors.irrigationCostMultiplier = 0.7;  // 30% lower irrigation (monsoon)
        seasonFactors.pesticideCostMultiplier = 1.15;  // Higher pest pressure
      } else if (season === 'Rabi') {
        seasonFactors.yieldMultiplier = 1.15;  // Best yields (winter)
        seasonFactors.priceMultiplier = 1.12;  // Better market prices
        seasonFactors.irrigationCostMultiplier = 1.1;  // Moderate irrigation needed
        seasonFactors.pesticideCostMultiplier = 0.85;  // Lower pest pressure
        seasonFactors.laborCostMultiplier = 1.08;  // Slightly higher labor availability issues
      } else if (season === 'Summer') {
        seasonFactors.yieldMultiplier = 0.85;  // Heat stress reduces yield
        seasonFactors.priceMultiplier = 1.25;  // Much higher prices (scarcity)
        seasonFactors.irrigationCostMultiplier = 1.4;  // 40% higher irrigation (heat)
        seasonFactors.pesticideCostMultiplier = 1.1;  // Moderate pest issues
        seasonFactors.laborCostMultiplier = 1.2;  // 20% higher labor costs (heat)
      } else if (season === 'Annual') {
        seasonFactors.yieldMultiplier = 1.0;  // Stable perennial crops
        seasonFactors.priceMultiplier = 1.0;  // Average prices
      }
    }
    
    // Calculate costs with all adjustments (irrigation + season)
    const seedCost = cropData.seedCost * area;
    const fertilizerCost = cropData.fertilizerCost * area;
    const laborCost = cropData.laborCost * area * seasonFactors.laborCostMultiplier;
    const irrigationCost = cropData.irrigationCost * area * irrigation.costMultiplier * seasonFactors.irrigationCostMultiplier;
    const pesticideCost = cropData.pesticideCost * area * seasonFactors.pesticideCostMultiplier;
    const transportCost = cropData.transportCost * area;
    const otherCosts = cropData.otherCosts * area;
    
    const totalInputCost = seedCost + fertilizerCost + laborCost + irrigationCost + 
                          pesticideCost + transportCost + otherCosts;
    
    // Calculate yield with irrigation and season bonuses
    const actualYield = cropData.expectedYield * irrigation.yieldBonus * seasonFactors.yieldMultiplier * area;
    
    // Calculate market rate with seasonal price variation
    const adjustedMarketRate = cropData.marketRate * seasonFactors.priceMultiplier;
    
    const grossIncome = actualYield * adjustedMarketRate;
    const netIncome = grossIncome - totalInputCost;
    const roi = (netIncome / totalInputCost) * 100;
    const profitPerHectare = netIncome / area;
    const breakEvenYield = totalInputCost / (adjustedMarketRate * area);
    const waterUsed = cropData.waterRequirement * area * (1 - irrigation.waterSaving);
    const waterCostEfficiency = netIncome / waterUsed;

    return {
      cropData,
      seasonFactors,
      isOptimalSeason,
      adjustedMarketRate,
      costs: {
        seed: seedCost,
        fertilizer: fertilizerCost,
        labor: laborCost,
        irrigation: irrigationCost,
        pesticide: pesticideCost,
        transport: transportCost,
        other: otherCosts,
        total: totalInputCost
      },
      revenue: {
        yield: actualYield,
        grossIncome,
        netIncome,
        roi,
        profitPerHectare,
        breakEvenYield,
        marginPerQuintal: netIncome / actualYield
      },
      efficiency: {
        waterUsed,
        waterCostEfficiency,
        yieldEfficiency: (actualYield / (cropData.expectedYield * area)) * 100,
        costPerQuintal: totalInputCost / actualYield
      }
    };
  };

  const economics = calculateDetailedEconomics();

  const getRiskColor = (risk) => {
    const colors = { 'Low': 'success', 'Medium': 'warning', 'High': 'error', 'Very High': 'error' };
    return colors[risk] || 'default';
  };

  const getTrendIcon = (trend) => {
    if (trend === 'Growing') return <TrendingUp sx={{ fontSize: 16 }} />;
    if (trend === 'Declining') return <TrendingDown sx={{ fontSize: 16 }} />;
    return <ShowChart sx={{ fontSize: 16 }} />;
  };

  const CostBreakdownChart = ({ costs }) => (
    <Box>
      {Object.entries(costs).filter(([key]) => key !== 'total').map(([key, value]) => {
        const percentage = (value / costs.total) * 100;
        return (
          <Box key={key} sx={{ mb: 2 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
              <Typography variant="body2" sx={{ textTransform: 'capitalize', fontWeight: 600 }}>
                {key === 'other' ? 'Miscellaneous' : key}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                ₹{value.toLocaleString()} ({percentage.toFixed(1)}%)
              </Typography>
            </Box>
            <LinearProgress
              variant="determinate"
              value={percentage}
              sx={{
                height: 8,
                borderRadius: 1,
                bgcolor: 'grey.200',
                '& .MuiLinearProgress-bar': {
                  bgcolor: key === 'labor' ? 'error.main' :
                          key === 'fertilizer' ? 'warning.main' :
                          key === 'irrigation' ? 'info.main' : 'primary.main'
                }
              }}
            />
          </Box>
        );
      })}
    </Box>
  );

  const InsightCard = ({ icon, title, value, subtitle, color = 'primary' }) => (
    <Card sx={{ 
      height: '100%', 
      bgcolor: `${color}.main`,
      color: 'white',
      boxShadow: 3
    }}>
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
          {icon}
          <Typography variant="body2" sx={{ ml: 1, fontWeight: 600 }}>
            {title}
          </Typography>
        </Box>
        <Typography variant="h4" sx={{ fontWeight: 700, mb: 0.5 }}>
          {value}
        </Typography>
        {subtitle && (
          <Typography variant="body2" sx={{ opacity: 0.95 }}>
            {subtitle}
          </Typography>
        )}
      </CardContent>
    </Card>
  );

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" gutterBottom sx={{ fontWeight: 700, display: 'flex', alignItems: 'center' }}>
          <Insights sx={{ fontSize: 40, mr: 2, color: 'primary.main' }} />
          {t('economic.smartTitle') || 'Smart Economic Analysis & Profitability Calculator'}
        </Typography>
        <Typography variant="body1" color="text.secondary">
          {t('economic.smartSubtitle') || 'Interactive tool to analyze crop economics, calculate ROI, and make data-driven farming decisions'}
        </Typography>
      </Box>

      <Grid container spacing={3}>
        {/* Input Panel */}
        <Grid item xs={12} lg={3}>
          <Card sx={{ position: 'sticky', top: 20 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, display: 'flex', alignItems: 'center' }}>
                <Agriculture sx={{ mr: 1 }} />
                {t('economic.farmParameters') || 'Farm Parameters'}
              </Typography>
              <Divider sx={{ my: 2 }} />
              
              <TextField
                fullWidth
                select
                label={t('economic.selectCrop') || 'Select Crop'}
                value={crop}
                onChange={(e) => setCrop(e.target.value)}
                margin="normal"
                variant="outlined"
              >
                {dropdownData.crops.map((c) => (
                  <MenuItem key={c} value={c}>{c}</MenuItem>
                ))}
              </TextField>

              <TextField
                fullWidth
                type="number"
                label={t('economic.cultivationArea') || 'Cultivation Area (hectares)'}
                value={area}
                onChange={(e) => setArea(Math.max(0.1, parseFloat(e.target.value) || 1))}
                margin="normal"
                inputProps={{ min: 0.1, step: 0.5 }}
                helperText={t('economic.enterFarmSize') || 'Enter your farm size'}
              />

              <TextField
                fullWidth
                select
                label={t('economic.season') || 'Season'}
                value={season}
                onChange={(e) => setSeason(e.target.value)}
                margin="normal"
              >
                <MenuItem value="Kharif">{t('economic.kharif') || 'Kharif (Monsoon)'}</MenuItem>
                <MenuItem value="Rabi">{t('economic.rabi') || 'Rabi (Winter)'}</MenuItem>
                <MenuItem value="Summer">{t('economic.summer') || 'Summer'}</MenuItem>
                <MenuItem value="Annual">{t('economic.annual') || 'Annual/Perennial'}</MenuItem>
              </TextField>

              <TextField
                fullWidth
                select
                label={t('economic.irrigationType') || 'Irrigation Type'}
                value={irrigationType}
                onChange={(e) => setIrrigationType(e.target.value)}
                margin="normal"
                helperText={t('economic.chooseIrrigation') || 'Choose your irrigation method'}
              >
                <MenuItem value="Drip">{t('economic.dripIrrigation') || 'Drip Irrigation (Most Efficient)'}</MenuItem>
                <MenuItem value="Sprinkler">{t('economic.sprinklerIrrigation') || 'Sprinkler Irrigation'}</MenuItem>
                <MenuItem value="Flood">{t('economic.floodIrrigation') || 'Flood/Traditional Irrigation'}</MenuItem>
                <MenuItem value="Rain-fed">{t('economic.rainfed') || 'Rain-fed (No Irrigation)'}</MenuItem>
              </TextField>

              {economics && (
                <Paper sx={{ mt: 3, p: 2, bgcolor: economics.revenue.netIncome > 0 ? 'success.light' : 'error.light' }}>
                  <Typography variant="body2" sx={{ fontWeight: 600, mb: 1 }}>
                    {t('economic.quickAssessment') || 'Quick Assessment'}
                  </Typography>
                  <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    {economics.revenue.netIncome > 0 ? (
                      <CheckCircle sx={{ color: 'success.dark', mr: 1 }} />
                    ) : (
                      <Warning sx={{ color: 'error.dark', mr: 1 }} />
                    )}
                    <Typography variant="body2">
                      {economics.revenue.netIncome > 0 
                        ? `${t('economic.profitableWith') || 'Profitable venture with'} ${economics.revenue.roi.toFixed(1)}% ${t('economic.roi') || 'ROI'}`
                        : t('economic.considerAlternatives') || 'Consider alternative crops or methods'
                      }
                    </Typography>
                  </Box>
                </Paper>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Results Panel */}
        <Grid item xs={12} lg={9}>
          {economics ? (
            <>
              {/* Key Metrics */}
              <Grid container spacing={2} sx={{ mb: 3 }}>
                <Grid item xs={6} md={3}>
                  <InsightCard
                    icon={<AttachMoney />}
                    title={t('economic.netProfit') || 'Net Profit'}
                    value={`₹${(economics.revenue.netIncome / 1000).toFixed(1)}K`}
                    subtitle={`₹${economics.revenue.profitPerHectare.toLocaleString()}/${t('economic.hectare') || 'hectare'}`}
                    color={economics.revenue.netIncome > 0 ? 'success' : 'error'}
                  />
                </Grid>
                <Grid item xs={6} md={3}>
                  <InsightCard
                    icon={<TrendingUp />}
                    title={t('economic.roi') || 'ROI'}
                    value={`${economics.revenue.roi.toFixed(1)}%`}
                    subtitle={economics.revenue.roi > 50 ? t('economic.excellentReturns') || 'Excellent returns' : economics.revenue.roi > 25 ? t('economic.goodReturns') || 'Good returns' : t('economic.moderateReturns') || 'Moderate returns'}
                    color="primary"
                  />
                </Grid>
                <Grid item xs={6} md={3}>
                  <InsightCard
                    icon={<Agriculture />}
                    title={t('economic.totalYield') || 'Total Yield'}
                    value={`${economics.revenue.yield.toFixed(1)}Q`}
                    subtitle={`${(economics.revenue.yield/area).toFixed(1)} ${t('economic.quintalsPerHectare') || 'quintals/hectare'}`}
                    color="info"
                  />
                </Grid>
                <Grid item xs={6} md={3}>
                  <InsightCard
                    icon={<WaterDrop />}
                    title={t('economic.waterEfficiency') || 'Water Efficiency'}
                    value={`₹${economics.efficiency.waterCostEfficiency.toFixed(0)}`}
                    subtitle={t('economic.profitPerWater') || 'Profit per mm water'}
                    color="secondary"
                  />
                </Grid>
              </Grid>

              {/* Tabs for detailed info */}
              <Card>
                <Tabs
                  value={tabValue}
                  onChange={(e, newValue) => setTabValue(newValue)}
                  variant="scrollable"
                  scrollButtons="auto"
                  sx={{ borderBottom: 1, borderColor: 'divider' }}
                >
                  <Tab icon={<BarChart />} label="Financial Analysis" iconPosition="start" />
                  <Tab icon={<PieChart />} label="Cost Breakdown" iconPosition="start" />
                  <Tab icon={<Timeline />} label="Market Intelligence" iconPosition="start" />
                  <Tab icon={<Insights />} label="Smart Recommendations" iconPosition="start" />
                </Tabs>

                <CardContent sx={{ p: 3 }}>
                  {/* Tab 1: Financial Analysis */}
                  {tabValue === 0 && (
                    <Grid container spacing={3}>
                      <Grid item xs={12} md={6}>
                        <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                          Revenue Analysis
                        </Typography>
                        <Paper sx={{ p: 2, bgcolor: 'success.lighter', mb: 2 }}>
                          <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                            <Typography variant="body2">Gross Income</Typography>
                            <Typography variant="body2" sx={{ fontWeight: 600 }}>
                              ₹{economics.revenue.grossIncome.toLocaleString()}
                            </Typography>
                          </Box>
                          <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                            <Typography variant="body2">Total Costs</Typography>
                            <Typography variant="body2" sx={{ fontWeight: 600, color: 'error.main' }}>
                              ₹{economics.costs.total.toLocaleString()}
                            </Typography>
                          </Box>
                          <Divider sx={{ my: 1 }} />
                          <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                            <Typography variant="body1" sx={{ fontWeight: 700 }}>Net Profit</Typography>
                            <Typography variant="body1" sx={{ fontWeight: 700, color: economics.revenue.netIncome > 0 ? 'success.dark' : 'error.main' }}>
                              ₹{economics.revenue.netIncome.toLocaleString()}
                            </Typography>
                          </Box>
                        </Paper>

                        <Typography variant="body2" color="text.secondary" paragraph>
                          • Expected yield: <strong>{economics.revenue.yield.toFixed(1)} quintals</strong> from {area} hectare(s)
                        </Typography>
                        <Typography variant="body2" color="text.secondary" paragraph>
                          • Market rate: <strong>₹{economics.adjustedMarketRate}/quintal</strong>
                          {economics.adjustedMarketRate !== economics.cropData.marketRate && (
                            <Chip 
                              label={`${((economics.adjustedMarketRate / economics.cropData.marketRate - 1) * 100).toFixed(0)}%`}
                              size="small"
                              color={economics.adjustedMarketRate > economics.cropData.marketRate ? 'success' : 'error'}
                              sx={{ ml: 1 }}
                            />
                          )}
                        </Typography>
                        <Typography variant="body2" color="text.secondary" paragraph>
                          • Margin per quintal: <strong>₹{economics.revenue.marginPerQuintal.toFixed(0)}</strong>
                        </Typography>
                        <Typography variant="body2" color="text.secondary" paragraph>
                          • Cost per quintal: <strong>₹{economics.efficiency.costPerQuintal.toFixed(0)}</strong>
                        </Typography>
                      </Grid>

                      <Grid item xs={12} md={6}>
                        <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                          Break-Even Analysis
                        </Typography>
                        <Paper sx={{ p: 2, bgcolor: 'warning.lighter', mb: 2 }}>
                          <Typography variant="body2" paragraph>
                            <strong>Break-even yield:</strong> {economics.revenue.breakEvenYield.toFixed(1)} quintals
                          </Typography>
                          <Typography variant="body2" paragraph>
                            <strong>Current yield:</strong> {economics.revenue.yield.toFixed(1)} quintals
                          </Typography>
                          <Typography variant="body2" paragraph>
                            <strong>Safety margin:</strong> {((economics.revenue.yield - economics.revenue.breakEvenYield) / economics.revenue.yield * 100).toFixed(1)}%
                          </Typography>
                          {economics.revenue.yield > economics.revenue.breakEvenYield ? (
                            <Alert severity="success" sx={{ mt: 1 }}>
                              You're {((economics.revenue.yield / economics.revenue.breakEvenYield - 1) * 100).toFixed(0)}% above break-even point
                            </Alert>
                          ) : (
                            <Alert severity="warning" sx={{ mt: 1 }}>
                              Need {(economics.revenue.breakEvenYield - economics.revenue.yield).toFixed(1)} more quintals to break even
                            </Alert>
                          )}
                        </Paper>

                        <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, mt: 3 }}>
                          Efficiency Metrics
                        </Typography>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                          <Typography variant="body2">Yield Efficiency</Typography>
                          <Chip
                            label={`${economics.efficiency.yieldEfficiency.toFixed(0)}%`}
                            size="small"
                            color={economics.efficiency.yieldEfficiency > 100 ? 'success' : 'warning'}
                          />
                        </Box>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                          <Typography variant="body2">Water Used</Typography>
                          <Typography variant="body2" sx={{ fontWeight: 600 }}>
                            {economics.efficiency.waterUsed.toFixed(0)} mm
                          </Typography>
                        </Box>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                          <Typography variant="body2">Growth Duration</Typography>
                          <Typography variant="body2" sx={{ fontWeight: 600 }}>
                            {economics.cropData.growthDuration} days
                          </Typography>
                        </Box>
                      </Grid>
                    </Grid>
                  )}

                  {/* Tab 2: Cost Breakdown */}
                  {tabValue === 1 && (
                    <Grid container spacing={3}>
                      <Grid item xs={12} md={8}>
                        <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                          Detailed Cost Breakdown
                        </Typography>
                        <CostBreakdownChart costs={economics.costs} />
                      </Grid>
                      <Grid item xs={12} md={4}>
                        <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                          Cost Summary
                        </Typography>
                        <Paper sx={{ p: 2, bgcolor: 'grey.50' }}>
                          <Typography variant="h5" sx={{ fontWeight: 700, color: 'primary.main', mb: 2 }}>
                            ₹{economics.costs.total.toLocaleString()}
                          </Typography>
                          <Typography variant="body2" color="text.secondary" paragraph>
                            Total investment required for {area} hectare(s) of {crop} cultivation
                          </Typography>
                          <Divider sx={{ my: 2 }} />
                          <Typography variant="body2" paragraph>
                            <strong>Cost per hectare:</strong><br />
                            ₹{(economics.costs.total / area).toLocaleString()}
                          </Typography>
                          <Typography variant="body2" paragraph>
                            <strong>Largest expense:</strong><br />
                            {Object.entries(economics.costs)
                              .filter(([key]) => key !== 'total')
                              .sort((a, b) => b[1] - a[1])[0][0]
                              .charAt(0).toUpperCase() + 
                              Object.entries(economics.costs)
                              .filter(([key]) => key !== 'total')
                              .sort((a, b) => b[1] - a[1])[0][0]
                              .slice(1)} (
                              {((Object.entries(economics.costs)
                                .filter(([key]) => key !== 'total')
                                .sort((a, b) => b[1] - a[1])[0][1] / economics.costs.total) * 100).toFixed(0)}%)
                          </Typography>
                          <Alert severity="info" sx={{ mt: 2 }}>
                            <Typography variant="body2">
                              Consider bulk purchase discounts and government subsidies to reduce input costs
                            </Typography>
                          </Alert>
                        </Paper>
                      </Grid>
                    </Grid>
                  )}

                  {/* Tab 3: Market Intelligence */}
                  {tabValue === 2 && (
                    <Grid container spacing={3}>
                      <Grid item xs={12} md={6}>
                        <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                          Market Indicators
                        </Typography>
                        
                        <Paper sx={{ p: 2, mb: 2 }}>
                          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                            <Typography variant="body2" color="text.secondary">Demand Trend</Typography>
                            <Box sx={{ display: 'flex', alignItems: 'center' }}>
                              {getTrendIcon(economics.cropData.demandTrend)}
                              <Typography variant="body1" sx={{ fontWeight: 600, ml: 1 }}>
                                {economics.cropData.demandTrend}
                              </Typography>
                            </Box>
                          </Box>
                          
                          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                            <Typography variant="body2" color="text.secondary">Price Volatility</Typography>
                            <Chip
                              label={economics.cropData.priceVolatility}
                              size="small"
                              color={economics.cropData.priceVolatility.includes('Low') ? 'success' : economics.cropData.priceVolatility === 'Medium' ? 'warning' : 'error'}
                            />
                          </Box>

                          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                            <Typography variant="body2" color="text.secondary">Export Potential</Typography>
                            <Chip
                              label={economics.cropData.exportPotential}
                              size="small"
                              color={economics.cropData.exportPotential.includes('High') ? 'success' : 'default'}
                            />
                          </Box>

                          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                            <Typography variant="body2" color="text.secondary">Risk Level</Typography>
                            <Chip
                              label={economics.cropData.riskLevel}
                              size="small"
                              color={getRiskColor(economics.cropData.riskLevel)}
                            />
                          </Box>
                        </Paper>

                        <Paper sx={{ p: 2, bgcolor: 'info.lighter' }}>
                          <Typography variant="body2" sx={{ fontWeight: 600, mb: 1 }}>
                            <Store sx={{ fontSize: 18, mr: 1, verticalAlign: 'middle' }} />
                            Storage Information
                          </Typography>
                          <Typography variant="body2">
                            Storage life: <strong>{economics.cropData.storageLife} days</strong>
                          </Typography>
                          {economics.cropData.storageLife < 30 && (
                            <Alert severity="warning" sx={{ mt: 1 }}>
                              Short storage life - plan for immediate sale or processing
                            </Alert>
                          )}
                        </Paper>
                      </Grid>

                      <Grid item xs={12} md={6}>
                        <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                          Government Support
                        </Typography>
                        <Paper sx={{ p: 2, bgcolor: 'success.lighter', mb: 2 }}>
                          <Typography variant="body1" sx={{ fontWeight: 600, mb: 1 }}>
                            {economics.cropData.governmentSupport}
                          </Typography>
                          <Typography variant="body2" color="text.secondary">
                            Ensure you register for government procurement schemes to get assured prices
                          </Typography>
                        </Paper>

                        <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                          Best Growing Seasons
                        </Typography>
                        <Box sx={{ mb: 2 }}>
                          {economics.cropData.bestSeasons.map((s) => (
                            <Chip
                              key={s}
                              label={s}
                              size="medium"
                              color={s === season ? 'primary' : 'default'}
                              sx={{ mr: 1, mb: 1 }}
                              icon={s === season ? <CheckCircle /> : undefined}
                            />
                          ))}
                        </Box>
                        {!economics.cropData.bestSeasons.includes(season) && season !== 'Annual' && (
                          <Alert severity="warning">
                            {crop} is not typically grown in {season} season. Consider seasonal alternatives for better yields.
                          </Alert>
                        )}

                        <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, mt: 3 }}>
                          Resource Requirements
                        </Typography>
                        <Paper sx={{ p: 2 }}>
                          <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                            <Typography variant="body2"><WaterDrop sx={{ fontSize: 16, verticalAlign: 'middle', mr: 0.5 }} />Water Requirement</Typography>
                            <Typography variant="body2" sx={{ fontWeight: 600 }}>
                              {economics.cropData.waterRequirement} mm
                            </Typography>
                          </Box>
                          <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                            <Typography variant="body2"><Timeline sx={{ fontSize: 16, verticalAlign: 'middle', mr: 0.5 }} />Growth Duration</Typography>
                            <Typography variant="body2" sx={{ fontWeight: 600 }}>
                              {economics.cropData.growthDuration} days
                            </Typography>
                          </Box>
                          <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mt: 2 }}>
                            Using {irrigationType} irrigation saves {(irrigationEfficiency[irrigationType].waterSaving * 100).toFixed(0)}% water
                          </Typography>
                        </Paper>
                      </Grid>
                    </Grid>
                  )}

                  {/* Tab 4: Smart Recommendations */}
                  {tabValue === 3 && (
                    <Box>
                      <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                        <Insights sx={{ verticalAlign: 'middle', mr: 1 }} />
                        Personalized Recommendations for Your Farm
                      </Typography>

                      <Grid container spacing={2} sx={{ mt: 1 }}>
                        {/* Season suitability alert */}
                        {!economics.isOptimalSeason && season !== 'Annual' && (
                          <Grid item xs={12}>
                            <Alert severity="error" icon={<Warning />}>
                              <Typography variant="body1" sx={{ fontWeight: 600 }}>
                                Wrong Season! Significant Yield & Profit Loss
                              </Typography>
                              <Typography variant="body2">
                                {crop} is NOT suitable for {season} season. You'll face:
                                • 35% lower yields • 15-30% higher costs • Increased pest/disease risk<br />
                                <strong>Best seasons:</strong> {economics.cropData.bestSeasons.join(', ')}
                              </Typography>
                            </Alert>
                          </Grid>
                        )}

                        {economics.isOptimalSeason && season !== 'Annual' && (
                          <Grid item xs={12}>
                            <Alert severity="success" icon={<CheckCircle />}>
                              <Typography variant="body1" sx={{ fontWeight: 600 }}>
                                Perfect Season! Optimal Growing Conditions
                              </Typography>
                              <Typography variant="body2">
                                {crop} in {season} season offers:
                                • {((economics.seasonFactors.yieldMultiplier - 1) * 100).toFixed(0)}% yield boost
                                • {((economics.seasonFactors.priceMultiplier - 1) * 100).toFixed(0)}% better prices
                                • {season === 'Kharif' ? 'Natural rainfall reduces irrigation costs' : 
                                   season === 'Rabi' ? 'Lower pest pressure and stable weather' : 
                                   'Higher market demand and premium prices'}
                              </Typography>
                            </Alert>
                          </Grid>
                        )}

                        {/* Profitability recommendation */}
                        <Grid item xs={12}>
                          {economics.revenue.roi > 50 ? (
                            <Alert severity="success" icon={<CheckCircle />}>
                              <Typography variant="body1" sx={{ fontWeight: 600 }}>
                                Excellent Choice! High Profitability Expected
                              </Typography>
                              <Typography variant="body2">
                                {crop} shows strong ROI of {economics.revenue.roi.toFixed(1)}% with current parameters. 
                                Expected profit: ₹{economics.revenue.profitPerHectare.toLocaleString()}/hectare.
                              </Typography>
                            </Alert>
                          ) : economics.revenue.roi > 25 ? (
                            <Alert severity="info" icon={<Info />}>
                              <Typography variant="body1" sx={{ fontWeight: 600 }}>
                                Good Profitability Potential
                              </Typography>
                              <Typography variant="body2">
                                {crop} offers moderate returns ({economics.revenue.roi.toFixed(1)}% ROI). 
                                Consider optimizing inputs or irrigation to improve margins.
                              </Typography>
                            </Alert>
                          ) : economics.revenue.roi > 0 ? (
                            <Alert severity="warning" icon={<Warning />}>
                              <Typography variant="body1" sx={{ fontWeight: 600 }}>
                                Low Returns - Optimization Needed
                              </Typography>
                              <Typography variant="body2">
                                ROI is only {economics.revenue.roi.toFixed(1)}%. Consider better irrigation, 
                                reducing input costs, or exploring alternative crops with higher margins.
                              </Typography>
                            </Alert>
                          ) : (
                            <Alert severity="error" icon={<Warning />}>
                              <Typography variant="body1" sx={{ fontWeight: 600 }}>
                                Loss Expected - Reconsider This Crop
                              </Typography>
                              <Typography variant="body2">
                                Current parameters show negative returns. Explore alternative crops or 
                                wait for better market conditions.
                              </Typography>
                            </Alert>
                          )}
                        </Grid>

                        {/* Irrigation optimization */}
                        {irrigationType !== 'Drip' && economics.revenue.netIncome > 0 && (
                          <Grid item xs={12} md={6}>
                            <Card sx={{ bgcolor: 'info.lighter', height: '100%' }}>
                              <CardContent>
                                <Typography variant="body1" sx={{ fontWeight: 600, mb: 1 }}>
                                  <WaterDrop sx={{ verticalAlign: 'middle', mr: 1 }} />
                                  Irrigation Optimization
                                </Typography>
                                <Typography variant="body2" paragraph>
                                  Switching to drip irrigation could:
                                </Typography>
                                <Typography variant="body2" component="div">
                                  • Increase yield by 15%<br />
                                  • Save 50% water<br />
                                  • Boost profit by ₹{(economics.revenue.profitPerHectare * 0.15).toFixed(0)}/hectare
                                </Typography>
                              </CardContent>
                            </Card>
                          </Grid>
                        )}

                        {/* Season timing */}
                        {!economics.cropData.bestSeasons.includes(season) && season !== 'Annual' && (
                          <Grid item xs={12} md={6}>
                            <Card sx={{ bgcolor: 'warning.lighter', height: '100%' }}>
                              <CardContent>
                                <Typography variant="body1" sx={{ fontWeight: 600, mb: 1 }}>
                                  <Timeline sx={{ verticalAlign: 'middle', mr: 1 }} />
                                  Seasonal Timing Alert
                                </Typography>
                                <Typography variant="body2" paragraph>
                                  {crop} grows best in: {economics.cropData.bestSeasons.join(', ')}
                                </Typography>
                                <Typography variant="body2">
                                  Consider waiting for optimal season or choosing seasonal alternatives 
                                  for better results.
                                </Typography>
                              </CardContent>
                            </Card>
                          </Grid>
                        )}

                        {/* Risk management */}
                        {economics.cropData.riskLevel !== 'Low' && (
                          <Grid item xs={12} md={6}>
                            <Card sx={{ bgcolor: 'warning.lighter', height: '100%' }}>
                              <CardContent>
                                <Typography variant="body1" sx={{ fontWeight: 600, mb: 1 }}>
                                  <Warning sx={{ verticalAlign: 'middle', mr: 1 }} />
                                  Risk Management
                                </Typography>
                                <Typography variant="body2" paragraph>
                                  {crop} has {economics.cropData.riskLevel.toLowerCase()} risk due to price volatility 
                                  ({economics.cropData.priceVolatility}).
                                </Typography>
                                <Typography variant="body2">
                                  • Consider crop insurance<br />
                                  • Diversify with multiple crops<br />
                                  • Lock advance prices if possible
                                </Typography>
                              </CardContent>
                            </Card>
                          </Grid>
                        )}

                        {/* Export potential */}
                        {economics.cropData.exportPotential.includes('High') && (
                          <Grid item xs={12} md={6}>
                            <Card sx={{ bgcolor: 'success.lighter', height: '100%' }}>
                              <CardContent>
                                <Typography variant="body1" sx={{ fontWeight: 600, mb: 1 }}>
                                  <TrendingUp sx={{ verticalAlign: 'middle', mr: 1 }} />
                                  Export Opportunity
                                </Typography>
                                <Typography variant="body2" paragraph>
                                  {crop} has {economics.cropData.exportPotential.toLowerCase()} export potential!
                                </Typography>
                                <Typography variant="body2">
                                  • Meet international quality standards<br />
                                  • Contact APEDA for export guidance<br />
                                  • Potential for 20-30% price premium
                                </Typography>
                              </CardContent>
                            </Card>
                          </Grid>
                        )}

                        {/* Cost reduction tips */}
                        <Grid item xs={12}>
                          <Card>
                            <CardContent>
                              <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>
                                💡 Cost Reduction Strategies
                              </Typography>
                              <Grid container spacing={2}>
                                <Grid item xs={12} sm={6} md={3}>
                                  <Typography variant="body2" sx={{ fontWeight: 600, mb: 0.5 }}>Seeds</Typography>
                                  <Typography variant="caption" color="text.secondary">
                                    • Buy certified seeds in bulk<br />
                                    • Join farmer cooperatives<br />
                                    • Consider seed treatment
                                  </Typography>
                                </Grid>
                                <Grid item xs={12} sm={6} md={3}>
                                  <Typography variant="body2" sx={{ fontWeight: 600, mb: 0.5 }}>Fertilizers</Typography>
                                  <Typography variant="caption" color="text.secondary">
                                    • Soil testing before application<br />
                                    • Use organic compost<br />
                                    • Apply subsidy schemes
                                  </Typography>
                                </Grid>
                                <Grid item xs={12} sm={6} md={3}>
                                  <Typography variant="body2" sx={{ fontWeight: 600, mb: 0.5 }}>Labor</Typography>
                                  <Typography variant="caption" color="text.secondary">
                                    • Mechanize operations<br />
                                    • Hire custom hiring centers<br />
                                    • Use MGNREGA schemes
                                  </Typography>
                                </Grid>
                                <Grid item xs={12} sm={6} md={3}>
                                  <Typography variant="body2" sx={{ fontWeight: 600, mb: 0.5 }}>Pesticides</Typography>
                                  <Typography variant="caption" color="text.secondary">
                                    • Integrated pest management<br />
                                    • Biological control methods<br />
                                    • Timely application only
                                  </Typography>
                                </Grid>
                              </Grid>
                            </CardContent>
                          </Card>
                        </Grid>

                        {/* Market timing */}
                        <Grid item xs={12}>
                          <Card sx={{ bgcolor: 'primary.lighter' }}>
                            <CardContent>
                              <Typography variant="h6" sx={{ fontWeight: 600, mb: 1 }}>
                                <Store sx={{ verticalAlign: 'middle', mr: 1 }} />
                                Marketing Strategy
                              </Typography>
                              <Grid container spacing={2}>
                                <Grid item xs={12} md={4}>
                                  <Typography variant="body2" sx={{ fontWeight: 600 }}>When to Sell</Typography>
                                  <Typography variant="caption">
                                    • Monitor e-NAM prices daily<br />
                                    • Avoid harvest season glut<br />
                                    • Store if prices are low (if storage life permits)
                                  </Typography>
                                </Grid>
                                <Grid item xs={12} md={4}>
                                  <Typography variant="body2" sx={{ fontWeight: 600 }}>Where to Sell</Typography>
                                  <Typography variant="caption">
                                    • Register on e-NAM platform<br />
                                    • Contact APMC/mandi<br />
                                    • Explore contract farming<br />
                                    • Direct B2B if quality is premium
                                  </Typography>
                                </Grid>
                                <Grid item xs={12} md={4}>
                                  <Typography variant="body2" sx={{ fontWeight: 600 }}>Price Protection</Typography>
                                  <Typography variant="caption">
                                    • Register for MSP if applicable<br />
                                    • Consider forward contracts<br />
                                    • Track market trends weekly<br />
                                    • Join FPO for better pricing
                                  </Typography>
                                </Grid>
                              </Grid>
                            </CardContent>
                          </Card>
                        </Grid>
                      </Grid>
                    </Box>
                  )}
                </CardContent>
              </Card>
            </>
          ) : (
            <Card sx={{ minHeight: 500, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <CardContent sx={{ textAlign: 'center', maxWidth: 500 }}>
                <BarChart sx={{ fontSize: 120, color: 'primary.main', opacity: 0.2, mb: 3 }} />
                <Typography variant="h5" gutterBottom sx={{ fontWeight: 600 }}>
                  Start Your Economic Analysis
                </Typography>
                <Typography variant="body1" color="text.secondary" paragraph>
                  Select your crop and enter farm parameters on the left to get:
                </Typography>
                <Grid container spacing={2} sx={{ mt: 2 }}>
                  <Grid item xs={6}>
                    <Paper sx={{ p: 2, textAlign: 'center' }}>
                      <AttachMoney sx={{ fontSize: 40, color: 'success.main', mb: 1 }} />
                      <Typography variant="body2">Profit & ROI Analysis</Typography>
                    </Paper>
                  </Grid>
                  <Grid item xs={6}>
                    <Paper sx={{ p: 2, textAlign: 'center' }}>
                      <PieChart sx={{ fontSize: 40, color: 'warning.main', mb: 1 }} />
                      <Typography variant="body2">Cost Breakdown</Typography>
                    </Paper>
                  </Grid>
                  <Grid item xs={6}>
                    <Paper sx={{ p: 2, textAlign: 'center' }}>
                      <Timeline sx={{ fontSize: 40, color: 'info.main', mb: 1 }} />
                      <Typography variant="body2">Market Intelligence</Typography>
                    </Paper>
                  </Grid>
                  <Grid item xs={6}>
                    <Paper sx={{ p: 2, textAlign: 'center' }}>
                      <Insights sx={{ fontSize: 40, color: 'primary.main', mb: 1 }} />
                      <Typography variant="body2">Smart Recommendations</Typography>
                    </Paper>
                  </Grid>
                </Grid>
              </CardContent>
            </Card>
          )}
        </Grid>
      </Grid>
    </Container>
  );
};

export default EconomicAnalysis;
