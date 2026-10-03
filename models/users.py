from sqlalchemy import String,Column,Integer,Float
from database import Base

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True)
    name = Column(String(100),nullable=False)
    password = Column(String,nullable=False)
    
