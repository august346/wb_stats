from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from starlette import status

import base_models
import security
from config import settings
from db.dal import UserDAL, UserDuplicates
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


@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=base_models.User)
async def signup(
    email: EmailStr = Body(...),
    password: str = Body(..., regex=r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$'),
    user_dal: UserDAL = Depends(get_user_dal)
):
    try:
        return await user_dal.create(email, security.get_password_hash(password))
    except UserDuplicates:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This email already exists")
