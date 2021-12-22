import os
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    wb_base_url: str

    db_name: str = "api_wb"
    redis: str = os.environ.get("REDIS", "redis://localhost")
    postgres: str = os.environ.get("POSTGRES", "postgresql+asyncpg://postgres:postgres@localhost")

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
