from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Dict, Any

class AlertEvent(BaseModel):
    alert_id: str
    severity: str = Field(description="P0 / P1 / P2 / P3")
    service: str
    title: str
    description: str
    labels: Dict[str, Any] = {}
    fired_at: datetime
    source: str = Field(description="prometheus / dingtalk / grafana / manual")

class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None

class AnalyzeRequest(BaseModel):
    logs: str
    context: Optional[str] = None

class AlertDiagnoseRequest(BaseModel):
    alerts: List[Dict[str, Any]]
    timerange: Optional[str] = None

class RCARequest(BaseModel):
    incident: str
    logs: Optional[str] = None

class FeedbackRequest(BaseModel):
    analysis_id: str
    correct: bool
    comment: Optional[str] = None

class AnalysisResult(BaseModel):
    content: str
    confidence: str
    confidence_score: float
    sources: List[Dict[str, Any]]
    analysis_id: str

class SourceInfo(BaseModel):
    id: str
    title: str
    similarity: float

class SSEToken(BaseModel):
    content: str

class SSEMetadata(BaseModel):
    sources: List[SourceInfo]
    confidence: str
    confidence_score: float

class SSEDone(BaseModel):
    analysis_id: str
    session_id: str
    total_tokens: int
