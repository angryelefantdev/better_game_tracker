from sqlalchemy import String,Column,Integer,Float
from database import Base

class Games(Base):
    __tablename__ = "games"
    id = Column(Integer,primary_key=True)
    name = Column(String(100),nullable=False)
    genre = Column(String(100))
    rating = Column(Float)
    developer = Column(String(100))
    rawg_id = Column(Integer)
    user_id = Column(Integer)

