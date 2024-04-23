from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    username: str
    firstname: str
    lastname: str
    phone: str
    company: bool
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[bool] = None
    # Password updates might be handled separately
    email: Optional[EmailStr] = None


class User(UserBase):
    id: int
    username: str
    firstname: str
    lastname: str
    phone: str
    company: bool

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str
