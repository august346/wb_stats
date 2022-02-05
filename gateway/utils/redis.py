import datetime
import json
from typing import Any, Optional, Union

import aioredis

from config import settings


_redis = aioredis.from_url(settings.redis)


async def _set_value(key: str, value: Any, ex: int):
    return await _redis.set(key, value, ex=ex)


async def _get_value(key: str):
    return await _redis.get(key)


class _BaseRedis:
    _ex: int = 3600*24

    @classmethod
    def _get_key(cls, k: str) -> str:
        return f"gw-{cls._get_sub_key()}-{k}"

    @staticmethod
    def _get_sub_key() -> str:
        raise NotImplementedError()

    @classmethod
    async def set(cls, key: str, data: Union[list, dict], ex: Optional[int] = None):
        value: str = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
        return await _set_value(cls._get_key(key), value, ex=cls._ex if ex is None else ex)

    @classmethod
    async def get(cls, key: str):
        value: Optional[str] = await _get_value(cls._get_key(key))
        return value and json.loads(value)


class History(_BaseRedis):
    _MAX_RANGE: int = 5

    _ex: int = 3600*24*7

    @staticmethod
    def _get_sub_key() -> str:
        return 'history'

    @staticmethod
    def _get_item_key(user_id: int, wak_id: int) -> str:
        return f'{user_id}-{wak_id}'

    @classmethod
    async def get_sale_reports(cls, user_id: int, wak_id: int) -> list:
        return await cls.get(cls._get_item_key(user_id, wak_id)) or []

    @classmethod
    async def add_sale_reports(
        cls, user_id: int, wak_id: int, d_from: datetime.date, d_to: datetime.date, brands: list[str]
    ) -> list[dict]:
        new_row: dict = {'date_from': d_from.isoformat(), 'date_to': d_to.isoformat(), 'brands': brands}

        history: list = await cls.get_sale_reports(user_id, wak_id)

        if new_row in history:
            history.remove(new_row)

        history.append(new_row)

        new_history: list[dict] = history[-cls._MAX_RANGE:]

        await cls.set(cls._get_item_key(user_id, wak_id), new_history)

        return new_history
