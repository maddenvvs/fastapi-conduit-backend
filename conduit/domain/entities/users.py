from dataclasses import dataclass, field
from typing import Optional, final

from typing_extensions import TypeAlias

UserID: TypeAlias = int


@dataclass(frozen=True)
class UserLoginDetails:
    email: str
    password: str


@dataclass(frozen=True)
class LoggedInUser:
    email: str
    username: str
    bio: str
    image: Optional[str]
    token: str


@dataclass(frozen=True)
class RegisterUserDetails:
    username: str
    email: str
    password: str


@dataclass(frozen=True)
class RegisteredUser:
    email: str
    username: str
    bio: str
    image: Optional[str]
    token: str


@dataclass(frozen=True)
class CreateUserDetails:
    username: str
    email: str
    password_hash: str


@final
@dataclass(frozen=True)
class UpdateUserDetails:
    username: Optional[str] = field(default=None)
    email: Optional[str] = field(default=None)
    password_hash: Optional[str] = field(default=None)
    bio: Optional[str] = field(default=None)
    image_url: Optional[str] = field(default=None)


@dataclass
class User:
    id: UserID
    email: str
    username: str
    bio: str
    image: Optional[str]
    password_hash: str

    def to_registered_user(self, token: str) -> RegisteredUser:
        return RegisteredUser(
            email=self.email,
            username=self.username,
            bio=self.bio,
            image=self.image,
            token=token,
        )

    def to_logged_in_user(self, token: str) -> LoggedInUser:
        return LoggedInUser(
            email=self.email,
            username=self.username,
            bio=self.bio,
            image=self.image,
            token=token,
        )
