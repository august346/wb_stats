from datetime import date

from aiohttp import ClientSession, ClientResponse
from fastapi import HTTPException, status
from starlette.responses import StreamingResponse

from config import settings


async def raise_resp(resp: ClientResponse):
    raise HTTPException(
        status_code=resp.status,
        detail=await resp.json(),
        headers=dict(resp.headers),
    )


class WbService:
    def __init__(self, http_session: ClientSession):
        self.http_session = http_session

    async def init_key(self, key: str) -> bool:
        async with self.http_session.post(
            settings.path_wb_service_init,
            json=key
        ) as resp:  # type: ClientResponse
            return resp.status == status.HTTP_202_ACCEPTED

    async def get_report(self, key: str, date_from: date, date_to: date, brands: list[str]):
        async with self.http_session.post(
            settings.path_wb_service_report,
            chunked=True,
            json=dict(api_key=key, date_from=date_from.isoformat(), date_to=date_to.isoformat(), brands=brands),
        ) as resp:
            if resp.status != status.HTTP_200_OK:
                await raise_resp(resp)

            yield StreamingResponse(
                resp.content.iter_chunked(1024),
                media_type="text/csv",
                headers={"Content-Disposition": resp.headers.get("Content-Disposition")}
            )

