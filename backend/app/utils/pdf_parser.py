import fitz
def extract_pages_from_pdf(pdf_path: str):
    doc = fitz.open(pdf_path)
    
    pages = []

    for index, page in enumerate(doc):
        text = page.get_text()
        if index == 0:
            print("========== AFTER EXTRACT ==========")
            print(text) 
        
        
        pages.append({"page": index + 1, "text": text})
        
    print("========== EXTRACTED TEXT ==========")
    print(repr(pages[0]["text"][:500]))
    
    return pages