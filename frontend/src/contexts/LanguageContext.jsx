import React, { createContext, useContext, useState, useEffect } from 'react';

// Create Language Context
const LanguageContext = createContext();

// Available languages
export const LANGUAGES = {
  en: {
    code: 'en',
    name: 'English',
    nativeName: 'English',
    flag: '🇺🇸'
  },
  hi: {
    code: 'hi',
    name: 'Hindi',
    nativeName: 'हिंदी',
    flag: '🇮🇳'
  },
  ta: {
    code: 'ta',
    name: 'Tamil',
    nativeName: 'தமிழ்',
    flag: '🇮🇳'
  },
  te: {
    code: 'te',
    name: 'Telugu',
    nativeName: 'తెలుగు',
    flag: '🇮🇳'
  }
};

// Language Provider Component
export const LanguageProvider = ({ children }) => {
  const [currentLanguage, setCurrentLanguage] = useState('en');
  const [translations, setTranslations] = useState({});
  const [loading, setLoading] = useState(true);

  // Load translations for a specific language
  const loadTranslations = async (languageCode) => {
    try {
      setLoading(true);
      const response = await import(`../locales/${languageCode}.json`);
      setTranslations(response.default);
    } catch (error) {
      console.error(`Failed to load translations for ${languageCode}:`, error);
      // Fallback to English if translation fails
      if (languageCode !== 'en') {
        const fallback = await import('../locales/en.json');
        setTranslations(fallback.default);
      }
    } finally {
      setLoading(false);
    }
  };

  // Change language
  const changeLanguage = (languageCode) => {
    if (LANGUAGES[languageCode]) {
      setCurrentLanguage(languageCode);
      localStorage.setItem('selectedLanguage', languageCode);
      loadTranslations(languageCode);
    }
  };

  // Get translation by key path (e.g., 'app.title')
  const t = (key, fallback = key) => {
    const keys = key.split('.');
    let value = translations;
    
    for (const k of keys) {
      if (value && typeof value === 'object' && k in value) {
        value = value[k];
      } else {
        return fallback;
      }
    }
    
    return typeof value === 'string' ? value : fallback;
  };

  // Initialize language on mount
  useEffect(() => {
    // Check for saved language preference
    const savedLanguage = localStorage.getItem('selectedLanguage');
    
    // Detect browser language if no saved preference
    const browserLanguage = navigator.language.split('-')[0];
    
    // Use saved language, browser language, or default to English
    const initialLanguage = savedLanguage || 
                           (LANGUAGES[browserLanguage] ? browserLanguage : 'en');
    
    setCurrentLanguage(initialLanguage);
    loadTranslations(initialLanguage);
  }, []);

  const value = {
    currentLanguage,
    availableLanguages: LANGUAGES,
    changeLanguage,
    t,
    loading,
    isRTL: false // None of our languages are RTL, but keeping for future expansion
  };

  return (
    <LanguageContext.Provider value={value}>
      {children}
    </LanguageContext.Provider>
  );
};

// Custom hook to use language context
export const useLanguage = () => {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
};

// Translation hook (shorthand)
export const useTranslation = () => {
  const { t } = useLanguage();
  return { t };
};
