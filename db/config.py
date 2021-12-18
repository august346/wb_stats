from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_async_engine("postgresql+asyncpg://postgres:postgres@localhost/test", echo=True)


def _get_session_maker(**kwargs):
    return sessionmaker(engine, autoflush=False, **kwargs)


AsyncSessionMaker = _get_session_maker(expire_on_commit=False, class_=AsyncSession)
# SyncSessionMaker = _get_session_maker()

Base = declarative_base()
