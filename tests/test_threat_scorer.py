from agent.threat_scorer import ThreatScorer

def test_severe_conditions():
    scorer = ThreatScorer()
    data = {"temp": 46, "wind": 65, "prec": 55}
    result = scorer.assess(data)
    
    assert result["level"] == "SEVERE"
    assert result["score"] == 100

def test_elevated_conditions():
    scorer = ThreatScorer()
    data = {"temp": 39, "wind": 45, "prec": 0}
    result = scorer.assess(data)
    
    assert result["level"] == "ELEVATED"
    assert result["score"] == 27

def test_normal_conditions():
    scorer = ThreatScorer()
    data = {"temp": 30, "wind": 10, "prec": 0}
    result = scorer.assess(data)
    
    assert result["level"] == "NORMAL"
    assert result["score"] == 0