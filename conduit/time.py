import datetime

from typing_extensions import Callable, TypeAlias

CurrentTime: TypeAlias = Callable[[], datetime.datetime]


def current_time() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)
