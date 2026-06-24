from app.models.message import Message


chat_history = {}

def save_message(db, user_id: str, role: str, content: str):
    msg = Message(user_id=user_id, role=role, content=content)
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg


def generate_response(db, user_id: str,message: str):  
    
    history = get_conversation_history(db, user_id)
    history_count = len(history)
    
    msg = message.lower()
    
    
    if "hello" in msg:
        response = "Hello!"
    elif "history" in msg:
        response = f"I remember {history_count} messages in our conversation."
    elif "last message" in msg:
        if history:
            response = f"Your last message was: {history[-1].content}"
        else:
            response = "No history found."
            
    elif "help" in msg:
        response = "I can help you with documents or summaries"
    else:
        response = f"You said: {message}"
 
    return response


def get_conversation_history(db, user_id: str):
    
    messages = (
        db.query(Message)
        .filter(Message.user_id == user_id)
        .all()       
    )
    return messages

