from dataclasses import dataclass, field
from typing import Optional, final

from conduit.domain.entities.users import UpdateUserDetails, User
from conduit.domain.repositories.unit_of_work import UnitOfWork
from conduit.domain.services.password_service import PasswordHasher


@final
@dataclass(frozen=True)
class UpdateCurrentUserRequest:
    current_user: User
    username: Optional[str] = field(default=None)
    email: Optional[str] = field(default=None)
    password: Optional[str] = field(default=None)
    bio: Optional[str] = field(default=None)
    image_url: Optional[str] = field(default=None)


@final
class UpdateCurrentUserUseCase:

    def __init__(
        self,
        unit_of_work: UnitOfWork,
        password_hasher: PasswordHasher,
    ) -> None:
        self._uow = unit_of_work
        self._password_hasher = password_hasher

    async def __call__(self, update_request: UpdateCurrentUserRequest) -> User:
        current_user = update_request.current_user

        async with self._uow.begin() as db:
            if (
                update_request.username
                and update_request.username != current_user.username
            ):
                if await db.users.get_by_username_or_none(update_request.username):
                    raise Exception("Already exists")

            if update_request.email and update_request.email != current_user.email:
                if await db.users.get_by_email_or_none(update_request.email):
                    raise Exception("Already exists")

            password_hash: Optional[str] = None
            if update_request.password:
                password_hash = self._password_hasher(update_request.password)

            update_details = UpdateUserDetails(
                username=update_request.username,
                email=update_request.email,
                password_hash=password_hash,
                bio=update_request.bio,
                image_url=update_request.image_url,
            )

            updated_user = await db.users.update(
                user_id=current_user.id,
                update_details=update_details,
            )

        return updated_user
