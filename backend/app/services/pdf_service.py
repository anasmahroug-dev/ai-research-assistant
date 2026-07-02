from app.models.pdf_document import PDFDocument
from app.utils.text_chunker import chunk_pages
from app.services.embedding_service import create_embedding, cosine_similarity

def save_pdf_document(db, conversation_id: int, filename: str, content: list):
    pdf = PDFDocument(conversation_id=conversation_id, filename=filename, content=content)
    db.add(pdf)
    db.commit()
    db.refresh(pdf)
    return pdf

def get_conversation_pdfs(db, conversation_id: int):
    return (db.query(PDFDocument).filter(PDFDocument.conversation_id == conversation_id).all())



def retrieve_relevant_chunks(pdfs, query):
    
    query_embedding = create_embedding(query)
    scored_chunks = []
    
    for pdf in pdfs:
        chunks = chunk_pages(pdf.content)
        
        for chunk in chunks:
            
            
            chunk_embedding = create_embedding(chunk["text"])
            score = cosine_similarity(query_embedding, chunk_embedding)
            
            scored_chunks.append({
                
                "score": score, 
                "text": chunk["text"],
                "page": chunk["page"],
                "filename": pdf.filename})
            
    
    top_chunks = sorted(scored_chunks, key=lambda x: x["score"], reverse=True)[:10]
    
    print("\nTOP CHUNKS:\n")
    
    for chunk in top_chunks:

        print(f"PAGE: {chunk['page']} | SCORE: {chunk['score']}")

        print(chunk["text"][:300])

        print("\n-----------------\n")



            
    return top_chunks

def build_rag_context(chunks):

    context = ""

    for chunk in chunks:

        context += f"""
        
        [DOCUMENT]
        File: {chunk["filename"]}
        Page: {chunk["page"]}

        {chunk["text"]}

        [/DOCUMENT]
        """

    return context