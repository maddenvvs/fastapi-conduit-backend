from typing import final

from conduit.domain.users.user import User


@final
class GetCurrentUserUseCase:
    async def __call__(self, current_user: User) -> User:
        return current_user
