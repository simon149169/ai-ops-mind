from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.models.schemas import AnalyzeRequest
from app.services.log_analyzer import analyze_logs, stream_analyze_logs
import json
import uuid

router = APIRouter()

@router.post("/")
async def analyze(request: AnalyzeRequest):
    if not request.logs:
        raise HTTPException(status_code=400, detail="日志内容不能为空")
    
    result = await analyze_logs(request.logs, request.context)
    result['analysis_id'] = str(uuid.uuid4())
    
    return result

@router.post("/stream")
async def analyze_stream(request: AnalyzeRequest):
    if not request.logs:
        raise HTTPException(status_code=400, detail="日志内容不能为空")
    
    analysis_id = str(uuid.uuid4())
    
    async def generate():
        async for part in stream_analyze_logs(request.logs, request.context):
            if part['type'] == 'token':
                yield f'data: {json.dumps({"event": "token", "data": {"content": part["content"]}})}\n\n'
            elif part['type'] == 'metadata':
                yield f'data: {json.dumps({"event": "metadata", "data": {"sources": part["sources"], "confidence": part["confidence"], "confidence_score": part["confidence_score"]}})}\n\n'
            elif part['type'] == 'done':
                yield f'data: {json.dumps({"event": "done", "data": {"analysis_id": analysis_id, "content": part["content"]}})}\n\n'
    
    return StreamingResponse(generate(), media_type="text/event-stream")
