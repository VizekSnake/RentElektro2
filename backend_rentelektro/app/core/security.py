import uuid
import warnings
from datetime import datetime, timedelta, timezone
from hashlib import sha256
from hmac import new as hmac_new
from secrets import token_urlsafe
from typing import Any, Optional, TypedDict

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette.requests import Request

from app.core.config import get_settings
from app.core.dependencies import get_db
from app.modules.users.models import User as UserModel

warnings.filterwarnings("ignore", category=DeprecationWarning, module="passlib.utils")
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/token", auto_error=False)
settings = get_settings()
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS

# TODO: add redis blacklist mechanism for token revocation,
# to handle cases like password change, account deletion, or manual
# logout from all devices. This will allow us to invalidate existing tokens without
# having to wait for them to expire naturally.


class TokenPayload(TypedDict):
    username: str
    id: uuid.UUID


def _normalize_token_data(data: dict[str, Any]) -> dict[str, Any]:
    normalized: dict[str, Any] = {}
    for key, value in data.items():
        if isinstance(value, uuid.UUID):
            normalized[key] = str(value)
        else:
            normalized[key] = value
    return normalized


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = _normalize_token_data(data)
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict):
    to_encode = _normalize_token_data(data)
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def generate_password_reset_token() -> str:
    return token_urlsafe(48)


def hash_password_reset_token(token: str) -> str:
    return hmac_new(SECRET_KEY.encode("utf-8"), token.encode("utf-8"), sha256).hexdigest()


def verify_token(token: str) -> TokenPayload:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if not isinstance(payload, dict):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        username = payload.get("username")
        user_id = payload.get("id")
        if not isinstance(username, str) or not isinstance(user_id, str):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        try:
            parsed_user_id = uuid.UUID(user_id)
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            ) from exc

        return {"username": username, "id": parsed_user_id}
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return bcrypt_context.hash(password)


def get_user_exception():
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return credentials_exception


async def get_access_token(
    request: Request, bearer_token: str | None = Depends(oauth2_scheme)
) -> str:
    token = bearer_token or request.cookies.get("access_token")
    if not token:
        raise get_user_exception()
    return token


async def get_current_user(token: str = Depends(get_access_token), db: Session = Depends(get_db)):
    try:
        payload = verify_token(token)
        user = db.query(UserModel).filter(UserModel.id == payload["id"]).first()
        if user is None:
            raise get_user_exception()
        return user
    except HTTPException:
        raise get_user_exception()
