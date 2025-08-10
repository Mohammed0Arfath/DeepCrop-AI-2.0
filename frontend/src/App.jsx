/**
 * MIT License
 * 
 * Main React application component for sugarcane disease detection
 */

import React, { useState } from 'react';
import { LanguageProvider } from './contexts/LanguageContext';
import { useTranslation } from './contexts/LanguageContext';
import LanguageSelector from './components/LanguageSelector';
import DiseaseSelector from './components/DiseaseSelector';
import ImageUpload from './components/ImageUpload';
import EnhancedQuestionnaire from './components/EnhancedQuestionnaire';
import Results from './components/Results';
import WeatherDashboard from './components/WeatherDashboard';
import './App.css';
import { getCompletionStatus } from './utils/questions';

// Main App Component (wrapped with translations)
const AppContent = () => {
  const { t } = useTranslation();
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

  // Completion status for questionnaire
  const status = selectedDisease
    ? getCompletionStatus(selectedDisease, questionnaireData)
    : { isComplete: false, answeredCount: 0, total: 0 };

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
    if (!selectedDisease || !uploadedImage) {
      setError(t('errors.imageRequired', 'Please upload an image'));
      return;
    }
    const localStatus = getCompletionStatus(selectedDisease, questionnaireData);
    if (!localStatus.isComplete) {
      setError(t('questionnaire.mustAnswerAll', 'Please answer all questions before analyzing.'));
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
        <div className="header-content">
          <div className="header-text">
            <h1>🌾 {t('app.title')}</h1>
            <p>{t('app.subtitle')}</p>
          </div>
          <div className="header-controls">
            <LanguageSelector />
          </div>
        </div>
      </header>

      <main className="app-main">
        {/* Weather Dashboard */}
        <section className="section">
          <WeatherDashboard />
        </section>

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
              <EnhancedQuestionnaire 
                diseaseType={selectedDisease}
                onAnswersChange={handleQuestionnaireChange}
                onComplete={handleQuestionnaireChange}
              />
            </section>

            {/* Submit Button */}
            <section className="section">
              <div className="submit-section">
                <button 
                  className="submit-btn"
                  onClick={handleSubmit}
                  disabled={loading || !uploadedImage || !status.isComplete}
                >
                  {loading ? t('buttons.analyzing') : t('buttons.submit')}
                </button>
                
                <button 
                  className="reset-btn"
                  onClick={handleReset}
                  disabled={loading}
                >
                  {t('buttons.reset')}
                </button>
              </div>
              {selectedDisease && !status.isComplete && (
                <div className="incomplete-status">
                  <small>
                    {t('questionnaire.incompleteProgress', 'Answered {answered} of {total}.')
                      .replace('{answered}', String(status.answeredCount))
                      .replace('{total}', String(status.total))}
                  </small>
                </div>
              )}
            </section>
          </>
        )}

        {/* Error Display */}
        {error && (
          <section className="section">
            <div className="error-message">
              <h3>❌ {t('errors.generic')}</h3>
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
        <p>{t('app.footer')}</p>
      </footer>
    </div>
  );
};

// Main App Component with Language Provider
function App() {
  return (
    <LanguageProvider>
      <AppContent />
    </LanguageProvider>
  );
}

export default App;
