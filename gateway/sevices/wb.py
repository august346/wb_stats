from aiohttp import ClientSession, ClientResponse
from starlette import status

from config import settings


class WbService:
    def __init__(self, http_session: ClientSession):
        self.http_session = http_session

    async def init_key(self, key: str) -> bool:
        async with self.http_session.post(
            settings.path_wb_service_init,
            json=key
        ) as resp:  # type: ClientResponse
            return resp.status == status.HTTP_202_ACCEPTED
