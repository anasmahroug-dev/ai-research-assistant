from app.models.pdf_document import PDFDocument
from app.utils.text_chunker import chunk_text

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


def retrieve_relevant_chunks(pdfs, query):
    relevant_chunks = []
    
    query_words = query.lower().split()
    
    for pdf in pdfs:
        chunks = chunk_text(pdf.content)
        
        for chunk in chunks:
            
            chunk_lower = chunk.lower()
            
            if any(word in chunk_lower for word in query_words):
                relevant_chunks.append(chunk)
    
    return relevant_chunks

def build_rag_context(chunks):

    context = ""

    for chunk in chunks:

        context += chunk + "\n\n"

    return context