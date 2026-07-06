from fastapi import APIRouter, Depends
from app.database.deps import get_db
from app.models.pdf_chunk import PDFChunk
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/{chunk_id}")
def get_chunk(chunk_id: int, db: Session = Depends(get_db)):
    chunk = (db.query(PDFChunk).filter(PDFChunk.id == chunk_id)
             .first())
    return {
        "id": chunk.id,
        "text": chunk.text,
        "page": chunk.page
        
    }