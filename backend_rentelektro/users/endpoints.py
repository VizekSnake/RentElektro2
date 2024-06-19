from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from core.dependencies import get_db
from users.schemas import UserCreate, UserUpdate, User, Token, RefreshTokenRequest
from core.security import oauth2_scheme, create_access_token, create_refresh_token, verify_token
from typing import List
from core.security import ACCESS_TOKEN_EXPIRE_MINUTES as EXPIRE_DELTA

import users.handlers

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=User)
async def register_user(user: UserCreate, db: Session = Depends(get_db)) -> User:
    db_user = users.handlers.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return users.handlers.create_user(db=db, user=user)


@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 db: Session = Depends(get_db)):
    user = users.handlers.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token({"username": user.username, "id": user.id},
                                       expires_delta=timedelta(minutes=EXPIRE_DELTA))
    refresh_token = create_refresh_token({"username": user.username, "id": user.id})
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post("/login", response_model=dict)
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
                db: Session = Depends(get_db)):
    user = users.handlers.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token({"username": user.username, "id": user.id},
                                       expires_delta=timedelta(minutes=EXPIRE_DELTA))

    response = JSONResponse(content={"access_token": access_token, "token_type": "bearer"})
    response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True)
    return response


@router.get("/me")
def read_users_me(access_token: str = Depends(oauth2_scheme)) -> dict:
    payload = verify_token(access_token)
    return {"username": payload["username"], "id": payload["id"]}


@router.get("/me/data")
def read_current_user_data(access_token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> JSONResponse:
    payload = verify_token(access_token)
    if not payload:
        raise HTTPException(detail='Could not validate credentials', status_code=404)
    db_user = users.handlers.get_user(db, user_id=payload["id"])
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
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
    db_user = users.handlers.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/all", response_model=List[User] | None)
async def get_all_users(db: Session = Depends(get_db)):
    users = users.handlers.get_all(db)  # Assuming crud_user has a get_all function
    if users:
        return users
    else:
        raise HTTPException(404, "Users not found")


@router.patch("/user/{user_id}", response_model=User)
async def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return users.handlers.update_user(db=db, user_id=user_id, user=user)


@router.delete("/delete/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    delete_user(db=db, user_id=user_id)
    return {"ok": True}


@router.post("/refresh", response_model=Token)
def refresh_access_token(request: RefreshTokenRequest):
    refresh_token = request.refresh_token
    payload = verify_token(refresh_token)
    new_access_token = create_access_token(data={"username": payload["username"], "id": payload["id"]})
    new_refresh_token = create_refresh_token(data={"username": payload["username"], "id": payload["id"]})

    return {"access_token": new_access_token, "refresh_token": new_refresh_token, "token_type": "bearer"}
