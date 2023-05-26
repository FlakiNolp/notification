from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, declarative_base, mapped_column

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    __table_args__ = {"schema": "public"}
    id: Mapped[int] = mapped_column(primary_key=True, comment="Уникальный идентификатор пользователя")
    email: Mapped[str] = mapped_column(unique=True, comment="Почта, по которой пользователь регистрировался")
    hashed_password: Mapped[str] = mapped_column(comment="Хеш пароля от аккаунта")
    api_token: Mapped[str] = mapped_column(unique=True, comment="Уникальный идентификационный токен, по которому будет "
                                                                "определяться пользователь при отправке логов")
    services: Mapped["Notification"] = relationship(back_populates="user", lazy="joined")


class Notification(Base):
    __tablename__ = "notification"
    __table_args__ = {"schema": "public"}
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id))
    email: Mapped[str] = mapped_column(nullable=True)
    telegram_id: Mapped[int] = mapped_column(nullable=True)
    vk_domain: Mapped[str] = mapped_column(nullable=True)
    website: Mapped[str] = mapped_column(nullable=True)
    user: Mapped["User"] = relationship(back_populates="services", lazy="joined")
