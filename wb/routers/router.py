import uuid
from datetime import date, datetime

from dateutil.relativedelta import relativedelta
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status, Body

from db.dal import SaleReportDAL
from dependencies import get_init_sale_reports_getter, get_sale_report_dal
from parse.api import SaleReportGetter
from tasks import tasks

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
async def exists(api_keys: list[str], sale_report_dal: SaleReportDAL = Depends(get_sale_report_dal)):
    return await sale_report_dal.exist_many(api_keys)


@router.post("/report", status_code=status.HTTP_200_OK)
async def new_report(api_key: str, date_from: date, date_to: date, background_tasks: BackgroundTasks) -> str:
    report_id: str = str(uuid.uuid4())
    background_tasks.add_task(tasks.create_report, api_key, date_from, date_to)
    return report_id


@router.get("/grouped")
async def get_report(api_key: str, date_from: date, date_to: date, sale_report_dal: SaleReportDAL = Depends(get_sale_report_dal)):
    return await sale_report_dal.get_grouped(api_key, date_from, date_to)
