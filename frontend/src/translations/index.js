// Export all translation files
export { en } from './en.js';
export { hi } from './hi.js';
export { mr } from './mr.js';
export { kn } from './kn.js';
export { ta } from './ta.js';
export { te } from './te.js';
export { bn } from './bn.js';
export { gu } from './gu.js';

// Available languages
export const availableLanguages = [
  { code: 'en', name: 'English', nativeName: 'English' },
  { code: 'hi', name: 'Hindi', nativeName: 'हिंदी' },
  { code: 'mr', name: 'Marathi', nativeName: 'मराठी' },
  { code: 'kn', name: 'Kannada', nativeName: 'ಕನ್ನಡ' },
  { code: 'ta', name: 'Tamil', nativeName: 'தமிழ்' },
  { code: 'te', name: 'Telugu', nativeName: 'తెలుగు' },
  { code: 'bn', name: 'Bengali', nativeName: 'বাংলা' },
  { code: 'gu', name: 'Gujarati', nativeName: 'ગુજરાતી' }
];

// Default language
export const defaultLanguage = 'en';

// Helper function to get translations for a specific language
export const getTranslations = (languageCode) => {
  switch (languageCode) {
    case 'hi':
      return require('./hi.js').hi;
    case 'mr':
      return require('./mr.js').mr;
    case 'kn':
      return require('./kn.js').kn;
    case 'ta':
      return require('./ta.js').ta;
    case 'te':
      return require('./te.js').te;
    case 'bn':
      return require('./bn.js').bn;
    case 'gu':
      return require('./gu.js').gu;
    case 'en':
    default:
      return require('./en.js').en;
  }
};
