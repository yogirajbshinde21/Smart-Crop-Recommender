# Translation Context & Hook Documentation

## Overview

The translation system uses React Context API to provide a centralized, efficient way to manage multilingual content across the application. It includes a custom `useTranslation` hook for easy access to translations and language switching functionality.

## Architecture

```
TranslationContext.jsx
├── TranslationProvider (Context Provider)
├── useTranslation (Custom Hook)
└── Translation Store (en, hi, mr)
```

## Setup

### 1. Provider Integration

The `TranslationProvider` is already integrated in `main.jsx`:

```jsx
import { TranslationProvider } from './context/TranslationContext';

ReactDOM.createRoot(document.getElementById('root')).render(
  <TranslationProvider defaultLanguage="en">
    <App />
  </TranslationProvider>
);
```

### 2. Using the Hook

Import and use the `useTranslation` hook in any component:

```jsx
import { useTranslation } from '../context/TranslationContext';

function MyComponent() {
  const { t, language, changeLanguage, availableLanguages } = useTranslation();
  
  return (
    <div>
      <h1>{t('navbar.home')}</h1>
      <button onClick={() => changeLanguage('hi')}>
        Switch to Hindi
      </button>
    </div>
  );
}
```

## API Reference

### useTranslation Hook

Returns an object with the following properties:

#### Properties

- **`language`** (string): Current active language code ('en', 'hi', 'mr')
- **`translations`** (object): Current language's full translation object
- **`availableLanguages`** (array): List of all available languages

#### Methods

##### `t(key, params?)`
Get translated text for a key with optional parameter interpolation.

**Parameters:**
- `key` (string): Translation key (e.g., 'navbar.home')
- `params` (object, optional): Parameters for string interpolation

**Returns:** (string) Translated text

**Examples:**
```jsx
// Simple translation
t('navbar.home') // "Home"

// With parameter interpolation
t('welcome.message') // If translation is "Hello {name}"
t('welcome.message', { name: 'John' }) // "Hello John"
```

##### `changeLanguage(languageCode)`
Change the current language.

**Parameters:**
- `languageCode` (string): Language code ('en', 'hi', 'mr')

**Example:**
```jsx
changeLanguage('hi'); // Switch to Hindi
changeLanguage('mr'); // Switch to Marathi
changeLanguage('en'); // Switch to English
```

##### `hasTranslation(key)`
Check if a translation key exists in the current language.

**Parameters:**
- `key` (string): Translation key

**Returns:** (boolean)

**Example:**
```jsx
if (hasTranslation('navbar.home')) {
  console.log('Translation exists');
}
```

##### `getAllTranslations()`
Get the complete translation object for the current language.

**Returns:** (object) All translations

**Example:**
```jsx
const allTranslations = getAllTranslations();
console.log(allTranslations);
```

##### `getTranslationForLanguage(key, languageCode)`
Get translation for a specific language without changing the current language.

**Parameters:**
- `key` (string): Translation key
- `languageCode` (string): Target language code

**Returns:** (string) Translated text

**Example:**
```jsx
const hindiText = getTranslationForLanguage('navbar.home', 'hi');
const marathiText = getTranslationForLanguage('navbar.home', 'mr');
```

## Usage Examples

### Basic Component

```jsx
import React from 'react';
import { useTranslation } from '../context/TranslationContext';
import { Typography, Button } from '@mui/material';

function WelcomeScreen() {
  const { t } = useTranslation();
  
  return (
    <div>
      <Typography variant="h4">
        {t('dashboard.welcome')}
      </Typography>
      <Typography variant="body1">
        {t('dashboard.subtitle')}
      </Typography>
      <Button variant="contained">
        {t('common.submit')}
      </Button>
    </div>
  );
}
```

### Form with Translations

```jsx
import React, { useState } from 'react';
import { useTranslation } from '../context/TranslationContext';
import { TextField, Button, Alert } from '@mui/material';

function LoginForm() {
  const { t } = useTranslation();
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');
  
  return (
    <form>
      <TextField
        label={t('form.email')}
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        fullWidth
      />
      {error && (
        <Alert severity="error">
          {t('form.errorRequired')}
        </Alert>
      )}
      <Button type="submit" variant="contained">
        {t('common.submit')}
      </Button>
    </form>
  );
}
```

### Language Switcher

```jsx
import React from 'react';
import { useTranslation } from '../context/TranslationContext';
import { Select, MenuItem } from '@mui/material';

function LanguageSwitcher() {
  const { language, changeLanguage, availableLanguages } = useTranslation();
  
  return (
    <Select
      value={language}
      onChange={(e) => changeLanguage(e.target.value)}
    >
      {availableLanguages.map((lang) => (
        <MenuItem key={lang.code} value={lang.code}>
          {lang.nativeName}
        </MenuItem>
      ))}
    </Select>
  );
}
```

### Conditional Rendering Based on Language

```jsx
import React from 'react';
import { useTranslation } from '../context/TranslationContext';
import { Typography } from '@mui/material';

function LocalizedContent() {
  const { language, t } = useTranslation();
  
  return (
    <div>
      <Typography variant="h4">
        {t('page.title')}
      </Typography>
      
      {language === 'mr' && (
        <Typography variant="caption">
          विशेष मराठी सामग्री
        </Typography>
      )}
      
      {language === 'hi' && (
        <Typography variant="caption">
          विशेष हिंदी सामग्री
        </Typography>
      )}
    </div>
  );
}
```

### Multi-language Display

```jsx
import React from 'react';
import { useTranslation } from '../context/TranslationContext';
import { Card, CardContent, Typography } from '@mui/material';

function MultiLanguageCard() {
  const { getTranslationForLanguage } = useTranslation();
  
  return (
    <Card>
      <CardContent>
        <Typography variant="h6">English</Typography>
        <Typography>{getTranslationForLanguage('navbar.home', 'en')}</Typography>
        
        <Typography variant="h6">हिंदी</Typography>
        <Typography>{getTranslationForLanguage('navbar.home', 'hi')}</Typography>
        
        <Typography variant="h6">मराठी</Typography>
        <Typography>{getTranslationForLanguage('navbar.home', 'mr')}</Typography>
      </CardContent>
    </Card>
  );
}
```

### Dynamic Parameter Interpolation

```jsx
import React from 'react';
import { useTranslation } from '../context/TranslationContext';
import { Typography } from '@mui/material';

function UserGreeting({ username, itemCount }) {
  const { t } = useTranslation();
  
  return (
    <div>
      {/* Translation: "Welcome back, {name}!" */}
      <Typography>
        {t('greeting.welcome', { name: username })}
      </Typography>
      
      {/* Translation: "You have {count} items" */}
      <Typography>
        {t('inventory.count', { count: itemCount })}
      </Typography>
    </div>
  );
}
```

## Advanced Features

### Automatic Language Persistence

The selected language is automatically saved to `localStorage` and restored on app reload:

```jsx
// Language is automatically saved when changed
changeLanguage('hi');

// On next visit, 'hi' is automatically restored
```

### Fallback to English

If a translation key doesn't exist in the current language, the system automatically falls back to English:

```jsx
// If 'new.feature' exists in English but not in Hindi
const { t, language } = useTranslation();
console.log(language); // 'hi'
console.log(t('new.feature')); // Returns English translation
```

### Console Warnings for Missing Keys

Missing translation keys are logged to the console during development:

```jsx
t('nonexistent.key'); // Console: "Translation key not found: nonexistent.key"
```

## Integration with Existing Components

### Navbar Integration

```jsx
import React from 'react';
import { useTranslation } from '../context/TranslationContext';
import LanguageSelector from './LanguageSelector';

function Navbar() {
  const { t } = useTranslation();
  
  return (
    <nav>
      <h1>{t('navbar.appName')}</h1>
      <LanguageSelector />
    </nav>
  );
}
```

### Dashboard Integration

```jsx
import React from 'react';
import { useTranslation } from '../context/TranslationContext';

function Dashboard() {
  const { t } = useTranslation();
  
  return (
    <div>
      <h1>{t('dashboard.title')}</h1>
      <p>{t('dashboard.subtitle')}</p>
      {/* ... rest of component */}
    </div>
  );
}
```

## Best Practices

1. **Always use the hook**: Don't import translation files directly
   ```jsx
   // ✅ Good
   const { t } = useTranslation();
   
   // ❌ Bad
   import { en } from '../translations/en';
   ```

2. **Destructure only what you need**: Optimize performance
   ```jsx
   // ✅ Good - only get what you need
   const { t, changeLanguage } = useTranslation();
   
   // ❌ Less optimal - getting everything
   const context = useTranslation();
   ```

3. **Use memoization for expensive operations**: Prevent unnecessary re-renders
   ```jsx
   import { useMemo } from 'react';
   
   const translatedItems = useMemo(() => {
     return items.map(item => ({
       ...item,
       name: t(`items.${item.key}`)
     }));
   }, [items, t]);
   ```

4. **Handle dynamic content carefully**: Use parameter interpolation
   ```jsx
   // ✅ Good
   t('message.greeting', { name: userName })
   
   // ❌ Bad - hard to translate
   `${t('message.hello')} ${userName}`
   ```

## Performance Considerations

- **Context Re-renders**: The context only re-renders when language changes
- **Memoized Functions**: Translation functions are memoized with `useCallback`
- **Lazy Loading**: Translation objects are loaded only when needed
- **LocalStorage**: Language preference persists across sessions

## Troubleshooting

### Hook Error: "useTranslation must be used within a TranslationProvider"

**Solution**: Ensure your component is wrapped in `TranslationProvider`:
```jsx
// In main.jsx
<TranslationProvider>
  <App />
</TranslationProvider>
```

### Translations Not Updating

**Solution**: Make sure you're using the `t` function from the hook:
```jsx
const { t } = useTranslation(); // Re-runs when language changes
```

### Missing Translation Keys

**Solution**: Check the translation files and ensure the key exists:
```jsx
const { hasTranslation } = useTranslation();
if (!hasTranslation('some.key')) {
  console.log('Key not found - add to translation files');
}
```

## Migration from Old System

If migrating from the old `translations.js` utility:

```jsx
// Old way
import { t, setLanguage } from '../utils/translations';

// New way
import { useTranslation } from '../context/TranslationContext';
const { t, changeLanguage } = useTranslation();
```

## Summary

The Translation Context provides:
- ✅ Centralized language management
- ✅ React Context-based state
- ✅ Custom hook for easy access
- ✅ Automatic persistence
- ✅ Fallback support
- ✅ Parameter interpolation
- ✅ Performance optimization
- ✅ Type-safe (when using TypeScript)

Use `useTranslation()` hook in all components for consistent, efficient multilingual support!
