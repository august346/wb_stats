from datetime import date, datetime
from functools import wraps, cached_property
from typing import Optional, Iterable

from fastapi import HTTPException
from sqlalchemy import func, Column, cast, Date
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import NoResultFound
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from sqlalchemy.sql import Select
from sqlalchemy.sql.functions import Function
from starlette import status

from db.config import Base
from db.models.sale_report import SaleReport
from utils.transformer import API_OPERATIONS_SALE_REFUND_DELIVERY_FINE


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

    async def get_min_max_created(
        self, api_key: str, dt_range: tuple[date, date] = None
    ) -> tuple[Optional[datetime], Optional[datetime]]:
        sel = select(
            func.min(SaleReport.created),
            func.max(SaleReport.created),
        ).filter(
            SaleReport.api_key == api_key
        )
        if dt_range:
            assert len(dt_range) == 2
            assert any(isinstance(x, date) for x in dt_range)
            sel = sel.filter(cast(SaleReport.created, Date).between(*dt_range))
        sel = sel.group_by(
            SaleReport.api_key
        )

        rows = await self._all(sel)

        for row in rows:
            return row

        return None, None

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
        return await self._all(
            select(
                *self._group_fields,
                *self._group_aggregate_funcs
            ).filter(
                SaleReport.api_key == api_key,
                cast(SaleReport.created, Date).between(date_from, date_to)
            ).group_by(
                *self._group_fields
            ).order_by(*self._group_fields)
        )

    @cached_property
    def _group_fields(self) -> list[Column]:
        return [
            SaleReport.wb_id,
            SaleReport.brand,
            SaleReport.name,
            SaleReport.barcode
        ]

    @property
    def _group_aggregate_funcs(self) -> Iterable[Function]:
        operations = zip(
            ("sale", "refund", "delivery", "fine"),
            zip(
                API_OPERATIONS_SALE_REFUND_DELIVERY_FINE,
                SaleReport.get_fields_sale_refund_delivery_fine()
            )
        )

        for name, (operation, field) in operations:
            f = SaleReport.operation == operation
            yield func.count(1).filter(f).label(f"count_{name}")
            yield func.coalesce(
                func.sum(field).filter(f), 0
            ).label(f"sum_{name}")

    async def get_brands(self, api_key: str) -> list[SaleReport]:
        return await self._all(
            select(SaleReport.brand).filter(
                SaleReport.api_key == api_key
            ).group_by(
                SaleReport.brand
            ).order_by(func.count(1).desc())
        )
