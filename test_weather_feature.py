#!/usr/bin/env python3
"""
Simple test script to verify the weather-based disease risk assessment feature.
This script tests the weather API endpoints and disease risk calculations.
"""

import asyncio
import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.weather import weather_service
from backend.app.disease_risk import disease_risk_assessor

async def test_weather_feature():
    """Test the weather feature with sample coordinates."""
    
    print("🌦️ Testing Weather-Based Disease Risk Assessment Feature")
    print("=" * 60)
    
    # Test coordinates for major Indian cities
    test_locations = [
        {"name": "Mumbai, Maharashtra", "lat": 19.0760, "lon": 72.8777},
        {"name": "Pune, Maharashtra", "lat": 18.5204, "lon": 73.8567},
        {"name": "Bangalore, Karnataka", "lat": 12.9716, "lon": 77.5946},
        {"name": "Chennai, Tamil Nadu", "lat": 13.0827, "lon": 80.2707},
        {"name": "Lucknow, Uttar Pradesh", "lat": 26.8467, "lon": 80.9462}
    ]
    
    for location in test_locations:
        print(f"\n📍 Testing location: {location['name']}")
        print("-" * 40)
        
        try:
            # Test weather data fetching
            print("Fetching weather data...")
            weather_data = await weather_service.get_current_weather(
                location['lat'], location['lon']
            )
            
            if weather_data:
                current = weather_data['current']
                print(f"✅ Weather data retrieved successfully")
                print(f"   Temperature: {current['temperature']:.1f}°C")
                print(f"   Humidity: {current['humidity']}%")
                print(f"   Conditions: {current['weather_description']}")
                print(f"   Wind Speed: {current['wind_speed']} m/s")
                print(f"   Rainfall (3h): {current['rainfall_3h']} mm")
                
                # Test disease risk assessment
                print("\nCalculating disease risk...")
                risk_assessment = disease_risk_assessor.calculate_combined_risk(weather_data)
                
                print(f"✅ Risk assessment completed")
                print(f"   Overall Risk: {risk_assessment['overall_risk']['risk_level'].upper()}")
                print(f"   Overall Score: {risk_assessment['overall_risk']['risk_score']:.1f}%")
                print(f"   Dead Heart Risk: {risk_assessment['deadheart']['risk_level'].upper()} ({risk_assessment['deadheart']['risk_score']:.1f}%)")
                print(f"   Tiller Risk: {risk_assessment['tiller']['risk_level'].upper()} ({risk_assessment['tiller']['risk_score']:.1f}%)")
                
                # Show top recommendations
                if risk_assessment['combined_recommendations']:
                    print(f"\n💡 Top Recommendations:")
                    for i, rec in enumerate(risk_assessment['combined_recommendations'][:3], 1):
                        print(f"   {i}. {rec}")
                
            else:
                print("❌ Failed to retrieve weather data")
                
        except Exception as e:
            print(f"❌ Error testing {location['name']}: {str(e)}")
            
        print()
    
    print("=" * 60)
    print("🎉 Weather feature test completed!")
    print("\nTo use the weather feature:")
    print("1. Make sure your OpenWeatherMap API key is set in .env file")
    print("2. Start the backend server: uvicorn backend.app.main:app --reload")
    print("3. Start the frontend: cd frontend && npm run dev")
    print("4. Open http://localhost:5173 and select your location")
    print("5. View real-time weather and disease risk assessment")

if __name__ == "__main__":
    # Set the API key for testing
    os.environ["OPENWEATHER_API_KEY"] = "1ea3a842272c34af40b89cb5daf9ad59"
    
    print("🔑 Using provided OpenWeatherMap API key")
    print("🌍 Testing with real weather data from OpenWeatherMap")
    
    # Run the test
    asyncio.run(test_weather_feature())
