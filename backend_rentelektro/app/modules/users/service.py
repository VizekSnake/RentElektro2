import logging
from datetime import UTC, datetime, timedelta
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.email import OutboundEmail, get_email_sender
from app.core.model_utils import apply_update
from app.core.security import (
    generate_password_reset_token,
    get_password_hash,
    hash_password_reset_token,
    verify_password,
)
from app.modules.users import repository
from app.modules.users.models import (
    PasswordResetToken as PasswordResetTokenModel,
    User as UserModel,
)
from app.modules.users.schemas import (
    AccountAnonymizeRequest,
    PasswordChangeRequest,
    PasswordResetConfirmRequest,
    PasswordResetRequest,
    UserCreate,
    UserUpdate,
)

logger = logging.getLogger(__name__)
settings = get_settings()


def validate_password_strength(password: str) -> None:
    if len(password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nowe haslo musi miec co najmniej 8 znakow.",
        )


def build_password_reset_link(token: str) -> str:
    parsed = urlsplit(settings.PASSWORD_RESET_URL_BASE)
    query = dict(parse_qsl(parsed.query, keep_blank_values=True))
    query["token"] = token
    return urlunsplit(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            urlencode(query),
            parsed.fragment,
        )
    )


def send_password_reset_message(recipient: str, reset_link: str) -> None:
    expiry_minutes = settings.PASSWORD_RESET_TOKEN_EXPIRE_MINUTES
    message = OutboundEmail(
        recipient=recipient,
        subject="RentElektro - reset hasla",
        text_body=(
            "Otrzymalismy prosbe o reset hasla do konta RentElektro.\n\n"
            f"Link do ustawienia nowego hasla (wazny {expiry_minutes} minut):\n"
            f"{reset_link}\n\n"
            "Jesli to nie Ty inicjowales tej operacji, zignoruj te wiadomosc."
        ),
    )
    get_email_sender().send(message)


def is_expired(expires_at: datetime, now: datetime) -> bool:
    comparable_expiry = expires_at
    if comparable_expiry.tzinfo is None:
        comparable_expiry = comparable_expiry.replace(tzinfo=UTC)
    return comparable_expiry < now


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


def get_user_or_404(db: Session, user_id: UUID) -> UserModel:
    user = repository.get_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def list_users_or_404(db: Session) -> list[UserModel]:
    users = repository.list_all(db)
    if not users:
        raise HTTPException(status_code=404, detail="Users not found")
    return users


def update_user(db: Session, user_id: UUID, user_update: UserUpdate) -> UserModel:
    db_user = get_user_or_404(db, user_id)
    apply_update(db_user, user_update)
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


def delete_user(db: Session, user_id: UUID) -> None:
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


def change_password(db: Session, user_id: UUID, payload: PasswordChangeRequest) -> None:
    user = get_user_or_404(db, user_id)
    if not verify_password(payload.current_password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Aktualne hasło jest nieprawidłowe."
        )

    validate_password_strength(payload.new_password)
    user.hashed_password = get_password_hash(payload.new_password)
    try:
        db.commit()
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from exc


def anonymize_user(db: Session, user_id: UUID, payload: AccountAnonymizeRequest) -> None:
    user = get_user_or_404(db, user_id)
    if not verify_password(payload.current_password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Aktualne hasło jest nieprawidłowe."
        )

    suffix = f"{user.id}-{int(datetime.now(UTC).timestamp())}"
    user.email = f"anon-{suffix}@deleted.rentelektro.app"
    user.username = f"anon_{suffix}"
    user.firstname = "Usunięte"
    user.lastname = "Konto"
    user.phone = ""
    user.company = False
    user.profile_picture = None
    user.role = None
    user.is_active = False
    user.hashed_password = get_password_hash(f"deleted-account-{suffix}")

    try:
        db.commit()
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from exc


def request_password_reset(db: Session, payload: PasswordResetRequest) -> None:
    logger.info("password_reset_request email=%s", payload.email)
    repository.delete_expired_password_reset_tokens(db)
    user = repository.get_by_email(db, str(payload.email))
    if user is None or not user.is_active:
        db.commit()
        return

    raw_token = generate_password_reset_token()
    token_hash = hash_password_reset_token(raw_token)
    expires_at = datetime.now(UTC) + timedelta(minutes=settings.PASSWORD_RESET_TOKEN_EXPIRE_MINUTES)
    reset_token = PasswordResetTokenModel(
        user_id=user.id,
        token_hash=token_hash,
        expires_at=expires_at,
    )

    repository.delete_password_reset_tokens_for_user(db, user.id)
    db.add(reset_token)

    try:
        db.commit()
    except SQLAlchemyError as exc:
        db.rollback()
        logger.exception("password_reset_request_db_error email=%s", payload.email)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from exc

    reset_link = build_password_reset_link(raw_token)
    send_password_reset_message(user.email, reset_link)


def confirm_password_reset(db: Session, payload: PasswordResetConfirmRequest) -> None:
    validate_password_strength(payload.new_password)

    token_hash = hash_password_reset_token(payload.token)
    reset_token = repository.get_password_reset_token_by_hash(db, token_hash)
    now = datetime.now(UTC)
    if reset_token is None or is_expired(reset_token.expires_at, now):
        if reset_token is not None:
            db.delete(reset_token)
            db.commit()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nieprawidlowy lub wygasly link do resetu hasla.",
        )

    user = repository.get_by_id(db, reset_token.user_id)
    if user is None or not user.is_active:
        repository.delete_password_reset_tokens_for_user(db, reset_token.user_id)
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nieprawidlowy lub wygasly link do resetu hasla.",
        )

    user.hashed_password = get_password_hash(payload.new_password)
    repository.delete_password_reset_tokens_for_user(db, user.id)

    try:
        db.commit()
    except SQLAlchemyError as exc:
        db.rollback()
        logger.exception("password_reset_confirm_db_error user_id=%s", user.id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from exc


def authenticate_user(username: str, password: str, db: Session) -> UserModel | None:
    logger.info(
        "authenticate_user_attempt username=%s password_bytes=%s",
        username,
        len(password.encode("utf-8")),
    )
    user = repository.get_by_username(db, username)
    if not user:
        logger.warning("authenticate_user_not_found username=%s", username)
        return None
    if not verify_password(password, user.hashed_password):
        logger.warning("authenticate_user_invalid_password username=%s", username)
        return None
    logger.info("authenticate_user_success user_id=%s username=%s", user.id, user.username)
    return user
