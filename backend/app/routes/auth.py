from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.database.deps import get_db
from app.schemas.user import RegisterRequest, LoginRequest, AuthResponse, UserResponse
from app.services.auth_service import register_user, login_user, create_guest_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentification"],
)

@router.post("/register", response_model=AuthResponse)
def register(
    data:RegisterRequest,
    db: Session = Depends(get_db),
):
    result, error = register_user(db, data)
    
    if error:
        raise HTTPException(status_code=400,
                            detail=error)
    return result

@router.post("/login", response_model=AuthResponse)
def login(data: LoginRequest,
          db: Session = Depends(get_db)):
    result, error = login_user(db, data)
    
    if error:
        raise HTTPException(
            status_code=401,
            detail=error
        )
        
    return result

@router.get(
    "/me",
    response_model=UserResponse,
)
def me(
    current_user: User = Depends(get_current_user),
):
    return current_user

@router.post("/guest", response_model=AuthResponse)
def guest(
    db: Session = Depends(get_db)
    ):
    return create_guest_user(db) 