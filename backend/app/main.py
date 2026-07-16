from dotenv import load_dotenv
load_dotenv()

import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.database.database import Base, engine
from app.models import (
    conversation as conversation_model,
    message,
    pdf_document,
)
from app.routes import (
    auth,
    chat,
    chunks,
    conversation,
    health,
    pdf,
)

FRONTEND_URL = os.getenv("FRONTEND_URL")

app = FastAPI()


BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

app.mount(
    "/uploads",
    StaticFiles(directory=str(UPLOAD_DIR)),
    name="uploads",
)


origins = [
    "http://localhost:3000",
]

if FRONTEND_URL:
    origins.append(FRONTEND_URL)

print("Allowed origins:", origins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Base.metadata.create_all(bind=engine)


app.include_router(
    health.router,
    prefix="/health",
    tags=["Health"],
)

app.include_router(
    chat.router,
    prefix="/chat",
    tags=["Chat"],
)

app.include_router(
    pdf.router,
    prefix="/pdf",
    tags=["PDF"],
)

app.include_router(
    conversation.router,
    prefix="/conversations",
    tags=["Conversations"],
)

app.include_router(
    chunks.router,
    prefix="/chunks",
    tags=["Chunks"],
)

app.include_router(auth.router)