from datetime import timedelta, datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

import security
from config import settings
from db.dal import UserDAL, EmailDuplicates
from dependencies import get_user_dal

router = APIRouter()


@router.post("/token", response_model=security.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await security.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = security.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(email: str, password: str, user_dal: UserDAL = Depends(get_user_dal)):
    try:
        await user_dal.create_user(email, security.get_password_hash(password))
    except EmailDuplicates:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This email already exists")
