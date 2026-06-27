from app.models.conversation import Conversation

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