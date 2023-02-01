from sqlalchemy import Column, String, ARRAY, ForeignKey, Integer
from app.models.database import Base


class Users(Base):
    __tablename__ = "users"
    id = Column("id", Integer, primary_key=True, unique=True)
    email = Column("email", String, unique=True)
    hashed_password = Column("hashed_password", String)
    api_key = Column("api_key", String, unique=True)
    ip = Column("ip", ARRAY)


class Push(Base):
    __tablename__ = "push"
    api_key = Column("api_key", String, ForeignKey(Users.api_key), primary_key=True, unique=True)
    email = Column("email", String, unique=True)
    telegram_id = Column("telegram_id", String, unique=True)
    vk_domain = Column("vk_domain", String, unique=True)
    website = Column("website", String, unique=True)
