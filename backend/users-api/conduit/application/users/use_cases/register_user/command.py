from dataclasses import dataclass
from typing import final


@final
@dataclass(frozen=True)
class RegisterUserCommand:
    username: str
    email: str
    password: str
