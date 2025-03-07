from typing import Any, final


@final
class Errors:
    @staticmethod
    def invalid_user_id(value: Any) -> Exception:
        return ValueError("Invalid user id", value)
