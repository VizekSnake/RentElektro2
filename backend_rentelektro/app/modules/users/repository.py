from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy.orm import Session, selectinload

from app.modules.tools.models import Tool as ToolModel
from app.modules.users.models import (
    PasswordResetToken as PasswordResetTokenModel,
    User as UserModel,
)

USER_RESPONSE_LOAD_OPTIONS = (selectinload(UserModel.tools).selectinload(ToolModel.category),)


def get_by_id(db: Session, user_id: UUID) -> UserModel | None:
    return (
        db.query(UserModel)
        .options(*USER_RESPONSE_LOAD_OPTIONS)
        .filter(UserModel.id == user_id)
        .first()
    )


def get_by_email(db: Session, email: str) -> UserModel | None:
    return db.query(UserModel).filter(UserModel.email == email).first()


def get_by_username(db: Session, username: str) -> UserModel | None:
    return db.query(UserModel).filter(UserModel.username == username).first()


def list_all(db: Session) -> list[UserModel]:
    return db.query(UserModel).options(*USER_RESPONSE_LOAD_OPTIONS).all()


def get_password_reset_token_by_hash(
    db: Session, token_hash: str
) -> PasswordResetTokenModel | None:
    return (
        db.query(PasswordResetTokenModel)
        .filter(PasswordResetTokenModel.token_hash == token_hash)
        .first()
    )


def delete_password_reset_tokens_for_user(db: Session, user_id: UUID) -> None:
    (
        db.query(PasswordResetTokenModel)
        .filter(PasswordResetTokenModel.user_id == user_id)
        .delete(synchronize_session=False)
    )


def delete_expired_password_reset_tokens(db: Session) -> None:
    now = datetime.now(UTC)
    (
        db.query(PasswordResetTokenModel)
        .filter(PasswordResetTokenModel.expires_at < now)
        .delete(synchronize_session=False)
    )
