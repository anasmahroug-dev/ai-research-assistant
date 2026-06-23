chat_history = {}

def generate_response(user_id: str, message: str):
    
    if user_id not in chat_history:
        chat_history[user_id] = []
    
    history = chat_history[user_id]
    
    history.append({"role": "user", "message": message})
    
    msg = message.lower()
    if "hello" in msg:
        response = "Hello!"
    elif "help" in msg:
        response = "I can help you with documents or summaries"
    elif "memory" in msg:
        response = f"You have {len(history)} messages in your history"
    else:
        response = f"You said: {message}"

    history.append({"role": "bot", "message": response})
    
    return response


