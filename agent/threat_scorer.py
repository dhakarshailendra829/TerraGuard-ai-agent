from typing import Dict

class ThreatScorer:
    def __init__(self):
        
        # Using a list sorted by threshold (highest first) for easier logic
        
        self.weights = {
            "temp": [{"threshold": 45, "score": 40}, {"threshold": 40, "score": 25}, {"threshold": 38, "score": 12}],
            "wind": [{"threshold": 60, "score": 30}, {"threshold": 40, "score": 15}],
            "prec": [{"threshold": 50, "score": 35}, {"threshold": 20, "score": 20}]
        }

    def assess(self, data: Dict) -> Dict:
        total_score = 0
        breakdown = {}

        for param, rules in self.weights.items():
            value = data.get(param, 0.0)
            score = self._score_param(value, rules)
            breakdown[param] = {"value": value, "score": score}
            total_score += score

        total_score = min(total_score, 100)
        return {
            "score": total_score,
            "level": self._get_level(total_score),
            "breakdown": breakdown
        }

    def _score_param(self, value: float, rules: list) -> int:
        for rule in rules:
            if value >= rule["threshold"]: # Using >= for edge cases
                return rule["score"]
        return 0

    def _get_level(self, score: int) -> str:
        if score >= 70: return "SEVERE"
        if score >= 40: return "WARNING"
        if score >= 15: return "ELEVATED" 
        return "NORMAL"