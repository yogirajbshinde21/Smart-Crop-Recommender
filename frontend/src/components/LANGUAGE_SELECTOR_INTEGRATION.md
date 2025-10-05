# Language Selector Integration Guide

## Overview

The Language Selector has been fully integrated into the Smart Farmer application with a polished, user-friendly interface that displays languages in their native scripts.

## Features

✅ **Native Language Display**
- English → "English"
- Hindi → "हिंदी" 
- Marathi → "मराठी"

✅ **Visual Feedback**
- Check icon (✓) next to current language
- Highlighted background for active language
- Smooth hover effects

✅ **Responsive Design**
- Navbar integration for desktop
- Mobile-optimized placement
- Drawer menu integration for small screens

✅ **Consistent Styling**
- Matches navbar color scheme (white text on green background)
- Smooth transitions and hover states
- Professional Material-UI design

## Component Variants

### 1. Navbar Variant (Default)

Used in the main navigation bar with white styling to match the AppBar.

```jsx
<LanguageSelector variant="navbar" />
```

**Styling:**
- White text and borders
- Compact size for navbar
- Transparent background with white accents
- Language icon prefix

### 2. Standard Variant

Used in drawer menus, settings pages, or forms with standard Material-UI styling.

```jsx
<LanguageSelector variant="standard" />
```

**Styling:**
- Standard Material-UI colors
- Full width option
- Language icon with each option

## Integration Points

### 1. Desktop Navbar (Right Side)

Located on the right side of the navbar, after the navigation buttons:

```
[Logo] ... [Dashboard] [Recommend] [Compare] [Language Selector]
```

### 2. Mobile Navbar (Right Side)

On mobile screens, appears next to the menu icon:

```
[Menu Icon] [Logo] ... [Language Selector]
```

### 3. Drawer Menu (Mobile)

At the top of the drawer menu, below the header:

```
┌─────────────────┐
│ 🌾 Smart Farmer │
│ Maharashtra AI  │
├─────────────────┤
│ Language Select │
├─────────────────┤
│ Menu Items...   │
```

## Usage Examples

### Basic Import and Use

```jsx
import LanguageSelector from '../components/LanguageSelector';

function MyComponent() {
  return (
    <div>
      {/* Navbar variant */}
      <LanguageSelector variant="navbar" />
      
      {/* Standard variant */}
      <LanguageSelector variant="standard" />
    </div>
  );
}
```

### In Navbar (Integrated)

The LanguageSelector is already integrated into `Navbar.jsx`:

```jsx
import LanguageSelector from './LanguageSelector';

// In the Navbar component
<Box sx={{ ml: 2 }}>
  <LanguageSelector variant="navbar" />
</Box>
```

### In Settings Page

```jsx
import LanguageSelector from '../components/LanguageSelector';
import { Box, Typography, Card, CardContent } from '@mui/material';

function SettingsPage() {
  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Language Settings
        </Typography>
        <LanguageSelector variant="standard" />
      </CardContent>
    </Card>
  );
}
```

### In Form

```jsx
import LanguageSelector from '../components/LanguageSelector';
import { Grid } from '@mui/material';

function UserPreferencesForm() {
  return (
    <form>
      <Grid container spacing={2}>
        <Grid item xs={12} md={6}>
          <LanguageSelector variant="standard" />
        </Grid>
        {/* Other form fields */}
      </Grid>
    </form>
  );
}
```

## Language Configuration

The available languages are defined in `TranslationContext.jsx`:

```javascript
const availableLanguages = [
  { code: 'en', name: 'English', nativeName: 'English' },
  { code: 'hi', name: 'Hindi', nativeName: 'हिंदी' },
  { code: 'mr', name: 'Marathi', nativeName: 'मराठी' }
];
```

### Adding a New Language

1. **Add translation file:**
   ```javascript
   // src/translations/gu.js (Gujarati example)
   export const translations = {
     "navbar.appName": "સ્માર્ટ ખેડૂત",
     // ... more translations
   };
   ```

2. **Update TranslationContext.jsx:**
   ```javascript
   import { gu } from '../translations/gu';
   
   const translations = {
     en, hi, mr,
     gu // Add new language
   };
   
   const availableLanguages = [
     { code: 'en', name: 'English', nativeName: 'English' },
     { code: 'hi', name: 'Hindi', nativeName: 'हिंदी' },
     { code: 'mr', name: 'Marathi', nativeName: 'मराठी' },
     { code: 'gu', name: 'Gujarati', nativeName: 'ગુજરાતી' }
   ];
   ```

3. **The LanguageSelector will automatically show the new language!**

## Styling Customization

### Navbar Variant Styling

```jsx
<LanguageSelector
  variant="navbar"
  sx={{
    // Custom styling
    minWidth: 140,
    '& .MuiOutlinedInput-root': {
      borderRadius: 2,
    }
  }}
/>
```

### Custom Colors

To match different navbar colors, modify the component:

```jsx
// In LanguageSelector.jsx
sx={{
  '& .MuiOutlinedInput-root': {
    color: 'YOUR_COLOR', // Change text color
    '& fieldset': {
      borderColor: 'YOUR_BORDER_COLOR',
    },
  },
}}
```

## User Experience

### Language Change Flow

1. User clicks language selector dropdown
2. Dropdown shows all languages with:
   - Native script names (हिंदी, मराठी, English)
   - English names in parentheses for Hindi/Marathi
   - Check mark on current language
   - Green highlight on current selection
3. User selects new language
4. Application immediately updates all translations
5. Language preference saved to localStorage

### Persistence

The selected language persists across:
- ✅ Page refreshes
- ✅ Browser sessions
- ✅ Tab closures
- ✅ Application restarts

Stored in: `localStorage.getItem('language')`

## Accessibility

- **Keyboard Navigation:** Full keyboard support (Tab, Arrow keys, Enter)
- **Screen Readers:** Proper ARIA labels and roles
- **Focus States:** Clear visual focus indicators
- **Color Contrast:** WCAG AA compliant

## Mobile Responsiveness

### Desktop (>900px)
```
┌─────────────────────────────────────────────────┐
│ [≡] Smart Farmer    [Connected] [Nav] [Lang] │
└─────────────────────────────────────────────────┘
```

### Tablet (600px-900px)
```
┌───────────────────────────────────┐
│ [≡] Smart Farmer  [Status] [Lang] │
└───────────────────────────────────┘
```

### Mobile (<600px)
```
┌─────────────────────────────┐
│ [≡] Smart Farmer     [Lang] │
└─────────────────────────────┘
```

## Testing

### Test Language Switching

1. Open application
2. Click language selector
3. Select "हिंदी" (Hindi)
4. Verify all UI elements translate to Hindi
5. Refresh page
6. Verify language persists
7. Select "मराठी" (Marathi)
8. Verify all UI elements translate to Marathi

### Test Responsive Behavior

1. Desktop view: Language selector in navbar
2. Tablet view: Language selector remains visible
3. Mobile view: Language selector accessible in drawer
4. All breakpoints: Selector remains functional

## Integration Checklist

- ✅ LanguageSelector component created
- ✅ Navbar variant implemented
- ✅ Standard variant implemented
- ✅ Integrated into desktop navbar
- ✅ Integrated into mobile navbar
- ✅ Integrated into drawer menu
- ✅ Native language scripts displayed
- ✅ Visual feedback (check marks)
- ✅ Responsive design
- ✅ localStorage persistence
- ✅ TranslationContext integration
- ✅ Proper styling for dark navbar
- ✅ Hover and focus states

## Troubleshooting

### Language Not Changing

**Issue:** Clicking language doesn't change the UI

**Solutions:**
1. Check TranslationProvider wraps app in main.jsx
2. Verify translation files exist for all languages
3. Check browser console for errors
4. Clear localStorage: `localStorage.clear()`

### Styling Issues

**Issue:** Language selector doesn't match navbar colors

**Solution:**
```jsx
// Ensure using navbar variant
<LanguageSelector variant="navbar" />
```

### Languages Not Showing

**Issue:** Dropdown is empty or shows wrong languages

**Solution:**
1. Check availableLanguages array in TranslationContext
2. Verify all translation files are imported
3. Check for typos in language codes

### Mobile Issues

**Issue:** Language selector not visible on mobile

**Solution:**
```jsx
// Ensure mobile conditional render exists
{isMobile && (
  <Box sx={{ ml: 1 }}>
    <LanguageSelector variant="navbar" />
  </Box>
)}
```

## Best Practices

1. **Always use variant prop:** Specify `variant="navbar"` or `variant="standard"`
2. **Native scripts first:** Display native language names prominently
3. **Visual feedback:** Always show which language is active
4. **Consistent placement:** Keep language selector in same location across views
5. **Accessible labels:** Include English names for non-Latin scripts

## Future Enhancements

Potential improvements:
- [ ] Language search/filter for many languages
- [ ] Flag icons alongside language names
- [ ] Keyboard shortcuts (e.g., Alt+L to open selector)
- [ ] Language auto-detection based on browser locale
- [ ] RTL support for Arabic/Urdu languages
- [ ] Voice-based language selection

## Summary

The Language Selector is now fully integrated into the Smart Farmer application with:
- **3 languages:** English, हिंदी (Hindi), मराठी (Marathi)
- **Native scripts:** Displayed prominently for authenticity
- **Seamless integration:** Works in navbar, drawer, and standalone
- **Professional design:** Matches application aesthetic
- **User-friendly:** Clear visual feedback and smooth interactions

Users can now easily switch languages from any page, with their preference persisting across sessions! 🌍✨
