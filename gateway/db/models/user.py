from sqlalchemy import Column, Integer, String, Boolean

from db.config import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String, nullable=False)
    disabled = Column(Boolean, default=True)

    __mapper_args__ = {"eager_defaults": True}
