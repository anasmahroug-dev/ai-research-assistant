from sqlalchemy import Column, Integer, String, Text
from app.database.database import Base


class PDFDocument(Base):
    __tablename__ = "pdf_documents"
    
    id = Column(Integer, primary_key=True, index=True)
    
    user_id = Column(String)
    
    filename = Column(String)
    
    content = Column(Text)
    