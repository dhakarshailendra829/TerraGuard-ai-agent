import json
import os
from api.llm_client import LLMClient

class PlanGenerator:
    def __init__(self):
        self.llm = LLMClient()
        # Load contacts into memory
        contacts_path = os.path.join("data", "contacts.json")
        with open(contacts_path, "r") as f:
            self.contacts_db = json.load(f)

    def generate(self, risk_data, rag_data, location_name):
        system_context = "You are a disaster management expert. Use specific local details."
        prompt = self._build_prompt(risk_data, rag_data, location_name)
        raw_plan = self.llm.generate_response(prompt, system_context)
        
        return self._inject_contacts(raw_plan, location_name)

    def _inject_contacts(self, plan_text, location):
        city_data = self.contacts_db.get(location, {})
        
        # Simple replacement logic for placeholders
        plan_text = plan_text.replace("[Local Police Station Number]", city_data.get("police", "100"))
        plan_text = plan_text.replace("[Local Hospital Number]", city_data.get("hospital", "102"))
        plan_text = plan_text.replace("[Electricity Department Contact Number]", city_data.get("electricity", "1912"))
        return plan_text

    def _build_prompt(self, risk_data, rag_data, location_name):
        return f"""
        Generate a professional Emergency Action Plan for {location_name}.
        Status: {risk_data['level']} (Score: {risk_data['score']})
        
        Use this format:
        ## 1. Immediate Actions
        ## 2. Resources
        ## 3. Contact Info
        """