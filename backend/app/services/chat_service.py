from app.models.message import Message
from app.services.pdf_service import get_user_pdfs, build_pdf_context, build_rag_context, retrieve_relevant_chunks
import requests


def save_message(db, user_id: str, role: str, content: str):
    msg = Message(user_id=user_id, role=role, content=content)
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg


def generate_response(db, user_id: str,message: str):  
    
    history = get_conversation_history(db, user_id)
    
    pdfs = get_user_pdfs(db, user_id)
    
    relevant_chunks = retrieve_relevant_chunks(pdfs, message)
    
    pdf_context = build_rag_context(relevant_chunks)
    
    conversation_prompt = build_prompt(history, message)
    prompt = f"""You are an AI research assistant.
    
    PDF Context:
    {pdf_context}
    
    Conversation History:
    {conversation_prompt}
    """
    
    
    
    
    response = requests.post("http://localhost:11434/api/generate",
                             json={
                                 "model": "mistral",
                                   "prompt": prompt,
                                   "stream": False
                                   }
                             )
    data = response.json()
    
    return data["response"]


def get_conversation_history(db, user_id: str):
    
    messages = (
        db.query(Message)
        .filter(Message.user_id == user_id)
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
        

