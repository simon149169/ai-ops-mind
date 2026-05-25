from app.services.llm_service import chat_completion, build_messages
from app.services.rag_engine import search_similar
from app.services.confidence_scorer import calculate_confidence, analyze_output_entropy
from app.prompts.alert_diagnosis import ALERT_DIAGNOSIS_PROMPT
from typing import List, Dict, Any

async def diagnose_alerts(alerts: List[Dict[str, Any]], timerange: str = None) -> Dict[str, Any]:
    if not alerts:
        return {
            'content': '没有提供告警信息',
            'confidence': '低',
            'confidence_score': 0.3,
            'sources': []
        }
    
    service = alerts[0].get('service', 'unknown')
    
    alert_descriptions = []
    for i, alert in enumerate(alerts):
        severity = alert.get('severity', 'unknown')
        title = alert.get('title', alert.get('alertname', ''))
        description = alert.get('description', '')
        alert_descriptions.append(f"{i+1}. [{severity}] {title}: {description}")
    
    alert_text = "\n".join(alert_descriptions)
    
    query = f"{service} {alert_text[:200]}"
    reference_cases = search_similar(query, top_k=3)
    
    prompt = ALERT_DIAGNOSIS_PROMPT.format(
        service=service,
        time_window=timerange or "未知",
        alert_count=len(alerts),
        alerts=alert_text
    )
    
    messages = build_messages("", prompt)
    result = await chat_completion(messages)
    
    output_entropy = analyze_output_entropy(result)
    similarity_scores = [1 - r['similarity'] for r in reference_cases] if reference_cases else []
    confidence, confidence_score = calculate_confidence(similarity_scores, output_entropy)
    
    return {
        'content': result,
        'confidence': confidence,
        'confidence_score': confidence_score,
        'sources': reference_cases,
        'service': service,
        'alert_count': len(alerts)
    }
