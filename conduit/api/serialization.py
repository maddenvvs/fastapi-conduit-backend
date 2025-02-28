import datetime
from typing import Annotated

from pydantic.functional_serializers import PlainSerializer


def _format_datetime(d: datetime.datetime) -> str:
    return d.strftime("%Y-%m-%dT%H:%M:%SZ")


DateTime = Annotated[
    datetime.datetime,
    PlainSerializer(
        func=_format_datetime,
        return_type=str,
        when_used="json",
    ),
]
