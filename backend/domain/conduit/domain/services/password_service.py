from typing import Callable

from typing_extensions import TypeAlias

PasswordHasher: TypeAlias = Callable[[str], str]
PasswordChecker: TypeAlias = Callable[[str, str], bool]


class PasswordService:
    def hash_password(self, password: str) -> str:
        return password

    def check_password(self, plain_password: str, hashed_password: str) -> bool:
        return plain_password == hashed_password
