from typing import Optional, final

from conduit.domain.entities.profiles import Profile
from conduit.domain.entities.users import User
from conduit.domain.services.profiles_service import ProfilesService
from conduit.domain.unit_of_work import UnitOfWorkFactory


@final
class FollowProfileUseCase:
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
        current_user: User,
    ) -> Optional[Profile]:
        async with self._uow_factory():
            profile = await self._profiles_service.get_by_username_or_none(username)
            if profile is None:
                return None

            await self._profiles_service.follow_profile(username, current_user)
            return Profile(
                id=profile.id,
                username=profile.username,
                bio=profile.bio,
                image=profile.image,
                following=True,
            )
