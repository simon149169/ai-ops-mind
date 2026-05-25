import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Any
from app.services.log_analyzer import analyze_logs
from app.services.alert_diagnoser import diagnose_alerts
from app.services.rca_generator import generate_rca
from app.services.notifier import send_notification
from app.models.database import AlertEvent as DBAlertEvent, AnalysisRecord, get_db
from sqlalchemy.orm import Session
import uuid

pending_alerts = {}

async def process_alert(alert: Dict[str, Any]):
    severity = alert.get('severity', 'P3').upper()
    service = alert.get('service', 'unknown')
    alert_id = alert.get('alert_id', str(uuid.uuid4()))
    
    if severity == 'P0':
        await handle_p0_alert(alert)
    elif severity == 'P1':
        await handle_p1_alert(alert)
    else:
        await handle_low_priority_alert(alert)

async def handle_p0_alert(alert: Dict[str, Any]):
    alert_id = alert.get('alert_id', str(uuid.uuid4()))
    
    result = await generate_rca(alert.get('title', 'Unknown Incident'), alert.get('description', ''))
    
    await save_analysis(alert_id, result)
    await send_notification(alert, result)

async def handle_p1_alert(alert: Dict[str, Any]):
    service = alert.get('service', 'unknown')
    
    if service not in pending_alerts:
        pending_alerts[service] = []
    
    pending_alerts[service].append(alert)
    
    if len(pending_alerts[service]) >= 3:
        await analyze_aggregated_alerts(service)
    else:
        await asyncio.sleep(120)
        if service in pending_alerts and pending_alerts[service]:
            await analyze_aggregated_alerts(service)

async def handle_low_priority_alert(alert: Dict[str, Any]):
    pass

async def analyze_aggregated_alerts(service: str):
    alerts = pending_alerts.pop(service, [])
    
    if alerts:
        result = await diagnose_alerts(alerts)
        
        for alert in alerts:
            await save_analysis(alert.get('alert_id'), result)
        
        await send_notification(alerts[0], result)

async def save_analysis(alert_id: str, result: Dict[str, Any]):
    db = next(get_db())
    
    analysis_record = AnalysisRecord(
        id=str(uuid.uuid4()),
        alert_id=alert_id,
        content=result.get('content', ''),
        confidence=result.get('confidence', '中'),
        confidence_score=result.get('confidence_score', 0.6),
        sources=str(result.get('sources', []))
    )
    
    db.add(analysis_record)
    db.commit()
