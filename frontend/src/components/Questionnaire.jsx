/**
 * MIT License
 * 
 * Questionnaire component for collecting plant condition data
 */

import React, { useState, useEffect } from 'react';

const Questionnaire = ({ diseaseType, onDataChange }) => {
  const [answers, setAnswers] = useState({});
  const [mode, setMode] = useState('form'); // 'form' or 'json'
  const [jsonInput, setJsonInput] = useState('');

  // Specific questions for tiller disease detection (15 questions in exact order)
  const tillerQuestions = [
    { id: 'affected_setts_spreading', text: 'Does the disease seem to be spreading by the use of affected setts for planting?', type: 'select', options: ['yes', 'no'] },
    { id: 'plants_stunted_slow_growth', text: 'Are the plants stunted and the few shoots that emerge are growing slowly?', type: 'select', options: ['yes', 'no'] },
    { id: 'honey_dew_sooty_mould', text: 'Do you see heavy secretion of honey dew on the leaves, leading to sooty mould development?', type: 'select', options: ['yes', 'no'] },
    { id: 'nodal_regions_infested', text: 'Are the nodal regions more infested than the internodal regions?', type: 'select', options: ['yes', 'no'] },
    { id: 'tillers_white_yellow', text: 'Are the tillers that are appearing white or yellow?', type: 'select', options: ['yes', 'no'] },
    { id: 'high_aphid_population', text: 'Is there a high population of aphids (Melanaphis sacchari and Rhopalosiphum maidis) in the field?', type: 'select', options: ['yes', 'no'] },
    { id: 'gaps_early_drying', text: 'Are there gaps in the field because the leaves are drying early?', type: 'select', options: ['yes', 'no'] },
    { id: 'cane_stunted_reduced_internodes', text: 'Does the cane become stunted with reduced internodal length?', type: 'select', options: ['yes', 'no'] },
    { id: 'no_millable_cane_formation', text: 'Is there no millable cane formation in the affected tillers?', type: 'select', options: ['yes', 'no'] },
    { id: 'profuse_lateral_buds', text: 'Have you observed any profuse sprouting of lateral buds with narrow, erect leaves?', type: 'select', options: ['yes', 'no'] },
    { id: 'woolly_matter_deposition', text: 'Is there a distinct deposition of woolly matter on the ground or soil?', type: 'select', options: ['yes', 'no'] },
    { id: 'gradual_yellowing_drying', text: 'Is there a gradual yellowing and drying of the foliage?', type: 'select', options: ['yes', 'no'] },
    { id: 'yellowing_from_tip_margins', text: 'Is there a yellowing of leaves from the tip along the margins?', type: 'select', options: ['yes', 'no'] },
    { id: 'profuse_tillering_3_4_months', text: 'Have you noticed profuse tillering in your 3-4 month old crop?', type: 'select', options: ['yes', 'no'] },
    { id: 'ratoon_crop_present', text: 'Do you have a ratoon crop (a second harvest from the same plant roots)?', type: 'select', options: ['yes', 'no'] }
  ];

  // Specific questions for dead heart disease detection (15 questions in exact order)
  const deadHeartQuestions = [
    { id: 'boreholes_plugged_excreta', text: 'Are there any boreholes at the base of the shoot that are plugged with excreta?', type: 'select', options: ['yes', 'no'] },
    { id: 'central_whorl_dry_withered', text: 'Is the central whorl of leaves on the plant dry or withered?', type: 'select', options: ['yes', 'no'] },
    { id: 'affected_shoots_come_off_easily', text: 'Are the affected shoots coming off easily when pulled?', type: 'select', options: ['yes', 'no'] },
    { id: 'affected_shoots_wilting_drying', text: 'Are the affected shoots wilting and drying up?', type: 'select', options: ['yes', 'no'] },
    { id: 'caterpillars_destroying_shoots', text: 'Are there any caterpillars destroying the young shoots?', type: 'select', options: ['yes', 'no'] },
    { id: 'reduction_millable_canes', text: 'Is there a reduction in the number of millable canes?', type: 'select', options: ['yes', 'no'] },
    { id: 'bore_holes_base_ground_level', text: 'Are there bore holes at the base of the shoot, just above the ground level?', type: 'select', options: ['yes', 'no'] },
    { id: 'dirty_white_larvae_violet_stripes', text: 'Have you observed any dirty white larvae with five dark violet stripes in the shoots?', type: 'select', options: ['yes', 'no'] },
    { id: 'central_shoot_comes_out_easily', text: 'When you pull on the central shoot, does it come out easily?', type: 'select', options: ['yes', 'no'] },
    { id: 'small_holes_stem_near_ground', text: 'Are there any small holes visible on the stem of the sugarcane plant near the ground?', type: 'select', options: ['yes', 'no'] },
    { id: 'crop_early_growth_phase', text: 'Is the sugarcane crop in an early phase of growth?', type: 'select', options: ['yes', 'no'] },
    { id: 'leaves_drying_tip_margins', text: 'Is there a drying of leaves from the tip along the margins?', type: 'select', options: ['yes', 'no'] },
    { id: 'plant_yellow_wilted', text: 'Does the plant look yellow and wilted?', type: 'select', options: ['yes', 'no'] },
    { id: 'rotten_central_shoot_foul_odor', text: 'Does the rotten portion of the central shoot have a foul odor?', type: 'select', options: ['yes', 'no'] },
    { id: 'rotten_straw_colored_dead_heart', text: 'Have you observed a rotten portion of the straw-colored dead heart?', type: 'select', options: ['yes', 'no'] }
  ];

  // Select questions based on disease type
  const questions = diseaseType === 'tiller' ? tillerQuestions : deadHeartQuestions;

  // Handle form input changes
  const handleInputChange = (questionId, value) => {
    const newAnswers = { ...answers, [questionId]: value };
    setAnswers(newAnswers);
    onDataChange(newAnswers);
  };

  // Handle JSON input changes
  const handleJsonChange = (e) => {
    const value = e.target.value;
    setJsonInput(value);
    
    try {
      const parsed = JSON.parse(value);
      setAnswers(parsed);
      onDataChange(parsed);
    } catch (error) {
      // Invalid JSON, don't update answers
    }
  };

  // Switch between form and JSON modes
  const switchMode = (newMode) => {
    if (newMode === 'json' && mode === 'form') {
      // Convert form answers to JSON
      setJsonInput(JSON.stringify(answers, null, 2));
    } else if (newMode === 'form' && mode === 'json') {
      // Try to parse JSON back to form
      try {
        const parsed = JSON.parse(jsonInput);
        setAnswers(parsed);
      } catch (error) {
        // Keep existing answers if JSON is invalid
      }
    }
    setMode(newMode);
  };

  // Load sample data
  const loadSampleData = () => {
    let sampleAnswers;
    
    if (diseaseType === 'tiller') {
      // Sample answers for tiller disease (15 questions)
      sampleAnswers = {
        affected_setts_spreading: 'yes',
        plants_stunted_slow_growth: 'yes',
        honey_dew_sooty_mould: 'no',
        nodal_regions_infested: 'yes',
        tillers_white_yellow: 'yes',
        high_aphid_population: 'yes',
        gaps_early_drying: 'yes',
        cane_stunted_reduced_internodes: 'yes',
        no_millable_cane_formation: 'yes',
        profuse_lateral_buds: 'no',
        woolly_matter_deposition: 'yes',
        gradual_yellowing_drying: 'yes',
        yellowing_from_tip_margins: 'yes',
        profuse_tillering_3_4_months: 'no',
        ratoon_crop_present: 'no'
      };
    } else {
      // Sample answers for dead heart disease (15 questions)
      sampleAnswers = {
        boreholes_plugged_excreta: 'yes',
        central_whorl_dry_withered: 'yes',
        affected_shoots_come_off_easily: 'yes',
        affected_shoots_wilting_drying: 'yes',
        caterpillars_destroying_shoots: 'no',
        reduction_millable_canes: 'yes',
        bore_holes_base_ground_level: 'yes',
        dirty_white_larvae_violet_stripes: 'no',
        central_shoot_comes_out_easily: 'yes',
        small_holes_stem_near_ground: 'yes',
        crop_early_growth_phase: 'yes',
        leaves_drying_tip_margins: 'yes',
        plant_yellow_wilted: 'yes',
        rotten_central_shoot_foul_odor: 'yes',
        rotten_straw_colored_dead_heart: 'yes'
      };
    }
    
    setAnswers(sampleAnswers);
    onDataChange(sampleAnswers);
    
    if (mode === 'json') {
      setJsonInput(JSON.stringify(sampleAnswers, null, 2));
    }
  };

  return (
    <div className="questionnaire">
      <div className="questionnaire-header">
        <h2>Plant Condition Assessment</h2>
        <p>Please provide information about the plant condition for {diseaseType} analysis:</p>
        
        <div className="mode-selector">
          <button 
            className={mode === 'form' ? 'active' : ''}
            onClick={() => switchMode('form')}
          >
            📝 Form Mode
          </button>
          <button 
            className={mode === 'json' ? 'active' : ''}
            onClick={() => switchMode('json')}
          >
            📄 JSON Mode
          </button>
          <button 
            className="sample-btn"
            onClick={loadSampleData}
          >
            📋 Load Sample
          </button>
        </div>
      </div>

      {mode === 'form' ? (
        <div className="form-mode">
          <div className="questions-grid">
            {questions.map((question) => (
              <div key={question.id} className="question-item">
                <label htmlFor={question.id}>{question.text}</label>
                
                {question.type === 'select' ? (
                  <select
                    id={question.id}
                    value={answers[question.id] || ''}
                    onChange={(e) => handleInputChange(question.id, e.target.value)}
                  >
                    <option value="">Select...</option>
                    {question.options.map((option) => (
                      <option key={option} value={option}>
                        {option.charAt(0).toUpperCase() + option.slice(1)}
                      </option>
                    ))}
                  </select>
                ) : (
                  <input
                    id={question.id}
                    type={question.type}
                    min={question.min}
                    max={question.max}
                    step={question.step}
                    value={answers[question.id] || ''}
                    onChange={(e) => handleInputChange(question.id, e.target.value)}
                    placeholder={`Enter ${question.text.toLowerCase()}`}
                  />
                )}
              </div>
            ))}
          </div>
        </div>
      ) : (
        <div className="json-mode">
          <p>Enter your questionnaire data as JSON:</p>
          <textarea
            value={jsonInput}
            onChange={handleJsonChange}
            placeholder='{"plant_age": 8, "leaf_yellowing": "yes", ...}'
            rows={15}
          />
          <div className="json-status">
            {(() => {
              try {
                JSON.parse(jsonInput);
                return <span className="valid">✅ Valid JSON</span>;
              } catch (error) {
                return <span className="invalid">❌ Invalid JSON</span>;
              }
            })()}
          </div>
        </div>
      )}

      <div className="questionnaire-summary">
        <p>
          <strong>Completed:</strong> {Object.keys(answers).length} / {questions.length} questions
        </p>
        {Object.keys(answers).length === 0 && (
          <p className="hint">💡 Fill out the questionnaire or use JSON mode to provide plant data</p>
        )}
      </div>
    </div>
  );
};

export default Questionnaire;
