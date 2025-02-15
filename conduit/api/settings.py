import functools
from typing import Any

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    debug: bool = False
    database_url: str = ""

    model_config = SettingsConfigDict(
        env_file=(".env", ".env.prod"),
    )

    @property
    def fastapi(self) -> dict[str, Any]:
        return dict(
            debug=self.debug,
        )

    @property
    def sqlalchemy_engine(self) -> dict[str, Any]:
        return dict(
            url=self.database_url,
            echo=True,
        )


@functools.cache
def get_settings() -> Settings:
    return Settings()
