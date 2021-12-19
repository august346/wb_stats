from fastapi import APIRouter, Depends, HTTPException, Body
from starlette import status

from db.dal import UserWbApiKeyDAL
from db.models.wb_api_key import UserWbApiKey
from dependencies import get_user_wb_api_key_dal, get_wb_service
from sevices.wb import WbService

router = APIRouter()


@router.get("/{wak_id}")
async def get(wak_id: int, wak_dal: UserWbApiKeyDAL = Depends(get_user_wb_api_key_dal)) -> UserWbApiKey:
    return await wak_dal.get(wak_id)


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
