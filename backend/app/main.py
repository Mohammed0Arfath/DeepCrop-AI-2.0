"""
MIT License

Sugarcane Disease Detection API
Main FastAPI application with endpoints for dead heart and tiller disease detection.
"""

import os
import logging
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from .models import DiseasePredictor
from .utils import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Sugarcane Disease Detection API",
    description="API for detecting dead heart and tiller diseases in sugarcane using YOLO and TabNet models",
    version="1.0.0"
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize disease predictors
try:
    deadheart_predictor = DiseasePredictor(
        disease_name="deadheart",
        yolo_model_path=os.getenv("DEADHEART_YOLO_PATH", "models/yolov_deadheart.pt"),
        tabnet_model_path=os.getenv("DEADHEART_TABNET_PATH", "models/tabnet_deadheart.joblib")
    )
    
    tiller_predictor = DiseasePredictor(
        disease_name="tiller",
        yolo_model_path=os.getenv("TILLER_YOLO_PATH", "models/yolov_tiller.pt"),
        tabnet_model_path=os.getenv("TILLER_TABNET_PATH", "models/tabnet_tiller.joblib")
    )
    
    logger.info("Disease predictors initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize predictors: {e}")
    # Continue without models for development/testing


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Sugarcane Disease Detection API is running"}


@app.post("/predict/deadheart")
async def predict_deadheart(
    image: UploadFile = File(..., description="Image file (JPEG/PNG)"),
    questions: str = Form(..., description="JSON string containing questionnaire answers")
):
    """
    Predict dead heart disease from image and questionnaire data
    
    Args:
        image: Uploaded image file (JPEG/PNG)
        questions: JSON string with questionnaire answers
        
    Returns:
        JSON response with prediction results and overlay image
    """
    try:
        # Validate file type
        if not image.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Process prediction
        result = await deadheart_predictor.predict(image, questions)
        return JSONResponse(content=result)
        
    except Exception as e:
        logger.error(f"Error in deadheart prediction: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@app.post("/predict/tiller")
async def predict_tiller(
    image: UploadFile = File(..., description="Image file (JPEG/PNG)"),
    questions: str = Form(..., description="JSON string containing questionnaire answers")
):
    """
    Predict tiller disease from image and questionnaire data
    
    Args:
        image: Uploaded image file (JPEG/PNG)
        questions: JSON string with questionnaire answers
        
    Returns:
        JSON response with prediction results and overlay image
    """
    try:
        # Validate file type
        if not image.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Process prediction
        result = await tiller_predictor.predict(image, questions)
        return JSONResponse(content=result)
        
    except Exception as e:
        logger.error(f"Error in tiller prediction: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"detail": "Endpoint not found"}
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


if __name__ == "__main__":
    # Run the application
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
