from sqlalchemy import Column, Integer, String, Text, JSON, ForeignKey
from app.database.database import Base
from sqlalchemy.orm import relationship
from app.enums.pdf_status import PdfStatus


class PDFDocument(Base):
    __tablename__ = "pdf_documents"
    
    id = Column(Integer, primary_key=True, index=True)
    
    conversation_id = Column(Integer,
                             ForeignKey("conversations.id", 
                                        ondelete="CASCADE"), 
                             nullable=False, 
                             index=True, )
    
    conversation = relationship(
        "Conversation",
        back_populates="pdfs"
    )
    
    chunks = relationship(
        "PDFChunk",
        back_populates="pdf",
        cascade="all, delete-orphan"
    )
    
    
    filename = Column(String)
    
    content = Column(JSON)
    
    cloudinary_url = Column(Text)

    cloudinary_public_id = Column(Text)
    
    status = Column(
        String,
        nullable=False,
        default=PdfStatus.PROCESSING
    )
    
    