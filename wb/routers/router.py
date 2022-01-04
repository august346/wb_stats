from datetime import date, datetime

from dateutil.relativedelta import relativedelta
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status, Body

from db.dal import SaleReportDAL
from dependencies import get_init_sale_reports_getter, get_sale_report_dal, prepare_sale_dates, SaleDates
from parse.api import SaleReportGetter
from tasks import tasks
from utils import utils
from utils.collector import add_stock_balances
from utils.transformer import add_sums

router = APIRouter()


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
    brands: list[str] = Body(default=[]),
    psd: SaleDates = Depends(prepare_sale_dates),
    sale_report_dal: SaleReportDAL = Depends(get_sale_report_dal)
):
    if any(x is None for x in (psd.min, psd.max)):
        raise utils.not_found_exc

    now: datetime = datetime.utcnow()
    if psd.min > psd.dt_from or psd.max < min(psd.dt_from, now):
        await tasks.async_collect_rows(api_key, psd.d_from, psd.d_to)

    sale_report_rows = await sale_report_dal.get_grouped(api_key, psd.d_from, psd.d_to)
    if not sale_report_rows:
        return []

    sale_report_dicts = map(dict, sale_report_rows)
    sale_reports_with_stock_balances = [d async for d in add_stock_balances(api_key, sale_report_dicts)]
    sale_reports_final = list(add_sums(brands, sale_reports_with_stock_balances))

    return sale_reports_final


@router.post("/sale_brands")
async def sale_brands(
    api_key: str = Body(...),
    sale_report_dal: SaleReportDAL = Depends(get_sale_report_dal)
):
    return [sr.brand for sr in (await sale_report_dal.get_brands(api_key))]
