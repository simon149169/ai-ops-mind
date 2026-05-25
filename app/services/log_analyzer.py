from app.services.llm_service import chat_completion, build_messages, stream_chat_completion
from app.services.rag_engine import search_similar
from app.services.confidence_scorer import calculate_confidence, analyze_output_entropy
from app.prompts.log_analysis import LOG_ANALYSIS_SYSTEM_PROMPT, LOG_ANALYSIS_USER_PROMPT
from app.utils.log_parser import parse_logs, extract_error_messages, extract_services
from typing import List, Dict, Any, AsyncGenerator

async def analyze_logs(logs: str, context: str = None) -> Dict[str, Any]:
    parsed_logs = parse_logs(logs)
    error_messages = extract_error_messages(parsed_logs)
    services = extract_services(parsed_logs)
    
    query = "\n".join(error_messages[:10]) if error_messages else logs
    
    reference_cases = search_similar(query, top_k=3)
    
    if reference_cases:
        reference_text = "\n".join([f"- [{r['id']}] {r['title']}" for r in reference_cases])
        similarity_scores = [1 - r['similarity'] for r in reference_cases]
    else:
        reference_text = "无"
        similarity_scores = []
    
    system_prompt = LOG_ANALYSIS_SYSTEM_PROMPT.format(
        reference_cases=reference_text,
        log_content=logs
    )
    
    user_prompt = LOG_ANALYSIS_USER_PROMPT.format(logs=logs)
    
    messages = build_messages(system_prompt, user_prompt)
    result = await chat_completion(messages)
    
    output_entropy = analyze_output_entropy(result)
    confidence, confidence_score = calculate_confidence(similarity_scores, output_entropy)
    
    return {
        'content': result,
        'confidence': confidence,
        'confidence_score': confidence_score,
        'sources': reference_cases,
        'services': services,
        'error_count': len(error_messages)
    }

async def stream_analyze_logs(logs: str, context: str = None) -> AsyncGenerator[Dict[str, Any], None]:
    parsed_logs = parse_logs(logs)
    query = "\n".join(extract_error_messages(parsed_logs)[:10])
    
    reference_cases = search_similar(query, top_k=3)
    
    if reference_cases:
        reference_text = "\n".join([f"- [{r['id']}] {r['title']}" for r in reference_cases])
    else:
        reference_text = "无"
    
    system_prompt = LOG_ANALYSIS_SYSTEM_PROMPT.format(
        reference_cases=reference_text,
        log_content=logs
    )
    
    user_prompt = LOG_ANALYSIS_USER_PROMPT.format(logs=logs)
    
    messages = build_messages(system_prompt, user_prompt)
    
    full_content = ""
    async for chunk in stream_chat_completion(messages):
        full_content += chunk
        yield {'type': 'token', 'content': chunk}
    
    output_entropy = analyze_output_entropy(full_content)
    similarity_scores = [1 - r['similarity'] for r in reference_cases] if reference_cases else []
    confidence, confidence_score = calculate_confidence(similarity_scores, output_entropy)
    
    yield {
        'type': 'metadata',
        'sources': reference_cases,
        'confidence': confidence,
        'confidence_score': confidence_score
    }
    
    yield {
        'type': 'done',
        'content': full_content
    }
