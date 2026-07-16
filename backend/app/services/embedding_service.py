from sentence_transformers import SentenceTransformer, CrossEncoder
import numpy as np
from numpy import dot
from numpy.linalg import norm

model = SentenceTransformer('all-MiniLM-L6-v2')
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def create_embedding(texts):
    
    return model.encode(texts,
                        batch_size=32,
                        convert_to_numpy=True,
                        normalize_embeddings=True,
                        show_progress_bar=False)


def cosine_similarity(query_embedding, chunk_embeddings):
    query_embedding = np.asarray(query_embedding)
    chunk_embeddings = np.asarray(chunk_embeddings)

    query_embedding /= np.linalg.norm(query_embedding)

    chunk_embeddings /= np.linalg.norm(
        chunk_embeddings,
        axis=1,
        keepdims=True,
    )

    return chunk_embeddings @ query_embedding

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