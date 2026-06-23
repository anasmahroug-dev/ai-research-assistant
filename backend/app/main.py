from fastapi import FastAPI
from app.routes import health, chat
from app.database.database import engine, Base
from app.models.message import Message

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