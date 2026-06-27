from fastapi import FastAPI
from app.routes import health, chat, pdf, conversation
from app.database.database import engine, Base
from app.models import (
    message,
    pdf_document,
    conversation as conversation_model
)


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(health.router,
                   prefix="/health",
                   tags=["Health"]
            )
app.include_router(chat.router,
                   prefix="/chat",
                     tags=["Chat"]
                     )

app.include_router(pdf.router,
                   prefix="/pdf",
                     tags=["PDF"]
                     )
app.include_router(conversation.router,
                   prefix ="/conversations",
                   tags=["Conversations"]
                   )