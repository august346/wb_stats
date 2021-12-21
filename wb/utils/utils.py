from datetime import date, datetime


def as_dt(d: date) -> datetime:
    return datetime.combine(d, datetime.min.time())
