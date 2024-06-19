import os

from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session
from users.models import User as UserModel
from core.security import get_password_hash, get_db
from core.security import  verify_password
from passlib.context import CryptContext
from users.schemas import UserCreate, UserUpdate, User
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import HTTPException, status

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


def get_user_by_username(db: Session, username: str):
    return db.query(UserModel).filter(UserModel.username == username).first()

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = UserModel(hashed_password=hashed_password, **user.model_dump(exclude={"password"}))
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError as e:
        db.rollback()
        if "ix_users_username" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nazwa użytkownika już istnieje"
            )
        elif "ix_users_email" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Adres email już istnieje"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Błąd podczas tworzenia użytkownika"
            )
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )



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


def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(UserModel)\
        .filter(UserModel.username == username)\
        .first()

    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
