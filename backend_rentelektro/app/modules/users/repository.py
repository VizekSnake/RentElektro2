from sqlalchemy.orm import Session

from app.modules.users.models import User as UserModel


def get_by_id(db: Session, user_id: int) -> UserModel | None:
    return db.query(UserModel).filter(UserModel.id == user_id).first()


def get_by_email(db: Session, email: str) -> UserModel | None:
    return db.query(UserModel).filter(UserModel.email == email).first()


def get_by_username(db: Session, username: str) -> UserModel | None:
    return db.query(UserModel).filter(UserModel.username == username).first()


def list_all(db: Session) -> list[UserModel]:
    return db.query(UserModel).all()
