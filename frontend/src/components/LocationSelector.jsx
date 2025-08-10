/**
 * MIT License
 * 
 * Location Selector component for choosing location for weather data
 */

import React, { useState, useEffect } from 'react';
import { useTranslation } from '../contexts/LanguageContext';
import './LocationSelector.css';

const LocationSelector = ({ onLocationChange }) => {
  const { t } = useTranslation();
  const [selectedState, setSelectedState] = useState('');
  const [selectedCity, setSelectedCity] = useState('');
  const [useGPS, setUseGPS] = useState(false);
  const [gpsLoading, setGpsLoading] = useState(false);
  const [gpsError, setGpsError] = useState('');

  // Major sugarcane growing regions in India
  const indianLocations = {
    'Uttar Pradesh': {
      'Lucknow': { lat: 26.8467, lon: 80.9462 },
      'Meerut': { lat: 28.9845, lon: 77.7064 },
      'Muzaffarnagar': { lat: 29.4727, lon: 77.7085 },
      'Saharanpur': { lat: 29.9680, lon: 77.5552 },
      'Bareilly': { lat: 28.3670, lon: 79.4304 }
    },
    'Maharashtra': {
      'Pune': { lat: 18.5204, lon: 73.8567 },
      'Mumbai': { lat: 19.0760, lon: 72.8777 },
      'Nashik': { lat: 19.9975, lon: 73.7898 },
      'Kolhapur': { lat: 16.7050, lon: 74.2433 },
      'Sangli': { lat: 16.8524, lon: 74.5815 }
    },
    'Karnataka': {
      'Bangalore': { lat: 12.9716, lon: 77.5946 },
      'Mysore': { lat: 12.2958, lon: 76.6394 },
      'Belgaum': { lat: 15.8497, lon: 74.4977 },
      'Mandya': { lat: 12.5218, lon: 76.8951 },
      'Shimoga': { lat: 13.9299, lon: 75.5681 }
    },
    'Tamil Nadu': {
      'Chennai': { lat: 13.0827, lon: 80.2707 },
      'Coimbatore': { lat: 11.0168, lon: 76.9558 },
      'Salem': { lat: 11.6643, lon: 78.1460 },
      'Erode': { lat: 11.3410, lon: 77.7172 },
      'Tiruchirapalli': { lat: 10.7905, lon: 78.7047 }
    },
    'Andhra Pradesh': {
      'Visakhapatnam': { lat: 17.6868, lon: 83.2185 },
      'Vijayawada': { lat: 16.5062, lon: 80.6480 },
      'Guntur': { lat: 16.3067, lon: 80.4365 },
      'Nellore': { lat: 14.4426, lon: 79.9865 },
      'Tirupati': { lat: 13.6288, lon: 79.4192 }
    },
    'Telangana': {
      'Hyderabad': { lat: 17.3850, lon: 78.4867 },
      'Warangal': { lat: 17.9689, lon: 79.5941 },
      'Nizamabad': { lat: 18.6725, lon: 78.0941 },
      'Karimnagar': { lat: 18.4386, lon: 79.1288 }
    },
    'Gujarat': {
      'Ahmedabad': { lat: 23.0225, lon: 72.5714 },
      'Surat': { lat: 21.1702, lon: 72.8311 },
      'Vadodara': { lat: 22.3072, lon: 73.1812 },
      'Rajkot': { lat: 22.3039, lon: 70.8022 }
    },
    'Haryana': {
      'Gurgaon': { lat: 28.4595, lon: 77.0266 },
      'Faridabad': { lat: 28.4089, lon: 77.3178 },
      'Panipat': { lat: 29.3909, lon: 76.9635 },
      'Ambala': { lat: 30.3782, lon: 76.7767 }
    },
    'Punjab': {
      'Ludhiana': { lat: 30.9010, lon: 75.8573 },
      'Amritsar': { lat: 31.6340, lon: 74.8723 },
      'Jalandhar': { lat: 31.3260, lon: 75.5762 },
      'Patiala': { lat: 30.3398, lon: 76.3869 }
    }
  };

  useEffect(() => {
    if (selectedState && selectedCity) {
      const location = indianLocations[selectedState][selectedCity];
      if (location) {
        onLocationChange({
          ...location,
          name: `${selectedCity}, ${selectedState}`,
          state: selectedState,
          city: selectedCity
        });
      }
    }
  }, [selectedState, selectedCity]);

  const handleGPSLocation = () => {
    if (!navigator.geolocation) {
      setGpsError('Geolocation is not supported by this browser');
      return;
    }

    setGpsLoading(true);
    setGpsError('');

    navigator.geolocation.getCurrentPosition(
      (position) => {
        const { latitude, longitude } = position.coords;
        onLocationChange({
          lat: latitude,
          lon: longitude,
          name: 'Current Location',
          isGPS: true
        });
        setUseGPS(true);
        setGpsLoading(false);
        setSelectedState('');
        setSelectedCity('');
      },
      (error) => {
        let errorMessage = 'Failed to get location';
        switch (error.code) {
          case error.PERMISSION_DENIED:
            errorMessage = 'Location access denied by user';
            break;
          case error.POSITION_UNAVAILABLE:
            errorMessage = 'Location information unavailable';
            break;
          case error.TIMEOUT:
            errorMessage = 'Location request timed out';
            break;
        }
        setGpsError(errorMessage);
        setGpsLoading(false);
      },
      {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 300000 // 5 minutes
      }
    );
  };

  const handleManualSelection = () => {
    setUseGPS(false);
    setGpsError('');
  };

  return (
    <div className="location-selector">
      <div className="location-header">
        <h3>{t('weather.selectLocation', 'Select Location')}</h3>
        <p>{t('weather.locationDesc', 'Choose your location to get accurate weather data')}</p>
      </div>

      <div className="location-options">
        {/* GPS Option */}
        <div className="location-option">
          <button 
            className={`gps-btn ${useGPS ? 'active' : ''}`}
            onClick={handleGPSLocation}
            disabled={gpsLoading}
          >
            {gpsLoading ? (
              <>
                <span className="loading-spinner small"></span>
                {t('weather.gettingLocation', 'Getting location...')}
              </>
            ) : (
              <>
                📍 {t('weather.useCurrentLocation', 'Use Current Location')}
              </>
            )}
          </button>
          {gpsError && (
            <div className="gps-error">
              <small>❌ {gpsError}</small>
            </div>
          )}
        </div>

        {/* Manual Selection */}
        <div className="location-option">
          <div className="manual-selection">
            <div className="selection-header">
              <span>🗺️ {t('weather.selectManually', 'Select Manually')}</span>
              <button
                className={`switch-btn ${!useGPS ? 'primary' : ''}`}
                onClick={handleManualSelection}
              >
                {!useGPS
                  ? t('weather.selectManually', 'Select Manually')
                  : t('weather.switchToManual', 'Switch to Manual')}
              </button>
            </div>

            {!useGPS && (
              <div className="dropdowns">
                <div className="dropdown-group">
                  <label>{t('weather.state', 'State')}:</label>
                  <select 
                    value={selectedState} 
                    onChange={(e) => {
                      setSelectedState(e.target.value);
                      setSelectedCity('');
                    }}
                    className="location-select"
                  >
                    <option value="">{t('weather.selectState', 'Select State')}</option>
                    {Object.keys(indianLocations).map(state => (
                      <option key={state} value={state}>{state}</option>
                    ))}
                  </select>
                </div>

                {selectedState && (
                  <div className="dropdown-group">
                    <label>{t('weather.city', 'City')}:</label>
                    <select 
                      value={selectedCity} 
                      onChange={(e) => setSelectedCity(e.target.value)}
                      className="location-select"
                    >
                      <option value="">{t('weather.selectCity', 'Select City')}</option>
                      {Object.keys(indianLocations[selectedState]).map(city => (
                        <option key={city} value={city}>{city}</option>
                      ))}
                    </select>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Selected Location Display */}
      {(selectedCity || useGPS) && (
        <div className="selected-location">
          <div className="location-display">
            <span className="location-icon">📍</span>
            <span className="location-name">
              {useGPS ? 
                t('weather.currentLocation', 'Current Location') : 
                `${selectedCity}, ${selectedState}`
              }
            </span>
            <span className="location-status">✅</span>
          </div>
        </div>
      )}
    </div>
  );
};

export default LocationSelector;
