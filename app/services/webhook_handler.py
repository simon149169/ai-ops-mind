import hmac
import hashlib
from datetime import datetime
from typing import Dict, Any
from app.config import settings
from app.services.triage_engine import process_alert
from app.utils.dedup import generate_fingerprint, is_duplicate, store_alert
from app.models.database import AlertEvent as DBAlertEvent, get_db
from sqlalchemy.orm import Session
import uuid

def verify_signature(body: bytes, signature: str) -> bool:
    if not settings.WEBHOOK_SECRET:
        return True
    
    expected = hmac.new(
        settings.WEBHOOK_SECRET.encode(),
        body,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(expected, signature)

async def process_webhook_alert(data: Dict[str, Any], source: str = 'webhook') -> Dict[str, Any]:
    fingerprint = generate_fingerprint(data)
    
    if is_duplicate(fingerprint):
        return {'status': 'duplicated', 'message': '告警已重复'}
    
    alert_id = data.get('alert_id', str(uuid.uuid4()))
    store_alert(alert_id, data.get('service', 'unknown'), data.get('severity', 'P3'))
    
    alert_event = {
        'alert_id': alert_id,
        'severity': data.get('severity', 'P3').upper(),
        'service': data.get('service', data.get('labels', {}).get('service', 'unknown')),
        'title': data.get('title', data.get('alertname', '')),
        'description': data.get('description', ''),
        'labels': data.get('labels', {}),
        'fired_at': data.get('fired_at', datetime.utcnow().isoformat()),
        'source': source
    }
    
    await save_alert(alert_event)
    
    async def process_async():
        await process_alert(alert_event)
    
    import asyncio
    asyncio.create_task(process_async())
    
    return {'status': 'accepted', 'message': '告警已接收并处理'}

async def save_alert(alert: Dict[str, Any]):
    db = next(get_db())
    
    db_alert = DBAlertEvent(
        id=alert['alert_id'],
        alert_id=alert['alert_id'],
        severity=alert['severity'],
        service=alert['service'],
        title=alert['title'],
        description=alert['description'],
        labels=str(alert['labels']),
        fired_at=datetime.fromisoformat(alert['fired_at'].replace('Z', '+00:00')),
        source=alert['source']
    )
    
    db.add(db_alert)
    db.commit()
