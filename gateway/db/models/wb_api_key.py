from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from db.config import Base


class WbApiKey(Base):
    __tablename__ = "wb_api_key"

    id = Column(Integer, primary_key=True)
    key = Column(String, nullable=False, unique=True)

    __mapper_args__ = {"eager_defaults": True}


class UserWbApiKey(Base):
    __tablename__ = "user_wb_api_key"

    name = Column(String, nullable=False)

    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    wb_api_key_id = Column(Integer, ForeignKey('wb_api_key.id', ondelete='RESTRICT'), primary_key=True)

    user = relationship('User', uselist=False, backref='user_wb_api_keys')
    wb_api_key = relationship('WbApiKey', uselist=False, backref='user_wb_api_keys')

    __mapper_args__ = {"eager_defaults": True}
    __table_args__ = (
        UniqueConstraint('user_id', 'wb_api_key_id'),
    )
