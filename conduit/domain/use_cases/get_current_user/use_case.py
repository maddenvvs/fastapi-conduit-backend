from typing import final

from conduit.domain.entities.users import User


@final
class GetCurrentUserUseCase:

    async def __call__(self, current_user: User) -> User:
        return current_user
