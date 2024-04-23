import os
from typing import List

from jose import jwt, JWTError
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from core.models import User as UserModel
from core.schemas.users import UserCreate, UserUpdate
from core.security import get_password_hash, ACCESS_TOKEN_EXPIRE_MINUTES
from core.security import create_access_token, verify_password
from datetime import timedelta
from passlib.context import CryptContext
from core.schemas.users import UserCreate, UserUpdate, User, UserLogin
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from starlette.requests import Request

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = "HS256"
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return bcrypt_context.hash(password)


def get_user(db: Session, user_id: int):
    return db.query(UserModel).filter(UserModel.id == user_id).first()


def get_all(db: Session) -> List[User]:
    return db.query(UserModel).all()

def get_user_by_email(db: Session, email: str):
    return db.query(UserModel).filter(UserModel.email == email).first()


def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = UserModel(hashed_password=hashed_password, **user.dict(exclude={"password"}))
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
        return db_user
    except SQLAlchemyError as e:
        db.rollback()
        raise e


def update_user(db: Session, user_id: int, user: UserUpdate):
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    for var, value in vars(user).items():
        setattr(db_user, var, value) if value else None
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
        return db_user
    except SQLAlchemyError as e:
        db.rollback()
        raise e


def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    try:
        db.delete(db_user)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise e


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return False
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


async def get_current_user(request: Request):
    try:
        token = request.cookies.get("access_token")
        if token is None:
            return None
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            logout(request)
        return {"username": username, "id": user_id}
    except JWTError:
        raise HTTPException(status_code=404, detail="Not found")