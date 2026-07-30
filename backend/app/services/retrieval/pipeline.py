from app.services.retrieval.semantic import retrieve_semantic_chunks
from app.services.reranker_service import rerank_chunks

def retrieve_chunks(db, conversation_id, query):
    semantic_chunks = retrieve_semantic_chunks(db, conversation_id, query)
    reranked_chunks = rerank_chunks(query, semantic_chunks)
    
    return reranked_chunks[:5]
    