from sqlalchemy import Boolean, Column, Integer, String, Float, Enum as SQLAlchemyEnum, ForeignKey, Boolean
from core.database import Base
from sqlalchemy.orm import relationship

class TypeEnum(SQLAlchemyEnum):
    hammer = "hammer"
    saw = "saw"
    drill = "drill"


class PowerSourceEnum(SQLAlchemyEnum):
    electric = "electric"
    gas = "gas"


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