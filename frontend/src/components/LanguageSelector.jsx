import React from 'react';
import {
  Box,
  Select,
  MenuItem,
  FormControl,
  Card,
  CardContent,
  Typography,
  Button
} from '@mui/material';
import { Language as LanguageIcon, Check as CheckIcon } from '@mui/icons-material';
import { useTranslation } from '../context/TranslationContext';

/**
 * Language Selector Component (Navbar Version)
 * 
 * A compact language selector designed for the navbar.
 * Displays languages in their native scripts with visual feedback.
 * 
 * Usage:
 * <LanguageSelector />
 */
const LanguageSelector = ({ variant = 'navbar' }) => {
  const { language, changeLanguage, availableLanguages } = useTranslation();

  const handleLanguageChange = (event) => {
    const newLang = event.target.value;
    changeLanguage(newLang);
  };

  // Navbar variant - compact and styled for navbar
  if (variant === 'navbar') {
    return (
      <FormControl
        size="small"
        sx={{
          minWidth: 120,
          '& .MuiOutlinedInput-root': {
            color: 'white',
            '& fieldset': {
              borderColor: 'rgba(255, 255, 255, 0.3)',
            },
            '&:hover fieldset': {
              borderColor: 'rgba(255, 255, 255, 0.5)',
            },
            '&.Mui-focused fieldset': {
              borderColor: 'white',
            },
          },
          '& .MuiSvgIcon-root': {
            color: 'white',
          },
        }}
      >
        <Select
          id="language-selector"
          value={language}
          onChange={handleLanguageChange}
          startAdornment={
            <LanguageIcon sx={{ fontSize: 18, mr: 0.5, color: 'white' }} />
          }
          sx={{
            '& .MuiSelect-select': {
              display: 'flex',
              alignItems: 'center',
              gap: 1,
              py: 1,
            },
          }}
        >
          {availableLanguages.map((lang) => (
            <MenuItem
              key={lang.code}
              value={lang.code}
              sx={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                gap: 2,
                fontWeight: language === lang.code ? 600 : 400,
                backgroundColor: language === lang.code ? 'rgba(46, 125, 50, 0.08)' : 'transparent',
                '&:hover': {
                  backgroundColor: language === lang.code ? 'rgba(46, 125, 50, 0.12)' : 'rgba(0, 0, 0, 0.04)',
                },
              }}
            >
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <Typography
                  sx={{
                    fontSize: '0.95rem',
                    fontWeight: language === lang.code ? 600 : 400,
                  }}
                >
                  {lang.nativeName}
                </Typography>
                {lang.code !== 'en' && (
                  <Typography
                    variant="caption"
                    sx={{
                      color: 'text.secondary',
                      fontSize: '0.75rem',
                    }}
                  >
                    ({lang.name})
                  </Typography>
                )}
              </Box>
              {language === lang.code && (
                <CheckIcon sx={{ fontSize: 18, color: 'primary.main' }} />
              )}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
    );
  }

  // Standard variant - for use in settings pages or forms
  return (
    <FormControl fullWidth size="small">
      <Select
        id="language-selector-standard"
        value={language}
        onChange={handleLanguageChange}
        sx={{
          '& .MuiSelect-select': {
            display: 'flex',
            alignItems: 'center',
            gap: 1,
          },
        }}
      >
        {availableLanguages.map((lang) => (
          <MenuItem
            key={lang.code}
            value={lang.code}
            sx={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              gap: 2,
            }}
          >
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <LanguageIcon sx={{ fontSize: 18, color: 'primary.main' }} />
              <Typography>{lang.nativeName}</Typography>
              {lang.code !== 'en' && (
                <Typography variant="caption" color="text.secondary">
                  ({lang.name})
                </Typography>
              )}
            </Box>
            {language === lang.code && (
              <CheckIcon sx={{ fontSize: 18, color: 'primary.main' }} />
            )}
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  );
};

/**
 * Translation Demo Component
 * 
 * This component demonstrates how to use translations in your components.
 * You can remove this component after understanding the translation system.
 */
export const TranslationDemo = () => {
  const { t, language, changeLanguage } = useTranslation();

  return (
    <Box sx={{ p: 3, maxWidth: 800, mx: 'auto' }}>
      <Card>
        <CardContent>
          <Typography variant="h5" gutterBottom>
            {t('dashboard.title')} - Translation Demo
          </Typography>
          
          <Box sx={{ mb: 3 }}>
            <LanguageSelector />
          </Box>

          <Typography variant="h6" gutterBottom sx={{ mt: 3 }}>
            Example Translations:
          </Typography>

          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            <Card variant="outlined">
              <CardContent>
                <Typography variant="body2" color="text.secondary">
                  navbar.appName
                </Typography>
                <Typography variant="h6">
                  {t('navbar.appName')}
                </Typography>
              </CardContent>
            </Card>

            <Card variant="outlined">
              <CardContent>
                <Typography variant="body2" color="text.secondary">
                  dashboard.welcome
                </Typography>
                <Typography variant="h6">
                  {t('dashboard.welcome')}
                </Typography>
              </CardContent>
            </Card>

            <Card variant="outlined">
              <CardContent>
                <Typography variant="body2" color="text.secondary">
                  crop.title
                </Typography>
                <Typography variant="h6">
                  {t('crop.title')}
                </Typography>
              </CardContent>
            </Card>

            <Card variant="outlined">
              <CardContent>
                <Typography variant="body2" color="text.secondary">
                  common.submit
                </Typography>
                <Button variant="contained">
                  {t('common.submit')}
                </Button>
              </CardContent>
            </Card>
          </Box>

          <Box sx={{ mt: 3, display: 'flex', gap: 2 }}>
            <Button
              variant={language === 'en' ? 'contained' : 'outlined'}
              onClick={() => changeLanguage('en')}
            >
              English
            </Button>
            <Button
              variant={language === 'hi' ? 'contained' : 'outlined'}
              onClick={() => changeLanguage('hi')}
            >
              हिंदी
            </Button>
            <Button
              variant={language === 'mr' ? 'contained' : 'outlined'}
              onClick={() => changeLanguage('mr')}
            >
              मराठी
            </Button>
          </Box>

          <Box sx={{ mt: 3, p: 2, bgcolor: 'info.light', borderRadius: 1 }}>
            <Typography variant="caption">
              <strong>Current Language:</strong> {language.toUpperCase()}
            </Typography>
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
};

export default LanguageSelector;
