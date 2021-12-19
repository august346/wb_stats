from fastapi import FastAPI

from routers.router import router
from db.config import engine, Base

app = FastAPI()
app.include_router(router)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def root():
    return {"service": "parse"}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", port=1112, host='127.0.0.1')
