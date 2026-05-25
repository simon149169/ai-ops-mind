from fastapi import APIRouter, HTTPException, Request
from app.services.webhook_handler import verify_signature, process_webhook_alert
import json

router = APIRouter()

@router.post("/alert")
async def webhook_alert(request: Request):
    signature = request.headers.get("X-Webhook-Signature", "")
    body = await request.body()
    
    if not verify_signature(body, signature):
        raise HTTPException(status_code=403, detail="签名验证失败")
    
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="无效的JSON格式")
    
    result = await process_webhook_alert(data, source='webhook')
    
    if result['status'] == 'duplicated':
        return {'status': 'duplicated', 'message': '告警已重复'}
    
    return {'status': 'accepted', 'message': '告警已接收并处理'}
