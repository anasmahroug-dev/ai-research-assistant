from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from app.routes import health, chat, pdf, conversation, chunks
from fastapi.staticfiles import StaticFiles
from app.database.database import engine, Base
from app.models import (
    message,
    pdf_document,
    conversation as conversation_model
)
from fastapi.middleware.cors import CORSMiddleware






app = FastAPI()

app.mount("/uploads",
          StaticFiles(directory="uploads"),
          name="uploads")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
Base.metadata.create_all(bind=engine)


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

app.include_router(chunks.router,
                   prefix = "/chunks",
                   tags=["Chunks"])