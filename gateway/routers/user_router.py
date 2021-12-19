from fastapi import APIRouter, Depends

from db.models.user import User
from dependencies import get_current_active_user

router = APIRouter()


@router.get("/users/me/")
async def get_me(current_user: User = Depends(get_current_active_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "disabled": current_user.disabled,
    }
