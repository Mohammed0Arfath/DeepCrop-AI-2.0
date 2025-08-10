import React, { useState } from 'react';
import { useTranslation } from '../contexts/LanguageContext';
import './EnhancedQuestionnaire.css';

const EnhancedQuestionnaire = ({ diseaseType, onAnswersChange, onComplete }) => {
  const { t } = useTranslation();
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState({});
  const [showImageModal, setShowImageModal] = useState(false);
  const [currentImage, setCurrentImage] = useState('');

  // Question definitions with image paths (fully localized via t())
  const getQuestionSets = () => {
    const deadheartDefs = [
      ['boreholes_plugged_excreta', '/images/deadheart/boreholes_plugged_excreta.jpg'],
      ['central_whorl_dry_withered', '/images/deadheart/central_whorl_dry_withered.jpg'],
      ['affected_shoots_come_off_easily', '/images/deadheart/affected_shoots_come_off_easily.jpg'],
      ['affected_shoots_wilting_drying', '/images/deadheart/affected_shoots_wilting_drying.jpg'],
      ['caterpillars_destroying_shoots', '/images/deadheart/caterpillars_destroying_shoots.jpg'],
      ['reduction_millable_canes', '/images/deadheart/reduction_millable_canes.jpg'],
      ['bore_holes_base_ground_level', '/images/deadheart/bore_holes_base_ground_level.jpg'],
      ['dirty_white_larvae_violet_stripes', '/images/deadheart/dirty_white_larvae_violet_stripes.jpg'],
      ['central_shoot_comes_out_easily', '/images/deadheart/central_shoot_comes_out_easily.jpg'],
      ['small_holes_stem_near_ground', '/images/deadheart/small_holes_stem_near_ground.jpg'],
      ['crop_early_growth_phase', '/images/deadheart/crop_early_growth_phase.jpg'],
      ['leaves_drying_tip_margins', '/images/deadheart/leaves_drying_tip_margins.jpg'],
      ['plant_yellow_wilted', '/images/deadheart/plant_yellow_wilted.jpg'],
      ['rotten_central_shoot_foul_odor', '/images/deadheart/rotten_central_shoot_foul_odor.jpg'],
      ['rotten_straw_colored_dead_heart', '/images/deadheart/rotten_straw_colored_dead_heart.jpg']
    ];
    const tillerDefs = [
      ['affected_setts_spreading', '/images/tiller/affected_setts_spreading.jpg'],
      ['plants_stunted_slow_growth', '/images/tiller/plants_stunted_slow_growth.jpg'],
      ['honey_dew_sooty_mould', '/images/tiller/honey_dew_sooty_mould.jpg'],
      ['nodal_regions_infested', '/images/tiller/nodal_regions_infested.jpg'],
      ['tillers_white_yellow', '/images/tiller/tillers_white_yellow.jpg'],
      ['high_aphid_population', '/images/tiller/high_aphid_population.jpg'],
      ['gaps_early_drying', '/images/tiller/gaps_early_drying.jpg'],
      ['cane_stunted_reduced_internodes', '/images/tiller/cane_stunted_reduced_internodes.jpg'],
      ['no_millable_cane_formation', '/images/tiller/no_millable_cane_formation.jpg'],
      ['profuse_lateral_buds', '/images/tiller/profuse_lateral_buds.jpg'],
      ['woolly_matter_deposition', '/images/tiller/woolly_matter_deposition.jpg'],
      ['gradual_yellowing_drying', '/images/tiller/gradual_yellowing_drying.jpg'],
      ['yellowing_from_tip_margins', '/images/tiller/yellowing_from_tip_margins.jpg'],
      ['profuse_tillering_3_4_months', '/images/tiller/profuse_tillering_3_4_months.jpg'],
      ['ratoon_crop_present', '/images/tiller/ratoon_crop_present.jpg']
    ];
    const mapDef = (disease, [id, image]) => ({
      id,
      text: t(`questions.${disease}.${id}.text`),
      description: t(`questions.${disease}.${id}.description`),
      image
    });
    return {
      deadheart: deadheartDefs.map(d => mapDef('deadheart', d)),
      tiller: tillerDefs.map(d => mapDef('tiller', d))
    };
  };

  const questions = getQuestionSets()[diseaseType] || [];
  const currentQuestion = questions[currentQuestionIndex];
  const progress = ((currentQuestionIndex + 1) / questions.length) * 100;
  const progressLabel = (t('questionnaire.progress', 'Question {current} of {total}'))
    .replace('{current}', currentQuestionIndex + 1)
    .replace('{total}', questions.length);

  const handleAnswer = (answer) => {
    const newAnswers = {
      ...answers,
      [currentQuestion.id]: answer
    };
    setAnswers(newAnswers);
    onAnswersChange(newAnswers);

    // Auto-advance to next question
    if (currentQuestionIndex < questions.length - 1) {
      setTimeout(() => {
        setCurrentQuestionIndex(currentQuestionIndex + 1);
      }, 300);
    } else {
      // All questions completed
      setTimeout(() => {
        onComplete(newAnswers);
      }, 300);
    }
  };

  const handlePrevious = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(currentQuestionIndex - 1);
    }
  };

  const handleNext = () => {
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
    }
  };

  const openImageModal = (imagePath) => {
    setCurrentImage(imagePath);
    setShowImageModal(true);
  };

  const closeImageModal = () => {
    setShowImageModal(false);
    setCurrentImage('');
  };

  if (!currentQuestion) {
    return (
      <div className="questionnaire-container">
        <div className="completion-message">
          <h3>✅ {t('questionnaire.completed', 'Questionnaire Complete!')}</h3>
          <p>{t('questionnaire.processing', 'All questions have been answered. Processing your responses...')}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="questionnaire-container">
      {/* Progress Bar */}
      <div className="progress-section">
        <div className="progress-info">
          <span className="progress-text">
            {progressLabel}
          </span>
          <span className="progress-percentage">{Math.round(progress)}%</span>
        </div>
        <div className="progress-bar">
          <div 
            className="progress-fill" 
            style={{ width: `${progress}%` }}
          ></div>
        </div>
      </div>

      {/* Question Card */}
      <div className="question-card">
        {/* Question Image */}
        <div className="question-image-section">
          <div className="image-container">
            <img
              src={currentQuestion.image}
              alt={`Visual guide for: ${currentQuestion.text}`}
              className="question-image"
              onClick={() => openImageModal(currentQuestion.image)}
              onError={(e) => {
                e.target.src = '/images/placeholder.jpg';
                e.target.alt = t('questionnaire.imageNotAvailable', 'Image not available - will be added soon');
              }}
            />
            <div className="image-overlay" onClick={() => openImageModal(currentQuestion.image)}>
              <span className="zoom-icon">🔍</span>
              <span className="zoom-text">{t('questionnaire.clickToEnlarge', 'Click to enlarge')}</span>
            </div>
          </div>
        </div>

        {/* Question Content */}
        <div className="question-content">
          <h3 className="question-title">{currentQuestion.text}</h3>
          <p className="question-description">{currentQuestion.description}</p>

          {/* Answer Buttons */}
          <div className="answer-buttons">
            <button
              className={`answer-btn yes-btn ${answers[currentQuestion.id] === 'yes' ? 'selected' : ''}`}
              onClick={() => handleAnswer('yes')}
            >
              ✅ {t('questionnaire.yes', 'Yes')}
            </button>
            <button
              className={`answer-btn no-btn ${answers[currentQuestion.id] === 'no' ? 'selected' : ''}`}
              onClick={() => handleAnswer('no')}
            >
              ❌ {t('questionnaire.no', 'No')}
            </button>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <div className="navigation-section">
        <button
          className="nav-btn prev-btn"
          onClick={handlePrevious}
          disabled={currentQuestionIndex === 0}
        >
          ← {t('buttons.previous', 'Previous')}
        </button>
        
        <div className="question-dots">
          {questions.map((_, index) => (
            <span
              key={index}
              className={`dot ${index === currentQuestionIndex ? 'active' : ''} ${answers[questions[index].id] ? 'answered' : ''}`}
              onClick={() => setCurrentQuestionIndex(index)}
            ></span>
          ))}
        </div>

        <button
          className="nav-btn next-btn"
          onClick={handleNext}
          disabled={currentQuestionIndex === questions.length - 1}
        >
          {t('buttons.next', 'Next')} →
        </button>
      </div>

      {/* Image Modal */}
      {showImageModal && (
        <div className="image-modal" onClick={closeImageModal}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <button className="close-btn" onClick={closeImageModal}>×</button>
            <img
              src={currentImage}
              alt="Enlarged view"
              className="modal-image"
              onError={(e) => {
                e.target.src = '/images/placeholder.jpg';
                e.target.alt = t('questionnaire.imageNotAvailable', 'Image not available - will be added soon');
              }}
            />
            <div className="modal-caption">
              <h4>{currentQuestion.text}</h4>
              <p>{currentQuestion.description}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default EnhancedQuestionnaire;
