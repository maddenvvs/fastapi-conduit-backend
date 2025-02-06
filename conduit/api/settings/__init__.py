import functools

from .base import Settings


@functools.cache
def get_settings() -> Settings:
    return Settings()
