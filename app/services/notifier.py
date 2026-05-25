import httpx
from app.config import settings
from typing import Dict, Any

async def send_notification(alert: Dict[str, Any], analysis: Dict[str, Any] = None):
    title = alert.get('title', '告警通知')
    service = alert.get('service', 'unknown')
    severity = alert.get('severity', 'P3')
    
    if severity in ['P0', 'P1']:
        if settings.DINGTALK_WEBHOOK_URL:
            await send_dingtalk(title, service, severity, analysis)
        
        if settings.FEISHU_WEBHOOK_URL:
            await send_feishu(title, service, severity, analysis)

async def send_dingtalk(title: str, service: str, severity: str, analysis: Dict[str, Any] = None):
    try:
        content = f"【{severity}告警】{title}\n服务: {service}"
        if analysis:
            content += f"\n置信度: {analysis.get('confidence', '中')}"
            content += f"\n分析摘要: {analysis.get('content', '')[:100]}..."
        
        payload = {
            "msgtype": "text",
            "text": {"content": content}
        }
        
        async with httpx.AsyncClient() as client:
            await client.post(settings.DINGTALK_WEBHOOK_URL, json=payload)
    except Exception:
        pass

async def send_feishu(title: str, service: str, severity: str, analysis: Dict[str, Any] = None):
    try:
        content = f"【{severity}告警】{title}\n服务: {service}"
        if analysis:
            content += f"\n置信度: {analysis.get('confidence', '中')}"
        
        payload = {
            "msg_type": "text",
            "content": {"text": content}
        }
        
        async with httpx.AsyncClient() as client:
            await client.post(settings.FEISHU_WEBHOOK_URL, json=payload)
    except Exception:
        pass
