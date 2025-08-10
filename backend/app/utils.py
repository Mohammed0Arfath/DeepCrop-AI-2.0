"""
MIT License

Utility functions for the sugarcane disease detection API
"""

import logging
import os
from typing import Dict, Any
from dotenv import load_dotenv


def setup_logging():
    """Setup logging configuration"""
    load_dotenv()
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


# ---------------- Gemini Recommendations Integration ----------------

def _get_gemini_model():
    """
    Configure and return a Gemini GenerativeModel instance.
    Tries configured model, then falls back to a text-capable model.
    Returns None if GEMINI_API_KEY is not set or configuration fails.
    """
    try:
        import google.generativeai as genai  # type: ignore
    except Exception as e:
        logging.getLogger(__name__).error(f"google-generativeai not installed: {e}")
        return None

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        logging.getLogger(__name__).warning("GEMINI_API_KEY not set; recommendations will be empty.")
        return None

    try:
        genai.configure(api_key=api_key)
        model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
        try:
            return genai.GenerativeModel(model_name=model_name)
        except Exception as e1:
            logging.getLogger(__name__).warning(f"Primary Gemini model '{model_name}' failed: {e1}. Trying fallback 'gemini-pro'.")
            return genai.GenerativeModel(model_name="gemini-pro")
    except Exception as e:
        logging.getLogger(__name__).error(f"Failed to configure Gemini: {e}", exc_info=True)
        return None


def generate_recommendations(context: Dict[str, Any], language: str = "en") -> list:
    """
    Generate farmer-friendly pest management recommendations using Gemini.

    Args:
        context: dict containing fields like:
            - pest_type (deadheart/tiller)
            - image_confidence, tabnet_prob, final_score, final_label
            - detections (list)
            - questionnaire (dict)
            - location (optional: name/state/city)
            - weather_risk (optional)
        language: ISO language code to respond in (en/hi/ta/te)

    Returns:
        List of recommendation strings. Empty when disabled or on error.
    """
    logger = logging.getLogger(__name__)
    model = _get_gemini_model()
    if model is None:
        return []

    # Build a concise, safe prompt
    pest_type = str(context.get("pest_type", "unknown"))
    image_conf = context.get("image_confidence", 0.0)
    tabnet_prob = context.get("tabnet_prob", 0.0)
    final_score = context.get("final_score", 0.0)
    final_label = context.get("final_label", "unknown")
    detections = context.get("detections", [])
    questionnaire = context.get("questionnaire", {})
    location = context.get("location", {})
    weather_risk = context.get("weather_risk", {})

    # Summarize detections for prompt brevity
    det_summary = []
    try:
        for d in detections[:5]:
            kind = d.get("type", "detection")
            score = d.get("score", 0.0)
            det_summary.append(f"{kind}:{score:.2f}")
    except Exception:
        pass

    prompt = f"""
You are an agricultural advisory assistant. Provide practical, safe, step-by-step pest management guidance for sugarcane.
Respond in language code: {language}.
Audience: smallholder farmers in India.

Context:
- Pest type: {pest_type}
- Fusion result: final_label={final_label}, final_score={final_score:.2f}
- Image confidence: {image_conf:.2f}
- Questionnaire probability: {tabnet_prob:.2f}
- Detections summary (type:score): {', '.join(det_summary) if det_summary else 'none'}
- Location (optional): {location}
- Weather risk (optional): {weather_risk}
- Questionnaire answers (yes/no): {questionnaire}

Requirements:
- Output 4 to 8 short bullet points.
- Use clear, non-technical language suitable for farmers.
- Include: immediate checks/monitoring, sanitation, cultural practices (field hygiene, irrigation, spacing), biological controls where appropriate, and when to consult local agri-extension.
- Do NOT prescribe specific pesticide brands or doses. Keep guidance general and safe.
- No placeholders. Do not include any analysis text outside the bullet points.

Return ONLY the bullet points.
""".strip()

    try:
        timeout_s = int(os.getenv("GEMINI_TIMEOUT", "15"))
    except ValueError:
        timeout_s = 15

    try:
        # Generate content (explicit generation config; pass contents as list for compatibility)
        generation_config = {"temperature": 0.4, "max_output_tokens": 512}
        response = model.generate_content([prompt], safety_settings=None, generation_config=generation_config, request_options={"timeout": timeout_s})
        text = getattr(response, "text", "") or ""
        if not text:
            try:
                # Fallback: assemble text from candidates/parts
                parts = []
                if hasattr(response, "candidates") and response.candidates:
                    for c in response.candidates:
                        if getattr(c, "content", None) and getattr(c.content, "parts", None):
                            for p in c.content.parts:
                                val = getattr(p, "text", None)
                                if not val and isinstance(p, str):
                                    val = p
                                if val:
                                    parts.append(val)
                if parts:
                    text = "\n".join(parts)
            except Exception:
                pass
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        # Normalize bullets
        recs = []
        import re
        for ln in lines:
            # Strip leading bullets
            if ln.startswith(("-", "•", "*")):
                ln = ln.lstrip("-•* ").strip()
            # Remove leading numbering like "1.", "1)", "1 -"
            ln = re.sub(r"^\s*\d+[\.\)]\s*", "", ln)
            if ln:
                recs.append(ln)
        # Fallback: if model returned a paragraph, split by ". "
        if not recs and text:
            chunks = [c.strip() for c in text.replace("•", "-").split("-") if c.strip()]
            if chunks:
                recs = chunks[:8]
        # Truncate to 8
        return recs[:8]
    except Exception as e:
        logger.error(f"Gemini recommendation error: {e}", exc_info=True)
        return []
