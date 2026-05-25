from app.models.database import Session as DBSession, Message, get_db
from datetime import datetime
import uuid
from typing import List, Dict, Any

def create_session() -> str:
    db = next(get_db())
    
    session_id = str(uuid.uuid4())
    session = DBSession(id=session_id)
    db.add(session)
    db.commit()
    
    return session_id

def add_message(session_id: str, role: str, content: str):
    db = next(get_db())
    
    session = db.query(DBSession).filter(DBSession.id == session_id).first()
    if not session:
        session = DBSession(id=session_id)
        db.add(session)
    
    message = Message(
        session_id=session_id,
        role=role,
        content=content
    )
    db.add(message)
    db.commit()

def get_messages(session_id: str) -> List[Dict[str, Any]]:
    db = next(get_db())
    
    messages = db.query(Message).filter(Message.session_id == session_id).order_by(Message.created_at).all()
    
    return [{
        'role': m.role,
        'content': m.content,
        'created_at': m.created_at.isoformat()
    } for m in messages]

def get_sessions() -> List[Dict[str, Any]]:
    db = next(get_db())
    
    sessions = db.query(DBSession).order_by(DBSession.created_at.desc()).all()
    
    return [{
        'id': s.id,
        'created_at': s.created_at.isoformat()
    } for s in sessions]

def delete_session(session_id: str):
    db = next(get_db())
    
    db.query(Message).filter(Message.session_id == session_id).delete()
    db.query(DBSession).filter(DBSession.id == session_id).delete()
    db.commit()
