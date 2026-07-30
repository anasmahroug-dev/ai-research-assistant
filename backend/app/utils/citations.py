import re
CITATION_PATTERN = re.compile(
    r"""
    \[
    Source:\s*
    (?P<filename>.+?\.pdf)
    ,\s*
    Page:\s*
    (?P<pages>\d+(?:\s*,\s*\d+)*)
    ,\s*
    Chunk:\s*
    (?P<chunk>\d+)
    \]
    """,
    re.VERBOSE | re.IGNORECASE,
)


def normalize_citations(text: str) -> str:
    """
    Repairs common citation mistakes made by the LLM.

    Supported repairs:
    - missing 'Source:'
    - source -> Source
    - Pages -> Page
    - page ranges (7-8 -> 7, 8)
    - multiple chunks -> split into multiple citations
    """

    # ----------------------------
    # Simple text normalization
    # ----------------------------

    text = text.replace("【", "[")
    text = text.replace("】", "]")
    
    text = re.sub(
        r"\[(?!\s*Source:)([^,\]]+?\.pdf)\s*,",
        r"[Source: \1,",
        text,
        flags=re.IGNORECASE,
    )

    text = re.sub(
        r"\[\s*source\s*:",
        "[Source:",
        text,
        flags=re.IGNORECASE,
    )

    text = re.sub(
        r"\bPages\b",
        "Page",
        text,
        flags=re.IGNORECASE,
    )

    text = re.sub(r"\s*,\s*", ", ", text)
    text = re.sub(r"\s*:\s*", ": ", text)
    text = re.sub(r"\s{2,}", " ", text)

    # ----------------------------
    # Split malformed citations
    # ----------------------------

    pattern = re.compile(
        r"""
        \[
        Source:\s*
        (?P<filename>.+?\.pdf)
        ,\s*
        Page:\s*
        (?P<pages>.+?)
        ,\s*
        Chunk:\s*
        (?P<chunks>.+?)
        \]
        """,
        re.VERBOSE | re.IGNORECASE,
    )

    def repair(match):

        filename = match.group("filename").strip()

        pages_raw = match.group("pages").strip()
        chunks_raw = match.group("chunks").strip()

        # ------------------------
        # Parse pages
        # ------------------------

        pages = []

        for part in pages_raw.split(","):

            part = part.strip()

            if "-" in part:

                try:
                    start, end = map(int, part.split("-"))

                    pages.extend(
                        str(i)
                        for i in range(start, end + 1)
                    )

                except ValueError:
                    continue

            elif part.isdigit():
                pages.append(part)

        # ------------------------
        # Parse chunks
        # ------------------------

        chunks = re.findall(r"\d+", chunks_raw)

        if not pages:
            pages = ["1"]

        if not chunks:
            return match.group(0)

        repaired = []

        for i, chunk in enumerate(chunks):

            page = pages[min(i, len(pages) - 1)]

            repaired.append(
                f"[Source: {filename}, Page: {page}, Chunk: {chunk}]"
            )

        return " ".join(repaired)

    return pattern.sub(repair, text)
    
def validate_citations(text: str) -> str:
    """
    Removes malformed citations.
    """

    def validate(match):

        citation = match.group(0)

        # Must match our grammar exactly
        parsed = CITATION_PATTERN.fullmatch(citation)

        if parsed is None:
            print(f"Removed invalid citation:\n{citation}\n")
            return ""

        pages = parsed.group("pages")
        chunk = parsed.group("chunk")

        # Reject page ranges like 7-8
        if "-" in pages:
            print(f"Removed page range citation:\n{citation}\n")
            return ""

        # Reject multiple chunks
        if "," in chunk:
            print(f"Removed multi-chunk citation:\n{citation}\n")
            return ""

        return citation

    return re.sub(
        r"\[[^\]]+\]",
        validate,
        text,
    )
    
def debug_citations(text: str):
    print("\n========== CITATIONS ==========")

    matches = re.findall(r"\[(.*?)\]", text)

    if not matches:
        print("No citations found.")
        return

    for i, citation in enumerate(matches, 1):
        print(f"{i}. [{citation}]")

    print("===============================\n")