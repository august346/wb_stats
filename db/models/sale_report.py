from sqlalchemy import Column, BigInteger, DateTime, Integer, String, Float, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB

from db.config import Base


class SaleReport(Base):
    __tablename__ = "sale_report"

    id = Column(BigInteger, primary_key=True)
    row_id = Column(BigInteger)     #rrd_id
    created = Column(DateTime)    # rr_dt
    report_list_id = Column(Integer)  # realizationreport_id
    wb_id = Column(Integer)     # nm_id
    name = Column(String)    # sa_name
    brand = Column(String)  # brand_name
    barcode = Column(String)    # barcode
    type = Column(String)  # doc_type_name
    operation = Column(String)  # supplier_oper_name
    for_pay = Column(Float)    # ppvz_for_pay
    reward = Column(Float)  # ppvz_reward
    delivery = Column(Float)    # delivery_rub

    api_version = Column(Integer)
    document = Column(JSONB)    # *

    wb_api_key_id = Column(ForeignKey("wb_api_key.id", ondelete='CASCADE'))

    __mapper_args__ = {"eager_defaults": True}