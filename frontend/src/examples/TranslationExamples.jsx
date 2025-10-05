/**
 * Translation System Example Usage
 * 
 * This file demonstrates various ways to use the translation context and hook
 * in your React components.
 */

import React, { useState } from 'react';
import { useTranslation } from '../context/TranslationContext';
import {
  Box,
  Button,
  Typography,
  TextField,
  Card,
  CardContent,
  Alert,
  Select,
  MenuItem
} from '@mui/material';

// ============================================================================
// Example 1: Basic Translation Usage
// ============================================================================
export function Example1_BasicTranslation() {
  const { t } = useTranslation();

  return (
    <div>
      <h1>{t('navbar.appName')}</h1>
      <p>{t('dashboard.subtitle')}</p>
      <button>{t('common.submit')}</button>
    </div>
  );
}

// ============================================================================
// Example 2: Language Switching
// ============================================================================
export function Example2_LanguageSwitcher() {
  const { language, changeLanguage, availableLanguages } = useTranslation();

  return (
    <Box>
      <Typography>Current Language: {language}</Typography>
      {availableLanguages.map((lang) => (
        <Button
          key={lang.code}
          variant={language === lang.code ? 'contained' : 'outlined'}
          onClick={() => changeLanguage(lang.code)}
          sx={{ m: 1 }}
        >
          {lang.nativeName}
        </Button>
      ))}
    </Box>
  );
}

// ============================================================================
// Example 3: Form with Translations
// ============================================================================
export function Example3_TranslatedForm() {
  const { t } = useTranslation();
  const [formData, setFormData] = useState({
    district: '',
    soilType: '',
    weather: ''
  });

  return (
    <Box component="form">
      <TextField
        label={t('crop.district')}
        name="district"
        value={formData.district}
        onChange={(e) => setFormData({ ...formData, district: e.target.value })}
        fullWidth
        margin="normal"
      />
      <TextField
        label={t('crop.soilType')}
        name="soilType"
        value={formData.soilType}
        onChange={(e) => setFormData({ ...formData, soilType: e.target.value })}
        fullWidth
        margin="normal"
      />
      <TextField
        label={t('crop.weather')}
        name="weather"
        value={formData.weather}
        onChange={(e) => setFormData({ ...formData, weather: e.target.value })}
        fullWidth
        margin="normal"
      />
      <Button variant="contained" type="submit" sx={{ mt: 2 }}>
        {t('crop.getRecommendations')}
      </Button>
    </Box>
  );
}

// ============================================================================
// Example 4: Conditional Rendering Based on Language
// ============================================================================
export function Example4_ConditionalContent() {
  const { language, t } = useTranslation();

  return (
    <Card>
      <CardContent>
        <Typography variant="h5">{t('dashboard.title')}</Typography>
        
        {language === 'en' && (
          <Typography color="primary">
            English-specific content
          </Typography>
        )}
        
        {language === 'hi' && (
          <Typography color="primary">
            विशेष हिंदी सामग्री
          </Typography>
        )}
        
        {language === 'mr' && (
          <Typography color="primary">
            विशेष मराठी सामग्री
          </Typography>
        )}
      </CardContent>
    </Card>
  );
}

// ============================================================================
// Example 5: Alert Messages with Translations
// ============================================================================
export function Example5_AlertMessages() {
  const { t } = useTranslation();
  const [showError, setShowError] = useState(true);

  return (
    <Box>
      {showError && (
        <Alert severity="error" onClose={() => setShowError(false)}>
          {t('crop.errorFillFields')}
        </Alert>
      )}
      <Alert severity="success" sx={{ mt: 2 }}>
        {t('common.success')}
      </Alert>
      <Alert severity="warning" sx={{ mt: 2 }}>
        {t('common.warning')}
      </Alert>
      <Alert severity="info" sx={{ mt: 2 }}>
        {t('common.info')}
      </Alert>
    </Box>
  );
}

// ============================================================================
// Example 6: Dynamic Parameter Interpolation
// ============================================================================
export function Example6_ParameterInterpolation() {
  const { t } = useTranslation();
  const username = 'John Doe';
  const itemCount = 5;

  // Note: Add these keys to your translation files for this to work
  // "greeting.welcome": "Welcome back, {name}!"
  // "inventory.count": "You have {count} items"

  return (
    <Box>
      <Typography>
        {t('greeting.welcome', { name: username })}
      </Typography>
      <Typography>
        {t('inventory.count', { count: itemCount })}
      </Typography>
    </Box>
  );
}

// ============================================================================
// Example 7: Checking Translation Existence
// ============================================================================
export function Example7_CheckTranslation() {
  const { t, hasTranslation } = useTranslation();

  return (
    <Box>
      {hasTranslation('navbar.home') && (
        <Typography>{t('navbar.home')}</Typography>
      )}
      
      {!hasTranslation('nonexistent.key') && (
        <Typography color="error">
          Translation key 'nonexistent.key' does not exist
        </Typography>
      )}
    </Box>
  );
}

// ============================================================================
// Example 8: Multi-language Display
// ============================================================================
export function Example8_MultiLanguageDisplay() {
  const { getTranslationForLanguage } = useTranslation();

  return (
    <Card>
      <CardContent>
        <Typography variant="h6">All Languages:</Typography>
        
        <Box sx={{ mt: 2 }}>
          <Typography variant="subtitle2">English:</Typography>
          <Typography>{getTranslationForLanguage('navbar.appName', 'en')}</Typography>
        </Box>
        
        <Box sx={{ mt: 2 }}>
          <Typography variant="subtitle2">हिंदी:</Typography>
          <Typography>{getTranslationForLanguage('navbar.appName', 'hi')}</Typography>
        </Box>
        
        <Box sx={{ mt: 2 }}>
          <Typography variant="subtitle2">मराठी:</Typography>
          <Typography>{getTranslationForLanguage('navbar.appName', 'mr')}</Typography>
        </Box>
      </CardContent>
    </Card>
  );
}

// ============================================================================
// Example 9: Complete Component with Translation
// ============================================================================
export function Example9_CompleteComponent() {
  const { t, language, changeLanguage } = useTranslation();
  const [district, setDistrict] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (!district) {
      setError(t('crop.errorFillFields'));
      return;
    }
    
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      setSuccess(true);
      setError(null);
    }, 1000);
  };

  return (
    <Box sx={{ maxWidth: 600, mx: 'auto', p: 3 }}>
      <Card>
        <CardContent>
          <Typography variant="h4" gutterBottom>
            {t('crop.title')}
          </Typography>
          
          <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
            {t('crop.subtitle')}
          </Typography>

          <Select
            value={language}
            onChange={(e) => changeLanguage(e.target.value)}
            size="small"
            sx={{ mb: 3 }}
          >
            <MenuItem value="en">English</MenuItem>
            <MenuItem value="hi">हिंदी</MenuItem>
            <MenuItem value="mr">मराठी</MenuItem>
          </Select>

          <form onSubmit={handleSubmit}>
            <TextField
              label={t('crop.district')}
              value={district}
              onChange={(e) => setDistrict(e.target.value)}
              fullWidth
              margin="normal"
              required
            />

            {error && (
              <Alert severity="error" sx={{ mt: 2 }}>
                {error}
              </Alert>
            )}

            {success && (
              <Alert severity="success" sx={{ mt: 2 }}>
                {t('common.success')}
              </Alert>
            )}

            <Button
              type="submit"
              variant="contained"
              fullWidth
              disabled={loading}
              sx={{ mt: 3 }}
            >
              {loading ? t('common.loading') : t('crop.getRecommendations')}
            </Button>
          </form>
        </CardContent>
      </Card>
    </Box>
  );
}

// ============================================================================
// Example 10: Navigation Menu with Translations
// ============================================================================
export function Example10_NavigationMenu() {
  const { t } = useTranslation();

  const menuItems = [
    { key: 'dashboard', path: '/', labelKey: 'navbar.dashboard' },
    { key: 'crop', path: '/crop', labelKey: 'navbar.cropRecommendation' },
    { key: 'nutrient', path: '/nutrient', labelKey: 'navbar.nutrientAnalysis' },
    { key: 'water', path: '/water', labelKey: 'navbar.waterQuality' },
  ];

  return (
    <nav>
      {menuItems.map((item) => (
        <Button key={item.key} href={item.path}>
          {t(item.labelKey)}
        </Button>
      ))}
    </nav>
  );
}

// ============================================================================
// Export all examples
// ============================================================================
export default {
  Example1_BasicTranslation,
  Example2_LanguageSwitcher,
  Example3_TranslatedForm,
  Example4_ConditionalContent,
  Example5_AlertMessages,
  Example6_ParameterInterpolation,
  Example7_CheckTranslation,
  Example8_MultiLanguageDisplay,
  Example9_CompleteComponent,
  Example10_NavigationMenu,
};
