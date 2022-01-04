from datetime import date, datetime

from fastapi import HTTPException
from starlette import status


def as_dt(d: date) -> datetime:
    return datetime.combine(d, datetime.min.time())


not_found_exc = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Item not found",
)