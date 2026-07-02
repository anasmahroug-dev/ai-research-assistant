def chunk_pages(pages, chunk_size=1000):
    chunks = []
    for page_data in pages:
        page_number = page_data["page"]
        text = page_data["text"]
        
        for i in range(0, len(text), chunk_size):
            chunk_text = text[i:i + chunk_size]
            
            chunks.append({
                "text": chunk_text,
                "page": page_number
            })
    
    return chunks

        