from app.models.pdf_document import PDFDocument
from app.utils.text_chunker import chunk_text
from app.services.embedding_service import create_embedding, cosine_similarity

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
    
    
    query_embedding = create_embedding(query)
    scored_chunks = []
    
     
    for pdf in pdfs:
        chunks = chunk_text(pdf.content)
        
        for chunk in chunks:
            
            
            chunk_embedding = create_embedding(chunk)
            score = cosine_similarity(query_embedding, chunk_embedding)
            
            scored_chunks.append((score, chunk))
    scored_chunks.sort(key=lambda x: x[0], reverse=True)
    
    top_chunks = [chunk for score, chunk in scored_chunks[:5]]
    
            
    return top_chunks

def build_rag_context(chunks):

    context = ""

    for chunk in chunks:

        context += chunk + "\n\n"

    return context