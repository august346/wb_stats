from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Body, Response
from starlette import status

from db.dal import UserWbApiKeyDAL
from db.models.wb_api_key import UserWbApiKey
from dependencies import get_user_wb_api_key_dal, get_wb_service
from sevices.wb import WbService
from utils import redis

router = APIRouter()


@router.get("/{wak_id}")
async def get(
    wak_id: int,
    wb_service: WbService = Depends(get_wb_service),
    wak_dal: UserWbApiKeyDAL = Depends(get_user_wb_api_key_dal)
):
    api_key = await wak_dal.get_with_key(wak_id)
    brands = await wb_service.get_brands(api_key.wb_api_key.key)
    return {
        "id": api_key.wb_api_key_id,
        "name": api_key.name,
        "key": f"...{api_key.wb_api_key.key[-6:]}",
        "brands": brands,
        "history": {
            "sale_reports": await redis.History.get_sale_reports(wak_dal.user_id, wak_id)
        }
    }


@router.patch("/{wak_id}")
async def update(
    wak_id: int,
    wak_name: str = Body(...),
    wak_dal: UserWbApiKeyDAL = Depends(get_user_wb_api_key_dal)
) -> UserWbApiKey:
    return await wak_dal.update(wak_id, wak_name)


@router.delete("/{wak_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(wak_id: int, wak_dal: UserWbApiKeyDAL = Depends(get_user_wb_api_key_dal)):
    await wak_dal.delete(wak_id)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(
    name: str = Body(...),
    key: str = Body(...),
    wak_dal: UserWbApiKeyDAL = Depends(get_user_wb_api_key_dal),
    wb_service: WbService = Depends(get_wb_service)
) -> UserWbApiKey:
    await wak_dal.assert_not_exist(key)

    if not (await wb_service.init_key(key)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid WB api key",
        )

    return await wak_dal.create(name, key)


@router.get("/")
async def get_list(wak_dal: UserWbApiKeyDAL = Depends(get_user_wb_api_key_dal)) -> list[UserWbApiKey]:
    return await wak_dal.list()


@router.post("/{wak_id}/report")
async def report(
    response: Response,
    wak_id: int,
    date_from: date = Body(...),
    date_to: date = Body(...),
    brands: list[str] = Body(default=[]),
    wb_service: WbService = Depends(get_wb_service),
    wak_dal: UserWbApiKeyDAL = Depends(get_user_wb_api_key_dal)
):
    data, headers = await wb_service.get_report(
        key=await wak_dal.get_key(wak_id),
        date_from=date_from,
        date_to=date_to,
        brands=brands
    )

    history: list[dict] = await redis.History.add_sale_reports(wak_dal.user_id, wak_id, date_from, date_to, brands)

    response.headers.update(headers)

    return {'data': data, 'history': history}
