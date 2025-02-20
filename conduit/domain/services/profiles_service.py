from typing import Optional, final

from conduit.domain.entities.profiles import Profile
from conduit.domain.entities.users import User, UserID
from conduit.domain.repositories.followers import FollowersRepository
from conduit.domain.repositories.users import UsersRepository


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
            is_following = True

        return Profile(
            id=target_user.id,
            username=target_user.username,
            bio=target_user.bio,
            image=target_user.image,
            following=is_following,
        )

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
            is_following = True

        return Profile(
            id=target_user.id,
            username=target_user.username,
            bio=target_user.bio,
            image=target_user.image,
            following=is_following,
        )

    async def follow_profile(
        self,
        username: str,
        current_user: User,
    ) -> None:
        if username == current_user.username:
            raise Exception

        target_user = await self._users_repository.get_by_username_or_none(username)

        if target_user is None:
            raise Exception

        if await self._followers_repository.exists(
            follower_id=current_user.id,
            following_id=target_user.id,
        ):
            raise Exception

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
            raise Exception

        target_user = await self._users_repository.get_by_username_or_none(username)

        if target_user is None:
            raise Exception

        if not await self._followers_repository.exists(
            follower_id=current_user.id,
            following_id=target_user.id,
        ):
            raise Exception

        await self._followers_repository.delete(
            follower_id=current_user.id,
            following_id=target_user.id,
        )
