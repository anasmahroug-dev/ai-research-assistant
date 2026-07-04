from sqlalchemy import Column, Integer, Text, ForeignKey, JSON
from app.database.database import Base

class PDFChunk(Base):
    __tablename__ = "pdf_chunks"
    
    id = Column(Integer, primary_key=True, index=True)
    
    pdf_id = Column(Integer, ForeignKey("pdf_documents.id"), index=True)
    
    page = Column(Integer)
    
    chunk_index = Column(Integer)
    
    text = Column(Text)
    
    embedding = Column(JSON)
    