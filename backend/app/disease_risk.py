"""
MIT License

Disease risk assessment module for sugarcane diseases based on weather conditions.
Implements risk calculation algorithms for Dead Heart and Tiller diseases.
"""

import logging
from typing import Dict, List, Tuple
from enum import Enum
from datetime import datetime

logger = logging.getLogger(__name__)

class RiskLevel(Enum):
    """Risk level enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class DiseaseRiskAssessment:
    """Disease risk assessment based on weather conditions."""
    
    def __init__(self):
        # Risk thresholds and weights
        self.risk_thresholds = {
            "low": 25,
            "medium": 50,
            "high": 75,
            "critical": 90
        }
    
    def _classify_risk_level(self, risk_score: float) -> RiskLevel:
        """Classify risk score into risk level."""
        if risk_score >= self.risk_thresholds["critical"]:
            return RiskLevel.CRITICAL
        elif risk_score >= self.risk_thresholds["high"]:
            return RiskLevel.HIGH
        elif risk_score >= self.risk_thresholds["medium"]:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW
    
    def _get_risk_color(self, risk_level: RiskLevel) -> str:
        """Get color code for risk level."""
        color_map = {
            RiskLevel.LOW: "#4CAF50",      # Green
            RiskLevel.MEDIUM: "#FF9800",   # Orange
            RiskLevel.HIGH: "#FF5722",     # Red-Orange
            RiskLevel.CRITICAL: "#F44336"  # Red
        }
        return color_map[risk_level]
    
    def calculate_deadheart_risk(self, weather_data: Dict) -> Dict:
        """
        Calculate Dead Heart disease risk based on weather conditions.
        
        Risk Factors:
        - High humidity (>80%) + Temperature 25-30°C = High Risk
        - Recent rainfall + stagnant water = Very High Risk
        - Dry conditions for 7+ days = Low Risk
        """
        current = weather_data["current"]
        
        temperature = current["temperature"]
        humidity = current["humidity"]
        rainfall_3h = current["rainfall_3h"]
        wind_speed = current["wind_speed"]
        weather_condition = current["weather_condition"]
        
        risk_score = 0
        risk_factors = []
        recommendations = []
        
        # Temperature factor (optimal range for disease: 25-30°C)
        if 25 <= temperature <= 30:
            risk_score += 30
            risk_factors.append(f"Optimal temperature for disease development ({temperature:.1f}°C)")
        elif 20 <= temperature <= 35:
            risk_score += 15
            risk_factors.append(f"Moderate temperature risk ({temperature:.1f}°C)")
        
        # Humidity factor (high risk: >80%)
        if humidity > 80:
            risk_score += 25
            risk_factors.append(f"High humidity level ({humidity}%)")
            recommendations.append("Monitor plants closely for early symptoms")
        elif humidity > 70:
            risk_score += 10
            risk_factors.append(f"Moderate humidity level ({humidity}%)")
        
        # Rainfall factor (recent rain increases risk)
        if rainfall_3h > 5:
            risk_score += 20
            risk_factors.append(f"Recent significant rainfall ({rainfall_3h:.1f}mm)")
            recommendations.append("Check for waterlogged areas and improve drainage")
        elif rainfall_3h > 0:
            risk_score += 10
            risk_factors.append(f"Recent light rainfall ({rainfall_3h:.1f}mm)")
        
        # Wind factor (low wind increases stagnant conditions)
        if wind_speed < 2:
            risk_score += 15
            risk_factors.append(f"Low wind speed ({wind_speed:.1f} m/s) - stagnant conditions")
        elif wind_speed < 5:
            risk_score += 5
            risk_factors.append(f"Moderate wind speed ({wind_speed:.1f} m/s)")
        
        # Weather condition factor
        if weather_condition in ["Rain", "Thunderstorm"]:
            risk_score += 15
            risk_factors.append(f"Wet weather conditions ({weather_condition})")
            recommendations.append("Avoid field activities until conditions improve")
        elif weather_condition in ["Drizzle", "Mist"]:
            risk_score += 10
            risk_factors.append(f"Moist weather conditions ({weather_condition})")
        
        # Combined high-risk conditions
        if humidity > 80 and 25 <= temperature <= 30:
            risk_score += 20  # Bonus for combined optimal conditions
            risk_factors.append("Critical combination: High humidity + optimal temperature")
            recommendations.append("Apply preventive fungicide spray immediately")
        
        if rainfall_3h > 5 and wind_speed < 2:
            risk_score += 15  # Bonus for stagnant water conditions
            risk_factors.append("Critical combination: Recent rain + low wind (stagnant water)")
            recommendations.append("Improve field drainage urgently")
        
        # Dry conditions reduce risk
        if humidity < 60 and rainfall_3h == 0 and weather_condition in ["Clear", "Sunny"]:
            risk_score = max(0, risk_score - 20)
            risk_factors.append("Dry conditions reduce disease risk")
            recommendations.append("Good conditions for field activities")
        
        risk_level = self._classify_risk_level(risk_score)
        
        # Add level-specific recommendations
        if risk_level == RiskLevel.CRITICAL:
            recommendations.extend([
                "URGENT: Apply fungicide treatment immediately",
                "Inspect all plants for early symptoms",
                "Improve drainage in waterlogged areas"
            ])
        elif risk_level == RiskLevel.HIGH:
            recommendations.extend([
                "Apply preventive fungicide spray",
                "Monitor plants daily for symptoms",
                "Ensure proper field drainage"
            ])
        elif risk_level == RiskLevel.MEDIUM:
            recommendations.extend([
                "Increase monitoring frequency",
                "Prepare fungicide for application if needed",
                "Check drainage systems"
            ])
        else:  # LOW
            recommendations.extend([
                "Continue regular monitoring",
                "Good time for field maintenance activities"
            ])
        
        return {
            "disease": "deadheart",
            "risk_level": risk_level.value,
            "risk_score": min(100, max(0, risk_score)),
            "risk_color": self._get_risk_color(risk_level),
            "risk_factors": risk_factors,
            "recommendations": recommendations,
            "assessment_time": datetime.now().isoformat()
        }
    
    def calculate_tiller_risk(self, weather_data: Dict) -> Dict:
        """
        Calculate Tiller disease risk based on weather conditions.
        
        Risk Factors:
        - High humidity (>85%) + Temperature 28-35°C = High Risk
        - Continuous moisture + poor drainage = Very High Risk
        - Strong winds + rain = Medium Risk
        """
        current = weather_data["current"]
        
        temperature = current["temperature"]
        humidity = current["humidity"]
        rainfall_3h = current["rainfall_3h"]
        wind_speed = current["wind_speed"]
        weather_condition = current["weather_condition"]
        
        risk_score = 0
        risk_factors = []
        recommendations = []
        
        # Temperature factor (optimal range for disease: 28-35°C)
        if 28 <= temperature <= 35:
            risk_score += 30
            risk_factors.append(f"Optimal temperature for disease development ({temperature:.1f}°C)")
        elif 25 <= temperature <= 38:
            risk_score += 15
            risk_factors.append(f"Moderate temperature risk ({temperature:.1f}°C)")
        
        # Humidity factor (high risk: >85%)
        if humidity > 85:
            risk_score += 30
            risk_factors.append(f"Very high humidity level ({humidity}%)")
            recommendations.append("Critical humidity - monitor plants hourly")
        elif humidity > 75:
            risk_score += 15
            risk_factors.append(f"High humidity level ({humidity}%)")
            recommendations.append("Increase plant monitoring frequency")
        
        # Rainfall factor (continuous moisture increases risk)
        if rainfall_3h > 10:
            risk_score += 25
            risk_factors.append(f"Heavy rainfall ({rainfall_3h:.1f}mm)")
            recommendations.append("Check for waterlogged areas immediately")
        elif rainfall_3h > 2:
            risk_score += 15
            risk_factors.append(f"Moderate rainfall ({rainfall_3h:.1f}mm)")
        
        # Wind and rain combination (medium risk)
        if wind_speed > 10 and rainfall_3h > 0:
            risk_score += 15
            risk_factors.append(f"Strong winds ({wind_speed:.1f} m/s) with rain - disease spread risk")
            recommendations.append("Monitor for wind-blown disease spread")
        elif wind_speed > 15:
            risk_score += 10
            risk_factors.append(f"Strong winds ({wind_speed:.1f} m/s) may spread disease")
        
        # Weather condition factor
        if weather_condition in ["Thunderstorm"]:
            risk_score += 20
            risk_factors.append(f"Severe weather conditions ({weather_condition})")
            recommendations.append("Expect increased disease pressure after storm")
        elif weather_condition in ["Rain", "Drizzle"]:
            risk_score += 15
            risk_factors.append(f"Wet weather conditions ({weather_condition})")
        
        # Combined high-risk conditions
        if humidity > 85 and 28 <= temperature <= 35:
            risk_score += 25  # Bonus for combined optimal conditions
            risk_factors.append("Critical combination: Very high humidity + optimal temperature")
            recommendations.append("Apply systemic fungicide immediately")
        
        if rainfall_3h > 5 and humidity > 80:
            risk_score += 20  # Bonus for continuous moisture
            risk_factors.append("Critical combination: Heavy rain + high humidity (continuous moisture)")
            recommendations.append("Improve drainage and air circulation")
        
        # Dry conditions reduce risk
        if humidity < 70 and rainfall_3h == 0:
            risk_score = max(0, risk_score - 15)
            risk_factors.append("Dry conditions reduce disease risk")
            recommendations.append("Favorable conditions for plant health")
        
        risk_level = self._classify_risk_level(risk_score)
        
        # Add level-specific recommendations
        if risk_level == RiskLevel.CRITICAL:
            recommendations.extend([
                "EMERGENCY: Apply systemic fungicide now",
                "Inspect all tillers for symptoms",
                "Implement emergency drainage measures",
                "Consider copper-based treatments"
            ])
        elif risk_level == RiskLevel.HIGH:
            recommendations.extend([
                "Apply preventive fungicide to tillers",
                "Monitor tiller development closely",
                "Improve field ventilation",
                "Check drainage systems"
            ])
        elif risk_level == RiskLevel.MEDIUM:
            recommendations.extend([
                "Increase tiller monitoring",
                "Prepare treatment materials",
                "Monitor weather forecasts closely"
            ])
        else:  # LOW
            recommendations.extend([
                "Continue routine monitoring",
                "Good conditions for tiller development"
            ])
        
        return {
            "disease": "tiller",
            "risk_level": risk_level.value,
            "risk_score": min(100, max(0, risk_score)),
            "risk_color": self._get_risk_color(risk_level),
            "risk_factors": risk_factors,
            "recommendations": recommendations,
            "assessment_time": datetime.now().isoformat()
        }
    
    def calculate_combined_risk(self, weather_data: Dict) -> Dict:
        """Calculate combined risk assessment for both diseases."""
        deadheart_risk = self.calculate_deadheart_risk(weather_data)
        tiller_risk = self.calculate_tiller_risk(weather_data)
        
        # Determine overall risk level
        max_score = max(deadheart_risk["risk_score"], tiller_risk["risk_score"])
        overall_risk_level = self._classify_risk_level(max_score)
        
        # Combine recommendations
        all_recommendations = []
        if deadheart_risk["risk_level"] in ["high", "critical"]:
            all_recommendations.extend([f"Dead Heart: {rec}" for rec in deadheart_risk["recommendations"][:3]])
        if tiller_risk["risk_level"] in ["high", "critical"]:
            all_recommendations.extend([f"Tiller: {rec}" for rec in tiller_risk["recommendations"][:3]])
        
        # Add general recommendations
        if overall_risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
            all_recommendations.append("Consider consulting agricultural extension officer")
            all_recommendations.append("Document symptoms with photos for expert review")
        
        return {
            "overall_risk": {
                "risk_level": overall_risk_level.value,
                "risk_score": max_score,
                "risk_color": self._get_risk_color(overall_risk_level)
            },
            "deadheart": deadheart_risk,
            "tiller": tiller_risk,
            "combined_recommendations": all_recommendations[:8],  # Limit to top 8
            "assessment_time": datetime.now().isoformat(),
            "weather_summary": {
                "temperature": weather_data["current"]["temperature"],
                "humidity": weather_data["current"]["humidity"],
                "rainfall": weather_data["current"]["rainfall_3h"],
                "conditions": weather_data["current"]["weather_description"]
            }
        }

# Global disease risk assessment instance
disease_risk_assessor = DiseaseRiskAssessment()
