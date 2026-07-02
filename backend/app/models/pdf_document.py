from sqlalchemy import Column, Integer, String, Text, JSON
from app.database.database import Base


class PDFDocument(Base):
    __tablename__ = "pdf_documents"
    
    id = Column(Integer, primary_key=True, index=True)
    
    conversation_id = Column(Integer, index=True)
    
    filename = Column(String)
    
    content = Column(JSON)
    