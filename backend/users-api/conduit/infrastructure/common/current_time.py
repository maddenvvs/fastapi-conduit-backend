import datetime
from typing import Callable

from typing_extensions import TypeAlias

CurrentTime: TypeAlias = Callable[[], datetime.datetime]


def current_time() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)
