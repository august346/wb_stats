from functools import wraps

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.exc import NoResultFound
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from sqlalchemy.sql import Select
from starlette import status

from db.config import Base
from db.models.user import User
from db.models.wb_api_key import WbApiKey


class NotFound(HTTPException):
    def __init__(self):
        super(NotFound, self).__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )


class EmailDuplicates(AssertionError):
    pass


class WbApiKeyDuplicates(AssertionError):
    pass


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
    async def _first(self, sel: Select):
        q = await self.db_session.execute(sel)
        return q.scalars().first()

    @raise_not_found
    async def _add(self, obj: Base):
        self.db_session.add(obj)
        return await self.db_session.flush()

    @raise_not_found
    async def _delete(self, obj: Base):
        await self.db_session.delete(obj)
        await self.db_session.flush()


class UserDAL(BaseDAL):
    async def _assert_not_exist(self, email: str):
        if await self._first(
            select(func.count()).filter(User.email == email)
        ):
            raise EmailDuplicates

    async def create(self, email: str, password: str):
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


class WbApiKeyDAL(BaseWithUserDal):
    async def _assert_not_exist(self, key: str):
        if await self._first(
            select(func.count()).filter(
                WbApiKey.user_id == self.user_id,
                WbApiKey.key == key
            )
        ):
            raise WbApiKeyDuplicates

    async def get(self, wb_api_key_id: int) -> WbApiKey:
        wb_api_key: WbApiKey = await self._first(
            select(WbApiKey).filter(
                WbApiKey.id == wb_api_key_id,
                WbApiKey.user_id == self.user_id
            )
        )

        if not wb_api_key:
            raise NotFound

        return wb_api_key

    async def create(self, name: str, key: str) -> WbApiKey:
        await self._assert_not_exist(key)

        new_wb_api_key = WbApiKey(user=self.user, name=name, key=key)
        await self._add(new_wb_api_key)

        return new_wb_api_key

    async def update(self, wb_api_key_id: int, name: str) -> WbApiKey:
        wb_api_key: WbApiKey = await self.get(wb_api_key_id)

        wb_api_key.name = name

        return wb_api_key

    async def delete(self, wb_api_key_id: int):
        wb_api_key = await self.get(wb_api_key_id)
        await self._delete(wb_api_key)

    async def list(self):
        return await self._all(
            select(WbApiKey).filter(
                WbApiKey.user_id == self.user_id
            )
        )
