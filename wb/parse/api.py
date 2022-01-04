import asyncio
import dataclasses
import http
import logging
from datetime import date, datetime, timedelta
from functools import cached_property, reduce
from typing import AsyncGenerator, Any

import aiohttp

from config import settings
from utils import redis

SALE_REPORT = "reportDetailByPeriod"


class ParseError(RuntimeError):
    pass


@dataclasses.dataclass
class SaleReportGetter:
    session: aiohttp.ClientSession
    key: str
    date_from: date
    date_to: date
    limit: int = 1_000

    @property
    def url(self) -> str:
        return f"/api/v1/supplier/{SALE_REPORT}"

    @cached_property
    def _base_params(self) -> dict:
        return dict(
            key=self.key,
            limit=self.limit,
            dateFrom=self.date_from.isoformat(),
            dateTo=self.date_to.isoformat(),
        )

    def req_params(self, from_id: int):
        return self._base_params | dict(rrdid=from_id)

    async def get_sale_reports(
        self,
        id_from: int,
        max_attempts: int = 3,
        pause_between: float = 0
    ) -> AsyncGenerator[list, Any]:
        attempts: int = max_attempts
        while id_from != -1 and attempts > 0:
            async with self.session.get(self.url, params=self.req_params(id_from)) as resp:
                if resp.status == http.HTTPStatus.OK:
                    attempts = max_attempts
                    data = (await resp.json())
                    yield data
                    id_from = reduce(lambda a, b: max(a, b["rrd_id"]), data, id_from) if data else -1
                else:
                    logging.warning(resp)
                    attempts -= 1
                if pause_between:
                    await asyncio.sleep(pause_between)
        if attempts == 0:
            raise ParseError("Failed requests")

    async def is_api_key_valid(self) -> bool:
        origin_limit, self.limit = self.limit, 1
        try:
            async for _ in self.get_sale_reports(id_from=0, max_attempts=3, pause_between=1):
                return True
        except ParseError:
            pass
        finally:
            self.limit = origin_limit

        return False


async def get_storage(key: str) -> dict[str, dict]:
    if cached := await redis.Storage.get(key):
        return cached

    async with aiohttp.ClientSession(base_url=settings.wb_base_url) as session:
        url: str = '/api/v1/supplier/stocks'
        date_from: str = (datetime.utcnow() - timedelta(days=2)).isoformat()
        params: dict = dict(key=key, dateFrom=date_from)
        for _ in range(3):
            async with session.get(url, params=params) as resp:
                if resp.status != http.HTTPStatus.OK:
                    await asyncio.sleep(0.3)
                else:
                    rows: list[dict] = await resp.json()
                    data = {r["nmId"]: r for r in rows}

                    await redis.Storage.set(key, data, None if data else 60)
                    return data
