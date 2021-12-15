from fastapi import APIRouter, Depends

from db.dal import UserDAL
from db.models.user import User
from dependencies import get_user_dal

router = APIRouter()


@router.post("/users")
async def create_user(email: str, password: str, user_dal: UserDAL = Depends(get_user_dal)):
    return await user_dal.create_user(email, password)


@router.get("/users")
async def get_user(email: str, user_dal: UserDAL = Depends(get_user_dal)) -> User:
    return await user_dal.get_user(email)
