from fastapi import APIRouter, Depends

from db.dal import UserDAL
from db.models.user import User
from dependencies import get_user_dal, get_current_active_user

router = APIRouter()


@router.get("/users/me/")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "disabled": current_user.disabled,
    }


@router.post("/users")
async def create_user(email: str, password: str, user_dal: UserDAL = Depends(get_user_dal)):
    return await user_dal.create_user(email, password)


@router.get("/users")
async def get_user(email: str, user_dal: UserDAL = Depends(get_user_dal)) -> User:
    return await user_dal.get_user(email)
