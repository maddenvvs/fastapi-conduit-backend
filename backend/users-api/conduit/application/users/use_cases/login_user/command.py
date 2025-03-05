from dataclasses import dataclass
from typing import final


@final
@dataclass(frozen=True)
class LoginUserCommand:
    email: str
    password: str
