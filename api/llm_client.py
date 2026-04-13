import os
import logging
import requests
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger("LLMClient")

class LLMClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LLMClient, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            logger.error("GEMINI_API_KEY missing in .env")
            raise ValueError("GEMINI_API_KEY not found")
        
        self.model_name = "gemini-1.5-flash"

    def generate_response(self, prompt: str, system_context: str = "") -> str:
        url = f"https://generativelanguage.googleapis.com/v1/models/{self.model_name}:generateContent?key={self.api_key}"
        
        headers = {'Content-Type': 'application/json'}
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": f"{system_context}\n\n{prompt}"
                }]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 1024,
            }
        }
        
        try:
            res = requests.post(url, headers=headers, json=payload, timeout=15)
            
            if res.status_code == 404:
                logger.warning("gemini-1.5-flash not found, trying gemini-pro...")
                return self._fallback_request(prompt, system_context)
                
            res.raise_for_status()
            res_json = res.json()
            
            if 'candidates' in res_json and len(res_json['candidates']) > 0:
                return res_json['candidates'][0]['content']['parts'][0]['text']
            else:
                return "AI returned empty response. Check safety filters."

        except Exception as e:
            logger.error(f"LLM Error: {e}")
            return f"Connection Error: {str(e)}"

    def _fallback_request(self, prompt, system_context):
        """Emergency fallback using the older stable Pro model."""
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={self.api_key}"
        payload = {
            "contents": [{"parts": [{"text": f"{system_context}\n\n{prompt}"}]}]
        }
        try:
            res = requests.post(url, json=payload, timeout=10)
            if res.status_code == 200:
                return res.json()['candidates'][0]['content']['parts'][0]['text']
            return f"API Error {res.status_code}: Model not found in your region."
        except:
            return "AI Service Unavailable."