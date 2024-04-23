from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from core.dependencies import get_db
from crud import crud_user
from core.schemas.users import UserCreate, UserUpdate, User, UserLogin
from core.security import create_access_token
from typing import List
from core.database import SessionLocal
from starlette.responses import Response

router = APIRouter(prefix="/api/users", tags=["users"])


@router.post("/register", response_model=User)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud_user.create_user(db=db, user=user)


@router.post("/login", response_class=JSONResponse)
async def login_user(user_login: UserLogin, db: Session = Depends(get_db)):
    db_user = crud_user.authenticate_user(db, email=user_login.email, password=user_login.password)
    if not db_user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user_login.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud_user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/all", response_model=List[User] | None)
async def get_all_users(db: Session = Depends(get_db)):
    users = crud_user.get_all(db)  # Assuming crud_user has a get_all function
    if users:
        return print(users)
    else:
        raise HTTPException(404, "Users not found")


@router.patch("/{user_id}", response_model=User)
async def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud_user.update_user(db=db, user_id=user_id, user=user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud_user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    crud_user.delete_user(db=db, user_id=user_id)
    return {"ok": True}


@router.post("/token")
async def login_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends(),
                                 db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return False
    token_expires = timedelta(minutes=60)
    token = create_access_token(user.username,
                                user.id,
                                expires_delta=token_expires)

    response.set_cookie(key="access_token", value=token, httponly=True)

    return True
