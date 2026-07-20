import re


def chunk_pages(pages):
    total_pages = len(pages)

    if total_pages <= 2:
        target_size = 500
    elif total_pages <= 10:
        target_size = 800
    elif total_pages <= 25:
        target_size = 1200
    else:
        target_size = 1600

    chunks = []

    for page_data in pages:
        page_number = page_data["page"]
        text = page_data["text"].strip()

        if not text:
            continue

        paragraphs = [
            p.strip()
            for p in re.split(r"\n\s*\n", text)
            if p.strip()
        ]

        current_chunk = ""

        for paragraph in paragraphs:

            if len(paragraph) > target_size:

                words = paragraph.split()

                current = ""

                for word in words:
                    if len(current) + len(word) + 1 <= target_size:
                        current += (" " if current else "") + word
                    else:
                        chunks.append({
                            "text": current,
                            "page": page_number,
                        })
                        current = word

                if current:
                    chunks.append({
                        "text": current,
                        "page": page_number,
                    })

                continue

            if len(current_chunk) + len(paragraph) + 2 <= target_size:

                if current_chunk:
                    current_chunk += "\n\n"

                current_chunk += paragraph

            else:

                if current_chunk:
                    chunks.append({
                        "text": current_chunk,
                        "page": page_number,
                    })

                current_chunk = paragraph

        if current_chunk:
            chunks.append({
                "text": current_chunk,
                "page": page_number,
            })

    return chunks