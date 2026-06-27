from fastapi import APIRouter, Depends
from  app.services.conversation_service import create_conversation
from app.database.deps import get_db
from sqlalchemy.orm import Session
from app.models.conversation import Conversation

router = APIRouter()

@router.post("/")
def create_new_conversation(user_id: str, db: Session = Depends(get_db)):
    conversation = create_conversation(db, user_id)
    
    return {
        "conversation_id": conversation.id,
        "title": conversation.title
    }
    
    
@router.get("/{user_id}")
def get_user_conversations(user_id: str, db: Session = Depends(get_db)):
    conversations = db.query(Conversation).filter(Conversation.user_id == user_id).all()
    
    return conversations
    
