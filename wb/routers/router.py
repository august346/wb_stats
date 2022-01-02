import csv
import io
from datetime import date, datetime

from dateutil.relativedelta import relativedelta
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status, Body
from starlette.responses import StreamingResponse

from db.dal import SaleReportDAL
from dependencies import get_init_sale_reports_getter, get_sale_report_dal
from parse.api import SaleReportGetter
from tasks import tasks
from utils import utils
from utils.collector import add_stock_balances
from utils.transformer import add_sums

router = APIRouter()

not_found_exc = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Item not found",
)


@router.post("/init", status_code=status.HTTP_202_ACCEPTED)
async def init(
        background_tasks: BackgroundTasks,
        init_getter: SaleReportGetter = Depends(get_init_sale_reports_getter),
):
    if not (await init_getter.is_api_key_valid()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid api key",
        )

    today: date = datetime.utcnow().date()
    three_months_ago: date = today - relativedelta(months=3)

    background_tasks.add_task(tasks.collect_rows, init_getter.key, three_months_ago, today)


@router.post("/exists")
async def exists(api_keys: list[str] = Body(...), sale_report_dal: SaleReportDAL = Depends(get_sale_report_dal)):
    return await sale_report_dal.exist_many(api_keys)


@router.post("/report")
async def report(
    api_key: str = Body(...),
    date_from: date = Body(...),
    date_to: date = Body(...),
    brands: list[str] = Body(default=[]),
    sale_report_dal: SaleReportDAL = Depends(get_sale_report_dal)
):
    now: datetime = datetime.utcnow()
    date_from_dt, date_to_dt = map(utils.as_dt, (date_from, date_to))

    if date_from_dt > now:
        raise not_found_exc

    min_created, max_created = await sale_report_dal.get_max_min_created(api_key)

    if any(x is None for x in (min_created, max_created)):
        raise not_found_exc

    now: datetime = datetime.utcnow()
    if min_created > date_from_dt or max_created < min(date_from_dt, now):
        await tasks.async_collect_rows(api_key, date_from, date_to)

    sale_report_rows = await sale_report_dal.get_grouped(api_key, date_from, date_to)
    if not sale_report_rows:
        return []

    sale_report_dicts = map(dict, sale_report_rows)
    sale_reports_with_stock_balances = [d async for d in add_stock_balances(api_key, sale_report_dicts)]
    sale_reports_final = list(add_sums(brands, sale_reports_with_stock_balances))

    return sale_reports_final
