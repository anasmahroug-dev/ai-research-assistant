from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.database.deps import get_db
from app.services.pdf_service import save_pdf_document



import os

from app.utils.pdf_parser import extract_text_from_pdf

router = APIRouter()

@router.post("/upload")

async def upload_pdf(user_id: str,
                    file: UploadFile = File(...),
                     db: Session = Depends(get_db)):
    
    os.makedirs("uploads", exist_ok=True)
    
    file_path = f"uploads/{file.filename}"
    
    with open(file_path, "wb") as f:
        f.write(await file.read())
        
    extracted_text = extract_text_from_pdf(file_path)
    
    save_pdf_document(
    db,
    user_id,
    file.filename,
    extracted_text
    )
    
    return{
        "filename": file.filename,
        "text_preview": extracted_text[:1000]       
    }
