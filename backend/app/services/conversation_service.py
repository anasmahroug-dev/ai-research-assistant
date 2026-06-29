from app.models.conversation import Conversation
from app.models.message import Message
from app.models.pdf_document import PDFDocument

def create_conversation(db, user_id, title="New Chat"):
    conversation = Conversation(user_id=user_id, title=title)
    
    db.add(conversation)
    
    db.commit()
    
    db.refresh(conversation)
    
    return conversation

def get_conversation(db,conversation_id: int
):

    return (
        db.query(Conversation)
        .filter(
            Conversation.id
            == conversation_id
        )
        .first()
    )
    
def delete_conversation_service(db, conversation_id: int):
    
    conversation = (
        db.query(Conversation)
        .filter(Conversation.id == conversation_id)
        .first()
        )
    if not conversation:
        return None
    db.query(Message).filter(Message.conversation_id == conversation_id).delete()
    db.query(PDFDocument).filter(PDFDocument.conversation_id == conversation_id).delete()
    db.delete(conversation)
    db.commit()
    return True


def rename_conversation_service(db, conversation_id: int, title:str):
    conversation = (db.query(Conversation)
                    .filter(Conversation.id == conversation_id)
                    .first()
                    )
    if not conversation:
        return None
    conversation.title = title
    db.commit()
    db.refresh(conversation)
    return conversation
    
    
    