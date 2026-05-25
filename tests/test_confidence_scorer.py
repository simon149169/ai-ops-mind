import pytest
from app.services.confidence_scorer import calculate_confidence, analyze_output_entropy, evaluate_sources

def test_calculate_confidence_high():
    similarity_scores = [0.95, 0.92, 0.88]
    confidence, score = calculate_confidence(similarity_scores)
    assert confidence == "高"
    assert score > 0.8

def test_calculate_confidence_medium():
    similarity_scores = [0.7, 0.65]
    confidence, score = calculate_confidence(similarity_scores)
    assert confidence == "中"
    assert 0.6 <= score < 0.8

def test_calculate_confidence_low():
    similarity_scores = [0.4, 0.35]
    confidence, score = calculate_confidence(similarity_scores)
    assert confidence == "低"
    assert score < 0.6

def test_analyze_output_entropy():
    text = "可能存在问题，也许需要进一步检查"
    entropy = analyze_output_entropy(text)
    assert entropy > 0.5

def test_evaluate_sources():
    sources = [
        {'id': 'case1', 'title': 'Test', 'similarity': 0.9},
        {'id': 'case2', 'title': 'Test2', 'similarity': 0.4}
    ]
    valid_sources, avg_score = evaluate_sources(sources)
    assert len(valid_sources) == 1
    assert valid_sources[0]['id'] == 'case1'
