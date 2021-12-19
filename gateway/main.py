from fastapi import FastAPI

from db.config import engine, Base
from routers import user_router, oauth2, wb_api_key

app = FastAPI()
app.include_router(oauth2.router, prefix='/auth')
app.include_router(user_router.router)
app.include_router(wb_api_key.router, prefix='/wb/wb_api_keys')


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def root():
    return {"service": "getaway"}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", port=1111, host='127.0.0.1')
