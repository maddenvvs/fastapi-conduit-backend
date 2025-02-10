from dataclasses import dataclass


@dataclass
class UserLoginDetails:
    email: str
    password: str


@dataclass
class LoggedInUser:
    email: str
    username: str
    bio: str
    image: str
    token: str


@dataclass
class User:
    id: str
    name: str
