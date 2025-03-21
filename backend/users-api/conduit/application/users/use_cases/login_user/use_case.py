from typing import final

from returns.converters import maybe_to_result
from returns.result import Result

from conduit.application.users.services.login_service import LoginService
from conduit.application.users.use_cases.login_user.command import LoginUserCommand
from conduit.domain.users.user import User
from conduit.shared.application.errors import ApplicationError, Errors
from conduit.shared.application.unit_of_work import UnitOfWorkFactory


@final
class LoginUserUseCase:
    def __init__(
        self,
        uow_factory: UnitOfWorkFactory,
        login_service: LoginService,
    ):
        self._uow_factory = uow_factory
        self._login_service = login_service

    async def __call__(
        self,
        login_details: LoginUserCommand,
    ) -> Result[User, ApplicationError]:
        async with self._uow_factory():
            user = await self._login_service.login(
                login_details.email,
                login_details.password,
            )
            return maybe_to_result(user).alt(self._map_service_error)

    def _map_service_error(self, _: None) -> ApplicationError:
        return Errors.invalid_credentials()
