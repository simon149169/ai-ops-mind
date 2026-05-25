from typing import List, Dict, Any

def calculate_confidence(similarity_scores: List[float], output_entropy: float = 0.0) -> tuple:
    if not similarity_scores:
        return "中", 0.6
    
    avg_similarity = sum(similarity_scores) / len(similarity_scores)
    max_similarity = max(similarity_scores)
    
    base_score = (avg_similarity * 0.6 + max_similarity * 0.4)
    
    adjusted_score = max(0.3, min(0.98, base_score - output_entropy * 0.1))
    
    if adjusted_score >= 0.8:
        confidence = "高"
    elif adjusted_score >= 0.6:
        confidence = "中"
    else:
        confidence = "低"
    
    return confidence, adjusted_score

def analyze_output_entropy(text: str) -> float:
    if not text:
        return 0.5
    
    words = text.split()
    unique_words = set(words)
    vocabulary_diversity = len(unique_words) / max(1, len(words))
    
    if "可能" in text or "也许" in text or "不确定" in text:
        vocabulary_diversity += 0.2
    
    return min(1.0, vocabulary_diversity)

def evaluate_sources(sources: List[Dict[str, Any]]) -> tuple:
    if not sources:
        return [], 0.0
    
    valid_sources = []
    scores = []
    
    for source in sources:
        similarity = source.get('similarity', 0.0)
        if similarity >= 0.5:
            valid_sources.append(source)
            scores.append(similarity)
    
    avg_score = sum(scores) / len(scores) if scores else 0.0
    
    return valid_sources, avg_score
