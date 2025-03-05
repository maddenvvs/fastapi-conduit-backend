from typing import final

from returns.result import Failure, Result, Success

from conduit.application.common.errors import ApplicationError, Errors
from conduit.application.common.unit_of_work import UnitOfWorkFactory
from conduit.application.users.repositories.users_repository import UsersRepository
from conduit.application.users.use_cases.register_user.command import (
    RegisterUserCommand,
)
from conduit.domain.users.new_user import NewUser
from conduit.domain.users.user import User


@final
class RegisterUserUseCase:
    def __init__(
        self,
        uow_factory: UnitOfWorkFactory,
        users_repository: UsersRepository,
    ) -> None:
        self._uow_factory = uow_factory
        self._users_repository = users_repository

    async def __call__(
        self,
        command: RegisterUserCommand,
    ) -> Result[User, ApplicationError]:
        async with self._uow_factory():
            user_with_email = await self._users_repository.get_by_email(
                email=command.email,
            )
            if user_with_email.value_or(None) is not None:
                return Failure(Errors.email_is_taken())

            user_with_username = await self._users_repository.get_by_username(
                username=command.username,
            )
            if user_with_username.value_or(None) is not None:
                return Failure(Errors.username_is_taken())

            new_user = NewUser(
                email=command.email,
                username=command.username,
                password=command.password,
            )
            created_user = await self._users_repository.create(new_user)
            return Success(created_user)
