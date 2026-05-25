from app.models.database import Feedback, AnalysisRecord, KnowledgeEntry, get_db
from app.services.rag_engine import add_document
from datetime import datetime
import uuid
from typing import Dict, Any

async def submit_feedback(analysis_id: str, correct: bool, comment: str = None):
    db = next(get_db())
    
    feedback = Feedback(
        analysis_id=analysis_id,
        correct=correct,
        comment=comment
    )
    db.add(feedback)
    
    analysis = db.query(AnalysisRecord).filter(AnalysisRecord.id == analysis_id).first()
    if analysis:
        analysis.feedback_status = "confirmed" if correct else "corrected"
    
    if correct and analysis:
        await add_to_knowledge_base(analysis_id, analysis)
    
    db.commit()
    
    return {'status': 'success', 'message': '反馈已提交'}

async def add_to_knowledge_base(analysis_id: str, analysis: AnalysisRecord):
    try:
        content = analysis.content
        
        metadata = {
            'title': f"分析案例 {analysis_id[:8]}",
            'source': 'auto',
            'confidence': analysis.confidence,
            'confidence_score': analysis.confidence_score
        }
        
        add_document(analysis_id, content, metadata)
        
        db = next(get_db())
        kb_entry = KnowledgeEntry(
            id=analysis_id,
            title=metadata['title'],
            content=content,
            type='analysis',
            source='auto'
        )
        db.add(kb_entry)
        db.commit()
    except Exception:
        pass

def get_feedback_stats():
    db = next(get_db())
    
    total = db.query(Feedback).count()
    correct = db.query(Feedback).filter(Feedback.correct == True).count()
    
    if total == 0:
        return {'total': 0, 'correct': 0, 'correct_rate': 0.0}
    
    return {
        'total': total,
        'correct': correct,
        'correct_rate': correct / total
    }
