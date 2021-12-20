from datetime import date
from functools import wraps
from typing import Optional

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import NoResultFound
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from sqlalchemy.sql import Select
from starlette import status

from .config import Base
from .models.sale_report import SaleReport


class NotFound(HTTPException):
    def __init__(self):
        super(NotFound, self).__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )


def raise_not_found(f):
    @wraps(f)
    async def wrapper(*args, **kwargs):
        try:
            return await f(*args, **kwargs)
        except NoResultFound:
            raise NotFound

    return wrapper


class BaseDAL:
    db_session: Session

    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def _all(self, sel: Select):
        q = await self.db_session.execute(sel)
        return q.fetchall()

    @raise_not_found
    async def _first(self, sel: Select) -> Base:
        q = await self.db_session.execute(sel)
        return q.scalars().first()

    @raise_not_found
    async def _add(self, obj: Base):
        self.db_session.add(obj)
        await self.db_session.flush()

    @raise_not_found
    async def _delete(self, obj: Base):
        await self.db_session.delete(obj)
        await self.db_session.flush()

    async def _get_or_create(self, sel: Select, obj: Base) -> Base:
        old_instance: Optional[Base] = await self._first(sel)

        if old_instance:
            return old_instance

        await self._add(obj)
        return obj


class SaleReportDAL(BaseDAL):
    async def exist_many(self, api_keys: list[str]) -> dict[str, bool]:
        db_api_keys: list[str] = await self._all(
            select(SaleReport.api_key).filter(
                SaleReport.api_key.in_(api_keys)
            ).group_by(SaleReport.api_key)
        )

        return {
            expected: expected in db_api_keys
            for expected in api_keys
        }

    async def exist(self, api_key: str) -> bool:
        return (await self.exist_many([api_key]))[api_key]

    async def get_max_row_id(self, api_key: str) -> int:
        max_row_id: Optional[int] = await self._first(
            select(func.max(SaleReport.row_id)).filter(
                SaleReport.api_key == api_key
            )
        )

        return max_row_id or 0

    async def add_many(self, rows: list[dict]) -> int:
        def batch(iterable, batch_size=1):
            size = len(iterable)
            for ndx in range(0, size, batch_size):
                yield iterable[ndx:min(ndx + batch_size, size)]

        for b_rows in batch(rows, batch_size=1_000):
            await self.db_session.execute(
                insert(SaleReport).values(b_rows).on_conflict_do_nothing()
            )

        await self.db_session.commit()
        return 1

    async def get_many(self, api_key: str, date_from: date, date_to: date) -> list[SaleReport]:
        return await self._all(
            select(SaleReport).filter(
                SaleReport.api_key == api_key,
                date_from <= SaleReport.created < date_to,
            )
        )

    async def get_grouped(self, api_key: str, date_from: date, date_to: date):
        group_cols = (
            SaleReport.wb_id,
            SaleReport.brand,
            SaleReport.name,
            SaleReport.barcode,
            SaleReport.type,
            SaleReport.operation
        )

        return await self._all(
            select(
                *group_cols,
                func.count().label("count"),
                func.sum(SaleReport.for_pay).label("for_pay"),
                func.sum(SaleReport.delivery).label("delivery"),
            ).filter(
                SaleReport.api_key == api_key,
                SaleReport.created.between(date_from, date_to)
            ).group_by(
                *group_cols
            )
        )
