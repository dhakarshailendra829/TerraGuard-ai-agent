import time
import os
import logging
import json
from datetime import datetime
from api.weather_client import WeatherClient
from agent.threat_scorer import ThreatScorer
from agent.rag_retriever import RAGRetriever
from agent.plan_generator import PlanGenerator
from agent.alert_dispatcher import AlertDispatcher

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("LEWRS")

class LEWRSAgent:
    def __init__(self):
        self.weather_client = WeatherClient()
        self.scorer = ThreatScorer()
        self.retriever = RAGRetriever()
        self.generator = PlanGenerator()
        self.dispatcher = AlertDispatcher()

        # Configuration for all tracked locations
        self.monitored_locations = [
            {"name": "Abu", "lat": 24.59, "lon": 72.71},
            {"name": "Chennai", "lat": 13.08, "lon": 80.27},
            {"name": "Mumbai", "lat": 19.07, "lon": 72.87}
        ]
        
        self.interval = int(os.getenv("ALERT_INTERVAL_SEC", 300))
        self.ui_path = "ui"

        if not os.path.exists(self.ui_path):
            os.makedirs(self.ui_path)

    def run(self):
        cycle_count = 0
        logger.info(f"LEWRS Global Command Center Active: Monitoring {len(self.monitored_locations)} locations")

        while True:
            cycle_count += 1
            logger.info(f"\n{'='*20} GLOBAL SYNC CYCLE #{cycle_count} {'='*20}")

            for location in self.monitored_locations:
                loc_name = location["name"]
                try:
                    logger.info(f"Processing intelligence for: {loc_name}")
                    
                    # 1. DATA ACQUISITION & ANALYSIS
                    weather = self.weather_client.fetch_weather(location)
                    
                    risk = self.scorer.assess(weather)
                    
                    rag_data = self.retriever.retrieve(weather)
                    
                    # 2. NEURAL STRATEGY GENERATION
                    plan = self.generator.generate(risk, rag_data, loc_name)
                    
                    # 3. UI STATE SYNCHRONIZATION
                    plan_output = {
                        "location": loc_name,
                        "plan": plan,
                        "score": risk.get("score", 0),
                        "level": risk.get("level", "NORMAL"),
                        "timestamp": datetime.now().strftime("%H:%M:%S")
                    }
                    
                    file_path = os.path.join(self.ui_path, f"plan_{loc_name}.json")
                    with open(file_path, "w", encoding="utf-8") as f:
                        json.dump(plan_output, f, indent=4)
                    
                    # 4. EXTERNAL DISPATCH
                    self.dispatcher.dispatch(plan, risk)
                    logger.info(f"Dashboard synchronized for {loc_name} [Risk: {risk['level']} | Score: {risk.get('score')}]")

                except Exception as e:
                    logger.error(f"Cycle failure for {loc_name}: {str(e)}")
            
            logger.info(f"{'='*15} Cycle Complete. Sleeping for {self.interval}s {'='*15}")
            time.sleep(self.interval)
if __name__ == "__main__":
    agent = LEWRSAgent()
    agent.run()