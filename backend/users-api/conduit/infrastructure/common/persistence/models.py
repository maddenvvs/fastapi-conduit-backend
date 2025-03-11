from datetime import datetime
from typing import Optional

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from conduit.domain.users.email_address import EmailAddress
from conduit.domain.users.image_url import ImageUrl
from conduit.domain.users.user import User
from conduit.domain.users.user_id import UserId
from conduit.domain.users.username import Username


class Base(DeclarativeBase):
    pass


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str]
    bio: Mapped[str]
    image_url: Mapped[Optional[str]] = mapped_column(nullable=True)
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]

    def to_user(self) -> User:
        return User(
            id=UserId(self.id),
            email=EmailAddress(self.email),
            username=Username(self.username),
            bio=self.bio,
            image_url=None if self.image_url is None else ImageUrl(self.image_url),
        )
