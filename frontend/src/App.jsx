/**
 * MIT License
 * 
 * Main React application component for sugarcane disease detection
 */

import React, { useState } from 'react';
import DiseaseSelector from './components/DiseaseSelector';
import ImageUpload from './components/ImageUpload';
import Questionnaire from './components/Questionnaire';
import Results from './components/Results';
import './App.css';

function App() {
  // State management
  const [selectedDisease, setSelectedDisease] = useState('');
  const [uploadedImage, setUploadedImage] = useState(null);
  const [imagePreview, setImagePreview] = useState('');
  const [questionnaireData, setQuestionnaireData] = useState({});
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // API base URL (configurable)
  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

  // Handle disease selection
  const handleDiseaseSelect = (disease) => {
    setSelectedDisease(disease);
    setResults(null);
    setError('');
  };

  // Handle image upload
  const handleImageUpload = (file, preview) => {
    setUploadedImage(file);
    setImagePreview(preview);
    setResults(null);
    setError('');
  };

  // Handle questionnaire data
  const handleQuestionnaireChange = (data) => {
    setQuestionnaireData(data);
  };

  // Submit prediction request
  const handleSubmit = async () => {
    if (!selectedDisease || !uploadedImage || Object.keys(questionnaireData).length === 0) {
      setError('Please select a disease, upload an image, and fill out the questionnaire.');
      return;
    }

    setLoading(true);
    setError('');

    try {
      // Prepare form data
      const formData = new FormData();
      formData.append('image', uploadedImage);
      formData.append('questions', JSON.stringify(questionnaireData));

      // Make API request
      const endpoint = `${API_BASE_URL}/predict/${selectedDisease}`;
      const response = await fetch(endpoint, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Prediction failed');
      }

      const result = await response.json();
      setResults(result);

    } catch (err) {
      console.error('Prediction error:', err);
      setError(err.message || 'An error occurred during prediction');
    } finally {
      setLoading(false);
    }
  };

  // Reset form
  const handleReset = () => {
    setSelectedDisease('');
    setUploadedImage(null);
    setImagePreview('');
    setQuestionnaireData({});
    setResults(null);
    setError('');
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>🌾 Sugarcane Disease Detection</h1>
        <p>AI-powered detection for dead heart and tiller diseases</p>
      </header>

      <main className="app-main">
        {/* Disease Selection */}
        <section className="section">
          <DiseaseSelector 
            selectedDisease={selectedDisease}
            onDiseaseSelect={handleDiseaseSelect}
          />
        </section>

        {/* Image Upload and Questionnaire (only show when disease is selected) */}
        {selectedDisease && (
          <>
            <section className="section">
              <ImageUpload 
                onImageUpload={handleImageUpload}
                imagePreview={imagePreview}
              />
            </section>

            <section className="section">
              <Questionnaire 
                diseaseType={selectedDisease}
                onDataChange={handleQuestionnaireChange}
              />
            </section>

            {/* Submit Button */}
            <section className="section">
              <div className="submit-section">
                <button 
                  className="submit-btn"
                  onClick={handleSubmit}
                  disabled={loading || !uploadedImage || Object.keys(questionnaireData).length === 0}
                >
                  {loading ? 'Analyzing...' : 'Analyze Disease'}
                </button>
                
                <button 
                  className="reset-btn"
                  onClick={handleReset}
                  disabled={loading}
                >
                  Reset
                </button>
              </div>
            </section>
          </>
        )}

        {/* Error Display */}
        {error && (
          <section className="section">
            <div className="error-message">
              <h3>❌ Error</h3>
              <p>{error}</p>
            </div>
          </section>
        )}

        {/* Results Display */}
        {results && (
          <section className="section">
            <Results results={results} diseaseType={selectedDisease} />
          </section>
        )}
      </main>

      <footer className="app-footer">
        <p>© 2024 Sugarcane Disease Detection System</p>
      </footer>
    </div>
  );
}

export default App;
