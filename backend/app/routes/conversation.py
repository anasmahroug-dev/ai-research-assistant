from fastapi import APIRouter, Depends
from  app.services.conversation_service import create_conversation, delete_conversation_service, rename_conversation_service
from app.database.deps import get_db
from app.models.user import User
from app.dependencies.auth import get_current_user
from sqlalchemy.orm import Session
from app.models.conversation import Conversation

router = APIRouter()

@router.post("/")
def create_new_conversation(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    conversation = create_conversation(db, current_user.id)
    
    return {
        "id": conversation.id,
        "title": conversation.title
    }
    
    
@router.get("/")
def get_user_conversations(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    conversations = (db.query(Conversation).filter(Conversation.user_id == current_user.id).order_by(Conversation.updated_at.desc()).all())
    
    return conversations

@router.delete("/{conversation_id}")
def delete_conversation(
    conversation_id: int,
    db: Session = Depends(get_db)
):
    success = delete_conversation_service(db, conversation_id)
    if not success:
        return {"error": "Conversation not found"}
    
    return {
        "message": "Conversation deleted"
    }
    

@router.put("/{conversation_id}")
def rename_conversation(conversation_id: int,
                        title: str,
                        db: Session = Depends(get_db)):
    conversation = rename_conversation_service(db, conversation_id, title)
    if not conversation:
        return{"error": "Conversation not found"}
    return conversation
    
