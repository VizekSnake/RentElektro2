from sqlalchemy import Boolean, Column, Integer, String, Text, Float, Enum as SQLAlchemyEnum, ForeignKey, DateTime, Boolean, Date
from core.database import Base
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum

class TypeEnum(SQLAlchemyEnum):
    hammer = "hammer"
    saw = "saw"
    drill = "drill"


class PowerSourceEnum(SQLAlchemyEnum):
    electric = "electric"
    gas = "gas"


class AcceptedEnum(PyEnum):
    accepted = "accepted"
    rejected_by_owner = "rejected_by_owner"
    canceled = "canceled"
    fulfilled = "fulfilled"
    paid_rented = "paid_rented"
    paid_not_rented = "paid_not_rented"
    viewed = "viewed"
    not_viewed = "not_viewed"
    problem = "problem"
    scam = "scam"

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
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="tools")
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
    tools = relationship("Tool", back_populates="category")
    creator_id = Column(Integer, ForeignKey("users.id"))


class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    tool_id = Column(Integer, index=True)
    user_id = Column(Integer)
    rating = Column(Float)
    comment = Column(String, nullable=True)


class Rental(Base):
    __tablename__ = "rentals"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    tool_id = Column(Integer, ForeignKey("tools.id"))
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime,nullable=False)
    comment = Column(String, nullable=True)
    owner_comment = Column(String, nullable=True)
    status = Column(SQLAlchemyEnum(AcceptedEnum))


