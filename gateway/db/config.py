import os

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from config import settings

DB_URL = f"{settings.postgres}/{settings.db_name}"

engine = create_async_engine(DB_URL, echo=settings.debug)


def _get_session_maker(**kwargs):
    return sessionmaker(engine, autoflush=False, **kwargs)


AsyncSessionMaker = _get_session_maker(expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()
