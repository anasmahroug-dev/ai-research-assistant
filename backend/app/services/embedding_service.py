from sentence_transformers import SentenceTransformer, CrossEncoder

from numpy import dot
from numpy.linalg import norm

model = SentenceTransformer('all-MiniLM-L6-v2')
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def create_embedding(text):
    
    return model.encode(text)


def cosine_similarity(a, b):
    return dot(a, b) / (norm(a) * norm(b))

def rerank_chunks(query, chunks):
    pairs = [(query, chunk["text"])
             for chunk in chunks]
    
    scores = reranker.predict(pairs)
    
    for chunk, score in zip(chunks, scores):
        chunk["rerank_score"] = float(score)
        
    reranked = sorted(
        chunks, 
        key=lambda x: x["rerank_score"],
        reverse=True
    )
    
    return reranked