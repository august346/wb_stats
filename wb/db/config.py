from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from config import settings

DB_URL = f"{settings.postgres}/{settings.db_name}"

Base = declarative_base()


def get_engine_and_session_maker():
    eng = create_async_engine(DB_URL, echo=settings.debug)

    def _get_session_maker(**kwargs):
        return sessionmaker(eng, autoflush=False, **kwargs)

    session_maker = _get_session_maker(expire_on_commit=False, class_=AsyncSession)

    return eng, session_maker


engine, AsyncSessionMaker = get_engine_and_session_maker()
