from datetime import date, datetime

import aiohttp
from fastapi import Body
from dateutil.relativedelta import relativedelta

from config import settings
from db.config import AsyncSessionMaker
from db.dal import SaleReportDAL
from parse.api import SaleReportGetter


async def get_sale_report_dal():
    async with AsyncSessionMaker() as session:
        async with session.begin():
            yield SaleReportDAL(session)


async def get_sale_reports_getter(key: str, date_from: date, date_to: date):
    async with aiohttp.ClientSession(base_url=settings.wb_base_url) as session:
        yield SaleReportGetter(
            session=session,
            key=key,
            date_from=date_from,
            date_to=date_to
        )


async def get_init_sale_reports_getter(api_key: str = Body(...)):
    today: date = datetime.utcnow().date()
    three_months_ago: date = today - relativedelta(months=3)
    async with aiohttp.ClientSession(base_url=settings.wb_base_url) as session:
        yield SaleReportGetter(
            session=session,
            key=api_key,
            date_from=three_months_ago,
            date_to=today
        )
