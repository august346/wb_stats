from functools import wraps
from typing import Optional

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.exc import NoResultFound
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from sqlalchemy.sql import Select
from starlette import status

from db.config import Base
from db.models.user import User
from db.models.wb_api_key import UserWbApiKey, WbApiKey


class NotFound(HTTPException):
    def __init__(self):
        super(NotFound, self).__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )


class AlreadyExist(HTTPException):
    def __init__(self, **kwargs):
        model_name = self.model.__name__
        model_info = f"{model_name}({', '.join(f'{k}={v}' for k, v in kwargs.items())})"

        super(AlreadyExist, self).__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"That {model_name} already exist: {model_info}"
        )

    @property
    def model(self) -> Base:
        raise NotImplemented


class UserDuplicates(AlreadyExist):
    model = User


class UserWbApiKeyDuplicates(AlreadyExist):
    model = UserWbApiKey


def raise_not_found(f):
    @wraps(f)
    async def wrapper(*args, **kwargs):
        try:
            return await f(*args, **kwargs)
        except NoResultFound:
            raise NotFound

    return wrapper


class BaseDAL:
    db_session: Session

    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def _all(self, sel: Select):
        q = await self.db_session.execute(sel)
        return q.scalars().fetchall()

    @raise_not_found
    async def _first(self, sel: Select) -> Base:
        q = await self.db_session.execute(sel)
        return q.scalars().first()

    @raise_not_found
    async def _add(self, obj: Base):
        self.db_session.add(obj)
        await self.db_session.flush()

    @raise_not_found
    async def _delete(self, obj: Base):
        await self.db_session.delete(obj)
        await self.db_session.flush()

    async def _get_or_create(self, sel: Select, obj: Base) -> Base:
        old_instance: Optional[Base] = await self._first(sel)

        if old_instance:
            return old_instance

        await self._add(obj)
        return obj


class UserDAL(BaseDAL):
    async def _assert_not_exist(self, email: str):
        if await self._first(
                select(func.count()).filter(User.email == email)
        ):
            raise UserDuplicates(email=email)

    async def create(self, email: str, password: str) -> User:
        await self._assert_not_exist(email)

        new_user = User(email=email, password=password)
        await self._add(new_user)

        return new_user

    async def get(self, email: str) -> User:
        return await self._first(select(User).filter(User.email == email))


class BaseWithUserDal(BaseDAL):
    user: User

    def __init__(self, db_session: Session, user: User):
        super().__init__(db_session)
        self.user = user

    @property
    def user_id(self):
        return self.user.id


class UserWbApiKeyDAL(BaseWithUserDal):
    async def assert_not_exist(self, key: str):
        if await self._first(
                select(func.count()).filter(
                    UserWbApiKey.user_id == self.user_id,
                    UserWbApiKey.wb_api_key.has(key=key)
                )
        ):
            raise UserWbApiKeyDuplicates(key=key)

    async def _get_or_create_wb_api_key(self, key: str) -> WbApiKey:
        return await self._get_or_create(
            select(WbApiKey).filter_by(key=key),
            WbApiKey(key=key)
        )

    async def get(self, wb_api_key_id: int) -> WbApiKey:
        wb_api_key: UserWbApiKey = await self._first(
            select(UserWbApiKey).filter(
                UserWbApiKey.user_id == self.user_id,
                UserWbApiKey.wb_api_key.has(id=wb_api_key_id),
            )
        )

        if not wb_api_key:
            raise NotFound

        return wb_api_key

    async def create(self, name: str, key: str) -> WbApiKey:
        await self.assert_not_exist(key)

        wb_api_key = await self._get_or_create_wb_api_key(key)
        new_user_wb_api_key = UserWbApiKey(user_id=self.user_id, wb_api_key_id=wb_api_key.id, name=name)

        await self._add(new_user_wb_api_key)

        return new_user_wb_api_key

    async def update(self, user_wb_api_key_id: int, name: str) -> WbApiKey:
        user_wb_api_key: UserWbApiKey = await self.get(user_wb_api_key_id)

        user_wb_api_key.name = name
        await self._add(user_wb_api_key)

        return user_wb_api_key

    async def delete(self, wb_api_key_id: int) -> None:
        user_wb_api_key = await self.get(wb_api_key_id)
        await self._delete(user_wb_api_key)

        # TODO delete keys if no refs

    async def list(self):
        return await self._all(
            select(UserWbApiKey).filter(
                UserWbApiKey.user_id == self.user_id
            )
        )
