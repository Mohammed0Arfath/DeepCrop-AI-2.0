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

  // Normalize names so backend "dead_heart" matches frontend "deadheart"
  const normalize = (s) => (s || '').toString().replace(/[_\s]/g, '').toLowerCase();

  // Determine result status
  const isPositive = normalize(final_label) === normalize(diseaseType);
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
            <h3>{isPositive ? `${diseaseType.toUpperCase()} DETECTED` : 'NO DISEASE DETECTED'}</h3>
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
                style={{ width: `${image_confidence * 100}%` }}
              ></div>
            </div>
            <div className="score-value">{(image_confidence * 100).toFixed(1)}%</div>
          </div>
          
          <div className="score-item">
            <div className="score-label">Plant Assessment</div>
            <div className="score-bar">
              <div 
                className="score-fill tabnet-score" 
                style={{ width: `${tabnet_prob * 100}%` }}
              ></div>
            </div>
            <div className="score-value">{(tabnet_prob * 100).toFixed(1)}%</div>
          </div>
          
          <div className="score-item final-score">
            <div className="score-label">Final Score</div>
            <div className="score-bar">
              <div 
                className={`score-fill final-score-fill ${confidenceLevel}`}
                style={{ width: `${final_score * 100}%` }}
              ></div>
            </div>
            <div className="score-value">{(final_score * 100).toFixed(1)}%</div>
          </div>
        </div>
        
        {metadata && (
          <div className="fusion-info">
            <p>
              <strong>Fusion Weights:</strong> Image {(metadata.fusion_weights.image * 100).toFixed(0)}%, 
              Plant Assessment {(metadata.fusion_weights.tabnet * 100).toFixed(0)}%
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
                  <th>Class</th>
                  <th>Confidence</th>
                  <th>Bounding Box</th>
                </tr>
              </thead>
              <tbody>
                {detections.map((detection, index) => (
                  <tr key={index}>
                    <td>{index + 1}</td>
                    <td className="detection-class">{detection.class}</td>
                    <td className="detection-confidence">
                      {(detection.score * 100).toFixed(1)}%
                    </td>
                    <td className="detection-box">
                      [{detection.box.map(coord => Math.round(coord)).join(', ')}]
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Recommendations */}
      <div className="recommendations">
        <h3>💡 Recommendations</h3>
        {isPositive ? (
          <div className="recommendation-list positive-recommendations">
            <div className="recommendation-item">
              <strong>🚨 Immediate Action Required</strong>
              <p>Disease detected with {confidenceLevel} confidence. Consider consulting with an agricultural expert.</p>
            </div>
            <div className="recommendation-item">
              <strong>🔍 Further Investigation</strong>
              <p>Examine neighboring plants and check for similar symptoms in the field.</p>
            </div>
            <div className="recommendation-item">
              <strong>📋 Treatment Options</strong>
              <p>Research appropriate treatment methods for {diseaseType} or consult agricultural extension services.</p>
            </div>
            <div className="recommendation-item">
              <strong>📊 Monitor Progress</strong>
              <p>Take regular photos and assessments to track disease progression or treatment effectiveness.</p>
            </div>
          </div>
        ) : (
          <div className="recommendation-list negative-recommendations">
            <div className="recommendation-item">
              <strong>✅ Plant Appears Healthy</strong>
              <p>No signs of {diseaseType} detected. Continue regular monitoring and maintenance.</p>
            </div>
            <div className="recommendation-item">
              <strong>🛡️ Preventive Measures</strong>
              <p>Maintain good field hygiene and proper irrigation to prevent future diseases.</p>
            </div>
            <div className="recommendation-item">
              <strong>📅 Regular Monitoring</strong>
              <p>Continue periodic assessments, especially during vulnerable growth stages.</p>
            </div>
          </div>
        )}
      </div>

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
