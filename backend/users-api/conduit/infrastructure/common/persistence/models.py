from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from conduit.domain.users.user import User


class Base(DeclarativeBase):
    pass


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str]
    bio: Mapped[str]
    image_url: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]

    def to_user(self) -> User:
        return User(
            id=self.id,
            email=self.email,
            username=self.username,
            bio=self.bio,
            image_url=self.image_url,
        )
