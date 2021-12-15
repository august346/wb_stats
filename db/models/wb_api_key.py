from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from db.config import Base
from db.models.sale_report import SaleReport


class WbApiKey(Base):
    __tablename__ = "wb_api_key"

    id = Column(Integer, primary_key=True)
    key = Column(String, nullable=False)
    name = Column(String, nullable=False)

    user_id = Column(ForeignKey("user.id", ondelete='CASCADE'))

    sale_reports = relationship(SaleReport, backref="wb_api_key", passive_deletes=True)

    __mapper_args__ = {"eager_defaults": True}
    __table_args__ = (
        UniqueConstraint('name', 'user_id', name='name_user_is_wbapikey_unique'),
    )
