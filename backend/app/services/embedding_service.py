from sentence_transformers import SentenceTransformer
from numpy import dot
from numpy.linalg import norm

model = SentenceTransformer('all-MiniLM-L6-v2')

def create_embedding(text):
    
    return model.encode(text)


def cosine_similarity(a, b):
    return dot(a, b) / (norm(a) * norm(b))