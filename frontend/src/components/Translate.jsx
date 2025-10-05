import React from 'react';
import { useTranslation } from '../context/TranslationContext';

/**
 * Translate Component
 * 
 * A reusable component for declarative translations using translation keys.
 * Automatically uses the current language from TranslationContext.
 * 
 * @param {Object} props - Component props
 * @param {string} props.tKey - Translation key (e.g., 'navbar.home') - PREFERRED METHOD
 * @param {string} props.children - Translation key (e.g., 'navbar.home') - LEGACY SUPPORT
 * @param {Object} props.params - Optional parameters for string interpolation
 * @param {string} props.fallback - Optional fallback text if translation is missing
 * @param {string} props.as - Optional HTML element to render (default: 'span')
 * @param {Object} props.style - Optional inline styles
 * @param {string} props.className - Optional CSS class name
 * 
 * @example
 * // Preferred usage with tKey prop
 * <Translate tKey="navbar.home" />
 * 
 * @example
 * // Legacy usage with children
 * <Translate>navbar.home</Translate>
 * 
 * @example
 * // With parameters
 * <Translate tKey="greeting.welcome" params={{ name: 'John' }} />
 * 
 * @example
 * // With custom fallback
 * <Translate tKey="navbar.home" fallback="Home" />
 * 
 * @example
 * // With custom element
 * <Translate tKey="dashboard.title" as="h1" />
 * 
 * @example
 * // With styling
 * <Translate tKey="navbar.home" className="title" style={{ color: 'blue' }} />
 */
const Translate = ({ 
  tKey,
  children, 
  params = {}, 
  fallback = null, 
  as = 'span',
  style = {},
  className = '',
  ...rest 
}) => {
  const { t } = useTranslation();
  
  // Accept translation key from either tKey prop or children (for backward compatibility)
  const translationKey = tKey || children;
  
  // Validate that we have a translation key
  if (typeof translationKey !== 'string') {
    console.error('Translate component expects a string as tKey prop or children');
    return fallback || null;
  }

  // Get the translation key
  const key = translationKey.trim();
  
  // Get translated text
  const translatedText = t(key, params);
  
  // Use fallback if translation returns the key itself (meaning not found)
  const displayText = translatedText === key && fallback 
    ? fallback 
    : translatedText;

  // Create the element dynamically
  const Element = as;
  
  return (
    <Element className={className} style={style} {...rest}>
      {displayText}
    </Element>
  );
};

/**
 * TranslateHTML Component
 * 
 * Similar to Translate but renders HTML content safely.
 * Useful for translations that contain HTML markup.
 * 
 * @param {Object} props - Component props
 * @param {string} props.children - Translation key
 * @param {Object} props.params - Optional parameters for string interpolation
 * @param {string} props.as - Optional HTML element to render (default: 'div')
 * 
 * @example
 * <TranslateHTML>content.richText</TranslateHTML>
 */
export const TranslateHTML = ({ 
  children, 
  params = {}, 
  as = 'div',
  ...rest 
}) => {
  const { t } = useTranslation();
  
  if (typeof children !== 'string') {
    console.error('TranslateHTML component expects a string as children (translation key)');
    return null;
  }

  const translationKey = children.trim();
  const translatedText = t(translationKey, params);
  
  const Element = as;
  
  return (
    <Element 
      {...rest}
      dangerouslySetInnerHTML={{ __html: translatedText }}
    />
  );
};

/**
 * TranslateWithContext Component
 * 
 * Provides additional context information along with translation.
 * Useful for debugging or displaying multiple language versions.
 * 
 * @param {Object} props - Component props
 * @param {string} props.children - Translation key
 * @param {boolean} props.showKey - Whether to show the translation key
 * @param {boolean} props.showLanguage - Whether to show current language
 * 
 * @example
 * <TranslateWithContext showKey>navbar.home</TranslateWithContext>
 * // Output: "Home (navbar.home)"
 */
export const TranslateWithContext = ({ 
  children, 
  showKey = false, 
  showLanguage = false,
  ...rest 
}) => {
  const { t, language } = useTranslation();
  
  if (typeof children !== 'string') {
    return null;
  }

  const translationKey = children.trim();
  const translatedText = t(translationKey);
  
  let displayText = translatedText;
  
  if (showKey) {
    displayText += ` (${translationKey})`;
  }
  
  if (showLanguage) {
    displayText += ` [${language}]`;
  }
  
  return <span {...rest}>{displayText}</span>;
};

/**
 * TranslatePlural Component
 * 
 * Handles plural translations based on count.
 * Expects translation keys with .singular and .plural suffixes.
 * 
 * @param {Object} props - Component props
 * @param {string} props.children - Base translation key (without .singular/.plural)
 * @param {number} props.count - Count to determine singular/plural
 * @param {Object} props.params - Additional parameters for interpolation
 * 
 * @example
 * // Translation keys: "items.singular": "You have {count} item"
 * //                   "items.plural": "You have {count} items"
 * <TranslatePlural count={1} params={{ count: 1 }}>items</TranslatePlural>
 * // Output: "You have 1 item"
 * 
 * <TranslatePlural count={5} params={{ count: 5 }}>items</TranslatePlural>
 * // Output: "You have 5 items"
 */
export const TranslatePlural = ({ 
  children, 
  count = 0, 
  params = {},
  ...rest 
}) => {
  const { t, hasTranslation } = useTranslation();
  
  if (typeof children !== 'string') {
    return null;
  }

  const baseKey = children.trim();
  const singularKey = `${baseKey}.singular`;
  const pluralKey = `${baseKey}.plural`;
  
  // Determine which key to use
  const translationKey = count === 1 ? singularKey : pluralKey;
  
  // Check if the key exists, otherwise fall back to base key
  const finalKey = hasTranslation(translationKey) ? translationKey : baseKey;
  
  const translatedText = t(finalKey, { count, ...params });
  
  return <span {...rest}>{translatedText}</span>;
};

/**
 * TranslateDate Component
 * 
 * Translates and formats dates according to current language.
 * 
 * @param {Object} props - Component props
 * @param {Date|string|number} props.date - Date to format
 * @param {Object} props.options - Intl.DateTimeFormat options
 * 
 * @example
 * <TranslateDate date={new Date()} options={{ dateStyle: 'full' }} />
 */
export const TranslateDate = ({ 
  date, 
  options = { dateStyle: 'medium' },
  ...rest 
}) => {
  const { language } = useTranslation();
  
  try {
    const dateObj = date instanceof Date ? date : new Date(date);
    const formatter = new Intl.DateTimeFormat(language, options);
    const formattedDate = formatter.format(dateObj);
    
    return <span {...rest}>{formattedDate}</span>;
  } catch (error) {
    console.error('Error formatting date:', error);
    return <span {...rest}>{String(date)}</span>;
  }
};

/**
 * TranslateNumber Component
 * 
 * Translates and formats numbers according to current language.
 * 
 * @param {Object} props - Component props
 * @param {number} props.value - Number to format
 * @param {Object} props.options - Intl.NumberFormat options
 * 
 * @example
 * <TranslateNumber value={1234.56} options={{ style: 'currency', currency: 'INR' }} />
 */
export const TranslateNumber = ({ 
  value, 
  options = {},
  ...rest 
}) => {
  const { language } = useTranslation();
  
  try {
    const formatter = new Intl.NumberFormat(language, options);
    const formattedNumber = formatter.format(value);
    
    return <span {...rest}>{formattedNumber}</span>;
  } catch (error) {
    console.error('Error formatting number:', error);
    return <span {...rest}>{String(value)}</span>;
  }
};

// Export both as default and named export for flexibility
export { Translate };
export default Translate;
