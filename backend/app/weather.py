"""
MIT License

Weather service for fetching weather data from OpenWeatherMap API
and providing weather-based insights for sugarcane disease detection.
"""

import os
import time
import logging
from typing import Dict, Optional, Tuple
from datetime import datetime, timedelta
import httpx
from fastapi import HTTPException

logger = logging.getLogger(__name__)

class WeatherService:
    """Service for fetching and caching weather data from OpenWeatherMap API."""
    
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        self.cache_duration = int(os.getenv("WEATHER_CACHE_DURATION", "1800"))  # 30 minutes default
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.cache = {}
        
        if not self.api_key:
            logger.warning("OpenWeatherMap API key not found. Weather features will be disabled.")
    
    def _get_cache_key(self, lat: float, lon: float, endpoint: str) -> str:
        """Generate cache key for weather data."""
        return f"{endpoint}_{lat}_{lon}"
    
    def _is_cache_valid(self, timestamp: float) -> bool:
        """Check if cached data is still valid."""
        return time.time() - timestamp < self.cache_duration
    
    async def _fetch_weather_data(self, endpoint: str, params: Dict) -> Dict:
        """Fetch weather data from OpenWeatherMap API."""
        if not self.api_key:
            raise HTTPException(
                status_code=503, 
                detail="Weather service unavailable. API key not configured."
            )
        
        params["appid"] = self.api_key
        params["units"] = "metric"  # Use Celsius for temperature
        
        url = f"{self.base_url}/{endpoint}"
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"Weather API error: {e.response.status_code} - {e.response.text}")
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Weather service error: {e.response.text}"
            )
        except Exception as e:
            logger.error(f"An unexpected error occurred in the weather service: {e}", exc_info=True)
            raise HTTPException(
                status_code=503,
                detail="Weather service temporarily unavailable"
            )
    
    async def get_current_weather(self, lat: float, lon: float) -> Dict:
        """Get current weather data for given coordinates."""
        cache_key = self._get_cache_key(lat, lon, "weather")
        
        # Check cache first
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if self._is_cache_valid(timestamp):
                logger.info(f"Returning cached weather data for {lat}, {lon}")
                return cached_data
        
        # Fetch fresh data
        params = {"lat": lat, "lon": lon}
        data = await self._fetch_weather_data("weather", params)
        
        # Process and structure the data
        weather_data = {
            "location": {
                "name": data.get("name", "Unknown"),
                "country": data.get("sys", {}).get("country", ""),
                "coordinates": {"lat": lat, "lon": lon}
            },
            "current": {
                "temperature": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "humidity": data["main"]["humidity"],
                "pressure": data["main"]["pressure"],
                "visibility": data.get("visibility", 0) / 1000,  # Convert to km
                "uv_index": 0,  # Not available in current weather API
                "wind_speed": data["wind"]["speed"],
                "wind_direction": data["wind"].get("deg", 0),
                "weather_condition": data["weather"][0]["main"],
                "weather_description": data["weather"][0]["description"],
                "weather_icon": data["weather"][0]["icon"],
                "clouds": data["clouds"]["all"],
                "rainfall_1h": data.get("rain", {}).get("1h", 0),
                "rainfall_3h": data.get("rain", {}).get("3h", 0),
                "timestamp": datetime.now().isoformat()
            }
        }
        
        # Cache the data
        self.cache[cache_key] = (weather_data, time.time())
        logger.info(f"Fetched and cached weather data for {lat}, {lon}")
        
        return weather_data
    
    async def get_weather_forecast(self, lat: float, lon: float, days: int = 5) -> Dict:
        """Get weather forecast for given coordinates."""
        cache_key = self._get_cache_key(lat, lon, f"forecast_{days}")
        
        # Check cache first
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if self._is_cache_valid(timestamp):
                logger.info(f"Returning cached forecast data for {lat}, {lon}")
                return cached_data
        
        # Fetch fresh data
        params = {"lat": lat, "lon": lon, "cnt": days * 8}  # 8 forecasts per day (3-hour intervals)
        data = await self._fetch_weather_data("forecast", params)
        
        # Process forecast data
        forecasts = []
        daily_data = {}
        
        for item in data["list"]:
            date = datetime.fromtimestamp(item["dt"]).date()
            date_str = date.isoformat()
            
            if date_str not in daily_data:
                daily_data[date_str] = {
                    "date": date_str,
                    "temperatures": [],
                    "humidity": [],
                    "rainfall": [],
                    "wind_speed": [],
                    "weather_conditions": [],
                    "pressure": []
                }
            
            daily_data[date_str]["temperatures"].append(item["main"]["temp"])
            daily_data[date_str]["humidity"].append(item["main"]["humidity"])
            daily_data[date_str]["rainfall"].append(item.get("rain", {}).get("3h", 0))
            daily_data[date_str]["wind_speed"].append(item["wind"]["speed"])
            daily_data[date_str]["weather_conditions"].append(item["weather"][0]["main"])
            daily_data[date_str]["pressure"].append(item["main"]["pressure"])
        
        # Aggregate daily data
        for date_str, day_data in daily_data.items():
            forecasts.append({
                "date": date_str,
                "temperature_min": min(day_data["temperatures"]),
                "temperature_max": max(day_data["temperatures"]),
                "temperature_avg": sum(day_data["temperatures"]) / len(day_data["temperatures"]),
                "humidity_avg": sum(day_data["humidity"]) / len(day_data["humidity"]),
                "humidity_max": max(day_data["humidity"]),
                "total_rainfall": sum(day_data["rainfall"]),
                "wind_speed_avg": sum(day_data["wind_speed"]) / len(day_data["wind_speed"]),
                "wind_speed_max": max(day_data["wind_speed"]),
                "pressure_avg": sum(day_data["pressure"]) / len(day_data["pressure"]),
                "dominant_weather": max(set(day_data["weather_conditions"]), 
                                      key=day_data["weather_conditions"].count)
            })
        
        forecast_data = {
            "location": {
                "name": data["city"]["name"],
                "country": data["city"]["country"],
                "coordinates": {"lat": lat, "lon": lon}
            },
            "forecast": sorted(forecasts, key=lambda x: x["date"])[:days]
        }
        
        # Cache the data
        self.cache[cache_key] = (forecast_data, time.time())
        logger.info(f"Fetched and cached forecast data for {lat}, {lon}")
        
        return forecast_data
    
    async def get_historical_rainfall(self, lat: float, lon: float, days_back: int = 7) -> float:
        """
        Get historical rainfall data for the past N days.
        Note: This is a simplified implementation. For production, you might want to use
        the OpenWeatherMap Historical Weather API (requires subscription).
        """
        # For now, we'll estimate based on current conditions
        # In production, you would use the historical weather API
        current_weather = await self.get_current_weather(lat, lon)
        
        # Simple estimation based on current rainfall and weather conditions
        current_rain = current_weather["current"]["rainfall_3h"]
        weather_condition = current_weather["current"]["weather_condition"]
        
        # Rough estimation - in production, use actual historical data
        if weather_condition in ["Rain", "Thunderstorm"]:
            estimated_rainfall = current_rain * 2.5  # Assume recent rainy period
        elif weather_condition in ["Clouds"]:
            estimated_rainfall = current_rain * 1.5  # Some recent moisture
        else:
            estimated_rainfall = current_rain * 0.5  # Mostly dry
        
        return min(estimated_rainfall, 100)  # Cap at 100mm for estimation

# Global weather service instance
weather_service = WeatherService()
