from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from core.dependencies import get_db
from core.security import get_current_user
from crud import crud_user
from core.schemas.users import UserCreate, UserUpdate, User, UserLogin, Token
from core.security import oauth2_scheme, create_access_token, create_refresh_token, verify_token, get_user_exception, \
    token_exception
from typing import List, Optional
from core.database import SessionLocal
from starlette.requests import Request
from starlette.responses import Response, HTMLResponse, RedirectResponse
from core.security import ACCESS_TOKEN_EXPIRE_MINUTES as EXPIRE_DELTA
from core.security import REFRESH_TOKEN_EXPIRE_DAYS  as REFRESH_DELTA

from crud.crud_user import authenticate_user

from core.schemas.users import RefreshTokenRequest

router = APIRouter(prefix="/api/users", tags=["users"])


@router.post("/register", response_model=User)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud_user.create_user(db=db, user=user)


@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token({"username": user.username, "id": user.id},
                                       expires_delta=timedelta(minutes=EXPIRE_DELTA))
    refresh_token = create_refresh_token({"username": user.username, "id": user.id})
    print(f"Refresh token: {refresh_token}")
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post("/login", response_model=dict)
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
                db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token({"username": user.username, "id": user.id},
                                       expires_delta=timedelta(minutes=EXPIRE_DELTA))

    response = JSONResponse(content={"access_token": access_token, "token_type": "bearer"})
    response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True)
    return response


# @router.get("/me")
# def read_users_me(access_token: str = Depends(oauth2_scheme)):
#     payload = verify_token(access_token)
#     return {"username": payload.username}

@router.get("/me")
def read_users_me(access_token: str = Depends(oauth2_scheme)):
    payload = verify_token(access_token)
    return {"username": payload["username"], "id": payload["id"]}


@router.get("/user/{user_id}", response_model=User)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud_user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/all", response_model=List[User] | None)
async def get_all_users(db: Session = Depends(get_db)):
    users = crud_user.get_all(db)  # Assuming crud_user has a get_all function
    if users:
        return users
    else:
        raise HTTPException(404, "Users not found")


@router.patch("/user/{user_id}", response_model=User)
async def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud_user.update_user(db=db, user_id=user_id, user=user)


@router.delete("/delete/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud_user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    crud_user.delete_user(db=db, user_id=user_id)
    return {"ok": True}


# @router.post("/refresh", response_model=Token)
# def refresh_access_token(refresh_token: str):
#     print(refresh_token)
#     payload = verify_token(refresh_token)
#     new_access_token = create_access_token(data={**payload.dict()})
#     new_refresh_token = create_refresh_token(data={**payload.dict()})
#     return {"access_token": new_access_token, "refresh_token": new_refresh_token, "token_type": "bearer"}

@router.post("/refresh", response_model=Token)
def refresh_access_token(request: RefreshTokenRequest):
    refresh_token = request.refresh_token
    payload = verify_token(refresh_token)
    new_access_token = create_access_token(data={"username": payload["username"], "id": payload["id"]})
    print(new_access_token)
    new_refresh_token = create_refresh_token(data={"username": payload["username"], "id": payload["id"]})

    return {"access_token": new_access_token, "refresh_token": new_refresh_token, "token_type": "bearer"}