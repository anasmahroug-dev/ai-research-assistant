from app.models.pdf_document import PDFDocument
from app.models.pdf_chunk import PDFChunk
from app.utils.text_chunker import chunk_pages

from app.services.embedding_service import create_embedding, cosine_similarity, rerank_chunks

def save_pdf_document(db, conversation_id: int, filename: str, content: list):
    pdf = PDFDocument(conversation_id=conversation_id, filename=filename, content=content)
    db.add(pdf)
    db.commit()
    db.refresh(pdf)
    return pdf

def get_conversation_pdfs(db, conversation_id: int):
    return (db.query(PDFDocument).filter(PDFDocument.conversation_id == conversation_id).all())

def save_pdf_chunks(db, pdf, chunks):
    for index, chunk in enumerate(chunks):
        embedding = create_embedding(chunk["text"]).tolist()
        db_chunk = PDFChunk(
            pdf_id=pdf.id,
            page=chunk["page"],
            chunk_index=index,
            text=chunk["text"],
            embedding=embedding
        )
        
        db.add(db_chunk)
    db.commit()

def retrieve_relevant_chunks(db, conversation_id, query):
    
    query_embedding = create_embedding(query)
    pdfs = get_conversation_pdfs(db, conversation_id)
    
    scored_chunks = []
    
    for pdf in pdfs:
        chunks = (db.query(PDFChunk).filter(PDFChunk.pdf_id == pdf.id).all())
        
        for chunk in chunks:
     
            score = cosine_similarity(query_embedding, chunk.embedding)
            
            scored_chunks.append({
                
                "score": score, 
                "text": chunk.text,
                "page": chunk.page,
                "filename": pdf.filename,
                "chunk_id": chunk.id,
                })
            
    
    semantic_chunks = sorted(scored_chunks, key=lambda x: x["score"], reverse=True)[:20]
    reranked_chunks = rerank_chunks(query, semantic_chunks)
    
    top_chunks = reranked_chunks[:5]
    
    return top_chunks

def build_rag_context(chunks):

    context = ""

    for chunk in chunks:

        context += f"""
        
        [DOCUMENT]
        File: {chunk["filename"]}
        Page: {chunk["page"]}
        Chunk ID: {chunk["chunk_id"]}

        {chunk["text"]}

        [/DOCUMENT]
        """

    return context