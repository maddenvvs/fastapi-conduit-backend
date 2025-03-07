from typing import Any, final


@final
class Errors:
    @staticmethod
    def invalid_user_id(value: Any) -> Exception:
        return ValueError("Invalid user id", value)

    @staticmethod
    def invalid_username(value: Any) -> Exception:
        return ValueError("Invalid username", value)

    @staticmethod
    def invalid_username_length(*, min_length: int, max_length: int) -> Exception:
        error_message = (
            f"Username length must be between {min_length} and {max_length}",
        )
        return ValueError(error_message)
