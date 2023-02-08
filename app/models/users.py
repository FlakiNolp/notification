from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, declarative_base, mapped_column
import sqlalchemy
from datetime import datetime
import uuid

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    __table_args__ = {"schema": "users"}
    id: Mapped[int] = mapped_column(primary_key=True, unique=True, comment="Уникальный идентификатор пользователя")
    email: Mapped[str] = mapped_column(unique=True, comment="Почта, по которой пользователь регистрировался")
    hashed_password: Mapped[str] = mapped_column(comment="Хеш пароля от аккаунта")
    api_token: Mapped[str] = mapped_column(unique=True, comment="Уникальный идентификационный токен, по которому будет "
                                                                "определяться пользователь при отправке логов")
    services: Mapped["Notification"] = relationship(back_populates="user", lazy="joined")
    token: Mapped["Token"] = relationship(back_populates="user", lazy="joined")


class Notification(Base):
    __tablename__ = "notification"
    __table_args__ = {"schema": "users"}
    user_id: Mapped[str] = mapped_column(ForeignKey(User.id), primary_key=True, unique=True)
    email: Mapped[str] = mapped_column(nullable=True)
    telegram_id: Mapped[int] = mapped_column(nullable=True)
    vk_domain: Mapped[str] = mapped_column(nullable=True)
    website: Mapped[str] = mapped_column(nullable=True)
    user: Mapped["User"] = relationship(back_populates="services", lazy="joined")


class Token(Base):
    __tablename__ = "token"
    __table_args__ = {"schema": "users"}
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id), primary_key=True, unique=True, comment="ID токена")
    token: Mapped[uuid.UUID] = mapped_column(unique=True, default=uuid.uuid4(), nullable=False)
    expires: Mapped[datetime] = mapped_column(nullable=False)
    user: Mapped["User"] = relationship(back_populates="token", lazy="write_only")
