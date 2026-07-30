from app.services.retrieval.semantic import retrieve_semantic_chunks
from app.services.retrieval.lexical import retrieve_lexical_chunks
from app.services.retrieval.fusion import reciprocal_rank_fusion
from app.services.reranker_service import rerank_chunks

def retrieve_chunks(db, conversation_id, query):
    semantic_chunks = retrieve_semantic_chunks(
        db, 
        conversation_id, 
        query)
    lexical_chunks = retrieve_lexical_chunks(
        db,
        conversation_id,
        query,
    )
    fused_chunks = reciprocal_rank_fusion(
        semantic_chunks,
        lexical_chunks,
    )
    print(semantic_chunks)
    print(lexical_chunks)
    
    reranked_chunks = rerank_chunks(query, fused_chunks)
    
    return reranked_chunks[:5]
    