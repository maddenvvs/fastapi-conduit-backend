from dataclasses import dataclass
from typing import Optional


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


@dataclass
class User:
    id: int
    email: str
    username: str
    bio: str
    image: Optional[str]

    def to_registered_user(self, token: str) -> RegisteredUser:
        return RegisteredUser(
            email=self.email,
            username=self.username,
            bio=self.bio,
            image=self.image,
            token=token,
        )
