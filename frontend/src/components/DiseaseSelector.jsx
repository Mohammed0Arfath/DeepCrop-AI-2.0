/**
 * MIT License
 * 
 * Disease selector component for choosing between dead heart and tiller diseases
 */

import React from 'react';
import { useTranslation } from '../contexts/LanguageContext';

const DiseaseSelector = ({ selectedDisease, onDiseaseSelect }) => {
  const { t } = useTranslation();
  const diseases = [
    {
      id: 'deadheart',
      name: t('diseases.deadheart'),
      description: 'A disease that affects the growing point of sugarcane, causing the central shoot to die.',
      icon: '💔'
    },
    {
      id: 'tiller',
      name: t('diseases.tiller'),
      description: 'A condition affecting the tillering process in sugarcane plants.',
      icon: '🌱'
    }
  ];

  return (
    <div className="disease-selector">
      <h2>{t('diseases.select')}</h2>
      <p>{t('diseases.selectDescription')}</p>
      
      <div className="disease-options">
        {diseases.map((disease) => (
          <div
            key={disease.id}
            className={`disease-option ${selectedDisease === disease.id ? 'selected' : ''}`}
            onClick={() => onDiseaseSelect(disease.id)}
          >
            <div className="disease-icon">{disease.icon}</div>
            <div className="disease-info">
              <h3>{disease.name}</h3>
              <p>{disease.description}</p>
            </div>
            <div className="selection-indicator">
              {selectedDisease === disease.id && <span>✓</span>}
            </div>
          </div>
        ))}
      </div>
      
      {selectedDisease && (
        <div className="selected-disease-info">
          <p>
            <strong>Selected:</strong> {diseases.find(d => d.id === selectedDisease)?.name}
          </p>
        </div>
      )}
    </div>
  );
};

export default DiseaseSelector;
