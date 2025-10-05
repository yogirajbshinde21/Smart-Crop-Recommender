# Translate Component Documentation

## Overview

The `Translate` component provides a declarative way to handle translations in React components. Instead of using the `t()` function, you can use JSX tags for cleaner, more readable code.

## Installation

The component is already available at `src/components/Translate.jsx`.

## Basic Usage

### Import

```jsx
import Translate from '../components/Translate';
```

### Simple Translation

```jsx
<Translate>navbar.home</Translate>
// Output: "Home" (or translated text based on current language)
```

### In a Component

```jsx
import React from 'react';
import Translate from '../components/Translate';
import { Typography } from '@mui/material';

function MyComponent() {
  return (
    <div>
      <h1>
        <Translate>dashboard.title</Translate>
      </h1>
      <p>
        <Translate>dashboard.subtitle</Translate>
      </p>
    </div>
  );
}
```

## Component Variants

### 1. Translate (Main Component)

Basic translation component with multiple options.

#### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | string | required | Translation key |
| `params` | object | {} | Parameters for interpolation |
| `fallback` | string | null | Fallback text if translation missing |
| `as` | string | 'span' | HTML element to render |
| `style` | object | {} | Inline styles |
| `className` | string | '' | CSS class name |

#### Examples

**Basic:**
```jsx
<Translate>navbar.home</Translate>
```

**With Custom Element:**
```jsx
<Translate as="h1">dashboard.title</Translate>
<Translate as="p">dashboard.subtitle</Translate>
<Translate as="button">common.submit</Translate>
```

**With Styling:**
```jsx
<Translate className="title" style={{ color: 'blue', fontSize: '24px' }}>
  navbar.home
</Translate>
```

**With Fallback:**
```jsx
<Translate fallback="Home Page">navbar.home</Translate>
```

**With Parameters:**
```jsx
{/* Translation: "Welcome back, {name}!" */}
<Translate params={{ name: 'John' }}>greeting.welcome</Translate>
// Output: "Welcome back, John!"
```

### 2. TranslateHTML

Renders translations containing HTML markup safely.

#### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | string | required | Translation key |
| `params` | object | {} | Parameters for interpolation |
| `as` | string | 'div' | HTML element to render |

#### Examples

```jsx
import { TranslateHTML } from '../components/Translate';

{/* Translation: "Visit <a href='/about'>our page</a>" */}
<TranslateHTML>content.richText</TranslateHTML>
```

**⚠️ Warning:** Only use with trusted translation content to avoid XSS attacks.

### 3. TranslateWithContext

Shows translation with additional context (useful for debugging).

#### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | string | required | Translation key |
| `showKey` | boolean | false | Show translation key |
| `showLanguage` | boolean | false | Show current language |

#### Examples

```jsx
import { TranslateWithContext } from '../components/Translate';

<TranslateWithContext showKey>navbar.home</TranslateWithContext>
// Output: "Home (navbar.home)"

<TranslateWithContext showLanguage>navbar.home</TranslateWithContext>
// Output: "Home [en]"

<TranslateWithContext showKey showLanguage>navbar.home</TranslateWithContext>
// Output: "Home (navbar.home) [en]"
```

### 4. TranslatePlural

Handles singular/plural translations based on count.

#### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | string | required | Base translation key |
| `count` | number | 0 | Count for plural determination |
| `params` | object | {} | Additional parameters |

#### Setup

Add to your translation files:
```javascript
// In en.js, hi.js, mr.js
{
  "items.singular": "You have {count} item",
  "items.plural": "You have {count} items"
}
```

#### Examples

```jsx
import { TranslatePlural } from '../components/Translate';

<TranslatePlural count={1} params={{ count: 1 }}>items</TranslatePlural>
// Output: "You have 1 item"

<TranslatePlural count={5} params={{ count: 5 }}>items</TranslatePlural>
// Output: "You have 5 items"
```

### 5. TranslateDate

Formats dates according to current language locale.

#### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `date` | Date\|string\|number | required | Date to format |
| `options` | object | { dateStyle: 'medium' } | Intl.DateTimeFormat options |

#### Examples

```jsx
import { TranslateDate } from '../components/Translate';

<TranslateDate date={new Date()} />
// Output: "Jan 15, 2025" (English)
// Output: "१५ जन, २०२५" (Hindi)

<TranslateDate 
  date={new Date()} 
  options={{ dateStyle: 'full' }} 
/>
// Output: "Monday, January 15, 2025"

<TranslateDate 
  date="2025-01-15" 
  options={{ year: 'numeric', month: 'long', day: 'numeric' }} 
/>
```

### 6. TranslateNumber

Formats numbers according to current language locale.

#### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `value` | number | required | Number to format |
| `options` | object | {} | Intl.NumberFormat options |

#### Examples

```jsx
import { TranslateNumber } from '../components/Translate';

<TranslateNumber value={1234.56} />
// Output: "1,234.56" (English)

<TranslateNumber 
  value={1234.56} 
  options={{ style: 'currency', currency: 'INR' }} 
/>
// Output: "₹1,234.56"

<TranslateNumber 
  value={0.85} 
  options={{ style: 'percent' }} 
/>
// Output: "85%"

<TranslateNumber 
  value={1000000} 
  options={{ notation: 'compact' }} 
/>
// Output: "1M"
```

## Real-World Examples

### Example 1: Navigation Menu

```jsx
import React from 'react';
import Translate from '../components/Translate';
import { Button } from '@mui/material';

function Navigation() {
  return (
    <nav>
      <Button>
        <Translate>navbar.dashboard</Translate>
      </Button>
      <Button>
        <Translate>navbar.cropRecommendation</Translate>
      </Button>
      <Button>
        <Translate>navbar.nutrientAnalysis</Translate>
      </Button>
    </nav>
  );
}
```

### Example 2: Form Labels

```jsx
import React from 'react';
import Translate from '../components/Translate';
import { TextField, Button } from '@mui/material';

function LoginForm() {
  return (
    <form>
      <TextField
        label={<Translate>form.email</Translate>}
        fullWidth
      />
      <TextField
        label={<Translate>form.password</Translate>}
        type="password"
        fullWidth
      />
      <Button type="submit">
        <Translate>common.submit</Translate>
      </Button>
    </form>
  );
}
```

### Example 3: Page Headers

```jsx
import React from 'react';
import Translate from '../components/Translate';
import { Typography, Box } from '@mui/material';

function PageHeader() {
  return (
    <Box>
      <Typography variant="h4">
        <Translate as="span">crop.title</Translate>
      </Typography>
      <Typography variant="body1" color="text.secondary">
        <Translate as="span">crop.subtitle</Translate>
      </Typography>
    </Box>
  );
}
```

### Example 4: Alert Messages

```jsx
import React from 'react';
import Translate from '../components/Translate';
import { Alert } from '@mui/material';

function Notifications({ type }) {
  return (
    <div>
      <Alert severity="error">
        <Translate>crop.errorFillFields</Translate>
      </Alert>
      <Alert severity="success">
        <Translate>common.success</Translate>
      </Alert>
    </div>
  );
}
```

### Example 5: Dynamic Content

```jsx
import React from 'react';
import Translate from '../components/Translate';
import { Card, CardContent, Typography } from '@mui/material';

function UserGreeting({ username }) {
  return (
    <Card>
      <CardContent>
        <Typography>
          <Translate params={{ name: username }}>
            greeting.welcome
          </Translate>
        </Typography>
      </CardContent>
    </Card>
  );
}
```

### Example 6: List Items

```jsx
import React from 'react';
import Translate from '../components/Translate';
import { List, ListItem, ListItemText } from '@mui/material';

function FeatureList() {
  const features = [
    'navbar.cropRecommendation',
    'navbar.nutrientAnalysis',
    'navbar.waterQuality',
    'navbar.cropComparison'
  ];

  return (
    <List>
      {features.map((feature) => (
        <ListItem key={feature}>
          <ListItemText>
            <Translate>{feature}</Translate>
          </ListItemText>
        </ListItem>
      ))}
    </List>
  );
}
```

### Example 7: Conditional Messages

```jsx
import React from 'react';
import Translate from '../components/Translate';
import { TranslatePlural } from '../components/Translate';
import { Typography } from '@mui/material';

function ItemCounter({ count }) {
  return (
    <Typography>
      <TranslatePlural count={count} params={{ count }}>
        items
      </TranslatePlural>
    </Typography>
  );
}
```

### Example 8: Rich Content

```jsx
import React from 'react';
import { TranslateHTML } from '../components/Translate';
import { Box } from '@mui/material';

function HelpContent() {
  return (
    <Box>
      {/* Translation contains HTML: "Click <b>here</b> for help" */}
      <TranslateHTML>help.instructions</TranslateHTML>
    </Box>
  );
}
```

### Example 9: Economic Data

```jsx
import React from 'react';
import { TranslateNumber } from '../components/Translate';
import Translate from '../components/Translate';
import { Card, CardContent, Typography } from '@mui/material';

function EconomicCard({ revenue, profit }) {
  return (
    <Card>
      <CardContent>
        <Typography variant="h6">
          <Translate>economic.revenue</Translate>
        </Typography>
        <Typography variant="h4">
          <TranslateNumber 
            value={revenue} 
            options={{ style: 'currency', currency: 'INR' }}
          />
        </Typography>
        
        <Typography variant="h6" sx={{ mt: 2 }}>
          <Translate>economic.profit</Translate>
        </Typography>
        <Typography variant="h4">
          <TranslateNumber 
            value={profit} 
            options={{ style: 'currency', currency: 'INR' }}
          />
        </Typography>
      </CardContent>
    </Card>
  );
}
```

### Example 10: Date Formatting

```jsx
import React from 'react';
import { TranslateDate } from '../components/Translate';
import Translate from '../components/Translate';
import { Typography } from '@mui/material';

function WeatherCard({ date, temperature }) {
  return (
    <div>
      <Typography variant="h6">
        <Translate>weather.currentWeather</Translate>
      </Typography>
      <Typography variant="body2">
        <TranslateDate 
          date={date} 
          options={{ dateStyle: 'full' }}
        />
      </Typography>
    </div>
  );
}
```

## Comparison: Hook vs Component

### Using Hook (t function)

```jsx
import { useTranslation } from '../context/TranslationContext';

function MyComponent() {
  const { t } = useTranslation();
  
  return (
    <div>
      <h1>{t('navbar.home')}</h1>
      <p>{t('dashboard.subtitle')}</p>
    </div>
  );
}
```

### Using Component

```jsx
import Translate from '../components/Translate';

function MyComponent() {
  return (
    <div>
      <h1><Translate>navbar.home</Translate></h1>
      <p><Translate>dashboard.subtitle</Translate></p>
    </div>
  );
}
```

## When to Use Which?

### Use `<Translate>` Component When:
- ✅ Writing JSX-heavy code
- ✅ Need cleaner, more declarative syntax
- ✅ Working with components that expect ReactNode children
- ✅ Want to avoid string interpolation in JSX

### Use `t()` Function When:
- ✅ Need translations in JavaScript logic
- ✅ Computing values or variables
- ✅ Working with props that expect strings
- ✅ Need better performance (no extra component wrapper)

## Best Practices

1. **Keep Keys Simple**: Use the component for simple translations
   ```jsx
   ✅ <Translate>navbar.home</Translate>
   ❌ <Translate>{computedKey}</Translate> // Use t() instead
   ```

2. **Use Semantic HTML**: Leverage the `as` prop
   ```jsx
   ✅ <Translate as="h1">dashboard.title</Translate>
   ❌ <h1><Translate>dashboard.title</Translate></h1>
   ```

3. **Provide Fallbacks**: For user-generated or dynamic content
   ```jsx
   <Translate fallback="Default Text">user.customField</Translate>
   ```

4. **Combine with Material-UI**: Works seamlessly
   ```jsx
   <Typography variant="h4">
     <Translate>crop.title</Translate>
   </Typography>
   ```

5. **Use Appropriate Variants**: Choose the right component for the job
   ```jsx
   // For HTML content
   <TranslateHTML>content.richText</TranslateHTML>
   
   // For plural forms
   <TranslatePlural count={items.length}>items</TranslatePlural>
   
   // For dates
   <TranslateDate date={new Date()} />
   ```

## Performance Considerations

- The `Translate` component uses React context, which re-renders when language changes
- Each `<Translate>` adds a wrapper element (customizable with `as` prop)
- For large lists, consider using `t()` function with `useMemo`

```jsx
// For better performance in lists
const translatedItems = useMemo(() => 
  items.map(item => ({ ...item, name: t(`items.${item.key}`) })),
  [items, t]
);
```

## TypeScript Support

For TypeScript projects, you can add type definitions:

```typescript
interface TranslateProps {
  children: string;
  params?: Record<string, any>;
  fallback?: string;
  as?: keyof JSX.IntrinsicElements;
  style?: React.CSSProperties;
  className?: string;
}
```

## Troubleshooting

### Translation Not Showing

**Problem:** Component displays the key instead of translation

**Solution:** 
- Check if key exists in translation files
- Verify TranslationProvider wraps your app
- Check browser console for warnings

### Styling Not Applied

**Problem:** Custom element or styling not working

**Solution:**
```jsx
// Make sure to use 'as' prop correctly
<Translate as="h1" className="my-class" style={{ color: 'red' }}>
  navbar.home
</Translate>
```

### Component Children Error

**Problem:** "Translate component expects a string as children"

**Solution:**
```jsx
// ❌ Wrong
<Translate>{someVariable}</Translate>

// ✅ Correct
<Translate>navbar.home</Translate>

// ✅ Or use t() for variables
{t(someVariable)}
```

## Summary

The `Translate` component family provides a powerful, flexible way to handle translations declaratively in React:

- **Translate**: Basic component for simple translations
- **TranslateHTML**: For HTML-rich content
- **TranslateWithContext**: For debugging
- **TranslatePlural**: For singular/plural forms
- **TranslateDate**: For date formatting
- **TranslateNumber**: For number formatting

Use them to create cleaner, more maintainable multilingual React applications! 🌍
