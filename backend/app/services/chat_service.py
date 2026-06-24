from app.models.message import Message
import requests


chat_history = {}

def save_message(db, user_id: str, role: str, content: str):
    msg = Message(user_id=user_id, role=role, content=content)
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg


def generate_response(db, user_id: str,message: str):  
    
    history = get_conversation_history(db, user_id)
    
    prompt = build_prompt(history, message)
    
    
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
        .limit(10)
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
        

