from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone

from app.database.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key =True)

    email = Column(String, unique=True, nullable=False)
   
    username = Column(String, nullable=False)
   
    password_hash = Column(String, nullable=False)
    
    created_at = Column(DateTime, default=lambda:datetime.now(timezone.utc))
    
    