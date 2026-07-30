from app.models.pdf_chunk import PDFChunk
from app.services.embedding_service import create_embedding, cosine_similarity
from app.services.pdf_service import get_conversation_pdfs



def retrieve_semantic_chunks(db, conversation_id, query):
    
    query_embedding = create_embedding(query)
    pdfs = get_conversation_pdfs(db, conversation_id)
    
    scored_chunks = []
    
    for pdf in pdfs:
        chunks = (db.query(PDFChunk).filter(PDFChunk.pdf_id == pdf.id).all())
        if not chunks:
            continue
        embeddings = [chunk.embedding for chunk in chunks]
        
        scores = cosine_similarity(query_embedding, embeddings)
        
        for chunk, score  in zip(chunks, scores):
     
            scored_chunks.append({
                
                "score": float(score), 
                "text": chunk.text,
                "page": chunk.page,
                "filename": pdf.filename,
                "chunk_id": chunk.id,
                })
            
    
    semantic_chunks = sorted(scored_chunks, key=lambda x: x["score"], reverse=True)[:10]
    
    return semantic_chunks