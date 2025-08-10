import React, { useState } from 'react';
import { useTranslation } from '../contexts/LanguageContext';
import './EnhancedQuestionnaire.css';

const EnhancedQuestionnaire = ({ diseaseType, onAnswersChange, onComplete }) => {
  const { t } = useTranslation();
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState({});
  const [showImageModal, setShowImageModal] = useState(false);
  const [currentImage, setCurrentImage] = useState('');

  // Question definitions with image paths
  const getQuestionSets = () => ({
    deadheart: [
      {
        id: 'boreholes_plugged_excreta',
        text: t('questions.deadheart.boreholes_plugged_excreta.text'),
        description: t('questions.deadheart.boreholes_plugged_excreta.description'),
        image: '/images/deadheart/boreholes_plugged_excreta.jpg'
      },
      {
        id: 'central_whorl_dry_withered',
        text: 'Is the central whorl dry and withered?',
        description: 'Check if the innermost leaves at the center of the plant are dried up',
        image: '/images/deadheart/central_whorl_dry_withered.jpg'
      },
      {
        id: 'affected_shoots_come_off_easily',
        text: 'Do affected shoots come off easily when pulled?',
        description: 'Gently pull the central shoot to see if it detaches without resistance',
        image: '/images/deadheart/affected_shoots_come_off_easily.jpg'
      },
      {
        id: 'affected_shoots_wilting_drying',
        text: 'Are affected shoots showing signs of wilting and drying?',
        description: 'Look for shoots that are losing their green color and becoming dry',
        image: '/images/deadheart/affected_shoots_wilting_drying.jpg'
      },
      {
        id: 'caterpillars_destroying_shoots',
        text: 'Are there caterpillars visible destroying the shoots?',
        description: 'Check for the presence of larvae feeding on the plant shoots',
        image: '/images/deadheart/caterpillars_destroying_shoots.jpg'
      },
      {
        id: 'reduction_millable_canes',
        text: 'Is there a noticeable reduction in millable canes?',
        description: 'Compare with healthy plants to see if cane production is reduced',
        image: '/images/deadheart/reduction_millable_canes.jpg'
      },
      {
        id: 'bore_holes_base_ground_level',
        text: 'Are there bore holes visible at the base near ground level?',
        description: 'Examine the stem base close to soil level for entry holes',
        image: '/images/deadheart/bore_holes_base_ground_level.jpg'
      },
      {
        id: 'dirty_white_larvae_violet_stripes',
        text: 'Can you see dirty white larvae with violet stripes?',
        description: 'Look for caterpillars with distinctive white body and purple markings',
        image: '/images/deadheart/dirty_white_larvae_violet_stripes.jpg'
      },
      {
        id: 'central_shoot_comes_out_easily',
        text: 'Does the central shoot come out easily when pulled?',
        description: 'Test if the main growing point can be removed without force',
        image: '/images/deadheart/central_shoot_comes_out_easily.jpg'
      },
      {
        id: 'small_holes_stem_near_ground',
        text: 'Are there small holes in the stem near the ground?',
        description: 'Check the lower portion of the stem for insect entry points',
        image: '/images/deadheart/small_holes_stem_near_ground.jpg'
      },
      {
        id: 'crop_early_growth_phase',
        text: 'Is the crop in its early growth phase (1-3 months)?',
        description: 'Consider the age of the sugarcane crop when symptoms appeared',
        image: '/images/deadheart/crop_early_growth_phase.jpg'
      },
      {
        id: 'leaves_drying_tip_margins',
        text: 'Are leaves drying from tip and margins?',
        description: 'Look for browning that starts at leaf tips and edges',
        image: '/images/deadheart/leaves_drying_tip_margins.jpg'
      },
      {
        id: 'plant_yellow_wilted',
        text: 'Is the plant showing yellowing and wilting symptoms?',
        description: 'Check for overall plant stress with yellow coloration',
        image: '/images/deadheart/plant_yellow_wilted.jpg'
      },
      {
        id: 'rotten_central_shoot_foul_odor',
        text: 'Is there a rotten central shoot with foul odor?',
        description: 'Smell for any unpleasant odor from the decaying central growing point',
        image: '/images/deadheart/rotten_central_shoot_foul_odor.jpg'
      },
      {
        id: 'rotten_straw_colored_dead_heart',
        text: 'Is there a rotten, straw-colored dead heart visible?',
        description: 'Look for the characteristic dried, yellowish-brown central shoot',
        image: '/images/deadheart/rotten_straw_colored_dead_heart.jpg'
      }
    ],
    tiller: [
      {
        id: 'affected_setts_spreading',
        text: 'Are affected setts spreading the symptoms to nearby plants?',
        description: 'Check if the problem is spreading from infected planting material',
        image: '/images/tiller/affected_setts_spreading.jpg'
      },
      {
        id: 'plants_stunted_slow_growth',
        text: 'Are plants showing stunted and slow growth?',
        description: 'Compare plant height and vigor with healthy plants',
        image: '/images/tiller/plants_stunted_slow_growth.jpg'
      },
      {
        id: 'honey_dew_sooty_mould',
        text: 'Is there honey dew and sooty mould present?',
        description: 'Look for sticky secretions and black fungal growth on leaves',
        image: '/images/tiller/honey_dew_sooty_mould.jpg'
      },
      {
        id: 'nodal_regions_infested',
        text: 'Are nodal regions heavily infested with insects?',
        description: 'Check the joints of the stem for high insect populations',
        image: '/images/tiller/nodal_regions_infested.jpg'
      },
      {
        id: 'tillers_white_yellow',
        text: 'Are tillers showing white to yellow coloration?',
        description: 'Look for side shoots that have lost their green color',
        image: '/images/tiller/tillers_white_yellow.jpg'
      },
      {
        id: 'high_aphid_population',
        text: 'Is there a high population of aphids visible?',
        description: 'Check for clusters of small, soft-bodied insects on plants',
        image: '/images/tiller/high_aphid_population.jpg'
      },
      {
        id: 'gaps_early_drying',
        text: 'Are there gaps in the field due to early plant drying?',
        description: 'Look for missing plants or dead spots in the field',
        image: '/images/tiller/gaps_early_drying.jpg'
      },
      {
        id: 'cane_stunted_reduced_internodes',
        text: 'Are canes stunted with reduced internodes?',
        description: 'Check if stem segments between nodes are shorter than normal',
        image: '/images/tiller/cane_stunted_reduced_internodes.jpg'
      },
      {
        id: 'no_millable_cane_formation',
        text: 'Is there no millable cane formation?',
        description: 'Assess if plants are failing to produce harvestable canes',
        image: '/images/tiller/no_millable_cane_formation.jpg'
      },
      {
        id: 'profuse_lateral_buds',
        text: 'Are there profuse lateral buds sprouting?',
        description: 'Look for excessive side bud development along the stem',
        image: '/images/tiller/profuse_lateral_buds.jpg'
      },
      {
        id: 'woolly_matter_deposition',
        text: 'Is there woolly matter deposition on plants?',
        description: 'Check for white, cotton-like material on plant surfaces',
        image: '/images/tiller/woolly_matter_deposition.jpg'
      },
      {
        id: 'gradual_yellowing_drying',
        text: 'Is there gradual yellowing and drying of plants?',
        description: 'Look for progressive color change from green to yellow to brown',
        image: '/images/tiller/gradual_yellowing_drying.jpg'
      },
      {
        id: 'yellowing_from_tip_margins',
        text: 'Is yellowing starting from leaf tips and margins?',
        description: 'Check if discoloration begins at leaf edges and spreads inward',
        image: '/images/tiller/yellowing_from_tip_margins.jpg'
      },
      {
        id: 'profuse_tillering_3_4_months',
        text: 'Is there profuse tillering at 3-4 months after planting?',
        description: 'Count the number of shoots per plant at this growth stage',
        image: '/images/tiller/profuse_tillering_3_4_months.jpg'
      },
      {
        id: 'ratoon_crop_present',
        text: 'Is this a ratoon crop (regrowth after harvest)?',
        description: 'Determine if this is the first crop or regrowth from previous harvest',
        image: '/images/tiller/ratoon_crop_present.jpg'
      }
    ]
  });

  const questions = getQuestionSets()[diseaseType] || [];
  const currentQuestion = questions[currentQuestionIndex];
  const progress = ((currentQuestionIndex + 1) / questions.length) * 100;

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
          <h3>✅ Questionnaire Complete!</h3>
          <p>All questions have been answered. Processing your responses...</p>
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
            Question {currentQuestionIndex + 1} of {questions.length}
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
                e.target.alt = 'Image not available - will be added soon';
              }}
            />
            <div className="image-overlay" onClick={() => openImageModal(currentQuestion.image)}>
              <span className="zoom-icon">🔍</span>
              <span className="zoom-text">Click to enlarge</span>
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
              ✅ Yes
            </button>
            <button
              className={`answer-btn no-btn ${answers[currentQuestion.id] === 'no' ? 'selected' : ''}`}
              onClick={() => handleAnswer('no')}
            >
              ❌ No
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
          ← Previous
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
          Next →
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
                e.target.alt = 'Image not available - will be added soon';
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
