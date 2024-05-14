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


class Tool(Base):
    __tablename__ = "tools"

    id = Column(Integer, primary_key=True, index=True)
    Type = Column(String)
    PowerSource = Column(String)
    Brand = Column(String)
    Description = Column(String)
    CategoryID = Column(Integer)
    Availability = Column(Boolean)
    Insurance = Column(Boolean)
    Power = Column(Integer)
    Age = Column(Float)
    RatePerDay = Column(Float)
    ImageURL = Column(String)


class TypeEnum(Enum):
    hammer = "hammer"
    saw = "saw"
    drill = "drill"

class PowerSourceEnum(Enum):
    electric = "electric"
    gas = "gas"