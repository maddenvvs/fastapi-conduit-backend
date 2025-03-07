from typing import Any, final


@final
class Errors:
    @staticmethod
    def invalid_user_id_type(value: Any) -> Exception:
        return ValueError("Invalid user id type", value)

    @staticmethod
    def invalid_username_type(value: Any) -> Exception:
        return ValueError("Invalid username type", value)

    @staticmethod
    def invalid_username_length(*, min_length: int, max_length: int) -> Exception:
        error_message = (
            f"Username length must be between {min_length} and {max_length}",
        )
        return ValueError(error_message)

    @staticmethod
    def invalid_email_type(value: Any) -> Exception:
        return ValueError("Invalid email type", value)

    @staticmethod
    def invalid_email_format(value: str) -> Exception:
        return ValueError("Invalid email format", value)
