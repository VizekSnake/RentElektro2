from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from core.dependencies import get_db
from core.security import get_current_user
from crud import crud_user
from core.schemas.users import UserCreate, UserUpdate, User, UserLogin
from core.security import create_access_token, get_user_exception, token_exception
from typing import List, Optional
from core.database import SessionLocal
from starlette.requests import Request
from starlette.responses import Response, HTMLResponse, RedirectResponse
from core.security import ACCESS_TOKEN_EXPIRE_MINUTES as EXPIRE_DELTA
from crud.crud_user import authenticate_user

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
        raise token_exception()
    token = create_access_token({"username": user.username, "id": user.id},
                                expires_delta=timedelta(minutes=EXPIRE_DELTA))

    return {"access_token": token, "token_type": "bearer"}

# @router.post("/login")
# async def login(response: RedirectResponse, form_data: OAuth2PasswordRequestForm = Depends(),
#                 db: Session = Depends(get_db)):
#     user_data = authenticate_user(form_data.username, form_data.password, db)
#     if not user_data:
#         return JSONResponse(content={"message": "Invalid credentials"}, status_code=status.HTTP_401_UNAUTHORIZED)
#
#     user = user_data
#     access_token = create_access_token({"username": user.username, "id": user.id},
#                                        expires_delta=timedelta(minutes=EXPIRE_DELTA))
#     response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
#     response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True)
#     return response

@router.post("/login", response_model=dict)
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
                db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token({"username": user.username, "id": user.id},
                                       expires_delta=timedelta(minutes=EXPIRE_DELTA))

    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)

    response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True)
    print(f'access_token: {access_token},{user.username}, logged succesfully :)')
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

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

