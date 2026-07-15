from datetime import datetime, timedelta, timezone

from jose import jwt, JWTError

SECRET_KEY = "CHANGE_ME"
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_DAYS = 365


def create_access_token(user_id: int):
    
    expire = datetime.now(timezone.utc) + timedelta(
        days=ACCESS_TOKEN_EXPIRE_DAYS)
    
    payload = {
        "sub": str(user_id),
        "exp": expire,
    }
    
    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    
def decode_access_token(token:str):
    try: 
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        
        return payload
    except JWTError:
        return None