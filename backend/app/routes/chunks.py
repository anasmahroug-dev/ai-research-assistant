from fastapi import APIRouter, Depends, HTTPException
from app.database.deps import get_db
from app.models.pdf_chunk import PDFChunk
from app.models.pdf_document import PDFDocument
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/{chunk_id}")
def get_chunk(chunk_id: int, db: Session = Depends(get_db)):
    chunk = (db.query(PDFChunk).join(PDFDocument)
             .filter(PDFChunk.id == chunk_id)
             .first())
    
    if not chunk:
        raise HTTPException(404)
    
    
    return {
        "id": chunk.id,
        "text": chunk.text,
        "page": chunk.page,
        "pdf_id": chunk.pdf.id,
        "cloudinary_url": chunk.pdf.cloudinary_url,
        
    }