from dataclasses import dataclass
from typing import final


@final
@dataclass(frozen=True)
class Tag:
    id: int
    name: str
