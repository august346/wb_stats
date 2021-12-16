from typing import Optional

from sqlalchemy import func
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from db.models.user import User


class EmailDuplicates(AssertionError):
    pass


class BaseDAL:
    db_session: Session

    def __init__(self, db_session: Session):
        self.db_session = db_session


class UserDAL(BaseDAL):
    async def create_user(self, email: str, password: str):
        await self._assert_email_not_exist(email)

        new_user = User(email=email, password=password)
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user

    async def _assert_email_not_exist(self, email: str):
        q = await self.db_session.execute(
            select(func.count()).filter(User.email == email)
        )
        if q.scalars().first():
            raise EmailDuplicates

    async def get_user(self, email: str) -> Optional[User]:
        q = await self.db_session.execute(
            select(User).filter(User.email == email)
        )
        return q.scalars().first()
