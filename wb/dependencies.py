from dataclasses import dataclass
from datetime import date, datetime

import aiohttp
from fastapi import Body, Depends, Response
from dateutil.relativedelta import relativedelta

from config import settings
from db.config import AsyncSessionMaker
from db.dal import SaleReportDAL
from parse.api import SaleReportGetter
from utils import utils


async def get_sale_report_dal():
    async with AsyncSessionMaker() as session:
        async with session.begin():
            yield SaleReportDAL(session)


@dataclass
class SaleDates:
    now: datetime
    d_from: date
    d_to: date
    dt_from: datetime
    dt_to: datetime
    min: datetime
    max: datetime


async def prepare_sale_dates(
    response: Response,
    api_key: str = Body(...),
    date_from: date = Body(...),
    date_to: date = Body(...),
    sale_report_dal: SaleReportDAL = Depends(get_sale_report_dal)
):
    now: datetime = datetime.utcnow()
    date_from_dt, date_to_dt = map(utils.as_dt, (date_from, date_to))

    if date_from_dt > now:
        raise utils.not_found_exc

    min_created, max_created = await sale_report_dal.get_max_min_created(api_key)
    response.headers["X-Data-Min-Created"] = min_created.isoformat()
    response.headers["X-Data-Max-Created"] = max_created.isoformat()
    return SaleDates(
        now=now,
        d_from=date_from,
        d_to=date_to,
        dt_from=date_from_dt,
        dt_to=date_to_dt,
        min=min_created,
        max=max_created
    )


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
