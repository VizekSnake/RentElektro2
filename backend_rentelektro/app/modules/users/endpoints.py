from datetime import timedelta
from uuid import UUID

from fastapi import APIRouter, Body, Depends, HTTPException, Request, Response, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.dependencies import get_db
from app.core.security import (
    ACCESS_TOKEN_EXPIRE_MINUTES as EXPIRE_DELTA,
    create_access_token,
    create_refresh_token,
    get_access_token,
    verify_token,
)
from app.modules.users import service as users_service
from app.modules.users.models import User as UserModel
from app.modules.users.schemas import (
    AccountAnonymizeRequest,
    LoginResult,
    MessageResponse,
    PasswordChangeRequest,
    PasswordResetConfirmRequest,
    PasswordResetRequest,
    RefreshTokenRequest,
    Token,
    User as UserResponse,
    UserCreate,
    UserProfile,
    UserUpdate,
)

router = APIRouter(prefix="/users", tags=["users"])
settings = get_settings()


def set_auth_cookies(response: Response, access_token: str, refresh_token: str) -> None:
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite="lax",
        max_age=EXPIRE_DELTA * 60,
        path="/",
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite="lax",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        path="/",
    )


def clear_auth_cookies(response: Response) -> None:
    response.delete_cookie(key="access_token", path="/")
    response.delete_cookie(key="refresh_token", path="/")


def create_login_response(user: UserModel) -> JSONResponse:
    access_token = create_access_token(
        {"username": user.username, "id": user.id},
        expires_delta=timedelta(minutes=EXPIRE_DELTA),
    )
    refresh_token = create_refresh_token({"username": user.username, "id": user.id})
    response = JSONResponse(LoginResult(authenticated=True, token_type="bearer").model_dump())
    set_auth_cookies(response, access_token, refresh_token)
    return response


@router.post("", response_model=UserResponse)
async def register_user(user: UserCreate, db: Session = Depends(get_db)) -> UserModel:
    return users_service.create_user(db=db, user=user)


@router.post("/token", response_model=LoginResult)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = users_service.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return create_login_response(user)


@router.post("/login", response_model=LoginResult)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = users_service.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return create_login_response(user)


@router.get("/me")
def read_users_me(access_token: str = Depends(get_access_token)) -> dict:
    payload = verify_token(access_token)
    return {"username": payload["username"], "id": payload["id"]}


@router.get("/me/data", response_model=UserProfile)
def read_current_user_data(
    access_token: str = Depends(get_access_token), db: Session = Depends(get_db)
) -> UserProfile:
    payload = verify_token(access_token)
    db_user = users_service.get_user_or_404(db, user_id=payload["id"])
    return UserProfile.model_validate(db_user, from_attributes=True)


@router.get("", response_model=list[UserResponse] | None)
async def get_all_users(db: Session = Depends(get_db)) -> list[UserModel]:
    return users_service.list_users_or_404(db)


@router.post(
    "/password-reset/request",
    response_model=MessageResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def request_password_reset(
    payload: PasswordResetRequest, db: Session = Depends(get_db)
) -> MessageResponse:
    users_service.request_password_reset(db=db, payload=payload)
    return MessageResponse(
        message="Jesli konto z tym adresem istnieje, link do resetu hasla zostal wygenerowany."
    )


@router.post("/password-reset/confirm", response_model=MessageResponse)
async def confirm_password_reset(
    payload: PasswordResetConfirmRequest, db: Session = Depends(get_db)
) -> MessageResponse:
    users_service.confirm_password_reset(db=db, payload=payload)
    return MessageResponse(message="Haslo zostalo zresetowane.")


@router.post("/me/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_current_user_password(
    payload: PasswordChangeRequest,
    db: Session = Depends(get_db),
    access_token: str = Depends(get_access_token),
):
    current_user = read_users_me(access_token)
    users_service.change_password(db=db, user_id=current_user["id"], payload=payload)


@router.post("/me/anonymize", status_code=status.HTTP_204_NO_CONTENT)
async def anonymize_current_user(
    payload: AccountAnonymizeRequest,
    response: Response,
    db: Session = Depends(get_db),
    access_token: str = Depends(get_access_token),
):
    current_user = read_users_me(access_token)
    users_service.anonymize_user(db=db, user_id=current_user["id"], payload=payload)
    clear_auth_cookies(response)


@router.post("/refresh", response_model=Token)
def refresh_access_token(
    response: Response,
    request: Request,
    payload: RefreshTokenRequest | None = Body(default=None),
) -> Token:
    refresh_token = payload.refresh_token if payload else request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing refresh token"
        )
    token_payload = verify_token(refresh_token)
    new_access_token = create_access_token(
        data={"username": token_payload["username"], "id": token_payload["id"]}
    )
    new_refresh_token = create_refresh_token(
        data={"username": token_payload["username"], "id": token_payload["id"]}
    )
    set_auth_cookies(response, new_access_token, new_refresh_token)
    return Token(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
        token_type="bearer",
    )


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(response: Response):
    clear_auth_cookies(response)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: UUID, db: Session = Depends(get_db)) -> UserModel:
    return users_service.get_user_or_404(db, user_id=user_id)


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(user_id: UUID, user: UserUpdate, db: Session = Depends(get_db)) -> UserModel:
    return users_service.update_user(db=db, user_id=user_id, user_update=user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: UUID, db: Session = Depends(get_db)):
    users_service.delete_user(db=db, user_id=user_id)
