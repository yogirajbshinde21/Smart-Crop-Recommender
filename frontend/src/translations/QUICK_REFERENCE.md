# Translation Quick Reference Guide

## 🚀 Quick Start

### 1. Import the translation function
```javascript
import { t } from '../utils/translations';
```

### 2. Use in your component
```javascript
<Typography variant="h4">{t('dashboard.title')}</Typography>
<Button>{t('common.submit')}</Button>
```

### 3. Change language
```javascript
import { setLanguage } from '../utils/translations';

setLanguage('hi'); // Switch to Hindi
setLanguage('mr'); // Switch to Marathi
setLanguage('en'); // Switch to English
```

## 📝 Available Translation Keys

### Navigation
- `navbar.appName` - "Smart Farmer"
- `navbar.dashboard` - "Dashboard"
- `navbar.cropRecommendation` - "Crop Recommendation"
- `navbar.nutrientAnalysis` - "Nutrient Analysis"
- `navbar.waterQuality` - "Water Quality"
- `navbar.cropComparison` - "Crop Comparison"
- `navbar.districtInsights` - "District Insights"
- `navbar.weatherPlanning` - "Weather Planning"
- `navbar.economicAnalysis` - "Economic Analysis"

### Common UI
- `common.submit` - "Submit"
- `common.cancel` - "Cancel"
- `common.save` - "Save"
- `common.delete` - "Delete"
- `common.edit` - "Edit"
- `common.loading` - "Loading..."
- `common.error` - "Error"
- `common.success` - "Success"
- `common.warning` - "Warning"

### Form Fields
- `crop.district` - "District"
- `crop.soilType` - "Soil Type"
- `crop.weather` - "Weather"
- `nutrient.crop` - "Crop"
- `water.analyzeWater` - "Analyze Water Quality"

### Status Messages
- `api.connecting` - "Connecting to server..."
- `api.connected` - "Connected"
- `api.disconnected` - "Disconnected"
- `crop.errorFillFields` - "Please fill in all fields"

### Units (English notation kept)
- `units.kgPerHa` - "kg/ha"
- `units.hectares` - "hectares"
- `units.celsius` - "°C"
- `units.rupees` - "₹"

### Nutrient Names (Untranslated)
- `nutrient.nitrogen` - "Nitrogen (N)"
- `nutrient.phosphorus` - "Phosphorus (P)"
- `nutrient.potassium` - "Potassium (K)"
- `nutrient.zinc` - "Zinc (Zn)"
- `nutrient.sulfur` - "Sulfur (S)"

## 💡 Usage Examples

### Basic Text
```javascript
<Typography>{t('dashboard.welcome')}</Typography>
```

### Button Labels
```javascript
<Button variant="contained">
  {t('common.submit')}
</Button>
```

### Form Labels
```javascript
<TextField
  label={t('crop.district')}
  name="District"
  value={formData.District}
/>
```

### Alert Messages
```javascript
<Alert severity="error">
  {t('crop.errorFillFields')}
</Alert>
```

### Titles and Headings
```javascript
<Typography variant="h4" gutterBottom>
  {t('crop.title')}
</Typography>
<Typography variant="body1" color="text.secondary">
  {t('crop.subtitle')}
</Typography>
```

## 🎨 Language Selector Integration

### Add to Navbar
```javascript
import LanguageSelector from './LanguageSelector';

// In Navbar component
<Toolbar>
  {/* Other navbar items */}
  <LanguageSelector />
</Toolbar>
```

### Standalone Usage
```javascript
import LanguageSelector from '../components/LanguageSelector';

function SettingsPage() {
  return (
    <Box>
      <Typography variant="h6">Language Settings</Typography>
      <LanguageSelector />
    </Box>
  );
}
```

## 🔄 Language Persistence

The selected language is automatically saved to `localStorage` and persists across sessions.

```javascript
// Get current language
const currentLang = getCurrentLanguage();

// Language is automatically loaded from localStorage on app start
initLanguage(); // Called automatically in translations.js
```

## ⚠️ Important Notes

1. **Nutrient names remain in English** across all translations for scientific accuracy
2. **Page reload required** after language change for full effect (can be optimized with React Context)
3. **Fallback to English** if translation key is missing in selected language
4. **Console warnings** shown for missing translation keys in development

## 🔧 Troubleshooting

### Translation not showing
- Check if key exists in translation file
- Verify import path is correct
- Check browser console for warnings

### Language not changing
- Ensure `setLanguage()` is called before component renders
- Use `window.location.reload()` after language change
- Clear localStorage if issues persist

### Missing translations
- Check `translations/[lang].js` files
- Verify key spelling matches exactly
- Add missing keys following naming convention

## 📚 Full Documentation

See `translations/README.md` for complete documentation.
