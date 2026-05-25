from datetime import datetime
from app.services.llm_service import chat_completion, build_messages
from app.services.rag_engine import search_similar
from app.services.confidence_scorer import calculate_confidence, analyze_output_entropy
from app.prompts.rca_report import RCA_REPORT_PROMPT
from app.utils.report_formatter import format_rca_report
from typing import List, Dict, Any

async def generate_rca(incident: str, logs: str = None) -> Dict[str, Any]:
    query = f"{incident} {logs[:200] if logs else ''}"
    reference_cases = search_similar(query, top_k=3)
    
    prompt = RCA_REPORT_PROMPT.format(
        incident=incident,
        logs=logs or "无",
        analysis_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )
    
    messages = build_messages("", prompt)
    result = await chat_completion(messages)
    
    output_entropy = analyze_output_entropy(result)
    similarity_scores = [1 - r['similarity'] for r in reference_cases] if reference_cases else []
    confidence, confidence_score = calculate_confidence(similarity_scores, output_entropy)
    
    timeline = extract_timeline(result)
    
    formatted_report = format_rca_report(incident, result, confidence, reference_cases, timeline)
    
    return {
        'content': formatted_report,
        'raw_content': result,
        'confidence': confidence,
        'confidence_score': confidence_score,
        'sources': reference_cases,
        'timeline': timeline
    }

def extract_timeline(content: str) -> List[Dict[str, str]]:
    timeline = []
    lines = content.split('\n')
    in_timeline = False
    
    for line in lines:
        if '时间线' in line or 'Timeline' in line:
            in_timeline = True
            continue
        
        if in_timeline and (line.startswith('-') or line.startswith('*')):
            parts = line[2:].split(':', 1)
            if len(parts) == 2:
                timeline.append({'time': parts[0].strip(), 'event': parts[1].strip()})
    
    return timeline
