from fastapi import APIRouter, HTTPException
from app.models.schemas import FeedbackRequest
from app.services.feedback_service import submit_feedback, get_feedback_stats

router = APIRouter()

@router.post("/")
async def submit(request: FeedbackRequest):
    if not request.analysis_id:
        raise HTTPException(status_code=400, detail="分析ID不能为空")
    
    result = await submit_feedback(request.analysis_id, request.correct, request.comment)
    return result

@router.get("/stats")
async def stats():
    return get_feedback_stats()
