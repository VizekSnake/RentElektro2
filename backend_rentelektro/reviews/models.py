from sqlalchemy import Column, Integer, String,Float
from core.database import Base

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    tool_id = Column(Integer, index=True)
    user_id = Column(Integer)
    rating = Column(Float)
    comment = Column(String, nullable=True)