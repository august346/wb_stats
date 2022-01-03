import os
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "WB Stats API"
    admin_email: str
    support_email: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    url_wb_service: str = "http://localhost:1112"
    path_wb_service_init: str = "/init"
    path_wb_service_report: str = "/report"

    db_name: str = "api_gateway"
    postgres: str = os.environ.get("POSTGRES", "postgresql+asyncpg://postgres:postgres@localhost")

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
