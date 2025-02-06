from typing import Any

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    debug: bool = True

    @property
    def fastapi_settings(self) -> dict[str, Any]:
        return dict(
            debug=self.debug,
        )

    @property
    def sqlalchemy_engine_settings(self) -> dict[str, Any]:
        return dict(
            url="sqlite+aiosqlite:///:memory:",
            echo=True,
        )
