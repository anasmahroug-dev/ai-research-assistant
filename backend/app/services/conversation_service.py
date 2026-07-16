from app.models.conversation import Conversation
from app.models.message import Message
from app.models.pdf_document import PDFDocument
from app.models.pdf_chunk import PDFChunk
from app.services.cloudinary_service import delete_pdf_from_cloudinary
from datetime import datetime, timezone



def create_conversation(db, user_id, title="New Chat"):
    conversation = Conversation(user_id=user_id, title=title, updated_at=datetime.now(timezone.utc))
    
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
    
def delete_conversation_service(db, conversation_id: int, current_user):
    pdfs = (
    db.query(PDFDocument)
    .filter(PDFDocument.conversation_id == conversation_id)
    .all()
    )
    
    for pdf in pdfs:
        if pdf.cloudinary_public_id:
            delete_pdf_from_cloudinary(pdf.cloudinary_public_id)
    
    
    db.query(PDFChunk).filter(
        PDFChunk.conversation_id == conversation_id
    ).delete(synchronize_session=False)

    db.query(PDFDocument).filter(
        PDFDocument.conversation_id == conversation_id
    ).delete(synchronize_session=False)

    db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).delete(synchronize_session=False)

    deleted = (
        db.query(Conversation)
        .filter(Conversation.id == conversation_id, 
                Conversation.user_id == current_user.id)
        .delete(synchronize_session=False)
    )

    if deleted == 0:
        db.rollback()
        return None

    db.commit()
    return True


def rename_conversation_service(db, conversation_id: int, current_user, title:str):
    conversation = (db.query(Conversation)
                    .filter(Conversation.id == conversation_id,
                            Conversation.user_id == current_user.id)
                    .first()
                    )
    if not conversation:
        return None
    conversation.title = title
    db.commit()
    db.refresh(conversation)
    return conversation
    
    
    