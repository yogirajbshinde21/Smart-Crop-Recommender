import { en, hi, mr, availableLanguages, defaultLanguage } from './translations/index.js';

// Translation store
const translations = {
  en,
  hi,
  mr
};

// Current language state (default)
let currentLanguage = defaultLanguage;

/**
 * Get the current language
 * @returns {string} Current language code
 */
export const getCurrentLanguage = () => currentLanguage;

/**
 * Set the current language
 * @param {string} languageCode - Language code (en, hi, mr)
 */
export const setLanguage = (languageCode) => {
  if (translations[languageCode]) {
    currentLanguage = languageCode;
    // Store in localStorage for persistence
    localStorage.setItem('language', languageCode);
  }
};

/**
 * Initialize language from localStorage or use default
 */
export const initLanguage = () => {
  const savedLanguage = localStorage.getItem('language');
  if (savedLanguage && translations[savedLanguage]) {
    currentLanguage = savedLanguage;
  }
};

/**
 * Get translated text for a key
 * @param {string} key - Translation key (e.g., 'navbar.home')
 * @param {string} lang - Optional language code, uses current language if not provided
 * @returns {string} Translated text or key if translation not found
 */
export const t = (key, lang = null) => {
  const language = lang || currentLanguage;
  const translation = translations[language];
  
  if (translation && translation[key]) {
    return translation[key];
  }
  
  // Fallback to English if translation not found
  if (language !== 'en' && translations.en[key]) {
    return translations.en[key];
  }
  
  // Return key if no translation found
  console.warn(`Translation key not found: ${key}`);
  return key;
};

/**
 * Get all available languages
 * @returns {Array} Array of language objects
 */
export const getAvailableLanguages = () => availableLanguages;

/**
 * Get all translations for current language
 * @returns {Object} Translation object
 */
export const getAllTranslations = () => translations[currentLanguage];

/**
 * Check if a translation key exists
 * @param {string} key - Translation key
 * @param {string} lang - Optional language code
 * @returns {boolean}
 */
export const hasTranslation = (key, lang = null) => {
  const language = lang || currentLanguage;
  return translations[language] && translations[language][key] !== undefined;
};

// Initialize language on module load
initLanguage();

// Export for use in components
export { availableLanguages, defaultLanguage };
