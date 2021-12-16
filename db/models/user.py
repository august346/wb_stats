from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from db.config import Base
from db.models.wb_api_key import WbApiKey


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String, nullable=False)
    disabled = Column(Boolean, default=True)

    wb_api_keys = relationship(WbApiKey, backref="user", passive_deletes=True)

    __mapper_args__ = {"eager_defaults": True}
