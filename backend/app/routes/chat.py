from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.message import Message


from app.models.chat import ChatRequest
from app.services.chat_service import generate_response, save_message
from app.services.conversation_service import get_conversation
from app.database.deps import get_db

router = APIRouter()

@router.post("/")
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    conversation = get_conversation(db, request.conversation_id)
    if not conversation:
        return {
            "error": "Conversation not found"
        }
        
    save_message(db, request.conversation_id, role="user", content=request.message)
    response = generate_response(db, request.conversation_id, request.message)
    save_message(db, request.conversation_id, role="bot", content=response)
    
    return {        
        "response" : response
    }

@router.get("/history/{conversation_id}")
def get_history(conversation_id: int, db: Session = Depends(get_db)):
    messages = db.query(Message).filter(Message.conversation_id == conversation_id).all()
    
    return [{
            "role":m.role,
            "message": m.content            
            }for m in messages]