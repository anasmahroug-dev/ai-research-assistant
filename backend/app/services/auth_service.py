from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import RegisterRequest, LoginRequest
from app.utils.security import hash_password, verify_password
from app.utils.jwt import create_access_token
from uuid import uuid4


def register_user(db: Session, data: RegisterRequest):
    existing_email =(
        db.query(User)
        .filter(User.email == data.email)
        .first()
    )
    
    if existing_email:
        return None, "Email already exists"
    
    
    user = User(
        username=data.username,
        email= data.email,
        password_hash= hash_password(data.password),
        is_guest=False,
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    token = create_access_token(user.id)
    
    return {
        "access_token" : token,
        "token_type": "bearer",
        "user": user,
    }, None
    
    
def login_user(db: Session, data: LoginRequest):
    
    user = (
        db.query(User)
        .filter(User.email == data.email)
        .first()
    )
    
    if not user:
        return None, "Invalid credentials"

    if not verify_password(
        data.password,
        user.password_hash,
    ):
        return None, "Invalid credentials"
    
    token = create_access_token(user.id)
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user,
    }, None
    
def create_guest_user(db: Session):
    guest_id = uuid4().hex[:8]
    guest = User(
        username=f"Guest-{guest_id}",
        email=f"guest-{guest_id}@aira.com",
        password_hash="",
        is_guest=True,
    )
    
    db.add(guest)
    db.commit()
    db.refresh(guest)
    
    token = create_access_token(user_id=guest.id)
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": guest,
    }