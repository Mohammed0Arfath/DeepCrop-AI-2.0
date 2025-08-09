/**
 * MIT License
 * 
 * Disease selector component for choosing between dead heart and tiller diseases
 */

import React from 'react';

const DiseaseSelector = ({ selectedDisease, onDiseaseSelect }) => {
  const diseases = [
    {
      id: 'deadheart',
      name: 'Dead Heart',
      description: 'A disease that affects the growing point of sugarcane, causing the central shoot to die.',
      icon: '💔'
    },
    {
      id: 'tiller',
      name: 'Tiller Disease',
      description: 'A condition affecting the tillering process in sugarcane plants.',
      icon: '🌱'
    }
  ];

  return (
    <div className="disease-selector">
      <h2>Select Disease Type</h2>
      <p>Choose the type of disease you want to detect:</p>
      
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
