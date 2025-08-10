import React, { useState } from 'react';
import { useLanguage } from '../contexts/LanguageContext';
import './LanguageSelector.css';

const LanguageSelector = () => {
  const { currentLanguage, availableLanguages, changeLanguage } = useLanguage();
  const [isOpen, setIsOpen] = useState(false);

  const handleLanguageChange = (languageCode) => {
    changeLanguage(languageCode);
    setIsOpen(false);
  };

  const toggleDropdown = () => {
    setIsOpen(!isOpen);
  };

  const currentLang = availableLanguages[currentLanguage];

  return (
    <div className="language-selector">
      <button 
        className="language-selector-button"
        onClick={toggleDropdown}
        aria-label="Select Language"
      >
        <span className="flag">{currentLang.flag}</span>
        <span className="language-name">{currentLang.nativeName}</span>
        <span className={`dropdown-arrow ${isOpen ? 'open' : ''}`}>▼</span>
      </button>

      {isOpen && (
        <div className="language-dropdown">
          {Object.values(availableLanguages).map((language) => (
            <button
              key={language.code}
              className={`language-option ${
                language.code === currentLanguage ? 'active' : ''
              }`}
              onClick={() => handleLanguageChange(language.code)}
            >
              <span className="flag">{language.flag}</span>
              <div className="language-info">
                <span className="native-name">{language.nativeName}</span>
                <span className="english-name">{language.name}</span>
              </div>
              {language.code === currentLanguage && (
                <span className="check-mark">✓</span>
              )}
            </button>
          ))}
        </div>
      )}

      {/* Overlay to close dropdown when clicking outside */}
      {isOpen && (
        <div 
          className="language-selector-overlay"
          onClick={() => setIsOpen(false)}
        />
      )}
    </div>
  );
};

export default LanguageSelector;
