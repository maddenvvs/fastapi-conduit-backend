from typing import Optional, final

from conduit.domain.entities.profiles import Profile
from conduit.domain.entities.users import User, UserID
from conduit.domain.exceptions import DomainException
from conduit.domain.repositories.followers import FollowersRepository
from conduit.domain.repositories.users import UsersRepository


def _to_profile(user: User, following: bool) -> Profile:
    return Profile(
        id=user.id,
        username=user.username,
        bio=user.bio,
        image=user.image,
        following=following,
    )


@final
class ProfilesService:

    def __init__(
        self,
        users_repository: UsersRepository,
        followers_repository: FollowersRepository,
    ) -> None:
        self._users_repository = users_repository
        self._followers_repository = followers_repository

    async def get_by_user_id_or_none(
        self,
        user_id: UserID,
        current_user: Optional[User] = None,
    ) -> Optional[Profile]:
        target_user = await self._users_repository.get_by_id_or_none(user_id)

        if target_user is None:
            return None

        is_following = False
        if current_user is not None:
            is_following = await self._followers_repository.exists(
                current_user.id,
                target_user.id,
            )

        return _to_profile(target_user, is_following)

    async def get_by_username_or_none(
        self,
        username: str,
        current_user: Optional[User] = None,
    ) -> Optional[Profile]:
        target_user = await self._users_repository.get_by_username_or_none(username)
        if target_user is None:
            return None

        is_following = False
        if current_user is not None:
            is_following = await self._followers_repository.exists(
                current_user.id,
                target_user.id,
            )

        return _to_profile(target_user, is_following)

    async def follow_profile(
        self,
        username: str,
        current_user: User,
    ) -> None:
        if username == current_user.username:
            raise DomainException("Cannot follow yourself")

        target_user = await self._users_repository.get_by_username_or_none(username)
        if target_user is None:
            raise DomainException("Cannot follow non-existing user")

        if await self._followers_repository.exists(
            follower_id=current_user.id,
            following_id=target_user.id,
        ):
            raise DomainException("Profile is already followed")

        await self._followers_repository.create(
            follower_id=current_user.id,
            following_id=target_user.id,
        )

    async def unfollow_profile(
        self,
        username: str,
        current_user: User,
    ) -> None:
        if username == current_user.username:
            raise DomainException("Cannot follow yourself")

        target_user = await self._users_repository.get_by_username_or_none(username)
        if target_user is None:
            raise DomainException("Cannot follow non-existing user")

        if not await self._followers_repository.exists(
            follower_id=current_user.id,
            following_id=target_user.id,
        ):
            raise DomainException("Profile is already unfollowed")

        await self._followers_repository.delete(
            follower_id=current_user.id,
            following_id=target_user.id,
        )

    async def list_by_user_ids(
        self,
        user_ids: list[UserID],
        current_user: Optional[User],
    ) -> list[Profile]:
        target_users = await self._users_repository.list_by_user_ids(user_ids)
        return [_to_profile(user, following=False) for user in target_users]
