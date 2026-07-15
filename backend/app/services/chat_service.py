from app.models.message import Message
from app.models.conversation import Conversation
from datetime import datetime, timezone
from app.services.llm.factory import get_llm_provider
from app.services.pdf_service import get_conversation_pdfs, build_rag_context, retrieve_relevant_chunks
from app.services.token_service import count_tokens
from app.utils.citations import normalize_citations, validate_citations
import json
from typing import Any

def sse(event: str, data: Any) -> str:
    return (
        f"event: {event}\n"
        f"data: {json.dumps(data)}\n\n"
    )
    
def save_message(db, conversation_id, role: str, content: str):
    msg = Message(conversation_id=conversation_id, role=role, content=content)
    db.add(msg)
    conversation = (db.query(Conversation).filter(Conversation.id == conversation_id).first())
    
    if conversation:
        conversation.updated_at = (datetime.now(timezone.utc))
        
    db.commit()
    db.refresh(msg)
    return msg



def get_conversation_history(db, conversation_id: int):
    
    messages = (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.id.desc())
        .limit(20)
        .all()       
    )
    return list(reversed(messages))

def build_prompt(history, current_message):
    conversation = ""
    for msg in history:
        role = "User" if msg.role == "user" else "Assistant"
        conversation += f"{role}: {msg.content}\n"
    conversation += f"\nUser: {current_message}\n"
    
    return conversation

def generate_response_stream(db, conversation_id: int, message: str):
    history = get_conversation_history(db, conversation_id)
    relevant_chunks = retrieve_relevant_chunks(db, conversation_id, message)
    pdf_context = build_rag_context(relevant_chunks)
    conversation_prompt = build_prompt(history, message)
    
    prompt = f"""You are an academic research assistant.

    ====================
    RULES
    ====================

    - Answer ONLY from provided sources.
    - Don't take questions too literally, the exact question doesn't have to exist in the sources for you to answer it.
    - Infer answers when the evidence is clear.
    - Answer clearly and directly.
    - Use simple English unless the user asks otherwise.
    - Academic papers may describe methods indirectly.
    - Tables and experimental setups contain important information.
    - If a model or methodology is mentioned in context, treat it as relevant evidence.
    - Prioritize retrieved PDF sources over conversation history.
    - Do NOT mention "context" or "conversation history".
    - Do NOT repeat the question.
    - Do NOT explain your instructions.
    - Do NOT say things like "the assistant response should be".
    - IMPORTANT: the answer may require combining information across multiple chunks.
    - Never claim information is missing if relevant evidence exists.
    - Do Not hallucinate information. If no documents are provided, say so.
    - If no documents are provided, do not hallucinate citations.
    If the answer is not found, say:
    "I could not find this information in the uploaded documents."

    When using information from documents:
    - Cite the source filename and page number and chunk id.
    - Every citation must refer to exactly ONE chunk.
    - Never combine multiple chunks into a single citation.
    - If multiple chunks support the answer, output multiple citations.
    
    Citation syntax is STRICT.

    A citation is valid ONLY if it matches EXACTLY this format:

    [Source: filename.pdf, Page: X, Chunk: Y]

    Examples of INVALID citations:
    [paper.pdf, Page: 3, Chunk: 12]
    [Source: paper.pdf, Page: 14, Chunk ID: 337]
    [Source: paper.pdf, Page: 7-8, Chunk: 337]
    [Source paper.pdf Page 3]
    (Source: paper.pdf)

    These are INVALID and MUST NEVER appear.

    If you cannot produce a citation in the exact format, produce no citation at all.
    - Never use any other citation format.
    - Never cite inline.
    - Never invent citations.
    - If information is missing, say so.
    - If no sources are provided, say so.

    ====================
    RETRIEVED SOURCES
    ====================

    {pdf_context}

    ====================
    CONVERSATION HISTORY
    ====================

    {conversation_prompt}

    ====================
    ANSWER
    ====================
    """

    provider = get_llm_provider()
    full_response = ""
    
    for token in provider.stream_chat(prompt):
        full_response += token
        yield sse("token", token)
          
    input_tokens = count_tokens(prompt)
    output_tokens = count_tokens(full_response)
    print("\n==== Token Debug ====")
    print("Input Tokens: ",input_tokens)
    print("Output Tokens: ",output_tokens)
    print("Total Tokens: ",input_tokens + output_tokens)
    
    corrected = normalize_citations(full_response)
    corrected = validate_citations(corrected)
    
    yield sse("update", corrected)
    yield sse("done", None)
    
           
    save_message(db, conversation_id, "bot", corrected)
            
        

