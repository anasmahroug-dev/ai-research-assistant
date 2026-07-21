import re
import fitz

def clean_text(text: str) -> str:
    text = re.sub(r"(?<=\w)-\n(?=\w)", "", text)    
    text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    
    return text.strip()

def extract_pages_from_pdf(pdf_bytes: bytes):
    doc = fitz.open(
        stream=pdf_bytes,
        filetype="pdf",
    )

    pages = []

    for index, page in enumerate(doc):
        
        text = page.get_text()
        
        pages.append({
            "page": index + 1,
            "text": text,
        })
         
        if index == 0:
            print("========== AFTER EXTRACT ==========")
            print(text)


    print("========== EXTRACTED TEXT ==========")
    print(repr(pages[0]["text"][:500]))

    doc.close()
    

    return pages

def split_into_blocks(text: str):
    raw_blocks = re.split(r"\n\s*\n+", text)

    raw_blocks = [
        block.strip()
        for block in raw_blocks
        if block.strip()
    ]

    merged_blocks = []

    i = 0
    while i < len(raw_blocks):

        block = raw_blocks[i]

        while (
            len(block) < 80
            and i + 1 < len(raw_blocks)
        ):
            i += 1
            block += "\n\n" + raw_blocks[i]

        merged_blocks.append(block)
        i += 1

    return merged_blocks
