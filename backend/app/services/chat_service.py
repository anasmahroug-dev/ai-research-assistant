from app.models.message import Message


chat_history = {}

def save_message(db, user_id: str, role: str, content: str):
    msg = Message(user_id=user_id, role=role, content=content)
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg


def generate_response(message: str):  
    msg = message.lower()
    if "hello" in msg:
        response = "Hello!"
    elif "help" in msg:
        response = "I can help you with documents or summaries"
    else:
        response = f"You said: {message}"
 
    return response


