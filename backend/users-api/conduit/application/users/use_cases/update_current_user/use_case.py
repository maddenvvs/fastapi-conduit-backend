from typing import final

from returns.result import Failure, Result, Success

from conduit.application.common.errors import ApplicationError, Errors
from conduit.application.common.unit_of_work import UnitOfWorkFactory
from conduit.application.users.repositories.users_repository import UsersRepository
from conduit.application.users.use_cases.update_current_user.command import (
    UpdateCurrentUserCommand,
)
from conduit.domain.users.updated_user import UpdatedUser
from conduit.domain.users.user import User


@final
class UpdateCurrentUserUseCase:
    def __init__(
        self,
        uow_factory: UnitOfWorkFactory,
        users_repository: UsersRepository,
    ) -> None:
        self._uow_factory = uow_factory
        self._users_repository = users_repository

    async def __call__(
        self,
        update_request: UpdateCurrentUserCommand,
    ) -> Result[User, ApplicationError]:
        current_user = update_request.current_user

        async with self._uow_factory():
            if (
                update_request.username
                and update_request.username != current_user.username
            ):
                user = await self._users_repository.get_by_username(
                    update_request.username,
                )
                if user.value_or(None) is not None:
                    return Failure(Errors.username_is_taken())

            if update_request.email and update_request.email != current_user.email:
                user = await self._users_repository.get_by_email(
                    update_request.email,
                )
                if user.value_or(None) is not None:
                    return Failure(Errors.email_is_taken())

            updated_user = UpdatedUser(
                id=current_user.id,
                username=update_request.username,
                email=update_request.email,
                password=update_request.password,
                bio=update_request.bio,
                image_url=update_request.image_url,
            )

            current_user = await self._users_repository.update(updated_user)
            return Success(current_user)
