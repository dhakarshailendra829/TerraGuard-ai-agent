import requests
import logging
from typing import Dict

# Set up logging for the client
logger = logging.getLogger("WeatherClient")

class WeatherClient:
    
    def __init__(self):
        self.base_url = "https://api.open-meteo.com/v1/forecast"

    def fetch_weather(self, location_data: Dict) -> dict:
        
        lat = location_data.get("lat")
        lon = location_data.get("lon")
        loc_name = location_data.get("name", "Unknown Location")

        if lat is None or lon is None:
            logger.error(f"Missing coordinates for {loc_name}")
            return self._fallback()

        params = {
            "latitude": lat,
            "longitude": lon,
            "current_weather": True,
            "hourly": "temperature_2m,precipitation,windspeed_10m",
            "timezone": "auto",
            "forecast_days": 1
        }

        try:
            response = requests.get(self.base_url, params=params, timeout=8)
            response.raise_for_status()
            data = response.json()
            
            logger.info(f"Weather synced for {loc_name}")
            return self._parse_weather(data)

        except requests.exceptions.RequestException as e:
            logger.error(f"Weather Fetch Failed for {loc_name}: {e}")
            return self._fallback()

    def _parse_weather(self, data: dict) -> dict:
        current = data.get("current_weather", {})
        hourly = data.get("hourly", {})

        precip_list = hourly.get("precipitation", [0.0])
        current_precip = precip_list[0] if precip_list else 0.0

        return {
            "temp": float(current.get("temperature", 0.0)),
            "wind": float(current.get("windspeed", 0.0)),
            "prec": float(current_precip)
        }

    def _fallback(self) -> dict:
        return {
            "temp": 25.0, 
            "wind": 5.0, 
            "prec": 0.0
        }