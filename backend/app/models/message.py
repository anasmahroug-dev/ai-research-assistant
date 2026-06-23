from sqlalchemy import Column, Integer, String
from app.database.database import Base

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    
    user_id = Column(String)
    
    role = Column(String)
    
    content = Column(String)