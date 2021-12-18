from fastapi import APIRouter, Depends
from starlette import status

from db.dal import WbApiKeyDAL
from db.models.user import WbApiKey
from dependencies import get_wb_api_key_dal

router = APIRouter()


@router.get("/{wak_id}")
async def get(wak_id: int, wak_dal: WbApiKeyDAL = Depends(get_wb_api_key_dal)) -> WbApiKey:
    return await wak_dal.get(wak_id)


@router.patch("/{wak_id}")
async def update(wak_id: int, wak_name: str, wak_dal: WbApiKeyDAL = Depends(get_wb_api_key_dal)) -> WbApiKey:
    return await wak_dal.update(wak_id, wak_name)


@router.delete("/{wak_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(wak_id: int, wak_dal: WbApiKeyDAL = Depends(get_wb_api_key_dal)):
    await wak_dal.delete(wak_id)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(name: str, key: str, wak_dal: WbApiKeyDAL = Depends(get_wb_api_key_dal)) -> WbApiKey:
    return await wak_dal.create(name, key)


@router.get("/")
async def get_list(wak_dal: WbApiKeyDAL = Depends(get_wb_api_key_dal)) -> list[WbApiKey]:
    return await wak_dal.list()
