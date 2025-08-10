/**
 * MIT License
 * 
 * Results component for displaying prediction results
 */

import React from 'react';

const Results = ({ results, diseaseType }) => {
  if (!results) return null;

  const {
    image_confidence,
    tabnet_prob,
    final_score,
    final_label,
    detections,
    overlay_image_base64,
    metadata
  } = results;

  // Determine result status
  const isPositive = final_label === diseaseType;
  const confidenceLevel = final_score >= 0.8 ? 'high' : final_score >= 0.5 ? 'medium' : 'low';

  return (
    <div className="results">
      <div className="results-header">
        <h2>🔬 Analysis Results</h2>
        <div className={`result-status ${isPositive ? 'positive' : 'negative'}`}>
          <div className="status-icon">
            {isPositive ? '⚠️' : '✅'}
          </div>
          <div className="status-text">
            <h3>{isPositive ? `${diseaseType.toUpperCase()} DETECTED` : 'NO PEST DETECTED'}</h3>
            <p>Confidence: {(final_score * 100).toFixed(1)}% ({confidenceLevel})</p>
          </div>
        </div>
      </div>

      {/* Overlay Image */}
      {overlay_image_base64 && (
        <div className="overlay-image-section">
          <h3>📸 Analyzed Image</h3>
          <div className="overlay-image-container">
            <img 
              src={overlay_image_base64} 
              alt="Analysis overlay" 
              className="overlay-image"
            />
          </div>
          {detections && detections.length > 0 && (
            <p className="detection-count">
              {detections.length} detection{detections.length !== 1 ? 's' : ''} found
            </p>
          )}
        </div>
      )}

      {/* Score Breakdown */}
      <div className="score-breakdown">
        <h3>📊 Score Breakdown</h3>
        <div className="scores-grid">
          <div className="score-item">
            <div className="score-label">Image Analysis</div>
            <div className="score-bar">
              <div 
                className="score-fill image-score" 
                style={{ width: `${Math.max(0, Math.min(100, ((image_confidence || 0) * 100)))}%` }}
              ></div>
            </div>
            <div className="score-value">{(image_confidence * 100).toFixed(1)}%</div>
          </div>
          
          <div className="score-item">
            <div className="score-label">Questionnaire Assessment</div>
            <div className="score-bar">
              <div 
                className="score-fill tabnet-score" 
                style={{ width: `${Math.max(0, Math.min(100, ((tabnet_prob || 0) * 100)))}%` }}
              ></div>
            </div>
            <div className="score-value">{(tabnet_prob * 100).toFixed(1)}%</div>
          </div>
          
          <div className="score-item final-score">
            <div className="score-label">Final Score</div>
            <div className="score-bar">
              <div 
                className={`score-fill final-score-fill ${confidenceLevel}`}
                style={{ width: `${Math.max(0, Math.min(100, ((final_score || 0) * 100)))}%` }}
              ></div>
            </div>
            <div className="score-value">{(final_score * 100).toFixed(1)}%</div>
          </div>
        </div>
        
        {metadata && (
          <div className="fusion-info">
            <p>
              <strong>Fusion Weights:</strong> Image {(metadata.fusion_weights.image * 100).toFixed(0)}%, 
              Questionnaire {(metadata.fusion_weights.tabnet * 100).toFixed(0)}%
            </p>
            <p>
              <strong>Detection Threshold:</strong> {(metadata.threshold * 100).toFixed(0)}%
            </p>
          </div>
        )}
      </div>

      {/* Detections Table */}
      {detections && detections.length > 0 && (
        <div className="detections-section">
          <h3>🎯 Detections</h3>
          <div className="detections-table">
            <table>
              <thead>
                <tr>
                  <th>#</th>
                  <th>Type</th>
                  <th>Class</th>
                  <th>Confidence</th>
                  <th>Region</th>
                </tr>
              </thead>
              <tbody>
                {detections.map((d, idx) => {
                  const kind = d.type || (Array.isArray(d.box) ? 'detection' : 'segmentation');
                  let region = '—';
                  if (kind === 'detection' && Array.isArray(d.box)) {
                    region = `[${d.box.map(n => Math.round(n)).join(', ')}]`;
                  } else if (kind === 'segmentation') {
                    if (Array.isArray(d.polygon)) {
                      region = `polygon (${d.polygon.length} points)`;
                    } else if (d.mask) {
                      region = 'mask';
                    }
                  }
                  return (
                    <tr key={idx}>
                      <td>{idx + 1}</td>
                      <td>{kind}</td>
                      <td className="detection-class">{d.class}</td>
                      <td className="detection-confidence">
                        {((d.score || 0) * 100).toFixed(1)}%
                      </td>
                      <td className="detection-box">{region}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Recommendations (Gemini-only) */}
      {Array.isArray(results.recommendations) && results.recommendations.length > 0 && (
        <div className="recommendations">
          <h3 className="gemini-header">
            💡 Gemini AI Recommendations
            <span className="gemini-badge">Gemini</span>
          </h3>
          {results.recommendations_info && (
            <div className="recommendation-meta">
              <span>Model: {results.recommendations_info.model}</span>
              <span>Language: {results.recommendations_info.language?.toUpperCase?.() || 'EN'}</span>
            </div>
          )}
          <ul className="recommendation-list">
            {results.recommendations.map((rec, idx) => (
              <li key={idx} className="recommendation-item">
                <span className="recommendation-icon">🌿</span>
                {rec}
              </li>
            ))}
          </ul>
        </div>
      )}

      {(!results.recommendations || results.recommendations.length === 0) && results.recommendations_info && (
        <div className="recommendations">
          <h3 className="gemini-header">
            💡 Gemini AI Recommendations
            <span className="gemini-badge warning">No Output</span>
          </h3>
          <div className="recommendation-meta">
            <span>Status: {results.recommendations_info.status}</span>
            <span>Model: {results.recommendations_info.model}</span>
            <span>Language: {results.recommendations_info.language?.toUpperCase?.() || 'EN'}</span>
          </div>
          <ul className="recommendation-list">
            <li className="recommendation-item">
              <span className="recommendation-icon">ℹ️</span>
              <span>
                No Gemini recommendations were returned. Ensure the backend has internet access, dependencies installed,
                and a valid Gemini API key, then analyze again.
              </span>
            </li>
          </ul>
        </div>
      )}

      {/* Technical Details (Collapsible) */}
      <details className="technical-details">
        <summary>🔧 Technical Details</summary>
        <div className="technical-content">
          <h4>Raw Results:</h4>
          <pre>{JSON.stringify(results, null, 2)}</pre>
        </div>
      </details>
    </div>
  );
};

export default Results;
