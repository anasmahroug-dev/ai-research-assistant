from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.message import Message

from app.models.chat import ChatRequest
from app.services.chat_service import generate_response, save_message
from app.database.deps import get_db

router = APIRouter()

@router.post("/")
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    save_message(db, request.user_id, role="user", content=request.message)
    response = generate_response(request.message)
    save_message(db, request.user_id, role="bot", content=response)
    
    return {        
        "response" : response
    }

@router.get("/history/{user_id}")
def get_history(user_id: str, db: Session = Depends(get_db)):
    messages = db.query(Message).filter(Message.user_id == user_id).all()
    
    return [{
            "role":m.role,
            "message": m.content            
            }for m in messages]