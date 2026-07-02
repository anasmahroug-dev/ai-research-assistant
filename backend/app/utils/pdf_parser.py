from pypdf import PdfReader

def extract_pages_from_pdf(pdf_path: str):
    reader = PdfReader(pdf_path)
    
    pages = []
    text = ""
    for index, page in enumerate(reader.pages):
        
        text = page.extract_text()
        pages.append({"page": index + 1, "text": text})
    
    return pages