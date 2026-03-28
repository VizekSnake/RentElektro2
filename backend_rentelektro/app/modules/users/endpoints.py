import os
from datetime import timedelta

from fastapi import APIRouter, Body, Depends, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from app.modules.users import service as users_service
from app.core.dependencies import get_db
from app.modules.users.schemas import (
    AccountAnonymizeRequest,
    PasswordChangeRequest,
    RefreshTokenRequest,
    Token,
    User,
    UserCreate,
    UserUpdate,
)
from app.core.security import (
    ACCESS_TOKEN_EXPIRE_MINUTES as EXPIRE_DELTA,
    create_access_token,
    create_refresh_token,
    get_access_token,
    oauth2_scheme,
    verify_token,
)
from typing import List

router = APIRouter(prefix="/users", tags=["users"])
COOKIE_SECURE = os.getenv("COOKIE_SECURE", "false").lower() == "true"


def set_auth_cookies(response: Response, access_token: str, refresh_token: str) -> None:
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=COOKIE_SECURE,
        samesite="lax",
        max_age=EXPIRE_DELTA * 60,
        path="/",
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=COOKIE_SECURE,
        samesite="lax",
        max_age=7 * 24 * 60 * 60,
        path="/",
    )


def clear_auth_cookies(response: Response) -> None:
    response.delete_cookie(key="access_token", path="/")
    response.delete_cookie(key="refresh_token", path="/")


@router.post("/register", response_model=User)
async def register_user(user: UserCreate, db: Session = Depends(get_db)) -> User:
    return users_service.create_user(db=db, user=user)


@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 db: Session = Depends(get_db)):
    user = users_service.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token({"username": user.username, "id": user.id},
                                       expires_delta=timedelta(minutes=EXPIRE_DELTA))
    refresh_token = create_refresh_token({"username": user.username, "id": user.id})
    response = JSONResponse(content={"token_type": "bearer", "authenticated": True})
    set_auth_cookies(response, access_token, refresh_token)
    return response


@router.post("/login", response_model=dict)
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
                db: Session = Depends(get_db)):
    user = users_service.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token({"username": user.username, "id": user.id},
                                       expires_delta=timedelta(minutes=EXPIRE_DELTA))

    response = JSONResponse(content={"token_type": "bearer", "authenticated": True})
    set_auth_cookies(response, access_token, create_refresh_token({"username": user.username, "id": user.id}))
    return response


@router.get("/me")
def read_users_me(access_token: str = Depends(get_access_token)) -> dict:
    payload = verify_token(access_token)
    return {"username": payload["username"], "id": payload["id"]}


@router.get("/me/data")
def read_current_user_data(access_token: str = Depends(get_access_token), db: Session = Depends(get_db)) -> JSONResponse:
    payload = verify_token(access_token)
    if not payload:
        raise HTTPException(detail='Could not validate credentials', status_code=404)
    db_user = users_service.get_user_or_404(db, user_id=payload["id"])
    response = JSONResponse(content={
        "email": db_user.email,
        "lastname": db_user.lastname,
        "phone": db_user.phone,
        "profile_picture": db_user.profile_picture,
        "is_active": db_user.is_active,
        "username": db_user.username,
        "firstname": db_user.firstname,
        "company": db_user.company,
        "role": db_user.role,
        "id": db_user.id
    })
    return response


@router.get("/user/{user_id}", response_model=User)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    return users_service.get_user_or_404(db, user_id=user_id)


@router.get("/all", response_model=List[User] | None)
async def get_all_users(db: Session = Depends(get_db)):
    return users_service.list_users_or_404(db)


@router.patch("/user/{user_id}", response_model=User)
async def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    return users_service.update_user(db=db, user_id=user_id, user_update=user)


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


@router.delete("/delete/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    users_service.delete_user(db=db, user_id=user_id)


@router.post("/refresh", response_model=Token)
def refresh_access_token(
    response: Response,
    request: Request,
    payload: RefreshTokenRequest | None = Body(default=None),
):
    refresh_token = payload.refresh_token if payload else request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing refresh token")
    payload = verify_token(refresh_token)
    new_access_token = create_access_token(data={"username": payload["username"], "id": payload["id"]})
    new_refresh_token = create_refresh_token(data={"username": payload["username"], "id": payload["id"]})
    set_auth_cookies(response, new_access_token, new_refresh_token)
    return {"access_token": new_access_token, "refresh_token": new_refresh_token, "token_type": "bearer"}


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(response: Response):
    clear_auth_cookies(response)
