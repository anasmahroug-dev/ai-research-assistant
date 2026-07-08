from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.models.message import Message
from app.models.pdf_document import PDFDocument
from datetime import datetime, timezone  


from app.database.database import Base

class Conversation(Base):
   
    __tablename__ = "conversations"
    
    __table_args__ = {
    "sqlite_autoincrement": True
    }
    
    id = Column(Integer, primary_key=True, index=True)
   
    user_id = Column(String)
   
    title = Column(String)
    
    updated_at = Column(DateTime, default =lambda:datetime.now(timezone.utc))
    
    messages = relationship(
        "Message",
        back_populates="conversation",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    pdfs = relationship(
        "PDFDocument",
        back_populates="conversation",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    
    
    
    