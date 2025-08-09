"""
MIT License

Utility functions for the sugarcane disease detection API
"""

import logging
import os
from typing import Dict, Any


def setup_logging():
    """Setup logging configuration"""
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    
    logging.basicConfig(
        level=getattr(logging, log_level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("app.log") if os.getenv("LOG_TO_FILE") else logging.NullHandler()
        ]
    )


def validate_image_file(file_content_type: str) -> bool:
    """
    Validate if the uploaded file is a valid image
    
    Args:
        file_content_type: Content type of the uploaded file
        
    Returns:
        True if valid image, False otherwise
    """
    valid_types = [
        "image/jpeg",
        "image/jpg",
        "image/png",
        "image/gif",
        "image/bmp",
        "image/webp"
    ]
    
    return file_content_type.lower() in valid_types


def validate_questions_json(questions_str: str) -> Dict[str, Any]:
    """
    Validate and parse questions JSON string
    
    Args:
        questions_str: JSON string with questionnaire answers
        
    Returns:
        Parsed dictionary
        
    Raises:
        ValueError: If JSON is invalid
    """
    import json
    
    try:
        questions_data = json.loads(questions_str)
        if not isinstance(questions_data, dict):
            raise ValueError("Questions must be a JSON object")
        return questions_data
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format: {e}")


def create_temp_directory():
    """Create temporary directory for file processing"""
    import tempfile
    temp_dir = tempfile.mkdtemp(prefix="sugarcane_detection_")
    return temp_dir


def cleanup_temp_files(temp_dir: str):
    """Clean up temporary files and directory"""
    import shutil
    try:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
    except Exception as e:
        logging.error(f"Failed to cleanup temp directory {temp_dir}: {e}")


def get_model_info(model_path: str) -> Dict[str, Any]:
    """
    Get information about a model file
    
    Args:
        model_path: Path to the model file
        
    Returns:
        Dictionary with model information
    """
    info = {
        "path": model_path,
        "exists": os.path.exists(model_path),
        "size": None,
        "modified": None
    }
    
    if info["exists"]:
        stat = os.stat(model_path)
        info["size"] = stat.st_size
        info["modified"] = stat.st_mtime
    
    return info


def format_prediction_response(
    image_confidence: float,
    tabnet_prob: float,
    final_score: float,
    final_label: str,
    detections: list,
    overlay_image_b64: str
) -> Dict[str, Any]:
    """
    Format the prediction response in a consistent way
    
    Args:
        image_confidence: Confidence from image model
        tabnet_prob: Probability from TabNet model
        final_score: Final fused score
        final_label: Final prediction label
        detections: List of detections
        overlay_image_b64: Base64 encoded overlay image
        
    Returns:
        Formatted response dictionary
    """
    return {
        "image_confidence": round(float(image_confidence), 3),
        "tabnet_prob": round(float(tabnet_prob), 3),
        "final_score": round(float(final_score), 3),
        "final_label": str(final_label),
        "detections": detections,
        "overlay_image_base64": overlay_image_b64,
        "metadata": {
            "fusion_weights": {
                "image": float(os.getenv("IMAGE_WEIGHT", "0.6")),
                "tabnet": float(os.getenv("TABNET_WEIGHT", "0.4"))
            },
            "threshold": float(os.getenv("PREDICTION_THRESHOLD", "0.5"))
        }
    }


def log_prediction_request(disease_type: str, image_filename: str, questions_count: int):
    """
    Log prediction request for monitoring
    
    Args:
        disease_type: Type of disease being predicted
        image_filename: Name of the uploaded image file
        questions_count: Number of questions in the questionnaire
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Prediction request - Disease: {disease_type}, Image: {image_filename}, Questions: {questions_count}")


def get_environment_config() -> Dict[str, Any]:
    """
    Get current environment configuration
    
    Returns:
        Dictionary with environment settings
    """
    return {
        "image_weight": float(os.getenv("IMAGE_WEIGHT", "0.6")),
        "tabnet_weight": float(os.getenv("TABNET_WEIGHT", "0.4")),
        "prediction_threshold": float(os.getenv("PREDICTION_THRESHOLD", "0.5")),
        "log_level": os.getenv("LOG_LEVEL", "INFO"),
        "log_to_file": os.getenv("LOG_TO_FILE", "false").lower() == "true",
        "model_paths": {
            "deadheart_yolo": os.getenv("DEADHEART_YOLO_PATH", "models/yolov_deadheart.pt"),
            "deadheart_tabnet": os.getenv("DEADHEART_TABNET_PATH", "models/tabnet_deadheart.joblib"),
            "tiller_yolo": os.getenv("TILLER_YOLO_PATH", "models/yolov_tiller.pt"),
            "tiller_tabnet": os.getenv("TILLER_TABNET_PATH", "models/tabnet_tiller.joblib")
        }
    }
