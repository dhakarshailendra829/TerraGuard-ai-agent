import json
import os
import logging

class RAGRetriever:
    def __init__(self):
        base_path = os.path.dirname(os.path.dirname(__file__))
        kb_path = os.path.join(base_path, "knowledge_base", "protocols.json")
        
        try:
            with open(kb_path, "r") as f:
                self.protocols = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            
            # Fallback if file is missing
            self.protocols = {"normal": {"protocol": ["Stay informed", "No immediate action required"]}}

    def retrieve(self, weather_data: dict) -> dict:
        temp = weather_data.get("temp", 0)
        prec = weather_data.get("prec", 0)
        wind = weather_data.get("wind", 0)

        # Priority-based matching
        if temp > 40: risk = "heatwave"
        elif prec > 50: risk = "flood"
        elif wind > 60: risk = "storm"
        else: risk = "normal"

        return {
            "risk_type": risk,
            "protocol": self.protocols.get(risk, self.protocols["normal"])["protocol"]
        }