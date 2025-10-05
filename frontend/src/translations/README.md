# Translation System Documentation

## Overview
This project uses a JavaScript object-based translation system with support for English, Hindi (हिंदी), and Marathi (मराठी).

## File Structure
```
frontend/src/
├── translations/
│   ├── en.js          # English translations
│   ├── hi.js          # Hindi translations
│   ├── mr.js          # Marathi translations
│   └── index.js       # Export file for all translations
└── utils/
    └── translations.js # Translation utility functions
```

## Translation Files

Each language file exports a `translations` object with key-value pairs:

```javascript
export const translations = {
  "navbar.home": "Home",
  "navbar.dashboard": "Dashboard",
  "common.submit": "Submit",
  // ... more translations
};
```

### Key Naming Convention
Translation keys follow a hierarchical dot notation:
- `navbar.*` - Navigation bar items
- `dashboard.*` - Dashboard page
- `crop.*` - Crop recommendation page
- `nutrient.*` - Nutrient analysis page
- `water.*` - Water quality page
- `compare.*` - Crop comparison page
- `district.*` - District insights page
- `weather.*` - Weather planning page
- `economic.*` - Economic analysis page
- `common.*` - Common UI elements
- `api.*` - API status messages
- `units.*` - Measurement units
- `season.*` - Season names
- `soil.*` - Soil types
- `footer.*` - Footer content

### Important Note: Nutrient Names
**Nutrient names remain untranslated across all language files** to maintain scientific consistency:
- Nitrogen (N)
- Phosphorus (P)
- Potassium (K)
- Zinc (Zn)
- Sulfur (S)

## Usage in Components

### Basic Usage

```javascript
import { t } from '../utils/translations';

function MyComponent() {
  return (
    <div>
      <h1>{t('navbar.home')}</h1>
      <button>{t('common.submit')}</button>
    </div>
  );
}
```

### Change Language

```javascript
import { setLanguage } from '../utils/translations';

// Change to Hindi
setLanguage('hi');

// Change to Marathi
setLanguage('mr');

// Change to English
setLanguage('en');
```

### Get Current Language

```javascript
import { getCurrentLanguage } from '../utils/translations';

const currentLang = getCurrentLanguage();
console.log(currentLang); // 'en', 'hi', or 'mr'
```

### Get Available Languages

```javascript
import { getAvailableLanguages } from '../utils/translations';

const languages = getAvailableLanguages();
// Returns:
// [
//   { code: 'en', name: 'English', nativeName: 'English' },
//   { code: 'hi', name: 'Hindi', nativeName: 'हिंदी' },
//   { code: 'mr', name: 'Marathi', nativeName: 'मराठी' }
// ]
```

### Check if Translation Exists

```javascript
import { hasTranslation } from '../utils/translations';

if (hasTranslation('navbar.home')) {
  // Translation exists
}
```

### Get All Translations

```javascript
import { getAllTranslations } from '../utils/translations';

const translations = getAllTranslations();
console.log(translations);
```

## Language Selector Component Example

```javascript
import React from 'react';
import { MenuItem, Select } from '@mui/material';
import { setLanguage, getCurrentLanguage, getAvailableLanguages } from '../utils/translations';

function LanguageSelector() {
  const [language, setCurrentLanguage] = React.useState(getCurrentLanguage());
  const languages = getAvailableLanguages();

  const handleLanguageChange = (event) => {
    const newLang = event.target.value;
    setLanguage(newLang);
    setCurrentLanguage(newLang);
    // Force re-render of components
    window.location.reload();
  };

  return (
    <Select value={language} onChange={handleLanguageChange}>
      {languages.map((lang) => (
        <MenuItem key={lang.code} value={lang.code}>
          {lang.nativeName}
        </MenuItem>
      ))}
    </Select>
  );
}

export default LanguageSelector;
```

## Integration with React Context

For better state management, integrate with AppContext:

```javascript
// In AppContext.jsx
import { getCurrentLanguage, setLanguage, t } from '../utils/translations';

const AppContext = createContext();

export const AppProvider = ({ children }) => {
  const [language, setCurrentLanguage] = useState(getCurrentLanguage());

  const changeLanguage = (newLang) => {
    setLanguage(newLang);
    setCurrentLanguage(newLang);
  };

  return (
    <AppContext.Provider value={{ language, changeLanguage, t }}>
      {children}
    </AppContext.Provider>
  );
};

// In components
import { useApp } from '../context/AppContext';

function MyComponent() {
  const { t, changeLanguage } = useApp();
  
  return (
    <div>
      <h1>{t('navbar.home')}</h1>
      <button onClick={() => changeLanguage('hi')}>हिंदी</button>
    </div>
  );
}
```

## Adding New Translations

To add a new translation key:

1. Add the key-value pair to `en.js`:
```javascript
"myFeature.title": "My Feature Title"
```

2. Add the Hindi translation to `hi.js`:
```javascript
"myFeature.title": "मेरी सुविधा शीर्षक"
```

3. Add the Marathi translation to `mr.js`:
```javascript
"myFeature.title": "माझे वैशिष्ट्य शीर्षक"
```

4. Use in your component:
```javascript
{t('myFeature.title')}
```

## Best Practices

1. **Consistent Keys**: Use descriptive, hierarchical keys
2. **Fallback**: System automatically falls back to English if translation is missing
3. **Persistence**: Selected language is saved in localStorage
4. **Nutrient Names**: Keep scientific terms (nutrient names) untranslated
5. **Context**: Provide enough context in key names (e.g., `crop.title` vs `nutrient.title`)
6. **Testing**: Test all language variations before deployment

## Translation Coverage

Current translation coverage:
- ✅ Navbar (9 items)
- ✅ Dashboard (8+ items)
- ✅ Crop Recommendation (15+ items)
- ✅ Nutrient Analysis (15+ items)
- ✅ Water Quality (15+ items)
- ✅ Crop Comparison (12+ items)
- ✅ District Insights (8+ items)
- ✅ Weather Planning (10+ items)
- ✅ Economic Analysis (15+ items)
- ✅ Common UI (20+ items)
- ✅ API Status (4 items)
- ✅ Units (8 items)
- ✅ Seasons (4 items)
- ✅ Soil Types (5 items)
- ✅ Weather Conditions (5 items)

**Total: 150+ translation keys**

## Supported Languages

- 🇬🇧 **English (en)** - Default
- 🇮🇳 **हिंदी (hi)** - Hindi
- 🇮🇳 **मराठी (mr)** - Marathi

## Future Enhancements

- Add more Indian languages (Gujarati, Kannada, etc.)
- Implement RTL support if needed
- Add date/time formatting per locale
- Add number formatting per locale
- Implement pluralization support
