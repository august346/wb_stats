from fastapi import Depends, HTTPException

from db.config import AsyncSessionMaker
from db.dal import UserDAL, WbApiKeyDAL
from db.models.user import User
from security import get_current_user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_user_dal():
    async with AsyncSessionMaker() as session:
        async with session.begin():
            yield UserDAL(session)


async def get_wb_api_key_dal(current_user: User = Depends(get_current_active_user)):
    async with AsyncSessionMaker() as session:
        async with session.begin():
            yield WbApiKeyDAL(session, current_user)
