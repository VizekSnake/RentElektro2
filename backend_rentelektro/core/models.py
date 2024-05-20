from sqlalchemy import Boolean, Column, Integer, String, Text, Float, Enum, ForeignKey
from core.database import Base
from sqlalchemy.orm import relationship


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


class Tool(Base):
    __tablename__ = "tools"

    id = Column(Integer, primary_key=True, index=True)
    Type = Column(String)
    PowerSource = Column(String)
    Brand = Column(String)
    Description = Column(String)
    Category = relationship("Category", back_populates="tools")
    Availability = Column(Boolean)
    Insurance = Column(Boolean)
    Power = Column(Integer)
    Age = Column(Float)
    RatePerDay = Column(Float)
    ImageURL = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="tools")


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String)
    description = Column(String)
    active = Column(Boolean, default=True)
    tools = relationship("Tool", back_populates="Category")
    creator_id = Column(Integer, ForeignKey("users.id"))


class TypeEnum(Enum):
    hammer = "hammer"
    saw = "saw"
    drill = "drill"


class PowerSourceEnum(Enum):
    electric = "electric"
    gas = "gas"
