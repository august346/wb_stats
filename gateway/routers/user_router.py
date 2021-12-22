from fastapi import APIRouter, Depends

import base_models
from db.models.user import User
from dependencies import get_current_active_user

router = APIRouter()


@router.get("/users/me/", response_model=base_models.User)
async def get_me(current_user: User = Depends(get_current_active_user)):
    return current_user
