import logging

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.modules.users import repository
from app.core.security import get_password_hash, verify_password
from app.modules.users.models import User as UserModel
from app.modules.users.schemas import UserCreate, UserUpdate

logger = logging.getLogger(__name__)


def create_user(db: Session, user: UserCreate) -> UserModel:
    logger.info("create_user_attempt email=%s username=%s", user.email, user.username)
    if repository.get_by_email(db, user.email):
        logger.warning("create_user_email_exists email=%s", user.email)
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user.password)
    db_user = UserModel(hashed_password=hashed_password, **user.model_dump(exclude={"password"}))
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
        logger.info("create_user_success user_id=%s username=%s", db_user.id, db_user.username)
        return db_user
    except IntegrityError as exc:
        db.rollback()
        message = str(exc.orig)
        if "username" in message:
            detail = "Nazwa użytkownika już istnieje"
        elif "email" in message:
            detail = "Adres email już istnieje"
        else:
            detail = "Błąd podczas tworzenia użytkownika"
        logger.warning("create_user_integrity_error email=%s detail=%s", user.email, detail)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail) from exc
    except SQLAlchemyError as exc:
        db.rollback()
        logger.exception("create_user_db_error email=%s", user.email)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from exc


def get_user_or_404(db: Session, user_id: int) -> UserModel:
    user = repository.get_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def list_users_or_404(db: Session) -> list[UserModel]:
    users = repository.list_all(db)
    if not users:
        raise HTTPException(status_code=404, detail="Users not found")
    return users


def update_user(db: Session, user_id: int, user_update: UserUpdate) -> UserModel:
    db_user = get_user_or_404(db, user_id)
    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    try:
        db.commit()
        db.refresh(db_user)
        return db_user
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from exc


def delete_user(db: Session, user_id: int) -> None:
    db_user = get_user_or_404(db, user_id)
    try:
        db.delete(db_user)
        db.commit()
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from exc


def authenticate_user(username: str, password: str, db: Session) -> UserModel | bool:
    logger.info("authenticate_user_attempt username=%s password_bytes=%s", username, len(password.encode("utf-8")))
    user = repository.get_by_username(db, username)
    if not user:
        logger.warning("authenticate_user_not_found username=%s", username)
        return False
    if not verify_password(password, user.hashed_password):
        logger.warning("authenticate_user_invalid_password username=%s", username)
        return False
    logger.info("authenticate_user_success user_id=%s username=%s", user.id, user.username)
    return user
