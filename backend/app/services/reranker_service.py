from sentence_transformers import CrossEncoder

reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def rerank_chunks(query, chunks):
    pairs = [(query, chunk["text"])
             for chunk in chunks]
    
    scores = reranker.predict(pairs, batch_size=16)
    
    for chunk, score in zip(chunks, scores):
        chunk["rerank_score"] = float(score)
        
    reranked = sorted(
        chunks, 
        key=lambda x: x["rerank_score"],
        reverse=True
    )
    
    return reranked

