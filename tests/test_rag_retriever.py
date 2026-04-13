from agent.rag_retriever import RAGRetriever

def test_priority_retrieval():
    retriever = RAGRetriever()
    weather = {"temp": 45, "wind": 10, "prec": 60}
    result = retriever.retrieve(weather)

    assert result["risk_type"] == "heatwave"
    assert "Stay indoors" in result["protocol"][0]

def test_normal_retrieval():
    retriever = RAGRetriever()
    weather = {"temp": 25, "wind": 10, "prec": 0}
    result = retriever.retrieve(weather)

    assert result["risk_type"] == "normal"
    assert len(result["protocol"]) > 0