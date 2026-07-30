from rank_bm25 import BM25Okapi
from app.models.pdf_chunk import PDFChunk
from app.services.pdf_service import get_conversation_pdfs

def tokenize(text: str):
    return text.lower().split()


def retrieve_lexical_chunks(db, conversation_id, query):
    
    pdfs = get_conversation_pdfs(db,conversation_id)

    all_chunks = []

    for pdf in pdfs:
        chunks = (
            db.query(PDFChunk)
            .filter(PDFChunk.pdf_id == pdf.id)
            .all()
        )

        for chunk in chunks:
            all_chunks.append({
                "chunk": chunk,
                "filename": pdf.filename,
            })
    if not all_chunks:
        return []
            
    corpus = [
        tokenize(item["chunk"].text)
        for item in all_chunks
    ]
    
    bm25 = BM25Okapi(corpus)
    
    query_tokens = tokenize(query)
    
    scores = bm25.get_scores(query_tokens)
    
    scored_chunks = []

    for item, score in zip(all_chunks, scores):

        chunk = item["chunk"]

        scored_chunks.append({
            "score": float(score),
            "text": chunk.text,
            "page": chunk.page,
            "filename": item["filename"],
            "chunk_id": chunk.id,
        })
        
    top_chunks = sorted(
        scored_chunks,
        key=lambda x: x["score"],
        reverse=True,
    )[:10]
    
    print("\n========== BM25 ==========")

    for chunk in top_chunks:
        print(
            f"{chunk['score']:.2f} | "
            f"{chunk['filename']} | "
            f"page {chunk['page']}"
        )
        print(chunk["text"][:150])
        print()
            
    return top_chunks
