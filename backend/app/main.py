"""
MIT License

Sugarcane Disease Detection API
Main FastAPI application with endpoints for dead heart and tiller disease detection.
"""

import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file at the very beginning
load_dotenv()

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from .models import DiseasePredictor
from .utils import setup_logging
from .weather import weather_service
from .disease_risk import disease_risk_assessor

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


# Weather and Disease Risk Endpoints

@app.get("/weather/current")
async def get_current_weather(lat: float, lon: float):
    """
    Get current weather data for given coordinates
    
    Args:
        lat: Latitude
        lon: Longitude
        
    Returns:
        Current weather data
    """
    if not weather_service.api_key:
        logger.warning("Attempted to access weather endpoint without API key.")
        raise HTTPException(
            status_code=503,
            detail="Weather service is unavailable. Administrator must configure OPENWEATHER_API_KEY."
        )
    try:
        weather_data = await weather_service.get_current_weather(lat, lon)
        return JSONResponse(content=weather_data)
    except HTTPException as e:
        # Re-raise HTTPException to preserve status code and detail
        raise e
    except Exception as e:
        logger.error(f"Error fetching weather data: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An unexpected error occurred while fetching weather data.")


@app.get("/weather/forecast")
async def get_weather_forecast(lat: float, lon: float, days: int = 5):
    """
    Get weather forecast for given coordinates
    
    Args:
        lat: Latitude
        lon: Longitude
        days: Number of days for forecast (default: 5)
        
    Returns:
        Weather forecast data
    """
    if not weather_service.api_key:
        logger.warning("Attempted to access weather endpoint without API key.")
        raise HTTPException(
            status_code=503,
            detail="Weather service is unavailable. Administrator must configure OPENWEATHER_API_KEY."
        )
    try:
        if days < 1 or days > 5:
            raise HTTPException(status_code=400, detail="Days must be between 1 and 5")
        
        forecast_data = await weather_service.get_weather_forecast(lat, lon, days)
        return JSONResponse(content=forecast_data)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error fetching forecast data: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An unexpected error occurred while fetching forecast data.")


@app.get("/weather/disease-risk")
async def get_disease_risk_assessment(lat: float, lon: float):
    """
    Get disease risk assessment based on current weather conditions
    
    Args:
        lat: Latitude
        lon: Longitude
        
    Returns:
        Disease risk assessment for both dead heart and tiller diseases
    """
    if not weather_service.api_key:
        logger.warning("Attempted to access weather endpoint without API key.")
        raise HTTPException(
            status_code=503,
            detail="Weather service is unavailable. Administrator must configure OPENWEATHER_API_KEY."
        )
    try:
        # Get current weather data
        weather_data = await weather_service.get_current_weather(lat, lon)
        
        # Calculate disease risk
        risk_assessment = disease_risk_assessor.calculate_combined_risk(weather_data)
        
        # Add weather data to response
        risk_assessment["weather_data"] = weather_data
        
        return JSONResponse(content=risk_assessment)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error calculating disease risk: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An unexpected error occurred during risk assessment.")


@app.get("/weather/disease-risk/{disease_type}")
async def get_specific_disease_risk(disease_type: str, lat: float, lon: float):
    """
    Get disease risk assessment for a specific disease type
    
    Args:
        disease_type: Either 'deadheart' or 'tiller'
        lat: Latitude
        lon: Longitude
        
    Returns:
        Disease risk assessment for the specified disease
    """
    if not weather_service.api_key:
        logger.warning("Attempted to access weather endpoint without API key.")
        raise HTTPException(
            status_code=503,
            detail="Weather service is unavailable. Administrator must configure OPENWEATHER_API_KEY."
        )
    try:
        if disease_type not in ["deadheart", "tiller"]:
            raise HTTPException(status_code=400, detail="Disease type must be 'deadheart' or 'tiller'")
        
        # Get current weather data
        weather_data = await weather_service.get_current_weather(lat, lon)
        
        # Calculate specific disease risk
        if disease_type == "deadheart":
            risk_assessment = disease_risk_assessor.calculate_deadheart_risk(weather_data)
        else:
            risk_assessment = disease_risk_assessor.calculate_tiller_risk(weather_data)
        
        # Add weather data to response
        risk_assessment["weather_data"] = weather_data
        
        return JSONResponse(content=risk_assessment)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error calculating {disease_type} risk: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred during risk assessment.")


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
