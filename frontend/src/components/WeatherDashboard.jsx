/**
 * MIT License
 * 
 * Weather Dashboard component for displaying current weather and disease risk assessment
 */

import React, { useState, useEffect, useCallback } from 'react';
import { useTranslation } from '../contexts/LanguageContext';
import LocationSelector from './LocationSelector';
import RiskIndicator from './RiskIndicator';
import './WeatherDashboard.css';

const WeatherDashboard = ({ onLocationSelected }) => {
  const { t } = useTranslation();
  const [location, setLocation] = useState(null);
  const [weatherData, setWeatherData] = useState(null);
  const [riskData, setRiskData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

  const fetchWeatherData = useCallback(async () => {
    if (!location) return;

    setLoading(true);
    setError('');

    try {
      // Fetch current weather
      const weatherResponse = await fetch(
        `${API_BASE_URL}/weather/current?lat=${location.lat}&lon=${location.lon}`
      );
      
      if (!weatherResponse.ok) {
        throw new Error('Failed to fetch weather data');
      }
      
      const weather = await weatherResponse.json();
      setWeatherData(weather);

      // Fetch disease risk assessment
      const riskResponse = await fetch(
        `${API_BASE_URL}/weather/disease-risk?lat=${location.lat}&lon=${location.lon}`
      );
      
      if (!riskResponse.ok) {
        throw new Error('Failed to fetch risk assessment');
      }
      
      const risk = await riskResponse.json();
      setRiskData(risk);

    } catch (err) {
      console.error('Weather fetch error:', err);
      setError(err.message || 'Failed to fetch weather data');
    } finally {
      setLoading(false);
    }
  }, [location, API_BASE_URL]);

  // Fetch weather and risk data when location changes
  useEffect(() => {
    if (location) {
      fetchWeatherData();
    }
  }, [location, fetchWeatherData]);

  const handleLocationChange = useCallback((newLocation) => {
    setLocation(newLocation);
    try {
      if (onLocationSelected) {
        onLocationSelected(newLocation);
      }
    } catch (e) {
      console.error('onLocationSelected callback error:', e);
    }
  }, [onLocationSelected]);

  const getWeatherIcon = (iconCode) => {
    // Map OpenWeatherMap icons to emojis
    const iconMap = {
      '01d': '☀️', '01n': '🌙',
      '02d': '⛅', '02n': '☁️',
      '03d': '☁️', '03n': '☁️',
      '04d': '☁️', '04n': '☁️',
      '09d': '🌧️', '09n': '🌧️',
      '10d': '🌦️', '10n': '🌧️',
      '11d': '⛈️', '11n': '⛈️',
      '13d': '❄️', '13n': '❄️',
      '50d': '🌫️', '50n': '🌫️'
    };
    return iconMap[iconCode] || '🌤️';
  };

  const formatTemperature = (temp) => {
    return `${Math.round(temp)}°C`;
  };

  const formatTime = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString([], { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  return (
    <div className="weather-dashboard">
      <div className="weather-header">
        <h2>🌦️ {t('weather.title', 'Weather & Pest Risk')}</h2>
        <p>{t('weather.subtitle', 'Current conditions and pest risk assessment')}</p>
      </div>

      <LocationSelector onLocationChange={handleLocationChange} />

      {loading && (
        <div className="weather-loading">
          <div className="loading-spinner"></div>
          <p>{t('weather.loading', 'Fetching weather data...')}</p>
        </div>
      )}

      {error && (
        <div className="weather-error">
          <p>❌ {error}</p>
          <button onClick={fetchWeatherData} className="retry-btn">
            {t('weather.retry', 'Retry')}
          </button>
        </div>
      )}

      {weatherData && !loading && (
        <div className="weather-content">
          {/* Current Weather Card */}
          <div className="weather-card">
            <div className="weather-main">
              <div className="weather-icon">
                {getWeatherIcon(weatherData.current.weather_icon)}
              </div>
              <div className="weather-info">
                <h3>{weatherData.location.name}</h3>
                <p className="weather-description">
                  {weatherData.current.weather_description}
                </p>
                <div className="temperature">
                  {formatTemperature(weatherData.current.temperature)}
                </div>
                <p className="feels-like">
                  {t('weather.feelsLike', 'Feels like')} {formatTemperature(weatherData.current.feels_like)}
                </p>
              </div>
            </div>

            <div className="weather-details">
              <div className="weather-detail">
                <span className="detail-icon">💧</span>
                <span className="detail-label">{t('weather.humidity', 'Humidity')}</span>
                <span className="detail-value">{weatherData.current.humidity}%</span>
              </div>
              <div className="weather-detail">
                <span className="detail-icon">💨</span>
                <span className="detail-label">{t('weather.windSpeed', 'Wind')}</span>
                <span className="detail-value">{weatherData.current.wind_speed} m/s</span>
              </div>
              <div className="weather-detail">
                <span className="detail-icon">🌧️</span>
                <span className="detail-label">{t('weather.rainfall', 'Rain (3h)')}</span>
                <span className="detail-value">{weatherData.current.rainfall_3h} mm</span>
              </div>
              <div className="weather-detail">
                <span className="detail-icon">📊</span>
                <span className="detail-label">{t('weather.pressure', 'Pressure')}</span>
                <span className="detail-value">{weatherData.current.pressure} hPa</span>
              </div>
            </div>

            <div className="weather-timestamp">
              {t('weather.lastUpdated', 'Last updated')}: {formatTime(weatherData.current.timestamp)}
            </div>
          </div>

          {/* Disease Risk Assessment */}
          {riskData && (
            <div className="risk-assessment-section">
              <h3>
                {t('weather.diseaseRisk', 'Pest Risk Assessment')}
                {riskData && (riskData.rule_mode === 'approx_free' || riskData.approx_mode) && (
                  <span className="approx-badge" style={{ marginLeft: '8px', padding: '2px 8px', borderRadius: '12px', background: '#eef3ff', color: '#1a73e8', fontSize: '12px', fontWeight: 600 }}>
                    OpenWeather Free (approx)
                  </span>
                )}
              </h3>
              
              {/* Overall Risk */}
              <div className="overall-risk">
                <RiskIndicator 
                  riskLevel={riskData.overall_risk.risk_level}
                  riskScore={riskData.overall_risk.risk_score}
                  riskColor={riskData.overall_risk.risk_color}
                  title={t('weather.overallRisk', 'Overall Risk')}
                />
              </div>

              {/* Individual Disease Risks */}
              <div className="disease-risks">
                <div className="disease-risk-card">
                  <h4>💔 {t('diseases.deadheart', 'Dead Heart')}</h4>
                  <RiskIndicator 
                    riskLevel={riskData.deadheart.risk_level}
                    riskScore={riskData.deadheart.risk_score}
                    riskColor={riskData.deadheart.risk_color}
                    compact={true}
                  />
                  <div className="risk-factors">
                    <h5>{t('weather.riskFactors', 'Risk Factors')}:</h5>
                    <ul>
                      {riskData.deadheart.risk_factors.slice(0, 3).map((factor, index) => (
                        <li key={index}>{factor}</li>
                      ))}
                    </ul>
                  </div>
                </div>

                <div className="disease-risk-card">
                  <h4>🌱 {t('diseases.tiller', 'Tiller')}</h4>
                  <RiskIndicator 
                    riskLevel={riskData.tiller.risk_level}
                    riskScore={riskData.tiller.risk_score}
                    riskColor={riskData.tiller.risk_color}
                    compact={true}
                  />
                  <div className="risk-factors">
                    <h5>{t('weather.riskFactors', 'Risk Factors')}:</h5>
                    <ul>
                      {riskData.tiller.risk_factors.slice(0, 3).map((factor, index) => (
                        <li key={index}>{factor}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>

              {/* Recommendations */}
              {riskData.combined_recommendations && riskData.combined_recommendations.length > 0 && (
                <div className="recommendations">
                  <h4>{t('weather.recommendations', 'Recommendations')}</h4>
                  <ul className="recommendation-list">
                    {riskData.combined_recommendations.map((recommendation, index) => (
                      <li key={index} className="recommendation-item">
                        <span className="recommendation-icon">💡</span>
                        {recommendation}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}
        </div>
      )}

      {!location && !loading && (
        <div className="weather-placeholder">
          <div className="placeholder-icon">📍</div>
          <h3>{t('weather.selectLocation', 'Select Your Location')}</h3>
          <p>{t('weather.selectLocationDesc', 'Choose your location to get weather-based pest risk assessment')}</p>
        </div>
      )}
    </div>
  );
};

export default WeatherDashboard;
