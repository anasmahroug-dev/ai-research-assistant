from fastapi import FastAPI
from app.routes import health, chat

app = FastAPI()

app.include_router(health.router,
                   prefix="/health",
                   tags=["Health"]
            )
app.include_router(chat.router,
                   prefix="/chat",
                     tags=["Chat"]
                     )