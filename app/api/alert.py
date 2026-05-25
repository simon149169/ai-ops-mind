from fastapi import APIRouter, HTTPException
from app.models.schemas import AlertDiagnoseRequest
from app.services.alert_diagnoser import diagnose_alerts
import uuid

router = APIRouter()

@router.post("/")
async def diagnose_alert(request: AlertDiagnoseRequest):
    if not request.alerts:
        raise HTTPException(status_code=400, detail="告警列表不能为空")
    
    result = await diagnose_alerts(request.alerts, request.timerange)
    result['analysis_id'] = str(uuid.uuid4())
    
    return result
