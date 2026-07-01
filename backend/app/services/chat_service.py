from app.models.message import Message
from app.models.conversation import Conversation
from datetime import datetime, timezone
from app.services.pdf_service import get_conversation_pdfs, build_rag_context, retrieve_relevant_chunks
import requests
import json


def save_message(db, conversation_id, role: str, content: str):
    msg = Message(conversation_id=conversation_id, role=role, content=content)
    db.add(msg)
    conversation = (db.query(Conversation).filter(Conversation.id == conversation_id).first())
    
    if conversation:
        conversation.updated_at = (datetime.now(timezone.utc))
        
    db.commit()
    db.refresh(msg)
    return msg


def generate_response(db, conversation_id: int, message: str):
    
    history = get_conversation_history(db, conversation_id)
    
    pdfs = get_conversation_pdfs(db, conversation_id)
    
    relevant_chunks = retrieve_relevant_chunks(pdfs, message)
    
    pdf_context = build_rag_context(relevant_chunks)
    
    conversation_prompt = build_prompt(history, message)
    prompt = f"""You are a research assistant.
    
    PDF Context:
    {pdf_context}
    
    Conversation History:
    {conversation_prompt}
    """
    
    
    
    
    response = requests.post("http://localhost:11434/api/generate",
                             json={
                                 "model": "mistral",
                                   "prompt": prompt,
                                   "stream": True
                                   }
                             )
    data = response.json()
    
    return data["response"]


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
    conversation += f"\nUser: {current_message}\nAssistant:"
    
    return conversation

def generate_response_stream(db, conversation_id: int, message: str):
    history = get_conversation_history(db, conversation_id)
    pdfs = get_conversation_pdfs(db, conversation_id)
    relevant_chunks = retrieve_relevant_chunks(pdfs, message)
    pdf_context = build_rag_context(relevant_chunks)
    conversation_prompt = build_prompt(history, message)
    
    prompt = f"""You are a research assistant.
    
    PDF Context:
    {pdf_context}
    
    Conversation History:
    {conversation_prompt}
    """
    
    response = requests.post("http://localhost:11434/api/generate",
                             json={
                                 "model": "mistral",
                                 "prompt": prompt},
                             stream=True)
    full_response = ""
    
    for line in response.iter_lines():
        if not line:
            continue
        try:
            data = json.loads(line)
            token = data.get("response", "")
            full_response += token
            
            yield token
        except Exception as e:
            print("Stream error: ", e)
        
            
    save_message(db, conversation_id, "bot", full_response)
            
        

