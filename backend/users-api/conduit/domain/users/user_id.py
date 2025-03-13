import uuid

from typing_extensions import TypeAlias

UserId: TypeAlias = uuid.UUID


def new_user_id() -> UserId:
    return uuid.uuid4()
