from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database.database import Base

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    
    conversation_id = Column(Integer, 
                             ForeignKey("conversations.id", 
                            ondelete="CASCADE"), 
                             nullable=False, 
                             index=True, )
    conversation = relationship(
        "Conversation",
        back_populates="messages"
    )
    
    role = Column(String)
    
    content = Column(String)
    
    created_at = Column(DateTime, default=lambda:datetime.now(timezone.utc))