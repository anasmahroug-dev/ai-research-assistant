def chunk_pages(pages, chunk_size=1200, overlap=200):
    chunks = []
    for page_data in pages:
        page_number = page_data["page"]
        text = page_data["text"]
        start = 0
        while start < len(text):
            end = min(start + chunk_size, len(text))
            
            if end < len(text):
                while end <len(text) and not text[end].isspace():
                    end+= 1
            
            chunks.append({
                "text": text[start:end],
                "page": page_number
            })
            
            if end >= len(text):
                break
            
            start = max(end - overlap, 0)
            
            while start > 0 and not text[start -1].isspace():
                start -= 1
        
    
    return chunks

        