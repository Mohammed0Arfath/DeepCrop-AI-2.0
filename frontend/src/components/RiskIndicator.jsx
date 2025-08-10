/**
 * MIT License
 * 
 * Risk Indicator component for displaying disease risk levels with visual indicators
 */

import React from 'react';
import { useTranslation } from '../contexts/LanguageContext';
import './RiskIndicator.css';

const RiskIndicator = ({ 
  riskLevel, 
  riskScore, 
  riskColor, 
  title, 
  compact = false 
}) => {
  const { t } = useTranslation();

  const getRiskIcon = (level) => {
    const icons = {
      low: '✅',
      medium: '⚠️',
      high: '🚨',
      critical: '🔴'
    };
    return icons[level] || '❓';
  };

  const getRiskLabel = (level) => {
    const labels = {
      low: t('weather.risk.low', 'Low Risk'),
      medium: t('weather.risk.medium', 'Medium Risk'),
      high: t('weather.risk.high', 'High Risk'),
      critical: t('weather.risk.critical', 'Critical Risk')
    };
    return labels[level] || level;
  };

  const getRiskDescription = (level) => {
    const descriptions = {
      low: t('weather.risk.lowDesc', 'Conditions are favorable'),
      medium: t('weather.risk.mediumDesc', 'Monitor plants closely'),
      high: t('weather.risk.highDesc', 'Take preventive action'),
      critical: t('weather.risk.criticalDesc', 'Immediate action required')
    };
    return descriptions[level] || '';
  };

  if (compact) {
    return (
      <div className="risk-indicator compact">
        <div className="risk-header">
          <span className="risk-icon">{getRiskIcon(riskLevel)}</span>
          <span className="risk-label">{getRiskLabel(riskLevel)}</span>
          <span className="risk-score">{Math.round(riskScore)}%</span>
        </div>
        <div className="risk-bar">
          <div 
            className="risk-fill" 
            style={{ 
              width: `${riskScore}%`, 
              backgroundColor: riskColor 
            }}
          ></div>
        </div>
      </div>
    );
  }

  return (
    <div className="risk-indicator">
      {title && <h4 className="risk-title">{title}</h4>}
      
      <div className="risk-content">
        <div className="risk-visual">
          <div className="risk-circle" style={{ borderColor: riskColor }}>
            <div className="risk-icon-large">{getRiskIcon(riskLevel)}</div>
            <div className="risk-score-large">{Math.round(riskScore)}%</div>
          </div>
        </div>
        
        <div className="risk-info">
          <div className="risk-level" style={{ color: riskColor }}>
            {getRiskLabel(riskLevel)}
          </div>
          <div className="risk-description">
            {getRiskDescription(riskLevel)}
          </div>
          
          <div className="risk-progress">
            <div className="risk-progress-bar">
              <div 
                className="risk-progress-fill" 
                style={{ 
                  width: `${riskScore}%`, 
                  backgroundColor: riskColor 
                }}
              ></div>
            </div>
            <div className="risk-progress-labels">
              <span>0%</span>
              <span>100%</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RiskIndicator;
