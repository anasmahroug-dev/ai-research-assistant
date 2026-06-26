from app.models.pdf_document import PDFDocument

def save_pdf_document(db, user_id: str, filename: str, content: str):
    pdf = PDFDocument( user_id=user_id, filename=filename, content=content)
    db.add(pdf)
    db.commit()
    db.refresh(pdf)
    return pdf

def get_user_pdfs(db, user_id: str):
    return (db.query(PDFDocument).filter(PDFDocument.user_id == user_id).all())

def build_pdf_context(pdfs):
    context = ""
    
    for pdf in pdfs:
        context += f"\nPDF: {pdf.filename}\n"
        
        context += pdf.content[:3000]
        
        context += "\n\n"
        
    return context