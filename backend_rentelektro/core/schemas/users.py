from pydantic import BaseModel, EmailStr, Field
from typing import List, Union, Optional
from .tools import Tool


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
    profile_picture: Optional[str] = None


class User(UserBase):
    id: int
    username: str
    firstname: str
    lastname: str
    phone: str
    company: bool
    tools: List[Tool] = []

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None
    scopes: List[str] = []


class RefreshTokenRequest(BaseModel):
    refresh_token: str
