import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { en } from '../translations/en';
import { hi } from '../translations/hi';
import { mr } from '../translations/mr';
import { kn } from '../translations/kn';
import { ta } from '../translations/ta';
import { te } from '../translations/te';
import { bn } from '../translations/bn';
import { gu } from '../translations/gu';

// Translation store
const translations = {
  en,
  hi,
  mr,
  kn,
  ta,
  te,
  bn,
  gu
};

// Available languages
const availableLanguages = [
  { code: 'en', name: 'English', nativeName: 'English' },
  { code: 'hi', name: 'Hindi', nativeName: 'हिंदी' },
  { code: 'mr', name: 'Marathi', nativeName: 'मराठी' },
  { code: 'kn', name: 'Kannada', nativeName: 'ಕನ್ನಡ' },
  { code: 'ta', name: 'Tamil', nativeName: 'தமிழ்' },
  { code: 'te', name: 'Telugu', nativeName: 'తెలుగు' },
  { code: 'bn', name: 'Bengali', nativeName: 'বাংলা' },
  { code: 'gu', name: 'Gujarati', nativeName: 'ગુજરાતી' }
];

// Create Translation Context
const TranslationContext = createContext(undefined);

/**
 * Translation Provider Component
 * Wraps the application and provides translation functionality to all children
 */
export const TranslationProvider = ({ children, defaultLanguage = 'en' }) => {
  // Initialize language from localStorage or use default
  const [currentLanguage, setCurrentLanguage] = useState(() => {
    const savedLanguage = localStorage.getItem('language');
    if (savedLanguage && translations[savedLanguage]) {
      return savedLanguage;
    }
    return defaultLanguage;
  });

  // Get current language translations
  const currentTranslations = translations[currentLanguage];

  /**
   * Change the current language
   * @param {string} languageCode - Language code (en, hi, mr)
   */
  const changeLanguage = useCallback((languageCode) => {
    if (translations[languageCode]) {
      setCurrentLanguage(languageCode);
      localStorage.setItem('language', languageCode);
    } else {
      console.warn(`Language '${languageCode}' is not available. Available languages:`, Object.keys(translations));
    }
  }, []);

  /**
   * Get translated text for a key
   * @param {string} key - Translation key (e.g., 'navbar.home')
   * @param {Object} params - Optional parameters for string interpolation
   * @returns {string} Translated text or key if translation not found
   */
  const t = useCallback((key, params = {}) => {
    let translation = currentTranslations[key];
    
    // Fallback to English if translation not found
    if (!translation && currentLanguage !== 'en') {
      translation = translations.en[key];
    }
    
    // If still not found, return the key
    if (!translation) {
      console.warn(`Translation key not found: ${key}`);
      return key;
    }

    // Simple parameter interpolation (e.g., "Hello {name}" with params={name: "John"})
    if (params && Object.keys(params).length > 0) {
      return translation.replace(/\{(\w+)\}/g, (match, paramKey) => {
        return params[paramKey] !== undefined ? params[paramKey] : match;
      });
    }

    return translation;
  }, [currentLanguage, currentTranslations]);

  /**
   * Check if a translation key exists
   * @param {string} key - Translation key
   * @returns {boolean}
   */
  const hasTranslation = useCallback((key) => {
    return currentTranslations[key] !== undefined;
  }, [currentTranslations]);

  /**
   * Get all translations for current language
   * @returns {Object} Translation object
   */
  const getAllTranslations = useCallback(() => {
    return currentTranslations;
  }, [currentTranslations]);

  /**
   * Get translation for a specific language (without changing current language)
   * @param {string} key - Translation key
   * @param {string} languageCode - Language code
   * @returns {string}
   */
  const getTranslationForLanguage = useCallback((key, languageCode) => {
    const langTranslations = translations[languageCode];
    if (langTranslations && langTranslations[key]) {
      return langTranslations[key];
    }
    return key;
  }, []);

  // Persist language changes to localStorage
  useEffect(() => {
    localStorage.setItem('language', currentLanguage);
  }, [currentLanguage]);

  const value = {
    // Current state
    language: currentLanguage,
    translations: currentTranslations,
    availableLanguages,
    
    // Functions
    changeLanguage,
    t,
    hasTranslation,
    getAllTranslations,
    getTranslationForLanguage
  };

  return (
    <TranslationContext.Provider value={value}>
      {children}
    </TranslationContext.Provider>
  );
};

/**
 * Custom hook to use translations in components
 * @returns {Object} Translation context object
 * 
 * @example
 * const { t, language, changeLanguage } = useTranslation();
 * 
 * // Use translation
 * <h1>{t('navbar.home')}</h1>
 * 
 * // Change language
 * changeLanguage('hi');
 * 
 * // Get current language
 * console.log(language); // 'en', 'hi', or 'mr'
 */
export const useTranslation = () => {
  const context = useContext(TranslationContext);
  
  if (context === undefined) {
    throw new Error('useTranslation must be used within a TranslationProvider');
  }
  
  return context;
};

// Export for convenience
export { availableLanguages };
export default TranslationContext;
