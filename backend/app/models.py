"""
MIT License

Disease prediction models integration
Handles YOLO image detection and TabNet questionnaire analysis with fusion scoring.
"""

import os
import json
import base64
import tempfile
import logging
from io import BytesIO
from typing import Dict, List, Any, Tuple
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import cv2
import joblib

# YOLO imports (using ultralytics)
try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False
    logging.warning("Ultralytics YOLO not available. Install with: pip install ultralytics")

logger = logging.getLogger(__name__)


class DiseasePredictor:
    """
    Main class for disease prediction combining YOLO image detection and TabNet questionnaire analysis
    """
    
    def __init__(self, disease_name: str, yolo_model_path: str, tabnet_model_path: str):
        """
        Initialize the disease predictor
        
        Args:
            disease_name: Name of the disease (e.g., 'dead_heart', 'tiller')
            yolo_model_path: Path to the YOLO model file (.pt)
            tabnet_model_path: Path to the TabNet model file (.joblib)
        """
        self.disease_name = disease_name
        self.yolo_model_path = yolo_model_path
        self.tabnet_model_path = tabnet_model_path
        
        # Fusion weights (configurable via environment variables)
        self.w_img = float(os.getenv("IMAGE_WEIGHT", "0.6"))
        self.w_tab = float(os.getenv("TABNET_WEIGHT", "0.4"))
        
        # Load models
        self.yolo_model = self._load_yolo_model()
        # Map class indices to names if available (Ultralytics provides model.names)
        self.class_names = {}
        try:
            if self.yolo_model and hasattr(self.yolo_model, "names"):
                names = self.yolo_model.names
                if isinstance(names, dict):
                    self.class_names = {int(k): str(v) for k, v in names.items()}
                elif isinstance(names, list):
                    self.class_names = {i: str(n) for i, n in enumerate(names)}
        except Exception:
            self.class_names = {}
        self.tabnet_model = self._load_tabnet_model()
        
        logger.info(f"Initialized {disease_name} predictor with weights: img={self.w_img}, tabnet={self.w_tab}")
    
    def _load_yolo_model(self):
        """Load YOLO model from file"""
        try:
            if not YOLO_AVAILABLE:
                logger.warning("YOLO not available, using mock model")
                return None
                
            if not os.path.exists(self.yolo_model_path):
                logger.warning(f"YOLO model not found at {self.yolo_model_path}, using mock model")
                return None
                
            model = YOLO(self.yolo_model_path)
            size_info = None
            try:
                size_info = os.path.getsize(self.yolo_model_path)
            except Exception:
                size_info = None
            # Log basic model info and classes if available
            names = []
            try:
                raw_names = getattr(model, "names", {})
                if isinstance(raw_names, dict):
                    names = [str(v) for _, v in sorted(raw_names.items(), key=lambda x: int(x[0]))]
                elif isinstance(raw_names, list):
                    names = [str(n) for n in raw_names]
            except Exception:
                names = []
            logger.info(f"Loaded YOLO model from {self.yolo_model_path} (size={size_info}) classes={names if names else 'unknown'}")
            return model
            
        except Exception as e:
            logger.error(f"Failed to load YOLO model: {e}")
            return None
    
    def _load_tabnet_model(self):
        """Load TabNet model from joblib file"""
        try:
            if not os.path.exists(self.tabnet_model_path):
                logger.warning(f"TabNet model not found at {self.tabnet_model_path}, using mock model")
                return None
                
            model = joblib.load(self.tabnet_model_path)
            logger.info(f"Loaded TabNet model from {self.tabnet_model_path}")
            return model
            
        except Exception as e:
            logger.error(f"Failed to load TabNet model: {e}")
            return None
    
    async def predict(self, image_file, questions_json: str) -> Dict[str, Any]:
        """
        Main prediction function combining YOLO and TabNet
        
        Args:
            image_file: Uploaded image file
            questions_json: JSON string with questionnaire answers
            
        Returns:
            Dictionary with prediction results
        """
        # Save uploaded image to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
            content = await image_file.read()
            temp_file.write(content)
            temp_image_path = temp_file.name
        
        try:
            # Process image with YOLO
            image_confidence, detections, overlay_image_b64 = self._process_image(temp_image_path)
            
            # Process questionnaire with TabNet
            tabnet_prob = self._process_questionnaire(questions_json)
            
            # Fusion scoring
            final_score, final_label = self._fusion_scoring(image_confidence, tabnet_prob)
            
            # Prepare response
            result = {
                "image_confidence": round(image_confidence, 3),
                "tabnet_prob": round(tabnet_prob, 3),
                "final_score": round(final_score, 3),
                "final_label": final_label,
                "detections": detections,
                "overlay_image_base64": overlay_image_b64
            }
            
            return result
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_image_path):
                os.unlink(temp_image_path)
    
    def _process_image(self, image_path: str) -> Tuple[float, List[Dict], str]:
        """
        Process image with YOLO model
        Handles both bounding box detection (tiller) and segmentation (dead heart)
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Tuple of (confidence, detections, overlay_image_base64)
        """
        # Load image
        image = Image.open(image_path)
        
        if self.yolo_model is None:
            raise RuntimeError(f"YOLO model not loaded for {self.disease_name}")
        
        # Run YOLO prediction with error handling for corrupted segmentation models
        logger.info(f"Running YOLO prediction for {self.disease_name}")
        conf = float(os.getenv("YOLO_CONF", "0.25"))
        iou = float(os.getenv("YOLO_IOU", "0.45"))
        imgsz = int(os.getenv("IMG_SIZE", "640"))
        device = os.getenv("YOLO_DEVICE", "").strip() or None
        
        try:
            results = self.yolo_model.predict(source=image_path, imgsz=imgsz, conf=conf, iou=iou, device=device, verbose=False)
        except AttributeError as e:
            if "'Segment' object has no attribute 'detect'" in str(e):
                logger.error(f"Segmentation model corruption detected: {e}")
                logger.info("Attempting to reload model with detection head...")
                
                # Try to reload as detection model
                try:
                    from ultralytics import YOLO
                    # Force reload the model
                    self.yolo_model = YOLO(self.yolo_model_path)
                    # Try prediction again
                    results = self.yolo_model.predict(source=image_path, imgsz=imgsz, conf=conf, iou=iou, device=device, verbose=False)
                    logger.info("Successfully reloaded and predicted with model")
                except Exception as reload_error:
                    logger.error(f"Model reload failed: {reload_error}")
                    # Use TabNet-only prediction as fallback
                    logger.info("Using TabNet-only prediction as fallback")
                    return self._tabnet_only_prediction(image)
            else:
                raise e
        except Exception as e:
            logger.error(f"Unexpected error during YOLO prediction: {e}")
            # Use TabNet-only prediction as fallback
            return self._tabnet_only_prediction(image)
        
        # Extract detections
        detections = []
        max_confidence = 0.0
        
        for result in results:
            logger.info(f"Processing result type: {type(result)}")
            logger.info(f"Result attributes: {[attr for attr in dir(result) if not attr.startswith('_')]}")
            
            # Handle segmentation masks (for dead heart - YOLOv8 segmentation)
            if hasattr(result, 'masks') and result.masks is not None:
                logger.info("Found segmentation masks")
                logger.info(f"Masks type: {type(result.masks)}")
                logger.info(f"Masks attributes: {[attr for attr in dir(result.masks) if not attr.startswith('_')]}")
                
                # YOLOv8 segmentation masks
                masks_data = result.masks.data.cpu().numpy()  # Shape: (N, H, W)
                logger.info(f"Masks data shape: {masks_data.shape}")
                
                # Get polygon coordinates
                masks_xy = result.masks.xy if hasattr(result.masks, 'xy') else None
                logger.info(f"Masks XY available: {masks_xy is not None}")
                
                # Get boxes, classes, and confidence scores if available
                if hasattr(result, 'boxes') and result.boxes is not None:
                    boxes_np = result.boxes.xyxy.cpu().numpy()
                    scores = result.boxes.conf.cpu().numpy()
                    classes_np = result.boxes.cls.cpu().numpy() if hasattr(result.boxes, 'cls') else np.zeros(len(scores))
                    logger.info(f"Found {len(scores)} instances with scores: {scores}")
                else:
                    boxes_np = np.zeros((len(masks_data), 4))
                    classes_np = np.zeros(len(masks_data))
                    scores = np.array([0.8] * len(masks_data))
                    logger.info("No boxes found, using default confidence and empty boxes")
                
                # Process each mask
                for i, (mask, score) in enumerate(zip(masks_data, scores)):
                    logger.info(f"Processing mask {i}: shape={mask.shape}, score={score}")
                    
                    # Get polygon coordinates if available
                    polygon = None
                    if masks_xy and i < len(masks_xy):
                        polygon_data = masks_xy[i]
                        if hasattr(polygon_data, 'tolist'):
                            polygon = polygon_data.tolist()
                        elif hasattr(polygon_data, 'cpu'):
                            polygon = polygon_data.cpu().numpy().tolist()
                        else:
                            polygon = polygon_data
                        logger.info(f"Polygon for mask {i}: {len(polygon) if polygon else 0} points")
                    
                    # Derive bounding box for this mask
                    if i < len(boxes_np):
                        x1, y1, x2, y2 = boxes_np[i]
                    else:
                        ys, xs = np.where(mask > 0.5)
                        if len(xs) > 0 and len(ys) > 0:
                            x1, y1, x2, y2 = np.min(xs), np.min(ys), np.max(xs), np.max(ys)
                        else:
                            x1, y1, x2, y2 = 0, 0, 0, 0
                    box_list = [int(x1), int(y1), int(x2), int(y2)]
                    # Class label
                    cls_idx = int(classes_np[i]) if i < len(classes_np) else 0
                    label_name = self.class_names.get(cls_idx, self.disease_name) if hasattr(self, "class_names") else self.disease_name
                    
                    detection = {
                        "mask": mask.tolist(),  # Binary mask
                        "polygon": polygon,     # Polygon coordinates
                        "box": box_list,
                        "score": float(score),
                        "class": label_name,
                        "type": "segmentation"
                    }
                    detections.append(detection)
                    max_confidence = max(max_confidence, float(score))
                    
                logger.info(f"Successfully processed {len(detections)} segmentation detections")
            
            # Handle bounding boxes (for tiller or detection fallback)
            elif hasattr(result, 'boxes') and result.boxes is not None:
                logger.info("Processing bounding boxes")
                boxes = result.boxes.xyxy.cpu().numpy()  # x1, y1, x2, y2
                scores = result.boxes.conf.cpu().numpy()
                classes = result.boxes.cls.cpu().numpy() if hasattr(result.boxes, 'cls') else [0] * len(boxes)
                
                logger.info(f"Found {len(boxes)} bounding boxes with scores: {scores}")
                
                for box, score, cls in zip(boxes, scores, classes):
                    label_name = self.class_names.get(int(cls), self.disease_name) if hasattr(self, "class_names") else self.disease_name
                    detection = {
                        "box": [int(box[0]), int(box[1]), int(box[2]), int(box[3])],
                        "score": float(score),
                        "class": label_name,
                        "type": "detection"
                    }
                    detections.append(detection)
                    max_confidence = max(max_confidence, float(score))
                    
                logger.info(f"Successfully processed {len(detections)} bounding box detections")
            
            else:
                logger.warning("No masks or boxes found in result")
        
        logger.info(f"Total detections: {len(detections)}, Max confidence: {max_confidence}")
        
        # Create overlay image with appropriate visualization
        overlay_image_b64 = self._create_overlay_image(image, detections)
        
        return max_confidence, detections, overlay_image_b64
    
    def _process_questionnaire(self, questions_json: str) -> float:
        """
        Process questionnaire data with TabNet model
        
        Args:
            questions_json: JSON string with questionnaire answers
            
        Returns:
            Probability score from TabNet model
        """
        try:
            # Parse questions JSON
            questions_data = json.loads(questions_json)
            
            # Convert to features (TODO: User needs to customize this based on their questionnaire)
            features = self._convert_questions_to_features(questions_data)
            
            if self.tabnet_model is None:
                # Mock prediction for development
                logger.info("Using mock TabNet prediction")
                return 0.65
            
            # Prepare input for TabNet
            X = np.array([features])
            
            # Try predict_proba first, fallback to predict
            if hasattr(self.tabnet_model, 'predict_proba'):
                proba = self.tabnet_model.predict_proba(X)
                # Assuming binary classification, take positive class probability
                return float(proba[0][1]) if proba.shape[1] > 1 else float(proba[0][0])
            else:
                prediction = self.tabnet_model.predict(X)
                # Convert prediction to probability (assuming 0-1 range or binary)
                return float(prediction[0]) if prediction[0] <= 1.0 else float(prediction[0] > 0.5)
                
        except Exception as e:
            logger.error(f"Error processing questionnaire: {e}")
            return 0.5  # Default neutral probability
    
    def _convert_questions_to_features(self, questions_data: Dict) -> List[float]:
        """
        Convert questionnaire answers to model features
        
        For tiller disease: 15 specific questions (all yes/no)
        For dead heart disease: Mixed question types
        
        Args:
            questions_data: Dictionary with question answers
            
        Returns:
            List of numerical features for the model
        """
        features = []
        
        if self.disease_name == 'tiller':
            # Tiller disease: 15 specific questions in exact order
            tiller_question_order = [
                'affected_setts_spreading',
                'plants_stunted_slow_growth', 
                'honey_dew_sooty_mould',
                'nodal_regions_infested',
                'tillers_white_yellow',
                'high_aphid_population',
                'gaps_early_drying',
                'cane_stunted_reduced_internodes',
                'no_millable_cane_formation',
                'profuse_lateral_buds',
                'woolly_matter_deposition',
                'gradual_yellowing_drying',
                'yellowing_from_tip_margins',
                'profuse_tillering_3_4_months',
                'ratoon_crop_present'
            ]
            
            # Convert each question in order (yes=1, no=0)
            for question_id in tiller_question_order:
                value = questions_data.get(question_id, 'no')
                if isinstance(value, str):
                    features.append(1.0 if value.lower() == 'yes' else 0.0)
                else:
                    features.append(0.0)
                    
        else:
            # Dead heart disease: 15 specific questions in exact order
            deadheart_question_order = [
                'boreholes_plugged_excreta',
                'central_whorl_dry_withered',
                'affected_shoots_come_off_easily',
                'affected_shoots_wilting_drying',
                'caterpillars_destroying_shoots',
                'reduction_millable_canes',
                'bore_holes_base_ground_level',
                'dirty_white_larvae_violet_stripes',
                'central_shoot_comes_out_easily',
                'small_holes_stem_near_ground',
                'crop_early_growth_phase',
                'leaves_drying_tip_margins',
                'plant_yellow_wilted',
                'rotten_central_shoot_foul_odor',
                'rotten_straw_colored_dead_heart'
            ]
            
            # Convert each question in order (yes=1, no=0)
            for question_id in deadheart_question_order:
                value = questions_data.get(question_id, 'no')
                if isinstance(value, str):
                    features.append(1.0 if value.lower() == 'yes' else 0.0)
                else:
                    features.append(0.0)
        
        # Ensure we have the right number of features (both diseases now have 15 questions)
        expected_features = 15
        
        if len(features) < expected_features:
            features.extend([0.0] * (expected_features - len(features)))
        elif len(features) > expected_features:
            features = features[:expected_features]
        
        return features
    
    def _fusion_scoring(self, image_confidence: float, tabnet_prob: float) -> Tuple[float, str]:
        """
        Combine image and tabnet predictions using weighted fusion
        
        Args:
            image_confidence: Confidence from YOLO model
            tabnet_prob: Probability from TabNet model
            
        Returns:
            Tuple of (final_score, final_label)
        """
        final_score = self.w_img * image_confidence + self.w_tab * tabnet_prob
        
        # Determine final label based on threshold
        threshold = float(os.getenv("PREDICTION_THRESHOLD", "0.5"))
        
        if final_score >= threshold:
            final_label = self.disease_name
        else:
            final_label = f"not_{self.disease_name}"
        
        return final_score, final_label
    
    def _create_overlay_image(self, image: Image.Image, detections: List[Dict]) -> str:
        """
        Create overlay image with bounding boxes, segmentation masks, and labels
        
        Args:
            image: PIL Image object
            detections: List of detection dictionaries
            
        Returns:
            Base64 encoded PNG image string
        """
        # Convert PIL image to OpenCV format for better mask handling
        img_array = np.array(image)
        if len(img_array.shape) == 3:
            img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        
        # Create overlay
        overlay = img_array.copy()
        
        # Process each detection
        for detection in detections:
            score = detection["score"]
            class_name = detection["class"]
            detection_type = detection.get("type", "detection")
            
            if detection_type == "segmentation" and ("mask" in detection or "polygon" in detection):
                # Handle segmentation masks (for dead heart)
                
                # Try polygon first (more accurate for YOLOv8 segmentation)
                if "polygon" in detection and detection["polygon"] is not None:
                    try:
                        polygon = np.array(detection["polygon"], dtype=np.int32)
                        if len(polygon.shape) == 2 and polygon.shape[1] == 2:
                            # Draw filled polygon
                            cv2.fillPoly(overlay, [polygon], (0, 255, 0))
                            
                            # Draw polygon outline
                            cv2.polylines(overlay, [polygon], True, (0, 255, 0), 2)
                            
                            # Add label near polygon centroid
                            M = cv2.moments(polygon)
                            if M["m00"] != 0:
                                cx = int(M["m10"] / M["m00"])
                                cy = int(M["m01"] / M["m00"])
                            else:
                                cx, cy = polygon[0]
                            
                            label = f"{class_name}: {score:.2f}"
                            label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
                            cv2.rectangle(overlay, (cx-10, cy-25), (cx + label_size[0] + 10, cy), (0, 255, 0), -1)
                            cv2.putText(overlay, label, (cx, cy - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                            
                    except Exception as poly_error:
                        logger.warning(f"Error drawing polygon: {poly_error}")
                        # Fall back to mask if polygon fails
                        if "mask" in detection:
                            mask = np.array(detection["mask"], dtype=np.uint8)
                            if mask.shape != img_array.shape[:2]:
                                mask = cv2.resize(mask, (img_array.shape[1], img_array.shape[0]))
                            
                            colored_mask = np.zeros_like(img_array)
                            colored_mask[mask > 0] = (0, 255, 0)
                            alpha = 0.4
                            overlay = cv2.addWeighted(overlay, 1-alpha, colored_mask, alpha, 0)
                
                # Use mask if no polygon available
                elif "mask" in detection:
                    mask = np.array(detection["mask"], dtype=np.uint8)
                    
                    # Resize mask to match image dimensions if needed
                    if mask.shape != img_array.shape[:2]:
                        mask = cv2.resize(mask, (img_array.shape[1], img_array.shape[0]))
                    
                    # Create colored mask overlay
                    color = (0, 255, 0)  # Green for dead heart segmentation
                    colored_mask = np.zeros_like(img_array)
                    colored_mask[mask > 0] = color
                    
                    # Blend with original image
                    alpha = 0.4
                    overlay = cv2.addWeighted(overlay, 1-alpha, colored_mask, alpha, 0)
                    
                    # Draw contours for better visibility
                    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    cv2.drawContours(overlay, contours, -1, (0, 255, 0), 2)
                    
                    # Add label near the largest contour
                    if contours:
                        largest_contour = max(contours, key=cv2.contourArea)
                        x, y, w, h = cv2.boundingRect(largest_contour)
                        label = f"{class_name}: {score:.2f}"
                        
                        # Draw label background
                        label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
                        cv2.rectangle(overlay, (x, y-25), (x + label_size[0] + 10, y), (0, 255, 0), -1)
                        
                        # Draw label text
                        cv2.putText(overlay, label, (x + 5, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            elif detection_type == "detection" and "box" in detection:
                # Handle bounding boxes (for tiller)
                box = detection["box"]
                
                # Draw bounding box
                cv2.rectangle(overlay, (box[0], box[1]), (box[2], box[3]), (0, 0, 255), 3)
                
                # Draw label with score
                label = f"{class_name}: {score:.2f}"
                label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
                
                # Draw label background
                cv2.rectangle(overlay, (box[0], box[1]-25), (box[0] + label_size[0] + 10, box[1]), (0, 0, 255), -1)
                
                # Draw label text
                cv2.putText(overlay, label, (box[0] + 5, box[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Convert back to PIL Image
        if len(overlay.shape) == 3:
            overlay_rgb = cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB)
        else:
            overlay_rgb = overlay
        
        overlay_pil = Image.fromarray(overlay_rgb)
        
        # Convert to base64
        buffer = BytesIO()
        overlay_pil.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return f"data:image/png;base64,{img_str}"
    


def calculate_fusion_score(image_confidence: float, tabnet_prob: float, 
                          w_img: float = 0.6, w_tab: float = 0.4) -> float:
    """
    Utility function for calculating fusion score (used in tests)
    
    Args:
        image_confidence: Image model confidence
        tabnet_prob: TabNet model probability
        w_img: Weight for image confidence
        w_tab: Weight for TabNet probability
        
    Returns:
        Fused score
    """
    return w_img * image_confidence + w_tab * tabnet_prob
