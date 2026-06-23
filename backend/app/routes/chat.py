from fastapi import APIRouter
from app.models.chat import ChatRequest
from app.services.chat_service import generate_response, chat_history

router = APIRouter()

@router.post("/")
def chat(request: ChatRequest):
    response = generate_response(request.user_id, request.message)
    
    return {        
        "response" : response
    }

@router.get("/history/{user_id}")
def get_history(user_id: str):
    return {
            "user_id": user_id,
            "history": chat_history.get(user_id, [])
            
            }