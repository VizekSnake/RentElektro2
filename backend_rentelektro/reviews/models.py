from core.database import Base
from sqlalchemy import Column, Float, Integer, String


class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    tool_id = Column(Integer, index=True)
    user_id = Column(Integer)
    rating = Column(Float)
    comment = Column(String, nullable=True)