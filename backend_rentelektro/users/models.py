from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    firstname = Column(String)
    lastname = Column(String)
    hashed_password = Column(String)
    phone = Column(String)
    company = Column(Boolean, default=False)
    profile_picture = Column(String)
    role = Column(String)
    is_active = Column(Boolean, default=True)
    tools = relationship("Tool", back_populates="owner")