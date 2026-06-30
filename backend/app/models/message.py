from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone
from app.database.database import Base

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    
    conversation_id = Column(Integer, index=True)
    
    role = Column(String)
    
    content = Column(String)
    
    created_at = Column(DateTime, default=lambda:datetime.now(timezone.utc))