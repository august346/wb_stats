import asyncio
from datetime import date

import aiohttp

from config import settings
from db.config import get_engine_and_session_maker
from db.dal import SaleReportDAL
from parse.api import SaleReportGetter
from utils.collector import Collector


async def _a_collect_rows(api_key: str, date_from: date, date_to: date):
    async with aiohttp.ClientSession(base_url=settings.wb_base_url) as http_session:
        sri = SaleReportGetter(
            key=api_key,
            date_from=date_from,
            date_to=date_to,
            session=http_session,
        )

        _, session_maker = get_engine_and_session_maker()

        async with session_maker() as db_session:
            sr_dal = SaleReportDAL(db_session)

            await Collector(sri=sri, sr_dal=sr_dal).run()


def collect_rows(api_key: str, date_from: date, date_to: date):
    new_loop = asyncio.new_event_loop()
    new_loop.run_until_complete(_a_collect_rows(api_key, date_from, date_to))
    new_loop.close()


def create_report(api_key: str, date_from: date, date_to: date):
    ...
