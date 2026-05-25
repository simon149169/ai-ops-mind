from fastapi import APIRouter, HTTPException
from app.models.schemas import RCARequest
from app.services.rca_generator import generate_rca
import uuid

router = APIRouter()

@router.post("/")
async def generate(request: RCARequest):
    if not request.incident:
        raise HTTPException(status_code=400, detail="事件名称不能为空")
    
    result = await generate_rca(request.incident, request.logs)
    result['analysis_id'] = str(uuid.uuid4())
    
    return result
