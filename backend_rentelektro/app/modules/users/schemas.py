from typing import List, Optional, Union

from pydantic import AliasChoices, BaseModel, ConfigDict, EmailStr, Field

from app.modules.tools.schemas import Tool


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    username: str
    firstname: str = Field(
        default="",
        validation_alias=AliasChoices("firstname", "first_name", "firstName"),
    )
    lastname: str = Field(
        default="",
        validation_alias=AliasChoices("lastname", "last_name", "lastName"),
    )
    phone: str = Field(
        default="",
        validation_alias=AliasChoices("phone", "phone_number", "phoneNumber"),
    )
    company: bool = Field(
        default=False,
        validation_alias=AliasChoices("company", "is_company", "isCompany"),
    )
    password: str = Field(
        ...,
        validation_alias=AliasChoices("password", "password1"),
    )

    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)


class UserUpdate(BaseModel):
    username: Optional[str] = None
    firstname: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("firstname", "first_name", "firstName"),
    )
    lastname: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("lastname", "last_name", "lastName"),
    )
    phone: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("phone", "phone_number", "phoneNumber"),
    )
    company: Optional[bool] = Field(
        default=None,
        validation_alias=AliasChoices("company", "is_company", "isCompany"),
    )
    # Password updates might be handled separately
    email: Optional[EmailStr] = None
    profile_picture: Optional[str] = None

    model_config = ConfigDict(populate_by_name=True)


class User(UserBase):
    id: int
    username: str
    firstname: str
    lastname: str
    phone: str
    company: bool
    tools: List[Tool] = []

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    username: str
    password: str


class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str


class AccountAnonymizeRequest(BaseModel):
    current_password: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None
    scopes: List[str] = []


class RefreshTokenRequest(BaseModel):
    refresh_token: str
