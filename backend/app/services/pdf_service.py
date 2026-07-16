from app.models.pdf_document import PDFDocument
from app.models.pdf_chunk import PDFChunk
from app.utils.text_chunker import chunk_pages
from app.services.cloudinary_service import delete_pdf_from_cloudinary
from pathlib import Path

from app.services.embedding_service import create_embedding, cosine_similarity, rerank_chunks

def save_pdf_document(db, conversation_id: int, filename: str, content: list, cloudinary_url: str, cloudinary_public_id: str):
    pdf = PDFDocument(conversation_id=conversation_id, filename=filename, content=content, cloudinary_url=cloudinary_url, cloudinary_public_id=cloudinary_public_id)
    db.add(pdf)
    db.commit()
    db.refresh(pdf)
    return pdf

def get_conversation_pdfs(db, conversation_id: int):
    return (db.query(PDFDocument).filter(PDFDocument.conversation_id == conversation_id).all())

def save_pdf_chunks(db, pdf, chunks):
    print(len(chunks))
    if chunks:
        
        print("========== BEFORE DB ==========")
        print(chunks[0]["text"])
        
        print("Creating embeddings...")
        texts = [chunk["text"] for chunk in chunks]
        embeddings = create_embedding(texts)
        print("Embeddings done.")
        db_chunks = []
        for index, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            db_chunks.append(PDFChunk(
                pdf_id=pdf.id,
                conversation_id=pdf.conversation_id,
                page=chunk["page"],
                chunk_index=index,
                text=chunk["text"],
                embedding=embedding.tolist()
            ))
            
    print("Before Bulk insert")
    db.bulk_save_objects(db_chunks)
    print("Before commit")
    db.commit()
    print("After commit")

def retrieve_relevant_chunks(db, conversation_id, query):
    
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

def delete_pdf_service(db, pdf_id: int):

    pdf =  db.query(PDFDocument).filter(
        PDFDocument.id == pdf_id
    ).first()
    
    if not pdf:
        return None
    
    db.query(PDFChunk).filter(
        PDFChunk.pdf_id == pdf_id
    ).delete(synchronize_session=False)
    
    delete_pdf_from_cloudinary(pdf.cloudinary_public_id)

    db.delete(pdf)

    db.commit()
    return True
    
    