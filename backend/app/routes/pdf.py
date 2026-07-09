from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.database.deps import get_db
from app.services.pdf_service import save_pdf_document, save_pdf_chunks, delete_pdf_service
from app.utils.text_chunker import chunk_pages
from app.services.conversation_service import get_conversation
from app.models.pdf_document import PDFDocument
from fastapi import Form
from app.utils.config import UPLOAD_DIR



import os

from app.utils.pdf_parser import extract_pages_from_pdf

router = APIRouter()

@router.post("/upload")

async def upload_pdf(conversation_id: int = Form(...),
                    file: UploadFile = File(...),
                     db: Session = Depends(get_db)):
    
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    file_path = f"{UPLOAD_DIR}/{file.filename}"
    
    with open(file_path, "wb") as f:
        f.write(await file.read())
        
    pages = extract_pages_from_pdf(file_path)

    conversation = get_conversation(db, conversation_id)
    if not conversation:
        return {
            "error": "Conversation not found"
        }
    pdf = save_pdf_document(
    db,
    conversation_id,
    file.filename,
    pages
    )
    chunks = chunk_pages(pages)
    save_pdf_chunks(db, pdf, chunks)
    
    return{
        "filename": file.filename,
        "text_preview": pages[1]["text"][:1000]       
    }


@router.get("/{conversation_id}")
def get_pdfs(
    conversation_id: int,
    db: Session = Depends(get_db)
):

    pdfs = db.query(PDFDocument).filter(
        PDFDocument.conversation_id == conversation_id
    ).all()

    return pdfs

@router.delete("/{pdf_id}")
def delete_pdf(
    pdf_id: int,
    db: Session = Depends(get_db)
):
    success = delete_pdf_service(db, pdf_id)
    if not success:
        return {"error": "PDF not found"}
    
    return {
        "message": "PDF deleted"
    }