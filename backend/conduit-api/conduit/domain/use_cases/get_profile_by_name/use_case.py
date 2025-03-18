from typing import Optional, final

from conduit.domain.entities.profiles import Profile
from conduit.domain.entities.users import User
from conduit.domain.services.profiles_service import ProfilesService
from conduit.shared.application.unit_of_work import UnitOfWorkFactory


@final
class GetProfileByNameUseCase:
    def __init__(
        self,
        uow_factory: UnitOfWorkFactory,
        profiles_service: ProfilesService,
    ) -> None:
        self._uow_factory = uow_factory
        self._profiles_service = profiles_service

    async def __call__(
        self,
        username: str,
        current_user: Optional[User],
    ) -> Optional[Profile]:
        async with self._uow_factory():
            return await self._profiles_service.get_by_username_or_none(
                username,
                current_user,
            )
