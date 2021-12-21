import json
import os
from typing import Any, Optional

import aioredis

REDIS_URL: str = os.environ.get("REDIS_URL", "redis://localhost")

_redis = aioredis.from_url(REDIS_URL)


async def _set_value(key: str, value: Any, ex: int):
    return await _redis.set(key, value, ex=ex)


async def _get_value(key: str):
    return await _redis.get(key)


class Storage:
    _ex: int = 60*60*3

    @staticmethod
    def _get_key(k: str) -> str:
        return f"storage-{k}"

    @classmethod
    async def set(cls, key: str, items: dict[str, dict]):
        value: str = json.dumps(items, separators=(",", ":"), ensure_ascii=False)
        return await _set_value(cls._get_key(key), value, ex=cls._ex)

    @classmethod
    async def get(cls, key: str):
        value: Optional[str] = await _get_value(cls._get_key(key))
        return value and json.loads(value)
