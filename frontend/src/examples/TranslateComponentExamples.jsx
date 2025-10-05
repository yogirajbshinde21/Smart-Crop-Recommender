/**
 * Translate Component Examples
 * 
 * This file demonstrates all the ways to use the Translate component
 * and its variants in your React application.
 */

import React, { useState } from 'react';
import Translate, {
  TranslateHTML,
  TranslateWithContext,
  TranslatePlural,
  TranslateDate,
  TranslateNumber
} from '../components/Translate';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  TextField,
  Alert,
  Divider,
  Grid,
  List,
  ListItem,
  ListItemText,
  Chip
} from '@mui/material';
import { useTranslation } from '../context/TranslationContext';

// ============================================================================
// Example 1: Basic Translate Component
// ============================================================================
export function Example1_BasicTranslate() {
  return (
    <Card>
      <CardContent>
        <Typography variant="h5" gutterBottom>
          Example 1: Basic Translate
        </Typography>
        
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          <div>
            <Typography variant="caption" color="text.secondary">
              Simple span:
            </Typography>
            <Typography>
              <Translate>navbar.appName</Translate>
            </Typography>
          </div>

          <div>
            <Typography variant="caption" color="text.secondary">
              As h1:
            </Typography>
            <Translate as="h1">dashboard.title</Translate>
          </div>

          <div>
            <Typography variant="caption" color="text.secondary">
              As paragraph:
            </Typography>
            <Translate as="p">dashboard.subtitle</Translate>
          </div>

          <div>
            <Typography variant="caption" color="text.secondary">
              With styling:
            </Typography>
            <Translate 
              as="h3" 
              style={{ color: '#2e7d32', fontWeight: 'bold' }}
            >
              crop.title
            </Translate>
          </div>
        </Box>
      </CardContent>
    </Card>
  );
}

// ============================================================================
// Example 2: Translate with Parameters
// ============================================================================
export function Example2_TranslateWithParams() {
  const [username] = useState('Ramesh');
  const [itemCount] = useState(5);

  return (
    <Card>
      <CardContent>
        <Typography variant="h5" gutterBottom>
          Example 2: With Parameters
        </Typography>
        
        <Alert severity="info" sx={{ mb: 2 }}>
          Add these to your translation files:<br/>
          <code>"greeting.welcome": "Welcome back, {'{name}'}!"</code><br/>
          <code>"inventory.count": "You have {'{count}'} items"</code>
        </Alert>

        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          <Typography>
            <Translate params={{ name: username }}>
              greeting.welcome
            </Translate>
          </Typography>

          <Typography>
            <Translate params={{ count: itemCount }}>
              inventory.count
            </Translate>
          </Typography>
        </Box>
      </CardContent>
    </Card>
  );
}

// ============================================================================
// Example 3: Translate with Fallback
// ============================================================================
export function Example3_TranslateWithFallback() {
  return (
    <Card>
      <CardContent>
        <Typography variant="h5" gutterBottom>
          Example 3: With Fallback
        </Typography>

        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          <Typography>
            <strong>Existing key:</strong>{' '}
            <Translate fallback="Dashboard">dashboard.title</Translate>
          </Typography>

          <Typography>
            <strong>Non-existing key:</strong>{' '}
            <Translate fallback="Custom Fallback Text">
              nonexistent.key
            </Translate>
          </Typography>
        </Box>
      </CardContent>
    </Card>
  );
}

// ============================================================================
// Example 4: TranslateHTML Component
// ============================================================================
export function Example4_TranslateHTML() {
  return (
    <Card>
      <CardContent>
        <Typography variant="h5" gutterBottom>
          Example 4: HTML Content
        </Typography>
        
        <Alert severity="warning" sx={{ mb: 2 }}>
          For demo: Add this to translations:<br/>
          <code>"content.richText": "Visit &lt;b&gt;our page&lt;/b&gt; for more &lt;i&gt;information&lt;/i&gt;"</code>
        </Alert>

        <TranslateHTML as="div" style={{ padding: '16px', background: '#f5f5f5' }}>
          content.richText
        </TranslateHTML>
      </CardContent>
    </Card>
  );
}

// ============================================================================
// Example 5: TranslateWithContext (Debug Mode)
// ============================================================================
export function Example5_TranslateWithContext() {
  return (
    <Card>
      <CardContent>
        <Typography variant="h5" gutterBottom>
          Example 5: Debug Mode
        </Typography>

        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          <Typography>
            <strong>Normal:</strong>{' '}
            <Translate>navbar.appName</Translate>
          </Typography>

          <Typography>
            <strong>With key:</strong>{' '}
            <TranslateWithContext showKey>
              navbar.appName
            </TranslateWithContext>
          </Typography>

          <Typography>
            <strong>With language:</strong>{' '}
            <TranslateWithContext showLanguage>
              navbar.appName
            </TranslateWithContext>
          </Typography>

          <Typography>
            <strong>With both:</strong>{' '}
            <TranslateWithContext showKey showLanguage>
              navbar.appName
            </TranslateWithContext>
          </Typography>
        </Box>
      </CardContent>
    </Card>
  );
}

// ============================================================================
// Example 6: TranslatePlural Component
// ============================================================================
export function Example6_TranslatePlural() {
  const [count, setCount] = useState(1);

  return (
    <Card>
      <CardContent>
        <Typography variant="h5" gutterBottom>
          Example 6: Plural Forms
        </Typography>
        
        <Alert severity="info" sx={{ mb: 2 }}>
          Add these to your translation files:<br/>
          <code>"items.singular": "You have {'{count}'} item"</code><br/>
          <code>"items.plural": "You have {'{count}'} items"</code>
        </Alert>

        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
          <Button 
            variant="outlined" 
            onClick={() => setCount(Math.max(0, count - 1))}
          >
            -
          </Button>
          <Typography variant="h4">{count}</Typography>
          <Button 
            variant="outlined" 
            onClick={() => setCount(count + 1)}
          >
            +
          </Button>
        </Box>

        <Typography variant="h6">
          <TranslatePlural count={count} params={{ count }}>
            items
          </TranslatePlural>
        </Typography>
      </CardContent>
    </Card>
  );
}

// ============================================================================
// Example 7: TranslateDate Component
// ============================================================================
export function Example7_TranslateDate() {
  const today = new Date();

  return (
    <Card>
      <CardContent>
        <Typography variant="h5" gutterBottom>
          Example 7: Date Formatting
        </Typography>

        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          <Box>
            <Typography variant="caption" color="text.secondary">
              Short:
            </Typography>
            <Typography>
              <TranslateDate date={today} options={{ dateStyle: 'short' }} />
            </Typography>
          </Box>

          <Box>
            <Typography variant="caption" color="text.secondary">
              Medium:
            </Typography>
            <Typography>
              <TranslateDate date={today} options={{ dateStyle: 'medium' }} />
            </Typography>
          </Box>

          <Box>
            <Typography variant="caption" color="text.secondary">
              Long:
            </Typography>
            <Typography>
              <TranslateDate date={today} options={{ dateStyle: 'long' }} />
            </Typography>
          </Box>

          <Box>
            <Typography variant="caption" color="text.secondary">
              Full:
            </Typography>
            <Typography>
              <TranslateDate date={today} options={{ dateStyle: 'full' }} />
            </Typography>
          </Box>

          <Box>
            <Typography variant="caption" color="text.secondary">
              Custom:
            </Typography>
            <Typography>
              <TranslateDate 
                date={today} 
                options={{ 
                  year: 'numeric', 
                  month: 'long', 
                  day: 'numeric',
                  weekday: 'long'
                }} 
              />
            </Typography>
          </Box>
        </Box>
      </CardContent>
    </Card>
  );
}

// ============================================================================
// Example 8: TranslateNumber Component
// ============================================================================
export function Example8_TranslateNumber() {
  return (
    <Card>
      <CardContent>
        <Typography variant="h5" gutterBottom>
          Example 8: Number Formatting
        </Typography>

        <Grid container spacing={2}>
          <Grid item xs={12} md={6}>
            <Box sx={{ p: 2, bgcolor: '#f5f5f5', borderRadius: 1 }}>
              <Typography variant="caption" color="text.secondary">
                Simple number:
              </Typography>
              <Typography variant="h6">
                <TranslateNumber value={1234567.89} />
              </Typography>
            </Box>
          </Grid>

          <Grid item xs={12} md={6}>
            <Box sx={{ p: 2, bgcolor: '#f5f5f5', borderRadius: 1 }}>
              <Typography variant="caption" color="text.secondary">
                Currency (INR):
              </Typography>
              <Typography variant="h6">
                <TranslateNumber 
                  value={50000} 
                  options={{ style: 'currency', currency: 'INR' }}
                />
              </Typography>
            </Box>
          </Grid>

          <Grid item xs={12} md={6}>
            <Box sx={{ p: 2, bgcolor: '#f5f5f5', borderRadius: 1 }}>
              <Typography variant="caption" color="text.secondary">
                Percentage:
              </Typography>
              <Typography variant="h6">
                <TranslateNumber 
                  value={0.856} 
                  options={{ style: 'percent' }}
                />
              </Typography>
            </Box>
          </Grid>

          <Grid item xs={12} md={6}>
            <Box sx={{ p: 2, bgcolor: '#f5f5f5', borderRadius: 1 }}>
              <Typography variant="caption" color="text.secondary">
                Compact:
              </Typography>
              <Typography variant="h6">
                <TranslateNumber 
                  value={1000000} 
                  options={{ notation: 'compact' }}
                />
              </Typography>
            </Box>
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );
}

// ============================================================================
// Example 9: Real-World Form
// ============================================================================
export function Example9_RealWorldForm() {
  const [formData, setFormData] = useState({
    district: '',
    soilType: '',
    weather: ''
  });
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    setSubmitted(true);
    setTimeout(() => setSubmitted(false), 3000);
  };

  return (
    <Card>
      <CardContent>
        <Typography variant="h5" gutterBottom>
          <Translate>crop.title</Translate>
        </Typography>
        
        <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
          <Translate>crop.subtitle</Translate>
        </Typography>

        <form onSubmit={handleSubmit}>
          <TextField
            label={<Translate>crop.district</Translate>}
            name="district"
            value={formData.district}
            onChange={(e) => setFormData({ ...formData, district: e.target.value })}
            fullWidth
            margin="normal"
            required
          />

          <TextField
            label={<Translate>crop.soilType</Translate>}
            name="soilType"
            value={formData.soilType}
            onChange={(e) => setFormData({ ...formData, soilType: e.target.value })}
            fullWidth
            margin="normal"
            required
          />

          <TextField
            label={<Translate>crop.weather</Translate>}
            name="weather"
            value={formData.weather}
            onChange={(e) => setFormData({ ...formData, weather: e.target.value })}
            fullWidth
            margin="normal"
            required
          />

          {submitted && (
            <Alert severity="success" sx={{ mt: 2 }}>
              <Translate>common.success</Translate>
            </Alert>
          )}

          <Button type="submit" variant="contained" fullWidth sx={{ mt: 3 }}>
            <Translate>crop.getRecommendations</Translate>
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}

// ============================================================================
// Example 10: Navigation List
// ============================================================================
export function Example10_NavigationList() {
  const navItems = [
    'navbar.dashboard',
    'navbar.cropRecommendation',
    'navbar.nutrientAnalysis',
    'navbar.waterQuality',
    'navbar.cropComparison',
    'navbar.districtInsights',
    'navbar.weatherPlanning',
    'navbar.economicAnalysis'
  ];

  return (
    <Card>
      <CardContent>
        <Typography variant="h5" gutterBottom>
          Example 10: Navigation Items
        </Typography>

        <List>
          {navItems.map((item, index) => (
            <ListItem key={item} divider={index < navItems.length - 1}>
              <ListItemText>
                <Translate>{item}</Translate>
              </ListItemText>
              <Chip 
                label={<Translate>common.next</Translate>} 
                size="small" 
                color="primary" 
                variant="outlined"
              />
            </ListItem>
          ))}
        </List>
      </CardContent>
    </Card>
  );
}

// ============================================================================
// Main Demo Component
// ============================================================================
export default function TranslateComponentExamples() {
  const { language, changeLanguage } = useTranslation();

  return (
    <Box sx={{ p: 3, maxWidth: 1200, mx: 'auto' }}>
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h3" gutterBottom>
            <Translate>navbar.appName</Translate> - Translate Component Examples
          </Typography>
          
          <Box sx={{ display: 'flex', gap: 2, alignItems: 'center', mb: 2 }}>
            <Typography>Current Language: <strong>{language}</strong></Typography>
            <Button 
              variant={language === 'en' ? 'contained' : 'outlined'}
              onClick={() => changeLanguage('en')}
              size="small"
            >
              English
            </Button>
            <Button 
              variant={language === 'hi' ? 'contained' : 'outlined'}
              onClick={() => changeLanguage('hi')}
              size="small"
            >
              हिंदी
            </Button>
            <Button 
              variant={language === 'mr' ? 'contained' : 'outlined'}
              onClick={() => changeLanguage('mr')}
              size="small"
            >
              मराठी
            </Button>
          </Box>
        </CardContent>
      </Card>

      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
        <Example1_BasicTranslate />
        <Example2_TranslateWithParams />
        <Example3_TranslateWithFallback />
        <Example4_TranslateHTML />
        <Example5_TranslateWithContext />
        <Example6_TranslatePlural />
        <Example7_TranslateDate />
        <Example8_TranslateNumber />
        <Example9_RealWorldForm />
        <Example10_NavigationList />
      </Box>
    </Box>
  );
}
