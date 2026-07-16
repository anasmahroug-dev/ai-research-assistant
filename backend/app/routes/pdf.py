from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.database.deps import get_db
from app.services.cloudinary_service import upload_file
from app.services.pdf_service import save_pdf_document, save_pdf_chunks, delete_pdf_service
from app.utils.text_chunker import chunk_pages
from app.services.conversation_service import get_conversation
from app.models.pdf_document import PDFDocument
from fastapi import Form

import tempfile
import os

from app.utils.pdf_parser import extract_pages_from_pdf


router = APIRouter()

@router.post("/upload")
async def upload_pdf(
    conversation_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    temp_path = None

    try:
        pdf_bytes = await file.read()

        with tempfile.NamedTemporaryFile(
            suffix=".pdf",
            delete=False,
        ) as temp_file:
            temp_file.write(pdf_bytes)
            temp_path = temp_file.name

        pages = extract_pages_from_pdf(pdf_bytes)

        cloudinary_file = upload_file(temp_path)

        conversation = get_conversation(db, conversation_id)
        if not conversation:
            return {
                "error": "Conversation not found"
            }

        pdf = save_pdf_document(
            db,
            conversation_id,
            file.filename,
            pages,
            cloudinary_file["url"],
            cloudinary_file["public_id"],
        )

        chunks = chunk_pages(pages)
        save_pdf_chunks(db, pdf, chunks)

        return {
            "filename": file.filename,
            "text_preview": pages[0]["text"][:1000],
        }

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
            
            
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