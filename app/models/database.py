from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Session(Base):
    __tablename__ = "sessions"
    id = Column(String, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    messages = relationship("Message", back_populates="session")

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("sessions.id"))
    role = Column(String)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    session = relationship("Session", back_populates="messages")

class AlertEvent(Base):
    __tablename__ = "alerts"
    id = Column(String, primary_key=True, index=True)
    alert_id = Column(String, index=True)
    severity = Column(String)
    service = Column(String)
    title = Column(String)
    description = Column(Text)
    labels = Column(Text)
    fired_at = Column(DateTime)
    source = Column(String)
    status = Column(String, default="pending")
    analysis_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class AnalysisRecord(Base):
    __tablename__ = "analyses"
    id = Column(String, primary_key=True, index=True)
    alert_id = Column(String, ForeignKey("alerts.id"))
    session_id = Column(String, ForeignKey("sessions.id"))
    content = Column(Text)
    confidence = Column(String)
    confidence_score = Column(Float)
    sources = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    feedback_status = Column(String, default="pending")

class Feedback(Base):
    __tablename__ = "feedbacks"
    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(String, ForeignKey("analyses.id"))
    correct = Column(Boolean)
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class KnowledgeEntry(Base):
    __tablename__ = "knowledge"
    id = Column(String, primary_key=True, index=True)
    title = Column(String)
    content = Column(Text)
    type = Column(String)
    source = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
