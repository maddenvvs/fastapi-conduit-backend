import functools
from typing import Any

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    debug: bool = False
    database_url: str = ""

    jwt_secret_key: str = Field(default="", min_length=16)
    jwt_algorithm: str = Field(default="HS256", min_length=1)
    jwt_token_expiration_minutes: int = Field(default=30, gt=1)

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
