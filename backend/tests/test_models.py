"""
MIT License

Unit tests for the disease prediction models
"""

import pytest
import numpy as np
from unittest.mock import Mock, patch
import sys
import os

# Add the parent directory to the path so we can import the app modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.models import calculate_fusion_score, DiseasePredictor


class TestFusionScoring:
    """Test cases for fusion scoring functionality"""
    
    def test_fusion_score_calculation(self):
        """Test basic fusion score calculation"""
        image_conf = 0.8
        tabnet_prob = 0.6
        w_img = 0.6
        w_tab = 0.4
        
        expected_score = w_img * image_conf + w_tab * tabnet_prob
        actual_score = calculate_fusion_score(image_conf, tabnet_prob, w_img, w_tab)
        
        assert abs(actual_score - expected_score) < 1e-6
    
    def test_fusion_score_edge_cases(self):
        """Test fusion scoring with edge case values"""
        # Test with zero values
        assert calculate_fusion_score(0.0, 0.0) == 0.0
        
        # Test with maximum values
        assert calculate_fusion_score(1.0, 1.0) == 1.0
        
        # Test with different weight combinations
        assert calculate_fusion_score(1.0, 0.0, 1.0, 0.0) == 1.0
        assert calculate_fusion_score(0.0, 1.0, 0.0, 1.0) == 1.0
    
    def test_fusion_score_default_weights(self):
        """Test fusion scoring with default weights"""
        image_conf = 0.7
        tabnet_prob = 0.5
        
        # Default weights are 0.6 and 0.4
        expected = 0.6 * 0.7 + 0.4 * 0.5
        actual = calculate_fusion_score(image_conf, tabnet_prob)
        
        assert abs(actual - expected) < 1e-6


class TestDiseasePredictor:
    """Test cases for DiseasePredictor class"""
    
    @patch('app.models.YOLO_AVAILABLE', False)
    def test_predictor_initialization_without_yolo(self):
        """Test predictor initialization when YOLO is not available"""
        predictor = DiseasePredictor(
            disease_name="test_disease",
            yolo_model_path="nonexistent.pt",
            tabnet_model_path="nonexistent.joblib"
        )
        
        assert predictor.disease_name == "test_disease"
        assert predictor.yolo_model is None
        assert predictor.tabnet_model is None
    
    def test_convert_questions_to_features(self):
        """Test question to feature conversion"""
        predictor = DiseasePredictor(
            disease_name="test_disease",
            yolo_model_path="nonexistent.pt",
            tabnet_model_path="nonexistent.joblib"
        )
        
        # Test with yes/no answers
        questions = {
            "question1": "yes",
            "question2": "no",
            "question3": "1",
            "question4": "0",
            "question5": "5.5"
        }
        
        features = predictor._convert_questions_to_features(questions)
        
        # Should convert to numerical values
        assert features[0] == 1.0  # "yes"
        assert features[1] == 0.0  # "no"
        assert features[2] == 1.0  # "1"
        assert features[3] == 0.0  # "0"
        assert features[4] == 5.5  # "5.5"
        
        # Should pad to expected length (30)
        assert len(features) == 30
    
    def test_fusion_scoring_method(self):
        """Test the fusion scoring method"""
        predictor = DiseasePredictor(
            disease_name="test_disease",
            yolo_model_path="nonexistent.pt",
            tabnet_model_path="nonexistent.joblib"
        )
        
        # Test with scores above threshold
        final_score, final_label = predictor._fusion_scoring(0.8, 0.7)
        assert final_score > 0.5
        assert final_label == "test_disease"
        
        # Test with scores below threshold
        final_score, final_label = predictor._fusion_scoring(0.2, 0.3)
        assert final_score < 0.5
        assert final_label == "not_test_disease"


if __name__ == "__main__":
    pytest.main([__file__])
