from fastapi import APIRouter
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from fastapi.responses import PlainTextResponse

router = APIRouter()

ops_llm_requests_total = Counter('ops_llm_requests_total', 'LLM调用总次数', ['model', 'endpoint'])
ops_llm_latency_seconds = Histogram('ops_llm_latency_seconds', 'LLM调用耗时分布')
ops_llm_tokens_total = Counter('ops_llm_tokens_total', 'Token用量', ['type'])
ops_rag_hit_rate = Gauge('ops_rag_hit_rate', 'RAG命中率')
ops_rag_top1_similarity = Histogram('ops_rag_top1_similarity', 'RAG最高相似度分布')
ops_webhook_received_total = Counter('ops_webhook_received_total', 'Webhook接收数量', ['severity', 'source'])
ops_webhook_dedup_total = Counter('ops_webhook_dedup_total', '去重丢弃数量')
ops_analysis_confidence = Histogram('ops_analysis_confidence', '分析置信度分布')
ops_feedback_correct_rate = Gauge('ops_feedback_correct_rate', '专家确认正确率')
ops_prompt_version = Gauge('ops_prompt_version', '当前Prompt模板版本号', ['prompt_name'])

@router.get("/")
async def metrics():
    return PlainTextResponse(generate_latest().decode('utf-8'), media_type='text/plain')
