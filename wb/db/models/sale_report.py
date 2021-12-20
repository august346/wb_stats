from sqlalchemy import Column, BigInteger, DateTime, Integer, String, DECIMAL
from sqlalchemy.dialects.postgresql import JSONB

from db.config import Base


class SaleReport(Base):
    __tablename__ = "sale_report"

    id = Column(BigInteger, primary_key=True)
    row_id = Column(BigInteger)     # rrd_id
    created = Column(DateTime)    # rr_dt
    report_list_id = Column(Integer)  # realizationreport_id
    wb_id = Column(Integer)     # nm_id
    name = Column(String)    # sa_name
    brand = Column(String)  # brand_name
    barcode = Column(String)    # barcode
    type = Column(String)  # doc_type_name
    operation = Column(String)  # supplier_oper_name
    for_pay = Column(DECIMAL(12, 2))    # ppvz_for_pay
    reward = Column(DECIMAL(12, 2))     # ppvz_reward
    delivery = Column(DECIMAL(12, 2))   # delivery_rub

    api_version = Column(Integer)
    document = Column(JSONB)    # *
    api_key = Column(String)

    __mapper_args__ = {"eager_defaults": True}

    @classmethod
    def get_fields_sale_refund_delivery_fine(cls) -> list[Column]:
        return [
            cls.for_pay,
            cls.for_pay,
            cls.delivery,
            cls.delivery
        ]
