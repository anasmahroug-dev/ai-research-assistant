from collections import defaultdict

RRF_K = 60

def reciprocal_rank_fusion(*ranked_lists, k = RRF_K):
    scores = defaultdict(float)
    chunks= {}
    
    for ranked_list in ranked_lists:
        for rank, chunk in enumerate(ranked_list, start=1):
            
            chunk_id = chunk["chunk_id"]
            
            scores[chunk_id] += 1 / (k + rank)
            
            chunks[chunk_id] = chunk
            
    fused = sorted(
        chunks.values(),
        key=lambda chunk: scores[chunk["chunk_id"]],
        reverse=True,
    )
    for chunk in fused:
        chunk["rrf_score"] = scores[chunk["chunk_id"]]
        print(chunk["rrf_score"], chunk["filename"], chunk["page"])
    
    return fused