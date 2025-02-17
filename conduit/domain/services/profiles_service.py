from typing import Optional, final

from conduit.domain.entities.profiles import Profile
from conduit.domain.entities.users import User, UserID
from conduit.domain.repositories.unit_of_work import UnitOfWork


@final
class ProfilesService:

    def __init__(self, unit_of_work: UnitOfWork) -> None:
        self._uow = unit_of_work

    async def get_by_user_id_or_none(
        self,
        user_id: UserID,
        current_user: Optional[User] = None,
    ) -> Optional[Profile]:
        async with self._uow.begin() as db:
            target_user = await db.users.get_by_id_or_none(user_id)

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
