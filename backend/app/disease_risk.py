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

    def _approx_esb_deadheart(self, weather_data: Dict, forecast_data: Dict) -> Dict:
        """
        Approximate ESB (Dead Heart) risk using OpenWeather free data:
        - Uses current + 3-hour forecast aggregated to daily.
        - Proxies 'last N days' with upcoming daily forecast and current rain.
        - Adds '(approx)' to reasons where proxy is used.
        """
        from statistics import mean

        current = weather_data.get("current", {})
        forecasts = (forecast_data or {}).get("forecast", [])

        # Helper getters with safe defaults
        def today_forecast():
            today_iso = datetime.now().date().isoformat()
            for d in forecasts:
                if d.get("date") == today_iso:
                    return d
            # fallback to first forecast day
            return forecasts[0] if forecasts else {}

        def next_n_days(n: int):
            return forecasts[:n] if forecasts else []

        td = today_forecast()

        # Extract fields with fallbacks
        min_temp_today = td.get("temperature_min", current.get("temperature", 0.0))
        max_temp_today = td.get("temperature_max", current.get("temperature", 0.0))
        eve_rh_today = td.get("evening_rh", current.get("humidity", 0))  # proxy
        morn_rh_today = td.get("morning_rh", current.get("humidity", 0))  # proxy
        rain_1h_now = current.get("rainfall_1h", 0.0)
        rain_3h_now = current.get("rainfall_3h", 0.0)
        total_rain_today = td.get("total_rainfall", 0.0)

        # Proxies for rainfall windows (approx, due to free plan limits)
        next3 = next_n_days(3)
        next7 = next_n_days(7)

        # Approximate "no significant rain in last 3 days"
        # Proxy: minimal current rain and very low rain expected today
        no_sig_rain_last3_proxy = (rain_1h_now == 0.0) and (total_rain_today <= 1.0)

        # Approximate "no rain in last 24h"
        # Proxy: current rain is 0 and today total is ~0
        no_rain_24h_proxy = (rain_1h_now == 0.0) and (total_rain_today == 0.0)

        # Approximate "consecutive dry days >= 4" (future outlook)
        consecutive_dry = 0
        for d in next7:
            if (d.get("total_rainfall", 0.0) < 2.0):
                consecutive_dry += 1
            else:
                break

        # Avg temp over next dry window (or next 4 if available)
        eval_days = next7[:max(4, consecutive_dry)] if next7 else []
        avg_temp_future = mean([d.get("temperature_avg", 0.0) for d in eval_days]) if eval_days else td.get("temperature_avg", current.get("temperature", 0.0))

        # Approx "prior rainfall week < 5mm" → future week outlook
        prior_week_rain_proxy = sum([d.get("total_rainfall", 0.0) for d in next7]) < 5.0

        # Temp above normal proxy: today > mean of next 7 days
        mean_7_future = mean([d.get("temperature_avg", 0.0) for d in next7]) if next7 else td.get("temperature_avg", current.get("temperature", 0.0))
        temp_above_normal_proxy = (td.get("temperature_avg", current.get("temperature", 0.0)) > mean_7_future)

        # Disrupters: heavy rain ≥50mm any day in next 7 or high RH day (>80%) in next 7
        heavy_rain_any_next7 = any(d.get("total_rainfall", 0.0) >= 50.0 for d in next7)
        rh80_any_next7 = any(d.get("humidity_max", 0.0) > 80.0 for d in next7)

        reasons = []
        risk_level = "low"
        score = 30  # default LOW score

        # Disrupters first: force LOW
        if heavy_rain_any_next7 or rh80_any_next7:
            reasons.append("Monsoon/disrupter: heavy rain ≥50mm or RH>80% expected (approx)")
            risk_level = "low"
            score = 30
        else:
            # High conditions
            high_A = (min_temp_today >= 23.0) and (eve_rh_today <= 60.0) and no_sig_rain_last3_proxy
            high_B = (max_temp_today >= 35.0) and (eve_rh_today <= 60.0) and no_rain_24h_proxy

            # Elevated conditions
            elevated_C = (consecutive_dry >= 4) and (avg_temp_future > 28.0)
            elevated_D = (morn_rh_today <= 50.0) and prior_week_rain_proxy and temp_above_normal_proxy

            if high_A:
                reasons.append("Min temp ≥23°C AND evening RH ≤60% AND ~no rain last 3 days (approx)")
                risk_level = "high"
                score = 90
            elif high_B:
                reasons.append("Max temp ≥35°C AND evening RH ≤60% AND ~no rain last 24h (approx)")
                risk_level = "high"
                score = 88
            elif elevated_C:
                reasons.append("≥4 dry days (<2mm) ahead AND avg temp >28°C (approx)")
                risk_level = "medium"  # treated as ELEVATED → between medium/high
                score = 65
            elif elevated_D:
                reasons.append("Morning RH ≤50% AND week rain <5mm AND temp above normal (approx)")
                risk_level = "medium"
                score = 60
            else:
                reasons.append("No high/elevated ESB conditions (approx) → Low")

        level_enum = RiskLevel.HIGH if risk_level == "high" else (RiskLevel.MEDIUM if risk_level == "medium" else RiskLevel.LOW)

        return {
            "disease": "deadheart",
            "risk_level": level_enum.value,
            "risk_score": score,
            "risk_color": self._get_risk_color(level_enum),
            "risk_factors": reasons,
            "recommendations": [],
            "assessment_time": datetime.now().isoformat(),
            "approx_mode": True
        }

    def calculate_combined_risk_with_forecast(self, weather_data: Dict, forecast_data: Dict) -> Dict:
        """Calculate combined risk using approx_free ESB rules for deadheart plus existing tiller."""
        deadheart_risk = self._approx_esb_deadheart(weather_data, forecast_data)
        tiller_risk = self.calculate_tiller_risk(weather_data)

        max_score = max(deadheart_risk["risk_score"], tiller_risk["risk_score"])
        overall_risk_level = self._classify_risk_level(max_score)

        all_recommendations = []
        if deadheart_risk["risk_level"] in ["high", "critical"]:
            all_recommendations.extend([f"Dead Heart: {rec}" for rec in deadheart_risk.get("recommendations", [])[:3]])
        if tiller_risk["risk_level"] in ["high", "critical"]:
            all_recommendations.extend([f"Tiller: {rec}" for rec in tiller_risk.get("recommendations", [])[:3]])

        return {
            "overall_risk": {
                "risk_level": overall_risk_level.value,
                "risk_score": max_score,
                "risk_color": self._get_risk_color(overall_risk_level)
            },
            "deadheart": deadheart_risk,
            "tiller": tiller_risk,
            "combined_recommendations": all_recommendations[:8],
            "assessment_time": datetime.now().isoformat(),
            "weather_summary": {
                "temperature": weather_data.get("current", {}).get("temperature"),
                "humidity": weather_data.get("current", {}).get("humidity"),
                "rainfall": weather_data.get("current", {}).get("rainfall_3h"),
                "conditions": weather_data.get("current", {}).get("weather_description")
            },
            "approx_mode": True,
            "rule_mode": "approx_free"
        }

# Global disease risk assessment instance
disease_risk_assessor = DiseaseRiskAssessment()
